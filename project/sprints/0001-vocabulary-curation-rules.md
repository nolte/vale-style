---
number: 1
status: planned
started: null
ended: null
value_statement: Curator agents and external contributors find written rules for accepting or rejecting vocabulary entries instead of guessing.
artifact_ref: null
last_commit: null
roadmap_items: [R-1]
features: [F-1]
---

## Goal

The `spec/vocabulary-and-style-curation/{en,de}.md` specification currently
ships as `Status: draft` with four Open Questions that block downstream
consumers (curator agents from `claude-shared`, external contributors)
from citing it authoritatively. This sprint closes those questions so the
spec becomes a settled reference rather than a draft one. Sprint value is
verified by `F-1:acceptance-5` — every remaining Open Question is either
removed or carries a `deferred until <event>` annotation.

## Features

- [F-1](../features/vocabulary-curation-spec.md) — status: ready

## Out of scope

- Authoring new vocabulary entries (no edits to
  `src/styles/config/vocabularies/<group>/accept.txt`).
- Authoring the first real Vale rule under `src/styles/nolte-styles/`
  (covered by a future roadmap item, not this sprint).
- Changing the consumer-facing `.vale.ini` shape (consumer responsibility
  per AUDIENCES.md bounded context).

## Review notes

_Populated by `sprint-review` at closure._
