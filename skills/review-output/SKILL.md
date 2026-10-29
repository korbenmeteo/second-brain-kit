---
name: review-output
description: Take the user's feedback on a Second Brain output, revise the draft, and when approved close the task card and capture anything worth remembering (a tone preference, a relationship nuance, a fact) in the wiki or the reference files. Use when the user comments on a draft, says "approved", "change this", or "I sent it".
---

## When to use

After the user has read an output in `4_outputs/` and has feedback, an approval, or has sent it.

## Inputs

- The output's path, or the task title.
- The feedback.

## Steps

1. Read the output and its task card.
2. If the feedback asks for changes, revise the output in place and show what changed.
3. If the user approves it:
   1. Set `status: approved` in the output.
   2. Move the card to `2_tasks/done/` and set `status: done`. Update the card's `output:` path if the file moves later.
4. If the user says they sent it themselves: move the output to `4_outputs/sent/`, set `status: sent`, and fix the path in the card.
   Whenever a card or an output moves, update the path on the other side in the same step (`task:` in the output, `output:` in the card). Links between the two break silently otherwise.
5. Ask once: "Anything from this worth remembering next time?" If yes, update the wiki page, `preferences.md` or `writing-style.md`.
6. Close the loop: if the output holds a decision, a new fact or a change of status, update the matching wiki page and link the output.
7. Report what changed.

## Safety rules

- Never send the approved output. Sending is the user's action.
- Never delete a draft. Approved drafts move; they do not disappear.
- Record the user's correction as they said it, not as a softened paraphrase.
