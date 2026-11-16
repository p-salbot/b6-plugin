# Document templates

Skills refer to a template by its section name. Paths are relative to the project root. Replace everything in
`<angle brackets>`. Write in the project language (see the `Language` section). Numbers (`R-001`, `0001`) and
priorities (`MUST`, `SHOULD`, `NICE`) are never translated.

## requirements.md

- Writer: main chat. When: at brainstorming (new rows) and at wrap-up (status and evidence).
- Path: `ctx/requirements.md`
- Rules: the file only grows. Numbers never change; a cancelled requirement stays with the reason. `Intent` is written
  once at the first brainstorming; if the purpose grows, add a dated line. `Out of scope` only gets dated items.
  A MUST without a checkable criterion is not approved. `met` is written after a fresh
  reviewer's `OK` with evidence for every criterion; the owner does not have to try it. `partly met`: the owner accepts
  a result although a criterion is not met; what is missing goes to `Evidence`. A status without evidence does not count.

```markdown
# Requirements

## Intent

<2-3 sentences: what, for whom, why.>

## Out of scope

- <date>: <item>

Statuses: proposed -> approved -> met or partly met; cancelled.

| ID | Priority | Requirement | Source | Acceptance criterion | Status | Evidence |
|---|---|---|---|---|---|---|
| R-001 | MUST | <what the user can do> | <who, date> | <how a test or the owner can tell it is met> | approved | - |
```

## TASKS.md

- Writer: main chat at the end of each piece of work; the owner at any time. When: all the time.
- Path: `ctx/TASKS.md`
- Rules: it is not a log. A finished task is deleted, not ticked off. Every task says who acts and what blocks it.
  Open questions for the owner stay here until decided.

```markdown
# Tasks

**Status <date>:** <one sentence: where the project stands and what it waits for.>

| Task | Who acts | What blocks it | Inputs | Next step |
|---|---|---|---|---|
| <task, with R-number> | <Claude / owner / name> | <nothing / what> | <files, results> | <one concrete action> |
```

## architecture.md

- Writer: `worker`, in the same change as the code. Checked by `reviewer`; the owner sees the change in the summary. When: only once
  the change is in the code.
- Path: `docs/architecture.md`
- Rules: only what is true in the code today; plans do not belong here. It says "how"; "why" is a link to a decision
  record. The column "What it means for changes" is the most important one.

```markdown
# Architecture

| Section | What holds today | What it means for changes | Why |
|---|---|---|---|
| <part of the system> | <how it works now> | <what the next change must not break> | decisions/<NNNN> |
```

## decision record

- Writer: main chat prepares it, the owner decides; written at the end of brainstorming, or by the `worker` when a brief
  names it (choice made during a run). When: the choice is hard to reverse (database, boundary between
  systems, a rule that existing data must follow). Test: undoing it would mean changing or moving existing data, or
  another system. An ordinary detail (optional field, option, output format) needs no record.
- Path: `docs/decisions/NNNN-<slug>.md`
- Rules: one file per decision; numbers never change. A record is not edited, with one exception: when a new decision
  replaces it, add a line pointing to the new record and move it to `docs/decisions/archive/`.

```markdown
# <NNNN> <Decision in one sentence>

Date: <date>

## Decision

<What was decided.>

## Reason

<Why, in two or three sentences.>

## Alternative considered

- <alternative>: rejected because <reason>.

## What would change it

<The event that would make us decide again, or "nothing foreseeable".>
```

## design

- Writer: main chat at the end of brainstorming. When: shown to the owner together with the requirements.
- Path: `ctx/plans/<YYYY-MM-DD>-<slug>-design.md`
- Rules: a working document of the run. `plan` and the briefs draw from it. It is deleted with the plan at wrap-up;
  what lasts lives in `requirements.md`, `docs/decisions/` and `docs/architecture.md`. Not created for size S.

```markdown
# Design: <title>

## Intent

<What, for whom, why.>

## Goals

- <goal>

## Out of scope

- <item>

## Constraints

- <limit: time, tools, data, rules>

## Approaches considered

| Option | Chosen? | Why |
|---|---|---|
| <option A> | yes | <reason> |
| <option B> | no | <reason> |

## Open questions

| Question | Who decides |
|---|---|
| <question> | <owner / name> |

## Links

- Requirements: <R-001, R-002>
- Decision records: <NNNN or none>
```

## plan

- Writer: main chat. When: discussed in chat first; written to the file only after the owner says "go".
- Path: `ctx/plans/<YYYY-MM-DD>-<slug>.md`. Working files of the run go in the folder `ctx/plans/<YYYY-MM-DD>-<slug>/`
  (`SUMMARY.md`, `briefs/`, `review-<n>.md`).
- Rules: not changed after "go". Levels come from `models.md`. Options for the owner come with a recommendation.
  The token estimate is approximate. The plan is not project memory and is deleted at wrap-up.

```markdown
# Plan: <title>

Requirements: <R-001, R-002>
Size: <M>
Language: <language of the project documents>

| # | Step | Agent | Model level | Task | How I verify |
|---|---|---|---|---|---|
| 1 | <short name> | worker | medium | <what to do> | <command or check and expected result> |

## Choices for the owner

- <choice>: <option A / option B>. Recommended: <one>, because <reason>.

## Token estimate

About <range> tokens (rough guide).
```

## SUMMARY.md

- Writer: main chat, updated after every step. When: during the run; the final version is written at the end of `build` (End), before `wrap-up`.
- Path: `ctx/plans/<YYYY-MM-DD>-<slug>/SUMMARY.md`
- Rules: the first lines say where we stopped, so a new chat can continue from them. Evidence is a command and its
  result, not "it works". The final version has a line that the run ended and how (all steps OK, owner accepted gaps, or
  owner stopped), and the section `## Steps not done` (R-IDs; "none" if all done); `wrap-up` step 4 makes tasks from it.

```markdown
# Summary: <title>

## Where we stopped

<Step number, what is done, what is next. Updated after every step.>

## Steps done

| # | Step | Result | Evidence |
|---|---|---|---|
| 1 | <step> | <OK / FIX> | <command -> result> |

## Decisions

- <decision, who made it, date>

## Rounds of fixes

- Step <n>: round <1 or 2>, <what was wrong>, <result>.

## Steps not done

- Step <n>: <name>, R-IDs <R-001>. Final version only; write "none" if all steps are done.

## Token use

About <number> tokens (estimate <range>).

Run ended: <yes, how: all steps OK / owner accepted gaps / owner stopped>. Final version only.
```

## brief

- Writer: main chat, one per step. When: before the `worker` starts.
- Path: `ctx/plans/<YYYY-MM-DD>-<slug>/briefs/<n>-<slug>.md`
- Rules: the worker gets only what is here. List the files it may change, and what it must not touch. Contradictions
  are reported, not decided. The report is at most 20 lines.

```markdown
# Brief <n>: <step name>

## Goal

<One or two sentences.>

## Requirements

| ID | Acceptance criterion |
|---|---|
| R-001 | <criterion copied from requirements.md> |

## Earlier review

<Only for a fix round: the path of the earlier `review-<n>.md` and the list of its findings to fix. Leave out otherwise.>

## Files to change

- <path>: <why>
- `docs/architecture.md`: update if how the system works changed.

## What not to do

- Do not change `ctx/` or `docs/decisions/`, except files in the run folder that this brief names.
- Do not change files that are not listed. Do not write outside the project folder. Trial copies and helper files go only to `<run folder>/scratch/` and are deleted before the report.
- Do not decide contradictions; list them in the report.
- Refused commands: a form refusal may be rewritten once into simple single commands; a second refusal counts as denied. A refused shell edit of a project file may be done with Read, Edit or Write. Anything else denied: stop; a script or another interpreter (`python -c`, PowerShell) is a variant. List every refused command in Open with how it ended (rewritten once, done with Edit/Write, skipped). Delete only the helper files you made.

## How to verify

<Command or check, and the expected result.>

## Report format

At most 20 lines: Done / Changed files / What I did / How I verified / Open.
```

## review

- Writer: `reviewer` (a fresh one for every result and every fix). When: after each step or fix round.
- Path: `ctx/plans/<YYYY-MM-DD>-<slug>/review-<n>.md`
- Rules: the reviewer changes nothing except this file. Every criterion has a status and evidence. Check that
  `docs/architecture.md` matches the changed files and describes no plans. Verdict is `OK` or `FIX`. A status can be
  `cannot verify` (with the reason and what is needed); on a MUST it means `FIX`. The section `Earlier findings` is used
  only when checking a fix.

```markdown
# Review <n>: <step name>

| Criterion | Status | Evidence |
|---|---|---|
| <criterion from the brief> | met / not met / cannot verify | <what was checked and what came out; for `cannot verify`: the reason and what would be needed> |

## Earlier findings

<Only when checking a fix. One row for each finding of the earlier review. Leave the section out otherwise.>

| Finding | Resolved? | Evidence |
|---|---|---|
| <finding from the earlier review> | resolved / not resolved | <what was checked and what came out> |

## Architecture check

<Does docs/architecture.md match the changed files, and does it describe no plans? List differences or write "matches".>

## Findings

- <finding with file and what is wrong>, or "none".

## Verdict

OK / FIX
```

## CLAUDE.md lines

- Writer: main chat, with the owner's consent, when the project is first set up, and again after every brainstorming:
  then it sets the language line to the chosen language and adds missing lines, never duplicating a line. Path: `CLAUDE.md` in the project root.
- Rules: exactly these three lines. The second keeps other brainstorming and planning skills from taking over.
  Replace `<language>` with the chosen project language.

```markdown
Work status is in `ctx/TASKS.md`, requirements in `ctx/requirements.md`, architecture in `docs/architecture.md`.
For building and changes, follow the method of the `b6` plugin (skill `workflow`), not another brainstorming or planning skill.
Project documents are written in <language>.
```

## Language

- Default language of the templates is English. At the end of brainstorming, ask which language the project
  documents use and recommend the language of the existing documents, or the language the user writes in if there are none. Ask also when
  the project already has documents. Record the choice in the third `CLAUDE.md` line.
  If the owner picks a language different from the existing documents, those stay as they are unless the owner asks to translate them.
- The plan and the working files of a run use the same language as the documents.
- File names, numbers (`R-001`, `0001`) and priorities (`MUST`, `SHOULD`, `NICE`) are never translated. Verdicts stay `OK` / `FIX`.
- Other language than English or Slovak: translate headers, column names and statuses in the same way, and write the
  translation of the statuses into the header of `requirements.md` (the "Statuses:" line).

| English | Slovak |
|---|---|
| ## Intent | ## Zámer |
| ## Out of scope | ## Mimo rozsahu |
| ID | ID |
| Priority | Priorita |
| Requirement | Požiadavka |
| Source | Zdroj |
| Acceptance criterion | Kritérium splnenia |
| Status | Stav |
| Evidence | Dôkaz |
| Task | Úloha |
| Who acts | Kto koná |
| What blocks it | Čo ju blokuje |
| Inputs | Vstupy |
| Next step | Ďalší krok |
| Section | Kapitola |
| What holds today | Čo dnes platí |
| What it means for changes | Čo z toho vyplýva pre zmeny |
| Why | Prečo |
| Decision | Rozhodnutie |
| Reason | Dôvod |
| Alternative considered | Zvažovaná alternatíva |
| What would change it | Čo by ho zmenilo |
| **Status <date>:** | **Stav <dátum>:** |
| ## Earlier review | ## Predchádzajúca kontrola |
| ## Earlier findings | ## Predchádzajúce nálezy |
| Resolved? | Vyriešené? |
| cannot verify | nedá sa overiť |
| proposed | návrh |
| approved | schválená |
| met | splnená |
| partly met | čiastočne splnená |
| cancelled | zrušená |
