#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 flxk1
"""RELEASES.json (the family's release/pin register) agrees with the checkouts and every pin is a release.

Repos: every CATALOGUE.json repository with a pyproject — version from `[project].version`
or the `[tool.setuptools.dynamic]` attribute, the tag naming that version, its commit, the
package name, whether the package is on PyPI. Edges: every family dependency in a consumer's
`[project].dependencies` (the range) and every `git+https://github.com/flxk1/<dep>@<ref>` in
its requirements-dev.txt (the pin); status is `release` only when the pin is a tagged release
inside the range. Private repositories are listed under `skipped` and need no checkout.

With --siblings DIR (checkouts at pushed main, tags fetched) or LOOMGROUND_RELEASES_ROOT the
register is re-derived and any difference fails; without, the register is checked on its own.
Any edge whose status is not `release` fails unless `accepted` lists it (a dependency without a release, or a transitive pin) — allowed only while
the dependency has no release. --write regenerates the register (PyPI is queried then only).
"""
from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = os.path.join(ROOT, "RELEASES.json")
OWNER = "flxk1"
STATUSES = ("release", "unreleased-commit", "out-of-range", "missing-range")
REPO_FIELDS = ("version", "tag", "commit", "package", "pypi", "family", "tools", "skills")
EDGE_FIELDS = ("consumer", "dependency", "range", "dev_pin", "dev_pin_release", "status")
REQ = re.compile(r"^\s*([A-Za-z0-9][\w.-]*)\s*(\[[^\]]*\])?\s*([^;]*?)\s*(;.*)?$")
PIN = re.compile(rf"git\+https://github\.com/{OWNER}/([\w.-]+?)(?:\.git)?@([^#\s]+)")
TAGVER = re.compile(r"(?:^|-)v(\d[\w.]*)$")
SPEC = re.compile(r"^(===|==|!=|<=|>=|<|>|~=)\s*(\S+)$")
SHA = re.compile(r"^[0-9a-f]{40}$")


def norm(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def vtuple(v: str) -> tuple[int, ...]:
    parts = []
    for p in v.split("."):
        m = re.match(r"\d+", p)
        if not m:
            break
        parts.append(int(m.group()))
    return tuple(parts)


def cmp(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    n = max(len(a), len(b))
    a, b = a + (0,) * (n - len(a)), b + (0,) * (n - len(b))
    return (a > b) - (a < b)


def in_range(version: str, spec: str) -> bool:
    v = vtuple(version)
    for clause in filter(None, (c.strip() for c in spec.split(","))):
        m = SPEC.match(clause)
        if not m:
            return False
        op, want = m.group(1), vtuple(m.group(2))
        c = cmp(v, want)
        if op == "~=":
            ceiling = want[:-2] + (want[-2] + 1,) if len(want) > 1 else want
            ok = c >= 0 and cmp(v, ceiling) < 0
        else:
            ok = {"==": c == 0, "===": c == 0, "!=": c != 0, "<": c < 0, "<=": c <= 0, ">": c > 0, ">=": c >= 0}[op]
        if not ok:
            return False
    return True


def git(path: str, *args: str) -> str:
    return subprocess.run(["git", "-C", path, *args], capture_output=True, text=True).stdout.strip()


def tags_of(path: str) -> dict[str, tuple[str, str]]:
    out = git(path, "for-each-ref", "--format=%(refname:short) %(*objectname) %(objectname)", "refs/tags")
    tags: dict[str, tuple[str, str]] = {}
    for line in out.splitlines():
        parts = line.split()
        tags[parts[0]] = (parts[1], parts[-1])
    return tags


def tag_version(name: str) -> str | None:
    m = TAGVER.search(name)
    return m.group(1) if m else None


def pick(tags: dict[str, tuple[str, str]], version: str) -> str | None:
    names = [t for t in tags if tag_version(t) == version]
    return max(names, key=lambda t: (len(t), t)) if names else None


def tag_at(tags: dict[str, tuple[str, str]], ref: str | None) -> str | None:
    names = [t for t, ids in tags.items() if ref in ids]
    return max(names, key=lambda t: (len(t), t)) if names else None


def version_of(path: str, pp: dict) -> str | None:
    project = pp.get("project", {})
    if isinstance(project.get("version"), str):
        return project["version"]
    attr = pp.get("tool", {}).get("setuptools", {}).get("dynamic", {}).get("version", {}).get("attr")
    if not attr:
        return None
    module, _, name = attr.rpartition(".")
    rel = module.replace(".", os.sep)
    for base in (path, os.path.join(path, "src")):
        for cand in (os.path.join(base, rel + ".py"), os.path.join(base, rel, "__init__.py")):
            if os.path.exists(cand):
                with open(cand, encoding="utf-8") as fh:
                    m = re.search(rf"""^{re.escape(name)}\s*=\s*["']([^"']+)["']""", fh.read(), re.M)
                return m.group(1) if m else None
    return None


def pyproject(path: str) -> dict | None:
    p = os.path.join(path, "pyproject.toml")
    if not os.path.exists(p):
        return None
    with open(p, "rb") as fh:
        return tomllib.load(fh)


def catalogue() -> list[str]:
    return [r["repo"] for r in catalogue_records()]


def catalogue_records() -> list[dict]:
    with open(os.path.join(ROOT, "CATALOGUE.json"), encoding="utf-8") as fh:
        return json.load(fh)["repos"]


def derive(siblings: str, skipped: list[str]) -> tuple[dict, list, list[str]]:
    errors: list[str] = []
    repos: dict[str, dict] = {}
    checkouts: dict[str, str] = {}
    cat = {r["repo"]: r for r in catalogue_records()}
    for name in catalogue():
        path = os.path.join(siblings, name)
        if name in skipped:
            if os.path.isdir(path):
                errors.append(f"{name}: listed under skipped but a checkout exists at {path}")
            continue
        if not os.path.isdir(path):
            errors.append(f"{name}: no checkout at {path} (private repositories go under skipped)")
            continue
        pp = pyproject(path)
        if pp is None:
            repos[name] = {"version": None, "tag": None, "commit": None, "package": None, "pypi": None,
                           "family": cat[name]["family"], "tools": cat[name]["tools"], "skills": cat[name]["skills"]}
            continue
        checkouts[name] = path
        version = version_of(path, pp)
        if version is None:
            errors.append(f"{name}: no version in pyproject or its dynamic attribute")
            continue
        tags = tags_of(path)
        tag = pick(tags, version)
        repos[name] = {"version": version, "tag": tag, "commit": tags[tag][0] if tag else None,
                       "package": pp.get("project", {}).get("name"), "pypi": None,
                       "family": cat[name]["family"], "tools": cat[name]["tools"], "skills": cat[name]["skills"]}
    by_package = {norm(r["package"]): n for n, r in repos.items() if r["package"]}
    edges = []
    for consumer, path in checkouts.items():
        pp = pyproject(path) or {}
        ranges: dict[str, str | None] = {}
        for dep in pp.get("project", {}).get("dependencies", []):
            m = REQ.match(dep)
            if not m:
                continue
            target = by_package.get(norm(m.group(1)))
            if target and target != consumer:
                ranges[target] = m.group(3) or None
        pins: dict[str, str] = {}
        req = os.path.join(path, "requirements-dev.txt")
        if os.path.exists(req):
            with open(req, encoding="utf-8") as fh:
                lines = [l.partition("#")[0] for l in fh]
                for m in PIN.finditer("\n".join(lines)):
                    dep, ref = m.group(1), m.group(2)
                    if dep not in repos or dep == consumer:
                        continue
                    if not SHA.match(ref):
                        resolved = git(os.path.join(siblings, dep), "rev-parse", "--verify", "-q", f"{ref}^{{commit}}")
                        ref = resolved or ref
                    pins[dep] = ref
        for dep in sorted(ranges.keys() | pins.keys()):
            rng, pin = ranges.get(dep), pins.get(dep)
            dtags = tags_of(os.path.join(siblings, dep))
            rel = tag_at(dtags, pin) if pin else repos[dep]["tag"]
            if rng is None:
                status = "missing-range"
            elif rel is None:
                status = "unreleased-commit"
            elif not in_range(tag_version(rel) or "", rng):
                status = "out-of-range"
            else:
                status = "release"
            edges.append({"consumer": consumer, "dependency": dep, "range": rng, "dev_pin": pin,
                          "dev_pin_release": rel if pin else None, "status": status})
    edges.sort(key=lambda e: (e["consumer"], e["dependency"]))
    return repos, edges, errors


def on_pypi(package: str) -> bool:
    try:
        urllib.request.urlopen(f"https://pypi.org/pypi/{package}/json", timeout=20).close()
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise


def shape(doc: dict) -> list[str]:
    errors: list[str] = []
    for key in ("generated", "repos", "edges", "accepted", "skipped"):
        if key not in doc:
            errors.append(f"register: key {key!r} missing")
    known = set(catalogue())
    for name, rec in doc.get("repos", {}).items():
        if name not in known:
            errors.append(f"{name}: record, but not in CATALOGUE.json")
        if tuple(rec) != REPO_FIELDS:
            errors.append(f"{name}: fields {list(rec)} differ from the contract")
        if rec.get("tag") is not None and tag_version(rec["tag"]) != rec.get("version"):
            errors.append(f"{name}: tag {rec['tag']!r} does not name version {rec.get('version')!r}")
        if (rec.get("tag") is None) != (rec.get("commit") is None):
            errors.append(f"{name}: tag and commit must both be set or both null")
    for e in doc.get("edges", []):
        if tuple(e) != EDGE_FIELDS:
            errors.append(f"edge {e.get('consumer')}->{e.get('dependency')}: fields differ from the contract")
        for end in ("consumer", "dependency"):
            if e.get(end) not in doc.get("repos", {}):
                errors.append(f"edge {e.get('consumer')}->{e.get('dependency')}: {end} has no record")
        if e.get("status") not in STATUSES:
            errors.append(f"edge {e.get('consumer')}->{e.get('dependency')}: status {e.get('status')!r}")
    for name in doc.get("skipped", []):
        if name not in known:
            errors.append(f"skipped {name}: not in CATALOGUE.json")
        if name in doc.get("repos", {}):
            errors.append(f"skipped {name}: also has a record")
    return errors


def diff(doc: dict, repos: dict, edges: list) -> list[str]:
    errors: list[str] = []
    have = doc.get("repos", {})
    for name in sorted(repos.keys() - have.keys()):
        errors.append(f"{name}: in the checkouts, no record in RELEASES.json")
    for name in sorted(have.keys() - repos.keys()):
        errors.append(f"{name}: record in RELEASES.json, no pyproject in the checkouts")
    for name in sorted(repos.keys() & have.keys()):
        for f in [f for f in REPO_FIELDS if f != "pypi"]:
            if repos[name][f] != have[name].get(f):
                errors.append(f"{name}: {f} {have[name].get(f)!r} != {repos[name][f]!r} in the checkout")
    key = lambda e: (e.get("consumer"), e.get("dependency"))
    mine = {key(e): e for e in edges}
    theirs = {key(e): e for e in doc.get("edges", [])}
    for k in sorted(mine.keys() - theirs.keys()):
        errors.append(f"edge {k[0]}->{k[1]}: in the checkouts, not in RELEASES.json")
    for k in sorted(theirs.keys() - mine.keys()):
        errors.append(f"edge {k[0]}->{k[1]}: in RELEASES.json, not in the checkouts")
    for k in sorted(mine.keys() & theirs.keys()):
        for f in EDGE_FIELDS[2:]:
            if mine[k][f] != theirs[k].get(f):
                errors.append(f"edge {k[0]}->{k[1]}: {f} {theirs[k].get(f)!r} != {mine[k][f]!r} in the checkouts")
    return errors


def offenders(doc: dict) -> list[str]:
    out: list[str] = []
    accepted = {(a.get("consumer"), a.get("dependency")): a for a in doc.get("accepted", [])}
    repos = doc.get("repos", {})
    status = {(e["consumer"], e["dependency"]): e.get("status") for e in doc.get("edges", [])}
    for (c, d), a in accepted.items():
        if not a.get("reason"):
            out.append(f"accepted {c}->{d}: no reason")
        if repos.get(d, {}).get("tag") is not None and status.get((c, d)) != "missing-range":
            out.append(f"accepted {c}->{d}: {d} has release {repos[d]['tag']}; accepted is only for a dependency "
                       f"without one, or for a transitive pin (missing-range)")
    for e in doc.get("edges", []):
        if e.get("status") == "release" or (e["consumer"], e["dependency"]) in accepted:
            continue
        out.append(f"{e['consumer']} -> {e['dependency']}: {e['status']} (range {e['range']}, pin "
                   f"{(e['dev_pin'] or 'none')[:12]}{' = ' + e['dev_pin_release'] if e['dev_pin_release'] else ''})")
    return out


def main(argv: list[str]) -> int:
    siblings = argv[argv.index("--siblings") + 1] if "--siblings" in argv else os.environ.get("LOOMGROUND_RELEASES_ROOT")
    write = "--write" in argv
    doc: dict = {"generated": None, "repos": {}, "edges": [], "accepted": [], "skipped": []}
    if os.path.exists(REGISTER):
        with open(REGISTER, encoding="utf-8") as fh:
            doc = json.load(fh)
    if write:
        if not siblings:
            print("--write needs --siblings DIR or LOOMGROUND_RELEASES_ROOT")
            return 2
        repos, edges, errors = derive(siblings, doc.get("skipped", []))
        if errors:
            print("CANNOT WRITE — the checkouts are incomplete:")
            for e in errors:
                print(f"  - {e}")
            return 1
        for rec in repos.values():
            rec["pypi"] = on_pypi(rec["package"]) if rec["package"] else False
        doc = {"generated": datetime.date.today().isoformat(), "repos": repos, "edges": edges,
               "accepted": doc.get("accepted", []), "skipped": doc.get("skipped", [])}
        with open(REGISTER, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"written: {len(repos)} repositories, {len(edges)} edges")
    errors = shape(doc)
    if siblings and not errors:
        repos, edges, derr = derive(siblings, doc.get("skipped", []))
        errors = derr + diff(doc, repos, edges)
    bad = offenders(doc)
    if errors:
        print("STALE — RELEASES.json and the checkouts disagree:" if siblings else "MALFORMED — RELEASES.json:")
        for e in errors:
            print(f"  - {e}")
    if bad:
        print(f"UNRELEASED — {len(bad)} edge(s) are not pinned to a release inside their range:")
        for b in bad:
            print(f"  - {b}")
    if errors or bad:
        return 1
    hist = {s: sum(1 for e in doc["edges"] if e["status"] == s) for s in STATUSES}
    print(f"in sync: {len(doc['repos'])} repositories, {len(doc['edges'])} edges, "
          + ", ".join(f"{v} {k}" for k, v in hist.items() if v) + f", {len(doc['skipped'])} skipped"
          + ("; checkouts agree" if siblings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
