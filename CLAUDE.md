# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo produces

A single release artifact, `nolte-styles.zip`, that downstream projects consume as a Vale `Packages` entry. There is no application code — the "build" just stages `src/` into `./build/nolte-styles/` (including `src/.vale.ini`) and zips it. Every change here ultimately flows out through a GitHub Release.

## Layout that matters

- `src/.vale.ini` — the `.vale.ini` that ships *inside* the zip. `StylesPath = styles` and `Vocab = technical` are resolved relative to the consumer's unpacked package, not this repo.
- `/.vale.ini` (repo root) — dogfoods the shipped assets: `StylesPath = src/styles`, `Vocab = technical, esphome`. `task test` (`vale .`) lints this repo's own Markdown through the same vocabularies consumers get from the zip. Scope blocks exempt `CLAUDE.md`, `spec/README.md`, `spec/**/de.md`, and `docs/de/**` from `Vale.Spelling` (the German docs aren't spell-checked against the English dictionary).
- `src/styles/config/vocabularies/<group>/accept.txt` — the actual vocabularies. One entry per line; Vale treats entries as regex, so patterns like `[Pp]robot` or `LEDs?` are intentional and expand both cases/forms. Existing groups: `technical`, `esphome`.
- `src/styles/nolte-styles/` — placeholder for a future custom Vale style (currently only `.keep`). `src/.vale.ini` already references `nolte-styles` in `BasedOnStyles`, so adding rule YAML here will light up automatically in the next release.
- `docs/{en,de}/glossary.md` — every term any `accept.txt` accepts is defined here, in both languages. `scripts/check_glossary_coverage.py` (`task glossary:check`, also a pre-commit hook) expands each regex entry to its accepted forms and fails on any term missing from either glossary, so a vocabulary term can't ship undefined. Hard cases — variants folded into a sibling's definition, or non-lemma patterns like the GPIO pin range — are recorded in `scripts/glossary_aliases.yml`. To add a term: edit `accept.txt`, run `task glossary:stubs`, fill the `TODO` in both files. See the [curation spec](spec/vocabulary-and-style-curation/en.md).

## Task entry points

`Taskfile.yml` wraps the canonical local commands:

- `task lint` — pre-commit across the tree (includes the glossary-coverage gate)
- `task test` — `vale .` against this repo's own Markdown
- `task glossary:check` — fail if any `accept.txt` term lacks a glossary entry (EN and DE)
- `task glossary:stubs` — scaffold `TODO` glossary stubs for uncovered terms
- `task docs` — `mkdocs build --strict`
- `task docs:serve` — live-reload MkDocs preview
- `task build` — stages `src/` into `./build/nolte-styles/` and zips it

Prefer the Taskfile targets over the raw commands; CI and local runs stay in sync that way.

## Build the archive locally

`task build` is the shorthand. Raw form for reference (matches `.github/workflows/release-cd-archive.yml`):

```sh
mkdir -p ./build/nolte-styles
cp -R src/* ./build/nolte-styles/
cp -R src/.vale.ini ./build/nolte-styles/.vale.ini
(cd ./build && zip -r nolte-styles.zip nolte-styles)
```

Note the explicit second `cp` for `.vale.ini` — `cp -R src/*` misses dotfiles. The subshell is deliberate so the working directory stays at the repo root afterwards.

## Specs live under `spec/`

Engineering specs — scope rules for vocabularies, curation process, acceptance criteria — live under `spec/<slug>/<lang>.md` with EN as canonical and DE as translation. Start at `spec/README.md` for the current index. When you change behaviour that a spec describes, update the canonical EN version and keep translations structurally in sync (same headings, same requirement bullets).

## Docs site

MkDocs Material, bilingual via `mkdocs-static-i18n` (`docs_structure: folder`). English is the default; pages live under `docs/en/` and the German translations under `docs/de/`, with `docs/css/` shared language-neutrally. Both `docs/en/index.md` and `docs/de/index.md` pull fragments from `README.md` via `include-markdown` (path `../../README.md`) between the `<!--intro-start-->`, `<!--archive-structure-start-->`, `<!--usage-start-->` marker pairs — those fragments stay English in both languages (they carry code), so keep the markers intact. Nav labels are translated in `mkdocs.yml` under the `i18n` plugin's `nav_translations`. When you add or rename a page, mirror it in both language trees.

```sh
pip install -r requirements-dev.txt
mkdocs serve
```

## CI and release flow

All heavy lifting is delegated to reusable workflows in `nolte/gh-plumbing` (all pinned to `v1.1.12`):

- `build-static-tests.yaml` — pre-commit, Trivy, chain-bench on every push.
- `spelling.yaml` — runs Vale against the PR using this package's own vocab.
- `release-drafter.yml` + `release-cd-archive.yml` — drafting a GitHub Release triggers the zip build and attaches `nolte-styles.zip` to the release. Version bumps happen by publishing a release, not by editing a file.
- `release-cd-deliver-docs.yml` — publishes the MkDocs site.
- `release-cd-refresh-master.yml` / `automerge.yaml` — branch hygiene; `develop` is the default working branch, `main` is the release target.

Renovate config extends the shared `nolte/gh-plumbing` common preset, so dependency PRs come in grouped (`group:all`).

## Pre-commit

`pre-commit install` once; hooks are minimal (`check-yaml`, `end-of-file-fixer`, `trailing-whitespace` for `.md`). Don't skip them — CI re-runs the same hooks via the reusable pre-commit workflow.
