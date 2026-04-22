# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo produces

A single release artifact, `nolte-styles.zip`, that downstream projects consume as a Vale `Packages` entry. There is no application code — the "build" just stages `src/` into `./build/nolte-styles/` (including `src/.vale.ini`) and zips it. Every change here ultimately flows out through a GitHub Release.

## Layout that matters

- `src/.vale.ini` — the `.vale.ini` that ships *inside* the zip. `StylesPath = styles` and `Vocab = technical` are resolved relative to the consumer's unpacked package, not this repo.
- `/.vale.ini` (repo root) — only used when linting `*.md` in this repo itself; points at `.github/styles` (currently empty).
- `src/styles/config/vocabularies/<group>/accept.txt` — the actual vocabularies. One entry per line; Vale treats entries as regex, so patterns like `[Pp]robot` or `LEDs?` are intentional and expand both cases/forms. Existing groups: `technical`, `esphome`.
- `src/styles/nolte-styles/` — placeholder for a future custom Vale style (currently only `.keep`). `src/.vale.ini` already references `nolte-styles` in `BasedOnStyles`, so adding rule YAML here will light up automatically in the next release.

## Build the archive locally

```sh
mkdir -p ./build/nolte-styles
cp -R src/* ./build/nolte-styles/
cp -R src/.vale.ini ./build/nolte-styles/.vale.ini
(cd ./build && zip -r nolte-styles.zip nolte-styles)
```

Note the explicit second `cp` for `.vale.ini` — `cp -R src/*` misses dotfiles. The subshell is deliberate so the working directory stays at the repo root afterwards. The release workflow (`.github/workflows/release-cd-archive.yml`) does both copies.

## Specs live under `spec/`

Engineering specs — scope rules for vocabularies, curation process, acceptance criteria — live under `spec/<slug>/<lang>.md` with EN as canonical and DE as translation. Start at `spec/README.md` for the current index. When you change behaviour that a spec describes, update the canonical EN version and keep translations structurally in sync (same headings, same requirement bullets).

## Docs site

MkDocs Material, sourced from `docs/`. `docs/index.md` pulls fragments from `README.md` via `include-markdown` between `<!--intro-start-->`, `<!--archive-structure-start-->`, `<!--usage-start-->` marker pairs — edits to those README sections propagate to the site, so keep the markers intact.

```sh
pip install -r requirements-dev.txt
mkdocs serve
```

## CI and release flow

All heavy lifting is delegated to reusable workflows in `nolte/gh-plumbing` (pinned to `v1.1.12`, except `spelling.yaml` which tracks `develop`):

- `build-static-tests.yaml` — pre-commit, Trivy, chain-bench on every push.
- `spelling.yaml` — runs Vale against the PR using this package's own vocab.
- `release-drafter.yml` + `release-cd-archive.yml` — drafting a GitHub Release triggers the zip build and attaches `nolte-styles.zip` to the release. Version bumps happen by publishing a release, not by editing a file.
- `release-cd-deliver-docs.yml` — publishes the MkDocs site.
- `release-cd-refresh-master.yml` / `automerge.yaml` — branch hygiene; `develop` is the default working branch, `main` is the release target.

Renovate config extends the shared `nolte/gh-plumbing` common preset, so dependency PRs come in grouped (`group:all`).

## Pre-commit

`pre-commit install` once; hooks are minimal (`check-yaml`, `end-of-file-fixer`, `trailing-whitespace` for `.md`). Don't skip them — CI re-runs the same hooks via the reusable pre-commit workflow.
