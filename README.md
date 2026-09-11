<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# loomground

Normative specification of the Loomground language: grammar, schemas, vocabulary, and conformance vectors for governing when an AI action may take effect.

## Problem

Every governance tool defines "policy", "gate" and "verdict" its own way; nothing is comparable or checkable. One normative language with vectors; a tool conforms or it does not.

## Read

Install nothing.

- `spec/SPEC.md` — normative; governs on any conflict.
- `spec/SYNTAX.md` — the textual grammar.
- `llms.txt` — agent entry point.

## Usage

A patch is a netlist (`.lg`), one statement per line (`examples/`); evaluation yields one verdict per gate and an ordered log (`docs/patch-views.md`). The whole path, documents in, verified proof out: `examples/end-to-end/`.

## Example

```
in : policy.lg — gate transfer risk high grant agent · reserve data_transfer by legal when risk >= high
     token {kind: data_transfer, risk: high, provenance: [span]} proposed by agent at transfer
out: results {'transfer': {'verdict': 'reserved', 'master': 'withhold'}}
     log [{'gate': 'transfer', 'verdict': 'reserved'}]
```

## Language

A `.lg` file states which actors may activate which gates at which risk, which action kinds a human role decides or are prohibited, and what reaches the master (egress). Forms: `actor` `human` `gate` `cord` `reserve` `prohibit` `obligation` `redress` `transfer`.

```
actor  bot7  grade L2                                  agent, granted grade L2
human  alice  role dpo                                 person, addressed by role
gate   decide  risk high  grant bot7                   bot7 at decide; floor high
reserve automated_decision by dpo when risk >= high    high risk: dpo decides, reserved
prohibit biometric_categorisation                      prohibited, whatever the grant
cord   decide -> master                                egress; released on auto only
```

Verdicts: `auto < human < refused < reserved < prohibited`. Full card: `docs/language-card.md`.

## Contracts

| Path | Content |
|---|---|
| `spec/`, `grammar/` | `SPEC.md` (normative), `SYNTAX.md`, `loomground.ebnf`, `tree-sitter/`; `OPERATORS.md` (operator contract) |
| `schema/`, `vocabulary/` | token, patch, observation, transport; nodes, cords, verdicts, declarations, guards, grades, grounding |
| `conformance/` | 65 vectors, `manifest.json`; conformance = all reproduced (§9) |
| `language-card.json`, `llms.txt`, `AGENTS.md`, `skills/loomground/` | the language as data; agent entry point and procedure, drift-checked |

## Family

Front door and normative base; tree: `CATALOGUE.md`, data: `CATALOGUE.json`. Each repository stands alone; install only the line you need. Three doors:

- Ground documents: `loomground-versum`.
- Write a policy: `spec/SPEC.md`, validated by `loomground-governance`.
- Reason over facts and rules: `loomground-solver`.

Consumes nothing; software conforms by reproducing `conformance/`. Pipeline: `source → loomground-ingest → loomground-versum → loomground-solver → applied or diagnostic planes`; every stage grounds in this language.

Rationale: `docs/design.md`.

## Status

Specification v0.11.0 (stable), tagged. 65 conformance vectors, each reproduced by two independent implementations (`conformance/README.md`). Packaged by `loomground-governance`, pinned to this tag. CI: 7 jobs. Tooling: Python 3 standard library.

## License

Apache-2.0 (`LICENSES/Apache-2.0.txt`); SPDX headers per file, `REUSE.toml` for the rest. Provenance: `docs/provenance.md`.
