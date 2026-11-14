# Model levels

Skills, plans and briefs name a **level**, never a model. This file is the only place that maps levels to models.
Agent files carry the short model name (`opus`, `sonnet`, `haiku`), not an exact version ID.

| Level | Model | Used by |
|---|---|---|
| strong | `opus` | main chat, `reviewer`, `worker` on a hard step and in the second fix round |
| medium | `sonnet` | `worker` (default), first fix round |
| cheap | `haiku` | nobody for now |

## Default level per role

- Main chat: strong. It talks to the owner, decides what goes into the plan and reads every agent report.
- `worker`: medium. Use strong when the step is hard (unclear rules, many files, risky change). Write the level in the plan.
- `reviewer`: strong, always. A fresh reviewer checks every result and every fix.
- Cheap is not assigned. If you want to use it, put it in the plan as an owner choice with a reason.

## Fix rounds

At most two rounds of fixes per step, each checked by a fresh `reviewer`:

1. Round 1: `worker` at medium level.
2. Round 2: `worker` at strong level.
3. Still not `OK` after round 2: stop and report to the owner what is wrong. Do not start a third round.

## If the model cannot be chosen

Sometimes the model of an agent cannot be set (an older Claude Code version, or the account does not offer it).
Then the agent runs on the model of the main chat. Tell the owner this in one sentence before the plan, for example
"Agents will run on the same model as this chat." Do not hide it and do not change the plan silently.
If the main chat itself is not on a strong model, say so before the plan as well.

## Token estimate

Rough guide only; real use depends on the project.

| Size | Typical use |
|---|---|
| S | about 50-150k tokens |
| M | about 300-700k tokens |

Put an estimate in every plan and mark it as approximate. After the work, write the real use into `SUMMARY.md`.
