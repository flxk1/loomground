#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 flxk1
"""CATALOGUE.md (the tree) and CATALOGUE.json (the same tree as data) agree.

Always: same repositories both ways, family = the tree branch, role = the tree
one-liner, record shape, pipeline references. With --siblings DIR..., each
record's description is compared to the README one-liner of DIR/<repo> (its main branch when a checkout).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIELDS = {"repo", "family", "role", "description", "pipeline_position", "depends_on", "tools", "skills", "install", "url"}
NAME = re.compile(r"[A-Za-z0-9][\w.-]*")
NODE = re.compile(r"^((?:[│ ]   )*)[├└]── (.*)$")


def tree(md: str) -> dict[str, tuple[str, str]]:
    body = md.split("```")[1].splitlines()[1:]
    stack: list[str] = []
    out: dict[str, tuple[str, str]] = {}
    for line in body:
        m = NODE.match(line)
        if not m:
            continue
        depth = len(m.group(1)) // 4
        name, dash, tail = m.group(2).partition("—")
        name = name.strip()
        stack = stack[:depth]
        if dash and NAME.fullmatch(name):
            out[name] = ("/".join(stack), tail.strip())
        else:
            stack.append(re.sub(r"\s{2,}.*$", "", name).strip())
    return out


def oneliner(text: str) -> str | None:
    lines = [l for l in text.splitlines() if not l.startswith("<!--")]
    for i, l in enumerate(lines):
        if l.startswith("# "):
            for m in lines[i + 1:]:
                s = m.strip()
                if s and not (s.startswith("**") and s.endswith("**")):
                    return s
    return None


def main(argv: list[str]) -> int:
    siblings = argv[argv.index("--siblings") + 1:] if "--siblings" in argv else []
    with open(os.path.join(ROOT, "CATALOGUE.md"), encoding="utf-8") as fh:
        md = tree(fh.read())
    with open(os.path.join(ROOT, "CATALOGUE.json"), encoding="utf-8") as fh:
        doc = json.load(fh)
    errors: list[str] = []
    records = {r.get("repo"): r for r in doc.get("repos", [])}
    for r in sorted(md.keys() - records.keys()):
        errors.append(f"{r}: in CATALOGUE.md, no record in CATALOGUE.json")
    for r in sorted(records.keys() - md.keys()):
        errors.append(f"{r}: record in CATALOGUE.json, not in the CATALOGUE.md tree")
    for name, rec in records.items():
        if set(rec) != FIELDS:
            errors.append(f"{name}: fields {sorted(set(rec) ^ FIELDS)} differ from the contract")
        if name not in md:
            continue
        family, role = md[name]
        if rec.get("family") != family:
            errors.append(f"{name}: family {rec.get('family')!r} != tree branch {family!r}")
        if rec.get("role") != role:
            errors.append(f"{name}: role {rec.get('role')!r} != tree one-liner {role!r}")
        if not isinstance(rec.get("description"), str) or not rec["description"].strip():
            errors.append(f"{name}: description missing")
        if rec.get("url") != f"https://github.com/flxk1/{name}":
            errors.append(f"{name}: url {rec.get('url')!r}")
        pos = rec.get("pipeline_position")
        if pos is not None and not isinstance(pos, int):
            errors.append(f"{name}: pipeline_position {pos!r} is not int|null")
    tools = {t for r in records.values() for t in r.get("tools", [])}
    for key in ("pipeline", "patch_from_documents"):
        for step in doc.get(key, []):
            if step.get("repo") not in records:
                errors.append(f"{key} step {step.get('step')}: repo {step.get('repo')!r} has no record")
            if step.get("tool") is not None and step["tool"] not in tools:
                errors.append(f"{key} step {step.get('step')}: tool {step['tool']!r} in no record")
    checked = 0
    for name, rec in records.items():
        for d in siblings:
            path = os.path.join(d, name, "README.md")
            if os.path.exists(path):
                text = subprocess.run(["git", "-C", os.path.dirname(path), "show", "main:README.md"],
                                      capture_output=True, text=True).stdout
                if not text:
                    with open(path, encoding="utf-8") as fh:
                        text = fh.read()
                got = oneliner(text)
                checked += 1
                if got != rec.get("description"):
                    errors.append(f"{name}: description != README one-liner in {path}\n    json  : {rec.get('description')}\n    readme: {got}")
                break
    if errors:
        print("MISMATCH — CATALOGUE.md and CATALOGUE.json disagree:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"in sync: {len(md)} repositories in the tree, {len(records)} records, "
          f"{len(doc.get('pipeline', []))} pipeline steps, {len(doc.get('patch_from_documents', []))} patch steps"
          + (f"; {checked} descriptions checked against sibling READMEs" if siblings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
