# Skilly ako firemné znalosti

Zhrnutie z brainstormingu, 2026-11-12. Je to názor, ktorý vznikol z praxe, nie výsledok merania. Vychádza
z autorovej vlastnej práce s dvoma sadami skillov pre AI asistenta (`strix-health`, znalosti o slovenskom
zdravotníctve, a `ps-metodika`, spôsob práce). Tvrdenia nižšie sú autorova skúsenosť, ak pri nich nie je
uvedený zdroj.

## 1  Hlavná myšlienka

Skill je textový súbor pre AI asistenta. Má krátky popis, ktorý AI spravidla vidí[^1], a telo, ktoré AI otvorí,
keď popis sedí na úlohu. Rozsiahlejšie podklady sa otvárajú, až keď sú potrebné. Formát nevyžaduje kroky ani
kód.

Slovo „skill“ naznačuje schopnosť niečo urobiť, preto ľudia hľadajú úlohy, ktoré by zautomatizovali,
a prehliadajú znalosti, na ktorých tie úlohy stoja. Skill však nemusí byť postup. Môže to byť
**znalostný skill**: čo v danej oblasti platí, čo znamenajú pojmy, kde sú pasce. Taký skill drží AI v hraniciach oblasti. Neuvedomili
si to ani mnohí schopní ľudia.

| Druh skillu | Čo obsahuje | Dá sa prirovnať k |
|---|---|---|
| Postup | kroky, príkazy, šablóny pre jednu opakovanú úlohu | pracovnému návodu |
| Znalostný skill | fakty, pojmy, pravidlá, pasce a otvorené otázky jednej oblasti | skúsenému kolegovi, ktorý sedí vedľa vás |
| Slovník | firemné pojmy, skratky a kódy s ich významom | firemnému slovníku |
| Osobný profil | rola, skutočné zručnosti a znalosti, štýl práce jedného človeka | predstaveniu sa novému spolupracovníkovi |

Postup zlepší jednu úlohu. Znalostný skill môže zlepšiť veľa úloh vo svojej oblasti a krátky, sústredený
funguje lepšie než úplný. Postup si AI často vymyslí sama; fakty o firme si zvyčajne vymyslieť nevie.

## 2  Na čo sa dajú skilly použiť

- **Odborné znalosti,** ktoré všeobecná AI nemá, lebo sú miestne, úzko špecializované alebo sa každý rok menia
  (napríklad úhrady v slovenskom zdravotníctve a ich dátové formáty).
- **Slovník:** pojmy, skratky a kódy, ktoré používa firma alebo tím, každý s jedným dohodnutým významom.
  AI potom číta a píše jazykom firmy a nemusí ho hádať.
- **Udržať AI v mantineloch:** čo pojem znamená, čo sa považuje za chybu, čo je v dátach bežné.
- **Opakované postupy** a časti procesu, ktoré sa dajú automatizovať.
- **Osobný profil:** pre koho AI pracuje, na akej pozícii a s akými skutočnými zručnosťami.
- **Akákoľvek rola, nielen IT:** CEO, logistika, HR, marketing, obchod. Kľúčoví ľudia sa naučili písať skilly,
  ktoré sú jednoduchšie, než aké by napísal špecialista na AI, a predsa stačia na automatizáciu časti procesu.

## 3  Čo tým firma môže získať

- **Menej vysvetľovania.** Kontext už netreba písať do každej požiadavky, alebo len jeho malú časť.
- **Zdieľané znalosti.** Jeden zdroj s históriou zmien slúži každému projektu a každému kolegovi, ktorý si ho
  pridá k svojmu asistentovi.
- **Zastupiteľnosť.** Kým je človek na dovolenke alebo práceneschopný, prácu môžu urobiť iní – v tej časti
  znalostí, ktorá je v skille zapísaná.
- **Rýchlejšie zaučenie.** AI asistent nového kolegu pozná zapísanú časť oblasti od prvého dňa.
- **Spoločný jazyk.** Ľudia aj ich AI asistenti používajú pojem naprieč tímami v rovnakom význame, lebo význam
  pochádza z jedného slovníka.
- **Kolektívna pamäť.** Skilly spolu tvoria usporiadaný text, teda znalosti zoradené podľa tém, ktoré vie čítať
  aj stroj a ktoré opisujú procesy a znalosti firmy.
- **Neskoršie využitie.** Text je obyčajný a čitateľný, takže ho môžu použiť iné AI modely, skilly, projekty
  a nástroje. Spôsob, akým si nástroj skill načíta, sa medzi nástrojmi líši; samotné znalosti sa prenášajú
  s textom.

## 4  Čo sa časom zlepšuje

- **Každý ďalší skill, projekt a postup vzniká ľahšie,** lebo AI už pozná človeka, jeho pozíciu, skutočné
  zručnosti a oblasť, v ktorej pracuje.
- **Hodnota rastie s používaním.** Čím viac človek s AI pracuje, tým viac si skilly cení: kontext, ktorý kedysi
  písal do každej požiadavky, tam už je. Prínosom je najmä práca, ktorú už netreba robiť.
- **Chyby sa môžu ukázať skôr než vo wiki.** Podľa autorovej skúsenosti môže chybná stránka vo wiki zostať
  nepovšimnutá celé roky. Skill sa používa denne, takže nesprávny údaj sa prejaví vo výsledkoch. Pomáha to len
  vtedy, keď funguje spätná väzba z §6.1; bez nej sa chyba šíri (§5).

## 5  Riziká a obmedzenia

| Riziko | Prečo na ňom záleží |
|---|---|
| Väčšina ľudí nebude písať skilly z vlastnej iniciatívy | Chýba im čas a návyk dávať znalostiam štruktúru. Niektorí tiež neveria tomu, čo sa so zdieľanými znalosťami stane (pozri riadok o nahraditeľnosti). |
| Zastarávanie | Zastaraný skill môže byť horší než žiadny, lebo AI mu verí. |
| Tichá chyba sa rozšíri ku všetkým | Kontext písaný ručne človek zakaždým vidí. Obsah skillu si znova nikto nečíta a jedno nesprávne pravidlo v zdieľanom skille zopakuje AI každého kolegu. |
| Skill je zhrnutie, nie zdroj | Číslo alebo kód prevzaté do zhrnutia môžu byť nesprávne. |
| Skill nenahrádza úsudok odborníka | Zástup alebo nováčik dostane len to, čo bolo zapísané, a výsledok musí vedieť skontrolovať sám. Spoliehanie sa iba na AI môže oslabiť vlastnú odbornosť ľudí, najzreteľnejšie v čase, keď sa ešte učia. |
| Znalostný skill AI ťažšie zachytí | Postup má zjavný okamih, keď ho treba použiť. Znalostný skill treba otvoriť vždy, keď sa téma objaví, aj keď ju nikto nepomenuje, a AI sa rozhoduje iba podľa popisu. |
| Znalostný skill sa ťažšie kontroluje | Nesprávny údaj vyzerá rovnako presvedčivo ako správny. |
| Veľa skillov | Popisy sa delia o obmedzený priestor a ako prvé vypadávajú popisy najmenej používaných skillov[^1], takže zriedkavo otváraný znalostný skill môže o svoj popis prísť. S rastúcim počtom je výber menej spoľahlivý: najčastejšie sa neotvorí žiadny skill, zriedkavejšie nesprávny. Skilly, ktoré sa na seba podobajú, škodia viac než samotný počet. |
| Prekrývanie skillov | Dva skilly, ktoré o jednej téme hovoria trochu odlišné veci, môžu AI zmiasť viac než žiadny skill. |
| Skilly usmerňujú, nevynucujú | Text funguje tam, kde ide o úsudok. Hranica, ktorú nikdy nemožno prekročiť (zákaznícke dáta, produkčné systémy, posielanie dát von), potrebuje prístupové práva a technické zábrany. |
| Citlivý obsah | Znalosti z HR, obchodu a vedenia obsahujú osobné údaje, platy, podmienky klientov a stratégiu. Osobný profil je osobný údaj. |
| Firemné pravidlá | O tom, ktorú AI službu možno použiť a čo sa do nej smie vložiť, rozhoduje firemná politika využívania AI a pravidlá ochrany údajov. |
| Skilly zvonka | Skill stiahnutý z internetu môže obsahovať škodlivé inštrukcie alebo programy. |
| Vlastník odíde | Skill bez vlastníka už nikto nekontroluje a zastaráva. |
| „Moju prácu zvládnu aj iní“ znie aj ako „dá sa ma nahradiť“ | Ľudia si potom to cenné nechávajú pre seba. |
| Hodnota sa ťažko ukazuje | Znalostný skill sám osebe nerobí nič viditeľné. |

## 6  Procesy, ktoré udržiavajú kvalitu

### 6.1  Dva najdôležitejšie

1. **Pravidelná kontrola.** Vlastník skill prejde v pevnom intervale a vždy, keď sa oblasť zmení. Kontrola
   zachytí to, čo sa zmenilo vo svete.
2. **Spätná väzba takmer bez námahy.** Kto si všimne nesprávnu odpoveď, povie to v tej istej konverzácii
   a oprava sa navrhne vlastníkovi. Spätná väzba zachytí to, čo bolo zle od začiatku. Ak nahlásenie vyžaduje
   formulár alebo tiket, ľudia si odpoveď opravia len pre seba a skill zostane chybný.

### 6.2  Podporné zásady

1. **Vlastník a platnosť.** Každý skill uvádza svojho vlastníka a autora, verziu zdroja, pre ktorú platí,
   a dátum posledného overenia.
2. **Odovzdanie a vyradenie.** Keď vlastník odíde alebo zmení rolu, skill dostane nového vlastníka, alebo sa
   vyradí. Pri kontrole sa prekrývajúce sa skilly zlúčia a nepoužívané odstránia, aby popisy zostali odlíšiteľné.
3. **Navrhuje ktokoľvek, schvaľuje vlastník.** Používatelia zdieľaný skill priamo nemenia.
4. **Druhý čitateľ pri zdieľaných skilloch.** Skill, ktorý používa viac ľudí, si pred vydaním prečíta ešte
   jeden človek. Skill zvonka sa prečíta celý skôr, než si ho ktokoľvek pridá.
5. **Kontrolné otázky.** Každý znalostný skill má krátky zoznam otázok so známymi odpoveďami, ktoré sa po každej
   zmene položia znova.
6. **Zdroje a citácie.** Číslo, kód alebo pravidlo, ktoré sa použije vo výpočte, v programe alebo pri
   rozhodovaní, má pri sebe odkaz na zdroj a pred použitím sa v ňom overí.
7. **Jeden údaj na jednom mieste.** Ostatné skilly naň odkazujú a neopakujú ho. Pojem sa definuje raz,
   v slovníku.
8. **Tri časti v každom znalostnom skille:** čo platí; v čom sa ľudia bežne mýlia; čo sa nevie alebo ešte nie je
   rozhodnuté. Tretia časť má obmedziť sebavedomé hádanie zo strany AI.
9. **Popis vyladený podľa skutočných otázok.** Keď AI odpovie na odbornú otázku bez toho, aby skill otvorila,
   popis sa upraví.
10. **Prístup podľa roly.** Celofiremné, tímové a osobné skilly sa držia oddelene. Do skillu nepatria
    zákaznícke dáta ani záznamy o skutočných osobách; príklady sú vymyslené. Výnimkou je osobný profil: človek
    si ho píše dobrovoľne a pre vlastnú potrebu, zostáva jeho vlastným skillom a neobsahuje údaje o iných
    ľuďoch. Samotný súhlas zamestnanca ako základ nestačí; platia firemné pravidlá (§5).
11. **Rozsiahle referenčné dáta zostávajú mimo textu.** V dlhom číselníku vyhľadáva malý program, AI ho nečíta.
12. **AI navrhne, človek schváli.** Po dokončenej úlohe AI navrhne skill alebo jeho zmenu; človek, ktorému
    znalosť patrí, doplní to, čo AI nevedela, návrh opraví a schváli. Hodnota je práve v tých doplneniach:
    návrh schválený bez zmeny má malú cenu. Znižuje to prekážku pre ľudí, ktorí by skill sami nenapísali.
13. **Uznanie a dôkazy.** Autorstvo je viditeľné a vedenie ho oceňuje. Ušetrený čas sa zaznamenáva a ostatným
    sa ukazuje tá istá otázka zodpovedaná so skillom a bez neho.

## 7  Ako sa jednotlivé riziká zmierňujú

Každé riziko z §5, jeho zmiernenie a proces z §6, ktorý ho zabezpečuje.

| Riziko | Zmiernenie | Proces |
|---|---|---|
| Väčšina ľudí nebude písať skilly z vlastnej iniciatívy | Kľúčoví ľudia sa naučia skilly písať. Po dokončenej úlohe AI navrhne skill; človek doplní to, čo AI nevedela, návrh opraví a schváli. | §6.2 bod 12 |
| Zastarávanie | Každý skill uvádza verziu svojho zdroja a dátum posledného overenia. Vlastník ho kontroluje v pevnom intervale a vždy, keď sa oblasť zmení. | §6.1 bod 1, §6.2 bod 1 |
| Tichá chyba sa rozšíri ku všetkým | Kto si všimne nesprávnu odpoveď, nahlási ju v tej istej konverzácii. Zdieľaný skill pred vydaním prečíta druhý človek a po každej zmene sa overí kontrolnými otázkami. | §6.1 bod 2, §6.2 body 4 a 5 |
| Skill je zhrnutie, nie zdroj | Číslo, kód alebo pravidlo, ktoré sa použije vo výpočte, v programe alebo pri rozhodovaní, má pri sebe odkaz na zdroj a pred použitím sa v ňom overí. Príklad pod tabuľkou. | §6.2 bod 6 |
| Skill nenahrádza úsudok odborníka | Výsledok skontroluje človek, ktorý ho vie posúdiť. Zastupovanie počas neprítomnosti sa obmedzuje na to, čo skill opisuje; rozhodnutia nad jeho rámec počkajú na odborníka. | v §6 zatiaľ nie je; dohodne sa v každom tíme |
| Znalostný skill AI ťažšie zachytí | Popis obsahuje slová, ktoré ľudia naozaj používajú: bežné pojmy, skratky, kódy a typické situácie. Keď AI odpovie na odbornú otázku bez otvorenia skillu, chýbajúce slová z tej otázky sa do popisu doplnia. Príklad pod tabuľkou. | §6.2 bod 9 |
| Znalostný skill sa ťažšie kontroluje | Znalostný skill má tri poistky: kontrolné otázky so známymi odpoveďami, odkazy na zdroj pri dôležitých tvrdeniach a časť o tom, čo sa nevie alebo nie je rozhodnuté. Príklad pod tabuľkou. | §6.2 body 5, 6 a 8 |
| Veľa skillov | Pri kontrole sa prekrývajúce sa skilly zlúčia a nepoužívané odstránia, aby popisy zostali odlíšiteľné. | §6.2 bod 2 |
| Prekrývanie skillov | Každý údaj je zapísaný na jednom mieste; ostatné skilly naň odkazujú. | §6.2 bod 7 |
| Skilly usmerňujú, nevynucujú | Hranicu, ktorú nikdy nemožno prekročiť, chránia prístupové práva a technické zábrany, nie text skillu. | mimo skillov; nastavuje IT |
| Citlivý obsah | Celofiremné, tímové a osobné skilly sa držia oddelene. Žiadne zákaznícke dáta ani záznamy o skutočných osobách; príklady sú vymyslené. Osobný profil si človek píše dobrovoľne a zostáva u neho. | §6.2 bod 10 |
| Firemné pravidlá | Pred zdieľaním vlastník skill porovná s firemnou politikou využívania AI a pravidlami ochrany údajov; kde to pravidlá vyžadujú, vyžiada si schválenie. | v §6 zatiaľ nie je; riadi sa firemnou politikou |
| Skilly zvonka | Skill zvonka sa prečíta celý skôr, než si ho ktokoľvek pridá. | §6.2 bod 4 |
| Vlastník odíde | Skill pri odovzdaní dostane nového vlastníka, alebo sa vyradí. | §6.2 bod 2 |
| „Moju prácu zvládnu aj iní“ znie aj ako „dá sa ma nahradiť“ | Autorstvo je v každom skille viditeľné a vedenie ho oceňuje. | §6.2 bod 13 |
| Hodnota sa ťažko ukazuje | Ušetrený čas sa zaznamenáva. Ostatným sa ukazuje tá istá otázka zodpovedaná so skillom a bez neho. | §6.2 bod 13 |

### Príklady k trom riadkom

**Skill je zhrnutie, nie zdroj.** Skill údaje zo zdroja prepisuje v skrátenej podobe; pri prepise sa môže stať
chyba, alebo sa zdroj medzičasom zmení. *Príklad:* skill uvádza základnú sadzbu pre daný rok. Kým sa ňou
prepočítajú úhrady, sadzba sa overí v platnom cenníku, na ktorý skill odkazuje. Bežné vysvetlenie pojmu sa
overovať nemusí.

**Znalostný skill AI ťažšie zachytí.** AI otvorí skill len vtedy, keď v jeho popise nájde slová z otázky,
a ľudia sa málokedy pýtajú odborným názvom témy. *Príklad:* kolega sa opýta „prečo má tento prípad nižšiu
úhradu, keď pacient ležal dlhšie?“ a slovo DRG nepovie. Ak sú v popise len slová „SK-DRG, zaraďovanie“, skill
sa neotvorí. Po doplnení „úhrada za hospitalizáciu, ošetrovacia doba, prípad“ sa otvorí.

**Znalostný skill sa ťažšie kontroluje.** Pri postupe je chyba vidieť hneď: krok zlyhá. Nesprávny fakt
nezlyhá, AI ho len zopakuje. *Príklad:* kontrolná otázka „Koľko položiek má riadok dávky 751d?“ má známu
odpoveď 29. Ak AI po úprave skillu odpovie inak, úprava niečo pokazila. V časti o neznámom môže stáť: „Či sa
pravidlo vzťahuje aj na opravné dávky, nie je potvrdené.“ AI potom medzeru nedoplní odhadom.

## Poznámka

Zdroj bol čítaný 2026-11-12.

[^1]: **Kedy AI popis nevidí** (Claude Code; iné nástroje sa správajú inak). Zoznam skillov, ktorý AI dostáva,
    má obmedzenú veľkosť: 1 % kontextového okna modelu. Limit sa dá zmeniť nastavením
    `skillListingBudgetFraction` alebo premennou prostredia `SLASH_COMMAND_TOOL_CHAR_BUDGET`. Zoznam vždy
    obsahuje názov každého skillu. Keď sa popisy nezmestia, Claude Code niektoré vynechá, počnúc skillmi, ktoré
    sa spúšťajú najmenej, a upozornenie zapíše iba do ladiaceho logu. Skill, ktorý prišiel o popis, sa dá
    vybrať už len podľa názvu. Okrem toho sa popis spolu s nepovinným poľom `when_to_use` v zozname skracuje na
    1 536 znakov a skill označený `disable-model-invocation: true` v zozname popis nemá vôbec; otvorí sa, iba
    keď ho zavolá človek. Dôsledok pre tento dokument: pri veľkom počte nainštalovaných skillov sa ako prvý
    stane neviditeľným znalostný skill, ktorý sa otvára zriedka, a používateľa na to nič neupozorní. Zdroj:
    dokumentácia Claude Code, „Extend Claude with skills“, <https://code.claude.com/docs/en/skills>.

@panthea.sk
