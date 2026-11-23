"""Statická kontrola pluginu b6 (K1-K13).

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
SPRIEVODCA_SKILLY = DOCS / "skills-as-personal-and-company-knowledge.html"
SPRIEVODCA_START = DOCS / "getting-started.html"
SPRIEVODCA_KDE = DOCS / "what-loads-when.html"
SPRIEVODCOVIA_TITLE = [(SPRIEVODCA, "Project memory"), (SPRIEVODCA_SKILLY, "Skills as company knowledge"),
                       (SPRIEVODCA_START, "Getting started with b6"), (SPRIEVODCA_KDE, "What loads when"),
                       (DOCS / "cowork-vs-claude-code.html", "Cowork and Claude Code")]
TEMPLATES = PLUGIN / "skills" / "workflow" / "references" / "templates.md"
HOOKS = PLUGIN / "hooks" / "hooks.json"

SKILLY = ["workflow", "brainstorming", "plan", "build", "wrap-up", "lessons"]
AGENTI = ["worker", "reviewer"]
MAX_RIADKOV_SKILLU = 80
MAX_ZNAKOV_POPISU = 1024

ZAKAZANE_SLOVA = ["pracovnik", "recenzent", "orchestrator", "SUHRN", "zadania", "fable"]
SLOVENSKA_DIAKRITIKA = "áäčďéíĺľňóôŕšťúýž"

STAVY_EN = ["proposed", "approved", "met", "partly met", "cancelled"]
STAVY_SK = ["návrh", "schválená", "splnená", "čiastočne splnená", "zrušená"]
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
                    "SUMMARY.md", "brief", "review", "CLAUDE.md lines", "Language", "lessons", "b6-lessons.md",
                    "CLAUDE.md lessons"]


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
    """K1: plugin.json je platný JSON s názvom b6, verziou 0.3.0, popisom a autorom Panthea s.r.o."""
    try:
        d = json.loads(cti(PLUGIN / ".claude-plugin" / "plugin.json"))
    except (OSError, ValueError) as e:
        return f"plugin.json sa nedá načítať: {e}"
    chyby = []
    if d.get("name") != "b6":
        chyby.append("name != b6")
    if d.get("version") != "0.3.0":
        chyby.append("version != 0.3.0")
    if not str(d.get("description", "")).strip():
        chyby.append("prázdny description")
    if d.get("author", {}).get("name") != "Panthea s.r.o.":
        chyby.append("author.name != Panthea s.r.o.")
    return "; ".join(chyby)


def k2():
    """K2: všetky súbory pluginu existujú (6 skillov, šablóny, modely, 2 agenti, README, LICENSE, NOTICE, sprievodcovia, hook)."""
    cesty = [PLUGIN / "skills" / s / "SKILL.md" for s in SKILLY]
    cesty += [TEMPLATES, PLUGIN / "skills" / "workflow" / "references" / "models.md"]
    cesty += [PLUGIN / "agents" / f"{a}.md" for a in AGENTI]
    cesty += [PLUGIN / n for n in ("README.md", "LICENSE", "NOTICE")] + [SPRIEVODCA, SPRIEVODCA_SKILLY, SPRIEVODCA_START, SPRIEVODCA_KDE, HOOKS]
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
    """K8: sprievodca má hlavičku Intent/Zámer a neobsahuje cesty zo starého balíka."""
    if not SPRIEVODCA.is_file():
        return "sprievodca chýba"
    text = cti(SPRIEVODCA)
    chyby = [f"chýba '{s}'" for s in ("Intent", "Out of scope", "Zámer", "Mimo rozsahu")
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
ZAKAZANE_SLOVA_BEZ_VELKOSTI = ("fable",)


def k10():
    """K10: všetci sprievodcovia v SPRIEVODCOVIA_TITLE majú obe jazykové časti, správny title a neobsahujú názvy klienta ani metodiky."""
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


# Hook smie iba vypísať text: nič nečíta zo siete, nezapisuje, nemaže a nespúšťa ďalšie príkazy.
ZAKAZANE_V_HOOKU = (">", "<", "|", "&", ";", "`", "$(", "curl", "wget", "rm ", "del ", "invoke-", "iwr", "irm",
                    "python", "node", "powershell", "pwsh", "bash", "sh -", "http")


def k11():
    """K11: plugin má iba hook SessionStart a jeho príkaz je jeden echo bez presmerovania, siete a zápisu."""
    if not HOOKS.is_file():
        return "hooks.json chýba"
    try:
        data = json.loads(cti(HOOKS))
    except ValueError as e:
        return f"hooks.json nie je platný JSON: {e}"
    udalosti = sorted(data.get("hooks", {}))
    if udalosti != ["SessionStart"]:
        return f"povolený je iba SessionStart, je: {udalosti}"
    chyby = []
    for skupina in data["hooks"]["SessionStart"]:
        for hook in skupina.get("hooks", []):
            prikaz = hook.get("command", "")
            if hook.get("type") != "command" or not prikaz.startswith("echo ") or "args" in hook:
                chyby.append(f"hook nie je jednoduchý echo: {prikaz[:40]}")
            chyby += [f"hook obsahuje '{z}'" for z in ZAKAZANE_V_HOOKU if z in prikaz.lower()]
            chyby += [f"hook obsahuje úvodzovky alebo zátvorky" for z in "'\"()" if z in prikaz][:1]
    return "; ".join(chyby)


AGENT_REVIEWER = PLUGIN / "agents" / "reviewer.md"
SKILL_BUILD = PLUGIN / "skills" / "build" / "SKILL.md"
SKILL_WORKFLOW = PLUGIN / "skills" / "workflow" / "SKILL.md"
ZASTARANE_FRAZY = ("ready to try", "na vyskúšanie", "Try R-")


def sekcia_sablony(text, nazov):
    """Text sekcie `## <názov>` v templates.md po ďalší nadpis druhej úrovne mimo blokov ```."""
    out = []
    v_sekcii = v_bloku = False
    for riadok in text.splitlines():
        if riadok.lstrip().startswith("```"):
            v_bloku = not v_bloku
        elif not v_bloku and riadok.startswith("## "):
            if v_sekcii:
                break
            v_sekcii = riadok[3:].strip() == nazov
            continue
        if v_sekcii:
            out.append(riadok)
    return "\n".join(out)


def obsahuje_cesta(cesta, slova):
    """Ako `obsahuje`, ale hlásenie uvádza cestu voči b6/ (ako K2)."""
    meno = str(cesta.relative_to(PLUGIN)) if PLUGIN in cesta.parents else cesta.name
    return [m.replace(cesta.name + ":", meno + ":", 1) for m in obsahuje(cesta, slova)]


def k12():
    """K12: súlad s požiadavkami R-025, R-026, R-028, R-030 a R-031 (nálezy z predchádzajúcich recenzií, nedá sa overiť,
    sprievodca kedy sa čo načíta, žiadne zastarané frázy, jazyk dokumentov)."""
    chyby = []
    sablony = cti(TEMPLATES) if TEMPLATES.is_file() else ""
    sekcia_review = sekcia_sablony(sablony, "review")
    # R-025
    chyby += [f"R-025: {m}" for m in obsahuje_cesta(AGENT_REVIEWER, ["Earlier findings"])]
    if "Earlier findings" not in sekcia_review:
        chyby.append("R-025: sekcia review v templates.md neobsahuje 'Earlier findings'")
    chyby += [f"R-025: {m}" for m in obsahuje_cesta(SKILL_BUILD, ["earlier `review-"])]
    # R-026
    for cesta in (AGENT_REVIEWER, TEMPLATES, SKILL_BUILD):
        chyby += [f"R-026: {m}" for m in obsahuje_cesta(cesta, ["cannot verify"])]
    # R-028
    if not SPRIEVODCA_KDE.is_file():
        chyby.append("R-028: docs/what-loads-when.html chýba")
    for cesta in (PLUGIN / "README.md", SKILL_WORKFLOW):
        chyby += [f"R-028: {m}" for m in obsahuje_cesta(cesta, ["what-loads-when"])]
    # R-030: všetky textové súbory v b6/ vrátane docs/ (aj vygenerované kópie sprievodcov *.sk.md, *.en.md); binárne (.pdf) sa preskakujú.
    for c in sorted(PLUGIN.rglob("*")):
        if not c.is_file() or c.suffix == ".pdf":
            continue
        try:
            text = cti(c)
        except (OSError, UnicodeDecodeError):
            continue
        chyby += [f"R-030: {c.relative_to(PLUGIN)} obsahuje '{f}'" for f in ZASTARANE_FRAZY if f.lower() in text.lower()]
    # R-031
    chyby += [f"R-031: {m}" for m in obsahuje_cesta(PLUGIN / "skills" / "brainstorming" / "SKILL.md", ["always ask which language"])]
    chyby += [f"R-031: {m}" for m in obsahuje_cesta(PLUGIN / "skills" / "plan" / "SKILL.md", ["document language written in `CLAUDE.md`"])]
    return "; ".join(chyby)


SKILL_LESSONS = PLUGIN / "skills" / "lessons" / "SKILL.md"
SKILL_WRAPUP = PLUGIN / "skills" / "wrap-up" / "SKILL.md"


def k13():
    """K13: súlad s požiadavkami R-035 až R-039 (poučenia: krok 5a vo wrap-up, podmienky a limit, zápis do CLAUDE.md,
    metodické poučenia v ctx/b6-lessons.md, jazykový riadok v šablónach)."""
    chyby = []
    # R-035: wrap-up má nadpis 5a pred nadpisom kroku 6 a volá skill lessons
    chyby += [f"R-035: {m}" for m in obsahuje_cesta(SKILL_WRAPUP, ["## 5a. Lessons", "`lessons`"])]
    if SKILL_WRAPUP.is_file():
        nadpisy = [r_ for r_ in cti(SKILL_WRAPUP).splitlines() if r_.startswith("## ")]
        i5a = next((i for i, r_ in enumerate(nadpisy) if r_.startswith("## 5a.")), None)
        i6 = next((i for i, r_ in enumerate(nadpisy) if r_.startswith("## 6.")), None)
        if i5a is None or i6 is None or i5a > i6:
            chyby.append("R-035: '## 5a. Lessons' nie je pred '## 6.' vo wrap-up/SKILL.md")
    # R-036 až R-038
    chyby += [f"R-036: {m}" for m in obsahuje_cesta(SKILL_LESSONS, ["all four conditions", "At most 2", "Zero lessons", "b6:reviewer"])]
    chyby += [f"R-037: {m}" for m in obsahuje_cesta(SKILL_LESSONS, ["## Lessons", "at most 10 lines", "Only after a yes"])]
    chyby += [f"R-038: {m}" for m in obsahuje_cesta(SKILL_LESSONS, ["ctx/b6-lessons.md", "Send nothing yourself"])]
    # R-039: riadok v tabuľke Language
    if ["## Lessons", "## Poučenia"] not in bunky_markdownu(sekcia_sablony(cti(TEMPLATES), "Language")):
        chyby.append("R-039: v sekcii Language v templates.md chýba riadok '| ## Lessons | ## Poučenia |'")
    return "; ".join(chyby)


KONTROLY = [("K1", k1), ("K2", k2), ("K3", k3), ("K4", k4), ("K5", k5), ("K6", k6), ("K7", k7), ("K8", k8),
            ("K9", k9), ("K10", k10), ("K11", k11), ("K12", k12), ("K13", k13)]


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
