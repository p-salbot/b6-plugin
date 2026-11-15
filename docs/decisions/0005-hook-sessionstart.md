# 0005 Plugin má hook `SessionStart`, ktorý iba vypíše pripomienku načítať `b6:workflow`

Dátum: 2026-11-15

## Rozhodnutie

`b6/hooks/hooks.json` obsahuje iba hook `SessionStart` s jedným príkazom `echo`: pred vytvorením, zmenou alebo zmazaním
súboru projektu načítaj skill `b6:workflow`. Hook nepresmerováva výstup, nejde na sieť a nič nezapisuje (stráži K11).
Popis skillu `workflow` je zároveň sprísnený (aj pri malej zmene, aj keď správa obsahuje „go“). Plugin tým prestal byť
iba textom bez kódu za behu.

## Dôvod

V scenároch S2 a S3 sa `workflow` v novom projekte pri krátkom príkaze nespustil a Claude hneď staval. Samotný popis
skillu nestačí, aby sa načítal vždy; jedna veta na začiatku každej session je najmenší zásah, ktorý nemení posúdenie
prístupov ani dát.

## Zvažovaná alternatíva

- Iba sprísnený popis `workflow` bez hooku: zamietnuté, lebo v S2 a S3 popis skillu sám nestačil; popis sa sprísnil
  a hook sa pridal spolu.

## Čo by ho zmenilo

Ak opakovaný beh S2 a S3 ukáže, že hook nepomáha, alebo ak Claude Code začne skilly spoľahlivo načítať bez neho.
