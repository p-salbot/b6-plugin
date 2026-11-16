# Skills as company knowledge

Summary of a brainstorming session, 2026-11-12. It records an opinion formed from practice, not a measured result.
The evidence is the author's own work with two sets of skills for an AI assistant (`strix-health`, knowledge of
Slovak healthcare, and `ps-metodika`, a working method). Statements below are the author's experience unless a source is given.

## 1  The main idea

A skill is a text file for an AI assistant. It has a short description, which the AI normally sees[^1], and a
body, which the AI opens when the description matches the task. Larger reference material is opened only when needed.
Nothing in the format requires steps or code.

The word "skill" suggests an ability to do something, so people look for tasks to automate and overlook the
knowledge those tasks rest on. A skill does not have to be a procedure. It can be a
**knowledge map**: what is true in a domain, what the terms mean, where the traps are. Such a map keeps the AI between the borders of the domain. Even many capable
people have not realised this.

| Kind of skill | What it contains | Comparable to |
|---|---|---|
| Procedure | steps, commands, templates for one recurring task | a work instruction |
| Knowledge map | facts, terms, rules, traps, open questions of a domain | an experienced colleague sitting next to you |
| Glossary | the company's terms, abbreviations and codes with their meaning | a company dictionary |
| Personal profile | role, real skills and knowledge, working style of one person | an introduction to a new co-worker |

A procedure improves one task. A knowledge map can improve many tasks in its domain, and a short, focused map
works better than a complete one. The AI can often work out a procedure for itself; it usually cannot work
out the company's own facts.

## 2  What skills can be used for

- **Domain knowledge** that a general AI lacks because it is local, niche or changes every year
  (for example Slovak healthcare reimbursement and its data formats).
- **Glossary:** the terms, abbreviations and codes a company or a team uses, each with one agreed meaning.
  The AI then reads and writes the company's language instead of guessing it.
- **Keeping the AI inside the lines:** what a term means, what counts as an error, what is normal in the data.
- **Recurring procedures** and the parts of a process that can be automated.
- **Personal profile:** who the AI works for, in what position and with what real skills.
- **Any role, not only IT:** CEO, logistics, HR, marketing, sales. Key people
  have been taught to write skills that are simpler than an AI specialist would write, yet sufficient to
  automate part of a process.

## 3  What the company can achieve

- **Less explaining.** The context no longer has to be typed into every request, or only a small part of it.
- **Shared knowledge.** One source with a history of changes serves every project and every colleague who
  adds it to their assistant.
- **Cover during absence.** Others can do the work while a person is on holiday or off work, for the part of
  the knowledge that is written in the skill.
- **Faster onboarding.** A newcomer's AI assistant knows the written part of the domain from the first day.
- **Common language.** People and their AI assistants use a term in the same meaning across teams, because
  the meaning comes from one glossary.
- **Collective memory.** The skills together are organised text, meaning knowledge arranged by topic that a
  machine can read, describing the company's processes and knowledge.
- **Reuse later.** The text is plain and readable, so other AI models, skills, projects and tools can use it.
  How a tool picks a skill up differs between tools; the knowledge itself moves with the text.

## 4  What improves over time

- **Every next skill, project and procedure is easier to create,** because the AI already knows the person,
  their position, their real skills and the domain.
- **The value grows with use.** The more a person works with the AI, the more they value the skills: the context
  that used to be typed into each request is already there. The benefit is mostly work that no longer has to be
  done.
- **Errors can surface sooner than in a wiki.** In the author's experience a wrong wiki page can sit unnoticed
  for years. A skill is used daily, so a wrong fact shows up in results. This helps only when the feedback process in §6.1 exists; without
  it the error spreads (§5).

## 5  Caveats

| Caveat | Why it matters |
|---|---|
| Most people will not write skills on their own initiative | They lack the time and the habit of structuring knowledge. Some also do not trust what will happen with the knowledge they share (see the row on being replaced). |
| Staleness | An outdated skill can be worse than none, because the AI trusts it. |
| A silent error spreads to everyone | Context typed by hand is seen by the person each time. The content of a skill is not re-read, and one wrong rule in a shared skill is repeated by every colleague's AI. |
| A skill is a summary, not the source | A summarised number or code can be wrong. |
| A skill does not replace the expert's judgment | A substitute or a newcomer gets only what was written down and must still be able to check the result. Relying on the AI alone can weaken people's own expertise, most clearly while they are still learning. |
| A knowledge map is harder for the AI to pick up | A procedure has an obvious moment. A knowledge map must be opened whenever the topic appears, even when nobody names it, and the AI decides that from the description alone. |
| A knowledge map is harder to check | A wrong fact looks as convincing as a right one. |
| Many skills | Descriptions share limited space, and those of the least used skills are dropped first[^1], so a rarely opened knowledge map can lose its description. As the number grows, the choice becomes less reliable: most often no skill is opened, less often the wrong one. Skills that resemble each other do more harm than the number itself. |
| Overlap between skills | Two skills that say slightly different things about one topic can confuse the AI more than no skill. |
| Skills guide; they do not enforce | Text works for judgment. A line that must never be crossed (customer data, live systems, sending data outside) needs access rights and technical blocks. |
| Sensitive content | Knowledge of HR, sales and management includes personal data, salaries, client terms and strategy. A personal profile is personal data. |
| Company rules | The company's AI policy and data protection rules decide which AI service may be used and what may be put into it. |
| Skills from outside | A skill taken from the internet can carry harmful instructions or programs. |
| The owner leaves | A skill without an owner is no longer reviewed and goes stale. |
| "Others can do my work" also reads as "I can be replaced" | People then keep the valuable parts to themselves. |
| The value is hard to show | A knowledge map does nothing visible by itself. |

## 6  Processes that maintain quality

### 6.1  The two that matter most

1. **Periodic review.** The owner reviews the skill at a fixed interval and whenever the domain changes. Review
   catches what changed in the world.
2. **Feedback at almost no cost.** Whoever notices a wrong answer says so in the same conversation, and the
   correction is proposed to the owner. Feedback catches what was wrong from the start. If reporting needs a
   form or a ticket, people fix the answer for themselves and the skill stays wrong.

### 6.2  Supporting practices

1. **Owner and validity.** Every skill names its owner and author, and states which version of the source it is
   valid for and when it was last verified.
2. **Handover and retirement.** When the owner leaves or changes role, the skill gets a new owner or is retired.
   At review, skills that overlap are merged and unused ones removed, so that descriptions stay distinct.
3. **Anyone proposes, the owner approves.** Users do not change a shared skill directly.
4. **Second reader for shared skills.** A skill used by more people is read by one more person before release.
   A skill from outside is read in full before anyone adds it.
5. **Test questions.** Each knowledge map has a short list of questions with known answers, asked again after
   every change.
6. **Sources and citations.** A number, code or rule that will be used in a calculation, in a program or in a decision
   carries a reference to its source and is verified there before use.
7. **One fact in one place.** Other skills refer to it instead of repeating it. A term is defined once, in the
   glossary.
8. **Three parts in every knowledge map:** what is true; what people commonly get wrong; what is unknown or
   undecided. The third part is meant to reduce confident guessing by the AI.
9. **Description tuned to real questions.** When the AI answers a domain question without opening the skill,
   the description is corrected.
10. **Access by role.** Company-wide, team and personal skills are kept apart. No customer data and no records
    of real persons go into a skill; examples are made up. The exception is the personal profile: the person
    writes it voluntarily and for their own use, it stays that person's own skill, and it holds no data about
    other people. An employee's agreement alone is not a sufficient basis; the company rules (§5) apply.
11. **Large reference data stay outside the text.** A long code list is looked up by a small program, not read.
12. **The AI drafts, the person approves.** After a finished task the AI proposes a skill or a change to one;
    the person who owns the knowledge adds what the AI did not know, corrects the draft and approves it. The
    value is in those additions: a draft approved as it stands is worth little. This lowers the barrier for
    people who would not write a skill themselves.
13. **Credit and evidence.** Authorship is visible and acknowledged by management. Time saved is recorded, and
    the same question answered with and without the skill is shown to others.

## 7  How each caveat is mitigated

Every caveat from §5 with its mitigation and the process in §6 that carries it.

| Caveat | Mitigation | Process |
|---|---|---|
| Most people will not write skills on their own initiative | Key people are taught to write skills. After a finished task the AI drafts the skill; the person adds what the AI did not know, corrects and approves it. | §6.2 item 12 |
| Staleness | Every skill states the version of its source and the date it was last verified. The owner reviews it at a fixed interval and whenever the domain changes. | §6.1 item 1, §6.2 item 1 |
| A silent error spreads to everyone | Anyone who notices a wrong answer reports it in the same conversation. A shared skill is read by a second person before release and checked with test questions after every change. | §6.1 item 2, §6.2 items 4 and 5 |
| A skill is a summary, not the source | A number, code or rule that will be used in a calculation, in a program or in a decision carries a reference to its source and is verified there before use. Example below the table. | §6.2 item 6 |
| A skill does not replace the expert's judgment | The result is checked by a person who can judge it. Work covered during an absence is limited to what the skill describes, and decisions outside it wait for the expert. | not yet a process in §6; to be agreed per team |
| A knowledge map is harder for the AI to pick up | The description contains the words people really use: everyday terms, abbreviations, codes and typical situations. When the AI answers a domain question without opening the skill, the missing words from that question are added to the description. Example below the table. | §6.2 item 9 |
| A knowledge map is harder to check | A knowledge map has three safeguards: test questions with known answers, references to the source for important claims, and a part that says what is unknown or undecided. Example below the table. | §6.2 items 5, 6 and 8 |
| Many skills | At review, overlapping skills are merged and unused ones removed, so that descriptions stay distinct. | §6.2 item 2 |
| Overlap between skills | Each fact is written in one place; other skills refer to it. | §6.2 item 7 |
| Skills guide; they do not enforce | A line that must never be crossed is protected by access rights and technical blocks, not by the text of a skill. | outside the skills; set up by IT |
| Sensitive content | Company-wide, team and personal skills are kept apart. No customer data and no records of real persons; examples are made up. A personal profile is written voluntarily by its person and stays with them. | §6.2 item 10 |
| Company rules | Before a skill is shared, the owner checks it against the company's AI policy and data protection rules; approval is obtained where the rules require it. | not yet a process in §6; follows company policy |
| Skills from outside | A skill from outside is read in full before anyone adds it. | §6.2 item 4 |
| The owner leaves | The skill gets a new owner at handover, or is retired. | §6.2 item 2 |
| "Others can do my work" also reads as "I can be replaced" | Authorship is visible in every skill and acknowledged by management. | §6.2 item 13 |
| The value is hard to show | Time saved is recorded. The same question answered with and without the skill is shown to others. | §6.2 item 13 |

### Examples for three of the rows

**A skill is a summary, not the source.** A skill copies facts from the source in a shortened form; a mistake
can happen in copying, or the source can change later. *Example:* the skill gives the base rate for a year.
Before reimbursements are recalculated with it, the rate is checked in the valid price list the skill refers
to. An ordinary explanation of a term does not need checking.

**A knowledge map is harder for the AI to pick up.** The AI opens a skill only when it finds words from the
question in the description, and people rarely ask with the official name of the topic. *Example:* a colleague
asks "why is the payment for this case lower when the patient stayed longer?" and never says DRG. If the
description holds only "SK-DRG, grouping", the skill is not opened. After "payment for a hospital stay, length
of stay, case" is added, it is.

**A knowledge map is harder to check.** In a procedure an error shows at once: a step fails. A wrong fact
does not fail; the AI repeats it. *Example:* the test question "How many items does a row of batch 751d have?"
has the known answer 29. If the AI answers differently after the skill was changed, the change broke
something. The part on unknowns can say: "Whether the rule also applies to corrective batches is not
confirmed." The AI then does not fill the gap with a guess.

## Note

The source was read on 2026-11-12.

[^1]: **When the AI does not see a description** (Claude Code; other tools differ). The list of skills given to
    the AI has a size limit of 1% of the model's context window. The limit can be changed with the setting
    `skillListingBudgetFraction` or the environment variable `SLASH_COMMAND_TOOL_CHAR_BUDGET`. The list always
    contains the name of every skill. When the descriptions do not fit, Claude Code drops some of them, starting
    with the skills that are invoked least, and writes a warning only to the debug log. A skill that has lost
    its description can be chosen by its name alone. In addition, the description together with the optional
    field `when_to_use` is cut at 1,536 characters in the list, and a skill marked
    `disable-model-invocation: true` has no description in the list at all; it opens only when a person calls
    it. The consequence for this document: with many skills installed, a knowledge map that is opened rarely is
    the first to become invisible, and nothing tells the user. Source: Claude Code documentation, "Extend
    Claude with skills", <https://code.claude.com/docs/en/skills>.

@panthea.sk
