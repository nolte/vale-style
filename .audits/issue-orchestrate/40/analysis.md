---
artifact-type: issue-orchestration-analysis
repo: nolte/vale-style
issue: "40"
classification: bug
secondary-classes: [infra]
route: direct
status: approved
created: 2026-11-15
---

# Issue Orchestration — Pre-analysis

## Issue metadata

- **Repository**: nolte/vale-style
- **Issue**: #40 — fix(vocab): v0.2.0 entries make Vale.Terms flag ordinary words in consumer repos
- **URL**: https://github.com/nolte/vale-style/issues/40
- **Labels**: bug
- **Linked items**: #30 (box 2 blocked by this), `nolte/claude-shared#751` (Renovate bump to v0.2.0, `lint` red)
- **Prior art checked**: no open PR touches `accept.txt`; `project/features/` and `project/roadmap.md` carry no item on Vale.Terms; #26 (`c667557`) introduced `REST`, `mS`, `kamerplanter`/`Kamerplanter('?s)?`, `[Tt]odo`/`TODOs?`.

## Classification

- **Primary class**: bug
- **Secondary class(es)**: infra (new lint guard)
- **Rationale**: a released artefact (v0.2.0) makes consumer CI fail on correct prose.
- **Asserted cause verified**: confirmed — (a) `claude-shared` run 43764369053 log: 38× `Use 'REST' instead of 'rest'`, 8× `mS`/`ms`, 13× `Kamerplanter('?s)?`, 1× `[Tt]odo`, 1× `Vale.Spelling` `und`; (b) local repro with Vale 3.15.2 + `Vocab = technical` on a 3-line sample reproduces all five shapes (scratchpad `repro/`).

## Scope

- **In scope**: correct the colliding / ordinary-word-forcing entries in `src/styles/config/vocabularies/*/accept.txt` (+ glossary EN/DE, `scripts/glossary_aliases.yml` as needed); a mechanical guard refusing the class; spec MUST in `spec/vocabulary-and-style-curation/{en,de}.md`; contributor docs.
- **Out of scope**: re-adding `und` (removed deliberately in #27 — the `claude-shared` hit is a German word in English prose, fixed there); the v0.2.1 release itself (`release-publish-trigger` after merge); #30 box 2 in `claude-shared` (follows after v0.2.1 is pinned).

## Route

- **Decision**: direct
- **Rationale**: one outcome (consumers can take a release without Vale.Terms false positives), one PR strand, no roadmap item.

## Measurement (established)

Every `accept.txt` entry expanded to its literal forms via `expand_regex` (`scripts/check_glossary_coverage.py:143`): 1021 forms, 1306 case variants (lower / Title / UPPER not themselves accepted).

- **Self-collisions** — accepted form flagged by its own vocabulary (`vale` on the forms file): `kamerplanter` (vs `Kamerplanter('?s)?`), `TODO` (vs `[Tt]odo`). 2 forms.
- **Ordinary-word forcing** — lowercase variant passes `Vale.Spelling` without the vocabulary, but `Vale.Terms` flags it with the vocabulary: `rest`(REST), `ms`(mS), `ac`(ACs?), `led`(LEDs?), `pr`(PRs?), `flux`(FLUX), `nous`(NOUS), `lix`(LIX), `musts`(MUSTs), `bun`(Bun), `renovate`(Renovate), `tailwind`(Tailwind), `anthropic`(Anthropic('s)?), `gemma`(Gemma). Digit-bearing variants (`gpio14`, `esp8285`, …) drop out because Vale.Spelling skips tokens with digits — they are not dictionary words.
- All-caps variants are skipped by `Vale.Spelling` (no `ANSIBLE` hit in the no-vocab run), so an all-caps-only entry (`REST`, `FLUX`, `NOUS`, `LIX`) adds nothing for spelling and only adds Terms forcing.

## Work packages

### P1 — Correct the colliding and word-forcing entries

- **Problem statement**: 2 self-collisions and the ordinary-word forcing cases above ship in v0.2.0.
- **Acceptance criteria**: (1) the 3-line repro sample lints clean against the worktree's vocabulary; (2) every expanded accepted form lints clean against its own vocabulary; (3) each of the 14 forcing entries is either rewritten so the ordinary word is no longer forced (remove an all-caps-only entry, plural-only acronym form such as `LEDs`, or a `(?i)` entry) or recorded as deliberate brand casing in the guard's allowlist with a one-line reason; (4) `task glossary:check` and `task test` stay green.
- **Touched files**: `src/styles/config/vocabularies/technical/accept.txt` (and `esphome/accept.txt` if an entry lives there), `docs/{en,de}/glossary.md`, `scripts/glossary_aliases.yml`.
- **Specialist**: `nolte-shared:prose-vale-curator` (owns `accept.txt` edits in a vocabulary-source repo).
- **Depends on**: P2 (the guard defines "clean"; entries are fixed until it passes).

### P2 — Guard: refuse self-collisions and unrecorded ordinary-word forcing

- **Problem statement**: nothing in `task lint` / CI lints the vocabulary against itself, so #26 shipped the class unnoticed and vale-style's own `task test` stayed green.
- **Acceptance criteria**: a `scripts/check_vocab_terms.py` (reusing `expand_regex`) plus `task vocab:check` and a pre-commit hook that (G3/G6) enumerates **every** expanded form of **every** group, not the reported sites; fails on any accepted form flagged by `Vale.Terms`; fails on any lowercase variant that is a `Vale.Spelling`-clean word yet flagged by `Vale.Terms`, unless allowlisted with a reason; (G7) asserts nothing beyond these two properties. Regression tests under `scripts/tests/` cover both failure shapes and the allowlist. Proven by running the guard against `origin/develop` (must fail, naming the measured entries) and against the fixed branch (must pass).
- **Touched files**: `scripts/check_vocab_terms.py`, `scripts/tests/test_check_vocab_terms.py`, allowlist (`scripts/vocab_terms_allow.yml` or a section in `glossary_aliases.yml`), `Taskfile.yml`, `.pre-commit-config.yaml`.
- **Specialist**: no matching specialised agent — generalist remediation (no Python/test or lint-guard specialist installed; `nolte-engineering` absent this session).
- **Depends on**: none.

### P3 — Spec and contributor docs

- **Problem statement**: the curation spec has no requirement against Vale.Terms collisions.
- **Acceptance criteria**: `spec/vocabulary-and-style-curation/en.md` gains a MUST (accepted forms don't collide; no unrecorded forcing of ordinary words) + acceptance criterion naming the guard; `de.md` structurally in sync; `docs/{en,de}/vocabularies.md` and `CLAUDE.md` mention `task vocab:check`.
- **Specialist**: `nolte-shared:spec` (spec EN→DE); docs lines by the generalist.
- **Depends on**: P2 (names the task and file).

## Dependency ordering

P2 → P1 → P3

## Risks

- **Vale in CI pre-commit**: the guard needs the `vale` binary; whether the reusable pre-commit job from `nolte/gh-plumbing` provides it is **unestablished** (settle by reading `reusable-build-static-tests` / a run log). Mitigation: pre-commit hook with `language: golang` + `additional_dependencies: [github.com/errata-ai/vale/v3/cmd/vale@v3.15.2]`, or skip-with-notice only locally and fail in CI — decide in P2.
- **Consumer-visible change**: removing all-caps entries (`REST`, `FLUX`, …) stops Terms from correcting e.g. `Rest API`. Acceptable: that correction is what breaks ordinary prose. Goes into release notes of v0.2.1.
- No security-sensitive paths.

## Operator decisions (2026-11-15)

- Pre-analysis approved; route `direct`.
- Requirements gate: **operator override** — no `requirements-elicit`; #40's Expected section is the requirement.
- Brand casing kept (allowlisted): `Renovate`, `Tailwind`, `Anthropic`, `Gemma`, `Bun`. Rebuilt: `REST`, `mS`, `ACs?`, `LEDs?`, `PRs?`, `FLUX`, `NOUS`, `LIX`, `MUSTs`.

## Open questions (resolved)

1. **Brand casing**: should `Renovate`, `Tailwind`, `Anthropic`, `Gemma`, `Bun` keep forcing their capitalised form (allowlisted as deliberate), or be relaxed? Proposal: allowlist these five, fix the other nine.
2. **Requirements gate**: no `project/requirements/` artefact exists; #40's Expected section states the four outcomes. Proposal: operator override instead of `requirements-elicit` (bounded bug with measured cause).

## Findings

- `claude-shared` also hits `und` (German word in English prose, 1×) — fix belongs in `claude-shared`, not here.
- vale-style's own `task test` is green on v0.2.0 because its docs never use `rest`/`ms` in prose — dogfooding alone can't catch this class; hence P2.
