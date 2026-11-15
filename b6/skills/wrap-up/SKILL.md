---
name: wrap-up
description: 'Closes a finished piece of work - summary, evidence, requirement status, TASKS.md, architecture check, and cleanup of the design, plan and run files. Called only by skill `build` when all steps are OK, and by skill `workflow` when the owner answers about a "Try R-..." task or agrees to remove leftover design, plan or run files. Slovak: Volá ho skill build na konci a skill workflow po odpovedi o skúške alebo pri odstránení zvyškov po práci.'
---

# wrap-up - write down the result

The hard rules in skill `workflow` apply. If it is not loaded yet, load it first.
Templates are read from the `workflow` skill folder in the plugin (`../workflow/references/templates.md`), not from the project.

Keep the owner's language.

## Where you come from

- From `build` (all steps OK): do steps 1-6 in order.
- From `workflow` after the owner answered about a trial (works, partly, does not work, not yet): use that answer,
  do not ask again. Do only steps 3-4 (and step 6 if working files are still there).
- From `workflow` to delete leftovers: do only step 6.

## 1. Summary for the owner

Say in plain words: what was made, what is verified (command and result), what is still open, how many tokens it used
(from `SUMMARY.md`).

## 2. Evidence and "ready to try"

In `ctx/requirements.md` write the evidence for each requirement covered and set its status to `ready to try`.
A status without evidence does not count. A MUST without evidence is not ready.
Tell the owner what to try and how, in steps a non-programmer can follow (a command and what they should see).

## 3. Owner confirms

Ask only this (not when coming from `workflow` - use the answer you already have): "Did you try it? Does it work?" Meaning counts, not the exact words. Deleting is a separate question (step 6).

- Works: set `met`. Works only in part: set `partly met` and write what is missing in the Evidence column.
- Not yet: leave `ready to try`. Do not push. Go to "Owner cannot try now" below.
- Does not work: keep `ready to try`, never `met`. In `ctx/TASKS.md` replace the "Try R-..." task (if there is one)
  with a task to fix it (who acts: owner decides the next step). Tell the owner the next step is a new change through `workflow`.
- Never set `met` before the owner tried it.

## 4. TASKS.md

In `ctx/TASKS.md` delete the finished tasks (do not tick them off), add what stayed open (with who acts and what
blocks it), and rewrite the `Status` line with today's date.

## 5. Architecture check

Check that `docs/architecture.md` describes what is in the code today and no plans. If it does not match, tell the owner
and start `b6:worker` with a brief to fix it, then a fresh `b6:reviewer`. You do not edit it yourself.

## 6. Delete the working files

Working files are the design file `ctx/plans/<YYYY-MM-DD>-<slug>-design.md`, the plan `ctx/plans/<YYYY-MM-DD>-<slug>.md`
and the run folder `ctx/plans/<YYYY-MM-DD>-<slug>/`. Requirements, decisions and architecture stay.

- Project with git: ask for the owner's agreement to commit; delete after the commit, so the files stay in history.
  Never commit without agreement. If the owner declines or postpones the commit, keep the files as for "Not yet" below.
- Project without git: ask separately "Delete the plan, design and working folder?" Delete only after an explicit
  "delete" (or the same meaning). "Not yet": keep them and say that the owner can ask to delete them at any time; skill
  `workflow` then hands over to this step.

## Owner cannot try now

Finish the closing with status `ready to try`. Delete the design, plan and run folder by the rule in step 6
(an uncommitted project without git keeps them until "delete"). If `ctx/TASKS.md` has no such task yet, add
"Try R-<n>: <what and how>", with the owner in "Who acts". At the next start, skill `workflow` announces it.
When the owner answers, skill `workflow` hands over here (see "Where you come from"): apply step 3 with all its
branches (works, partly met, does not work, not yet), delete the task when it is done, update the `Status` line (step 4).
