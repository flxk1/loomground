<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# loomground

Normative specification of the Loomground language: grammar, schemas, vocabulary, and conformance vectors for governing when an AI action may take effect.

A patch is a typed policy graph evaluated before release. Each evaluation is recorded, so later alteration is detectable.

## Read

A specification, not a package.

- `spec/SPEC.md` — normative; governs on any conflict.
- `spec/SYNTAX.md` — the textual grammar.
- `llms.txt` — agent and tool entry point (`AGENTS.md` points here).

## Usage

A patch is written as a netlist (`.lg`), one statement per line:

```
actor  bot7
human  alice  role legal
gate   intake  risk low    grant bot7
gate   decide  risk high   grant bot7
reserve automated_decision by legal when risk >= high
cord bot7   -> intake
cord bot7   -> decide
cord intake -> decide      # pipe
cord decide -> master      # egress
```

Its observation (`schema/observation.schema.json`) projects nodes, cords, and reservations; evaluation yields one verdict per gate and an ordered log trace (`docs/patch-views.md`).

## Contracts

| Path | Content |
|---|---|
| `spec/SPEC.md`, `spec/SYNTAX.md` | language, grammar (normative) |
| `spec/OPERATORS.md` | diagnostic-operator contract |
| `grammar/loomground.ebnf` | the grammar, ISO/IEC 14977 |
| `grammar/tree-sitter/` | tree-sitter grammar (`tree-sitter generate`) |
| `schema/` | JSON Schemas: token, patch, observation, transport |
| `vocabulary/` | node classes, cords, verdicts, declarations, guards, grades, grounding (JSON) |
| `conformance/` | 65 vectors + `manifest.json`; reproducing every vector = conformance (§9) |
| `examples/` | sample `.lg` netlists |
| `language-card.json` | the language as data |
| `llms.txt`, `AGENTS.md` | agent entry point, drift-checked |
| `skills/loomground/` | agent procedure generated from the language (`make_skill.py`) |

## Family

Family front door and normative base specification. The repository tree, one line per repository: `CATALOGUE.md`.

- Consumes: nothing. The specification names no implementation; software relates to it by reproducing the vectors in `conformance/`.
- Consumed by: the language planes (`loomground-governance`, `loomground-factual`, `loomground-deontic`, `loomground-epistemic`, `loomground-topos`), the contracts (`loomground-workspace`, `loomground-vertical`, `skill-governance-block`), and the diagnostic operators via `spec/OPERATORS.md`.
- Pipeline: `source → loomground-ingest → loomground-versum → loomground-solver → applied or diagnostic planes`; every stage grounds in this language.

Rationale: `docs/design.md`.

## Status

Specification v0.11.0 (stable); tag `v0.11.0`. 65 conformance vectors, each reproduced by two independent implementations (`conformance/README.md`). Packaged by `loomground-governance`, pinned to this tag, byte-equality proven in its CI. CI: 6 jobs (`.github/workflows/ci.yml`). Tooling: Python 3 standard library.

## License

Apache-2.0 — `LICENSES/Apache-2.0.txt`; per-file SPDX headers, `REUSE.toml` for files that carry none. Provenance: `docs/provenance.md`.
