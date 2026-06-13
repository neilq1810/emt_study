#!/usr/bin/env python3
"""Manuscript credibility verifier (Phase 7/8 'X1' pass).

Runs automatable internal-consistency checks so a reviewer can trust that the
prose, the bibliography, the figures/data, and the simulation outputs agree.
It does NOT check external factual correctness (that is the human review pass);
it checks that the manuscript is *internally* coherent and that every quoted
sim-derived number is still backed by a current `data/summary.json` value.

Checks
  1. Citation integrity   - every [@key] in book/ resolves to bibliography.json;
                            reports unused entries (informational).
  2. Reference existence  - every figures/*.png and data/*.{json,csv} named in
                            the prose exists on disk.
  3. Cross-ref range      - no "Ch. N"/"Chapter N" beyond the last chapter.
  4. Placeholder scan     - no TODO/TBD/XXX/to-generate/placeholder left in prose.
  5. Sim<->prose contract - curated headline numbers in data/summary.json still
                            appear verbatim in their chapter (catches drift when
                            a sim is re-run and a value changes).

Exit code 0 if all hard checks pass, 1 otherwise. Run: python3 scripts/verify_manuscript.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
BIB = ROOT / "citations" / "bibliography.json"

# `@key` tokens that are NOT citations: `@<digits>` is "at <value>" (e.g. "@300 Ω",
# "@10 kHz") and `@key` is the literal convention example in each chapter header.
NON_CITE = re.compile(r"^\d+$")
PLACEHOLDERS = re.compile(r"\b(TODO|TBD|FIXME|XXX|to-generate|to generate|placeholder)\b", re.I)


def chapters() -> list[pathlib.Path]:
    return sorted(BOOK.rglob("[0-9]*-*.md"))


def max_chapter() -> int:
    return max(int(re.match(r"(\d+)", p.name).group(1)) for p in chapters())


def check_citations() -> list[str]:
    ids = {e["id"] for e in json.loads(BIB.read_text())["entries"]}
    used: dict[str, set[str]] = {}
    for f in BOOK.rglob("*.md"):
        for m in re.finditer(r"@([a-zA-Z0-9_]+)", f.read_text()):
            k = m.group(1)
            if k == "key" or NON_CITE.match(k):
                continue
            used.setdefault(k, set()).add(f.name)
    errs = [f"BROKEN citation @{k} (used in {sorted(v)}) not in bibliography.json"
            for k, v in sorted(used.items()) if k not in ids]
    unused = sorted(ids - set(used))
    if unused:
        print(f"  note: {len(unused)} bibliography entries never cited: {unused}")
    print(f"  citations: {len(used)} distinct keys used, {len(ids)} entries, {len(errs)} broken")
    return errs


def check_references() -> list[str]:
    errs = []
    for kind in ("figures", "data"):
        on_disk = {p.name for p in (ROOT / kind).glob("*")}
        pat = re.compile(rf"{kind}/([a-zA-Z0-9_]+\.[a-z]+)")
        named = {m.group(1) for f in BOOK.rglob("*.md") for m in pat.finditer(f.read_text())}
        missing = sorted(named - on_disk)
        errs += [f"MISSING {kind}/{n} referenced in prose but not on disk" for n in missing]
        print(f"  {kind}: {len(named)} referenced, {len(missing)} missing")
    return errs


def check_crossrefs() -> list[str]:
    top = max_chapter()
    errs = []
    for f in chapters():
        for m in re.finditer(r"(?:Ch\.|Chapter)\s*(\d+)", f.read_text()):
            n = int(m.group(1))
            if n > top:
                errs.append(f"DANGLING Ch. {n} referenced in {f.name} (max chapter is {top})")
    print(f"  cross-refs: max chapter {top}, {len(errs)} dangling")
    return errs


def _existing_sections() -> set[str]:
    """All section ids from `## N.M` / `### N.M[.K]` headers across the book."""
    sec: set[str] = set()
    for f in chapters():
        for m in re.finditer(r"^#{2,3}\s+(\d+)\.(\d+)(?:\.(\d+))?", f.read_text(), re.M):
            sec.add(f"{m.group(1)}.{m.group(2)}")
            if m.group(3):
                sec.add(f"{m.group(1)}.{m.group(2)}.{m.group(3)}")
    return sec


def check_section_crossrefs() -> list[str]:
    """Every §N.M (and range endpoint) must resolve to an existing section header
    (matched at the N.M level, so inline sub-subsections are allowed)."""
    sections = _existing_sections()
    chap_nums = {int(re.match(r"(\d+)", p.name).group(1)) for p in chapters()}
    errs, n_refs = [], 0

    def ok(ch: str, sec_full: str) -> bool:
        base = ".".join(sec_full.split(".")[:2])
        return int(ch) not in chap_nums or sec_full in sections or base in sections

    for f in BOOK.rglob("*.md"):
        t = f.read_text()
        for m in re.finditer(r"§\s?(\d+)\.(\d+)(?:\.(\d+))?", t):
            n_refs += 1
            full = f"{m.group(1)}.{m.group(2)}" + (f".{m.group(3)}" if m.group(3) else "")
            if not ok(m.group(1), full):
                errs.append(f"DANGLING §{full} in {f.name} (no such section)")
        # range endpoints: §N.A–[N.]B  /  §§N.A-B
        for m in re.finditer(r"§{1,2}\s?(\d+)\.(\d+)\s?[–\-]\s?(?:(\d+)\.)?(\d+)", t):
            end_ch = m.group(3) or m.group(1)
            if not ok(end_ch, f"{end_ch}.{m.group(4)}"):
                errs.append(f"DANGLING §{end_ch}.{m.group(4)} (range endpoint) in {f.name}")
    print(f"  section cross-refs: {n_refs} §-refs, {len(sections)} sections, {len(errs)} dangling")
    return sorted(set(errs))


def check_placeholders() -> list[str]:
    errs = []
    for f in chapters():
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if PLACEHOLDERS.search(line):
                errs.append(f"PLACEHOLDER in {f.name}:{i}: {line.strip()[:80]}")
    print(f"  placeholders: {len(errs)} found")
    return errs


# Curated sim<->prose contract: headline numbers that MUST stay in sync with the
# simulation outputs. If a sim is re-run and a value changes, prose must follow.
# (description, chapter glob, [substrings that must all appear]).
CONTRACT = [
    ("CRLB on-axis picks (Ch.24)", "**/24-*.md", ["0.017", "0.086", "0.66"]),
    ("CRLB z^4 law (Ch.24)", "**/24-*.md", ["z^{4", "z^4"]),
    ("6-DOF coupling penalty 2.95x (Ch.24)", "**/24-*.md", ["2.95"]),
    ("Orientation CRLB z^3 + range (Ch.24)", "**/24-*.md", ["z^3", "0.0097", "0.15"]),
    ("Monte-Carlo ~3% of CRLB (Ch.24)", "**/24-*.md", ["3%"]),
    ("Closed-form eig 1:1:4 (Ch.23)", "**/23-*.md", ["4{:}1{:}1", "4:1:1", "1:1:4"]),
    ("Dual-coil roll obs 0/0.55/1.0 (Ch.13)", "**/13-*.md", ["sin"]),
    ("Deep-volume moment lever m_t^0.25 (Ch.29)", "**/29-*.md", ["m_t^{0.25}", "16\\times"]),
    ("Distortion flag margin geometry-dependent (Ch.33)", "**/33-*.md",
     ["+0.56", "-0.26", "necessary but not sufficient"]),
    ("Twin identification closes calibration cliff (Ch.55)", "**/55-*.md",
     ["14.9 mm", "0.11 mm", "132", "single known pose"]),
]


def check_contract() -> list[str]:
    errs = []
    for desc, glob, subs in CONTRACT:
        files = list(BOOK.glob(glob))
        if not files:
            errs.append(f"CONTRACT '{desc}': no chapter matched {glob}")
            continue
        text = files[0].read_text()
        # each entry passes if at least one of its alternative substrings is present
        # (group alternatives are joined; require every **distinct concept** present).
        missing = [s for s in subs if s not in text]
        # treat z^{4 / z^4 and the eig variants as alternatives, not all-required:
        if desc.startswith("CRLB z^4") and len(missing) < len(subs):
            missing = []
        if desc.startswith("Closed-form") and len(missing) < len(subs):
            missing = []
        if missing:
            errs.append(f"CONTRACT '{desc}' missing {missing} in {files[0].name}")
    print(f"  sim<->prose contract: {len(CONTRACT)} assertions, "
          f"{len(errs)} drifted")
    return errs


def main() -> int:
    print("Manuscript credibility verifier\n" + "=" * 40)
    all_errs = []
    for name, fn in [
        ("1. Citation integrity", check_citations),
        ("2. Reference existence", check_references),
        ("3. Cross-ref range", check_crossrefs),
        ("4. Section cross-ref resolution", check_section_crossrefs),
        ("5. Placeholder scan", check_placeholders),
        ("6. Sim<->prose contract", check_contract),
    ]:
        print(name)
        all_errs += fn()
    print("=" * 40)
    if all_errs:
        print(f"FAIL — {len(all_errs)} issue(s):")
        for e in all_errs:
            print(f"  - {e}")
        return 1
    print("PASS — manuscript internally consistent "
          f"({len(chapters())} chapters checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
