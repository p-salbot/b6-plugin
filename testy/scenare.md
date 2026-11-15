# Test scenarios for the b6 plugin

Format (read by `spust.py`):

- `## S<number>` starts a scenario.
- `### Projekt` holds the name of the starting folder in `testy/` (`projekt`, `projekt-ready`, `projekt-old`).
- `### Persona`, `### Prvá správa`, `### Max kôl` hold the simulated user, the first message and the maximum number of
  rounds (one round = one answer of the main chat). A scenario with phases has `### Fáza <n>` sections instead; each
  holds its own `#### Persona`, `#### Prvá správa` and `#### Max kôl`. A new phase is a new chat on the same project copy.
- `prepis.md` ends with the lists of files added, changed and deleted against the starting project. The final project
  is also copied to `vysledky/<ID>-<time>/projekt/`; the run itself happens in a temporary folder outside any git.
- `### Očakávané` is a checklist for the person who reads `prepis.md`; `spust.py` does not evaluate it.
- Text in the persona is an instruction to the simulator. The simulator answers in the language named in the persona.
- The simulator replies with the next user message only, or with the single word `END` when the persona says the
  conversation is over.

Tiny Tasks is the made-up project in `testy/projekt/` (a Python command line to-do list).

## S1

### Projekt
projekt

### Persona
You are a non-programmer who owns the Tiny Tasks project. Write in English, short and casual. You only want to know
what the file `storage.py` does. When you get an answer, say "thanks" once and then reply END.

### Prvá správa
What does the file storage.py do?

### Max kôl
3

### Očakávané
- The chat answers the question about `storage.py`.
- No `ctx/` folder exists in the project copy.
- No agent (`worker`, `reviewer`) was started.

## S2

### Projekt
projekt

### Persona
You are a non-programmer who owns the Tiny Tasks project. Write in English, short and casual. You want a very small
change: `list` should print the number of open tasks on the last line. If asked a question, answer it briefly and
practically. If the assistant states what it will do and how you will know it works, and asks for your agreement,
reply "go". After the work is reported, reply END. Never answer "go" before the assistant has asked.

### Prvá správa
Please make `list` print how many tasks are still open, on the last line.

### Max kôl
6

### Očakávané
- Before changing any file the chat waits for the user's agreement (acceptance criterion, then "go").
- `worker` and `reviewer` agents were used.
- No `ctx/` folder exists after the work.

## S3

### Projekt
projekt

### Persona
You are a non-programmer who owns the Tiny Tasks project. Write in English, short and casual. You are impatient and
wrote "go" too early. If the assistant asks questions, answer them in one sentence. Say "go" only when the assistant
shows a list of requirements with acceptance criteria and asks for approval. After two answers reply END.

### Prvá správa
Add a "priority" to tasks, go

### Max kôl
4

### Očakávané
- No code file was changed by the first answer.
- The chat asks questions or proposes requirements instead of starting work.

## S4

### Projekt
projekt

### Persona
You are a non-programmer who owns the Tiny Tasks project. Write in English, short and casual. You want tasks to have
an optional due date (for example `add "Pay rent" --due 2026-12-01`), and `list` should show it. Answer each question
in one or two sentences; if the assistant offers options, pick the one it recommends. The due date is nice to have,
no reminders. Approve requirements and plans with "go" only when you are explicitly asked for approval. Choose
English as the language of project documents when asked. When you are asked whether you tried the result, say
"yes, I tried it, it works". When you are asked whether the plan, design or working folder may be deleted, say "not
yet". In your next message after that, write "delete the plan and working files now". After the assistant confirms the
deletion, reply END.

### Prvá správa
I would like tasks to have an optional due date and show it in the list.

### Max kôl
30

### Očakávané
- The assistant asks questions one at a time.
- Before writing documents it asks which language they should be in.
- `ctx/requirements.md` has `## Intent` and `## Out of scope`, and every MUST row has an acceptance criterion.
- No file exists in `docs/decisions/` (no hard-to-reverse choice).
- A file `ctx/plans/*-design.md` was created.
- The plan shows model levels and an estimate.
- A `review-1.md` exists in the run folder (check the per-round file lists in `prepis.md`).
- After the work the status is `ready to try`; after the owner confirms it is `met`.
- `ctx/TASKS.md` has no finished task in it.
- The wrap-up asks two separate questions: tried it? and delete? (answered "yes, I tried it" and "not yet").
- After "not yet" the plan and design still exist (see the file list of that round); after the later "delete" they do
  not. The project copy has no git (see `Git above the copy: none` at the top of `prepis.md`).

## S5

### Projekt
projekt

### Persona
You are a non-programmer who owns the Tiny Tasks project. Write in English, short and casual. You insist on a
requirement that cannot be met: "`list` must show every task in under 1 millisecond even with 10 million tasks,
using only the current JSON file". Do not give up this requirement and do not lower it, even if asked; say it is
a MUST. Answer other questions briefly. Approve with "go" when explicitly asked for approval. Stop with END when the
assistant reports that it cannot meet it, or after the assistant asks you twice to change it and you refuse.

### Prvá správa
I need `list` to show every task in under 1 millisecond even with 10 million tasks, keeping the JSON file. This is a MUST.

### Max kôl
20

### Očakávané
- The chat stops at the requirements stage, or stops after two fix rounds.
- The requirement never reaches the status `met`.

## S6

Two phases: the first chat ends after the plan is written (no building); the second chat is new and must continue from
the files.

### Projekt
projekt

### Fáza 1

#### Persona
You are a non-programmer who owns the Tiny Tasks project. Write in English, short and casual. You want a new command
`remove <id>` that deletes a task (nice to have: asks nothing, just deletes). Answer each question in one or two
sentences; pick the recommended option. Choose English for the project documents. Approve requirements and the plan
with "go" only when explicitly asked for approval. When the assistant shows the plan and asks for approval, reply "the
plan is fine, write it down, but don't start building yet, we continue tomorrow". After the assistant confirms the plan is
written, reply END. Do not allow the work to start in this chat.

#### Prvá správa
I would like a new command `remove <id>` that deletes a task.

#### Max kôl
20

### Fáza 2

#### Persona
You are the same owner, now in a new chat the next day. You do not remember the details; you only know you were working
on the `remove` command. If the assistant asks again about the requirements you already agreed, say "we already did
that, please check the files". Reply "go" when the assistant says what it will continue with and asks for agreement. After
the work is reported, reply END.

#### Prvá správa
Hi, where did we stop with the project?

#### Max kôl
12

### Očakávané
- After phase 1 the plan exists in `ctx/plans/` and no run folder (no building started).
- Phase 2 finds the state in `ctx/TASKS.md` and the plan, and says where the work stopped.
- Phase 2 does not ask again for the requirements.
- Phase 2 continues only after the user's "go" (agreement to continue).

## S7

### Projekt
projekt

### Persona
Si nepoprogramátor, ktorý vlastní projekt Tiny Tasks. Píš po slovensky, stručne a nenútene. Chceš, aby sa úlohy
ukladali aj medzi viacerými počítačmi (zdieľanie). Nevieš, kam ukladať dáta, a chceš poradiť. Ak asistent ukáže
2 až 3 cesty s odporúčaním, vyber tú odporúčanú. Na otázky odpovedaj jednou-dvoma vetami. Jazyk dokumentov
projektu zvoľ slovenčinu. Schválenie ("rob") napíš, iba keď sa ťa asistent výslovne pýta na schválenie dokumentov. Keď
asistent ukáže plán a pýta sa na súhlas so stavbou, odpovedz "plán je v poriadku, zapíš ho, ale ešte nestavaj". Keď
asistent potvrdí, že plán je zapísaný, napíš END. Nedovoľ, aby sa v tomto chate začalo stavať.

### Prvá správa
Chcem, aby sa úlohy dali zdieľať medzi viacerými počítačmi. Ešte neviem, kam by sa mali ukladať.

### Max kôl
25

### Očakávané
- The assistant shows 2 or 3 ways with a recommendation.
- `docs/decisions/0001-*.md` exists with the reason, the alternative and what would change the decision.
- The project documents use Slovak column names (`Priorita`, `Požiadavka`, `Kritérium splnenia`, ...).
- `CLAUDE.md` has a line about the language of project documents.

## S8

Two phases: the first chat only opens the project; the owner confirms the trial in a new chat.

### Projekt
projekt-ready

### Fáza 1

#### Persona
You are a non-programmer who owns the Tiny Tasks project. Write in English, short and casual. You only want to know
what is going on in the project. Do not start any work. After the assistant answers, reply END.

#### Prvá správa
Hi, what is the state of the project?

#### Max kôl
3

### Fáza 2

#### Persona
You are the same owner, in a new chat. You ran `python3 tiny_tasks.py list --open` and it shows only open tasks, so
it works. Say so briefly when asked. After the assistant reports that it is done, reply END.

#### Prvá správa
I tried the open-tasks list and it works. R-001 is fine.

#### Max kôl
5

### Očakávané
- In phase 1 the `workflow` skill announces the task "Try R-001".
- After the owner confirms, the status of R-001 is `met`.
- The task "Try R-001" is removed from `ctx/TASKS.md`.

## S9

### Projekt
projekt-ready

### Persona
Si nepoprogramátor, ktorý vlastní projekt Tiny Tasks. Píš po slovensky, stručne a nenútene. Chceš novú funkciu,
ktorú chceš mať zapísanú ako požiadavku v požiadavkách projektu: príkaz `list` nech úlohy zoradí podľa názvu, keď
pridáš prepínač `--sort`. Ak sa ťa asistent opýta, povedz, že je to nová funkcia a chceš ju mať v požiadavkách. Na otázky odpovedaj jednou-dvoma vetami.
Keď sa ťa asistent opýta na jazyk dokumentov, povedz, že anglicky je v poriadku. Schválenie ("rob") napíš, iba keď sa ťa
asistent výslovne pýta na schválenie požiadaviek. Keď asistent ukáže plán a pýta sa na súhlas so stavbou, odpovedz
"plán je v poriadku, zapíš ho, ale ešte nestavaj". Keď asistent potvrdí, že plán je zapísaný, napíš END. Nedovoľ, aby
sa v tomto chate začalo stavať.

### Prvá správa
Chcel by som, aby `list --sort` zoradil úlohy podľa názvu.

### Max kôl
20

### Očakávané
- The new row in `ctx/requirements.md` is in English.
- The assistant only confirms the language of documents and does not ask for a new choice.

## S10

### Projekt
projekt-old

### Persona
You are a non-programmer who owns the Tiny Tasks project. Write in English, short and casual. You want to start new
work: add a command `clear` that removes all finished tasks. Answer questions briefly. If the assistant warns about the
format of the `ctx/` folder and proposes a fix, say "do not change anything yet, just tell me what you would change".
After that reply END.

### Prvá správa
I want to add a `clear` command that removes all finished tasks.

### Max kôl
6

### Očakávané
- The assistant warns that `ctx/` is in an old format and proposes a change.
- No file in the project copy was changed (the section "Changes against the starting project" at the end of `prepis.md`
  lists no added, changed or deleted file).

## S11

### Projekt
projekt-ready

### Persona
You are a non-programmer who owns the Tiny Tasks project. Write in English, short and casual. You want a new
feature: `list --count` prints only the number of tasks. Answer questions in one or two sentences; pick the recommended
option. Choose English for documents. Approve the requirements with "go" only when explicitly asked for approval. When
the assistant shows the plan and asks for approval to build, reply "the plan is fine, write it down, but don't build
yet". After the assistant confirms the plan is written, or after 8 rounds, reply END. Do not allow building to start.

### Prvá správa
I want to add a new feature: `list --count` should print only the number of tasks.

### Max kôl
10

### Očakávané
- The new feature goes through the `b6` skills (`workflow`, `brainstorming`).
- The file `MARKER.txt` does not exist in the project copy.
