---
name: handoff-task
description: Execute a Second Brain task card. Reads the card, every linked wiki page and source, and the user's writing style, produces the output as a draft in 4_outputs/drafts/, links it both ways and moves the card to review. Use when the user says "do this card", "hand off", "work on <task>", instead of starting from a blank prompt.
---

## When to use

When a card in `2_tasks/todo/` or `2_tasks/handoff/` is ready to be done.

## Inputs

- The card's path, or its title. If several cards match, list them and ask.

## Steps

1. Read the card. Move it to `2_tasks/handoff/` and set `status: handoff` while you work.
2. Read every page in `wiki:` and every file in `source:`.
3. Read `1_knowledge/reference/writing-style.md` and `preferences.md`.
4. If context is still missing, look in the wiki and `raw/` (see the retrieval order in `CLAUDE.md`). If it is not there, say what is missing before producing anything.
5. Follow the handoff prompt. Produce the output.
6. Write it to `4_outputs/drafts/YYYY-MM-DD-short-title.md`:
   ```yaml
   ---
   type: output
   kind: email | message | brief | plan | deck | summary | other
   created: YYYY-MM-DD
   task: 2_tasks/review/<card file name>
   wiki_read: []
   status: draft
   ---
   ```
7. Update the card: `status: review`, `output:` set to the draft's path, a one-line summary under `## Output`. Move it to `2_tasks/review/`.
8. Show the output and say what to check.

## Safety rules

- Never send, post or share the output. Write it to `drafts/` and stop.
- Match the voice in `writing-style.md`. If that file is still empty, say so at the top of the draft.
- Do not pad a thin output. A short draft that names the missing context beats a long generic one.
