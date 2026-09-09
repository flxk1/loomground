<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Patch views — netlist and observation

Moved verbatim from `README.md` (Usage). The normative source is `spec/SPEC.md`; the observation schema is `schema/observation.schema.json`.

A Loomground patch has an authored surface and a canonical projection:

- **Netlist** — the authored, diffable text form (`spec/SYNTAX.md`, `examples/`).
  Files end in `.lg`. (`.loom`, the pre-v0.6 name, was replaced at v0.6.0; its
  one-minor-version deprecation window has closed, and a v0.7 reader need not
  accept it.)
- **Observation** — the machine-checkable projection: graph and reservation data
  (`schema/observation.schema.json`). Prohibitions and obligations act during
  evaluation and are not projected. Evaluation also produces an ordered log trace;
  that runtime record is not a patch view.

To read the language in full:

- `spec/SPEC.md` — the normative specification (nodes, cords, the token, evaluation,
  the governance declarations, conformance).
- `spec/SYNTAX.md` — the concrete textual grammar.
- `conformance/` — the vectors that define a conforming implementation.
- `examples/` — sample patches (`.lg` netlists).
