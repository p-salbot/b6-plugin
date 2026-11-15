# Súhrn scenárov – plugin b6 0.1.0

Beh 2026-11-15, model hlavného chatu `opus`, simulátor `sonnet`, spustil Peter vo vlastnom termináli (sandbox session
nepustí `claude -p --resume`). Celková cena asi 19,3 $. Vyhodnotenie: S1–S3, S5 hlavný chat; S4, S6–S11 agent podľa
`### Očakávané` v `scenare.md`.

| Scenár | Výsledok | Cena | Čo nesedelo |
|---|---|---|---|
| S1 | splnené | 0,22 $ | – |
| S2 | **nesplnené** | 0,21 $ | `workflow` sa nespustil: zmena hneď, bez súhlasu, bez worker/reviewer, zmenený aj skutočný `tasks.json` |
| S3 | **nesplnené** | 0,63 $ | „Add priority, go“ v novom projekte: hneď stavba, 4 súbory zmenené (pravidlo č. 1 plánu) |
| S4 | čiastočne | 6,38 $ | prvá správa má súhlas so súbormi a 5 otázok naraz (nie „po jednej“); ostatné splnené |
| S5 | čiastočne | 0,31 $ | nesplniteľnú požiadavku odmietol, nič nezmenil; do fázy požiadaviek a opráv sa nedostal, FIX a stop neoverené |
| S6 | **nesplnené** | 1,15 $ | nová funkcia zaradená ako S, plán nevznikol, dohoda uložená do pamäte Claude mimo projektu; fáza 2 stav z pamäte |
| S7 | splnené | 5,55 $ | persona schválila aj stavbu (drahý beh) |
| S8 | splnené | 0,30 $ | – |
| S9 | splnené | 2,22 $ | worker nechal `mk.py`, `verify.py` mimo projektu; persona schválila aj stavbu |
| S10 | splnené | 0,47 $ | `workflow/SKILL.md:64` berie slovenské stĺpce ako znak starého formátu, šablóna ich používa |
| S11 | splnené | 1,85 $ | odhad 300–700k tokenov pri ~40k skutočnosti (`models.md:41`) |

## Chyby pluginu podľa závažnosti

1. `workflow` sa v projekte bez `ctx/` nespustí pri krátkom príkaze (S2, S3); pri „I would like…“ áno (S4).
2. Nová funkcia sa dá zaradiť ako S; pri S nie je kam zapísať odložený plán, model použije pamäť Claude (S6).
3. Prvá správa zlučuje súhlas so súbormi a viac otázok (S4, S7, S10): `workflow/SKILL.md:58` vs. `brainstorming/SKILL.md:27`.
4. Worker píše pomocné súbory mimo projektu (S9, `agents/worker.md`).
5. Drobné: znak starého formátu „Slovak column names“ (`workflow/SKILL.md:64`), pevné pásmo odhadu tokenov (`models.md:41`).

## Testy

- Persony S7, S9, S11 schvaľujú aj stavbu; doplniť „write the plan, don't build yet“ podľa S6.
- Testovací chat má zapnutú automatickú pamäť (S6 ju použil): vypnúť v `spust.py` (`autoMemoryEnabled: false`).
- Po opravách pustiť znova aspoň S2, S3, S4, S6, S9.
