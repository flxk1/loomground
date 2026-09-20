# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""A `name @ <url>` dependency declares no version range, and the tool must not read the URL as one.

Reading it as a range marked every sibling edge out-of-range once the family moved its
declarations from version specifiers to git refs, which is the whole reason this file exists.
"""
import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location(
    "cr", pathlib.Path(__file__).resolve().parents[1] / "tools" / "check_releases.py")
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)


def rest(dep: str) -> str:
    m = cr.REQ.match(dep)
    assert m, dep
    return (m.group(3) or "").strip()


def test_a_direct_reference_is_recognised_by_its_leading_at():
    assert rest("a2a-compliance @ git+https://github.com/flxk1/a2a-compliance@v0.4.0").startswith("@")


def test_a_version_specifier_is_not_mistaken_for_one():
    assert rest("mcp>=2,<3") == ">=2,<3"
    assert not rest("mcp>=2,<3").startswith("@")


def test_the_url_never_reaches_the_range_comparison():
    url = rest("loomground-deontic @ git+https://github.com/flxk1/loomground-deontic@loomground-deontic-v0.2.1")
    assert not cr.in_range("0.2.1", url), "a URL read as a range puts every pinned sibling out of range"
