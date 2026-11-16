*Sprievodca · plugin b6*

# Čo sa načíta kedy

Claude si v jednom chate pamätá len to, čo sa doň načítalo. Keď sa kontext zaplní, práca sa spomalí, zdražie a robí sa v nej viac chýb. Plugin b6 preto načítava veľa vecí až vtedy, keď sa naozaj použijú.

## Šesť pojmov

*Vždy*

### Kontext

Všetko, čo Claude v jednom chate drží v hlave: tvoje správy, jeho odpovede, prečítané súbory, výstupy príkazov. Rastie s každou správou; zmenší sa až pri zhustení (compact) alebo v novom chate. Plný kontext znamená pomalšiu a drahšiu prácu a viac chýb. Preto je lepšie čítať málo a až vtedy, keď to treba.

*Pri použití*

### Skill

Textový súbor s postupom. Jeho krátky popis (v hlavičke) Claude vidí vždy. Celé telo `SKILL.md` sa načíta, až keď popis sedí na tvoju požiadavku. Obyčajná otázka, ktorá nemení súbory, ho nepotrebuje; otázky o stave práce alebo o postupe („čo je rozrobené“, „kde sme“, „ako to funguje“) `workflow` načítajú.

*Pri kroku*

### Referencia

Súbor, ktorý skill otvorí iba v kroku, ktorý ho potrebuje: `templates.md` (tvary dokumentov) a `models.md` (úrovne modelov a odhad tokenov) v skille `workflow`. Pri jasnej drobnej zmene sa neotvorí vôbec.

*Vlastný kontext*

### Agent

`worker` a `reviewer`. Každý začína s čistým kontextom: nevidí chat; okrem vlastných pokynov (`agents/<meno>.md`) a `CLAUDE.md` projektu dostane len zadanie (brief). Vráti najviac 20 riadkov, takže hlavný chat sa nezaplní. Reviewer je vždy nový, nevidel prácu workera.

*Pri štarte*

### Hook SessionStart

Jeden riadok, ktorý sa vloží na začiatku chatu: plugin je aktívny a pred každou zmenou súboru sa má načítať skill `b6:workflow`. Nič iné sa tým nenačíta.

*Podľa potreby*

### Súbory projektu

`CLAUDE.md` sa načíta vždy. Priečinky `ctx/` (požiadavky, úlohy, plány) a `docs/` (architektúra, rozhodnutia) sa čítajú iba vtedy, keď ich krok potrebuje.

## Čo je v kontexte v ktorom momente

Príklad: jedna zmena veľkosti M, od štartu chatu po uzavretie. Hlavný chat je kontext, ktorý rastie. Agenti pracujú vo vlastnom kontexte a do hlavného vrátia len krátku správu.

| Moment | Pribudne do hlavného chatu | Nenačíta sa |
|---|---|---|
| Štart chatu | **vždy** `CLAUDE.md`, krátke popisy skillov a agentov, riadok z hooku SessionStart | telá skillov, referencie, `ctx/`, `docs/` |
| Zadanie zmeny | **skill** telo `workflow`, ktorý na začiatku prečíta `ctx/TASKS.md`, ak existuje; potom podľa veľkosti M skill `brainstorming` | `plan`, `build`, `wrap-up`, agenti |
| Brainstorming | **referencia** `templates.md` pri zápise požiadaviek; **súbory** `ctx/`, `docs/` a existujúci kód, ktoré sú k téme; na konci sa opýta na jazyk dokumentov a po schválení zapíše `ctx/`, `docs/` a riadky do `CLAUDE.md` podľa `templates.md` | `models.md` |
| Plán | **skill** telo `plan`; **súbory** `ctx/requirements.md` a návrh `ctx/plans/<dátum>-<slug>-design.md`; **referencie** `templates.md` a `models.md` (úrovne a odhad tokenov) | telo `build`, agenti |
| Krok stavby | **skill** telo `build`; **referencia** `templates.md` (zadanie, recenzia, `SUMMARY.md`); plán a `SUMMARY.md`; kontrolu spúšťa hlavný chat sám; od `worker` len správa (najviac 20 riadkov) | ostatné kroky; práca workera v hlavnom chate |
| Recenzia | v hlavnom chate od `reviewer` len verdikt, očíslované nálezy a cesta k súboru `review-<n>.md` | čo reviewer čítal |
| Uzavretie | **skill** telo `wrap-up`; **referencia** `templates.md`; súbory, ktoré treba aktualizovať (`ctx/requirements.md`, `ctx/TASKS.md`, `docs/architecture.md`); `review-<n>.md` a `SUMMARY.md` behu; `met` sa zapíše až po `OK` od nového recenzenta | `models.md`; agenti len keď treba opraviť architektúru alebo odkazy |

Pri malej zmene S (jeden či dva existujúce súbory) sa brainstorming, plán ani šablóny nečítajú, v `ctx/` sa nevytvárajú žiadne súbory a `ctx/TASKS.md` sa nemení. Stačí `workflow` (ten pri štarte prečíta `ctx/TASKS.md`, ak existuje), zmena cez `worker` a kontrola cez `reviewer`. Dôkaz sa zapíše do `ctx/requirements.md` iba vtedy, keď sa zmena dotýka požiadavky, ktorá tam už je.

## Čo z toho vyplýva

- Dlhý chat spomaľuje a draží. Novú úlohu začni v novom chate; pokračovanie je v `SUMMARY.md` a v `ctx/`.
- Popis skillu rozhoduje, či sa skill otvorí. Preto obsahuje slová, ktoré ľudia naozaj používajú.
- Jeden krok robí agent s čistým kontextom: nevidí chat, preto zadanie musí byť úplné.
- Do `CLAUDE.md` patrí len to, čo platí vždy. Čo platí iba pri jednej práci, patrí do skillu alebo do dokumentu v `ctx/` či `docs/`.

---

Interné · @panthea.sk
