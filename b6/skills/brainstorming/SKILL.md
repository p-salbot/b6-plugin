---
name: brainstorming
description: Turns an idea into approved requirements before anything is planned or built. Use when the request is vague, big, or has no measurable result (size M), or when the owner says "let's clarify this", "brainstorming", "help me write the task". Slovak triggers - poďme si to ujasniť, brainstorming, pomôž mi sformulovať zadanie, čo vlastne chcem, nový nápad, nová funkcia, požiadavky.
---

# Brainstorming: from idea to approved requirements

The hard rules in skill `workflow` apply. If it is not loaded yet, load it first.
Templates are read from the folder of skill `workflow` in the plugin (`../workflow/references/templates.md`), not from
the project. Refer to a template by its section name.

This skill does not write code, does not write the plan and does not build trial versions. "go" said during
brainstorming means "yes, write the documents", never "build it".

## 1. Look first

Before the first question, read what the project already has: `ctx/`, `docs/`, `CLAUDE.md`, existing skills and code.
If something similar already exists, or the idea is not worth the effort, say so and let the owner decide.

## 2. First message

Write the request in your own words and what you found. Or, if you cannot even do that, ask one open question and say
why you ask it.

## 3. Ask well

- One question per message.
- Until you know why the owner wants this, ask open questions without a list of options.
- After that, offer concrete options with your recommendation.
- Ask only what changes the result. For everything else make your own proposal and mark it as a proposal.
- From time to time sum up what you understood so far and ask: "What is wrong or missing?"

## 4. Hard-to-undo choices

Where to keep data, a border between systems, a rule over data: show two or three ways with a recommendation. After the
owner chooses, note the decision and record it at the end (step 7) as `docs/decisions/NNNN-<slug>.md` with the reason,
the alternative and what would change it (section `decision record`). An ordinary technical detail gets no record.

## 5. Requirements

- Every requirement has an ID (`R-NNN`), a priority, a source and an acceptance criterion someone can check.
- A MUST without a checkable criterion is not approved: ask for the criterion.
- If a MUST cannot be met, say so plainly and do not write it as approved. Offer to change it or to move it down.

## 6. Show everything at once

When the picture is clear, show in the chat in one message: intent, out of scope, the requirements (priority, source,
criterion), decisions, open questions, and a short design (goals, constraints, approaches considered and why one was
chosen). Then ask which language the project documents use. Suggest the language the owner writes in. In a project
that already has documents, only confirm their language (section `Language`).

## 7. After approval

Write, in the project language. Create `ctx/` and `docs/` now from the templates (`requirements.md`, `TASKS.md`,
`architecture.md`, `docs/decisions/`), only the files that are still missing:

1. `ctx/requirements.md` (section `requirements.md`): header plus new rows with status `approved`. `Intent` is written
   once; later brainstorming never changes it (add a dated line if the purpose grew). `Out of scope` only gets dated items.
2. Decision records, if any were made.
3. Open questions into `ctx/TASKS.md` (section `TASKS.md`), with who decides.
4. The design to `ctx/plans/<YYYY-MM-DD>-<slug>-design.md` (section `design`).
5. The lines in `CLAUDE.md` (section `CLAUDE.md lines`), including the document language.

If the language is not English or Slovak, translate as the section `Language` says.
Then hand over to skill `plan`.
