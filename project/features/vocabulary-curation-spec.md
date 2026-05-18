---
id: F-1
title: Vocabulary curation spec open questions closed
status: ready
roadmap_item: R-1
sprint: 1
created: 2026-05-18
ended: null
verifies_sprint_value: acceptance-5
consistency_check:
  performed_at: 2026-05-18
  agent_version: feature-consistency-reviewer@b4ae9e0
  findings:
    - kind: clean
      target: n/a
      resolution: proceed
---

## Description

The `spec/vocabulary-and-style-curation/{en,de}.md` specification ships as
`Status: draft` and carries four Open Questions that block downstream
consumers — curator agents (`prose-vale-curator`, `vocab-drift-audit` from
`claude-shared`) and reviewers — from citing the spec authoritatively. This
feature closes those questions: each is either decided and folded into the
`Requirements` (or `Acceptance Criteria`) section, or formally deferred with
a written rationale that names the awaited event. After the feature ships,
every term and rule decision can quote a settled rule instead of a draft
one.

## Acceptance criteria

- [ ] **acceptance-1** Open Question 1 (alphabetical sorting as MUST?) is
      decided and incorporated into the Requirements section of
      `spec/vocabulary-and-style-curation/en.md`, or removed from the
      `## Open Questions` list with a rationale.
- [ ] **acceptance-2** Open Question 2 (rule authoring scope — own spec
      vs. extension of this one) is decided.
- [ ] **acceptance-3** Open Question 3 (removal policy) is decided.
- [ ] **acceptance-4** Open Question 4 (vocabulary group vetting procedure)
      is decided.
- [ ] **acceptance-5** Every remaining bullet in the `## Open Questions`
      section of `spec/vocabulary-and-style-curation/en.md` either
      disappears or carries a `deferred until <event>` annotation.
- [ ] **acceptance-6** `spec/vocabulary-and-style-curation/de.md` mirrors
      the EN structure after all changes (same headings, same requirement
      bullets).

## Test hooks

- **acceptance-1** — manual: review Requirements diff for sorting-policy
  decision — pending
- **acceptance-2** — manual: review for rule-authoring-scope decision —
  pending
- **acceptance-3** — manual: review for removal-policy decision — pending
- **acceptance-4** — manual: review for vetting-procedure decision —
  pending
- **acceptance-5** — `awk '/^## Open Questions/{f=1;next} /^## /{f=0} f && /^- / && !/deferred until/' spec/vocabulary-and-style-curation/en.md | wc -l`
  returns `0` — pending
- **acceptance-6** — manual: structural diff EN ↔ DE (heading parity,
  bullet parity) — pending

## Consistency notes

The `feature-consistency-reviewer` agent re-run at SHA `b4ae9e0` after the
draft was redesigned. The earlier `duplication` finding (against
`spec/vocabulary-and-style-curation/en.md`) and the earlier `drift` finding
(against the bracket-class MUST in the same spec, line 36) were both
dissolved by construction:

- the feature now consumes the existing spec by closing its Open Questions
  in place rather than re-authoring rules in parallel, and
- the `[Pp]robot` example was removed entirely, so no acceptance criterion
  contradicts the bracket-class MUST.

The clean re-review records `proceed` as the only resolution available for
a `kind: clean` finding per the canonical feature spec's resolution
vocabulary. No sibling features exist to merge into, supersede, or split
out toward.

## Risks

- **Bikeshedding on Open Question 1 (alphabetical sorting).** Diff-review
  ergonomics is a legitimate concern but turning it into a MUST might
  force noisy re-ordering PRs. Mitigation: prefer a SHOULD or a tooling
  hook over a MUST unless the operator explicitly votes otherwise.
- **Premature decision on Open Question 4 (group vetting).** No external
  consumer is identified today, so the "at least one external consumer
  identified first" branch is hard to validate. Mitigation: accept the
  internal-consumer-only path as the working default and defer the
  external-consumer branch until a real consumer appears.
- **DE/EN drift during the same feature.** Closing four Open Questions in
  EN while keeping DE structurally in sync is a real chore; a partial
  merge that updates EN but forgets DE breaks `acceptance-6`. Mitigation:
  ship EN and DE changes in the same commit per the existing spec-
  translation conventions.
