---
name: workflow
description: Entry point of the b6 method. Use it BEFORE creating, changing or deleting any file in the project, even for a one-line change and even when the message already says "go". Also use it for every request to build something, change something, add a feature or command, fix behaviour, continue earlier work, "what is in progress", "where are we", "how does this work", and at the start of a new chat in a project that has ctx/TASKS.md. In a project that uses b6, this skill is used INSTEAD of any other brainstorming or planning skill. Not for plain questions that change no file. Slovak triggers - postaviť, vytvoriť, pridať funkciu, pridať príkaz, zmeniť, upraviť, opraviť, pokračuj, čo je rozrobené, kde sme, nový chat, ako to funguje, rob, go.
---

# workflow

You lead the work in a project that uses the b6 method. Load this skill before the first change to any project file,
however small, and use b6 skills, not other brainstorming or planning skills. Talk to the owner in the language they write in. Keep it plain; the owner is not a programmer.
Consent means the meaning, in any language ("go", "yes, build it", "rob").

## Hard rules (they apply to every b6 skill)

1. Build nothing until the owner has approved the requirements and said "go" to the plan (size S: "go" to the
   criterion in chat). A "go" in the first message, or before the requirements are approved, builds nothing: ask, or
   propose requirements.
2. The main chat does no work or fixes itself. The `b6:worker` agent does them from a brief.
3. A fresh `b6:reviewer` checks every result and every fix. At most two rounds of fixes (first `medium`, then `strong`),
   then stop and report to the owner.
4. A MUST requirement without evidence is not done. "met" is written only after the owner tried it.
5. The main chat does not decide for the owner. Conflicts and choices are listed with a recommendation.
6. Models only by level (see `references/models.md`). If the main chat is not on a strong model, say so before the plan.
7. The state of the work lives only in project files (`ctx/`, `docs/`), never in Claude's memory.

## Start

1. If `ctx/TASKS.md` exists, read it. Say in two or three sentences where the project stands and what waits for the owner.
2. A task for the owner such as "Try R-001": tell the owner what to try. After they answer, hand over to `wrap-up`.
3. A plan file `ctx/plans/<date>-<slug>.md` (not `*-design.md`) or `SUMMARY.md` exists, its requirements are not yet
   `ready to try`, `partly met` or `met`, and this is a new chat: say where the work stopped; continue after the owner agrees.
4. A plan, design or run folder whose requirements are `ready to try`, `partly met` or `met` is a leftover, not work in
   progress: never continue or rebuild it. Say so and offer to delete it (skill `wrap-up`, step 6).
5. Read project documents only as needed; do not read everything.

## Size

| Size | When | Way |
|---|---|---|
| S | small change to existing behaviour in 1-2 files, no new requirement, done in this chat | no brainstorming, no plan file, no `ctx/`: criterion in chat, owner says "go", worker, reviewer, then write down |
| M | new feature or command, several files, unclear request, work that continues later | full way below |

- A new feature or a new command is always M, however small. When in doubt, it is M. The owner may change the size.
- S that changes the criterion of an existing requirement, or needs a new one, is M. S cannot be paused: if the owner
  wants to continue later, switch to M, so that the agreement is written to `ctx/`.
- S write-down: the worker updates `docs/architecture.md` in the same brief if behaviour changed (if `docs/` does not
  exist, skip it and tell the owner); evidence on the requirement it touches. Nothing in `ctx/TASKS.md`. Tell the owner what to try.
- Questions, typos and formatting are not work for this method: just do them.

## Which skill is next (size M)

- Requirements not approved yet: `brainstorming`.
- Requirements approved, no plan: `plan`.
- Plan file `ctx/plans/<date>-<slug>.md` written, requirements still open (not a leftover, Start point 4): `build`.
- All plan steps OK: `build` hands over to `wrap-up`.

## First use in a project

Templates are read from the folder of this skill in the plugin (`references/templates.md`), not from the project.
Only say in a few lines what will be created (`ctx/` and `docs/` from the templates, lines in the project `CLAUDE.md`)
and ask for consent. The same message has at most one question about the request; more come one per message. Do not create the files now: skill `brainstorming` creates them at the end, in the language the owner chooses.
For size S `ctx/` is not created; `docs/architecture.md` is touched only if it exists or the owner wants it.

## Old or incomplete `ctx/`

Signs: a summary file with a Slovak name, `- [x]` ticks for done work, decisions inside `requirements.md`, column
names that are in neither list of the templates (both the English and the Slovak names there are fine), or a missing file. Do not convert and do not overwrite. Say what you found, propose changes according to the templates,
and change nothing without consent.

## Language of documents

Existing documents decide the language. If they differ from the language the owner writes in, only confirm it with one
question. Do not mix languages in the documents.

## Context

When the context is more than half full, or after a large step, write the state to `ctx/TASKS.md` (and `SUMMARY.md` of the run) and suggest a new chat.

## How does this work

For "how does this work", point first to `../../docs/getting-started.html`; for the project documents to `../../docs/project-memory.html` (paths from this skill's folder).
