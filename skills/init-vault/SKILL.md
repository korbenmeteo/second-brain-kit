---
name: init-vault
description: Create the Second Brain folder structure (inbox, raw, wiki, reference, task lanes, operations, outputs, archive) and its CLAUDE.md in a new or existing folder, without overwriting anything, then walk the user through filling in their identity and writing style. Use when the user wants to set up a second brain, a knowledge vault or an Obsidian vault for Claude.
---

## When to use

Once, to start a vault. Again at any time on an existing vault: it only adds what is missing.

## Steps

1. Ask where the vault should live if the user has not said. An existing Obsidian vault is fine.
2. Run, from this skill's directory:
   ```bash
   python3 scripts/vault.py init "<vault>"
   ```
   It copies `template/` into the vault and never overwrites a file that exists. If the folder
   already has a `CLAUDE.md`, show the user both and offer to merge them; do not merge unasked.
3. Fill in the three files that make every later output sharper, one at a time, by asking:
   - `1_knowledge/reference/identity.md`: who they are, what they do, what they are building.
   - `1_knowledge/reference/writing-style.md`: ask for three emails they are proud of, put them under Samples, then describe the voice from them.
   - `1_knowledge/reference/tools.md`: which sources they want in `raw/`, and which systems are read-only.
4. Offer next steps: `sync-source` for the first source, or drop a few notes in `0_inbox/` and run `refresh-knowledge`.
5. Run `python3 scripts/vault.py check "<vault>"` and show the result.

## Safety rules

- Never overwrite or delete a file in an existing folder.
- Do not invent content for the reference files. Leave a section empty rather than guess.
