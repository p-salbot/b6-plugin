## 2026-11-19 Odhad tokenov podhodnocuje recenzie a opravné kolá

- Čo sa stalo: Plán s 4 krokmi odhadol beh na 350–600k tokenov podľa `models.md`, skutočnosť bola približne 1,1 milióna.
  Príčiny: šesť recenzií silným modelom po približne 80k, dve opravné kolá (každé s novou úplnou recenziou) a jeden
  krok náročnejší, než plán počítal.
- Cena: odhad prekročený asi dvojnásobne; dve opravné kolá.
- Navrhovaná zmena v plugine: `b6/skills/workflow/references/models.md`, sekcia „Token estimate“: počítať `worker`
  a `reviewer` zvlášť (recenzia silným modelom približne 50–100k bez ohľadu na veľkosť kroku; odhad z jedného behu)
  a opravné kolo ako novú prácu `worker` plus celú novú recenziu, nie „polovicu kroku“.
- Verzia b6: 0.2.0
- Tento záznam neobsahuje mená ani údaje klienta.
