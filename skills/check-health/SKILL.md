---
name: check-health
description: Report on the state of a Second Brain vault. Unprocessed raw files, overdue task cards, cards in the wrong lane, links to pages that do not exist, stale or failing sources and open issues, with a suggested fix for each. Use at the start of a week, after a sync may have failed, or when the vault feels stale.
---

## When to use

At the start of a working week, when a sync may have failed, or when something feels out of date.

## Steps

1. Run the checker that ships with the `init-vault` skill, from this skill's directory:
   ```bash
   python3 ../init-vault/scripts/vault.py check "<vault>"
   ```
   Add `--json` to read the counts programmatically. It exits 1 when it finds an error.
2. Read `3_operations/logs/` for errors since the last check.
3. Report in four parts, most urgent first:
   - **Sources:** healthy, stale or failing, with the last sync date.
   - **Backlog:** raw files not processed yet, inbox items to sort.
   - **Tasks:** overdue cards (oldest first), cards in the wrong lane, cards in review with no output.
   - **Wiki:** links to pages not written yet, grouped by target. A name linked three times probably deserves a page.
4. Suggest one fix per problem: run `refresh-knowledge`, reschedule or close a card, create a page, fix a sync login.

## Safety rules

- Do not fix anything on your own. Report, then ask which fixes to apply.
- Never close or delete an overdue card. Ask whether to reschedule it, finish it or drop it.

## Afterwards

When a problem is fixed, set the issue file's `status: resolved`.
