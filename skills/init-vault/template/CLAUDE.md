# Second Brain: system brief

This vault is a personal second brain. It takes in context from meetings, email, calendar and
loose notes, turns it into durable wiki pages and task cards, and helps produce outputs: email
drafts, meeting briefs, plans and summaries.

You are working inside this system as a collaborator, not an executor. Read before you act. Ask
when context is missing. Never send, post, delete or write to an external system without explicit
approval.

---

## Folder map

| Folder | Purpose |
|---|---|
| `0_inbox/` | Unsorted drops: quick notes, voice memos, clippings |
| `1_knowledge/raw/` | Raw files from syncs and imports, one subfolder per source. Never edited, except their `status` |
| `1_knowledge/wiki/` | Durable knowledge: people, companies, projects, topics, decisions |
| `1_knowledge/reference/` | Operating context: identity, preferences, writing style, tools, rules, schemas |
| `2_tasks/` | Task cards in lanes: `todo/` → `handoff/` → `review/` → `done/` |
| `3_operations/` | Sync scripts, health files, logs |
| `4_outputs/` | Produced artefacts: `drafts/` while in progress, then `sent/`, `briefs/`, `plans/` |
| `5_archive/` | Retired files. Archiving means moving here, never deleting |

---

## Retrieval order

Before answering a question or starting a task, look in this order:

1. The task card, if there is one.
2. Every wiki page linked from the card.
3. A search of `1_knowledge/wiki/` for related pages.
4. Recent material in `1_knowledge/raw/` and `0_inbox/`.
5. A live connector call, only if local context is missing or stale.
6. If it is still missing, ask.

Do not start from a blank prompt when the vault already holds the context.

---

## Writing and output rules

- Write in the voice described in `1_knowledge/reference/writing-style.md` and `preferences.md`.
- Every output goes to `4_outputs/drafts/` first. If an email connector can create drafts, you may also create one there. Sending is a separate action that needs approval.
- Every output carries `type: output`, a `kind` and links to the task card and wiki pages it used. See `1_knowledge/reference/schemas.md`.
- **Close the loop.** When an output carries durable knowledge (a decision, a new fact, a new contact, a change of status), update the wiki page it concerns and link the output. This is what makes the vault compound.

---

## Hard guardrails

Each of these needs explicit approval, every time. Not implied consent, not once and for all.

1. **Never send an email or a message.** Drafts only.
2. **Never delete or archive a file.** No `rm`, no trash, no move to `5_archive/` without asking.
3. **Never write to the sources listed as read-only** in `1_knowledge/reference/tools.md`.
4. **Never post to a chat, a social network or any other channel.** Drafts only.
5. **Never run a destructive shell command** (`rm -rf`, `git reset --hard`) without asking.

---

## Soft rules

- Link people, companies and projects with `[[wikilinks]]` when their page exists.
- If a note has no links in or out, flag it as loose at the end of the session.
- Keep task cards in the lane that matches their `status`.
- At the end of a session that touched more than three files, list what changed.
- Run `check-health` at the start of a working week.

---

## Skills

| Skill | When to use |
|---|---|
| `init-vault` | Create this structure in a new folder, or check it |
| `refresh-knowledge` | After new raw files arrive: update the wiki |
| `create-task-card` | When something needs action |
| `handoff-task` | Execute a task card and produce its output |
| `review-output` | Give feedback on an output, revise, close the card |
| `write-draft` | Produce any prose output in your voice |
| `researcher` | Answer a question from the wiki and sources first |
| `check-health` | Backlog, overdue cards, stale sources, broken links |
| `sync-source` | Add a new source and decide how it lands in `raw/` |
