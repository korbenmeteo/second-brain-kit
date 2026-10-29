# second-brain-kit

A markdown second brain run by Claude. Meetings, email and notes come in as raw files;
Claude turns them into wiki pages and task cards, and task cards into drafts you approve.
Folder structure, `CLAUDE.md`, nine skills and a health checker, as a Claude Code plugin.

I have run my own vault this way since 18 May 2026. Twenty-three weeks in, it holds 145 wiki
pages (65 companies, 31 people, 21 projects, 19 topics, 8 decisions) joined by 665 links. They
were built from 470 synced sources: 132 meeting transcripts, 282 email threads and 56 days of
calendar. Along the way Claude opened 54 task cards and wrote 162 briefs, email drafts and plans.

The wiki is what compounds. A meeting from June still answers questions in October, because its
people, decisions and open threads live on pages that every later meeting extends. Folders alone
drift, though: cards move lanes, drafts move to sent, sources stop syncing, and nothing complains.
That is why the kit ships a checker, not just folders.

## What it does

**A structure Claude can find its way around.** `init-vault` creates it in any folder (an
Obsidian vault works) and never overwrites a file:

```
0_inbox/                      unsorted drops
1_knowledge/raw/<source>/     one file per meeting, email or event, never rewritten
1_knowledge/wiki/             people, companies, projects, topics, decisions
1_knowledge/reference/        identity, writing style, preferences, tools, rules, schemas
2_tasks/todo|handoff|review|done/
3_operations/                 sync scripts, health files, logs
4_outputs/drafts|sent|briefs|plans/
5_archive/
CLAUDE.md                     folder map, retrieval order, guardrails
```

The `CLAUDE.md` sets a retrieval order (task card, linked pages, wiki, raw sources, and only then a
live connector) and five guardrails: no sending, no deleting, no writing to read-only systems, no
posting, no destructive commands, without asking each time.

**Nine skills for the loop.**

| Skill | Does |
|---|---|
| `init-vault` | Creates the structure, then helps you fill in your identity and writing style |
| `sync-source` | Connects a source so it lands in `raw/` with idempotent frontmatter and a health file |
| `refresh-knowledge` | Turns unprocessed raw files into wiki updates and proposed task cards |
| `create-task-card` | Writes a card with context, linked pages and a handoff prompt |
| `handoff-task` | Executes a card: reads what it links to, writes a draft, moves the card to review |
| `write-draft` | Writes an email, brief or plan in your voice, without a card |
| `review-output` | Revises on feedback, closes the card, records what to remember |
| `researcher` | Answers from the vault first, with sources and dates |
| `check-health` | Backlog, overdue cards, broken links, stale sources, with a fix for each |

**A checker.** `vault.py check` reads every frontmatter and reports, without changing anything:

```
vault ~/Notes on 2026-10-27
  raw      3 files, 1 not processed yet
  wiki     5 pages; links to pages not written yet: 1
  tasks    todo 2, handoff 0, review 1, done 1; 1 overdue
  outputs  2
  sources  2, 1 stale
  inbox    to sort: 1
WARNING  1_knowledge/wiki/projects/Winter blend launch.md: [[Lisbon coffee fair]] has no page yet
WARNING  2_tasks/todo/2026-10-21-reply-to-green-bean-quote.md: overdue since 2026-10-24
WARNING  3_operations/health/source-email.md: stale: last sync 2026-10-23, expected every 24 h
```

It exits 1 on errors (a card whose status disagrees with its lane, a link to a file that does not
exist, a date that is not a date), so it can run in a hook or a scheduled job.

**Optional modules**, in their own repositories:

- [connector-sync](https://github.com/korbenmeteo/connector-sync): daily syncs of claude.ai connectors (Granola, Gmail, Google Calendar) into `raw/`, with catch-up after failures.
- [x-bookmarks-triage](https://github.com/korbenmeteo/x-bookmarks-triage): your X bookmarks, triaged critically and routed into the wiki.

## Requirements

- Claude Code (or Claude Cowork).
- Python 3.10+, standard library only, for the checker.
- A folder for your notes. Obsidian is a good reader for it but not required.
- Connectors or exports for the sources you want. None is needed to start: `0_inbox/` takes notes by hand.

## Install

As a Claude Code plugin:

```
/plugin marketplace add korbenmeteo/second-brain-kit
/plugin install second-brain-kit@second-brain-kit
```

Or copy the folders under `skills/` into `~/.claude/skills/`.

## Quick start

1. Ask Claude: *"Set up a second brain in ~/Notes."* Or by hand: `python3 skills/init-vault/scripts/vault.py init ~/Notes`.
2. Open Claude Code in that folder. Fill in `identity.md` and `writing-style.md` with Claude's help: three emails you are proud of are enough for the style.
3. Feed it. Drop a meeting note in `0_inbox/`, or connect a source with `sync-source`.
4. Run the loop: *"Refresh the wiki"*, then *"Do the card about ..."*, then review the draft.
5. Once a week: *"Check the health of my vault."*

To see the checker on a fictional vault (a small coffee roastery):

```bash
bash examples/run-example.sh
```

## Privacy

Everything stays in your folder, on your machine. The kit sends nothing anywhere; the skills
only read and write files in the vault, and Claude asks before any live connector call. Never
create your vault inside a clone of this repository, and never commit it: `.gitignore` covers
`vault/` and `my-vault/` in case you do.

## Limits

- The skills are instructions. Claude follows them well, not perfectly: read the drafts, and run the checker.
- The checker reads a subset of YAML (`key: value`, inline lists, `- item` lists). Anything fancier in a frontmatter is ignored, not misread.
- Links between files are paths. Moving a card without updating its draft breaks the link; the checker finds it, it does not fix it.
- A large backlog of raw files takes many sessions to process. `refresh-knowledge` offers to split it by source or month.

## Author

Built by Ruben Hallali ([@RubenHallali](https://x.com/RubenHallali)). I am building my own
tooling in public; issues and pull requests are welcome.

## Licence

MIT
