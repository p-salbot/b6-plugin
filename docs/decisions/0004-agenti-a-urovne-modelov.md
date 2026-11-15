# 0004 Prácu robia dvaja sebestační agenti `worker` a `reviewer`, modely sa určujú iba úrovňami

Dátum: 2026-11-14

## Rozhodnutie

Hlavný chat vedie rozhovor a zapisuje; prácu robí agent `worker` podľa briefu a každý výsledok aj opravu kontroluje
čerstvý `reviewer` bez nástroja `Edit`. Agenti sú sebestační: formát správy a recenzie majú v sebe a brief dostanú celý
v prompte. Skilly, plány a briefy hovoria iba úrovňami `strong`, `medium`, `cheap`; mapovanie na modely je iba
v `models.md` (hlavný chat a `reviewer` `opus`, `worker` `sonnet`). Plugin nepočíta s modelom Fable.

## Dôvod

Oddelená práca a nezávislá kontrola riešia, že výsledok sa nekontroluje voči zadaniu, a šetria tokeny hlavného chatu.
Dvoch agentov sa dá neprogramátorovi vysvetliť jednou vetou. Úrovne v jednom súbore umožnia zmeniť modely bez úpravy
skillov a fungujú na Team účtoch bez Fable.

## Zvažovaná alternatíva

- Bez agentov (všetko v hlavnom chate): zamietnuté, lebo chýba nezávislá kontrola a kontext sa rýchlo zaplní.
- Viac rolí (analytik, tester, dokumentarista): zamietnuté pre verziu 0.1.0 ako príliš ťažké pre malé zmeny.
- Presné ID modelov v agentoch: zamietnuté, lebo by sa museli meniť pri každej novej verzii modelu.

## Čo by ho zmenilo

Ak by Team účty klienta nemali dostupný `opus` alebo `sonnet`, alebo ak by sa metodika rozšírila o ďalšie roly.
