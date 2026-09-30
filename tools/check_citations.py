#!/usr/bin/env python3
"""REC-15 — CI citation check (pure stdlib).

Two checks over the repository Markdown corpus (vendor `senior-rules/`,
`.git/`, `.github/` excluded from *scanning*; their files still count as
definition and resolution targets):

1. IDS — every cited ID from the REC-15 series set
   (FR, TC, BR, RISK, ASM, DEP, GAP, AC, SEC, SEC-REQ, REC, TD) must be
   *defined* somewhere: a filename stem, a table first cell, a `**bold**`
   span, or a heading. Group references (e.g. `AC-NFR-011` for the family
   `AC-NFR-011-01/-02`) pass when any member is defined. Lines that state
   the next free allocator ID ("next free …", "the next is …") are
   forward-allocation prose and are skipped.

2. PATHS — every backticked file path (`.md` / `.py`, optional `:line`
   suffix, ` §…` tail) must resolve, in order: literally from the
   repository root / `docs/` / the citing file's directory, or by unique
   *tail-boundary match* (the cited tail `entities/wallet.md` matches
   `docs/08-database/entities/wallet.md`) — the corpus's documented
   domain-relative shorthand. Globs/templates and two explicit sets are
   skipped: ILLUSTRATIVE (anti-pattern filename examples) and PHANTOM
   (IDs/paths cited *as evidence of not existing*, per open findings
   CT-12/finding 7 and HAL-12).

Exit codes: 0 = green, 1 = dangling citation(s) found.
Usage: python tools/check_citations.py [--quiet]
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_SKIP_DIRS = {".git", ".github", "senior-rules", "node_modules"}
INDEX_SKIP_DIRS = {".git", "node_modules"}

# --------------------------------------------------------------------------
# ID series (REC-15 acceptance set). Patterns are uppercase-only and
# guarded against mid-token matches (e.g. `DOC-FR-000` must not count as
# `FR-000`), so template placeholders (FR-nnn, AC-FRnnn-05, GAP-NNN) and
# document_id frontmatter never match.
# --------------------------------------------------------------------------
GUARD = r"(?<![A-Za-z0-9-])"
SERIES: dict[str, re.Pattern[str]] = {
    "FR": re.compile(GUARD + r"FR-\d{3}\b"),
    "TC": re.compile(GUARD + r"TC-\d{3}\b"),
    "BR": re.compile(GUARD + r"BR-[A-Z]{2,5}-\d{2}\b"),
    "RISK": re.compile(GUARD + r"RISK-\d{3}\b"),
    "ASM": re.compile(GUARD + r"ASM-\d{2}\b"),
    "DEP": re.compile(GUARD + r"DEP-\d{2}\b"),
    "GAP": re.compile(GUARD + r"GAP-\d{2,3}\b"),
    "AC": re.compile(GUARD + r"AC-(?:[A-Z0-9]+-)+[A-Z0-9]*\d{2}\b"),
    "SEC": re.compile(GUARD + r"SEC-\d{3}\b"),
    "SEC-REQ": re.compile(GUARD + r"SEC-REQ-\d{3}\b"),
    "REC": re.compile(GUARD + r"REC-\d{2}\b"),
    "TD": re.compile(GUARD + r"TD-\d{2}\b"),
}
ALL_ID = re.compile(
    GUARD
    + r"(?:FR-\d{3}|TC-\d{3}|BR-[A-Z]{2,5}-\d{2}|RISK-\d{3}|ASM-\d{2}"
    + r"|DEP-\d{2}|GAP-\d{2,3}|AC-(?:[A-Z0-9]+-)+[A-Z0-9]*\d{2}"
    + r"|SEC-REQ-\d{3}|SEC-\d{3}|REC-\d{2}|TD-\d{2})\b"
)

# Forward-allocation prose: the allocator file states the next free ID.
FORWARD_LINE = re.compile(r"next free|the next is|next is\b", re.I)

# Documented phantom IDs — cited *as evidence of not existing*.
#   AC-WF-012-01: consistency-audit finding 7 / CT-12 (zero definitions).
PHANTOM_IDS = {"AC-WF-012-01"}
# Per-file phantom cites (historical self-references inside the change
# rows that document the correction itself).
PHANTOM_ID_PAIRS = {
    ("docs/19-traceability/core/requirements-to-tests.md", "AC-FR020-05"),
}

# Illustrative filename examples / anti-patterns — never real targets.
ILLUSTRATIVE_PATHS = {
    "lowercase-kebab-case.md",
    "final.md",
    "latest.md",
    "new-final.md",
    "draft2.md",
    "Untitled.md",
    "sub-orders.md",
    "workflow-013.md",
}

# Documented phantom paths: (citing file relpath, raw token).
#   07-api/authorization.md: quoted by HAL-12 as the broken cite it
#   documents, by actors-and-roles.md's change row that records the
#   correction, and by the consistency/recommendation/session records of
#   that same fix (the live cite now points at 06-backend/authorization.md).
#   Session work files quote dead paths *as evidence of the fix* — allow
#   only the file that narrates the correction, never a new live citation.
PHANTOM_PATHS = {
    ("docs/20-validation/core/hallucination-audit.md", "07-api/authorization.md"),
    ("docs/00-project-overview/actors-and-roles.md", "07-api/authorization.md"),
    ("docs/20-validation/core/consistency-audit.md", "07-api/authorization.md"),
    ("docs/21-completion/recommendations.md", "07-api/authorization.md"),
    ("docs/sessions/session-008-archdoc-brinv-citation-ci.md", "07-api/authorization.md"),
    ("session_track.md", "07-api/authorization.md"),
}

# Backticked tokens that look like file paths.
BACKTICK = re.compile(r"`([^`\n]+)`")
PATH_SUFFIX = re.compile(r":\d+(?:[,\-]\d+)*$")
SECTION_TAIL = re.compile(r"\s+§.*$")
PATH_OK = re.compile(r"^[A-Za-z0-9_./\-]+\.(?:md|py)$")

# Definition positions
TABLE_FIRST_CELL = re.compile(r"^\|[ \t]*([^|\n]+?)\s*\|", re.M)
BOLD_SPAN = re.compile(r"\*\*([^*\n]+)\*\*")
HEADING = re.compile(r"^#{1,6}\s+(.+)$", re.M)


def walk(skip: set[str]) -> list[str]:
    out: list[str] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for fn in filenames:
            out.append(os.path.join(dirpath, fn))
    return out


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def main() -> int:
    quiet = "--quiet" in sys.argv[1:]

    scan_files = [
        p
        for p in walk(SCAN_SKIP_DIRS)
        if p.endswith(".md") and os.path.getsize(p) > 0
    ]
    index_files = walk(INDEX_SKIP_DIRS)
    all_rel = [rel(p) for p in index_files]

    # ---------------- definitions + group prefixes ----------------
    defined: set[str] = set()
    for path in index_files:
        if not path.endswith(".md"):
            continue
        stem = os.path.basename(path)[: -len(".md")]
        if ALL_ID.fullmatch(stem):
            defined.add(stem)
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            continue
        for cell in TABLE_FIRST_CELL.findall(text):
            defined.update(ALL_ID.findall(cell))
        for span in BOLD_SPAN.findall(text):
            defined.update(ALL_ID.findall(span))
        for head in HEADING.findall(text):
            defined.update(ALL_ID.findall(head))

    groups: set[str] = set()
    for d in defined:
        idx = 0
        while (idx := d.find("-", idx + 1)) != -1:
            groups.add(d[:idx])

    # ---------------- check pass ----------------
    dangling_ids: list[str] = []
    dangling_paths: list[str] = []
    cites = 0

    for path in scan_files:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            continue
        here = os.path.dirname(path)
        rpath = rel(path)

        # IDs: every occurrence is a citation; must be defined above.
        for lineno, line in enumerate(text.splitlines(), 1):
            if FORWARD_LINE.search(line):
                continue  # allocator prose: next free ID is not a cite
            for tok in ALL_ID.findall(line):
                cites += 1
                if (
                    tok in defined
                    or tok in PHANTOM_IDS
                    or tok in groups
                    or (rpath, tok) in PHANTOM_ID_PAIRS
                ):
                    continue
                dangling_ids.append(f"{rpath}:{lineno}: {tok}")

        # Paths: backticked file references.
        for raw in BACKTICK.findall(text):
            tok = raw.strip()
            if "http" in tok or "*" in tok or "<" in tok or "{" in tok:
                continue
            tok = SECTION_TAIL.sub("", tok).strip()
            tok = PATH_SUFFIX.sub("", tok).strip()
            if not tok or not PATH_OK.match(tok):
                continue
            if "nnn" in tok or "NNN" in tok:
                continue  # template placeholder
            if (rpath, tok) in PHANTOM_PATHS or tok in ILLUSTRATIVE_PATHS:
                continue
            if "/" not in tok:
                if os.path.isfile(os.path.join(ROOT, tok)) or any(
                    os.path.basename(r) == tok for r in all_rel
                ):
                    continue
                dangling_paths.append(f"{rpath}: {raw}")
                continue
            candidates = [
                os.path.join(ROOT, tok),
                os.path.join(ROOT, "docs", tok),
                os.path.join(here, tok),
            ]
            if any(os.path.isfile(c) for c in candidates):
                continue
            # tail-boundary match: cited tail aligns on a path separator
            if any(r == tok or r.endswith("/" + tok) for r in all_rel):
                continue
            dangling_paths.append(f"{rpath}: {raw}")

    # ---------------- report ----------------
    seen: set[str] = set()
    uniq_ids = [d for d in dangling_ids if not (d in seen or seen.add(d))]
    seen.clear()
    uniq_paths = [d for d in dangling_paths if not (d in seen or seen.add(d))]

    if not quiet:
        for d in uniq_ids:
            print(f"ID    dangling: {d}")
        for d in uniq_paths:
            print(f"PATH  dangling: {d}")
    total = len(uniq_ids) + len(uniq_paths)
    print(
        f"check_citations: {len(scan_files)} files scanned; "
        f"{cites} ID citations; {len(uniq_ids)} unresolved ID(s); "
        f"{len(uniq_paths)} dangling path(s); total problems: {total}"
    )
    if total:
        print("RESULT: FAIL — dangling citations (REC-15)")
        return 1
    print("RESULT: PASS — every cited path and ID resolves (REC-15)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
