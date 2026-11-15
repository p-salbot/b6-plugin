# 0008 Brainstorming končí požiadavkami s hlavičkou Zámer a Mimo rozsahu; návrhový dokument je iba pracovný

Dátum: 2026-11-14

## Rozhodnutie

Výsledok brainstormingu, ktorý ostáva, sú riadky v `ctx/requirements.md` s jednou hlavičkou na projekt (`Zámer`,
`Mimo rozsahu`), prípadné záznamy rozhodnutí v `docs/decisions/` a otvorené otázky v `ctx/TASKS.md`. Návrh
`ctx/plans/<dátum>-<slug>-design.md` sa schvaľuje spolu s požiadavkami, slúži plánu a briefom a pri uzavretí sa zmaže
spolu s plánom. Plán nie je pamäť projektu.

## Dôvod

Návrhový dokument po stavbe zastará, požiadavky a rozhodnutia ostávajú platné. Hlavička zachová „prečo“ a „čo nie“
bez toho, aby vznikal ďalší trvalý dokument. Rovnaké súbory opisuje sprievodca „Project memory“.

## Zvažovaná alternatíva

- Trvalý návrhový dokument a plán ako v superpowers: zamietnuté, lebo zastarajú a odporujú si s kódom.
- Iba riadky požiadaviek bez hlavičky: zamietnuté, lebo by sa stratil zámer a hranica rozsahu.

## Čo by ho zmenilo

Ak by sa ukázalo, že po zmazaní návrhu chýbajú informácie, ktoré nie sú ani v požiadavkách, ani v rozhodnutiach, ani
v architektúre.
