# Vocabulary and Style Curation

Status: draft

## Context

This repository produces a single artefact, `nolte-styles.zip`, that downstream projects consume as a Vale `Packages` entry. Any change to a vocabulary or style therefore propagates to every consuming repo on the next release. Without a written curation process, these recurring problems appear:

- Entries accumulate piecemeal, duplicate across groups, or mask legitimate typos that Vale should flag.
- The on-disk vocabulary groups drift away from how `README.md` and `docs/vocabularies.md` describe them — as happened when `claude-shared` was referenced in docs after it had been folded back into `technical`.
- The `src/styles/nolte-styles/` directory is wired into `BasedOnStyles` but holds only a `.keep` file, so it is unclear under which conditions the first real rule can land.
- A term can be accepted by a vocabulary yet never defined for readers: the glossary (`docs/en/glossary.md` and `docs/de/glossary.md`) silently drifts behind `accept.txt`, as happened when entries added in one PR were only partially covered in the next.
- An entry can break correct prose in every consumer: Vale turns each `accept.txt` entry into a `Vale.Terms` substitution that flags any case-insensitive match differing from the accepted form. v0.2.0 shipped `REST` and `mS`, which flagged the ordinary words "rest" and "ms", and the colliding pairs `kamerplanter` / `Kamerplanter('?s)?` and `[Tt]odo` / `TODOs?`, where one entry flags a form the other accepts (nolte/vale-style#40). The same substitution flagged sentence-initial capitals of lowercase entries (`cron` flagged "Cron jobs run nightly.") and capitalised ordinary words (`MRs` flagged "Mrs"). This repo's own `vale .` stayed green because its docs never used those words in prose.

This spec defines the maintenance process so that the shipped package produces a consistent lint signal across all consumers, and so that this repo's own documentation always matches the artefact it publishes.

## Goals

- Give every vocabulary group a single, documented scope so each term has exactly one correct home.
- Define entry conventions (regex form, case policy, variant collapsing) that a reviewer can check without guessing.
- Keep the on-disk state, `README.md`, and `docs/vocabularies.md` structurally in sync — a group exists in all three or in none.
- Describe how custom rule YAMLs may land under `src/styles/nolte-styles/` without further schema churn.
- Dogfood the package inside this repo so vocabulary regressions surface locally before a release.
- Guarantee that every accepted term is defined for readers: each `accept.txt` entry has a matching glossary entry in both languages, enforced automatically so a term can never ship undefined.
- Guarantee that accepting a term never makes `Vale.Terms` flag correct prose: no entry flags a form the vocabulary accepts, and no entry forces a casing onto an ordinary English word unless that is a recorded decision.

## Non-Goals

- Authoring actual Vale rule YAMLs. When the first rule lands, it earns its own spec.
- Prescribing consumer-side `.vale.ini` settings such as `MinAlertLevel` or `IgnoredScopes`.
- Automating the release cadence. Publishing a GitHub Release already triggers the existing archive workflow; this spec does not change that flow.
- Defining vocabularies for other authors' domains. New groups are added through this process, not enumerated here.

## Requirements

- **MUST**
  - Each vocabulary group MUST live at `src/styles/config/vocabularies/<group>/accept.txt`, one entry per line.
  - Every entry MUST be a valid Vale regex. Literal strings are valid regex and are allowed.
  - Entries MUST default to case-sensitive matching (e.g. `[Aa]llowlist`, not `(?i)allowlist`) so the vocabulary still flags wrong-case variants. A leading `(?i)` flag is permitted only where the case-sensitive entry would make `Vale.Terms` flag an ordinary English word (e.g. `(?i)PRs?`, `(?i)MUSTs`).
  - Entries for product or brand names MUST use the canonical casing the upstream publishes (e.g. `MkDocs`, `Probot`, `Claude`, `Dependabot`, `Vitest`) and MUST NOT use a bracket-class entry like `[Pp]robot`, because a bracket class silently accepts off-brand casings in prose. Bracket classes remain correct for generic English words whose leading letter legitimately varies with sentence position (e.g. `[Aa]llowlist`, `[Ff]rontend`), and for a project whose own canonical name is lowercase, so that the name can still open a sentence (e.g. `[Kk]amerplanter('?s)?`, `[Nn]pm`, `[Mm]ypy`).
  - Every entry that refers to a product or brand MUST be verified against its upstream canonical source (the project's README, logo, or official style guide) before it lands. The PR description MUST name the source that was checked so a reviewer can reproduce the decision; the same applies to any change of casing or removal.
  - Any commit that adds or removes a vocabulary group MUST update `docs/vocabularies.md` and the "Available vocabularies" section in `README.md` in the same commit.
  - `src/.vale.ini` (shipped in the archive) and the repo-root `.vale.ini` (used for dogfooding) MUST reference only groups that exist on disk.
  - `accept.txt` files MUST contain only regex entries — no blank lines, no comment lines — because Vale interprets every line as a pattern.
  - Every term any `accept.txt` accepts MUST have a matching entry in both `docs/en/glossary.md` and `docs/de/glossary.md`. Because each entry is a regex, a glossary entry "matches" when its readable lemma normalizes to one of the literal forms the regex accepts (lowercase, trailing plural or possessive `s` collapsed). A lemma counts as a glossary entry only on a definition-list term line (a line that starts at the left margin and whose next non-blank line is a `:` definition) or inside the dedicated inflected- and possessive-forms section under `### Inflected and possessive forms`; a term merely mentioned anywhere else in prose does not satisfy coverage. A term whose only documentation is folded into a sibling entry's definition (e.g. `severities` under `severity`) MUST be recorded in `scripts/glossary_aliases.yml` so the mapping is explicit; a pattern entry that is not a discrete lemma (e.g. a numeric pin range) MUST be exempted only via a justified entry in that file's `ignore` list.
  - The coverage check `scripts/check_glossary_coverage.py` (run via `task glossary:check`) MUST pass before a change merges. It runs as a `local` pre-commit hook and therefore also in the CI pre-commit job, so an `accept.txt` term added without a glossary entry fails the PR rather than shipping silently.
  - A literal form an entry accepts MUST NOT be flagged by `Vale.Terms` of the vocabularies that accept it. This holds for each group on its own and for all groups enabled together, because a consumer may enable any combination.
  - An entry whose accepted form is a plain lowercase word MUST also accept that form with a capital first letter (`[Cc]ron`, not `cron`), because `Vale.Terms` cannot tell a sentence start and would flag "Cron" there. Mixed-case and underscore forms (`pH`, `arXiv`, `baud_rate`) keep their exact casing.
  - An entry MUST NOT make `Vale.Terms` flag the lowercase or capitalised form of an ordinary English word, that is, a word `Vale.Spelling` accepts without any vocabulary. The only exception is enforced casing recorded with a one-line reason in `scripts/vocab_terms_allow.yml`; an allowlist record that no longer forces any word, or names no existing entry, is itself a violation.
  - The Vale.Terms check `scripts/check_vocab_terms.py` (run via `task vocab:check`) MUST pass before a change merges. It runs as the `local` pre-commit hook `vocab-terms` and therefore also in the CI pre-commit job.
- **SHOULD**
  - Related forms SHOULD be collapsed into one regex entry (`[Hh]ostnames?`, `CLIs?`, `[Aa]gents?`) instead of listed separately, unless the collapsed form would make `Vale.Terms` flag an ordinary word.
  - Before a term is added, the author SHOULD confirm that a current English dictionary still flags it — terms already known to Vale's base dictionary do not belong in an `accept.txt`.
  - A term SHOULD be placed in the narrowest group that fits: `technical` is the default for cross-project terminology, `esphome` for ESPHome-specific hardware and configuration terms, and a new group SHOULD be created only when a clearly bounded domain warrants it.
  - The repo-root `.vale.ini` SHOULD enable the same vocabularies it ships, so local `vale .` runs exercise the package's own assets.
  - Removing a term from a vocabulary SHOULD be preceded by a quick check of known consumer repos to avoid surprise lint failures on their next `vale sync`.
  - An entry that fails the Vale.Terms check SHOULD be fixed with the narrowest remedy that works, in this order: drop the entry if `Vale.Spelling` already accepts its forms unaided, including the possessive `'s` form, which Vale otherwise accepts only for vocabulary entries (`REST` and `REST's` pass; `LIX's` does not, so `LIX` stays as `(?i)LIX`); keep only the form that needs accepting (the plural `LEDs`, since `LED` passes unaided); merge colliding entries into one pattern (`(TODO|[Tt]odo)s?`); or add a leading `(?i)` flag (`(?i)MUSTs`).
  - When adding a vocabulary term, the author SHOULD run `task glossary:stubs` to scaffold the missing glossary entries, then replace each `TODO` placeholder with a real definition (or a brief placement note for a brand) in both language files before opening the PR.
- **MAY**
  - Entries MAY be sorted alphabetically within a group when it aids review, but neither Vale nor the build depends on ordering.
  - Custom Vale rule YAMLs MAY be added under `src/styles/nolte-styles/`; the shipped `src/.vale.ini` already lists `nolte-styles` in `BasedOnStyles`, so new rules activate automatically in the next release.
  - A new vocabulary group MAY be introduced in the same PR that adds its first consumer inside this repo's own docs, to demonstrate the group is exercised end-to-end.

## Acceptance Criteria

- [ ] Every group referenced in `src/.vale.ini` and the repo-root `.vale.ini` exists as a directory under `src/styles/config/vocabularies/`.
- [ ] `docs/vocabularies.md` describes exactly the set of groups present on disk — no extra section, no missing section.
- [ ] The "Available vocabularies" list in `README.md` names the same groups, in the same order, as `docs/vocabularies.md`.
- [ ] Every `accept.txt` in the repo contains only non-empty lines and no comments.
- [ ] Every product or brand name entry in every `accept.txt` matches the upstream project's canonical casing (no bracket-class entry for brands, except for a project whose canonical name is lowercase), and each such entry's introducing or modifying PR cites the upstream source that was checked.
- [ ] Running `vale sync && vale .` at the repo root passes using only the vocabularies this package ships.
- [ ] The archive built via the `Build the archive locally` snippet in `README.md` unpacks to the structure documented in the same file, including `.vale.ini`.
- [ ] Adding a new rule file under `src/styles/nolte-styles/` does not require editing `src/.vale.ini`.
- [ ] `task glossary:check` passes: every `accept.txt` term across all groups is covered in both `docs/en/glossary.md` and `docs/de/glossary.md`, with any non-lemma pattern or sibling-folded variant recorded in `scripts/glossary_aliases.yml`.
- [ ] The glossary-coverage check runs as a pre-commit hook (and thus in the CI pre-commit job), failing the build on any uncovered term.
- [ ] `task vocab:check` passes: across every group alone and all groups together, no accepted form and no sentence-initial capital of a lowercase accepted form is flagged by `Vale.Terms`, and every entry that forces a casing onto an ordinary English word is recorded in `scripts/vocab_terms_allow.yml`.
- [ ] The Vale.Terms check runs as the pre-commit hook `vocab-terms` (and thus in the CI pre-commit job), failing the build on any collision or unrecorded forcing.

## Open Questions

- Should alphabetical sorting inside `accept.txt` become a `MUST` so diff review is mechanical?
- When the first real `nolte-styles` rule is added, should rule authoring move to its own spec, or extend this one?
- Is a removal policy needed — for instance, requiring a grep across known consumer repos before a term is dropped — or is the release changelog signal enough?
- How is a brand-new vocabulary group vetted? Is a single consumer inside this repo's docs sufficient proof of need, or should at least one external consumer be identified first?
- Should sibling-folded variants (a term documented inside another entry's definition, mapped in `scripts/glossary_aliases.yml`) eventually earn their own glossary lines, or is the alias mapping their permanent home?
- Should a consumer-corpus check (linting known consumer repos with a release candidate before publishing) complement the Vale.Terms check, which proves only what the vocabulary does to the words it lists, not to the rest of a consumer's prose?
