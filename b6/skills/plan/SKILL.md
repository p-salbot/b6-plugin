---
name: plan
description: Turn approved requirements and the design document into a step-by-step plan for the owner to approve. Use after brainstorming, when requirements are approved and a design file exists, or when the owner says "plan it", "make a plan", "how will we build it". Slovak triggers - naplánuj, plán, urob plán, ako to postavíme, rob (až po schválení plánu).
---

# plan - how to build it

The hard rules in skill `workflow` apply. If it is not loaded yet, load it first.
Templates are read from the `workflow` skill folder in the plugin (`../workflow/references/templates.md` and
`../workflow/references/models.md`), not from the project.

## Before you start

1. Read `ctx/requirements.md` and the design file `ctx/plans/<YYYY-MM-DD>-<slug>-design.md`.
2. Stop if the requirements are not `approved` or the design file is missing (size M). Go back to skill `brainstorming`.
   Do not plan from memory.
3. Confirm the language of the project documents in one sentence, for example "I will write the plan in English,
   like the other documents." The language is in `CLAUDE.md` or in the existing documents. Do not ask again if it is clear.
4. If this chat does not run on the strong level (see `models.md`), say so in one sentence before the plan.
   If agent models cannot be set, say that agents will run on the model of this chat.

## Plan in the chat first

Show the plan in the chat, using template `plan`. Keep it short enough to read in one minute.

- List the R-IDs it covers and the size.
- Table of steps: `# | Step | Agent | Model level | Task | How I verify`. One step is one piece the `worker` can finish
  and the `reviewer` can check. Agent is `worker`. Level comes from `models.md` (default medium, strong for a hard step).
  "How I verify" is a command or a check with the expected result, taken from the acceptance criteria.
- Choices for the owner, each with options and a recommendation with a reason.
- Token estimate from `models.md`, marked as approximate.

Then ask for agreement in plain words: what will be built, how the owner will know it works, and "say go to start"
(or "write the plan, but do not build yet").
Do not write any file and do not start any work before the owner agrees.

## After the owner agrees

Agreement is "go" or the same meaning in the owner's language ("rob", "yes, build it").

1. Write the plan to `ctx/plans/<YYYY-MM-DD>-<slug>.md` (template `plan`). Use the same `<slug>` as the design file.
   After this the plan is never changed. If something must change, tell the owner and write a new plan.
2. Add the task to `ctx/TASKS.md` (template `TASKS.md`): task with R-numbers, who acts, what blocks it, next step.
   Update the `Status` line with the date.
3. Hand over to skill `build`. If the owner said "write the plan, but do not start yet" (or similar), write the plan,
   add the task "Build per plan <file>" to `ctx/TASKS.md` and stop; do not start `build`.

If the owner changes the plan in the chat, show the changed plan again and ask again. A "go" given before the plan
was shown does not count.
