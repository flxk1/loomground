<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright 2026 flxk1 -->
# Loomground

A declarative language for governing when an AI system or agent action may take
effect. A patch is a typed policy graph evaluated before release; each evaluation
is recorded so later alteration is detectable.

This repository contains the language specification: grammar, schemas,
vocabulary, and conformance vectors. It describes *what* governance applies; it
does not define execution, scheduling, storage, or communication. The
specification references no host program.

## Patch and Observation

A Loomground patch has an authored surface and a canonical projection:

- **Netlist** — the authored, diffable text form (`spec/SYNTAX.md`, `examples/`).
- **Observation** — the machine-checkable projection: graph and reservation data
  (`schema/observation.schema.json`). Prohibitions and obligations act during
  evaluation and are not projected. Evaluation also produces an ordered log trace;
  that runtime record is not a patch view.

## Read the specification

- `spec/SPEC.md` — the normative specification (nodes, cords, the token, evaluation,
  the governance declarations, conformance).
- `spec/SYNTAX.md` — the concrete textual grammar.
- `conformance/` — the vectors that define a conforming implementation.
- `examples/` — sample patches (`.loom` netlists).

## Machine-readable

The normative content is also available as data, so tools and agents consume the
language without parsing prose:

- `grammar/loomground.ebnf` — the textual grammar, standalone (ISO/IEC 14977).
- `grammar/tree-sitter/` — a tree-sitter grammar. `tree-sitter generate` builds
  the parser, AST, and editor tooling. Verified against every `.loom` in the repo.
- `schema/` — JSON Schemas for the `token`, the `patch` (a policy graph as data),
  the `observation` (a vector's `expected.json`), and transport runs. Validated
  against the vectors.
- `vocabulary/` — node classes, cords, the verdict lattice, declarations, the guard
  domain, risk levels, and the grounding map, each as JSON.
- `conformance/manifest.json` — a machine index of every vector.
- `language-card.json` — a compact, agent-facing summary of the whole language.
- `llms.txt` / `AGENTS.md` — the agent/tool entry point: a compact guide to
  reading, emitting, and validating Loomground, kept in sync by a drift check.

## Layout

```
llms.txt      agent/tool entry point (AGENTS.md points here)
spec/         SPEC.md (the language), SYNTAX.md (grammar)
grammar/      loomground.ebnf + tree-sitter/
schema/       JSON Schemas (token, patch, observation, transport)
vocabulary/   node classes, cords, verdicts, declarations, guards, grounding (JSON)
conformance/  vectors that define a conforming implementation + manifest.json
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

Pre-1.0, specification v0.6. This repository carries only the language:
specification, grammar, schemas, vocabulary, and conformance vectors. Reference
implementations are out of scope. An implementation conforms by reproducing the
vectors in `conformance/`; §9 requires two independent implementations to
reproduce every vector.

## Provenance

This specification and its supporting materials were drafted with AI assistance
(Claude, Anthropic) under human direction. The human author makes the design
decisions and is responsible for the content; the AI was used as a drafting and
review tool. This assistance is acknowledged here and in `NOTICE`; it is not
recorded as authorship — the commits do not credit AI tools as authors or
co-authors.
