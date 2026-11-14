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

Pick one way:

- In Claude Code, run `/plugin` and add this plugin. TODO: Panthea will add the exact
  approved steps here.
- For a quick test, start Claude Code with `claude --plugin-dir <path to the b6 folder>`.

## First use

Start Claude Code in your project and write what you want to build, in your own words.
The plugin then leads you through four stages:

1. Brainstorming - a few questions, one at a time, ending with written requirements you approve.
2. Plan - how the work will be split and checked.
3. Build - helper agents do the work and a reviewer checks it.
4. Wrap-up - a summary, and you decide what to keep.

Nothing is built before you approve the requirements and say "go" on the plan.
Small changes skip brainstorming and the plan: Claude tells you how it will check the result
and waits for your "go".

## Guide

Start here: `docs/getting-started.html` shows how to use the plugin step by step, with a diagram (for people new to Claude Code).

An illustrated guide to the project documents is in `docs/project-memory.html`.
Open it in a browser. It has a Slovak and an English version.

A one-page guide to using skills as company knowledge, not only as procedures, is in `docs/skills-as-company-knowledge.html`.
It also has a Slovak and an English version.

## License

See `LICENSE` (draft terms, to be confirmed) and `NOTICE`.
