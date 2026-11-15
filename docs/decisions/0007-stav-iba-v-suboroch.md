# 0007 Stav práce je iba v súboroch projektu, nikdy v pamäti Claude

Dátum: 2026-11-15

## Rozhodnutie

Plugin učí, že stav práce, dohody a odložené plány sa zapisujú iba do súborov projektu (`ctx/`, `docs/`), nikdy do
pamäte Claude (tvrdé pravidlo 7 vo `workflow`). Zmena S sa preto nedá odložiť: ak chce vlastník pokračovať neskôr,
prepne sa na M, aby sa dohoda zapísala do `ctx/`. Nová funkcia alebo príkaz je vždy M.

## Dôvod

V scenári S6 sa nová funkcia zaradila ako S, plán nevznikol a dohoda sa uložila do pamäte Claude mimo projektu. Pamäť
Claude nevidí vlastník ani iný človek v projekte, nie je v gite a nedá sa skontrolovať; súbory projektu áno.

## Zvažovaná alternatíva

- Povoliť pamäť Claude ako doplnok k `ctx/TASKS.md`: zamietnuté, lebo by vznikli dva zdroje stavu, ktoré sa rozídu.

## Čo by ho zmenilo

Nič predvídateľné.
