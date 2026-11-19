---
name: lessons
description: 'Picks at most two lessons worth keeping from a finished run, only from evidence in the run files (fix rounds, a stop after two rounds, refused commands that stopped work, an owner report that something does not work, a token estimate exceeded). A project lesson becomes one line in the project CLAUDE.md after the owner agrees; a method lesson goes to ctx/b6-lessons.md and is shown in chat for the owner to send to the b6 maintainer. Called only by skill `wrap-up`, before the working files are deleted. Slovak triggers - poučenia, čo sme sa naučili, poučenie z behu.'
---

# lessons - keep only what is worth learning

The hard rules in skill `workflow` apply. If it is not loaded yet, load it first.
Templates (`brief`, `review`, `lessons`, `b6-lessons.md`, `CLAUDE.md lessons`) are read from the `workflow` skill folder
in the plugin (`../workflow/references/templates.md`), not from the project.
Talk in the owner's language; write documents in the language in `CLAUDE.md`.
When you start `b6:worker` or `b6:reviewer`, read their refused commands and handle them as in `build` (hard rule 8).

## 1. Quick check (main chat, no agents)

If `wrap-up` did not call this skill, do nothing, say so in one sentence and go back to `workflow`; lessons are
picked only when a run is closed.
Do nothing more when there is no run folder (size S), or when `SUMMARY.md` and the `review-*.md` files of the run show no
evidence: no fix round, no stop after two rounds, no refused command that stopped work, no gap accepted by the owner, no
token estimate exceeded, no owner report "does not work" (Evidence column of `ctx/requirements.md`).
Then tell the owner in one sentence ("nothing worth learning from this run") and go back to `wrap-up`. Write nothing.

## 2. Candidates (worker)

Start a fresh `b6:worker` at strong level (model from `models.md`) with a brief (template `brief`). Inputs: `SUMMARY.md`,
`review-*.md`, `ctx/requirements.md`, the lessons section of `CLAUDE.md`, and the plugin texts (read only, for condition 4).
It writes only `<run folder>/lessons.md` (template `lessons`). A candidate passes only if it meets all four conditions:

1. Cost: a proven cost with a link to a run file (for example `review-3.md`).
2. General: it would happen again (project: in later work in this project; method: in another project).
3. Actionable: exactly what to change (project: one line for `CLAUDE.md`; method: a plugin file and the change in 1-2 sentences).
4. New: it is not in the rules yet. If a rule exists and was broken, the lesson says why the rule did not work.

Each lesson has a level, `project` or `method`. At most 2 lessons, the ones with the highest cost; every other candidate
gets one line with the reason under `Rejected`. Zero lessons is a normal, valid result.
No small things: a one-off slip without cost, typos, style. No names, client data, user names in paths, or quotes from
client files.

## 3. Review (reviewer)

Start a fresh `b6:reviewer` (strong). It checks `lessons.md` against the four conditions, the limit of 2 and the ban on
names and client data, and writes `review-<n>.md`. `FIX`: fix rounds as in `build` (at most two). Still `FIX` after
round 2: drop the lessons, tell the owner in one sentence, go back to `wrap-up`. This never stops the wrap-up.

## 4. After OK: project lesson

Show the line and ask the owner "Add this line to CLAUDE.md?" (in the owner's language). Only after a yes, write it into
the lessons section of `CLAUDE.md` (template `CLAUDE.md lessons`). Look for it under `## Lessons` or under its heading in
the `Language` table of `templates.md` (by the language in `CLAUDE.md`); never create the other one. If neither exists,
create it at the end of `CLAUDE.md`. The section has at most 10 lines: when it has 10, do not write an 11th; propose deleting the oldest or an
outdated line, and add the new one only after the owner agrees. No means no change to `CLAUDE.md`.

## 5. After OK: method lesson

Add an entry with today's date at the end of `ctx/b6-lessons.md` (template `b6-lessons.md`; create the file if missing).
Show the same text in chat and say that the owner should copy it and send it to the maintainer of the b6 plugin (mail or
chat). Send nothing yourself: no mail, no issue, no change to plugin files.

## Rules

- The main chat writes `CLAUDE.md` and `ctx/b6-lessons.md` itself (like `requirements.md` and `TASKS.md`); agents do the rest.
- Nothing is written to `SUMMARY.md`. Then `wrap-up` continues with its step 6.
