# 0001 Metodika brainstormingu vychádza zo skillu `brainstorming` pluginu superpowers, plugin je samostatný a nesie jeho licenčné oznámenie MIT

Dátum: 2026-11-14

## Rozhodnutie

Skill `brainstorming` pluginu `b6` vychádza z postupu skillu `brainstorming` pluginu superpowers (pozri sa pred otázkou,
prvá správa, jedna otázka v správe, otvorené otázky, kým nie je známe „prečo“, priebežné zhrnutie). Plugin `b6` je
samostatná metodika, nie nadstavba nad superpowers. Texty sú napísané nanovo; `b6/NOTICE` uvádza pôvod a plné znenie
licencie MIT. Autorské práva na plugin má Panthea s.r.o.

## Dôvod

Postup superpowers je overený a dobre vedie rozhovor od nápadu k zadaniu. Ich plánovanie (`writing-plans`) je však
anglické, pre programátorov a ukladá sa inam, než chce metodika `b6`. Licencia MIT pri prevzatí metódy vyžaduje
licenčné oznámenie.

## Zvažovaná alternatíva

- Nadstavba nad superpowers s ich skillom `writing-plans`: zamietnuté, lebo plán je pre programátorov, po anglicky
  a mimo `ctx/`, a plugin by závisel od iného pluginu.
- Vlastná metodika bez prevzatia: zamietnuté, lebo by sa zahodil overený postup rozhovoru.

## Čo by ho zmenilo

Zmena licencie superpowers alebo rozhodnutie prepísať brainstorming úplne bez ich postupu (potom by sa dalo zvážiť
odstránenie `NOTICE`).
