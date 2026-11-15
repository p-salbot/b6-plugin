# Úlohy

**Stav 2026-11-15:** Plugin 0.1.0 je postavený, `testy/kontrola.py` K1–K11 OK; opakovaný beh S2, S3, S4, S6, S9 (Windows,
bez sandboxu): 4 splnené, S4 čiastočne (`testy/vysledky/suhrn-0.1.0-beh2.md`). Zostávajú tri chyby pluginu, licencia,
postup inštalácie u klienta, potom odovzdanie.

| Úloha | Kto koná | Čo ju blokuje | Vstupy | Ďalší krok |
|---|---|---|---|---|
| Opraviť chyby z behu 2 (R-007, R-012): záznam rozhodnutia pri bežnom detaile (`b6/skills/brainstorming/SKILL.md:35`), `reviewer` bez pravidla pre pomocné súbory mimo projektu (`b6/agents/reviewer.md`), postup pri zablokovanom príkaze v `build` (nemeniť si povolenia, nevyberať za vlastníka) | Peter rozhodne, `worker` upraví | rozhodnutie Petra | `testy/vysledky/suhrn-0.1.0-beh2.md` | Po oprave spustiť S3, S4, S6 a S9 so stavbou, potom znova zabaliť zip iba z `b6/` |
| Overiť R-012 scenárom so stavbou: persona S9 zakazuje stavbu, `worker` sa nespustil | Claude | nič | `testy/scenare.md` (S9) | Navrhnúť Petrovi úpravu persony S9 alebo iný scenár |
| `spust.py` nechá v `%TEMP%` priečinky `b6-test-*` s kópiou projektu | Claude | nič (nie je blokujúce) | `testy/spust.py` | Po skopírovaní výsledku priečinok zmazať |
| Overiť dve kolá opráv a stop (R-005): S5 sa do fázy opráv nedostal | Peter rozhodne, Claude upraví | rozhodnutie Petra | `testy/scenare.md` (S5), `testy/vysledky/suhrn-0.1.0.md` | Peter rozhodne: upraviť personu S5 tak, aby prešla k plánu a stavbe, alebo overiť inak |
| Overiť riziká `wrap-up`/`workflow` (R-006, R-018): dvojitá ponuka zmazania pri úlohe „Try R-…“ a zvyškoch, plán s požiadavkami v rôznych stavoch, pri „not yet“ z `build` kroky 4–6 | Peter | nič | `stav-stavby.md` „Otvorené“ (git a0364be) | Pri opakovanom behu S4 a S6 sledovať tieto body; S8 pustiť znova `py -3 -I testy/spust.py S8` |
| Overiť riziká testovacieho behu: `END` v simulátore bez ohľadu na veľkosť písmen, persony S7/S9/S11 schvaľujú aj plán, či `--setting-sources` skryje používateľské skilly, pri prerušení sa projekt neskopíruje do `vysledky/` | Claude | nič (nie je blokujúce) | `testy/spust.py`, `testy/scenare.md` | Navrhnúť Petrovi opravy `spust.py` a person; meniť až po súhlase |
| Potvrdiť znenie licencie (R-022) | Peter | nič | `b6/LICENSE`, `b6/README.md` | Potvrdiť podmienky (ideálne s advokátom); potom odstrániť označenie návrhu v `LICENSE` a „draft terms“ v README a spustiť `kontrola.py` |
| Zistiť postup schválenia a inštalácie pluginu u klienta (R-023) | klient (pýta sa Peter) | odpoveď klienta | `b6/README.md` „Install“ | Peter sa opýta klienta na schvaľovanie pluginov a formu balíka |
| Overiť modely a limity Team účtov klienta (R-013) | klient (pýta sa Peter) | odpoveď klienta | `b6/skills/workflow/references/models.md` | Peter sa opýta, či sú dostupné `opus` a `sonnet` a aké sú limity |
| Odovzdať plugin klientovi | Peter | licencia, postup inštalácie, opakovaný beh scenárov | `b6-0.1.0.zip` (iba z `b6/`) | Po potvrdení licencie znova zabaliť iba `b6/` a odovzdať |
