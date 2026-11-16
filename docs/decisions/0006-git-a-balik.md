# 0006 Git má iba priečinok nástroja so súkromným repozitárom na GitHube; odovzdáva sa iba zip z `b6/`

Dátum: 2026-11-15

## Rozhodnutie

Vlastný git má iba priečinok `nastroje/b6-plugin/`, so vzdialeným súkromným repozitárom na GitHube. Repozitár nesmie
obsahovať dôverné informácie klienta. Na odovzdanie sa balí iba priečinok `b6/` do `b6-<verzia>.zip`; dokumenty
o stavbe a `testy/` sa neodovzdávajú.

## Dôvod

Plugin je nástroj Panthea a jeho história má byť zálohovaná oddelene od dokumentov klienta. Zip iba z `b6/` zaručí, že
klient dostane plugin bez pracovných dokumentov a testov.

## Zvažovaná alternatíva

- Git celého priečinka klienta: zamietnuté, lebo by do histórie a na vzdialený repozitár išli dôverné dokumenty klienta.
- Iba lokálny git bez vzdialeného repozitára: zamietnuté, lebo plugin by nemal zálohu ani prístup z druhého počítača.

## Doplnenie 2026-11-16

Do zipu ide okrem `b6/` aj `.claude-plugin/marketplace.json` (zdroj pluginov `panthea`), oba v koreni zipu. Bez neho
klient plugin v `/plugin` nevidí a môže ho spustiť iba cez `--plugin-dir`. Súbor obsahuje iba názov, autora a cestu
`./b6`, žiadne informácie klienta.

## Doplnenie 2026-11-16 – verejný repozitár

Repozitár je verejný, aby si ho klient mohol pridať ako zdroj pluginov bez prístupu na GitHub (rozhodnutie Petra).
Pred zverejnením boli z repozitára aj celej histórie odstránené pracovné dokumenty s informáciami o klientovi
(`navrh.md`, `posudenie-*.md`, `plan.md`, `stav-stavby.md`, `ctx/plans/`); ostávajú iba lokálne a sú v `.gitignore`.
Do repozitára patrí iba plugin, jeho dokumentácia, rozhodnutia a testy so syntetickými dátami.

## Čo by ho zmenilo

Presun pluginu do repozitára Panthea pre viac klientov (potom aj premenovanie z `b6`), alebo požiadavka klienta
na iné úložisko.
