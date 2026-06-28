# Loomground — for agents

If you are an agent or tool working with Loomground, read **`llms.txt`** — the
self-contained guide to reading, emitting, and validating the language. In short:

- The language and its declarations: `llms.txt`, `language-card.json`.
- Emit a `.loom` patch and validate it against `schema/patch.schema.json`.
- Apply the litmus: a regulation *names* it → express it; a deployment chooses
  values → policy; a runtime *does* it (compute, aggregate, schedule, persist,
  communicate) → host, **not** expressible — hand it off rather than forcing it
  into a guard.
- The normative source is `spec/SPEC.md`; it governs over this file and `llms.txt`.

This file and `llms.txt` describe the language; they reference no host or program.
