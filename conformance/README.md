<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 The Loomground Authors -->
# Loomground conformance vectors

These vectors **define** what it means to be a conforming Loomground
implementation. They are language-side data: an implementation conforms if and
only if it reproduces every vector (see the specification, Conformance). The
vectors name no implementation and assume none — any implementer supplies their
own runner.

## The observation schema (v0.6)

A patch vector's `expected.json` records the **observation** of a policy graph:

- `nodes` — `{id, class}` for each node (`class` ∈ `actor` | `human` | `gate` |
  `master`); a `human` carries its `role`, a `gate` its `risk_floor` and, if declared,
  its `grade_required` (a graded gate is a source gate); an `actor` carries its `grade`
  (the granted autonomy grade) if declared. Listed in declaration order, the master last.
- `cords` — `{from, to, type}` (`type` ∈ `authority` | `pipe` | `egress`), in
  declaration order.
- `reservations` — the graph-level reservation declarations
  `{kind, by[, when][, duration, on_elapse]}`. In v0.6 a reservation keys on the
  token's `kind`; it is not attached to one gate. A quorum `by` target is canonical
  (`<m> of {roles}` / `role and role`); `duration`/`on_elapse` appear only when a
  temporal window is declared.

A `transport.json` adds a run: `activations` (each `{source, token}`, where
`source` is a source gate) and the `expected` per-gate `verdict` and, for a
terminal gate, the `master` decision (`act` | `withhold`). It also carries `log` —
the **ordered log trace**, one `{gate, verdict}` entry per activated gate in
evaluation order, concatenated across activations in activation order (the
specification, Record and Conformance). A runner MUST check it: a missing or
misordered entry is itself a conformance failure, so the mandatory record (not only
the final verdicts) is tested.

## The three vector kinds

**Patch vectors** — input `.loom` + `expected.json` (+ optional `transport.json`):
- `draft-decide` — static projection: a routine gate and a decide gate that
  reserves a high-risk automated decision; two terminal gates.
- `draft-decide-run` — one transport: routine → `auto` → act; the reserved path →
  `reserved` → withhold.
- `multi-hop-pipeline` — strictest-wins propagation: an interior gate's `reserved`
  verdict joins to the terminal gate, which withholds.
- `multi-issue-reservations` — two reservations on distinct kinds coexist.
- `rack-approval` — the `rack` abstraction expands to two parallel pipelines.
- `redress-decl` — a released decision declared contestable: redress by an appeals
  role, empowered to overturn, within a window.
- `guard-tags` — a tag-guarded reservation (information-flow): `tags contains
  non_eu` → `reserved` → withhold; without the tag → `auto` → act.
- `prohibit-tags` — a guarded prohibition: `tags contains untrusted_model` →
  `prohibited` → withhold; without the tag → `auto` → act.
- `grade-auto` / `grade-human` — granted L3 ≥ required L2 → `auto` → act; granted L1 <
  required L3 → `human` → withhold (language-determined at the source gate).
- `grade-ungraded-at-graded` — ungraded actor at a source gate requiring L2 → `human`,
  fail-closed.
- `grade-graded-at-ungraded` — static projection: a granted grade round-trips onto the
  actor; the gate carries no `grade_required`; no verdict pinned (ungated = policy, §10).
- `grade-join` — a graded source gate's grade-`human` joins strictest-wins to a plain
  piped terminal; the proposing actor's grade is read, not a second grantee's. Grade
  lives on the source gate, never on a piped gate.
- `grade-reserved-precedence` — at a source gate that is both grade-gated and reserved on
  the token's kind, step (3) `reserved` pre-empts the step-(4) grade comparison.
- `party-projection` — a gate's `party` projects as a node attribute in the observation.
- `reserve-quorum` — a quorum reservation target projects verbatim in canonical form
  (`<m> of {roles}` and `role and role`); a matching token yields `reserved`.
- `reserve-temporal` — a reserved kind's `duration` window and `on_elapse` (`halt`/`proceed`)
  project onto the reservation; the elapse resolution itself is the host's.
- `egress-obligation` — an obligation on a terminal gate is attached (declared) and not
  projected; an `auto` gate still releases.
- `refused-precedence` — an unauthorized actor yields `refused`; `refused` pre-empts
  `reserved`, and `prohibited` pre-empts `refused`.
- `grant-narrowing` — a narrowed grant `a[kind]` / `a[kind:risks]` scopes authority; a
  token outside the grant's kind or risk scope is `refused`.

**Token vectors** — `tokens.json`, a list of `{valid, token}` an implementation
MUST classify identically (see the specification, The token):
- `token-validation` — a well-formed token has `id`, `kind`, `risk`, `party`,
  `provenance`, and an optional `tags` (an array of strings); each defect (missing
  field, out-of-domain `risk`, malformed `provenance` or `tags`, non-object) is
  rejected.

**Negative vectors** — input `.loom` + `reject.json`
(`{"stage": "parse" | "apply"}`) pinning what MUST be rejected, fail-closed:
- `reject-human-authority`, `reject-agent-to-master`, `reject-pipe-cycle`,
  `reject-unknown-target`, `reject-bad-risk` (apply-time);
- `reject-guard-id`, `reject-guard-provenance` — the no-id wall on a reservation
  guard; `reject-prohibit-guard-id`, `reject-prohibit-guard-provenance` — the same
  wall on a prohibition guard (apply-time);
- `reject-bad-grade` — a grade outside the active ladder (on both carrier positions);
  `reject-delegation-grade-amplify`, `reject-delegation-grade-from-nothing` — a delegate
  grade above the delegator's (pairwise) and a graded delegate under an ungraded
  delegator (apply-time);
- `reject-delegation-risk-amplify` — a delegate's granted risk set over a kind exceeds
  the delegator's; no-amplification (§6) makes the graph ill-formed (apply-time);
- `reject-missing-arrow`, `reject-unknown-keyword` (parse-time).

## Status

Aligned to specification v0.6. Every vector has been reproduced by two
independent reference implementations, neither derived from the other (maintained
as separate projects — this repository carries no implementation). Each
`expected.json` is the observation a conforming implementation emits; each negative
vector rejects at the stage shown; `token-validation` classifies identically. Two
independent implementations reproducing every vector is the interoperability
criterion (the specification, Conformance §9).
