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
2. Make the run folder `ctx/plans/<YYYY-MM-DD>-<slug>/` with `briefs/` and `scratch/` inside; put a file
   `scratch/.gitignore` with the single line `*` into `scratch/`. If `SUMMARY.md` already exists there,
   read it and continue from "Where we stopped".
3. Otherwise create `SUMMARY.md` (template `SUMMARY.md`).

## For every step, one after another

1. **Brief.** Write the brief (template `brief`) from the plan, the requirements and the design. It lists the files the
   worker may change, what it must not touch, the acceptance criteria and how to verify. Put the whole brief in the
   prompt, or save it to `briefs/<n>-<slug>.md` and give the path.
2. **Worker.** Start agent `b6:worker` with the level from the plan (medium: default; strong: pass the model that
   `models.md` gives for strong).
   One step, one worker.
3. **Look yourself.** Read the report, then see the result: run the test or command from the plan. A trial
   run on a copy of the project uses a copy in `scratch/`, deleted after the check. Do not trust "works" without running it.
4. **Reviewer.** Start a fresh `b6:reviewer` (strong). Give it the brief and the run folder; it writes `review-<n>.md`; `n` counts up across the run (next free number), never overwrite a review. After a fix, also give it the earlier `review-<n>.md`.
5. **Verdict.** `OK`: go to the next step. `FIX`: fix round below. If a `cannot verify` needs the owner, ask the owner too (see Fix rounds).
6. **Record.** Update `SUMMARY.md`: where we stopped, the step, the result, the evidence (command and result), fix rounds.

## Fix rounds

- Round 1: a fresh `worker` at medium level gets a brief with the findings and the path of the earlier `review-<n>.md`. Then a fresh `reviewer`, who gets that review too.
- Round 2: a fresh `worker` at strong level (model from `models.md`), brief as in round 1. Then a fresh `reviewer`, who also gets the earlier review.
- Still `FIX` after round 2: stop and report to the owner in plain words (hard rule 3). Do not start a third round. If the
  owner then accepts the result with gaps, record it in `SUMMARY.md`, say whether the remaining plan steps depend on the
  stopped step, and ask: build the remaining steps now (recommended when they do not depend on it) or stop now.
  Build now: continue with the next step as usual. Stop now: go to "End". If the owner does not accept, the owner decides the next step.
- A `cannot verify` that only the owner can settle (access, data, a manual trial): ask the owner in plain words, with options and a recommendation. If it is the only kind of finding, start no fix round. If there are also ordinary findings, start round 1 for them and ask the owner in the same message.
- You never fix anything yourself, not even a typo (hard rule 2).

## Rules during the run

- Agents report in at most 20 lines. Details live in files.
- A conflict or choice that an agent lists in "Open" goes to the owner with your recommendation. You do not decide it.
- A hard-to-undo choice made during the run (section `decision record`): after the owner decides, the next brief names
  `docs/decisions/NNNN-<slug>.md` and the worker writes it.
- Do not change the plan. A change of scope needs the owner and a new plan.
- A command is blocked (refused or denied, for example a test command): follow hard rule 8 (form refusal: rewrite once
  into simple commands; denial: no variants, ask the owner "May I run it?", rerun only after an explicit yes). Before you
  accept a step, read the agent's list of refused, rewritten or skipped commands. A refused shell edit done with
  Edit/Write instead, or a form refusal rewritten once that then worked: accept it and mention it to the owner.
  Anything else (a script workaround, a skipped check, a second refusal): ask the owner by hard rule 8 before you
  accept the step. Never report "rewritten once" unless the
  agent's report says so.
- Context: follow the section `Context, and "how does this work"` of skill `workflow`.

## End

The run ends when every step is `OK`, when the owner accepted gaps and the remaining steps are done, or when the owner
chose "stop now". Then write the final `SUMMARY.md`: the real token use, that the run ended, and the steps not done
with their R-IDs (if any). Only then hand over to skill `wrap-up` (it sets `partly met` for accepted gaps).
