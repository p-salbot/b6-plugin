# b6

A Claude Code plugin that helps you build things step by step. You describe what you want.
The plugin asks questions, writes down the requirements, makes a plan, builds it with helper
agents, and wraps up with a short summary.

## Before you install

If you have the old `orchestracia` package installed, remove it first. It is not a plugin: it was copied into your
user folder `%USERPROFILE%\.claude\` (on macOS `~/.claude/`). Ask Claude: "Uninstall the orchestracia package according
to its README.md", or delete by hand the skill and the two agents its README lists, and the block between the
`orchestracia` markers in that folder's `CLAUDE.md`. Keep the `ctx/` folders in your projects. Then restart Claude Code
and check in `/skills` and `/agents` that the old skill and agents are gone. Two methods that do the same job will
confuse Claude.

The same goes for the English version of that package, `orchestration`. It is copied the same way into
`%USERPROFILE%\.claude\` and has one skill, two agents (`worker.md` and `reviewer.md`, the same file names as the b6
agents) and a block between its own `orchestration` markers in that folder's `CLAUDE.md`. Ask Claude: "Uninstall the
orchestration package according to its README.md", or delete those by hand. Remove it before you install b6.

## Install

Install the plugin only the way your company approved for Claude Code plugins. If you do not know it, ask your IT
or the person who gave you the plugin before you install it.

- Approved company way: in Claude Code run `/plugin`, find `b6` in the plugin source your company set up and choose
  install. Then restart Claude Code.
- a) From the zip file: unpack the zip into a folder of your own (for example `Documents\b6-0.1.0`). It holds the
  folder `.claude-plugin` (the plugin source `panthea`) and the folder `b6` (the plugin). In Claude Code run:
  1. `/plugin marketplace add <path to the unpacked folder>` (the folder that holds `.claude-plugin`, not `b6`)
  2. `/plugin install b6@panthea`
  3. Restart Claude Code.

  New version: unpack the new zip into the same folder, run `/plugin marketplace update panthea`, then `/plugin`,
  pick `b6` and update it.
- b) From GitHub: the plugin source is the private repository `p-salbot/b6-plugin`. You need access to it (ask the
  person who gave you the plugin) and Git signed in to GitHub on your computer. In Claude Code run:
  1. `/plugin marketplace add p-salbot/b6-plugin`
  2. `/plugin install b6@panthea`
  3. Restart Claude Code.

  New version: run `/plugin marketplace update panthea`, then `/plugin`, pick `b6` and update it. You do not need
  a new zip.
- For trying it out without installing: start Claude Code with `claude --plugin-dir <path to the unpacked b6 folder>`.
  The plugin is active only in that session; start it the same way each time.

Check that it works: in a new chat write "how does this work?". Claude should point you to `docs/getting-started.html`.

## What it can reach

The plugin is text only: skills, agents and guides. It has no connectors, no network access and no access to any
system. Its only hook prints one line of text at the start of a chat, so that Claude uses the `workflow` skill
before it changes files. Claude works with the access you give your own Claude Code; the plugin adds none.

## Turn it off or remove it

- Turn it off: run `/plugin`, open the installed plugins, pick `b6` and choose disable. Enable it the same way.
- Remove it: in the same menu choose uninstall. If you started it with `--plugin-dir`, just start Claude Code without
  that option and delete the folder. To remove the plugin source too, run `/plugin marketplace remove panthea`.
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
Every guide in `docs/` is also there as Markdown (`<name>.en.md`, `<name>.sk.md`) and as PDF for printing
(`<name>.en.pdf`, `<name>.sk.pdf`).

An illustrated guide to the project documents is in `docs/project-memory.html`.
Open it in a browser. It has a Slovak and an English version.

A guide to using skills as personal and company knowledge, not only as procedures, is in `docs/skills-as-personal-and-company-knowledge.html`.
It also has a Slovak and an English version.

A short guide to what Claude loads and when (context, skills, references, agents, the start hook, project files) is in `docs/what-loads-when.html`.
It also has a Slovak and an English version.

## License

See `LICENSE` and `NOTICE`.
