# 0010 Poučenia pre projekt sa ukladajú do CLAUDE.md projektu

Dátum: 2026-11-19

## Rozhodnutie

Poučenie, ktoré platí pre jeden projekt, sa po súhlase vlastníka zapíše ako riadok do sekcie poučení v `CLAUDE.md`
projektu (anglicky `## Lessons`, slovensky `## Poučenia`). Sekcia má najviac 10 riadkov; keď je plná, navrhne sa
zmazanie najstaršieho alebo prekonaného riadku. Poučenie pre metódu b6 ide do `ctx/b6-lessons.md` a vlastník ho pošle
správcovi; nič sa neodosiela automaticky.

## Dôvod

`CLAUDE.md` sa načíta pri každej session, takže poučenie naozaj zaberie; zodpovedá to odporúčaniu Anthropicu dávať do
`CLAUDE.md` to, čo Claude nevyčíta z kódu a čo bolo treba opraviť opakovane. Limit 10 riadkov chráni, aby dlhý
`CLAUDE.md` nezhoršil dodržiavanie ostatných pokynov.

## Zvažovaná alternatíva

- Samostatný súbor `ctx/lessons.md` s odkazom z `CLAUDE.md`: zamietnuté vlastníkom, Claude ho číta iba keď si spomenie.
- Odosielanie poučení pre metódu automaticky (mail, issue na GitHube): zamietnuté, repozitár je verejný a každé
  odoslanie potrebuje súhlas.

## Čo by ho zmenilo

Ak sekcia napriek limitu prerastá, alebo sa ukáže, že zhoršuje dodržiavanie ostatných pokynov v `CLAUDE.md`.
