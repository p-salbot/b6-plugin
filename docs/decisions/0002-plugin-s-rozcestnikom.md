# 0002 Metodika sa dodáva ako jeden plugin s rozcestníkom `workflow` a samostatnými krokmi ako skillmi

Dátum: 2026-11-14

## Rozhodnutie

Metodika je plugin Claude Code `b6`. Skill `workflow` je rozcestník s tvrdými pravidlami a určením veľkosti práce;
kroky `brainstorming`, `plan`, `build` a `wrap-up` sú samostatné skilly. Ďalšie časti metodiky pribúdajú ako nové skilly.

## Dôvod

Plugin znamená jednu inštaláciu a jednu verziu pre všetkých ľudí vo firme. Pravidlá sú na jednom mieste, každý krok sa
dá zavolať sám a nová časť nevyžaduje prepisovať existujúce skilly.

## Zvažovaná alternatíva

- Voľné súbory (skilly kopírované do projektov): zamietnuté, lebo verzie by sa rozišli a aktualizácia by bola ručná.
- Iba samostatné kroky bez rozcestníka: zamietnuté, lebo pravidlá by sa opakovali v každom skille.
- Jeden skill s referenciami: zamietnuté, lebo krok by sa nedal zavolať sám a skill by bol príliš dlhý.

## Čo by ho zmenilo

Ak by Claude Code prestal podporovať pluginy pre Team účty, alebo ak by klient požadoval iný spôsob distribúcie.
