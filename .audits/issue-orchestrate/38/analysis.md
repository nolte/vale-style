---
artifact-type: issue-orchestration-analysis
repo: "nolte/vale-style"
issue: "38"
classification: "security"
secondary-classes: ["bug"]
route: "direct"
status: draft
created: "2026-11-15"
---

# Issue Orchestration — Pre-analysis

## Issue metadata

- **Repository**: nolte/vale-style
- **Issue**: #38 — Harden release-cd-archive.yml (pinning, immutable asset, permissions, build parity)
- **URL**: https://github.com/nolte/vale-style/issues/38
- **Labels**: cicd
- **Author / trust**: `nolte` (repository owner, trusted); no comments
- **Linked items**: found during #29, delivered in #36; findings from `nolte-shared:cicd-pipeline-reviewer` (2026-11-15)
- **Prior art checked**: no open PR (`gh pr list --state open --base develop` → `[]`), no remote `fix/*release*` branch, no requirements artifact

## Classification

- **Primary class**: security (supply-chain hardening: unpinned actions, mutable release asset, missing least-privilege permissions)
- **Secondary class(es)**: bug (release notes of every published release are wiped, see below)
- **Rationale**: the issue's items are CI supply-chain and artifact-integrity controls. The measurement adds a user-visible defect with the same root (the release-mutating upload step).
- **Operator confirmed** the classification on 2026-11-15.
- **Asserted causes verified** (`develop` @ `f11e3ac`, `.github/workflows/release-cd-archive.yml`):
  - Unpinned actions: confirmed. L15 `actions/checkout@master`, L23 `vimtor/action-zip@v1.2`, L30 `ncipollo/release-action@v1.20.0`. Every other workflow uses only `nolte/gh-plumbing` reusable workflows `@v1.1.19` (`grep -h 'uses:' .github/workflows/*`).
  - Overwritable asset: confirmed. `replacesArtifacts` defaults to `'true'` (`ncipollo/release-action` `action.yml:102-105` @v1.20.0), combined with `allowUpdates: true` (L35) and the `workflow_dispatch` recovery path (L4–9).
  - No `permissions` and no `concurrency` block: confirmed (absent in the file).
  - Inline build drift: confirmed. Workflow L16–27 vs `Taskfile.yml` L39–47 (rm -rf only in Taskfile; `cp -R` vs `cp` for `.vale.ini`; `vimtor/action-zip` vs `zip -r`).
- **New defect (measured)**: on update, `ncipollo/release-action` sends `body = ""` unless `omitBody`/`omitBodyDuringUpdate` is set (`src/Inputs.ts:70-82, 228-231` @v1.20.0). It also sends name = tag, and draft/prerelease = false. Every published release has an empty body: v0.1.14, v0.1.15, v0.1.16 and v0.1.17 all report `bodylen=0` (`gh release view`), while the release-drafter draft v0.2.0 has 836 characters. The archive runs for these tags succeeded. Their logs are expired (HTTP 410), so the wipe is inferred from the action source plus the empty bodies, not observed in a log. **Unestablished**: observing it directly would need a fresh release run.
- **Further measured gaps**:
  - On `workflow_dispatch`, `actions/checkout` without `ref:` checks out the dispatching branch, not the requested tag. A recovery run therefore builds the zip from the wrong commit (GitHub checkout default; the workflow passes no `ref`).
  - `Taskfile.yml` L47 `zip -r` updates an existing `build/nolte-styles.zip` in place, so files removed from `src/` survive in a locally rebuilt zip (`rm -rf` at L42 clears only the staging dir).
  - CLAUDE.md L61 says the reusable workflows are "pinned to `v1.1.12`", while they use `@v1.1.19`.

## Requirements gate

- No requirement artifact. **Operator override recorded on 2026-11-15**: the issue lists the concrete controls.

## Operator decisions (2026-11-15)

- Upload: replace `ncipollo/release-action` **and** `vimtor/action-zip` with `task build` plus `gh release upload <tag> nolte-styles.zip`. Without `--clobber` this fails if the asset exists, and it never touches release metadata.
- Task in CI: `go-task/setup-task`, digest-pinned, with a pinned Task version and archive checksum.
- Also in scope: file an upstream issue in `nolte/gh-plumbing` (items 6/7), and correct the CLAUDE.md pin.
- Not in scope: restoring the wiped bodies of v0.1.14–v0.1.17.

## Scope

- **In scope**: items 1–5 of #38; the checkout `ref` fix; the stale-zip fix in `task build`; docs that describe the archive build; the CLAUDE.md pin; the upstream issue for items 6/7.
- **Out of scope**: restoring past release notes (operator decision). Provenance attestation and a reusable workflow belong upstream (items 6/7).

## Route

- **Decision**: direct
- **Rationale**: one workflow file plus its Taskfile and doc mirrors, one PR strand, no roadmap item.

## Work packages

### P1 — Rewrite release-cd-archive.yml

- **Acceptance criteria**:
  - Workflow-level `permissions: contents: read`; the job gets `contents: write` only.
  - `concurrency` grouped by workflow and tag, with `cancel-in-progress: false`.
  - `actions/checkout` pinned to the v7.0.1 digest with a version comment, `ref:` set to the release tag, and `persist-credentials: false`.
  - `go-task/setup-task` pinned to the v2.2.0 digest with a pinned Task `version` and `checksum`.
  - The build runs via `task build`.
  - The upload uses `gh release upload "$TAG" build/nolte-styles.zip` without `--clobber`. The tag reaches the shell via `env:`, never as inline `${{ }}`.
  - No `vimtor/action-zip` and no `ncipollo/release-action` remain.
  - YAML parses, and `actionlint` is clean if available.
- **Touched files**: `.github/workflows/release-cd-archive.yml`
- **Specialist**: skill `nolte-shared:cicd-pipeline-design` (scaffold/patch)
- **Depends on**: P2

### P2 — Make `task build` CI-safe and reproducible

- **Acceptance criteria**: `task build` removes a stale `build/nolte-styles.zip` before zipping. Run twice in a row, after deleting a file from the staging input, the zip no longer lists that file. The zip still lists `nolte-styles/LICENSE` and `nolte-styles/.vale.ini`.
- **Touched files**: `Taskfile.yml`
- **Specialist**: skill `nolte-shared:cicd-pipeline-design` (same dispatch as P1, since local/CI parity is its §E concern)
- **Depends on**: none

### P3 — Docs

- **Acceptance criteria**: CLAUDE.md says the reusable workflows are pinned to `v1.1.19`. CLAUDE.md, README and `docs/{en,de}/contributing.md` describe the archive workflow as running `task build` and `gh release upload`, and the "same three copies" wording becomes "runs `task build`". EN and DE stay in sync. Vale is clean, `mkdocs build --strict` is green.
- **Touched files**: `CLAUDE.md`, `README.md`, `docs/en/contributing.md`, `docs/de/contributing.md`
- **Specialist**: agent `nolte-shared:audience-doc-author`
- **Depends on**: P1

### P4 — Upstream issue in nolte/gh-plumbing

- **Acceptance criteria**: one issue in `nolte/gh-plumbing` proposes a reusable "build archive and attach to release" workflow with build provenance (`actions/attest-build-provenance`) and an artifact-to-securing-stage mapping. It cites #38 and the body-wipe pitfall of `ncipollo/release-action` without `omit*DuringUpdate`, and suggests a portfolio guard against tag- or branch-pinned third-party actions. The issue is filed only after the operator confirms its text.
- **Touched files**: none (GitHub issue)
- **Specialist**: no matching specialised agent — generalist remediation
- **Depends on**: P1 (cites the implemented pattern)

## Dependency ordering

P2 → P1 → P3 ; P4 after P1 (independent of P3)

## Defect-class decision (bug secondary)

- **Class**: a workflow step mutates the metadata of an already published release.
- **Repair**: the only such step (`ncipollo/release-action` with `allowUpdates`) is removed. `gh release upload` without `--clobber` adds an asset only.
- **Guard**: a mechanical guard against tag- or branch-pinned third-party actions belongs portfolio-wide (`nolte/gh-plumbing` pre-commit or CI), so it goes into P4's upstream issue rather than becoming a local one-off. The class sweep predicate (`grep -nE 'release-action|gh release (edit|create)|allowUpdates' .github/workflows/*`) is run before the PR, and its count is recorded in the `fix` PR's `## Class sweep`.

## Risks

- A wrong digest or checksum breaks the next release. Mitigation: resolve the digests from the tag via the API (`gh api repos/<r>/commits/<tag>`), take the checksum from the Task release's checksums file, and run `task build` locally. The workflow itself only runs on a release, so it is first exercised by the next release. A failure there is loud: an upload fails closed, it doesn't wipe anything.
- Security-sensitive path (`.github/workflows/`): `cicd-pipeline-reviewer` re-audits it and a security review of the diff runs before the PR.

## Open questions

none

## Findings

| Finding | Source | Outcome | Reproduction | Issue |
|---|---|---|---|---|
| Published release bodies wiped by `ncipollo/release-action` update defaults | acquire measurement | fixed by P1 (step removed); past bodies not restored (operator) | `gh release view v0.1.17 --json body` | #38 |
| `workflow_dispatch` recovery checks out the dispatching branch, not the tag | acquire scan | fixed in P1 (`ref:`) | workflow L15 has no `ref` | #38 |
| Local `zip -r` keeps stale entries in an existing zip | acquire scan | fixed in P2 | `Taskfile.yml` L47 | #38 |
| CLAUDE.md pin `v1.1.12` vs `@v1.1.19` | acquire scan | fixed in P3 | `CLAUDE.md:61` | #38 |

## Dispatch log
2026-11-15 P2+P1 dispatched to skill nolte-shared:cicd-pipeline-design — rewrite with pinned checkout v7.0.1 (refs/tags ref, no persisted creds), setup-task v2.2.0 (exact version, checksum, repo-token empty), task build, gh release upload -- "$TAG" without --clobber, permissions read/write-at-job, concurrency per tag, ubuntu-24.04; Taskfile clears stale zip. actionlint clean; local build + stale-entry test OK. Re-audit nolte-shared:cicd-pipeline-reviewer: 8/8 prior findings fixed; N1 (token to setup-task) fixed via repo-token empty (installer.ts:95-98 skips API on exact semver); N2 refs/tags fixed; N3 -- fixed; N4 refuted (checksum declared + verified installer.ts:160); N5 + provenance + reuse -> P4 upstream; pre-merge build check (CI §F) -> P4
Class sweep predicate: grep -nE "release-action|gh release (edit|create)|allowUpdates" .github/workflows -> develop 2 hits, after 0
2026-11-15 P3 dispatched to nolte-shared:audience-doc-author — CLAUDE.md (pin v1.1.19, archive bullet, raw block mirrors Taskfile), README, docs/{en,de}/contributing.md; vale clean, task lint green, mkdocs --strict exit 0. Corpus grep found AUDIENCES.md:46 @v1.1.12 -> fixed. renovate.json5 preset stays v1.1.12 (pinDigests only from gh-plumbing v2.0.0) -> noted for P4/PR
2026-11-15 P4 generalist (no matching specialised agent — generalist remediation) — filed nolte/gh-plumbing#446 after operator confirmation; interim note added to release-cd-archive.yml
2026-11-15 security review (general-purpose agent on worktree diff, 7 files): no blocking findings; notes: provenance (-> #446), tag ruleset (repo setting, out of scope), manual partial-asset cleanup on recovery (documented in PR)
