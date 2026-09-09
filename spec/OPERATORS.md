<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Diagnostic-operator contract

Common contract of the six diagnostic operators: brief, collapse, escalation, falsifiability, mandate, proxy.

- Input: solver output — a decomposition, trajectory, evidence set, or measurement, with its grounding references.
- Output: a verdict and an attribution naming the input terms that determined it.
- Fail-closed: a missing, unmeasured, or unattributable input yields the most restrictive verdict; an unmeasured term is reported as unmeasured, distinct from a measured floor.
- Resolves nothing: an operator reports; it alters no input, releases no action, and settles no unresolved material.
- Deterministic: equal inputs yield equal verdict and attribution.

Each operator states its defining question and public definition in its own repository.
