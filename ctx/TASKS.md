# Úlohy

**Stav 2026-11-15:** Plugin 0.1.0 je postavený a `testy/kontrola.py` K1–K11 je OK; čaká sa na opakovaný beh
scenárov po opravách, potvrdenie licencie a postup inštalácie u klienta, potom odovzdanie.

| Úloha | Kto koná | Čo ju blokuje | Vstupy | Ďalší krok |
|---|---|---|---|---|
| Znova spustiť scenáre S2, S3, S4, S6, S9 po opravách (R-002, R-003, R-008, R-009, R-012, R-018) | Peter | nič | `testy/scenare.md`, `testy/vysledky/suhrn-0.1.0.md` | Vo vlastnom termináli z koreňa repozitára `py -3 -I testy/spust.py S2` (potom S3, S4, S6, S9) |
| Zapísať výsledky opakovaného behu do súhrnu a stavy do `ctx/requirements.md` | Claude | opakovaný beh scenárov | `testy/vysledky/` | Po behu vyhodnotiť prepisy podľa `### Očakávané` v `testy/scenare.md` a navrhnúť stavy |
| Overiť dve kolá opráv a stop (R-005): S5 sa do fázy opráv nedostal | Peter rozhodne, Claude upraví | rozhodnutie Petra | `testy/scenare.md` (S5), `testy/vysledky/suhrn-0.1.0.md` | Peter rozhodne: upraviť personu S5 tak, aby prešla k plánu a stavbe, alebo overiť inak |
| Overiť riziká `wrap-up`/`workflow` (R-006, R-018): dvojitá ponuka zmazania pri úlohe „Try R-…“ a zvyškoch, plán s požiadavkami v rôznych stavoch, pri „not yet“ z `build` kroky 4–6 | Peter | nič | `stav-stavby.md` „Otvorené“ | Pri opakovanom behu S4 a S6 sledovať tieto body; S8 pustiť znova `py -3 -I testy/spust.py S8` |
| Overiť riziká testovacieho behu: `END` v simulátore bez ohľadu na veľkosť písmen, persony S7/S9/S11 schvaľujú aj plán, či `--setting-sources` skryje používateľské skilly, pri prerušení sa projekt neskopíruje do `vysledky/` | Claude | nič (nie je blokujúce) | `testy/spust.py`, `testy/scenare.md` | Navrhnúť Petrovi opravy `spust.py` a person; meniť až po súhlase |
| Potvrdiť znenie licencie (R-022) | Peter | nič | `b6/LICENSE`, `b6/README.md` | Potvrdiť podmienky (ideálne s advokátom); potom odstrániť označenie návrhu v `LICENSE` a „draft terms“ v README a spustiť `kontrola.py` |
| Zistiť postup schválenia a inštalácie pluginu u klienta (R-023) | klient (pýta sa Peter) | odpoveď klienta | `b6/README.md` „Install“ | Peter sa opýta klienta na schvaľovanie pluginov a formu balíka |
| Overiť modely a limity Team účtov klienta (R-013) | klient (pýta sa Peter) | odpoveď klienta | `b6/skills/workflow/references/models.md` | Peter sa opýta, či sú dostupné `opus` a `sonnet` a aké sú limity |
| Odovzdať plugin klientovi | Peter | licencia, postup inštalácie, opakovaný beh scenárov | `b6-0.1.0.zip` (iba z `b6/`) | Po potvrdení licencie znova zabaliť iba `b6/` a odovzdať |
