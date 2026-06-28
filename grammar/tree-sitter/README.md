<!-- SPDX-License-Identifier: Apache-2.0 -->
# tree-sitter-loomground

A **generatable** grammar for the Loomground textual surface (`.loom`),
specification v0.6. `grammar.js` is the source; the parser, AST, and editor
tooling (highlighting, structural navigation) are derived from it.

## Build & test
```bash
tree-sitter generate          # grammar.js -> src/parser.c (a parser)
tree-sitter test              # run test/corpus against the generated parser
tree-sitter parse FILE.loom   # print the AST of a .loom program
```
Requires the tree-sitter CLI (and a C compiler). The generated parser (`src/`,
bindings) is a build output and is not committed; run `tree-sitter generate`.

## Relationship to the standard
This is the grammar of `grammar/loomground.ebnf` and the specification companion
(SYNTAX) in generatable form; the specification governs. It defines only syntax —
not well-formedness or semantics, which the specification fixes and which an
implementation (e.g. the reference implementation) checks.
