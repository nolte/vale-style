---
mission_statement: vale-style ships a single curated Vale style package that consuming nolte/* repositories integrate via one .vale.ini entry to lint markdown consistently across the portfolio.
relevant_outcomes: [O-5]
audiences:
  - "nolte/* consumer repositories"
  - "Claude Code agents / skills"
  - "nolte (primary maintainer)"
verifies_via: F-1:acceptance-5
time_bound:
  kind: mvp_completion
mvp_status: defining
created: 2026-05-18
revised_at: null
---

## Statement

vale-style ships a single curated Vale style package that consuming
`nolte/*` repositories integrate via one `.vale.ini` entry to lint
markdown consistently across the portfolio.

SMART decomposition:

- **Specific** — `mission_statement` names the deliverable (a curated Vale
  style package distributed as a single ZIP) and the "for whom" (`nolte/*`
  consumer repositories plus the Claude Code curator agents and the
  primary maintainer who keep the package authoritative).
- **Measurable** — `verifies_via: F-1:acceptance-5` anchors achievement on
  one concrete acceptance criterion (every Open Question in
  `spec/vocabulary-and-style-curation/en.md` resolved or formally
  deferred). When that criterion is checked, the mission is measurably
  achieved.
- **Achievable** — the MVP scope is exactly one roadmap item (R-1),
  targeted at sprint 1 with `detail: fine`. One item, one sprint — well
  below the two-to-five-sprints SMART bound.
- **Relevant** — `relevant_outcomes: [O-5]` ties the mission to the
  outcome it directly delivers: curator agents and maintainers cite
  written rules instead of guessing. Outcomes O-1 through O-4 benefit
  indirectly once the curation rules are settled but aren't claimed here.
- **Time-bound** — `time_bound: { kind: mvp_completion }` binds the
  mission to the moment `mvp_status` reaches `achieved`. No calendar date,
  per the spec's prohibition on calendar deadlines for hobby-scale
  projects.

## Audiences

### nolte/* consumer repositories

These repositories integrate `nolte-styles.zip` via a `.vale.ini`
`Packages` entry. The MVP delivers them a citable curation reference (the
settled `vocabulary-and-style-curation` spec) so they can quote a written
rule when a vocabulary change lands rather than reading the repo's git
history. Concretely: every new term added to an `accept.txt` arrives with
a PR description that names which spec rule justifies it, which is the
auditability consumer repos need to know upstream additions won't silently
break their lint output.

### Claude Code agents / skills

The curator agents (`prose-vale-curator`, `vocab-drift-audit` from
`claude-shared`) need a stable, citable spec to ground their automated
curation decisions. The MVP delivers them exactly that: every Open
Question of the spec is closed or formally deferred, so the agents cite a
settled rule when proposing accept-list entries rather than embedding
rationale inline. The same surface is what allows `vocab-drift-audit` to
recommend retiring an entry on a spec ground instead of an ad-hoc
judgment call.

### nolte (primary maintainer)

The repo's primary maintainer adds and removes vocabulary entries through
ordinary PR flow. The MVP delivers them a self-contained reference for
what qualifies for inclusion, what the removal policy is, and how a new
vocabulary group is vetted — the three Open Questions whose answers most
directly affect day-to-day curation. Once shipped, review effort goes
into the actual edits rather than re-deriving the policy each time.

## Verification

Anchored on `F-1:acceptance-5`:

> Every remaining bullet in the `## Open Questions` section of
> `spec/vocabulary-and-style-curation/en.md` either disappears or carries
> a `deferred until <event>` annotation.

When this acceptance criterion is checked (per `project/features/vocabulary-curation-spec.md`),
the spec is settled enough for downstream consumers to cite, and the MVP
scope (R-1) is delivered.

## Source

- Audience artefact: `AUDIENCES.md` at the repo root, uncommitted at
  mission write time (file co-authored in this same bootstrap session;
  the SHA will be captured on the first commit that lands the
  `project/` planning suite).
- Outcomes consulted: O-5 from `project/goals.md`.
- Operator: nolte (`git config user.name`) via `mission-define` skill,
  commit-pending.
