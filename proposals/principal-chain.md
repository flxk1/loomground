<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Proposal: the principal chain — making the agent–principal relation first-class

**Status: draft for v0.7. Additive; no node class, no cord type, no verdict added.**

## Claim

The deepest relation in this language is already the agency relation — an actor
acting *for* someone, with authority that must not exceed what it was given. The
no-amplification invariant (§6) is agency law's oldest rule stated in OCAP terms.
But v0.6 treats that relation as a side-constraint on grants, not as the spine of
the graph. Four precise gaps follow, each verifiable against the current tree:

1. **The chain cannot root in a person.** §6 binds delegation between "two
   declared actors"; a `human` cannot be a delegator. The ultimate principal —
   the person or accountable party on whose behalf the whole run happens — is
   expressible only by modelling them as a synthetic `actor`, which conflates
   *being answerable* with *proposing actions*.
2. **The chain may cycle.** Only the pipe relation is required to be acyclic
   (§5.1). Two actors delegating to each other with equal grant sets satisfy
   no-amplification (subset is reflexive) and are well-formed today. "Everyone
   acts on behalf of everyone" is an accountability void the grammar admits.
3. **The chain is invisible in the observation.** `on_behalf_of` is in
   `schema/patch.schema.json` (input) but not in `schema/observation.schema.json`
   (output; `additionalProperties: false`). It is apply-checked, then dropped —
   the same parsed-then-unprojected defect the temporal fields had before the
   RVND hand-off. All three delegation vectors are negative; nothing pins that
   the binding round-trips.
4. **The chain does not carry responsibility.** `party` and `on-behalf-of` are
   unlinked: the specification says each actor and gate bears a party, the
   grammar makes `party` optional, and no rule says whose party a partyless
   delegate bears. The relation that *should* allocate answerability doesn't.

In short: v0.6 covers agent–principal as **authority attenuation** (who may not
exceed whom — genuinely well done, pairwise over risk and grade, fail-closed) and
does not cover it as **accountability anchoring** (who answers for the act). This
proposal adds the second half, with the same discipline as everything else in the
language: declared facts, no computation, fail-closed.

## The design split

Authority and answerability travel on different rails, and the proposal keeps
them apart:

- **Authority** comes only from cords and grants at gates (§5.1) — unchanged.
- **Answerability** travels the `on-behalf-of` chain — the *principal chain* —
  which this proposal makes rooted, acyclic, projected, and party-bearing.

A human terminus therefore adds no authority (consistent with §3: "a role does
not by itself confer authority") and no cord (the human stays graph-disconnected;
`on-behalf-of` is an attribute on the delegate's declaration, as today).

## Changes

**P1 — a `human` MAY be a delegator.** `actor a on-behalf-of alice` where
`alice` is a declared `human`. The no-amplification invariant ranges over
actor→actor links only; the human link is an accountability anchor, not an
authority source. A chain whose last link names a human is *rooted in a person*.
Grounding: the principal of agency law ([BGB §164]; [RESTATEMENT] §1.01); the
human on whose behalf a solely-automated decision is made ([GDPR] Art. 22); the
deployer's oversight duty ([AIA] Art. 26).

**P2 — the on-behalf-of relation MUST be acyclic** (well-formedness, §5.1 list).
Every chain then terminates — at a human (P1), at an actor with no delegator, or
nowhere new: a cycle is ill-formed and the graph has no effect (fail-closed).
Transitive attenuation needs no new rule: pairwise subset composes along the now
well-founded chain; a vector pins the three-link case.

**P3 — project the chain.** `on_behalf_of` becomes a projected actor attribute in
`schema/observation.schema.json`, exactly as `grade` and `party` are. The agency
relation becomes part of the canonical form conformance compares, and of the
recorded inputs that make the log usable for attribution (§7.4, §7.5). This is
the identical fix `duration`/`on_elapse` received; the lockstep gate exists so
this class of gap (parsed, checked, unprojected) cannot recur silently.

**P4 — party inheritance along the chain.** A delegate that declares no `party`
bears its delegator's party, resolved at apply by walking the (acyclic, P2)
chain to the nearest declared party; if the chain ends with no party declared
anywhere, the actor is partyless exactly as today. A declared inheritance,
resolved from declared facts — a selection, not a computed value (the §4
declared-maximum precedent). The party-guard and quorum distinctness then see
through delegation instead of past it.

**P5 (profile, not core) — rooted-chain conformance profile.** A deployment MAY
require: every actor's principal chain terminates at a `human` or at a
party-bearing actor. This is the "no unaccountable agent" property regulators
will ask for by name; it stays a profile because purely organisational
principals (the org as party-bearing actor) are legitimate. Cf. controller /
processor ([GDPR] Art. 4(7), 4(8)); provider/deployer ([AIA] Art. 3).

## New vectors

| Vector | Pins |
| --- | --- |
| `obo-projection` | `on_behalf_of` round-trips into the observation (positive) |
| `obo-chain-attenuation` | a→b→c: pairwise subset holds along a three-link chain |
| `obo-human-root` | a chain terminating at a `human` is well-formed; the human gains no authority |
| `party-inheritance` | a partyless delegate projects its delegator's party |
| `reject-obo-cycle` | mutual delegation is ill-formed at apply |
| `reject-obo-undeclared` | on-behalf-of naming an undeclared node is ill-formed at apply |

## Compatibility

Additive. No existing vector declares `on-behalf-of` positively, so no
`expected.json` changes; the observation schema gains one optional attribute;
the well-formedness list gains one clause (P2) that no conforming patch relied
on violating. Grammar: `on-behalf-of <id>` already parses; P1 only widens what
the id may resolve to at apply. Targets v0.7 with the two-implementation
criterion of §9 applying to the new vectors as to all others.

## Not proposed

Apparent authority, ratification of an unauthorized act (redress-adjacent;
separate discussion), revocation within a run (authority is fixed per
activation, §5.2 — unchanged), and runtime conferral on sub-actors (§10 —
unchanged). The chain declares who answers; it does not simulate agency law.

## Grounding additions

[RESTATEMENT] Restatement (Third) of Agency §1.01 (2006): agency as the
fiduciary relation arising when a principal manifests assent that an agent act
on the principal's behalf and subject to the principal's control. [BGB §164]
Bürgerliches Gesetzbuch §§164–181 (Stellvertretung; §181 self-dealing is the
classical cousin of the quorum distinctness check). [RFC8693] OAuth 2.0 Token
Exchange, `act` and `may_act` claims — deployed prior art for representing and
*chaining* on-behalf-of relations in the token itself, and for projecting the
chain into what a verifier sees. [XACML-ADMIN] OASIS XACML v3.0 Administration
and Delegation Profile — prior art for delegation constraints checked at policy
level.
