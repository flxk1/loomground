<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Design notes

Paragraphs moved verbatim from `README.md` (README canon, 2026-09). The normative source is `spec/SPEC.md`.

## Scope

This repository contains the language specification: grammar, schemas,
vocabulary, and conformance vectors. It describes *what* governance applies; it
does not define execution, scheduling, storage, or communication. The
specification references no host program.

## Specification, not a package

Loomground is a **specification, not a package** — there is nothing to install
and nothing to import. Read it, or consume its machine-readable forms directly:

- Read `spec/SPEC.md` (the normative specification) and `spec/SYNTAX.md` (the grammar).
- Tools and agents start from `llms.txt` / `AGENTS.md` and `language-card.json` —
  a compact, agent-facing summary of the whole language.

Conformance, not installation, is how software relates to this repo: an
implementation *conforms* by reproducing the vectors in `conformance/` (see
[Status](#status)).

## Machine-readable surface

The normative content is also available as data, so tools and agents consume the
language without parsing prose:

- `grammar/loomground.ebnf` — the textual grammar, standalone (ISO/IEC 14977).
- `grammar/tree-sitter/` — a tree-sitter grammar. `tree-sitter generate` builds
  the parser, AST, and editor tooling. Verified against every `.lg` in the repo.
- `schema/` — JSON Schemas for the `token`, the `patch` (a policy graph as data),
  the `observation` (a vector's `expected.json`), and transport runs. Validated
  against the vectors.
- `vocabulary/` — node classes, cords, the verdict lattice, declarations, the guard
  domain, risk levels, and the grounding map, each as JSON.
- `conformance/manifest.json` — a machine index of every vector.
- `language-card.json` — a compact, agent-facing summary of the whole language.
- `llms.txt` / `AGENTS.md` — the agent/tool entry point: a compact guide to
  reading, emitting, and validating Loomground, kept in sync by a drift check.
- `skills/loomground/` — an agent procedure for drafting, classifying, and validating
  patches. Its factual sections are *generated* from the vocabulary, schemas,
  and vectors (`skills/loomground/make_skill.py`, CI-checked), so the skill grows with the
  language and its examples are conformance-tested by construction.

## Family — dependency direction

Loomground is the **language at the base of the knowledge plane** — the *what*
that everything downstream grounds in. Dependencies point one way, toward this
base: implementations and planes depend on the language; the language depends on
nothing and names no implementation.

- **Conforms to it** — software relates to this repo by *conforming*, never by
  being named in it: an implementation reproduces the vectors in `conformance/`,
  and §9 requires two independent implementations to reproduce every vector. The
  specification privileges none of them — naming a reference implementation here
  would break the neutrality the standard is built on.
- **Builds on it** — the knowledge-plane substrate realizes the language's
  declarations and grounding map:
  [loomground-governance](https://github.com/flxk1/loomground-governance) (when an
  action may take effect), [loomground-epistemic](https://github.com/flxk1/loomground-epistemic)
  and [loomground-factual](https://github.com/flxk1/loomground-factual) (the modal
  and assertoric planes).
- **Pipeline it feeds** — Language →
  [ingest](https://github.com/flxk1/loomground-ingest) →
  [versum](https://github.com/flxk1/loomground-versum) →
  [solver](https://github.com/flxk1/loomground-solver) →
  [patchbay](https://github.com/flxk1/loomground-patchbay).
- **Consumed from outside, never depended on backward** — downstream governance
  and orchestration layers consume the grounding this language provides; nothing
  here points back at them, and this prose names none of them by product. (See
  `repo-standards/topology.md` for the full three-plane map and the arrow rules.)

This list is a map, not a manifest — representative members, not exhaustive.

## Licensing

Everything in this repository — the specification, grammars, vocabulary,
schemas, conformance vectors, examples, and tooling — is licensed under the
Apache License, Version 2.0. See `LICENSES/Apache-2.0.txt`.

Per-file SPDX headers throughout; `REUSE.toml` covers files that cannot carry one.
The tree is REUSE-compliant (checked in CI).

## Status (v0.8 cycle)

Pre-1.0, specification v0.8 (draft); latest release v0.7.0. This repository carries only the language:
specification, grammar, schemas, vocabulary, and conformance vectors. Reference
implementations are out of scope. An implementation conforms by reproducing the
vectors in `conformance/`; §9 requires two independent implementations to
reproduce every vector, a criterion v0.7 meets (see `conformance/README.md`,
Status).
