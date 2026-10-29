---
name: create-task-card
description: Create a Second Brain task card in 2_tasks/todo/ when something needs action (a reply, a decision, a deliverable, a follow-up), with context, links to the wiki pages and sources involved, and a handoff prompt complete enough for Claude to execute later. Use when the user says "make a card", "add a task", or when a meeting or email surfaces an action.
---

## When to use

When a meeting, an email or a note surfaces something that needs doing.

## Inputs

- What needs doing. Ask if it is not clear.
- The source file, if there is one.
- Priority (high, medium, low) and a due date, if known.

## Steps

1. Check `2_tasks/` in every lane for a card on the same thing. If one exists, update it instead.
2. Search `1_knowledge/wiki/` for the people, companies and projects involved. Note which pages exist.
3. Write the card from the template below to `2_tasks/todo/YYYY-MM-DD-short-title.md`.
4. The handoff prompt matters most: write it as a direct instruction to Claude, with the task, the audience, the voice, the constraints and what success looks like. Someone reading only the card should be able to do the work.
5. Show the path and the card.

## Template

```markdown
---
type: task
title:
status: todo
priority: medium
created: YYYY-MM-DD
due:
source: []
wiki: []
output: null
---

## What

What needs to be done, in one or two sentences.

## Why

Why it matters and what happens if it slips.

## Context

What the sources and the wiki say that the person doing it needs to know.

## Handoff prompt

A direct instruction to Claude.

## Output

(Empty until produced.)

## Review notes

(Empty until reviewed.)
```

`source`, `wiki` and `output` hold vault paths (`1_knowledge/wiki/people/Sam Rivera.md`) or
wikilinks (`[[Sam Rivera]]`). `vault.py check` reports any that do not exist.

## Safety rules

- Do not create cards from vague signals. "We should catch up sometime" is not a task. Ask when unsure.
- One card per action. Split a card that hides three deliverables.

## Afterwards

If the card came from a raw file, mention the card under a `## Tasks` heading in the matching wiki page, not in the raw file.
