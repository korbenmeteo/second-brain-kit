---
type: reference
name: operating-rules
description: Non-negotiable rules and soft conventions for the system.
last_updated: null
---

## Hard rules: explicit approval every time

1. Never send an email or a message. Write a draft in `4_outputs/drafts/`, and in the email client too if its connector can create drafts, then ask.
2. Never delete or archive a file. Ask first, every time.
3. Never write to a system listed as read-only in `tools.md`.
4. Never post to a chat, a social network or any external channel.
5. Never run a destructive shell command (`rm -rf`, `git reset --hard`) without asking.

## Soft rules: follow unless told otherwise

- Before any task, check the wiki for the people, companies and projects involved.
- When a note mentions a person, company or project with a page, add a `[[wikilink]]`.
- At the end of a session that touched more than three files, list what changed.
- If a note has no links in or out after 48 hours, surface it for triage.
- Every task card carries a handoff prompt, complete enough to run without further explanation.

## Output conventions

- Email drafts are complete: subject, to, cc, body. No half drafts.
- Meeting briefs list attendees, agenda, relevant context and open questions.
- Every output links to its task card and to the wiki pages read.
- Outputs stay `status: draft` until you approve them.

### Where outputs live

| `kind` | In progress | Once done |
|---|---|---|
| `email`, `message` | `drafts/` | `sent/` after you have sent it yourself |
| `brief` | `drafts/` | `briefs/` |
| `plan` | `drafts/` | `plans/` |
| `deck`, `summary`, `other` | `drafts/` | a folder of the same name, created when first needed |

Never delete an output. Archiving is moving, not removing.

### Close the loop to the wiki

After producing or finalising an output, check whether it holds durable knowledge: a
decision, a new fact about a person, company or project, a new contact, a change of status.
If so, update or create the wiki page and link the output. A sent email that shows a deal
moved forward should leave the project page more current than before.

## Health conventions

- A source is stale when its last sync is older than twice its cadence.
- A problem that needs you gets a file in `3_operations/health/issue-YYYY-MM-DD-<slug>.md`.
