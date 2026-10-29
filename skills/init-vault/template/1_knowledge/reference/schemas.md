---
type: reference
name: schemas
description: Frontmatter and sections for every kind of file in the vault.
---

# Schemas

`scripts/vault.py check` reads only the frontmatter fields marked *checked*. The sections are
conventions for Claude and for you.

## Raw file

One file per item from a source, in `1_knowledge/raw/<source>/YYYY-MM-DD-<title>.md`.
Written once by a sync or an import, never rewritten. Only `status` and `processed` change.

```yaml
---
type: raw_source          # checked
source: meetings          # the subfolder name
source_id: ""             # the source's own id, so a rerun can skip what it already has
title: ""
date: YYYY-MM-DD
participants: []
status: unprocessed       # checked: unprocessed | processed
processed: null           # YYYY-MM-DD, set by refresh-knowledge
---
```

## Wiki page

One page per durable thing, in `1_knowledge/wiki/<people|companies|projects|topics|decisions>/`.
The file name is the page title, so `[[Sam Rivera]]` finds `people/Sam Rivera.md`.

`type` is checked and must be one of `person`, `company`, `project`, `topic`, `decision`, `concept`.

### Person

```yaml
---
type: person
name: ""
role: ""
company: ""               # [[Company]]
last_updated: YYYY-MM-DD
sources: []               # raw files this page draws on
---

## Identity
## Relationship
## Current context
## Recent interactions
## Open threads
## Notes
```

### Company

```yaml
---
type: company
name: ""
last_updated: YYYY-MM-DD
sources: []
---

## What they do
## Relationship
## Key contacts
## Current context
## Notes
```

### Project

```yaml
---
type: project
name: ""
status: active            # active | paused | done
last_updated: YYYY-MM-DD
sources: []
---

## Summary
## Current state
## Decisions
## People
## Open questions
## Next actions
```

### Topic

```yaml
---
type: topic
name: ""
last_updated: YYYY-MM-DD
sources: []
---

## Summary
## What I know
## Open questions
## Related
```

### Decision

```yaml
---
type: decision
name: ""
date: YYYY-MM-DD
status: decided           # proposed | decided | reversed
project: ""               # [[Project]]
sources: []
---

## Decision
## Why
## Options considered
## Consequences
```

## Task card

In `2_tasks/<lane>/YYYY-MM-DD-short-title.md`. The lane folder and `status` always agree.

`source`, `wiki`, `output` (and `task` in an output) are checked when they hold a `[[wikilink]]`
or a `.md` path: the target must exist. URLs and free text are left alone.

```yaml
---
type: task                # checked
title: ""
status: todo              # checked: todo | handoff | review | done, same as the folder
priority: medium          # high | medium | low
created: YYYY-MM-DD
due: null                 # checked: YYYY-MM-DD; overdue cards are reported
source: []                # raw files or notes that raised it
wiki: []                  # wiki pages to read first
output: null              # path of the output once produced
---

## What
## Why
## Context
## Handoff prompt
A direct instruction to Claude: the task, the voice, the constraints, what success looks
like. Complete enough to run without further explanation.
## Output
## Review notes
```

## Output

In `4_outputs/drafts/` while in progress. Then `sent/` once you have sent it yourself,
or the folder of its kind (`briefs/`, `plans/`) once final. Never deleted.

```yaml
---
type: output              # checked
kind: email               # checked: email | message | brief | plan | deck | summary | other
created: YYYY-MM-DD
task: null                # path of the task card
wiki_read: []             # pages read to produce it
status: draft             # draft | approved | sent | final
---
```

## Health file

In `3_operations/health/source-<name>.md`, written by the sync job after every run.

```yaml
---
type: source_health       # checked
source: meetings
status: healthy           # checked: healthy | error
last_sync: YYYY-MM-DD     # checked: stale once older than twice the cadence
cadence_hours: 24         # checked
error: ""
---
```

An open problem gets its own file, `issue-YYYY-MM-DD-<slug>.md`, with `type: issue` and
`status: open | resolved`. Open issues are reported.
