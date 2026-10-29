---
type: reference
name: tools
description: Sources and connectors feeding the vault, and which ones are read-only.
last_updated: null
---

## Sources

| Source | How it arrives | Lands in | Cadence | Access |
|---|---|---|---|---|
| Meetings | (connector or export) | `1_knowledge/raw/meetings/` | daily | read-only |
| Email | (connector or export) | `1_knowledge/raw/email/` | daily | read, drafts only |
| Calendar | (connector or export) | `1_knowledge/raw/calendar/` | daily | read-only |

## Read-only systems

Systems Claude may read but must never write to (task managers, CRMs, shared wikis):

-

## Sync scripts

| Script | Source | Schedule |
|---|---|---|
