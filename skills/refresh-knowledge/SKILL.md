---
name: refresh-knowledge
description: Process unprocessed raw files (meetings, email, calendar, notes) into the Second Brain wiki. Extracts people, companies, projects, topics and decisions, updates or creates their pages with sources, proposes task cards for clear actions, and marks each raw file processed. Use after a sync or an import, or when the user asks to update the wiki.
---

## When to use

After new files land in `1_knowledge/raw/` or `0_inbox/`, by hand or after a sync job.

## Inputs

- Files in `1_knowledge/raw/` with `status: unprocessed`, and anything in `0_inbox/`.
- The existing pages in `1_knowledge/wiki/`. Schemas are in `1_knowledge/reference/schemas.md`.

## Steps

1. List the raw files with `status: unprocessed`. More than about 30: say how many, and offer to process them by source or by month, in parallel sub-agents if available, before starting.
2. For each file:
   1. Read it.
   2. Extract the people, companies, projects, topics and decisions it mentions.
   3. For each one, look for its page in `1_knowledge/wiki/`. Match on name and aliases; a person may appear by first name only.
   4. If the page exists, add the new context to the right section with the date and a link to the raw file, update `last_updated`, and add the file to `sources`.
   5. If it does not, create a page only when the entity is clearly important or appears in more than one source. Otherwise leave it in the raw file.
   6. List clear actions (a reply owed, a deliverable, a follow-up with a date). Do not create cards yet.
   7. Set `status: processed` and `processed: <today>` in the raw file's frontmatter. Change nothing else in it.
3. Sort what is in `0_inbox/` the same way, then propose where each item should move. Move only with approval.
4. Show the list of actions and create the cards the user confirms, with `create-task-card`.
5. Report: files processed, pages updated, pages created, cards created.

## Safety rules

- Never rewrite the body of a raw file. Only `status` and `processed` change.
- Never delete a wiki page or a section of one. Extend, or mark something as superseded with a date.
- If an entity is ambiguous (two people with the same first name, a company and a project with one name), ask before creating a page.
- Record facts with their date and source. When a new source contradicts a page, keep both and flag it.

## Afterwards

Append one line to `3_operations/logs/refresh-knowledge.log`: date, files processed, pages touched.
