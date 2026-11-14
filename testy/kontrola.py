"""Statická kontrola pluginu b6 (K1-K10).

Spustenie: python3 -I testy/kontrola.py   (Windows: py -3 -I testy/kontrola.py)
Výstup: riadok "OK K<n>" alebo "FAIL K<n>: <dôvod>"; exit 0 iba ak je všetko OK.
"""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
PLUGIN = KOREN / "b6"
DOCS = PLUGIN / "docs"
SPRIEVODCA = DOCS / "project-memory.html"
SPRIEVODCA_SKILLY = DOCS / "skills-as-company-knowledge.html"
SPRIEVODCA_START = DOCS / "getting-started.html"
SPRIEVODCOVIA_TITLE = [(SPRIEVODCA, "Project memory"), (SPRIEVODCA_SKILLY, "Skills as company knowledge"),
                       (SPRIEVODCA_START, "Getting started with b6")]
TEMPLATES = PLUGIN / "skills" / "workflow" / "references" / "templates.md"

SKILLY = ["workflow", "brainstorming", "plan", "build", "wrap-up"]
AGENTI = ["worker", "reviewer"]
MAX_RIADKOV_SKILLU = 80
MAX_ZNAKOV_POPISU = 1024

ZAKAZANE_SLOVA = ["pracovnik", "recenzent", "orchestrator", "SUHRN", "zadania", "fable"]
SLOVENSKA_DIAKRITIKA = "áäčďéíĺľňóôŕšťúýž"

STAVY_EN = ["proposed", "approved", "ready to try", "met", "partly met", "cancelled"]
STAVY_SK = ["návrh", "schválená", "na vyskúšanie", "splnená", "čiastočne splnená", "zrušená"]
STLPCE_POZIADAVIEK_EN = ["ID", "Priority", "Requirement", "Source", "Acceptance criterion", "Status", "Evidence"]
STLPCE_POZIADAVIEK_SK = ["ID", "Priorita", "Požiadavka", "Zdroj", "Kritérium splnenia", "Stav", "Dôkaz"]
STLPCE_ULOH_EN = ["Task", "Who acts", "What blocks it", "Inputs", "Next step"]
STLPCE_ULOH_SK = ["Úloha", "Kto koná", "Čo ju blokuje", "Vstupy", "Ďalší krok"]
RIADOK_STAVU_EN = "**Status <date>:**"
RIADOK_STAVU_SK = "**Stav <dátum>:**"
HLAVICKA_EN = ["## Intent", "## Out of scope"]
HLAVICKA_SK = ["## Zámer", "## Mimo rozsahu"]
STLPCE_ARCHITEKTURY_EN = ["Section", "What holds today", "What it means for changes", "Why"]
STLPCE_ARCHITEKTURY_SK = ["Kapitola", "Čo dnes platí", "Čo z toho vyplýva pre zmeny", "Prečo"]
POLIA_ROZHODNUTIA_EN = ["Decision", "Reason", "Alternative considered", "What would change it"]
POLIA_ROZHODNUTIA_SK = ["Rozhodnutie", "Dôvod", "Zvažovaná alternatíva", "Čo by ho zmenilo"]
HODNOTY_EN = (STAVY_EN + STLPCE_POZIADAVIEK_EN + STLPCE_ULOH_EN + STLPCE_ARCHITEKTURY_EN + POLIA_ROZHODNUTIA_EN
              + [RIADOK_STAVU_EN] + HLAVICKA_EN)
HODNOTY_SK = (STAVY_SK + STLPCE_POZIADAVIEK_SK + STLPCE_ULOH_SK + STLPCE_ARCHITEKTURY_SK + POLIA_ROZHODNUTIA_SK
              + [RIADOK_STAVU_SK] + HLAVICKA_SK)
# Hlavičky tabuliek, ktoré musia byť v šablónach presne (poradie aj znenie).
HLAVICKY_TABULIEK_EN = [STLPCE_POZIADAVIEK_EN, STLPCE_ULOH_EN, STLPCE_ARCHITEKTURY_EN]
HLAVICKY_TABULIEK_SK = [STLPCE_POZIADAVIEK_SK, STLPCE_ULOH_SK, STLPCE_ARCHITEKTURY_SK, POLIA_ROZHODNUTIA_SK]
NADPISY_ROZHODNUTIA_EN = ["## " + p for p in POLIA_ROZHODNUTIA_EN]

SEKCIE_TEMPLATES = ["requirements.md", "TASKS.md", "architecture.md", "decision record", "design", "plan",
                    "SUMMARY.md", "brief", "review", "CLAUDE.md lines", "Language"]


def cti(cesta):
    return cesta.read_text(encoding="utf-8")


def hlavicka(cesta):
    """Vráti slovník z YAML hlavičky (---) alebo None; zvláda `kľúč: hodnota`, blokové `>` a `|` a zoznamy `- x`
    (zoznam sa spojí čiarkami, blokový text medzerami)."""
    text = cti(cesta)
    m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None
    out = {}
    kluc = None
    casti = []
    for riadok in m.group(1).splitlines():
        if riadok.strip() and not riadok.startswith((" ", "\t", "-")) and ":" in riadok:
            if kluc is not None:
                out[kluc] = zloz_hodnotu(casti)
            kluc, hodnota = riadok.split(":", 1)
            kluc = kluc.strip()
            hodnota = hodnota.strip()
            casti = [] if hodnota in (">", "|", ">-", "|-", "") else [hodnota.strip("\"'")]
        elif kluc is not None and riadok.strip():
            casti.append(riadok.strip().lstrip("-").strip().strip("\"'"))
    if kluc is not None:
        out[kluc] = zloz_hodnotu(casti)
    return out


def zloz_hodnotu(casti):
    """Spojí pokračovacie riadky hodnoty hlavičky do jedného reťazca."""
    return ", ".join(casti) if len(casti) > 1 and all(len(c.split()) == 1 for c in casti) else " ".join(casti)


def casti_sprievodcu():
    """Rozdelí sprievodcu na slovenskú a anglickú časť podľa <div id="lang-sk"> a <div id="lang-en">
    (tak je postavený aj ../Pamäť projektu.html). Vráti (sk, en) alebo None, ak značky chýbajú."""
    zdroj = re.sub(r"<!--.*?-->", "", cti(SPRIEVODCA), flags=re.S)
    i_sk = zdroj.find('id="lang-sk"')
    i_en = zdroj.find('id="lang-en"')
    if i_sk < 0 or i_en < 0 or i_en < i_sk:
        return None
    i_skript = zdroj.find("<script", i_en)
    return zdroj[i_sk:i_en], zdroj[i_en:i_skript if i_skript > 0 else len(zdroj)]


class ZberPrvkov(HTMLParser):
    """Zbiera celý viditeľný text každého prvku td/th/span/code/strong/li (html.unescape robí parser) a hlavičky
    tabuliek (zoznam th pre každú tabuľku)."""
    PRVKY = ("td", "th", "span", "code", "strong", "li")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.texty = set()
        self.hlavicky = []
        self._zasobnik = []
        self._tabulka = []

    def handle_starttag(self, tag, attrs):
        if tag in self.PRVKY:
            self._zasobnik.append((tag, []))

    def handle_data(self, data):
        for _, kusy in self._zasobnik:
            kusy.append(data)

    def handle_endtag(self, tag):
        for i in range(len(self._zasobnik) - 1, -1, -1):
            if self._zasobnik[i][0] == tag:
                text = " ".join("".join(self._zasobnik[i][1]).split())
                del self._zasobnik[i:]
                if text:
                    self.texty.add(text)
                    if tag == "th":
                        self._tabulka.append(text)
                break
        if tag == "thead" and self._tabulka:
            self.hlavicky.append(self._tabulka)
            self._tabulka = []


def prvky_html(cast):
    """Vráti (množina textov prvkov, zoznam hlavičiek tabuliek) pre kus HTML."""
    zber = ZberPrvkov()
    zber.feed(cast)
    return zber.texty, zber.hlavicky


def bunky_markdownu(text):
    """Vráti zoznam riadkov tabuliek v Markdown (každý ako zoznam buniek bez okrajových rúr)."""
    riadky = []
    for r_ in text.splitlines():
        if r_.lstrip().startswith("|"):
            riadky.append([b.strip() for b in r_.strip().strip("|").split("|")])
    return riadky


def obsahuje_postupnost(zoznam, hladane):
    """True, ak sa `hladane` nachádza v `zoznam` ako súvislá podpostupnosť."""
    n = len(hladane)
    return any(zoznam[i:i + n] == hladane for i in range(len(zoznam) - n + 1))


def k1():
    """K1: plugin.json je platný JSON s názvom b6, verziou 0.1.0, popisom a autorom Panthea s.r.o."""
    try:
        d = json.loads(cti(PLUGIN / ".claude-plugin" / "plugin.json"))
    except (OSError, ValueError) as e:
        return f"plugin.json sa nedá načítať: {e}"
    chyby = []
    if d.get("name") != "b6":
        chyby.append("name != b6")
    if d.get("version") != "0.1.0":
        chyby.append("version != 0.1.0")
    if not str(d.get("description", "")).strip():
        chyby.append("prázdny description")
    if d.get("author", {}).get("name") != "Panthea s.r.o.":
        chyby.append("author.name != Panthea s.r.o.")
    return "; ".join(chyby)


def k2():
    """K2: všetky súbory pluginu existujú (5 skillov, šablóny, modely, 2 agenti, README, LICENSE, NOTICE, sprievodca)."""
    cesty = [PLUGIN / "skills" / s / "SKILL.md" for s in SKILLY]
    cesty += [TEMPLATES, PLUGIN / "skills" / "workflow" / "references" / "models.md"]
    cesty += [PLUGIN / "agents" / f"{a}.md" for a in AGENTI]
    cesty += [PLUGIN / n for n in ("README.md", "LICENSE", "NOTICE")] + [SPRIEVODCA, SPRIEVODCA_SKILLY, SPRIEVODCA_START]
    chybajuce = [str(c.relative_to(PLUGIN)) for c in cesty if not c.is_file()]
    return "chýbajú: " + ", ".join(chybajuce) if chybajuce else ""


def k3():
    """K3: skilly a agenti majú hlavičku s name a neprázdnym description do 1024 znakov; SKILL.md má najviac 80 riadkov."""
    chyby = []
    cesty = [(s, PLUGIN / "skills" / s / "SKILL.md") for s in SKILLY]
    cesty += [(a, PLUGIN / "agents" / f"{a}.md") for a in AGENTI]
    for nazov, cesta in cesty:
        if not cesta.is_file():
            chyby.append(f"{nazov}: súbor chýba")
            continue
        h = hlavicka(cesta)
        if h is None:
            chyby.append(f"{nazov}: chýba hlavička")
            continue
        if h.get("name") != nazov:
            chyby.append(f"{nazov}: name='{h.get('name')}'")
        popis = h.get("description", "")
        if not popis or len(popis) > MAX_ZNAKOV_POPISU:
            chyby.append(f"{nazov}: description prázdny alebo dlhší než {MAX_ZNAKOV_POPISU}")
        if cesta.name == "SKILL.md" and len(cti(cesta).splitlines()) > MAX_RIADKOV_SKILLU:
            chyby.append(f"{nazov}: SKILL.md dlhší než {MAX_RIADKOV_SKILLU} riadkov")
    return "; ".join(chyby)


def subory_pluginu():
    """Textové súbory v b6/ mimo docs/."""
    for c in sorted(PLUGIN.rglob("*")):
        if c.is_file() and DOCS not in c.parents and c.name != ".DS_Store":
            yield c


def k4():
    """K4: v plugine (mimo docs/) nie sú zakázané slová a slovenská diakritika (okrem templates.md a riadku description:)."""
    chyby = []
    for c in subory_pluginu():
        try:
            text = cti(c)
        except UnicodeDecodeError:
            continue
        nizke = text.lower()
        meno = str(c.relative_to(PLUGIN))
        for slovo in ZAKAZANE_SLOVA:
            if slovo.lower() in nizke:
                chyby.append(f"{meno}: zakázané slovo '{slovo}'")
        if c != TEMPLATES:
            # Diakritika je povolená iba v riadku `description:` hlavičky (slovenské spúšťacie slová).
            bez_popisu = "\n".join(r for r in text.splitlines() if not r.startswith("description:"))
            znaky = sorted({z for z in bez_popisu if z.lower() in SLOVENSKA_DIAKRITIKA})
            if znaky:
                chyby.append(f"{meno}: slovenská diakritika ({''.join(znaky)})")
    return "; ".join(chyby)


def stavy_zo_vety(texty, uvod):
    """Vráti množinu stavov z vety `<uvod>: a → b → c / d; e.` (prvok li, ktorý začína na `uvod`)."""
    for text in texty:
        if text.startswith(uvod + ":"):
            return {s.strip(" .") for s in re.split(r"[→/;]", text.split(":", 1)[1])}
    return set()


def chyby_sablon():
    """Chyby v templates.md: hlavičky tabuliek presne, celé hodnoty v tabuľke Language, nadpisy záznamu rozhodnutia."""
    text = cti(TEMPLATES)
    riadky = bunky_markdownu(text)
    bunky = {b for r_ in riadky for b in r_}
    chyby = [f"templates.md: chýba riadok hlavičky '| {' | '.join(h)} |'" for h in HLAVICKY_TABULIEK_EN
             if h not in riadky]
    # hlavičky a riadok stavu sú v tabuľke Language ako celá bunka; EN stĺpce sú aj v hlavičkách tabuliek
    chyby += [f"templates.md: v tabuľke Language chýba '{h}'" for h in HODNOTY_EN + HODNOTY_SK if h not in bunky]
    chyby += [f"templates.md: chýba nadpis '{n}'" for n in NADPISY_ROZHODNUTIA_EN if n not in text.splitlines()]
    return chyby


def chyby_sprievodcu(nazov, cast, hodnoty, hlavicky, uvod_stavov, stavy):
    """Chyby v jednej jazykovej časti sprievodcu: hlavičky tabuliek, riadok stavu, nadpisy a veta so stavmi."""
    texty, th = prvky_html(cast)
    chyby = [f"sprievodca {nazov}: chýba tabuľka s hlavičkou {h}" for h in hlavicky
             if not any(obsahuje_postupnost(zoznam, h) for zoznam in th)]
    celé = [h for h in hodnoty if h not in stavy]
    chyby += [f"sprievodca {nazov}: chýba '{h}'" for h in celé if h not in texty]
    chyby += [f"sprievodca {nazov}: vo vete '{uvod_stavov}' chýba stav '{s}'"
              for s in stavy if s not in stavy_zo_vety(texty, uvod_stavov)]
    return chyby


def k5():
    """K5 (plán, vlna 3): šablóny a sprievodca používajú rovnaké stavy, stĺpce a hlavičky; porovnávajú sa celé hodnoty
    (bunky tabuliek, celé texty prvkov), nie podreťazce."""
    if not TEMPLATES.is_file() or not SPRIEVODCA.is_file():
        return "chýba templates.md alebo sprievodca"
    chyby = chyby_sablon()
    casti = casti_sprievodcu()
    if casti is None:
        return "; ".join(chyby + ["sprievodca: chýbajú bloky id=lang-sk / id=lang-en"])
    chyby += chyby_sprievodcu("SK", casti[0], HODNOTY_SK, HLAVICKY_TABULIEK_SK, "Stavy", STAVY_SK)
    chyby += chyby_sprievodcu("EN", casti[1], HODNOTY_EN, HLAVICKY_TABULIEK_EN, "Statuses", STAVY_EN)
    return "; ".join(chyby)


def k6():
    """K6: worker beží na modeli sonnet, reviewer na opus a reviewer nemá nástroj Edit."""
    chyby = []
    for agent, model in (("worker", "sonnet"), ("reviewer", "opus")):
        cesta = PLUGIN / "agents" / f"{agent}.md"
        h = hlavicka(cesta) if cesta.is_file() else None
        if h is None:
            chyby.append(f"{agent}: chýba súbor alebo hlavička")
            continue
        if h.get("model") != model:
            chyby.append(f"{agent}: model='{h.get('model')}', čakané {model}")
        if agent == "reviewer":
            nastroje = set(re.findall(r"[A-Za-z]+", h.get("tools", "")))
            if not nastroje:
                chyby.append("reviewer: tools je prázdne alebo sa nedá prečítať")
            if nastroje & {"Edit", "MultiEdit"}:
                chyby.append("reviewer: tools obsahuje Edit")
    return "; ".join(chyby)


def obsahuje(cesta, slova):
    if not cesta.is_file():
        return [f"{cesta.name}: súbor chýba"]
    text = cti(cesta)
    return [f"{cesta.name}: chýba '{s}'" for s in slova if s not in text]


def k7():
    """K7: NOTICE uvádza Jesse Vincent a MIT, LICENSE uvádza Panthea s.r.o."""
    chyby = obsahuje(PLUGIN / "NOTICE", ["Jesse Vincent", "MIT"])
    return "; ".join(chyby + obsahuje(PLUGIN / "LICENSE", ["Panthea s.r.o."]))


def k8():
    """K8: sprievodca má hlavičku Intent/Zámer a stav ready to try, a neobsahuje cesty zo starého balíka."""
    if not SPRIEVODCA.is_file():
        return "sprievodca chýba"
    text = cti(SPRIEVODCA)
    chyby = [f"chýba '{s}'" for s in ("Intent", "Out of scope", "Zámer", "Mimo rozsahu", "ready to try", "na vyskúšanie")
             if s not in text]
    chyby += [f"obsahuje '{s}'" for s in ("ctx/plans", "-design.md") if s in text]
    return "; ".join(chyby)


def nadpisy_mimo_kodu(text):
    """Vráti názvy nadpisov druhej úrovne (`## názov`) mimo ohradených blokov ```."""
    nazvy = []
    v_bloku = False
    for riadok in text.splitlines():
        if riadok.lstrip().startswith("```"):
            v_bloku = not v_bloku
        elif not v_bloku and riadok.startswith("## "):
            nazvy.append(riadok[3:].strip())
    return nazvy


def k9():
    """K9 (plán, vlna 3): templates.md má všetky sekcie ako presné nadpisy `## <názov>` mimo blokov kódu."""
    if not TEMPLATES.is_file():
        return "templates.md chýba"
    nadpisy = nadpisy_mimo_kodu(cti(TEMPLATES))
    chyba = [s for s in SEKCIE_TEMPLATES if s not in nadpisy]
    return "chýbajú sekcie: " + ", ".join(chyba) if chyba else ""


# B6 iba veľkými písmenami: malé b6 je názov pluginu.
ZAKAZANE_SLOVA_VELKE = ("B6",)
ZAKAZANE_SLOVA_BEZ_VELKOSTI = ("strix", "ps-metodika", "fable")


def k10():
    """K10: všetci traja sprievodcovia majú obe jazykové časti, správny title a neobsahujú názvy klienta ani metodiky."""
    chyby = []
    for cesta, title in SPRIEVODCOVIA_TITLE:
        meno = cesta.name
        if not cesta.is_file():
            chyby.append(f"{meno}: chýba")
            continue
        text = cti(cesta)
        chyby += [f"{meno}: chýba '{s}'" for s in ('id="lang-sk"', 'id="lang-en"', f"<title>{title}</title>")
                  if s not in text]
        chyby += [f"{meno}: obsahuje '{s}'" for s in ZAKAZANE_SLOVA_VELKE
                  if re.search(rf"(?<![A-Za-z0-9]){re.escape(s)}(?![A-Za-z0-9])", text)]
        chyby += [f"{meno}: obsahuje '{s}'" for s in ZAKAZANE_SLOVA_BEZ_VELKOSTI
                  if re.search(rf"(?<![A-Za-z0-9]){re.escape(s)}(?![A-Za-z0-9])", text, re.IGNORECASE)]
    return "; ".join(chyby)


KONTROLY = [("K1", k1), ("K2", k2), ("K3", k3), ("K4", k4), ("K5", k5), ("K6", k6), ("K7", k7), ("K8", k8),
            ("K9", k9), ("K10", k10)]


def main():
    zlyhalo = False
    for id_, funkcia in KONTROLY:
        dovod = funkcia()
        if dovod:
            zlyhalo = True
            print(f"FAIL {id_}: {dovod}")
        else:
            print(f"OK {id_}")
    return 1 if zlyhalo else 0


if __name__ == "__main__":
    sys.exit(main())
