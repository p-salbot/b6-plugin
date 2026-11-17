# Walkthrough: rebuilding an old VBA tool with Claude Code and the b6 method

This is a recorded Claude Code session that rebuilds a small old Access/VBA tool as a new Python tool, using the b6 plugin method: brainstorming, requirements, plan, build with worker and reviewer agents, and wrap-up. The old tool is invented for this example and all data is synthetic. The project folder started with only old/ReorderSettings.bas and a one-line CLAUDE.md. The finished project is here: <https://github.com/p-salbot/b6-plugin/tree/main/examples/reorder-settings>.

Each step shows what the owner typed, what happened, and Claude's final reply in that step. The full console output of every step is in walkthrough.html (same folder).

## The old tool: old/ReorderSettings.bas

```vb
Attribute VB_Name = "ReorderSettings"
Option Compare Database
Option Explicit

' Reorder settings per item. Table: tblReorder(ItemNo, MinQty, ReorderQty, Supplier)

Public Sub ShowReorder(ByVal itemNo As String)
    Dim rs As DAO.Recordset
    Set rs = CurrentDb.OpenRecordset( _
        "SELECT * FROM tblReorder WHERE ItemNo = '" & itemNo & "'")
    If rs.EOF Then
        MsgBox "Item not found"
    Else
        MsgBox rs!ItemNo & ": min " & rs!MinQty & ", reorder " & rs!ReorderQty & ", " & rs!Supplier
    End If
    rs.Close
End Sub

Public Sub SaveReorder(ByVal itemNo As String, ByVal minQty As Long, _
                       ByVal reorderQty As Long, ByVal supplier As String)
    Dim db As DAO.Database
    Set db = CurrentDb
    db.Execute "DELETE FROM tblReorder WHERE ItemNo = '" & itemNo & "'"
    db.Execute "INSERT INTO tblReorder (ItemNo, MinQty, ReorderQty, Supplier) VALUES ('" & _
        itemNo & "', " & minQty & ", " & reorderQty & ", '" & supplier & "')"
End Sub
```

## Step 1: Start: read the old code

**You (owner):**

> I'm new to Claude Code. I have an old Access tool. The VBA module old/ReorderSettings.bas reads and writes one table with reorder settings per item (minimum stock, reorder quantity, supplier). I want to rebuild it as a small, simple tool that another person can maintain too. First read the old code and tell me in plain words what it does. Then help me write down the requirements for the new tool. Don't build anything yet.

**What happens:** The owner describes the old tool in plain words and says what they want. Claude reads the VBA module, explains it in plain words and points out its weak spots. Before writing any file it loads the b6 method (skill `b6:workflow`) and asks for consent to create the project documents. Then it asks the first question.

**Claude (final reply):**

```text
What the old code does, in plain words

The module works with one table, tblReorder. Each row is one item and holds
four things:

┌────────────┬─────────────────────────────────────────────────────────────┐
│   Field    │                           Meaning                           │
├────────────┼─────────────────────────────────────────────────────────────┤
│ ItemNo     │ the item number (text)                                      │
├────────────┼─────────────────────────────────────────────────────────────┤
│ MinQty     │ the minimum stock: when stock falls below this, you should  │
│            │ reorder                                                     │
├────────────┼─────────────────────────────────────────────────────────────┤
│ ReorderQty │ how many to order each time                                 │
├────────────┼─────────────────────────────────────────────────────────────┤
│ Supplier   │ who you order from                                          │
└────────────┴─────────────────────────────────────────────────────────────┘

It can do only two things:

1. Show an item (ShowReorder): you give it an item number and it looks the
   item up. If it finds it, a pop-up shows something like "A-100: min 5,
   reorder 20, Acme". If not, a pop-up says "Item not found".
2. Save an item (SaveReorder): you give it the item number and the three
   values. It deletes any existing row for that item, then inserts a new one.
   So it either creates a new item or overwrites an old one.

That's all of it. It does not do these things:
- show a list of all items
- delete an item on purpose
- check the values (a minimum of -5 or a supplier left empty is accepted)
- calculate anything (it only stores the settings and never looks at actual
  stock)

Weak spots worth fixing in the new tool:
- An apostrophe breaks it. Text is glued straight into the database command,
  so a supplier like O'Brien makes saving fail. The same flaw also lets
  someone tamper with the command on purpose.
- A failed save can lose data. Saving first deletes the row, then inserts the
  new one. If the insert fails, the old settings are gone and nothing replaces
  them.
- Messages only appear as pop-ups. That's awkward to use and hard to test.

Next: writing down the requirements

This project uses the b6 method. So before we write requirements, I need your
OK to set up a few files. They'll be created at the end of our requirements
talk, not now:
- a ctx/ folder for the requirements, the task list and later the plans
- a docs/ folder for a short description of how the tool works, which helps
  the next person maintain it
- a few lines added to CLAUDE.md about how we work and which language the
  documents use

Nothing gets built until you approve the requirements and then the plan.

Is it OK to set up these files? Once you say yes, we'll go through the
requirements one question at a time. The first one:

Who will use the new tool, and how? For example: only you on one computer, or
several people sharing the same data.
```

## Step 2: Consent

**You (owner):**

> Yes, go ahead

**What happens:** The brainstorming skill loads. From now on Claude asks one question per message.

**Claude (final reply):**

```text
Thanks. The files will be created at the end of our talk, once you've approved
the requirements.

I checked the project folder. Besides the old module there's nothing yet: no
requirements, docs or other code. So we start from a clean slate.

We'll go one question at a time. The question from before is still open, and
it matters most because it decides where the data lives and what kind of tool
fits:

Who will use the new tool, and how? For example: only you on one computer, or
several people sharing the same data. It also helps to know whether the
current Access database is still used for other things, or only for these
reorder settings.
```

## Step 3: Who uses it

**You (owner):**

> Mostly me, on my own PC. Sometimes a planner looks up an item, but only one person uses it at a time. The Access database is only for these reorder settings, nothing else.

**What happens:** The answer decides what kind of storage fits: one person on one PC needs no server.

**Claude (final reply):**

```text
Got it. The tool is used mainly by you on your PC, sometimes a planner looks
something up, only one person at a time, and the Access database holds nothing
except these settings. That keeps things simple: we don't need a server or
multi-user locking, and the old database doesn't need to stay around for
anything else.

Next question:

What made you want to rebuild it? What bothers you about the old tool today,
or what should the new one do better? For example the pop-ups, missing
features, dependence on Access, or that nobody else can maintain VBA. Tell me
in your own words.
```

## Step 4: Why rebuild

**You (owner):**

> Only I understand the Access file and the VBA. If I'm away, nobody can fix or change it. I want it documented and easy to change. Also, I'm not sure the save always works: once an item seemed to disappear after an error

**What happens:** The owner knows the symptom (an item disappeared), not the cause. Claude connects it to the old code: the save deletes first and inserts second. A choice that is hard to undo (where the data lives) gets options and a recommendation.

**Claude (final reply):**

```text
That clears it up, and your memory of the disappearing item is probably right.
The old save works in two separate steps: first it deletes the item, then it
writes it back. If the second step fails (for example because of an apostrophe
in the supplier name, like O'Brien), the delete has already happened and the
item is gone. The new tool has to make saving all-or-nothing: either the new
values are stored, or the old ones stay untouched.

So the goals are:
1. Someone other than you can understand it, fix it and change it.
2. It's documented.
3. Saving never loses data.

The next question is a choice that would be hard to undo later, so I'll give
you options:

Where should the reorder settings be stored in the new tool?

Option: A. A small database file (SQLite) + a small Python tool (my
  recommendation)
What it is: One file on your PC, like the Access file now, but it needs no
  Access.
For: Built-in all-or-nothing saving. It can reject bad values such as
  negative quantities or two rows for the same item. It's free and common,
  so plenty of people know it.
Against: You need the tool (or a free viewer) to look inside the file.
────────────────────────────────────────
Option: B. A plain table file (CSV) + a small Python tool
What it is: A text file that opens in Excel.
For: It's the most transparent option: anyone can open the data.
Against: Safe saving has to be built by hand. If someone edits the file in
  Excel, it can quietly break the data, for example by dropping leading
  zeros from item numbers like 00123.
────────────────────────────────────────
Option: C. Keep Access and only fix and document the VBA
What it is: The same file, with corrected code.
For: It's the smallest change.
Against: It doesn't fix the main problem: other people still need Access and
  VBA skills.

I recommend A. It fixes the lost-save problem at the root, it stays a single
file on your PC, and the code around it stays short and easy to read. If you
want, the tool can also export to a CSV file for viewing in Excel.

Which do you choose: A, B or C? (Or tell me if something important is
missing.)
```

## Step 5: Decision: where the data lives

**You (owner):**

> A. SQLite and a small Python tool. I don't want people editing the data in Excel.

**What happens:** The owner picks SQLite and gives a reason. This becomes a decision record in docs/decisions/.

**Claude (final reply):**

```text
Noted: SQLite + a small Python tool, with no editing in Excel. That also means
we skip the CSV export. I'll write this choice down as a decision record at
the end.

Next question: How do you and the planner want to work with the tool?

Option: A. A simple window (my recommendation)
What it looks like: A small program window: a field for the item number, the
  three values, Save and Delete buttons, and a list of all items.
For: It's easy for you and the planner, with no commands to remember. Python
  has this built in, so there's nothing extra to install.
Against: It's slightly more code than option B.
────────────────────────────────────────
Option: B. Commands in a terminal
What it looks like: You type something like reorder show A-100 or reorder
  save A-100 --min 5 ....
For: It's the least code and the easiest to test.
Against: It's unfriendly for a planner who only looks things up now and
  then.
────────────────────────────────────────
Option: C. A small page in the browser
What it looks like: It runs on your PC and you open it in Chrome or Edge.
For: It looks modern.
Against: It needs a small background server and an extra library, so there's
  more to understand and maintain.

I recommend A. Either way, I'd keep the part that stores and checks the data
separate from the window, so it can be tested on its own and the window can be
swapped out later if needed.

Which do you prefer: A, B or C?
```

## Step 6: Decision: how to use it

**You (owner):**

> B. Commands in a terminal are fine for now. The planner can ask me. Keep it small.

**What happens:** The owner does not take Claude's recommendation (a window) and picks terminal commands to keep it small. Claude accepts it and sums up what it understood, asking: what is wrong or missing?

**Claude (final reply):**

```text
Noted: terminal commands, kept small.

Here's a summary of what I've understood so far. Items marked (proposal) are
my suggestions for details you haven't decided yet.

Purpose: replace the Access/VBA tool with a small Python tool that someone
else can understand, fix and change, that is documented, and that never loses
data when saving.

Decided:
- The data lives in one SQLite file on your PC. It's used by one person at a
  time and is never edited in Excel.
- The tool is used through terminal commands.

Commands (proposal):
- show <item>: shows the settings for one item, or says clearly that the item
  doesn't exist.
- save <item> --min … --reorder … --supplier …: creates an item or updates it.
  All-or-nothing: if anything fails, the old values stay.
- list: shows all items in a table. This is new; the old tool had no list.
- delete <item>: removes an item on purpose. Also new.
- import <file.csv>: a one-time move of the existing data. You export
  tblReorder from Access to CSV (Access has a menu for this), and the tool
  loads it in. It refuses if the database already contains items, so nothing
  gets overwritten by accident.

Checks when saving (proposal):
- The item number and supplier must not be empty. Spaces at the start and end
  are removed.
- Minimum stock must be 0 or more, and reorder quantity must be 1 or more.
  Both must be whole numbers.
- Item numbers match regardless of upper/lower case (a-100 = A-100), the same
  as in Access.
- Names with apostrophes, like O'Brien, work.
- A bad input gives a clear message and changes nothing.

For the next maintainer (proposal):
- a short README: how to install, how to run, the commands
- a short description of how the tool is built
- automatic tests that someone can run with one command

Not included (proposal): a window or web page, multiple users at the same
time, any calculation from actual stock levels, CSV export, and the Access
file itself (it can be archived after the import).

Open question: Is Python installed on your PC, and on the PC of whoever would
maintain it? We can check that later.

What is wrong or missing?
```

## Step 7: Scope cut

**You (owner):**

> Looks good. Two changes: no delete and no import for now. Keep only show, save and list. I'll type the few items in by hand. Python is installed on my PC.

**What happens:** The owner removes delete and import. Claude shows the full picture at once: purpose, what is not included, requirements R-001 to R-010 with a checkable criterion each, the decision, a short design and open questions. Then it asks for the language of the documents.

**Claude (final reply):**

```text
Noted: only show, save and list. No delete, no import; you'll type the items
in by hand. Python is installed on your PC.

Here's the full picture to check before I write anything down.

Purpose

A small Python tool, used from the terminal, that stores the reorder settings
for each item (minimum stock, reorder quantity, supplier) and replaces the old
Access/VBA tool. It's for you, and a planner occasionally gets answers
through you. The reason for rebuilding: someone other than you should be able
to understand, fix and change it, it should be documented, and saving must
never lose data.

Not included

- a window or web page
- deleting items
- importing from Access, and CSV export
- several users at the same time
- any calculation from actual stock levels
- editing the data in Excel

Requirements

Source for all of them: you, 2026-11-17. R-008 and R-010 are my proposals.

ID: R-001
Priority: MUST
Requirement: show <item> shows the item's settings.
How to check it's done: It prints the item number, min, reorder qty and
  supplier. For an unknown item it prints a clear "not found" message and
  nothing else.
────────────────────────────────────────
ID: R-002
Priority: MUST
Requirement: save <item> --min … --reorder … --supplier … creates a new item
  or updates an existing one.
How to check it's done: After save, show returns the new values. Saving the
  same item again replaces its values, and there's still only one row for
  it.
────────────────────────────────────────
ID: R-003
Priority: MUST
Requirement: Saving is all-or-nothing.
How to check it's done: A test makes the save fail partway through.
  Afterwards the old values are still there, unchanged.
────────────────────────────────────────
ID: R-004
Priority: MUST
Requirement: Bad input is refused.
How to check it's done: The item number and supplier must not be empty
  (spaces at the ends are removed). Min must be a whole number 0 or more;
  reorder qty a whole number 1 or more. Bad input gets a message naming the
  problem, and the stored data doesn't change.
────────────────────────────────────────
ID: R-005
Priority: MUST
Requirement: Apostrophes and other special characters work.
How to check it's done: Save supplier O'Brien, then show returns exactly
  O'Brien.
────────────────────────────────────────
ID: R-006
Priority: MUST
Requirement: list shows all items.
How to check it's done: It prints a table of all items sorted by item
  number. With no items it says "no items".
────────────────────────────────────────
ID: R-007
Priority: MUST
Requirement: Item numbers ignore upper/lower case.
How to check it's done: Save A-100, then show a-100 finds it. Saving a-100
  updates that item instead of creating a second one.
────────────────────────────────────────
ID: R-008
Priority: MUST
Requirement: It's documented for the next maintainer.
How to check it's done: A README covers how to install, how to run, and
  every command with an example. docs/architecture.md describes how it's
  built. Someone following only the README can run show, save and list.
────────────────────────────────────────
ID: R-009
Priority: MUST
Requirement: It has automatic tests.
How to check it's done: One command (python -m unittest) runs tests for
  R-001 to R-007, and all of them pass.
────────────────────────────────────────
ID: R-010
Priority: MUST
Requirement: It needs nothing beyond Python itself.
How to check it's done: The code uses only what comes with Python, so
  there's no extra installation.

Decision (written down as a decision record)

- 0001: the data lives in one SQLite file, used through a small Python tool. A
  plain CSV file was rejected because safe saving would have to be built by
  hand and Excel can quietly damage the data. Keeping Access was rejected
  because others would still need Access and VBA skills. What would change it:
  needing several people working at the same time, or needing the data inside
  another system.

Short design

- Goals: easy for others to maintain, safe saving, small.
- Limits: only plain Python, one user at a time, data on your PC.
- Options weighed: storage (SQLite chosen, CSV and Access not) and how you use
  it (terminal chosen, a window or browser page not, to keep it small).
- How it's built (proposal): two parts.
  - A storage part holds all the database work and the checks, so saving and
    validation live in one place and are easy to test.
  - A command part reads what you type and prints the results.
- Where the data file lives (proposal): reorder.db in the project folder. It's
  not stored in git, because it holds data rather than code, so backing it up
  is up to you.

Open questions

┌─────────────────────────────────────────────────────────────┬───────────┐
│                          Question                           │   Who     │
│                                                             │  decides  │
├─────────────────────────────────────────────────────────────┼───────────┤
│ Which Python version is on your PC? I'll check this when    │ Claude    │
│ building starts.                                            │           │
├─────────────────────────────────────────────────────────────┼───────────┤
│ Will the future maintainer have Python on their PC?         │ you       │
├─────────────────────────────────────────────────────────────┼───────────┤
│ Who will be the maintainer if you're away? This affects who │ you       │
│  reads the README.                                          │           │
└─────────────────────────────────────────────────────────────┴───────────┘

Which language should the project documents be written in? No documents exist
yet, so I recommend English, the language you write in.
```

## Step 8: Language

**You (owner):**

> English

**What happens:** Documents will be in English. Next comes one explicit question: do you approve the requirements?

**Claude (final reply):**

```text
Thank you, the documents will be in English.

Do you approve these requirements?
```

## Step 9: Approval

**You (owner):**

> Yes, I approve these requirements.

**What happens:** Only now are files written: ctx/requirements.md, the decision record, ctx/TASKS.md, the design, docs/architecture.md and three lines in CLAUDE.md. Nothing is built yet.

**Claude (final reply):**

```text
I've written down the requirements you approved. Nothing has been built.

Files created:
- ctx/requirements.md: the purpose, what's not included, and requirements
  R-001 to R-010, all marked approved.
- docs/decisions/0001-sqlite-file-with-python-tool.md: why we chose SQLite
  with a small Python tool, which alternatives were rejected, and what would
  make us decide again.
- ctx/TASKS.md: what happens next and the open questions, each with who
  decides.
- ctx/plans/2026-11-17-reorder-cli-design.md: the short design (goals, limits,
  the options we weighed, the proposed structure).
- docs/architecture.md: empty for now. It gets filled in alongside the code,
  so it only ever describes what actually exists.
- CLAUDE.md: three lines added, saying where the status and requirements live,
  that we follow the b6 method, and that documents are in English.

Two questions are yours to answer whenever you like (they're listed in
ctx/TASKS.md): will the future maintainer have Python on their PC, and who
will maintain the tool when you're away?

Next step, when you're ready: I write a step-by-step plan for building it. You
read it and only say "go" if you agree.
```

## Step 10: The plan

**You (owner):**

> Yes, write the plan.

**What happens:** Skill `b6:plan`: three steps, each with an agent, a model level and how it will be verified. One choice for the owner (where the data file lives) and a token estimate. Nothing starts without "go".

**Claude (final reply):**

```text
I'll write the plan in English, like the other documents. This chat runs on
the strong model. The worker agents run on the medium model, and every result
is checked by a fresh reviewer on the strong model.

Plan: reorder settings command-line tool

Covers: R-001 to R-010. Size: M.

#: 1
Step: Storage part
Agent: worker
Model level: medium
Task: First check which Python version you have. Then build the part that
  stores the data: the SQLite file, the checks on input, one row per item
  regardless of case, and an all-or-nothing save. Add tests for it and write
  its description into docs/architecture.md.
How I verify: python -m unittest passes. Tests cover: create and update
  (R-002), a save that fails partway leaving the old values intact (R-003),
  bad input refused with nothing changed (R-004), O'Brien (R-005), and a-100
  = A-100 (R-007). The code uses only plain Python (R-010).
────────────────────────────────────────
#: 2
Step: Commands
Agent: worker
Model level: medium
Task: Build the commands show, save and list (run as python -m reorder …),
  with clear messages. Add their tests, keep reorder.db out of git, and
  extend docs/architecture.md.
How I verify: python -m unittest passes. Test runs: show for a known item
  and an unknown one (R-001), save followed by show (R-002), list with items
  and when empty (R-006), and bad input producing a message (R-004).
────────────────────────────────────────
#: 3
Step: README
Agent: worker
Model level: medium
Task: Write README.md for the next maintainer: install, run, every command
  with an example, how to run the tests, and where the data file is.
How I verify: The reviewer copies the project into a scratch folder and
  follows only the README there: save, show and list all work, and the tests
  pass (R-008, R-009).

Choice for you

- Where the data file reorder.db lives:
  - (a) Always in the tool's own folder (recommended). The data is always in
    the same place, no matter where you open the terminal.
  - (b) In whichever folder you run the command from. It's easy to end up with
    several separate data files by accident.

  Either way, the tests use their own throwaway file and never touch your real
  data.

Token estimate

Roughly 250,000–450,000 tokens for three steps with checks. Each fix round, if
one is needed, adds about half a step on top. This is a rough guide.

What gets built: a small Python tool with three commands (show, save, list),
tests, a README and a description of how it's built.

How you'll know it works: every step is checked by a fresh reviewer against
the criteria we agreed. At the end you'll get the evidence (commands and their
results), plus a few commands you can try yourself if you want.

Tell me (a) or (b) for the data file, then say "go" to start. Or say "write
the plan, but don't build yet" if you'd rather wait.
```

## Step 11: Go: building

**You (owner):**

> a, go

**What happens:** Skill `b6:build`. For each step Claude writes a brief, a worker agent (medium model) builds, Claude runs the tests itself, then a fresh reviewer (strong model) checks against the requirements. The reviewer sends step 1 back once (the docs described code that did not exist yet). In step 2 the reviewer finds a real bug ("1_0" read as 10) and a Windows character-set problem. Claude does not decide that for the owner: it asks, with options and a recommendation.

**Claude (final reply):**

```text
The reviewer sent step 2 back for a fix. One finding is a plain bug that will
be fixed. The other needs a decision from you.

The bug (will be fixed): the number fields accept 1_0 and read it as 10, and
also accept unusual digit characters such as ５. From now on only plain digits
will be accepted, and there will be a test for it.

Your decision: special characters when output is saved to a file.

Typing commands and reading the results in your terminal should work fine with
names like Müller or Łódź. You'll be able to try it yourself at the end.

The problem starts when the output is saved to a file, for example python -m
reorder list > items.txt, or passed on to another program. Then Windows
switches to an old character set:
- Müller comes out as M?ller in the file. The stored data is correct.
- Names with letters outside that old set, like Łódź, make the tool crash
  after saving. The data is saved, but the tool shows an error, so you would
  think the save failed. That's misleading, and it's what bothers me most.

Option: A. Always write output in UTF-8 (my recommendation)
What it means: Every character comes out correctly, also in files, and the
  tool never crashes on a name. It's a few lines in one file. A very old
  program reading the file might show odd characters, but no data is lost or
  wrongly reported.
────────────────────────────────────────
Option: B. Replace characters it can't write with "?"
What it means: It never crashes, but Łódź shows up as ?ód? in saved output.
────────────────────────────────────────
Option: C. Change nothing, mention the limit in the README
What it means: It's the least work, but the misleading crash stays.

Which do you choose: A, B or C? Both fixes go to a worker in one round once
you answer.

My earlier question is also still open: do your item numbers ever contain
accented letters such as Ü or Č? Until you tell me otherwise, I'm assuming
they don't.
```

## Step 12: Owner's decision

**You (owner):**

> A. And no, item numbers never contain accented letters.

**What happens:** Fixes go to a worker, each checked by a fresh reviewer. Step 2 needs two fix rounds, step 3 (README) is checked by a reviewer who copies the project and follows only the README. At the end of this turn the owner pressed Esc by accident, so Claude stopped and waited.

**Claude (final reply):**

```text
Step 3 of 3, the README, is written, and a fresh reviewer is checking it.

What's in it: installing, running, the three commands with real example
output, the input rules, a table of error messages, where the data file is and
how to back it up, how to run the tests, and a short section for the next
maintainer.

What I checked myself:
- I read the whole README.
- I tried the supplier quoting on a copy, in both PowerShell and cmd. Names
  like O'Brien & Sons and O'Neil Ltd are saved and shown exactly as typed.

The reviewer's main task: follow only the README on a fresh copy, the way a
newcomer would, and see if everything works as described. The worker didn't do
this part itself. The reviewer also judges two small points:
- The README says the data file is created by the first command you run.
  That's what the code does, and it's correct.
- "Python 3.8 or newer" hasn't been tried on 3.8, so the wording may need to
  be more careful.

If the reviewer says OK, I'll close the run and give you the result, with a
few commands you can try yourself.
```

## Step 13: Continue after the interruption

**You (owner):**

> ok, continue with the README

**What happens:** The owner just says to continue. Claude picks up where it stopped (the state is in the project files). README fixed, review OK, then skill `b6:wrap-up`: what was made, how it was checked, what you can try, what is still open, and a question about commit and clean-up.

**Claude (final reply):**

```text
The new tool is finished: all ten requirements are met, and each was confirmed
by a fresh reviewer.

What was made

- A small Python tool, used from the terminal, with three commands: show, save
  and list. The data lives in one file, reorder.db, in the project folder. It
  needs nothing besides Python, which is already on your PC.
- Saving is all-or-nothing. A failed save can no longer lose an item, which is
  the problem you saw with the old tool.
- Bad input is refused with a message that names the problem: empty fields,
  negative numbers, or text where a number belongs.
- Names like O'Brien or Łódź work, in the terminal and when output is saved to
  a file.
- a-100 and A-100 are the same item.
- Documentation for the next person: README.md (how to install, run and test)
  and docs/architecture.md (how it's built, and what a change must not break).

How it was checked

- python -m unittest runs 33 automatic tests, and all pass.
- A reviewer followed only the README on a fresh copy, like a newcomer would,
  and every output matched what the README says.
- I tried the commands myself in PowerShell and in cmd.
- Four fix rounds were needed along the way, all of them small. Each was
  checked by a fresh reviewer.
- The agents used about 330,000 tokens, within the planned range.

What you can try

Open PowerShell in the folder C:\Users\you\examples\reorder-settings and
type:

1. python -m reorder save A-100 --min 5 --reorder 20 --supplier "O'Brien"
   You should see: Saved A-100: minimum stock 5, reorder qty 20, supplier
   O'Brien
2. python -m reorder show a-100
   You should see four lines with A-100, 5, 20 and O'Brien.
3. python -m reorder save A-100 --min -1 --reorder 20 --supplier "O'Brien"
   You should see: Minimum stock must be a whole number 0 or more, and nothing
   changes.
4. python -m reorder list
   You should see a table of your items.

These commands create the real data file reorder.db. Type in your real items
whenever you like. If something doesn't work later, just tell me and we'll
handle it as a new change.

Still open

These two questions are yours, whenever it suits you. Both are noted in
ctx/TASKS.md:
- Will the future maintainer have Python on their PC?
- Who will maintain the tool when you're away?

Last step: save and tidy up

The plan, the design and the run folder with its reviews were only needed
while building. The requirements, decisions, architecture and README stay.

I suggest first saving the whole project in git as its first commit, so those
working files stay in the history. Then I'd delete them from the folder.
Nothing has been committed yet.

May I commit the project to git and then delete the working files?
```

## Step 14: Commit

**You (owner):**

> Yes, commit. But keep the plan, the design and the run folder. I want to show them to a colleague

**What happens:** The project is committed to git. The owner keeps the plan, the design and the run folder (briefs and reviews) to show them.

**Claude (final reply):**

```text
I've committed the whole project to git as its first commit, 3dfcecb, on the
master branch. Nothing is left uncommitted.

Kept for your colleague, nothing deleted:
- ctx/plans/2026-11-17-reorder-cli.md: the plan you approved
- ctx/plans/2026-11-17-reorder-cli-design.md: the design, with the options we
  weighed
- ctx/plans/2026-11-17-reorder-cli/: the run folder. It holds SUMMARY.md (the
  whole run on one page), the instructions each worker got (briefs/), and all
  seven reviews (review-1.md to review-7.md), including the ones that sent
  work back for a fix.

For your colleague, SUMMARY.md is the best place to start. It lists each step,
how it was checked, and which fix rounds were needed and why.

In ctx/TASKS.md:
- I've noted that you're keeping these files for now. When you no longer need
  them, just say "delete the working files". I'll remove them then, and
  they'll stay in the git history.
- Your two open questions are still there: whether the future maintainer has
  Python, and who maintains the tool while you're away.
```

## Step 15: Try it

**You (owner):**

> Run the four commands for me.

**What happens:** Claude runs the four commands it suggested and reports the results. It also warns that the sample item is now in the real data file, and does not delete anything without being asked.

**Claude (final reply):**

```text
I ran all four commands in PowerShell in the project folder, and each one did
what I said it would:

┌─────┬────────────────────────────┬──────────────────────────────────────┐
│  #  │          Command           │                Result                │
├─────┼────────────────────────────┼──────────────────────────────────────┤
│     │ save A-100 --min 5         │ Saved A-100: minimum stock 5,        │
│ 1   │ --reorder 20 --supplier    │ reorder qty 20, supplier O'Brien     │
│     │ "O'Brien"                  │                                      │
├─────┼────────────────────────────┼──────────────────────────────────────┤
│ 2   │ show a-100 (lowercase)     │ Found A-100 and showed four lines:   │
│     │                            │ 5, 20, O'Brien                       │
├─────┼────────────────────────────┼──────────────────────────────────────┤
│     │                            │ Refused with Minimum stock must be a │
│ 3   │ save A-100 --min -1 …      │  whole number 0 or more. Nothing     │
│     │                            │ changed.                             │
├─────┼────────────────────────────┼──────────────────────────────────────┤
│ 4   │ list                       │ A table with A-100: 5, 20, O'Brien.  │
│     │                            │ Step 3 left the values unchanged.    │
└─────┴────────────────────────────┴──────────────────────────────────────┘

Your real data file now has a sample item. Before these commands there was no
data file. Command 1 created reorder.db in the project folder, so the sample
item A-100 / O'Brien is now in your real data. The tool has no delete command
(we left that out on purpose), so the item can't be removed from inside the
tool. You have two simple options:
- Keep the file: overwrite A-100 later with its real values using save.
- Start clean: delete reorder.db, and the next command creates a new, empty
  one. It holds nothing else yet, so nothing is lost. Deleting it removes your
  data, so I'll only do it if you ask.
```

## Where to look in the project

- `ctx/requirements.md`: purpose, out of scope, requirements with criteria and status
- `ctx/TASKS.md`: where the work stands and what waits for whom
- `docs/decisions/0001-…`: why SQLite, what was rejected, what would change it
- `docs/architecture.md`: how it is built and what a change must not break
- `ctx/plans/2026-11-17-reorder-cli-design.md` and `…-reorder-cli.md`: the design and the plan
- `ctx/plans/2026-11-17-reorder-cli/`: `SUMMARY.md` of the run, the briefs for each worker, all seven reviews
- `CLAUDE.md`: the lines that tell Claude where everything is

@panthea.sk
