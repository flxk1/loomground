<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Changelog

## 0.11.2 (2026-10-09)

- Spec consistency: the guard domain in `spec/SPEC.md` §6 stated four fields
  in three places (`{kind, risk, party, tags}`) where the grammar, `spec/SYNTAX.md`,
  `vocabulary/guard-domain.json`, and five conformance vectors already use six
  (`{kind, risk, reversibility, uncertainty, party, tags}`); SPEC.md now states
  six everywhere. `spec/SPEC.md` and `spec/SYNTAX.md` version headers, which
  read "Version 0.8 (draft)", now match the manifest release. `conformance/README.md`'s
  Status section described an implementation "bundled elsewhere in this
  repository" (a `standard/` directory, a companion-skill "checker") that this
  repository does not contain; rewritten to state what the repository
  actually carries. Every claim that the two existing evaluators are
  "independent" (`CATALOGUE.md`, `CATALOGUE.json`, `proposals/v0.8-punch-list.md`)
  is corrected to state the §9 independence criterion as open, matching
  `conformance/README.md`, which already stated it correctly.
- Normative log order: SPEC §7.4 now fixes the tie-break where pipes admit
  more than one topological order — declaration order — as the rule both
  existing evaluators already implement; §7.5 extends determinism to
  evaluation order (byte-identical log traces across conforming
  implementations) and states three rules: repeated runs yield identical
  observations; a semantics-preserving reordering of declarations yields the
  same per-gate verdicts and master decision; the log is the same under
  reordering only where the pipes admit a single topological order, and
  otherwise follows the §7.4 tie-break for the new declaration order.
  `spec/SYNTAX.md` §2 now says the same: verdicts and decisions are
  order-independent, log order among topological ties is not.
- Vector-format contract, documented in `conformance/README.md` and
  `schema/transport.schema.json`: every negative vector's `reject.json` now
  carries a `reason` from the closed set in the new `vocabulary/reject-reasons.json`,
  alongside `stage`; a parse-time rejection is a correct outcome only for a
  vector declaring `stage: parse`; comparison is of the whole observation
  object, not named keys; a new `determinism` vector kind (`repeat`,
  `permutations` in `transport.json`, each permutation a `{file, log}` entry)
  has a runner execute repeats and declaration-order permutations itself,
  checking verdicts and decisions against one `expected` and each
  permutation's log against its own `log`; a log
  entry MAY carry `token` and `observed`, pinning SPEC §7.4's declared-vs-observed
  record requirement where a vector exercises it.
- Conformance: six vectors for situations the suite did not compose —
  `topo-fanout-fanin-declared-order` / `-variant` (a second fan-out/fan-in
  topology that genuinely admits two topological orders, with the expected
  log fixed by declaration order and differing between the pair);
  `determinism-repeat-permute` (the new determinism kind, no topological tie);
  `determinism-topo-tie` (a determinism vector over a graph with a three-way
  topological tie: verdicts and decision invariant under three permutations,
  each permutation's log fixed by the §7.4 tie-break for its declaration order);
  `prohibit-grade-reservation-precedence` (a prohibition, a high grade, and a
  same-kind reservation on one gate, prohibition wins); `record-declared-and-observed`
  (a declared-vs-observed risk divergence, pinning both in the log entry);
  69 → 75 vectors. All 31 existing negative vectors gained a `reason`.

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
