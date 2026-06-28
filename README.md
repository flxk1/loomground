<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright 2026 flxk1 -->
# Loomground

A **declarative language for the governance of AI systems and AI agents**. A patch
is a typed policy graph evaluated before an action takes effect and recorded so
later alteration is detectable.

This repository is the **language specification**: a grammar, schemas, and the
conformance vectors that define a valid implementation. It describes *what*
governance applies; it defines no execution, scheduling, storage, or communication;
those are outside this specification. The specification depends on nothing outside
itself, and references no other system.

## Two surfaces

A Loomground patch has two textual surfaces (the observation is a *projection*, lossy by design — not an equivalent view):

- **Netlist** — the authored, human-writable, diffable text form (`spec/SYNTAX.md`, `examples/`).
- **Observation** — its canonical projection: the graph and reservations as a machine-checkable form (`schema/observation.schema.json`); prohibitions and obligations act at evaluation and are not projected. (Evaluation additionally produces a tamper-evident log — the runtime record, not a view of the patch.)

## Read the specification

- `spec/SPEC.md` — the normative specification (nodes, cords, the token, evaluation,
  the governance declarations, conformance).
- `spec/SYNTAX.md` — the concrete textual grammar.
- `conformance/` — the vectors that **define** a conforming implementation.
- `examples/` — sample patches (`.loom` netlists).

## Machine-readable

The normative content is also available as data, so tools and agents consume the
language without parsing prose:

- `grammar/loomground.ebnf` — the textual grammar, standalone (ISO/IEC 14977).
- `grammar/tree-sitter/` — a **generatable** grammar: `tree-sitter generate` yields
  a parser, an AST, and editor tooling. Verified against every `.loom` in the repo.
- `schema/` — JSON Schemas for the `token`, the `patch` (a policy graph as data),
  the `observation` (a vector's `expected.json`), and transport runs. Validated
  against the vectors.
- `vocabulary/` — node classes, cords, the verdict lattice, declarations, the guard
  domain, risk levels, and the grounding map, each as JSON.
- `conformance/manifest.json` — a machine index of every vector.
- `language-card.json` — a compact, agent-facing summary of the whole language.
- `llms.txt` / `AGENTS.md` — the entry point for an agent or tool: a self-contained
  guide to reading, emitting, and validating Loomground (kept in sync with the
  language by a test).

## Layout

```
llms.txt      agent/tool entry point (AGENTS.md points here)
spec/         SPEC.md (the language), SYNTAX.md (grammar)
grammar/      loomground.ebnf + tree-sitter/ (generatable grammar)
schema/       JSON Schemas (token, patch, observation, transport)
vocabulary/   node classes, cords, verdicts, declarations, guards, grounding (JSON)
conformance/  vectors that DEFINE a conforming implementation + manifest.json
examples/     sample patches (.loom netlists)
language-card.json   agent-facing summary
```

## Licensing (split)

- **Spec, the EBNF grammar, and vocabulary** (`spec/`, `grammar/loomground.ebnf`,
  `vocabulary/`, `language-card.json`): CC-BY-4.0 — see `LICENSE-SPEC`.
- **Schemas, vectors, examples, the tree-sitter grammar, tooling** (`schema/`,
  `conformance/`, `examples/`, `grammar/tree-sitter/`, CI): Apache-2.0 — see `LICENSE-CODE`.

Per-file SPDX headers throughout; `REUSE.toml` covers files that cannot carry one.
The tree is REUSE-compliant (checked in CI).

## Status

Pre-1.0, specification v0.6. This repository carries the language specification
only — spec, grammar, schemas, vocabulary, and conformance vectors. Reference
implementations are out of scope here: an implementation conforms by reproducing
the vectors in `conformance/`. Conformance (§9) requires two implementations,
neither derived from the other, to reproduce every vector. The specification is
machine-readable (grammar, schemas, and vocabulary as data).

## Provenance

This specification and its supporting materials were drafted with AI assistance
(Claude, Anthropic) under human direction. The human author makes the design
decisions and is responsible for the content; the AI was used as a drafting and
review tool. This assistance is acknowledged here and in `NOTICE`; it is not
recorded as authorship — the commits do not credit AI tools as authors or
co-authors.
