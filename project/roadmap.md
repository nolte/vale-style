# Roadmap

This file is the queue governed by `spec/project/roadmap/` (canonical version
lives in `nolte/claude-shared`). Detail levels (`fine` / `coarse` / `backlog`)
and lifecycle (`proposed → active → done | cancelled`) are enforced by the
`roadmap-refine` and `roadmap-planner` skills. Item IDs (`R-<n>`) are
monotonic across the project's lifetime and never reused; the next item to be
added starts at `R-1`.

Items are added via `/nolte-shared:roadmap-planner`.

### R-1 — Vocabulary curation spec

```yaml
id: R-1
title: Vocabulary curation spec
detail: fine
outcomes: [O-5]
target_sprint: 1
mvp: true
status: proposed
```

Curator agents and external contributors find written rules for accepting or rejecting vocabulary entries instead of guessing; the existing `spec/vocabulary-and-style-curation/{en,de}.md` is taken from `Status: draft` to settled by closing all four Open Questions.

- [ ] vocabulary-curation-spec
