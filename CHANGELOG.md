<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Changelog

## 0.11.1 (2026-09-26)

- Conformance: four vectors for situations the suite did not compose — an invalid token inside a transport (`transport-invalid-token`, `transport-invalid-token-only`), authority at a downstream gate (`pipe-authority-downstream`), a gate with two pipe successors (`pipe-fanout`); 65 → 69 vectors. The transport schema admits `invalid: true` on an activation whose token deliberately fails token validation (it denotes ⊥); every other token keeps the strict token schema. No language change.

## Unreleased

- `RELEASES.json`: release/pin register over the family (version, tag, commit, package, index presence per repository; range, dev pin, status per dependency edge), derived from the sibling checkouts by `tools/check_releases.py`; `releases` CI job clones every public repository at its pushed main and fails on a stale register or a pin that is not a release inside its range.

- Standard synced to 0.11.0 from loomground-governance `standard/`: declarations reversibility, uncertainty, mandate, transfer; grade ladder default L0–L6; host-observed `kind` with fail-closed floor; 18 new conformance vectors incl. `grounder/`; schemas, grammar, tree-sitter, vocabulary (roles, reversibility, uncertainty), language card and llms.txt updated. Skill regenerated with mandate and transfer guidance; lockstep probes added.

- README to canon; `CATALOGUE.md` (family tree); `spec/OPERATORS.md` (diagnostic-operator
  contract); rationale, patch views, and provenance moved verbatim to `docs/`. No language change.
- Repository layout: `check_llms_txt.py` → `tools/`, `lockstep_meta_test.py` →
  `tests/`, `skill/` → `skills/loomground/`; bare `LICENSE` dropped in favour of
  `LICENSES/Apache-2.0.txt` + `REUSE.toml`. No language change.
