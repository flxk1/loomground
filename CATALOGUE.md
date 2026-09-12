<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Catalogue

Which line: `examples/end-to-end/` runs the whole path; `loomground-versum` grounds documents, `loomground-solver` reasons over them.

```
Loomground
├── Standard
│   ├── loomground                 — family front door and normative base specification
│   ├── loomground-governance      — installable governance-language plane and conformance distribution (lockstep copy of the standard, own release axis)
│   ├── language planes
│   │   ├── loomground-factual     — assertoric base language; the fact representation consumed by modal planes
│   │   ├── loomground-deontic     — deontic language and algebra; language separate from inference
│   │   ├── loomground-epistemic   — epistemic language plane; depends on loomground-factual
│   │   └── loomground-topos       — legal-system topology language (authority, hierarchy, competence, inter-system relations); experimental
│   ├── contracts
│   │   ├── loomground-workspace   — workspace identity and boundary contract
│   │   ├── loomground-vertical    — domain-registration contract: vocabulary, jurisdiction pack, requirements house
│   │   └── skill-governance-block — vendor-neutral skill-manifest binding; external contract
│   └── reference implementation
│       └── loomground-ref         — independent reference implementation
├── Evidence pipeline
│   ├── loomground-ingest          — deterministic normalization and evidence packaging
│   ├── loomground-versum          — span-grounded knowledge and evidence plane; the single persistent knowledge layer
│   └── loomground-solver          — shared reasoning kernel
├── Applied reasoning
│   ├── loomground-norm            — general normative-reasoning plane
│   ├── loomground-legal           — legal domain plane; experimental
│   └── policy-compiler            — compiles written policy into deontic norms, surfacing conflicts, undetermined rules, and residual spans
├── Diagnostic operators           (contract: spec/OPERATORS.md)
│   ├── loomground-brief           — selects the minimum unresolved material required for human review
│   ├── loomground-collapse        — identifies the limiting term in a fail-closed conjunction
│   ├── loomground-escalation      — computes the autonomy ceiling imposed by multiple governance factors
│   ├── loomground-falsifiability  — ranks oversight evidence by independent falsifiability
│   ├── loomground-mandate         — compares an observed trajectory with its declared mandate
│   └── loomground-proxy           — tests whether a proxy measurement still represents its declared target
├── Assurance artifacts
│   ├── governance-certification   — family index: predicate type, required pillars, verifier
│   ├── 5d-nd                      — grounding-reference resolver (pillar: grounding)
│   ├── oversight-certificate      — certificate fields, issue and verify operations (pillar: oversight)
│   ├── enforcement-posture        — posture, evidence window, comparison, coverage (pillar: enforcement state)
│   ├── effect-reconciliation      — the three reported mismatches (pillar: observed effects)
│   ├── norm-freshness             — RulePin, observed source state, freshness verdict (pillar: source validity)
│   ├── obligation-discharge       — may a permit proceed; were attached duties discharged (pillar: attached duties)
│   ├── loomground-audit-chain     — append-only, hash-chained, Ed25519-signed event log with chain verification (pillar: intact)
│   ├── oversight-ladder           — human-oversight obligations keyed to the L0-L6 autonomy ladder (pillar: oversight obligation)
│   └── evidence-emitter           — composes the installed assurance components into one signed, offline-verifiable evidence package
├── Runtime controls               — decide-at-tempo primitives a governance runtime enforces with: locks, lanes, drift, erasure, privacy and fleet control. Each is optional to its consumer and stands alone
│   ├── loomground-lock            — egress and ingress locks, capability tokens, at-rest seal of a folder's memory
│   ├── loomground-lane            — durable approval envelopes (actions, data, connectors, folder, policy) per graded agent
│   ├── loomground-drift           — leased autonomy, tripwires, quarantine; drift against a recorded baseline
│   ├── loomground-erasure         — controller-signed erasure sweeps, pending-erase markers, forgotten-subjects ledger
│   ├── privacy-shield             — local PII/PHI detection, clean overlays, and egress control
│   └── a2a-compliance             — A2A maker control with role authority and optional Loomground grounding
├── Interfaces and authoring
│   ├── loomground-plugins         — multi-host skill catalogue and package builder
│   ├── loomground-patchbay        — reusable presentation contract and console shell
│   └── loomground-mcp             — one MCP server exposing the planes as tools and the skills as prompts
└── Domain agents                  — private; place reserved
```

Pipeline: `source → loomground-ingest → loomground-versum → loomground-solver → applied or diagnostic planes`
