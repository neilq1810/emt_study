#!/usr/bin/env python3
"""Reader's dependency map: a Part x Part cross-reference heatmap derived from the
manuscript's own `Ch. N` references. Front-matter aid for a 57-chapter book.

Run:  python3 scripts/chapter_graph.py   ->  figures/readers_dependency_map.png
"""
from __future__ import annotations

import re
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
         "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII"]

# chapter number -> part directory; ordered parts
ch_part: dict[int, str] = {}
part_order: list[str] = []
for f in sorted(BOOK.rglob("[0-9]*-*.md")):
    part = f.parent.name
    if part not in part_order:
        part_order.append(part)
    ch_part[int(re.match(r"(\d+)", f.name).group(1))] = part
part_order = sorted(part_order, key=lambda p: int(re.match(r"part-(\d+)", p).group(1)))
pidx = {p: i for i, p in enumerate(part_order)}
P = len(part_order)
M = np.zeros((P, P))

for f in sorted(BOOK.rglob("[0-9]*-*.md")):
    src = pidx[f.parent.name]
    for m in re.finditer(r"Ch\.\s*(\d+)", f.read_text()):
        tgt_ch = int(m.group(1))
        if tgt_ch in ch_part:
            M[src, pidx[ch_part[tgt_ch]]] += 1

def _roman(p: str) -> str:
    return ROMAN[int(re.match(r"part-(\d+)", p).group(1))]


labels = [_roman(p) for p in part_order]
np.fill_diagonal(M, 0)  # emphasize *inter*-part dependencies

fig, ax = plt.subplots(figsize=(9.5, 8.2))
im = ax.imshow(np.log1p(M), cmap="magma_r", aspect="equal")
ax.set_xticks(range(P)); ax.set_xticklabels(labels, fontsize=7)
ax.set_yticks(range(P)); ax.set_yticklabels(labels, fontsize=7)
ax.set_xlabel("Part referenced  (a dependency)"); ax.set_ylabel("Part doing the referencing")
ax.set_title("Reader's dependency map: inter-part cross-references\n"
             "(row Part leans on column Part; from the manuscript's own Ch. N references)",
             fontsize=10)
for i in range(P):
    for j in range(P):
        if M[i, j] >= 4:
            ax.text(j, i, int(M[i, j]), ha="center", va="center", fontsize=6,
                    color="white" if M[i, j] > M.max() * 0.4 else "black")
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cb.set_label("log(1 + reference count)")
fig.tight_layout()
fig.savefig(ROOT / "figures" / "readers_dependency_map.png", dpi=150)
plt.close(fig)

# most-referenced parts (the "load-bearing foundations")
incoming = M.sum(axis=0)
top = sorted(range(P), key=lambda i: -incoming[i])[:6]
print("dependency map written. Most-referenced parts (foundations):")
for i in top:
    print(f"  Part {labels[i]:5s} {part_order[i]:42s} incoming refs={int(incoming[i])}")
