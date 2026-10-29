#!/usr/bin/env python3
"""Set up and check a Second Brain vault. Python 3.10+, standard library only.

  vault.py init  VAULT                       copy the folder skeleton; never overwrites a file
  vault.py check VAULT [--today YYYY-MM-DD] [--json]

check exits 1 when it finds an error (a card in the wrong lane, a link to a file that
does not exist, a malformed date). Warnings (backlog, overdue cards, stale sources,
links to pages not written yet) are reported but do not fail.
"""
import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "template"
LANES = ("todo", "handoff", "review", "done")
WIKI_TYPES = {"person", "project", "company", "topic", "decision", "concept"}
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")


def unquote(value):
    value = value.strip()
    if len(value) > 1 and value[0] == value[-1] and value[0] in "'\"":
        value = value[1:-1]
    return "" if value.lower() in ("null", "none", "~") else value


def frontmatter(path):
    """The YAML subset the vault uses: `key: value`, `key: [a, b]` and `- item` lists."""
    text = path.read_text(encoding="utf-8")
    block = re.match(r"---\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    meta, key = {}, None
    for line in block.group(1).splitlines() if block else []:
        item = re.match(r"\s*-\s+(.*)", line)
        if item and key:
            if not isinstance(meta[key], list):
                meta[key] = []
            meta[key].append(unquote(item.group(1)))
            continue
        pair = re.match(r"([A-Za-z_]\w*):\s*(.*)", line)
        if pair:
            key, value = pair.group(1), pair.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                meta[key] = [unquote(v) for v in value[1:-1].split(",") if v.strip()]
            else:
                meta[key] = unquote(value)
    return meta


def as_list(value):
    return value if isinstance(value, list) else [value] if value else []


def parse_date(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def init(vault):
    created = 0
    for src in sorted(TEMPLATE.rglob("*")):
        if src.name == ".DS_Store":
            continue
        dst = vault / src.relative_to(TEMPLATE)
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        elif not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            created += 1
    print(f"init: {created} files created in {vault}, existing files left untouched")


def check(vault, today):
    problems = []
    notes = list(vault.rglob("*.md"))
    stems = {p.stem.lower() for p in notes}

    def rel(p):
        return p.relative_to(vault).as_posix()

    def report(level, path, message):
        problems.append({"level": level, "file": rel(path), "message": message})

    def resolves(name):
        """A wikilink target: `Name`, `folder/Name`, `Name|alias` or `Name#heading`."""
        return re.split(r"[|#]", name)[0].split("/")[-1].strip().lower() in stems

    def broken_ref(ref):
        """Frontmatter references are checked when they are `[[wikilinks]]` or `.md` paths.
        URLs and free text ("call with Sam, 3 May") are left alone."""
        ref = ref.strip()
        if ref.startswith("[[") and ref.endswith("]]"):
            return not resolves(ref[2:-2])
        if ref.startswith(("~", "/")):
            return ref.endswith(".md") and not Path(ref).expanduser().exists()
        return ref.endswith(".md") and not (vault / ref).exists()

    def md(folder):
        return sorted((vault / folder).rglob("*.md")) if (vault / folder).is_dir() else []

    raw = md("1_knowledge/raw")
    backlog = 0
    for p in raw:
        m = frontmatter(p)
        if m.get("type") != "raw_source":
            report("warning", p, "raw file without `type: raw_source`")
        if m.get("status") != "processed":
            backlog += 1

    wiki = md("1_knowledge/wiki")
    broken = 0
    for p in wiki:
        m = frontmatter(p)
        if m.get("type") not in WIKI_TYPES:
            report("warning", p, f"wiki page type `{m.get('type', '')}` is not one of {sorted(WIKI_TYPES)}")
        for link in WIKILINK.findall(p.read_text(encoding="utf-8")):
            if not resolves(link):
                broken += 1
                report("warning", p, f"[[{link}]] has no page yet")

    lanes, overdue = {}, 0
    for lane in LANES:
        cards = md(f"2_tasks/{lane}")
        lanes[lane] = len(cards)
        for p in cards:
            m = frontmatter(p)
            if m.get("type") != "task":
                report("warning", p, "task card without `type: task`")
            if m.get("status") != lane:
                report("error", p, f"status is `{m.get('status', '')}` but the card sits in {lane}/")
            due = m.get("due")
            if due and not parse_date(due):
                report("error", p, f"due date `{due}` is not YYYY-MM-DD")
            elif due and lane != "done" and parse_date(due) < today:
                overdue += 1
                report("warning", p, f"overdue since {due}")
            if lane in ("review", "done") and not m.get("output"):
                report("warning", p, f"in {lane}/ with no output linked")
            for ref in as_list(m.get("wiki")) + as_list(m.get("source")) + as_list(m.get("output")):
                if broken_ref(ref):
                    report("error", p, f"links to `{ref}`, which does not exist")

    outputs = md("4_outputs")
    for p in outputs:
        m = frontmatter(p)
        if m.get("type") != "output" or not m.get("kind"):
            report("warning", p, "output without `type: output` and a `kind`")
        for ref in as_list(m.get("task")):
            if broken_ref(ref):
                report("error", p, f"links to task `{ref}`, which does not exist")

    sources, stale = 0, 0
    for p in md("3_operations/health"):
        m = frontmatter(p)
        if m.get("type") == "issue" and m.get("status") != "resolved":
            report("warning", p, "open issue")
        if m.get("type") != "source_health":
            continue
        sources += 1
        last, hours = parse_date(m.get("last_sync")), m.get("cadence_hours", "24")
        if m.get("status") == "error":
            report("error", p, f"source reports an error: {m.get('error') or 'no detail'}")
        elif not last or not hours.isdigit():
            report("error", p, "needs `last_sync: YYYY-MM-DD` and a whole number in `cadence_hours`")
        elif (today - last).days * 24 > 2 * int(hours):
            stale += 1
            report("warning", p, f"stale: last sync {last}, expected every {hours} h")

    inbox = [p for p in (vault / "0_inbox").glob("*") if not p.name.startswith(".")] if (vault / "0_inbox").is_dir() else []
    return {
        "vault": str(vault),
        "today": today.isoformat(),
        "counts": {
            "raw": len(raw), "backlog": backlog, "wiki": len(wiki), "broken_links": broken,
            **{f"tasks_{lane}": n for lane, n in lanes.items()}, "overdue": overdue,
            "outputs": len(outputs), "sources": sources, "stale_sources": stale, "inbox": len(inbox),
        },
        "errors": sum(p["level"] == "error" for p in problems),
        "problems": problems,
    }


def print_report(r):
    c = r["counts"]
    print(f"vault {r['vault']} on {r['today']}")
    print(f"  raw      {c['raw']} files, {c['backlog']} not processed yet")
    print(f"  wiki     {c['wiki']} pages; links to pages not written yet: {c['broken_links']}")
    print(f"  tasks    todo {c['tasks_todo']}, handoff {c['tasks_handoff']}, review {c['tasks_review']}, "
          f"done {c['tasks_done']}; {c['overdue']} overdue")
    print(f"  outputs  {c['outputs']}")
    print(f"  sources  {c['sources']}, {c['stale_sources']} stale")
    print(f"  inbox    to sort: {c['inbox']}")
    for p in r["problems"]:
        print(f"{p['level'].upper():8} {p['file']}: {p['message']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["init", "check"])
    ap.add_argument("vault", type=Path)
    ap.add_argument("--today", type=date.fromisoformat, default=date.today())
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.command == "init":
        return init(a.vault)
    if not a.vault.is_dir():
        sys.exit(f"check: {a.vault} is not a folder")
    r = check(a.vault.resolve(), a.today)
    print(json.dumps(r, indent=2)) if a.json else print_report(r)
    sys.exit(1 if r["errors"] else 0)


if __name__ == "__main__":
    main()
