# Požiadavky

## Zámer

Jednoduchý zoznam úloh z príkazového riadku pre jedného človeka.

## Požiadavky

| ID | Priorita | Požiadavka | Stav |
|---|---|---|---|
| R-001 | MUST | Zoznam vie ukázať iba otvorené úlohy | splnená |
| R-002 | SHOULD | Úloha sa dá označiť ako hotová | splnená |

## Rozhodnutia

- 2026-10-18: Úlohy sa ukladajú do súboru `tasks.json`, nie do databázy. Dôvod: jeden používateľ, málo údajov.
- 2026-10-19: Príkazy sú `add`, `list`, `done`. Dôvod: najmenšia použiteľná sada.
