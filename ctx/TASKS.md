# Úlohy

**Stav 2026-11-16:** Plugin 0.1.0 je postavený vrátane plánu `2026-11-15-z-orchestracie` (R-025 až R-031) a opráv
z behu 2; `testy/kontrola.py` K1–K12 OK; opakované behy S3, S4, S6, S8, S9 (Windows, bez sandboxu, 2026-11-16) vyhodnotené
v `review-24.md` až `review-34.md`. Požiadavky so scenárovým alebo recenzným dôkazom sú `splnená`, R-029 `čiastočne
splnená`. Zostáva: rozhodnutie o medzere R-029, overenie R-005 (S5), R-003, R-011, R-015, R-016 a R-024 bez nového
dôkazu, úpravy testov, zmena dokumentácie od Petra a odovzdanie zipu iba z `b6/`.

| Úloha | Kto koná | Čo ju blokuje | Vstupy | Ďalší krok |
|---|---|---|---|---|
| Push walkthrough a ukážkového projektu (R-032 až R-034, commit lokálne) na verejný GitHub | Peter | pokyn Petra | lokálny commit | Peter povie „push“ |
| Medzera R-029: druhé prepisy zložených príkazov, nepresné zoznamy odmietnutí, „skipped“ prijaté bez otázky vlastníkovi; cesta „May I run it?“ neoverená (spúšťač je neinteraktívny) | Peter rozhodne, `worker` upraví | rozhodnutie Petra | `ctx/plans/2026-11-15-z-orchestracie/review-34.md` (nálezy 1–4) | Peter rozhodne, či medzeru opraviť ďalšou zmenou cez `workflow`, alebo ju ponechať |
| Požiadavky bez nového dôkazu: R-003, R-015, R-016 (iba S2, S10, S1 z 2026-11-15), R-024 (bez dôkazu); R-011 je v rozpore s R-031 („iba potvrdí“ vs. „vždy sa opýta“) | Peter rozhodne, Claude upraví | rozhodnutie Petra | `testy/vysledky/suhrn-0.1.0-beh2.md`, `ctx/plans/2026-11-15-z-orchestracie/review-24.md`, `review-28.md` | Peter rozhodne: znova S1, S2, S10, alebo uznať dôkazy z 2026-11-15; R-011 preformulovať podľa R-031 a uzavrieť |
| Nápad: mapa znalostí v skilloch postavená postupom b6 – odkaz „knowledge skills“ so šablónou mapy (téma → skill/podklad → vlastník → zdroj → dátum overenia), kontrolné otázky ako kritériá, test načítania skillu podľa popisu, údržba mimo behu (vlastník, pravidelná kontrola), hranica P-05 | Peter rozhodne | rozhodnutie Petra (zatiaľ nič nerobiť) | rozhovor 2026-11-16; `b6/docs/skills-as-personal-and-company-knowledge.sk.md` kap. 6 | Ak áno, nová zmena cez `workflow` (veľkosť M) |
| `spust.py` nechá v `%TEMP%` priečinky `b6-test-*` s kópiou projektu | Claude | nič (nie je blokujúce) | `testy/spust.py` | Po skopírovaní výsledku priečinok zmazať |
| Overiť dve kolá opráv a stop (R-005): S5 sa do fázy opráv nedostal | Peter rozhodne, Claude upraví | rozhodnutie Petra | `testy/scenare.md` (S5), `testy/vysledky/suhrn-0.1.0.md` | Peter rozhodne: upraviť personu S5 tak, aby prešla k plánu a stavbe, alebo overiť inak |
| Overiť riziko `wrap-up`/`workflow`: plán s požiadavkami v rôznych stavoch (zvyšok po R-006 a R-018, ktoré sú zrušené; „not yet“ a S8 overené 2026-11-16) | Peter | nič | `stav-stavby.md` „Otvorené“ (git a0364be) | Pri ďalšom behu S4 alebo S6 sledovať tento bod |
| Overiť riziká testovacieho behu: `END` v simulátore bez ohľadu na veľkosť písmen, persony S7/S9/S11 schvaľujú aj plán, či `--setting-sources` skryje používateľské skilly, pri prerušení sa projekt neskopíruje do `vysledky/` | Claude | nič (nie je blokujúce) | `testy/spust.py`, `testy/scenare.md` | Navrhnúť Petrovi opravy `spust.py` a person; meniť až po súhlase |
| Upraviť testy po behu 2026-11-16 (`review-28.md`, `review-29.md`, `review-31.md`, `review-34.md`): persóna S8 (nemení jazyk, nevedie mimo projektu, povie „go“), persóna S4 pri otázke na povolenie, `Očakávané` S4 a S6 o odmietnutých príkazoch a zápisoch mimo kópie (kritérium R-012 je už v S4/S6), `prepis.md` bez zamietnutých príkazov; spúšťač je neinteraktívny, výzva na povolenie = zamietnutie | Claude | nič (nie je blokujúce) | `testy/scenare.md`, `testy/spust.py` | Navrhnúť Petrovi úpravy; meniť až po súhlase |
| Odovzdať plugin klientovi | Peter | nič | `b6-0.1.0.zip` (`b6/` a `.claude-plugin/marketplace.json`, zabalený 2026-11-16; inštalácia overená v čistom profile) | Poslať nový zip klientovi s postupom cez `/plugin marketplace add` |
