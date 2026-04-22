# Vocabulary and Style Curation

Status: draft

## Context

This repository produces a single artefact, `nolte-styles.zip`, that downstream projects consume as a Vale `Packages` entry. Any change to a vocabulary or style therefore propagates to every consuming repo on the next release. Without a written curation process, three recurring problems appear:

- Entries accumulate ad hoc, duplicate across groups, or mask legitimate typos that Vale should flag.
- The on-disk vocabulary groups drift away from how `README.md` and `docs/vocabularies.md` describe them — as happened when `claude-shared` was referenced in docs after it had been folded back into `technical`.
- The `src/styles/nolte-styles/` directory is wired into `BasedOnStyles` but holds only a `.keep` file, so it is unclear under which conditions the first real rule can land.

This spec defines the maintenance process so that the shipped package produces a consistent lint signal across all consumers, and so that this repo's own documentation always matches the artefact it publishes.

## Goals

- Give every vocabulary group a single, documented scope so each term has exactly one correct home.
- Define entry conventions (regex form, case policy, variant collapsing) that a reviewer can check without guessing.
- Keep the on-disk state, `README.md`, and `docs/vocabularies.md` structurally in sync — a group exists in all three or in none.
- Describe how custom rule YAMLs may land under `src/styles/nolte-styles/` without further schema churn.
- Dogfood the package inside this repo so vocabulary regressions surface locally before a release.

## Non-Goals

- Authoring actual Vale rule YAMLs. When the first rule lands, it earns its own spec.
- Prescribing consumer-side `.vale.ini` settings such as `MinAlertLevel` or `IgnoredScopes`.
- Automating the release cadence. Publishing a GitHub Release already triggers the existing archive workflow; this spec does not change that flow.
- Defining vocabularies for other authors' domains. New groups are added through this process, not enumerated here.

## Requirements

- **MUST**
  - Each vocabulary group MUST live at `src/styles/config/vocabularies/<group>/accept.txt`, one entry per line.
  - Every entry MUST be a valid Vale regex. Literal strings are valid regex and are allowed.
  - Entries MUST default to case-sensitive matching (e.g. `[Pp]robot`, not `(?i)probot`) so the vocabulary still flags wrong-case variants.
  - Any commit that adds or removes a vocabulary group MUST update `docs/vocabularies.md` and the "Available vocabularies" section in `README.md` in the same commit.
  - `src/.vale.ini` (shipped in the archive) and the repo-root `.vale.ini` (used for dogfooding) MUST reference only groups that exist on disk.
  - `accept.txt` files MUST contain only regex entries — no blank lines, no comment lines — because Vale interprets every line as a pattern.
- **SHOULD**
  - Related forms SHOULD be collapsed into one regex entry (`LEDs?`, `[Hh]ostnames?`, `CLIs?`) instead of listed separately.
  - Before a term is added, the author SHOULD confirm that a current English dictionary still flags it — terms already known to Vale's base dictionary do not belong in an `accept.txt`.
  - A term SHOULD be placed in the narrowest group that fits: `technical` is the default for cross-project terminology, `esphome` for ESPHome-specific hardware and configuration terms, and a new group SHOULD be created only when a clearly bounded domain warrants it.
  - The repo-root `.vale.ini` SHOULD enable the same vocabularies it ships, so local `vale .` runs exercise the package's own assets.
  - Removing a term from a vocabulary SHOULD be preceded by a quick check of known consumer repos to avoid surprise lint failures on their next `vale sync`.
- **MAY**
  - Entries MAY be sorted alphabetically within a group when it aids review, but neither Vale nor the build depends on ordering.
  - Custom Vale rule YAMLs MAY be added under `src/styles/nolte-styles/`; the shipped `src/.vale.ini` already lists `nolte-styles` in `BasedOnStyles`, so new rules activate automatically in the next release.
  - A new vocabulary group MAY be introduced in the same PR that adds its first consumer inside this repo's own docs, to demonstrate the group is exercised end-to-end.

## Acceptance Criteria

- [ ] Every group referenced in `src/.vale.ini` and the repo-root `.vale.ini` exists as a directory under `src/styles/config/vocabularies/`.
- [ ] `docs/vocabularies.md` describes exactly the set of groups present on disk — no extra section, no missing section.
- [ ] The "Available vocabularies" list in `README.md` names the same groups, in the same order, as `docs/vocabularies.md`.
- [ ] Every `accept.txt` in the repo contains only non-empty lines and no comments.
- [ ] Running `vale sync && vale .` at the repo root passes using only the vocabularies this package ships.
- [ ] The archive built via the `Build the archive locally` snippet in `README.md` unpacks to the structure documented in the same file, including `.vale.ini`.
- [ ] Adding a new rule file under `src/styles/nolte-styles/` does not require editing `src/.vale.ini`.

## Open Questions

- Should alphabetical sorting inside `accept.txt` become a `MUST` so diff review is mechanical?
- When the first real `nolte-styles` rule is added, should rule authoring move to its own spec, or extend this one?
- Is a removal policy needed — for instance, requiring a grep across known consumer repos before a term is dropped — or is the release changelog signal enough?
- How is a brand-new vocabulary group vetted? Is a single consumer inside this repo's docs sufficient proof of need, or should at least one external consumer be identified first?
