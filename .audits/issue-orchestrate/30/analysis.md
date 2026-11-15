---
artifact-type: issue-orchestration-analysis
repo: nolte/vale-style
issue: "30"
classification: feature-request
secondary-classes: [docs]
route: direct
status: verified
created: 2026-11-15
---

# Issue Orchestration — Pre-analysis

## Issue metadata

- **Repository**: nolte/vale-style
- **Issue**: #30 — Vocabulary: accept common author/company names cited in claude-shared spec Sources sections
- **URL**: https://github.com/nolte/vale-style/issues/30
- **Labels**: none
- **Author / trust**: `nolte` (repository owner; trusted)
- **Linked items**: nolte/claude-shared#469, nolte/claude-shared#483 (merged)
- **Prior art checked**: unpushed branch `feat/claude-shared-vocabulary` (worktree `claude-shared-vocab`, commit `1911c72`, "Refs #30") adds 92 claude-shared terms; it contains **none** of the 16 names below (measured: `grep -c` per name = 0). Operator decision: build on that branch. Rebased onto `origin/develop` `d3a8302` as `2cc7a91`; `accept.txt` conflict resolved as sorted union (416 + 92 = 508 lines, 0 duplicate keys); `check_glossary_coverage.py`: 527 terms covered EN+DE. No open PR references #30 (`gh pr list --search "30 in:body"`).

## Requirements gate

- **No artefact under `project/requirements/`** (`ls project/requirements` → not found).
- **Operator override (2026-11-15)**: requirements-elicit skipped. Rationale: the issue is concrete and the term list is measured, not elicited (see Scope).

## Classification

- **Primary class**: feature-request
- **Secondary class(es)**: docs (glossary entries)
- **Rationale**: Widens the shipped vocabulary so consumers can write the names as prose; no defect in this repo.
- **Asserted cause verified**: confirmed. Code-spans in citation lines of `nolte/claude-shared/spec/**/*.md` (every line containing `http`, span matching a capitalised proper-noun pattern) were stripped of backticks and run through `vale --config .vale.ini` on `develop`: `Vale.Spelling` flags exactly 18 tokens; 16 are names (below), `Rego` and `Makefile` are code (excluded by operator).

## Scope

- **In scope**: accept 16 tokens in `technical/accept.txt` and define each in `docs/en/glossary.md` and `docs/de/glossary.md`:

| Token | Kind | claude-shared site (first) |
|---|---|---|
| Anchore | company | spec/project/dockerfile-best-practices/en.md:144 |
| Datadog | company | spec/project/test-falsifiability/en.md:163 |
| Denzin | author (Norman K. Denzin) | spec/project/e2e-failure-diagnosis/en.md:189 |
| Echobind | company | spec/project/portfolio-inherited-spec-layer/en.md:205 |
| Fairwinds | company | spec/project/kubernetes-deployment-best-practices/en.md:118 |
| Hidekazu, Konishi | author (Hidekazu Konishi) | spec/project/portfolio-inherited-spec-layer/en.md:203 |
| Inozemtseva | author (Laura Inozemtseva) | spec/project/capability-maturity-assessment/en.md:190 |
| Marmelab | company | spec/project/taskfile/en.md:86 |
| Mergify | company / product | spec/project/pull-request-workflow/en.md:218 |
| Midlibrary | site | spec/design/corporate-design-colors/en.md:179 |
| Mikulcik | author (Simon Mikulcik) | spec/project/quality-gate/en.md:110 |
| Semgrep | tool / company | spec/project/e2e-failure-diagnosis/en.md:188 |
| Snyk | company (4 sites) | spec/project/dockerfile-best-practices/en.md:139 |
| Sonrai | company (Sonrai Security) | spec/project/portfolio-inherited-spec-layer/en.md:203 |
| Tenki | company | spec/project/pull-request-workflow/en.md:218 |

- **Out of scope**:
  - `Rego`, `Makefile` — legitimate code spans (operator decision).
  - Issue checkbox 2 (drop the code-span workaround in claude-shared) — happens in nolte/claude-shared after a release ships this; the issue stays open for it unless the operator decides otherwise.

## Route

- **Decision**: direct
- **Rationale**: one coherent outcome, one PR strand (together with the rebased 92-term commit), no roadmap item.

## Work packages

### P1 — Accept the 16 tokens

- **Problem statement**: `Vale.Spelling` rejects the 16 tokens.
- **Acceptance criteria**: each token added to `src/styles/config/vocabularies/technical/accept.txt` as an exact-case entry, placed in sort order (case-insensitive, regex syntax ignored); the 16-line sample (`<name> text.`) passes `vale --config .vale.ini` with 0 `Vale.Spelling` alerts; adjacent-pair sort check reports 0.
- **Touched files**: `src/styles/config/vocabularies/technical/accept.txt`
- **Specialist**: `nolte-shared:prose-vale-curator` (extends an existing `accept.txt` in a vocabulary-owning repo)
- **Depends on**: none

### P2 — Glossary entries EN + DE

- **Problem statement**: `scripts/check_glossary_coverage.py` fails for every new term without an EN and DE definition.
- **Acceptance criteria**: `task glossary:check` passes (543 terms) and `task docs` (`mkdocs build --strict`) is green; each entry sits alphabetically under "Tools, products, and brands" (companies/products) or the section holding cited authors, matching the style of neighbouring entries; first/last name split names (`Hidekazu`, `Konishi`) defined once via a `scripts/glossary_aliases.yml` alias if the existing pattern does so.
- **Touched files**: `docs/en/glossary.md`, `docs/de/glossary.md`, possibly `scripts/glossary_aliases.yml`
- **Specialist**: no matching specialised agent — generalist remediation (`audience-doc-author` needs an audience artefact and authors audience docs, not glossary entries)
- **Depends on**: P1

## Dependency ordering

P1 → P2

## Risks

- Proper nouns accepted portfolio-wide could mask a real typo of the same word: low, the tokens are distinctive. Mitigation: exact-case entries, no regex widening.
- No security-sensitive path touched.

## Open questions

none

## Findings

| Finding | Source | Outcome | Reproduction | Issue |
|---|---|---|---|---|

## Dispatch log
2026-11-15 P1 dispatched to nolte-shared:prose-vale-curator — 16 exact-case entries added; sample 0 alerts, sort check 0 (re-verified by orchestrator)
2026-11-15 P2 handled by generalist (no matching specialised agent) — 16 EN+DE glossary entries; glossary:check 543/543, vale glossary: only the 3 pre-existing develop alerts, mkdocs build --strict green, task lint green
