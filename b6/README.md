# b6

A Claude Code plugin that helps you build things step by step. You describe what you want.
The plugin asks questions, writes down the requirements, makes a plan, builds it with helper
agents, and wraps up with a short summary.

## Before you install

If you have the old `orchestracia` package installed, remove it first: run `/plugin`, open
the installed plugins, pick `orchestracia` and choose uninstall. If it was copied into your
project as files, delete its skills and agents from the project's `.claude/` folder. Two
plugins that do the same job, with the same agent names, will confuse Claude.

## Install

Install the plugin only the way your company approved for Claude Code plugins. If you do not know it, ask your IT
or the person who gave you the plugin before you install it.

- Approved company way: in Claude Code run `/plugin`, find `b6` in the plugin source your company set up and choose
  install. Then restart Claude Code.
- From the zip file, for trying it out: unpack the zip into a folder of your own (for example `Documents\b6`) and
  start Claude Code with `claude --plugin-dir <path to the unpacked b6 folder>`. The plugin is active only in that
  session; start it the same way each time.

Check that it works: in a new chat write "how does this work?". Claude should point you to `docs/getting-started.html`.

## What it can reach

The plugin is text only: skills, agents and guides. It has no connectors, no network access and no access to any
system. Its only hook prints one line of text at the start of a chat, so that Claude uses the `workflow` skill
before it changes files. Claude works with the access you give your own Claude Code; the plugin adds none.

## Turn it off or remove it

- Turn it off: run `/plugin`, open the installed plugins, pick `b6` and choose disable. Enable it the same way.
- Remove it: in the same menu choose uninstall. If you started it with `--plugin-dir`, just start Claude Code without
  that option and delete the folder.
- Files the plugin wrote into a project (`ctx/`, `docs/`, lines in `CLAUDE.md`) stay; they are ordinary project files.

## First use

Start Claude Code in your project and write what you want to build, in your own words.
The plugin then leads you through four stages:

1. Brainstorming - a few questions, one at a time, ending with written requirements you approve.
2. Plan - how the work will be split and checked.
3. Build - helper agents do the work and a reviewer checks it.
4. Wrap-up - a summary, and you decide what to keep.

Nothing is built before you approve the requirements and say "go" on the plan.
Small changes skip brainstorming and the plan: Claude tells you how it will check the result
and waits for your "go". A new feature or command is never a small change.

Work only in your company Claude account. Do not put personal data, whole exports, passwords or keys into the chat or
the project; made-up data is enough for trying things out.

## Guide

Start here: `docs/getting-started.html` shows how to use the plugin step by step, with a diagram (for people new to Claude Code).
The same guide is also in `docs/getting-started.en.md` / `.sk.md` (Markdown) and `docs/getting-started.en.pdf` / `.sk.pdf`
(for printing).

An illustrated guide to the project documents is in `docs/project-memory.html`.
Open it in a browser. It has a Slovak and an English version.

A one-page guide to using skills as company knowledge, not only as procedures, is in `docs/skills-as-company-knowledge.html`.
It also has a Slovak and an English version.

## License

See `LICENSE` (draft terms, to be confirmed) and `NOTICE`.
