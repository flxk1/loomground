<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Proposal: carry `duration` + `on_elapse` in the projected reservation

## The gap

The engine parses `reserve K by R … duration 30d : halt`, validates it "ok", and then
`project()` **drops** the duration — it never reaches the observation. The observation
schema even *forbids* it: the reservation item is `additionalProperties: false` over
`{kind, by, when}`. So a deployer's deadline silently vanishes from the canonical form.

The proof it's an oversight, not a design choice: the **same concept is handled correctly
for `redress`**. In `schema/observation.schema.json`:

| declaration | time field | projected? |
|---|---|---|
| `redress … within 14d` | `within` | **yes** — required, materialised as `null` when absent |
| `reserve … duration 30d : halt` | `duration` / `on_elapse` | **no** — schema-forbidden, dropped |

Two structurally identical concepts (a time window on a governance declaration), opposite
treatment. And it is a latent correctness bug: today `reserve x by a duration 30d:halt`
and `reserve x by a` project to **identical** observations, so two different policies are
canonically equal — which §9 (equal observation ⇔ equal policy) says must not happen.

## The change

**1. `schema/observation.schema.json`** — add two optional properties to the reservation
item (the `when` pattern: present only when declared; additive, touches no existing vector):

```json
"reservations": { "items": {
  "required": ["kind", "by"],
  "additionalProperties": false,
  "properties": {
    "kind":      { "type": "string" },
    "by":        { "type": "string" },
    "when":      { "type": "string" },
    "duration":  { "type": "string" },
    "on_elapse": { "enum": ["halt", "proceed"] }
  }
}}
```

**2. `project()`** — copy the two fields from the parsed reservation when present (the
parser already produces them; only the projection drops them).

**3. add the vector** — [`vectors/reserve-temporal`](vectors/reserve-temporal/) (drafted
here; its `expected.json` is already written to this target form, so it fails until 1+2 land).

### Why optional, not materialised (the `when` pattern, not the `redress` pattern)

`redress` *materialises* `within: null` always. Doing the same for reservations would add
`duration`/`on_elapse` to **every** existing reservation observation — rewriting
`multi-issue-reservations`, `guard-tags`, `draft-decide`, etc. The optional form matches
`when` (also an optional reservation field), is purely additive, and changes nothing that
exists. If the standard prefers uniformity with `redress`, that is the only reason to
choose materialisation — at the cost of churning every reservation vector.

## Ordering + blast radius

- **Schema + projection land together, before any engine emits the fields** — otherwise the
  emitted observation fails the (still strict) schema. Then the vector.
- **No external dependents exist yet**, so the blast radius is one downstream implementation, and the change is
  backward-compatible: existing observations validate unchanged; a consumer that ignores the
  fields is unaffected. This is the cheapest moment the change will ever be — additive now,
  versus coordinating N implementations once an ecosystem exists.

## Guardrail (apply-stage, fail-closed)

`on_elapse: proceed` is fail-open (no sign-off → the action proceeds). The standard should
consider rejecting `proceed` at apply on a kind whose reservation exists because the law
requires a human — a reserved-by-law action must never time out *into* action. Hosts should
enforce this regardless (see [`../quorum-temporal-concept.md`](../quorum-temporal-concept.md));
pinning it as a negative vector (`reject-temporal-proceed-on-…`) would make it normative.
