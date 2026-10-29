#!/usr/bin/env bash
# Builds a vault from the template, adds the fictional example on top, and checks what
# vault.py reports. One assertion per line: under `set -e`, `a && b` would not stop the script.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
HERE="$(cd "$(dirname "$0")" && pwd)"
VAULT_PY="$HERE/../skills/init-vault/scripts/vault.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
V="$TMP/vault"
fails() { if "$@"; then echo "expected a failure: $*" >&2; exit 1; fi; }
count() { python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["counts"][sys.argv[2]])' "$TMP/report.json" "$1"; }
snapshot() { (cd "$V" && find . -type f -exec cksum {} + | sort); }

echo "--- init builds the skeleton"
python3 "$VAULT_PY" init "$V"
test -f "$V/CLAUDE.md"
test -f "$V/1_knowledge/reference/schemas.md"
test -d "$V/2_tasks/handoff"
test -d "$V/5_archive"

echo "--- init again creates nothing and keeps your edits"
echo "My own rule." >> "$V/CLAUDE.md"
second="$(python3 "$VAULT_PY" init "$V")"
test "${second%% files created*}" = "init: 0"
grep -q "My own rule." "$V/CLAUDE.md"

echo "--- an empty vault is healthy"
python3 "$VAULT_PY" check "$V" --today 2026-10-27

echo "--- the example vault"
cp -R "$HERE/vault/." "$V/"
python3 "$VAULT_PY" check "$V" --today 2026-10-27
python3 "$VAULT_PY" check "$V" --today 2026-10-27 --json > "$TMP/report.json"
test "$(count raw)" -eq 3
test "$(count backlog)" -eq 1
test "$(count wiki)" -eq 5
test "$(count broken_links)" -eq 1
test "$(count tasks_todo)" -eq 2
test "$(count tasks_review)" -eq 1
test "$(count tasks_done)" -eq 1
test "$(count overdue)" -eq 1
test "$(count outputs)" -eq 2
test "$(count sources)" -eq 2
test "$(count stale_sources)" -eq 1
test "$(count inbox)" -eq 1
grep -q '"errors": 0' "$TMP/report.json"

echo "--- dates move with --today"
python3 "$VAULT_PY" check "$V" --today 2026-10-24 --json > "$TMP/report.json"
test "$(count overdue)" -eq 0
test "$(count stale_sources)" -eq 0

echo "--- check reads, never writes"
before="$(snapshot)"
python3 "$VAULT_PY" check "$V" --today 2026-10-27 > /dev/null
test "$before" = "$(snapshot)"

echo "--- a card in the wrong lane fails"
cp -R "$V" "$TMP/wrong-lane"
sed -i.bak 's/^status: review$/status: todo/' "$TMP/wrong-lane/2_tasks/review/2026-10-20-winter-blend-label-brief.md"
fails python3 "$VAULT_PY" check "$TMP/wrong-lane" --today 2026-10-27

echo "--- a card linking to a missing page fails"
cp -R "$V" "$TMP/missing-page"
mv "$TMP/missing-page/1_knowledge/wiki/people/Sam Rivera.md" "$TMP/sam.md"
fails python3 "$VAULT_PY" check "$TMP/missing-page" --today 2026-10-27

echo "--- a due date that is not a date fails"
cp -R "$V" "$TMP/bad-date"
sed -i.bak 's/^due: 2026-11-15$/due: mid November/' "$TMP/bad-date/2_tasks/todo/2026-10-22-book-lisbon-fair-stand.md"
fails python3 "$VAULT_PY" check "$TMP/bad-date" --today 2026-10-27

echo "--- untyped notes and free-text sources warn without failing"
cp -R "$V" "$TMP/loose"
sed -i.bak '/^type: raw_source$/d' "$TMP/loose/1_knowledge/raw/email/2026-10-22-green-bean-quote.md"
sed -i.bak "s|^source: \[\]$|source: [call with Sam, 3 May, https://example.com/fair, $HERE/vault/0_inbox/2026-10-26-voice-memo-packaging.md]|" "$TMP/loose/2_tasks/todo/2026-10-22-book-lisbon-fair-stand.md"
python3 "$VAULT_PY" check "$TMP/loose" --today 2026-10-27 > "$TMP/loose.txt"
grep -q 'raw file without `type: raw_source`' "$TMP/loose.txt"

echo "All checks passed."
