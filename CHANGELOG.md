<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Changelog

## Unreleased

- `docs/pitch/`: the project pitch as a seven-card carousel (`loomground-pitch.pdf`, the seven cards, `pitch.md`, `alt.txt`), CC BY 4.0.

## 0.11.4 (2026-10-20)

- Conformance: `guard-risk-above-threshold` runs a `critical` token against a
  `risk >= high` reservation. Every earlier run against a `>=` risk guard sat at
  the threshold value, where `>=` and `=` coincide, so an evaluator reading the
  guard as an equality passed all 75; found by a semantic-mutant battery in
  loomground-ref. 76 vectors.
- `spec/SPEC.md` §11 cites ISO/IEC 22989 for levels of automation: its Table 1
  (clause 5.13) gives seven levels and reserves autonomy for level 6, so the
  glossary no longer credits it with a level-of-autonomy concept.
  `vocabulary/grounding.json` follows.
- The construct is called a grade wherever the prose names it: the spec text and
  glossary, the schema descriptions, the reject-reason meaning, the grounding map,
  the guard-domain note, `llms.txt`, the language card and the skill. The keyword
  `grade` and the identifier `autonomy-grade` are unchanged.
- `CATALOGUE.json` lists `versum_select`, and `RELEASES.json` registers
  governance 0.12.1 and the deontic floor of the tool server.

## 0.11.3 (2026-10-11)

- Citations of external works in `spec/SPEC.md` corrected against the
  sources. The W3C Process criterion is independent interoperable
  implementations (§6.3.2, 18 August 2025 edition) and states no number of
  implementations. RFC 6962 is marked as obsoleted by RFC 9162. AI Act
  Art. 3(4) is cited as the definition of deployer. The `prohibited`
  grounding names the XACML deny-overrides combining algorithm (App. C.2), and
  the `refused` grounding names `NotApplicable` or `Indeterminate` denied by a
  deny-biased PEP (§7.2.2); `vocabulary/grounding.json` follows. No language
  semantics change.
- Grounder support gold 0.2.1: g01 quotes the Official Journal masthead and
  AI Act Art. 113 in place of a secondary text; g29 quotes Art. 16(f); g07 and
  g23 end as Art. 113 does; g14 marks its second elision; g36 quotes GDPR
  Art. 37(1)(a) in full. Labels and the label distribution are unchanged.
- The `loomground-plugins` catalogue record and the assistant instructions
  file describe hosts by function rather than by product name.

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
