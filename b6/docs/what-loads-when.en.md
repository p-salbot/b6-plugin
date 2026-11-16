*Guide · b6 plugin*

# What loads when

In one chat, Claude keeps in mind only what was loaded into it. When the context fills up, work gets slower, costs more and makes more mistakes. So the b6 plugin loads many things only at the moment they are really used.

## Six terms

*Always*

### Context

Everything Claude holds in mind in one chat: your messages, its answers, files it read, command outputs. It grows with every message; it shrinks only when it is compacted or in a new chat. A full context means slower, more expensive work and more mistakes. That is why it is better to read little, and only when needed.

*When used*

### Skill

A text file with a procedure. Its short description (in the header) is always visible to Claude. The whole `SKILL.md` body loads only when the description fits your request. A plain question that changes no file does not need it; questions about the work or the method ("what is in progress", "where are we", "how does this work") do load `workflow`.

*In one step*

### Reference

A file a skill opens only in the step that needs it: `templates.md` (shapes of documents) and `models.md` (model levels and token estimate) in the skill `workflow`. For a clear small change it is never opened.

*Own context*

### Agent

`worker` and `reviewer`. Each starts with a fresh context: it does not see the chat; besides its own instructions (`agents/<name>.md`) and the project `CLAUDE.md` it gets only the brief. It returns at most 20 lines, so the main chat does not fill up. The reviewer is always new and did not see the worker's work.

*At start*

### SessionStart hook

One line added at the start of the chat: the plugin is active and the skill `b6:workflow` must be loaded before any file is changed. Nothing else is loaded by it.

*As needed*

### Project files

`CLAUDE.md` is always loaded. The folders `ctx/` (requirements, tasks, plans) and `docs/` (architecture, decisions) are read only when a step needs them.

## What is in context at which moment

Example: one change of size M, from the start of the chat to wrap-up. The main chat is the context that grows. Agents work in their own context and return only a short report to the main chat.

| Moment | Added to the main chat | Not loaded |
|---|---|---|
| Start of chat | **always** `CLAUDE.md`, short descriptions of skills and agents, the SessionStart hook line | skill bodies, references, `ctx/`, `docs/` |
| Request for a change | **skill** body of `workflow`, which at the start reads `ctx/TASKS.md` if it exists; then, for size M, skill `brainstorming` | `plan`, `build`, `wrap-up`, agents |
| Brainstorming | **reference** `templates.md` when requirements are written; **files** `ctx/`, `docs/` and existing code related to the topic; at the end it asks for the document language and, after approval, writes `ctx/`, `docs/` and the `CLAUDE.md` lines from `templates.md` | `models.md` |
| Plan | **skill** body of `plan`; **files** `ctx/requirements.md` and the design `ctx/plans/<date>-<slug>-design.md`; **references** `templates.md` and `models.md` (levels and token estimate) | body of `build`, agents |
| Build step | **skill** body of `build`; **reference** `templates.md` (brief, review, `SUMMARY.md`); the plan and `SUMMARY.md`; the main chat runs the check itself; from `worker` only the report (at most 20 lines) | other steps; the worker's own work |
| Review | in the main chat from `reviewer` only the verdict, numbered findings and the path to the file `review-<n>.md` | what the reviewer read |
| Wrap-up | **skill** body of `wrap-up`; **reference** `templates.md`; files to update (`ctx/requirements.md`, `ctx/TASKS.md`, `docs/architecture.md`); the run's `review-<n>.md` and `SUMMARY.md`; `met` is set only after `OK` from a fresh reviewer | `models.md`; agents only if architecture or links need a fix |

For a small change of size S (one or two existing files), brainstorming, the plan and the templates are not read, no files in `ctx/` are created and `ctx/TASKS.md` is not changed. `workflow` (which reads `ctx/TASKS.md` at the start if it exists), the change by `worker` and the check by `reviewer` are enough. Evidence goes into `ctx/requirements.md` only if the change touches a requirement that is already there.

## What follows from this

- A long chat makes work slower and more expensive. Start a new task in a new chat; the continuation is in `SUMMARY.md` and in `ctx/`.
- The description of a skill decides whether the skill opens. That is why it holds words people really use.
- One step is done by an agent with a fresh context: it does not see the chat, so the brief must be complete.
- Only what is always true belongs in `CLAUDE.md`. What holds for one piece of work belongs in a skill or in a document in `ctx/` or `docs/`.

---

Internal · @panthea.sk
