# Audiences — vale-style

<!--
Produced via the `audience-identify` skill, following
spec/project/audience-identification/ in claude-shared.
Do not add audiences without first declaring the bounded context below.
-->

## Bounded context

- **What this is:** A versioned Vale style package, distributed as the GitHub release artifact `nolte-styles.zip`. Contents: curated Vale vocabularies (`technical`, `esphome`) under `src/styles/config/vocabularies/<group>/accept.txt`, a package-internal `.vale.ini`, and a placeholder `src/styles/nolte-styles/` for future Vale rule YAML. Consuming repositories integrate the package via a `Packages` entry plus `StylesPath` in their own Vale configuration.
- **Boundaries:**
  - Source of truth for the shipped vocabularies and (future) rule sets
  - Curation specs under `spec/<slug>/<lang>.md` that codify accept / reject rules
  - Dogfooding via the root `/.vale.ini` (lints this repository's own markdown against the shipped vocabularies)
  - MkDocs site (`docs/`) as consumer-facing documentation
  - CI and release plumbing via reusable workflows from `nolte/gh-plumbing`
- **Explicitly out of scope:**
  - How consuming repositories assemble their own `.vale.ini` (consumer responsibility)
  - The Vale engine itself (external toolchain dependency)
  - Non-Vale linters (for example prose linters without a Vale backend)
  - Content-level judgments on whether a single term is "correct" — decided through curation specs, not ad hoc
  - Distribution outside GitHub releases (no npm, PyPI, or Homebrew publication path)

## Audiences

Each entry: label, relationship category, interaction surface, expectation,
open questions, `confirmed` or `assumed`, criticality (primary / secondary /
peripheral). A whole category is marked `none — <reason>` when it does not apply.

### Direct consumers

- **nolte/* consumer repositories** — _category_: direct-consumer · _surface_: `.vale.ini` `Packages` entry, GitHub release URL · _expects_: stable, SemVer-versioned ZIP URL; runnable vocabularies; backwards-compatible vocabulary names (`technical`, `esphome`) · _status_: `assumed` · _criticality_: primary
  - Open questions: which `nolte/*` repos actually consume this package today? Is the list discoverable via a search across `nolte/*` for `Packages = nolte-styles` style strings?
- **CI pipelines in consumer repos** — _category_: direct-consumer · _surface_: `vale-action` or `vale .` in GitHub Actions workflows · _expects_: reproducible lint runs, no flaky vocabulary drift, no breaking changes without a major version bump · _status_: `assumed` · _criticality_: primary
  - Open questions: do consumers pin to a specific release tag, or do they float on `latest`? The answer changes the blast radius of every release.
- **Local developers in consumer repos** — _category_: direct-consumer · _surface_: `vale .` CLI locally · _expects_: identical behaviour locally and in CI; documented accept / exception syntax · _status_: `assumed` · _criticality_: secondary
  - Open questions: are developers expected to install Vale themselves, or via a project-level task / devcontainer?
- **External consumers (public, non-`nolte`)** — _category_: direct-consumer · _surface_: GitHub release asset on the public repo · _expects_: discoverability via GitHub search / README, licence clarity · _status_: `assumed` · _criticality_: peripheral
  - Open questions: is external adoption a goal, or a tolerated side-effect of the repo being public?

### Operators

- **nolte (repository maintainer)** — _category_: operator · _surface_: GitHub Releases UI, `Taskfile.yml`, `.github/workflows/release-*` · _expects_: runnable `task build` / `task test` / `task docs`; reproducible release cuts via release-drafter → `release-cd-archive.yml`; predictable SemVer bumps · _status_: `assumed` · _criticality_: primary
  - Open questions: none beyond ordinary release hygiene.
- **GitHub Actions runners / platform** — _category_: operator · _surface_: workflow YAML, reusable workflows pinned to `nolte/gh-plumbing@v1.1.12` · _expects_: stable pinned versions, deterministic builds, no unpinned actions · _status_: `assumed` · _criticality_: secondary
  - Open questions: none.
- **Renovate / Mend bot** — _category_: operator · _surface_: `renovate.json5`, Probot Settings · _expects_: readable dependency definitions, PRs against `develop`, grouped `group:all` updates · _status_: `assumed` · _criticality_: peripheral
  - Open questions: is the Mend dashboard reachable and showing activity for this repo? (verifiable via Renovate-app installation check)

### Contributors / maintainers

- **nolte (primary maintainer)** — _category_: contributor · _surface_: local `git`, PR flow on `develop`, Conventional Commits, pre-commit, Taskfile · _expects_: working hooks, fast local lint (`task test`), traceable develop → main release path · _status_: `assumed` · _criticality_: primary
  - Open questions: none.
- **Claude Code agents / skills** (`prose-vale-curator`, `vocab-drift-audit` from `claude-shared`) — _category_: contributor · _surface_: skill invocations against `src/styles/.../accept.txt`, `.claude/settings.json` permission allowlist · _expects_: writable vocabulary files, PR flow against `develop`, curation specs under `spec/` to ground decisions · _status_: `assumed` · _criticality_: primary
  - Open questions: which skills should be allow-listed without per-call prompts, and which require a confirm step (per `permission-allowlist-maintain`)?
- **External contributors** — _category_: contributor · _surface_: GitHub PRs, `CONTRIBUTING.md`, issue templates · _expects_: documented accept / reject rules (specs under `spec/`), traceable CI checks (Vale, Trivy, chain-bench, MkDocs `--strict`) · _status_: `assumed` · _criticality_: secondary
  - Open questions: is external contribution actively solicited, or only opportunistically accepted?

### Governing parties

- **nolte (repo owner)** — _category_: governing · _surface_: branch protection rules, `.github/settings.yml` via Probot Settings, spec approval · _expects_: veto authority on vocabulary and style changes; final say on SemVer-major cuts · _status_: `assumed` · _criticality_: primary
  - Open questions: none.
- **nolte portfolio consensus** (specs under `claude-shared/spec/`) — _category_: governing · _surface_: pull-request-workflow, branching-model, release-automation, project-structure specs · _expects_: repo stays conformant; deviations propagate via spec update, not silently · _status_: `assumed` · _criticality_: primary
  - Open questions: does this repo need its own per-spec opt-out tracking, or does conformance suffice?

### Indirect audiences

- **Readers of markdown content in consumer repos** — _category_: indirect · _surface_: rendered README / docs / ADRs in `nolte/*` repos, processed through Vale · _expects_: consistent spelling and correct technical terms (`Probot`, `ESPHome`, `LEDs`); no linguistic inconsistencies across repos · _status_: `assumed` · _criticality_: secondary
  - Open questions: how is "consistency across repos" measured today — anecdotally, or via a portfolio-wide audit?
- **FOSS community as reference consumers** — _category_: indirect · _surface_: public GitHub repo, MkDocs site · _expects_: the repo serves as a traceable template for their own Vale style packages; clear licence footprint · _status_: `assumed` · _criticality_: peripheral
  - Open questions: is reference value an explicit goal, or only a side benefit?

## Open questions (cross-cutting)

- Should consumer-repo discovery (which `nolte/*` repos depend on this package, at which version) be tracked here, or in a separate `consumers.md` / portfolio register?
- Is there a minimum threshold below which a new vocabulary entry should be added directly versus via spec update?
- Does the audience list need explicit re-validation when `claude-shared` introduces a new spec that this repo must conform to (for example a new portfolio-wide gate)?

## Revisit triggers

- A new vocabulary group is added beyond `technical` and `esphome`
- `src/styles/nolte-styles/` graduates from placeholder to shipping rule YAML
- The release pipeline moves off `nolte/gh-plumbing` reusable workflows
- A consuming repository is identified outside `nolte/*` and adopted as an explicit audience
- A regulated data class is introduced (currently none — pure FOSS vocabulary content)
- A new Claude Code skill or agent claims this repo as a write target
