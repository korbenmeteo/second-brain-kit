---
name: sync-source
description: Connect a new source (meeting notes, email, calendar, a task manager, an export) to the Second Brain. Decides what to pull, where it lands in 1_knowledge/raw/, the frontmatter that makes reruns idempotent, the health file that shows when it breaks, and how to schedule it. Use when the user wants to add, import or sync a source into their vault.
---

## When to use

When the user wants a new source to feed the vault, as a one-off import or a recurring sync.

## Steps

1. Ask:
   - What is the source, and how can it be reached: a Claude connector, an API, a file export?
   - What should come in: all meetings, starred threads only, one calendar, one project?
   - How often: once, daily, weekly?
2. Pick the route:
   - **A Claude connector** (Granola, Gmail, Google Calendar and others on claude.ai): use the optional `connector-sync` module, which runs Claude Code headless on a schedule with one prompt per source.
   - **An API or an export**: write `3_operations/sync/sync-<source>.py` in standard-library Python.
   - **A one-off import**: run it by hand, no schedule.
3. Whatever the route, the output contract is the same:
   - One markdown file per item in `1_knowledge/raw/<source>/YYYY-MM-DD-<title>.md`.
   - Frontmatter from `1_knowledge/reference/schemas.md`: `type: raw_source`, `source`, `source_id`, `date`, `status: unprocessed`.
   - Before writing, look for an existing file with the same `source_id`, so a rerun adds nothing.
   - After each run, write `3_operations/health/source-<source>.md` (`type: source_health`, `status`, `last_sync`, `cadence_hours`, `error`) and append one JSON line to `3_operations/logs/<source>.jsonl`.
   - Fail loudly. A run that writes nothing and reports success is the failure that costs the most.
4. Add the source to `1_knowledge/reference/tools.md`, marking it read-only if Claude must never write back.
5. Test with a single small fetch. Show the files. Run it again and confirm nothing new appears.
6. Only then schedule it (launchd, cron or a scheduled task), and explain how to check it: `check-health`.

## Safety rules

- Never put a key or a token in a script or in the vault. Use environment variables or the system keychain, and list the file that holds them in `.gitignore`.
- Never enable a schedule before a manual run has worked twice.
- Pull only what the user asked for. A sync that grabs everything is hard to trust and slow to process.
