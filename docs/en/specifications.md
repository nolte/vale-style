# Specifications

Engineering specs for this package live in the repository under [`spec/`](https://github.com/nolte/vale-style/tree/main/spec) — not inside this docs site. Each spec has a canonical English version and a German translation that must stay structurally in sync (same headings, same requirement bullets, same acceptance criteria).

## Current specs

| Slug | Title | EN | DE |
| --- | --- | --- | --- |
| `vocabulary-and-style-curation` | Vocabulary and Style Curation | [en.md](https://github.com/nolte/vale-style/blob/main/spec/vocabulary-and-style-curation/en.md) | [de.md](https://github.com/nolte/vale-style/blob/main/spec/vocabulary-and-style-curation/de.md) |

## How to read a spec

Specs follow a fixed template: **Context**, **Goals**, **Non-Goals**, **Requirements** (RFC 2119 keywords — `MUST`, `SHOULD`, `MAY`), **Acceptance Criteria**, **Open Questions**. A requirement in a spec is authoritative over anything written here on the docs site — if the two disagree, the spec wins and the docs should be updated.

## Adding or updating a spec

The canonical version is the only source of truth. Edits flow: canonical EN → regenerate each translation. Editing a translation directly is not the right path — lift the change into the canonical and regenerate. The [spec index](https://github.com/nolte/vale-style/blob/main/spec/README.md) in the repo lists status and last-updated information per spec.
