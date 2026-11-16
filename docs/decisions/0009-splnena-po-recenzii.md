# 0009 Požiadavka je splnená po verdikte OK recenzenta, bez skúšky vlastníkom

Dátum: 2026-11-15

## Rozhodnutie

Požiadavka dostane stav `met`/`splnená` po verdikte `OK` čerstvého `reviewer` s dôkazom pri každom kritériu. Vlastník ju
nemusí skúšať; `wrap-up` mu povie, čo si môže vyskúšať. Ak neskôr hlási, že to nefunguje, ide nová zmena cez `workflow`.
Nahrádza tvrdé pravidlo 4 v časti „met is written only after the owner tried it“ a požiadavky R-006 a R-018.

## Dôvod

Peter 2026-11-15 pri porovnaní s balíkom `orchestracia`, kde je práca hotová po OK recenzenta: menej krokov a čakania
na vlastníka; dôkaz zabezpečuje nezávislý `reviewer`.

## Zvažovaná alternatíva

- Ponechať `met` až po skúške vlastníkom (stav `ready to try` medzi tým): zamietnuté vlastníkom.
- Predvolene skúška vlastníkom, ktorú môže vlastník odpustiť: zamietnuté vlastníkom.

## Čo by ho zmenilo

Ak by sa ukázalo, že veci s verdiktom `OK` vlastníkom často nefungujú (opakované nové zmeny „nefunguje“ po uzavretí).
