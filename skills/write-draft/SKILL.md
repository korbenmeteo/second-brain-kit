---
name: write-draft
description: Write a prose output (email, message, meeting brief, plan, summary) in the user's own voice, using the Second Brain's writing style, preferences and the wiki pages of the people and projects involved, and save it as a draft in 4_outputs/drafts/. Never sends. Use for "draft a reply", "write a brief for my meeting with", "prepare a plan".
---

## When to use

When the user needs a written artefact and there is no task card for it. With a card, use `handoff-task`.

## Inputs

- The kind of output, who it is for, what it must say.
- Any wiki pages or source files the user points to.

## Steps

1. Read `1_knowledge/reference/writing-style.md` and `preferences.md`.
2. Read the wiki pages of the people, companies and projects involved, and the latest raw files about them.
3. For a reply, read the whole thread, not only the last message.
4. Draft. Lead with the point. Match the length to the stakes.
5. Check against `writing-style.md`: words to avoid, greeting and sign-off, sentence length. Fix what fails.
6. Save to `4_outputs/drafts/YYYY-MM-DD-short-title.md`:
   ```yaml
   ---
   type: output
   kind: email | message | brief | plan | summary | other
   created: YYYY-MM-DD
   task: null
   wiki_read: []
   status: draft
   ---
   ```
   An email draft carries subject, to and cc above the body.
7. If an email connector that can create drafts is available and the user wants it, create the draft there too. Do not send.
8. Show the draft and ask for feedback.

## Safety rules

- Never send or post.
- If `writing-style.md` is empty, say so in the draft's first line so the user knows why it sounds generic.
