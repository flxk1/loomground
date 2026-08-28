<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Loomground

A declarative language for governing when an AI system or agent action may take
effect. A patch is a typed policy graph evaluated before release; each evaluation
is recorded so later alteration is detectable.

This repository contains the language specification: grammar, schemas,
vocabulary, and conformance vectors. It describes *what* governance applies; it
does not define execution, scheduling, storage, or communication. The
specification references no host program.

## Install

Loomground is a **specification, not a package** — there is nothing to install
and nothing to import. Read it, or consume its machine-readable forms directly:

- Read `spec/SPEC.md` (the normative specification) and `spec/SYNTAX.md` (the grammar).
- Tools and agents start from `llms.txt` / `AGENTS.md` and `language-card.json` —
  a compact, agent-facing summary of the whole language.

Conformance, not installation, is how software relates to this repo: an
implementation *conforms* by reproducing the vectors in `conformance/` (see
[Status](#status)).

## Usage

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

## API / Contracts

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
- `skill/` — an agent procedure for drafting, classifying, and validating
  patches. Its factual sections are *generated* from the vocabulary, schemas,
  and vectors (`skill/make_skill.py`, CI-checked), so the skill grows with the
  language and its examples are conformance-tested by construction.

```
llms.txt      agent/tool entry point (AGENTS.md points here)
spec/         SPEC.md (the language), SYNTAX.md (grammar)
grammar/      loomground.ebnf + tree-sitter/
schema/       JSON Schemas (token, patch, observation, transport)
vocabulary/   node classes, cords, verdicts, declarations, guards, grounding (JSON)
conformance/  vectors that define a conforming implementation + manifest.json
examples/     sample patches (.lg netlists)
skill/        agent procedure (SKILL.md, generated from the language)
language-card.json   agent-facing summary
```

## Family

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

## License

Everything in this repository — the specification, grammars, vocabulary,
schemas, conformance vectors, examples, and tooling — is licensed under the
Apache License, Version 2.0. See `LICENSE`.

Per-file SPDX headers throughout; `REUSE.toml` covers files that cannot carry one.
The tree is REUSE-compliant (checked in CI).

## Status

Pre-1.0, specification v0.8 (draft); latest release v0.7.0. This repository carries only the language:
specification, grammar, schemas, vocabulary, and conformance vectors. Reference
implementations are out of scope. An implementation conforms by reproducing the
vectors in `conformance/`; §9 requires two independent implementations to
reproduce every vector, a criterion v0.7 meets (see `conformance/README.md`,
Status).

## Provenance

This specification and its supporting materials were drafted with AI assistance
under human direction. The human author makes the design
decisions and is responsible for the content; AI was used as a drafting and
review tool. This assistance is acknowledged here and in `NOTICE` (which names
the tools used); it is not
recorded as authorship. An assisted commit ends with a plain assisted line
naming the tool, never an authorship or co-authorship trailer (see
`CONTRIBUTING.md`; enforced in CI). The language itself is tool- and
vendor-neutral: no normative document depends on or references any model,
vendor, or agent framework.
