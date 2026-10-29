---
name: researcher
description: Answer a question about a person, company, project, decision or topic from the Second Brain first (wiki, raw sources, inbox), citing the files read and how fresh they are, and only then suggest a live lookup. Use for "what do we know about", "when did I last talk to", "what did we decide on", "remind me".
---

## When to use

For any question the vault might answer, before reaching for web search or a live connector.

## Steps

1. Pick out the entities and the time frame in the question.
2. Search `1_knowledge/wiki/` for their pages. Read them and the pages they link to.
3. Search `1_knowledge/raw/` for recent material, newest first, by name and by keyword.
4. Check `0_inbox/` and `2_tasks/` for anything open on the subject.
5. Answer. Cite each file you used and give its `last_updated` or `date`.
6. Say plainly what is stale or missing. If a live lookup would help, say which and ask before making it.

## Output

The answer first, then the sources:

```
Answer in a few sentences.

Read: wiki/people/Sam Rivera.md (updated 2026-10-20), raw/meetings/2026-10-20-roaster-sync.md
Gap: nothing since 20 October; the quote email of 22 October is not processed yet.
```

## Safety rules

- Never present wiki content as current fact without its date.
- Never fill a gap with a guess. "The vault does not say" is a valid answer.

## Afterwards

If the answer pulled together something worth keeping, offer to add it to the wiki page.
