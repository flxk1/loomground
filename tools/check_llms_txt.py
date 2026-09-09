#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 The Loomground Authors
"""Drift check for llms.txt — the compact agent guide.

Expectations are derived from the CANONICAL machine sources — `vocabulary/*.json`
and `schema/token.schema.json`, which track the spec — NOT from the hand-maintained
`language-card.json`. The check then ALSO asserts the card matches those canonical
sources, so neither llms.txt nor the card can silently drift from the language. Run
by CI; exits non-zero on any drift.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def _text(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


# ── canonical truth: the vocabulary + the token schema (these track the spec) ──
NODES = [c["class"] for c in _load("vocabulary/node-classes.json")]
CORDS = [c["type"] for c in _load("vocabulary/cords.json")["permitted"]]
VERDICTS = _load("vocabulary/verdicts.json")["alphabet"]
DECLS = [d["name"] for d in _load("vocabulary/declarations.json")]
GUARD_FIELDS = _load("vocabulary/guard-domain.json")["ranges_over"]
GRADES = _load("vocabulary/grades.json")["levels"]
_tok_schema = _load("schema/token.schema.json")
TOKEN_FIELDS = list(_tok_schema["required"]) + [
    p for p in _tok_schema["properties"] if p not in _tok_schema["required"]
]  # required + optional (tags)

llms = _text("llms.txt")
agents = _text("AGENTS.md")
card = _load("language-card.json")
errors: list[str] = []

# declaration name (canonical) -> the surface keyword it appears as in llms.txt
DECL_KEYWORD = {
    "reservation": "reserve", "quorum": "quorum", "prohibition": "prohibit",
    "temporal": "temporal", "egress-obligation": "obligation", "redress": "redress",
    "party": "party", "delegation": "delegation", "autonomy-grade": "grade",
}


def need(token, what):
    # Word-boundary match, not substring: `auto` must not match inside `automated`,
    # `id` inside `valid`, `L0` inside `L05`. Letters/digits count as word chars.
    if not re.search(r"(?<![A-Za-z0-9])" + re.escape(token) + r"(?![A-Za-z0-9])", llms):
        errors.append(f"llms.txt {what}: {token!r} not found (as a whole word)")


def count_header(label, expected):
    m = re.search(rf"{label} \((\d+)\)", llms)
    if not m:
        errors.append(f"llms.txt: missing count header '{label} (N)'")
    elif int(m.group(1)) != expected:
        errors.append(f"llms.txt: '{label} ({m.group(1)})' header != {expected}")


# ── 1. llms.txt covers every element of the canonical language ──
for n in NODES: need(n, "node class")
for v in VERDICTS: need(v, "verdict")
for t in TOKEN_FIELDS: need(t, "token field")
for f in GUARD_FIELDS: need(f, "guard field")
for lvl in GRADES: need(lvl, "grade level")
for d in DECLS: need(DECL_KEYWORD.get(d, d), f"declaration '{d}'")
count_header("Nodes", len(NODES))
count_header("Cords", len(CORDS))
count_header("Declarations", len(DECLS))
if "llms.txt" not in agents:
    errors.append("AGENTS.md no longer points to llms.txt")
for _term in ("names", "policy", "host"):  # the litmus inlined in AGENTS.md must stay
    if _term not in agents:
        errors.append(f"AGENTS.md litmus no longer states {_term!r}")

# ── 2. the hand-maintained card must itself match the canonical sources ──
def card_eq(field, canonical):
    got = card.get(field)
    if got != canonical:
        errors.append(f"language-card.json {field} {got} != canonical {canonical}")

card_eq("nodes", NODES)
card_eq("verdicts", VERDICTS)
card_eq("token", TOKEN_FIELDS)
card_eq("declarations", DECLS)
for ct in CORDS:  # card cords are formatted strings, e.g. "authority (actor -> gate)"
    if not any(ct in c for c in card.get("cords", [])):
        errors.append(f"language-card.json cords omit the {ct!r} cord type")

if errors:
    print("DRIFT — out of sync with the canonical language:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(
    "in sync with the canonical language (vocabulary + token schema): "
    f"{len(NODES)} nodes, {len(CORDS)} cords, {len(VERDICTS)} verdicts, "
    f"{len(TOKEN_FIELDS)} token fields, {len(GUARD_FIELDS)} guard fields, "
    f"{len(GRADES)} grade levels, {len(DECLS)} declarations — llms.txt covers all, "
    "the card matches, AGENTS.md points to llms.txt."
)
