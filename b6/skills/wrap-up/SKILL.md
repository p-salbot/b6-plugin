---
name: wrap-up
description: 'Closes a finished piece of work - summary, evidence, requirement status, what the owner can try, TASKS.md, architecture check, and cleanup of the design, plan and run files. Called only by skill `build` when all steps are OK or when the owner accepts a result with gaps after two fix rounds, and by skill `workflow` when the owner reports that a met requirement does not work or agrees to remove leftover design, plan or run files. Slovak: Volá ho skill build na konci (aj keď vlastník prijme výsledok s medzerami po dvoch kolách opráv) a skill workflow, keď vlastník hlási, že splnená požiadavka nefunguje, alebo pri odstránení zvyškov po práci.'
---

# wrap-up - write down the result

The hard rules in skill `workflow` apply. If it is not loaded yet, load it first.
Templates are read from the `workflow` skill folder in the plugin (`../workflow/references/templates.md`), not from the project.
When you start `b6:worker` or `b6:reviewer` (steps 5 and 6), read their refused commands and handle them as in `build` (hard rule 8).

Talk in the owner's language; write documents in the language in `CLAUDE.md`.

## Where you come from

- From `build` (all steps OK): do steps 1-6 in order.
- From `build` after two fix rounds, the owner accepts the result with gaps (remaining steps built, or the owner stopped):
  do steps 1-6 in order; step 2 sets `partly met`, step 4 adds the steps not done.
- From `workflow` because the owner reports that a `met` requirement does not work: do only "Owner reports it does not
  work" below.
- From `workflow` to delete leftovers: do only step 6.

## 1. Summary for the owner

Say in plain words: what was made, what is verified (command and result), what is still open, how many tokens it used
(from `SUMMARY.md`).

## 2. Evidence and status

In `ctx/requirements.md` write the evidence for each requirement covered (from the review files of the run) and set its
status. A status without evidence does not count.

- `met`: a fresh reviewer gave `OK` with evidence for every criterion of the requirement. The owner does not have to try it.
- `partly met`: the owner accepts the result although a criterion is not met (for example after the stop after two
  rounds of fixes). Write what is missing in the Evidence column.
- A MUST without evidence for every criterion is not `met`.

## 3. What the owner can try

Tell the owner what they can try and how, in steps a non-programmer can follow (a command and what they should see).
This is information only: do not ask whether they tried it and add no task for it. Say that if something does not work
later, they just tell Claude, and it becomes a new change.

## 4. TASKS.md

In `ctx/TASKS.md` delete the finished tasks (do not tick them off), add what stayed open (with who acts and what
blocks it), and rewrite the `Status` line with today's date. For every step not done (listed in the final `SUMMARY.md`)
add a task with its R-IDs; those requirements stay `approved`.

## 5. Architecture check

Check that `docs/architecture.md` describes what is in the code today and no plans. If it does not match, tell the owner
and start `b6:worker` with a brief to fix it, then a fresh `b6:reviewer`. You do not edit it yourself.

## 6. Delete the working files

Working files are the design file `ctx/plans/<YYYY-MM-DD>-<slug>-design.md`, the plan `ctx/plans/<YYYY-MM-DD>-<slug>.md`
and the run folder `ctx/plans/<YYYY-MM-DD>-<slug>/` (with its `scratch/`). Requirements, decisions and architecture stay.

Ask the owner first; fix links only after a yes.

- Project with git: ask for the owner's agreement to commit. Never commit without agreement. If the owner declines or
  postpones the commit, keep the files as for "Not yet" below and change nothing.
- Project without git: ask separately "Delete the plan, design and working folder?" Delete only after an explicit
  "delete" (or the same meaning). "Not yet": keep them, change nothing, and say that the owner can ask to delete them at
  any time; skill `workflow` then hands over to this step.
- After a yes, while the run folder still exists: find links to the working files in `ctx/`, `docs/` and `CLAUDE.md`.
  Start `b6:worker` with a brief that names those files as allowed, then a fresh `b6:reviewer` (review in the run folder);
  you do not edit them yourself. A link becomes a note without a commit hash, for example "removed at wrap-up <date>; in
  git history" (git) or "removed at wrap-up <date>" (no git).
- Then with git: commit, then delete, so the files stay in history. Without git: delete.

## Owner reports it does not work

In `ctx/requirements.md` set the requirement back to `approved` and add a dated note to the Evidence column
(`<date>: owner reports: <what does not work>`); keep the earlier evidence. Rewrite the `Status` line in `ctx/TASKS.md`
(step 4). First offer to delete leftover working files (step 6). Then tell the owner the next step is a new change through `workflow`; never restart the finished run.
