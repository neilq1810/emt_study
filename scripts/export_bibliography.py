#!/usr/bin/env python3
"""Export citations/bibliography.json to BibTeX and CSV.

Usage:
    python3 scripts/export_bibliography.py

Reads:  citations/bibliography.json
Writes: citations/bibliography.bib, citations/bibliography.csv

No third-party dependencies (stdlib only) so it runs in any environment.
"""
from __future__ import annotations

import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "citations" / "bibliography.json"
BIB = ROOT / "citations" / "bibliography.bib"
CSV_OUT = ROOT / "citations" / "bibliography.csv"

# Map our 'type' field to BibTeX entry types.
BIBTEX_TYPE = {
    "article": "article",
    "inproceedings": "inproceedings",
    "conference": "inproceedings",
    "book": "book",
    "phdthesis": "phdthesis",
    "dissertation": "phdthesis",
    "patent": "patent",
    "standard": "techreport",
    "techreport": "techreport",
    "misc": "misc",
}

CSV_FIELDS = [
    "id", "type", "title", "authors", "year", "venue", "volume", "issue",
    "pages", "doi", "url", "publisher", "source_type", "keywords",
    "relevance", "confidence", "verified", "notes",
]


def fmt_authors_bibtex(authors: list[str]) -> str:
    return " and ".join(authors)


def to_bibtex(entry: dict) -> str:
    bt = BIBTEX_TYPE.get(entry.get("type", "misc"), "misc")
    lines = [f"@{bt}{{{entry['id']},"]
    fields = {
        "title": entry.get("title"),
        "author": fmt_authors_bibtex(entry.get("authors", [])),
        "year": entry.get("year"),
        "journal": entry.get("venue") if bt == "article" else None,
        "booktitle": entry.get("venue") if bt == "inproceedings" else None,
        "volume": entry.get("volume"),
        "number": entry.get("issue"),
        "pages": entry.get("pages"),
        "doi": entry.get("doi"),
        "url": entry.get("url"),
        "publisher": entry.get("publisher"),
        "note": entry.get("notes"),
    }
    for key, val in fields.items():
        if val:
            lines.append(f"  {key} = {{{val}}},")
    lines.append("}")
    return "\n".join(lines)


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: {SRC} not found", file=sys.stderr)
        return 1
    data = json.loads(SRC.read_text(encoding="utf-8"))
    entries = data.get("entries", [])

    # BibTeX
    BIB.write_text(
        "\n\n".join(to_bibtex(e) for e in entries) + "\n", encoding="utf-8"
    )

    # CSV
    with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for e in entries:
            row = dict(e)
            row["authors"] = "; ".join(e.get("authors", []))
            row["keywords"] = "; ".join(e.get("keywords", []))
            writer.writerow(row)

    print(f"Wrote {len(entries)} entries -> {BIB.name}, {CSV_OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
