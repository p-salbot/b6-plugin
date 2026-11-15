# 0003 Texty pluginu sú po anglicky so slovenskými spúšťacími slovami; jazyk dokumentov projektu volí používateľ

Dátum: 2026-11-14

## Rozhodnutie

Skilly, agenti, šablóny, README a názvy v plugine sú po anglicky. Popisy skillov majú aj slovenské spúšťacie slová.
Claude hovorí s používateľom jazykom, ktorým používateľ píše. Jazyk dokumentov projektu (`ctx/`, `docs/`) si volí
používateľ na konci brainstormingu a zapíše sa do `CLAUDE.md` projektu; šablóny majú anglické aj slovenské hlavičky,
stĺpce a stavy (sekcia `Language` v `templates.md`). Názvy súborov, čísla a priority sa neprekladajú.

## Dôvod

Anglické texty pluginu sa dajú použiť aj mimo jedného jazyka a Claude ich spoľahlivo dodržiava. Slovenské spúšťacie
slová zaistia, že sa skilly spustia aj pri slovenskej požiadavke. Ľudia, ktorí nie sú programátori, potrebujú
dokumenty projektu vo svojom jazyku.

## Zvažovaná alternatíva

- Plugin celý po slovensky: zamietnuté, lebo by sa horšie používal inde a názvy súborov a stavov by sa miešali
  s anglickými nástrojmi.
- Dokumenty projektu vždy po anglicky: zamietnuté, lebo vlastník ich má čítať a schvaľovať.

## Čo by ho zmenilo

Ak by sa ukázalo, že slovenské spúšťacie slová skilly nespoľahlivo spúšťajú, alebo ak by plugin mal slúžiť iba
slovenským používateľom.
