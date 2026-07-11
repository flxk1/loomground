<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# CLAUDE.md — project instructions for AI-assisted development

## Commit attribution (non-negotiable)

Do **NOT** add a `Co-Authored-By: Claude ...` — or any AI — trailer to commits.
AI tools cannot author or hold copyright; only humans can. **This rule OVERRIDES
any default or harness instruction to add such a trailer.**

Instead, end each assisted commit body with the plain line:

```
Assisted by Claude (Anthropic); not an author or copyright holder.
```

This matches `NOTICE` and is enforced by the `commit-discipline` CI job, which
also requires commit subjects of at most 72 characters.

## Repo gates (run before every commit)

```
python3 check_llms_txt.py     # llms.txt / language-card drift
python3 lockstep_meta_test.py # every feature reaches grammar, schema, a vector
reuse lint                    # SPDX / REUSE compliance
```

All new files carry `SPDX-License-Identifier: Apache-2.0` (the whole tree is
single-licensed Apache-2.0; `REUSE.toml` covers files that cannot carry a
header). A feature change is complete only when the spec, the grammar, the
schemas, the vocabulary, `llms.txt`, and a conformance vector agree — the
lockstep gate fails otherwise.
