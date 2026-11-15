---
artifact-type: issue-orchestration-analysis
repo: "nolte/vale-style"
issue: "29"
classification: "infra"
secondary-classes: ["docs"]
route: "direct"
status: draft
created: "2026-11-15"
---

# Issue Orchestration — Pre-analysis

## Issue metadata

- **Repository**: nolte/vale-style
- **Issue**: #29 — Add a LICENSE file (MIT) — license-check NOASSERTION exception expires 2026-10-24
- **URL**: https://github.com/nolte/vale-style/issues/29
- **Labels**: none
- **Author / trust**: `nolte` (repository owner, trusted)
- **Linked items**: nolte/claude-shared#467 (audit), nolte/claude-shared#455 (refs); no linked PR in this repo (`closedByPullRequestsReferences: []`)
- **Prior art checked**: no open PR, no `project/requirements/` artifact, no roadmap item for licensing. No PR in this repo references #29 (`gh pr list --search "29 in:body"` returned only the unrelated #3 and #4).

## Classification

- **Primary class**: infra (repository and release packaging, not CI health, so it does not short-circuit to workflow-health-triage)
- **Secondary class(es)**: docs
- **Rationale**: The issue asks for a missing repository artifact (LICENSE) and a release that carries it. No behaviour of the vocabularies changes.
- **Asserted cause verified**: confirmed. There is no `LICENSE*` at the repo root (`ls -a` on 51c6217). `gh api repos/nolte/vale-style --jq .license` returns `null`, which yields `NOASSERTION` in downstream SBOMs. No `.md` or YAML file declares a licence (`grep -rniE 'licen[cs]e'` hits only AUDIENCES.md:39,71, which expect "licence clarity", and glossary terms).
- **Deadline**: the recorded exception expired on 2026-10-24. Today is 2026-11-15, so it is already overdue.

## Requirements gate

- No requirement artifact exists. **Operator override recorded on 2026-11-15**: the requirement (an MIT LICENSE) is unambiguous, so requirements-elicit is skipped.

## Operator decisions (2026-11-15)

- Scope: the LICENSE goes at the repo root **and** ships inside `nolte-styles.zip`, because MIT requires the notice in every copy. The README gets a License section.
- Copyright line: `Copyright (c) 2024-2026 nolte` (first commit 2024-01-11).

## Scope

- **In scope**: the root `LICENSE` (MIT); a LICENSE copy in the zip via `task build` and `.github/workflows/release-cd-archive.yml`; the documentation that mirrors the build recipe or the archive layout (README build section, archive-structure fragment, a new `## License` section, CLAUDE.md build section, `docs/{en,de}/contributing.md`).
- **Out of scope**:
  - Issue checkbox 2 ("Cut a release"). This is not PR content. It happens after the merge via `release-publish-trigger`, with operator confirmation. The issue stays open until then.
  - `actions/checkout@master` and other unpinned actions in `release-cd-archive.yml`. This is a pre-existing pinning gap, triaged under Findings and not fixed here.

## Route

- **Decision**: direct
- **Rationale**: one coherent outcome (licence clarity), one PR strand, no roadmap item.

## Work packages

### P1 — Root LICENSE file

- **Problem statement**: the repo has no licence, so GitHub and SBOM tooling resolve `NOASSERTION`.
- **Acceptance criteria**: `LICENSE` exists at the root with the verbatim MIT text and `Copyright (c) 2024-2026 nolte`. GitHub's licensee detection reports `MIT` after the merge (`gh api repos/nolte/vale-style/license --jq .license.spdx_id`).
- **Touched files**: `LICENSE`
- **Specialist**: no matching specialised agent — generalist remediation (portfolio gap: no licence-scaffolding skill; project-structure-apply covers its artefact list, which doesn't include LICENSE)
- **Depends on**: none

### P2 — Ship LICENSE in nolte-styles.zip

- **Problem statement**: the release zip is a copy of the software and carries no licence notice.
- **Acceptance criteria**: after `task build`, `unzip -l build/nolte-styles.zip` lists `nolte-styles/LICENSE`. `release-cd-archive.yml` performs the same copy. No other workflow change.
- **Touched files**: `Taskfile.yml`, `.github/workflows/release-cd-archive.yml`
- **Specialist**: `nolte-shared:cicd-pipeline-design` (skill; designs, scaffolds and patches workflow files). Verified afterwards by the read-only `nolte-shared:cicd-pipeline-reviewer` agent and by the built-in `security-review`, since the change touches `.github/workflows/`.
- **Depends on**: P1

### P3 — Documentation sync

- **Problem statement**: the build recipe and the archive layout are documented in five places, and the README has no licence statement.
- **Acceptance criteria**: README, CLAUDE.md and `docs/{en,de}/contributing.md` show the LICENSE copy in the build recipe. The archive-structure tree lists `LICENSE`. README has `## License` with `[MIT](LICENSE)` and the copyright holder. EN and DE stay structurally in sync. `task test`, `task docs` (`mkdocs build --strict`) and `task lint` are green.
- **Touched files**: `README.md`, `CLAUDE.md`, `docs/en/contributing.md`, `docs/de/contributing.md`
- **Specialist**: `nolte-shared:audience-doc-author` (agent; refines docs against the existing `AUDIENCES.md` artifact)
- **Depends on**: P2 (the recipe must match the implemented commands)

## Dependency ordering

P1 → P2 → P3

## Risks

- A workflow edit in `.github/workflows/` is security-sensitive, so `security-review` must run on the worktree diff before the PR. Mitigation: a minimal one-line `cp` change; the reviewers verify it.
- Vale may flag the MIT boilerplate or "licence/license". Mitigation: `/.vale.ini` lints Markdown only, and LICENSE has no `.md` extension. Verified via `task test`.
- The docs build pulls README fragments between markers, so a broken marker breaks the site. Mitigation: `mkdocs build --strict` runs in verify.

## Open questions

none

## Findings

| Finding | Source | Outcome | Reproduction | Issue |
|---|---|---|---|---|
| C1–C3: `actions/checkout@master`, `vimtor/action-zip@v1.2`, `ncipollo/release-action@v1.20.0` not digest-pinned (GHA §A) | cicd-pipeline-reviewer | pre-existing, out of scope; proposed to file | `release-cd-archive.yml:15,23,30` | — |
| C4: `allowUpdates: true` + `workflow_dispatch` can overwrite a published `nolte-styles.zip` (CD §B immutability) | cicd-pipeline-reviewer | pre-existing, out of scope; proposed to file | `release-cd-archive.yml:4-8,35` | — |
| W1/W2: no `permissions` block, no `concurrency` group | cicd-pipeline-reviewer | pre-existing, out of scope; proposed to file | `release-cd-archive.yml:1-13` | — |
| W3/W4/S2: no build provenance, no artifact-to-securing-stage matrix, archive logic local instead of gh-plumbing | cicd-pipeline-reviewer | pre-existing; upstream candidate (nolte/gh-plumbing) | `release-cd-archive.yml:29-35` | — |
| W5: workflow re-implements the build inline instead of `task build` (already diverges: rm -rf, cp vs cp -R, zip tool) | cicd-pipeline-reviewer | pre-existing, out of scope; proposed to file | `release-cd-archive.yml:16-27` vs `Taskfile.yml:34-42` | — |

## Dispatch log
2026-11-15 P1 generalist (no matching specialised agent — generalist remediation) — LICENSE added, MIT text matches SPDX modulo line wrap, commit 3e5f48d
2026-11-15 P2 dispatched to skill nolte-shared:cicd-pipeline-design (scaffold, narrow patch) — `cp LICENSE` in Taskfile build + release-cd-archive.yml; `task build` zip lists nolte-styles/LICENSE; audit by nolte-shared:cicd-pipeline-reviewer: no new finding from the added line, 12 pre-existing findings triaged above
2026-11-15 P3 dispatched to nolte-shared:audience-doc-author — README (build recipe, archive tree, ## License), CLAUDE.md, docs/{en,de}/contributing.md; vale 0 alerts on touched files, task lint green, mkdocs build --strict green
