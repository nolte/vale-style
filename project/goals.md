# Vision

`vale-style` supplies the nolte portfolio with curated Vale vocabularies and
(later) style rules, so that markdown content across every `nolte/*`
repository is linted consistently and technical terms like `Probot`,
`ESPHome`, or `LEDs` are decided in one place rather than reinvented per
repository.

## Outcomes

- **O-1** — Consumer repository maintainers integrate the package via a single
  `.vale.ini` `Packages` entry and get a working lint setup without
  duplicating vocabularies. _(audience: nolte/\* consumer repositories)_
- **O-2** — CI pipelines in consumer repos stay deterministic across
  releases; vocabulary changes ship through SemVer-versioned release tags
  rather than silent drift. _(audience: CI pipelines in consumer repos)_
- **O-3** — Local developers see identical lint behaviour locally and in CI,
  so corrections happen before push. _(audience: local developers in consumer repos)_
- **O-4** — Readers of markdown across the nolte portfolio see consistent
  spelling and correct technical terms regardless of which repo they land
  in. _(audience: readers of markdown content in consumer repos)_
- **O-5** — Maintainers (human or skill-driven) add a new vocabulary entry
  through a spec-grounded PR without learning the package layout from
  scratch. _(audience: nolte primary maintainer, Claude Code agents)_
