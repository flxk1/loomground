<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Contributing

## Neutrality

The language is tool- and vendor-neutral. No normative document (`spec/`,
`grammar/`, `schema/`, `vocabulary/`, `conformance/`, `llms.txt`,
`language-card.json`) may depend on or reference a specific AI model, vendor,
product, or agent framework. A proposal may name one only as a clearly marked
example. Per-tool instruction files are contributor
tooling, not part of the standard; each states the rules of this file for its
tool and adds nothing normative. Prose documents (README, NOTICE, this file)
name no AI model or vendor; the commit history's assisted lines record which
tool assisted a given change. The standard also names no implementation —
conformance is a criterion (reproduce every vector), not a product list;
hand-off records under `proposals/` are the one place an implementation may be
named, as dated working notes.

## Commit convention (enforced by the commit-discipline CI job)

- Subjects are at most 72 characters.
- Do **not** add a `Co-Authored-By: <AI tool> ...` — or any AI — trailer.
  AI tools cannot author or hold copyright; only humans can.
- An AI-assisted commit instead ends the body with a plain line naming the
  tool actually used:

  ```
  Assisted by <tool> (<vendor>); not an author or copyright holder.
  ```

## Gates (run before every commit)

```
python3 check_llms_txt.py     # llms.txt / language-card drift
python3 lockstep_meta_test.py # every feature reaches grammar, schema, a vector
reuse lint                    # SPDX / REUSE compliance
```

All new files carry an Apache-2.0 SPDX header (the whole tree is
single-licensed Apache-2.0; `REUSE.toml` covers files that cannot carry one).
Do not quote the raw SPDX tag string in prose — the REUSE extractor scans whole
files and chokes on it.

## Lockstep

A feature change is complete only when the spec, the grammar, the schemas, the
vocabulary, `llms.txt`, and a conformance vector agree — the lockstep gate
fails otherwise. A conformance claim is real only when both independent
implementations reproduce every vector (specification, Conformance §9).
