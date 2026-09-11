<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Changelog

## Unreleased

- `RELEASES.json`: release/pin register over the family (version, tag, commit, package, index presence per repository; range, dev pin, status per dependency edge), derived from the sibling checkouts by `tools/check_releases.py`; `releases` CI job clones every public repository at its pushed main and fails on a stale register or a pin that is not a release inside its range.

- Standard synced to 0.11.0 from loomground-governance `standard/`: declarations reversibility, uncertainty, mandate, transfer; grade ladder default L0–L6; host-observed `kind` with fail-closed floor; 18 new conformance vectors incl. `grounder/`; schemas, grammar, tree-sitter, vocabulary (roles, reversibility, uncertainty), language card and llms.txt updated. Skill regenerated with mandate and transfer guidance; lockstep probes added.

- README to canon; `CATALOGUE.md` (family tree); `spec/OPERATORS.md` (diagnostic-operator
  contract); rationale, patch views, and provenance moved verbatim to `docs/`. No language change.
- Repository layout: `check_llms_txt.py` → `tools/`, `lockstep_meta_test.py` →
  `tests/`, `skill/` → `skills/loomground/`; bare `LICENSE` dropped in favour of
  `LICENSES/Apache-2.0.txt` + `REUSE.toml`. No language change.
