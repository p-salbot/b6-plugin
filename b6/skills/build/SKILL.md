---
name: build
description: Carry out an approved plan step by step with worker and reviewer agents. Use after the owner said go to a plan, when a plan file exists in ctx/plans/, or when continuing a run in a new chat from SUMMARY.md. Slovak triggers - postav, realizuj plán, pokračuj v stavbe, rob podľa plánu, pokračuj podľa SUMMARY.
---

# build - lead the agents

The hard rules in skill `workflow` apply. If it is not loaded yet, load it first.
Templates (`brief`, `review`, `SUMMARY.md`) are read from the `workflow` skill folder in the plugin
(`../workflow/references/templates.md`), not from the project.

## Start

1. Read the plan `ctx/plans/<YYYY-MM-DD>-<slug>.md`. It must exist and the owner must have said "go". If not, go back to skill `plan`.
2. Make the run folder `ctx/plans/<YYYY-MM-DD>-<slug>/` with `briefs/` inside. If `SUMMARY.md` already exists there,
   read it and continue from "Where we stopped".
3. Otherwise create `SUMMARY.md` (template `SUMMARY.md`).

## For every step, one after another

1. **Brief.** Write the brief (template `brief`) from the plan, the requirements and the design. It lists the files the
   worker may change, what it must not touch, the acceptance criteria and how to verify. Put the whole brief in the
   prompt, or save it to `briefs/<n>-<slug>.md` and give the path.
2. **Worker.** Start agent `b6:worker` with the level from the plan (medium: default; strong: pass the model that
   `models.md` gives for strong).
   One step, one worker.
3. **Look yourself.** Read the report, then see the result: run the test or command from the plan. Do not trust
   "works" without running it.
4. **Reviewer.** Start a fresh `b6:reviewer` (strong). Give it the brief and the run folder; it writes `review-<n>.md`; `n` counts up across the run (next free number), never overwrite a review.
5. **Verdict.** `OK`: go to the next step. `FIX`: fix round below.
6. **Record.** Update `SUMMARY.md`: where we stopped, the step, the result, the evidence (command and result), fix rounds.

## Fix rounds

- Round 1: a fresh `worker` at medium level gets a brief with the findings. Then a fresh `reviewer`.
- Round 2: a fresh `worker` at strong level (model from `models.md`). Then a fresh `reviewer`.
- Still `FIX` after round 2: stop and report to the owner in plain words (hard rule 3). Do not start a third round.
- You never fix anything yourself, not even a typo (hard rule 2).

## Rules during the run

- Agents report in at most 20 lines. Details live in files.
- A conflict or choice that an agent lists in "Open" goes to the owner with your recommendation. You do not decide it.
- A hard-to-undo choice made during the run (section `decision record`): after the owner decides, the next brief names
  `docs/decisions/NNNN-<slug>.md` and the worker writes it.
- Do not change the plan. A change of scope needs the owner and a new plan.
- Context: follow the section "Context" of skill `workflow`.

## End

When every step is `OK`, write the final `SUMMARY.md` (add the real token use) and hand over to skill `wrap-up`.
