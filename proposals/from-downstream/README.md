<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Proposals for the Loomground standard (hand-off)

These drafts close a coverage gap found while checking a downstream implementation:
the suite pins 7 of the 9 declared declarations but **not
`quorum` or `temporal`** — so an implementation can pass every vector while leaving both
features unwired. See [`../quorum-temporal-concept.md`](../quorum-temporal-concept.md).

## The durable fix: `lockstep_meta_test.py`

The two missing vectors are symptoms; the root cause is that nothing asserts a feature
reaches all four of Loomground's representations (grammar → parser → projection+schema →
vector). [`lockstep_meta_test.py`](lockstep_meta_test.py) is a proposed CI gate that does,
in three stdlib checks (declaration→vector, schema-field→vector, grammar-keyword→vector).
Run it against the live tree today and it reports **7 gaps** — `quorum`, `temporal`, and
(a bonus the manual audit missed) the untested `name` clause, plus the keyword-level detail
that quorum has two syntaxes (`and` / `of {`) and temporal two modes (`halt` / `proceed`).
Landing the two vectors below drops it to a 3-item punch-list (`and`, `name`, `proceed`).
This one gate would have caught `temporal`, `quorum`, and the grant-clause→cord lag fixed
earlier — it is the standard-side parity check for every implementation.

## The schema change

[`schema-change-temporal.md`](schema-change-temporal.md) — the precise, additive edit to
`observation.schema.json` + `project()` so the observation carries `duration`/`on_elapse`
(today they are parsed then dropped, and the schema forbids them — while `redress.within`,
the identical concept, is projected correctly). Required before `reserve-temporal` can pass.

## `vectors/reserve-quorum`  — ready to land as-is
Pins that `reserve K by 2 of { … }` projects its quorum target verbatim on `by` and
produces `reserved`. **Validated against the current engine** (`project()` already emits
`by: "2 of {legal, finance}"`). The m-of-n *distinctness* is an implementation duty
(the host's approval layer), not a language verdict — the language fixes the target.

## `vectors/reserve-temporal`  — needs one schema change first
The engine parses `duration <d> : halt|proceed` but `project()` **drops** them, so they are
unobservable today. To pin temporal, extend the observation's reservation form:

```
reservations[]:  { kind, by, when?, duration?, on_elapse? }     # add duration, on_elapse
```

and have `project()` carry them through (they are already on the parsed reservation). The
`expected.json` here is written to that **target** form, so it will fail until the schema +
projection land — by design. `on_elapse ∈ { halt, proceed }`; `halt` is the safe default
(deny on elapse = timeout-is-deny), `proceed` is fail-open and should be rejected at apply
on a reserved-by-law kind; the standard may choose to pin that guardrail too.

## After landing
Implementations should run the quorum vector through their normal conformance gate. The
language↔enforcement handoff that a vector *cannot* see — that a quorum reservation routes
to two distinct approvers, and that a duration denies or proceeds on elapse — belongs in
the consuming host's integration tests.
