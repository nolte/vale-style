---
artifact-type: issue-orchestration-analysis
repo: "nolte/vale-style"
issue: "28"
classification: "refactor"
secondary-classes: ["spec-change"]
route: "direct"
status: draft
created: "2026-11-15"
---

# Issue Orchestration — Pre-analysis

## Issue metadata

- **Repository**: nolte/vale-style
- **Issue**: #28 — Harden the glossary-coverage checker (deferred review follow-ups from #27)
- **URL**: https://github.com/nolte/vale-style/issues/28
- **Labels**: enhancement
- **Author / trust**: `nolte` (repository owner, trusted); no comments
- **Linked items**: introduced in #27 (`8abc7fd`, the only commit touching the checker); no linked or open PR (`closedByPullRequestsReferences: []`; `gh pr list --state open --base develop` empty)
- **Prior art checked**: no `project/requirements/` artifact, no roadmap or feature entry for the checker

## Classification

- **Primary class**: refactor (hardening of latent defects and a DRY cleanup; no defect triggers on today's corpus)
- **Secondary class(es)**: spec-change (one clarifying sentence on what counts as a glossary entry)
- **Rationale**: none of the four items changes today's `task glossary:check` result. They close latent false-gap and false-coverage paths and remove duplication.
- **Asserted causes verified** (all on `ef90500`, `scripts/check_glossary_coverage.py`):
  1. Escapes: confirmed. `expand_regex(r'node\.js')` → `{'node\\.js'}`, `expand_regex(r'C\+\+')` → `{'C\\+\\+'}`, `expand_regex(r'back\.?end')` → `{'back\\.end','back\\end'}`. `parse_atom` (L118–143) has no `\\` branch. No current `accept.txt` entry contains `\` (`grep -n '\\' src/styles/config/vocabularies/*/accept.txt` is empty).
  2. EN heading in DE: confirmed. The fresh-section fallback at L353 hardcodes ``## `{group}` vocabulary``. `_group_section` (L330–336) matches any H2 that carries the backticked group, so a wrong heading never self-heals.
  3. Prose false coverage: confirmed mechanism (L255–270 counts every backtick token on non-`:` lines). Measured: exactly 7 entries per language are covered *only* via prose (`commit's`, `criteria's`, `else's`, `HA's`, `maintainer's`, `navigations`, `rebased`). All of them come from the single paragraph under `### Inflected and possessive forms` / `### Beugungs- und Possessivformen` (line 1528 in both files). Every other entry is covered by a definition-term line.
  4. DRY: confirmed. `check()` L281–288 and `write_stubs()` L306–313 duplicate load → parse → per-language gaps. In the stub path each glossary is read twice (L265 `glossary_keys`, L341 `_append_stubs`).

## Requirements gate

- No requirement artifact. **Operator override recorded on 2026-11-15**: the issue states the four changes precisely, so requirements-elicit is skipped.

## Operator decisions (2026-11-15)

- Regression tests: stdlib `unittest` under `scripts/tests/`, no new dependency, run by a `local` pre-commit hook (so also in CI) plus a `task glossary:test` target.
- Item 3 allowlist: a localized prose-block H3 heading per language in the `GLOSSARIES` config (like `placeholder` / `subheading`). Glossary files stay unchanged.
- Spec: add one clarifying sentence to the curation spec (EN canonical + DE) on what counts as a glossary entry.

## Scope

- **In scope**: the four proposed changes of #28, regression tests for each latent case, Taskfile, pre-commit and CLAUDE.md wiring for the tests, and the spec sentence.
- **Out of scope** (listed in #28 itself as "related but out of scope"):
  - Removing `und` upstream in claude-shared (another repo).
  - Local `vale .` alerts on `asyncio`, `dataclass`, `Millisiemens` in `docs/en/glossary.md`. They are still present (seen in every `task test` run this session). This is a separate prose and vocabulary cleanup.

## Route

- **Decision**: direct
- **Rationale**: one coherent outcome (a hardened checker), one PR strand, no roadmap item.

## Work packages

### P1 — Test harness + baseline

- **Problem statement**: the checker has no tests, so the hardening can't be shown to preserve behaviour.
- **Acceptance criteria**: `scripts/tests/test_check_glossary_coverage.py` (unittest) covers today's behaviour: expansion of classes, groups and `?`, `normalize_key`, `display_lemma`, and that the real corpus passes. `python3 -m unittest discover -s scripts/tests` is green. A `local` pre-commit hook runs it when `scripts/` changes, and `task glossary:test` exists. The CLAUDE.md task list mentions it.
- **Touched files**: `scripts/tests/test_check_glossary_coverage.py`, `.pre-commit-config.yaml`, `Taskfile.yml`, `CLAUDE.md`
- **Specialist**: no matching specialised agent — generalist remediation (portfolio gap: no Python or test-authoring specialist in the installed catalog; `nolte-engineering` not installed)
- **Depends on**: none

### P2 — Shared gap pipeline, single read (item 4)

- **Problem statement**: `check()` and `write_stubs()` duplicate the pipeline, and the stub path reads each glossary twice.
- **Acceptance criteria**: a single `compute_gaps()`-style helper is used by both. Each glossary file is read exactly once per run, with the text passed to `glossary_keys` and `_append_stubs`. Output of `task glossary:check` is byte-identical before and after. The P1 tests stay green.
- **Touched files**: `scripts/check_glossary_coverage.py`, tests
- **Specialist**: generalist (same gap)
- **Depends on**: P1

### P3 — Escape handling (item 1)

- **Acceptance criteria**: `parse_atom` handles `\x` as the literal `x`. Tests: `node\.js` → `{'node.js'}`, `C\+\+` → `{'C++'}`, `back\.?end` → `{'back.end','backend'}`. A trailing lone `\` raises ValueError, which hits the existing fallback.
- **Touched files**: `scripts/check_glossary_coverage.py`, tests
- **Specialist**: generalist
- **Depends on**: P2

### P4 — Localized group heading (item 2)

- **Acceptance criteria**: `GLOSSARIES[lang]` gains a `group_heading` template (EN ``## `{group}` vocabulary``, DE ``## Vokabular `{group}` ``) that the fresh-section fallback uses. A test with a temp DE glossary lacking the group gets the DE heading, and a second stub run inserts under it instead of duplicating it.
- **Touched files**: `scripts/check_glossary_coverage.py`, tests
- **Specialist**: generalist
- **Depends on**: P2

### P5 — Tighten covered lemmas (item 3)

- **Acceptance criteria**: a backtick token counts as covered only (a) on a definition-term line, meaning a non-`:` line whose next non-blank line starts with `:`, or (b) inside the localized allowlisted prose block (`GLOSSARIES[lang]["covering_prose_heading"]`, up to the next heading). Tests: a backticked term in an intro paragraph no longer covers, and the inflected-forms paragraph still does. The real corpus still passes 543/543 in both languages (measured: the only prose-covered entries are the 7 in the allowlisted block).
- **Touched files**: `scripts/check_glossary_coverage.py`, tests
- **Specialist**: generalist
- **Depends on**: P2

### P6 — Spec clarification

- **Acceptance criteria**: `spec/vocabulary-and-style-curation/en.md` §MUST (glossary-coverage bullet) states that an entry is a definition-list term, or a lemma listed in the dedicated inflected/possessive-forms paragraph. `de.md` mirrors it structurally. Vale is clean on the touched spec.
- **Touched files**: `spec/vocabulary-and-style-curation/{en,de}.md`
- **Specialist**: `nolte-shared:spec` (skill; creates, updates and translates specs, keeps translations in sync)
- **Depends on**: P5 (the wording must match the implemented rule)

## Dependency ordering

P1 → P2 → {P3, P4, P5} → P6 (P3, P4 and P5 are independent of each other; they run sequentially in one working copy)

## Risks

- P5 could make a currently-covered entry a gap. Mitigation: the measurement above shows exactly 7 prose-only entries, all in the allowlisted block. The corpus test and `task glossary:check` must stay 543/543.
- The new pre-commit hook must not slow down unrelated commits. Mitigation: `files:` restricted to `^scripts/`.
- No security-sensitive path is touched (no workflow, no secrets).

## Open questions

none

## Findings

| Finding | Source | Outcome | Reproduction | Issue |
|---|---|---|---|---|
| `_expand_class` treats `\` inside `[..]` literally too (same class as item 1) | acquire scan, L75–86 | fix in P3 together with the atom branch | `expand_regex(r'[\.]x')` | — |

## Dispatch log
2026-11-15 P1 generalist (no matching specialised agent — generalist remediation) — unittest harness, pre-commit hook glossary-checker-tests, task glossary:test, CLAUDE.md; 15517be
2026-11-15 P2 generalist — compute_gaps(), one read per glossary; check output byte-identical; read-once test fails on old code; 175b41b
2026-11-15 P3 generalist — escapes in atoms and classes, \\d/\\w fall back; tests fail on old code; b196a7e
2026-11-15 P4 generalist — localized group_heading; self-heal test fails on old code; 67c7f07
2026-11-15 P5 generalist — coverage only from term lines + covering_prose_heading block; corpus 543/543 both langs; old code counted intro/heading tokens; 3d2d89a
2026-11-15 P6 dispatched to skill nolte-shared:spec — one sentence EN+DE §MUST glossary bullet, structure 22/7 both, vale clean; checker module docstring aligned
