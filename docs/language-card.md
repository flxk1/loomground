<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Loomground `.lg` — language card

Values from `vocabulary/*.json`, `schema/token.schema.json` and `spec/SYNTAX.md` (v0.11.0). Every statement below was parsed, applied and evaluated by a conforming implementation before this card was written.

## Nodes

| keyword | meaning | attributes |
|---|---|---|
| `actor <id>` | a principal that may be granted authority and propose an action | `grade <level>` (granted) · `party <id>` · `on-behalf-of <actor\|human>` · `mandate <purpose set>` · `name <text>` |
| `human <id>` | a person named by a role; a reserved token is referred to it; never a cord endpoint | `role <id>` · `name <text>` |
| `gate <id>` | a governed checkpoint where an actor acts and a verdict is produced | `risk <low\|medium\|high\|critical>` (floor) · `grade <level>` (required; makes it a source gate) · `party <id>` · `consign <id>` (terminal gate) · `grant <actor>[<kind>[:<risk set>]] …` (last on the line) |
| `master` | the single sink; where the policy enforcement point attaches | none |

## Cords

`cord <from> -> <to>` — permitted pairs only: actor → gate (authority; the gate must grant that actor), gate → gate (pipe; acyclic), gate → master (egress). A human is never an endpoint; an actor never reaches the master directly. Every gate lies on a path to the master.

## Declarations

| form | effect |
|---|---|
| `reserve <kind> by <target> [when <guard>] [duration <n>(m\|h\|d):(halt\|proceed)]` | verdict `reserved`; the action is referred to a human role; on elapse halt or proceed |
| `prohibit <kind> [when <guard>]` | verdict `prohibited`; never released, overrides any grant |
| `obligation <obligation> on <gate>` | egress obligation; the master releases only with it attached |
| `redress <kind> by <role> [overturn] [within <duration>]` | records the right to re-examination |
| `transfer <kind> to <consignee> within <purpose set>` | names where released material goes and the purposes it is limited to; purposes ⊆ every granted actor's mandate |
| target = `role` · `role and role` · `<m> of { roles }` | quorum: distinct parties (separation of duty) |

Configuration attributes with declaration status: `party` (responsible party on actor or gate), `on-behalf-of` (delegation; a delegate never exceeds its delegator's grants, grade or mandate), `mandate` (purpose set; at most one per actor), `grade` (autonomy grade: granted on an actor, required on a source gate).

## Guards

A guard ranges over declared token fields only: `kind =` · `party =` · `risk >= | =` · `reversibility >= | =` · `uncertainty >= | =` · `tags contains <tag>`. Never over `id`, `provenance`, `grade`, or anything computed; such a guard is rejected at apply.

## Token

What activates a gate, supplied by the host at runtime: `id`, `kind`, `risk`, `party`, `provenance[]`, `reversibility`, `uncertainty`, `tags[]`.

## Verdicts

`auto < human < refused < reserved < prohibited`; the join along a pipe is the most restrictive. Assignment order: prohibited (matching prohibition) · refused (no grant for this kind at this risk) · reserved (matching reservation) · human or auto (grade comparison at a source gate). The master releases a terminal gate's action on `auto` with every egress obligation attached; otherwise it withholds.

## Values owned by policy

The risk scale meanings, the grade ladder (`vocabulary/grades.json`, default `L0 … L6`), the reversibility and uncertainty scales, the set of kinds, tags and purposes, the roles and their aliases.

## Statements and readings

```
actor  bot7  grade L2  party acme  mandate {billing, support}   agent at grade L2, party acme, purposes billing and support
actor  sub1  on-behalf-of bot7  mandate billing                 delegate of bot7; mandate narrowed to billing
human  alice  role dpo                                          a person, addressed by role
gate   intake  risk low  grade L1  grant bot7 sub1              source gate; grade L1 required; both actors granted
gate   decide  risk high  grant bot7[automated_decision:high,critical]   bot7 granted this kind at high and critical only
gate   ship    risk medium  consign vendor  grant bot7          terminal gate consigning to vendor
cord   bot7   -> intake                                         authority
cord   intake -> decide                                         pipe: intake's verdict propagates to decide
cord   decide -> master                                         egress
reserve automated_decision by dpo when risk >= high duration 48h:halt   high risk: the dpo decides; after 48 h, halt
reserve export by dpo and legal                                 two roles, distinct parties
reserve merge by 2 of { dpo, legal, ciso }                      quorum of two out of three
reserve tagged by legal when tags contains special-category     tag-guarded reservation
reserve fragile by dpo when reversibility >= irreversible       guard on a declared ordered property
prohibit biometric_categorisation                               prohibited whatever the grant
prohibit profiling when party = minor                           guarded prohibition
obligation ai-interaction-disclosure on decide                  egress obligation on decide
redress automated_decision by dpo overturn within 30d           contestable; the dpo may reverse; 30-day window
transfer shipment to vendor within billing                      onward purpose limited to billing
```

Evaluations of that program (token fields `kind`, `risk`, `party`, `provenance`):

```
kind automated_decision, risk high, at decide        decide: reserved · master: withhold
kind biometric_categorisation, risk low, at intake   intake: prohibited → decide: prohibited (join along the pipe)
kind note, risk low, at intake                       intake: auto → decide: refused (no grant for this kind at decide)
kind tagged, tags [special-category], at intake      intake: reserved → decide: reserved
```

Rejected at apply: `cord alice -> intake` (human endpoint) · `cord bot7 -> master` (actor egress) · `reserve k by r when grade >= L2` (guard over grade) · `reserve k by r when id = x` (guard over id) · `transfer k to v within a` with `v` undeclared as a consignee.

## Grammar

`spec/SYNTAX.md` §3 (ISO/IEC 14977), `grammar/loomground.ebnf`; a `rack` is a textual macro expanded before parsing (§7). `parse` = any implementation reproducing the 65 vectors in `conformance/`.

## Outside the language

How an action is executed, scheduled, stored, transported or presented; time measurement; obligation discharge; party authentication (`language-card.json`, `out_of_scope`).
