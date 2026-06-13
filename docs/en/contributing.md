# Contributing

The maintenance rules for this package are codified in the [Vocabulary and Style Curation spec](https://github.com/nolte/vale-style/blob/main/spec/vocabulary-and-style-curation/en.md). This page is the task-level cookbook — read the spec for the reasoning behind these steps.

## Adding a term to a vocabulary

1. Pick the narrowest group that fits: project-agnostic terms go in `src/styles/config/vocabularies/technical/accept.txt`; ESPHome-specific hardware, GPIO pins, or YAML keys go in `src/styles/config/vocabularies/esphome/accept.txt`. Introduce a new group only when a clearly bounded domain warrants it — and in the same PR update `docs/en/vocabularies.md`, `docs/de/vocabularies.md`, and the `README.md` list.
2. Before adding a term, confirm a current English dictionary still flags it. Words Vale's base dictionary already knows don't belong in `accept.txt`.
3. Add the term on its own line. Prefer a **regex that collapses variants** (`LEDs?`, `[Hh]ostnames?`, `GPIO(0[0-9]|[1-3][0-9])`) over multiple literal entries.
4. Keep entries case-sensitive unless the term really should match any casing — the vocabulary doubles as a nudge toward the correct spelling.
5. `accept.txt` files hold regex entries only: no blank lines, no comment lines, because Vale treats every line as a pattern.

## Adding a Vale rule

The directory `src/styles/nolte-styles/` is the home for custom Vale rule YAMLs. The shipped `src/.vale.ini` already lists `nolte-styles` in `BasedOnStyles`, so:

- Drop a new rule file at `src/styles/nolte-styles/<RuleName>.yml` (following [Vale's rule format](https://vale.sh/docs/topics/styles/)).
- No edit to `src/.vale.ini` is required — new rules activate automatically in the next release.
- Today the directory contains only a `.keep` file; the first real rule earns its own spec under `spec/` before landing.

## Testing changes locally

Build the package zip the same way CI does, then point a test project at the local zip:

```sh
mkdir -p ./build/nolte-styles
cp -R src/* ./build/nolte-styles/
cp -R src/.vale.ini ./build/nolte-styles/.vale.ini
(cd ./build && zip -r nolte-styles.zip nolte-styles)
```

The explicit second `cp` is required: `cp -R src/*` does not include the leading-dot `.vale.ini`.

In a consumer project, temporarily replace the `Packages =` URL with the local path:

```ini
Packages = ./path/to/build/nolte-styles.zip
```

Then run `vale sync && vale .` against a sample doc that exercises your new term or rule.

This repo also dogfoods its own assets: the root `.vale.ini` points at `src/styles` and activates `technical, esphome`, so `vale .` at the repo root lints this package's own Markdown using its own vocabularies.

## Pre-commit

Install the hooks once:

```sh
pip install -r requirements-dev.txt
pre-commit install
```

They run `check-yaml`, `end-of-file-fixer`, and `trailing-whitespace` — the same hooks CI runs via the reusable `nolte/gh-plumbing` pre-commit workflow. Don't skip them.

## Release flow

Releases are cut through GitHub Releases:

1. Release-drafter maintains a draft release on `main` as PRs merge.
2. Publishing the draft triggers `.github/workflows/release-cd-archive.yml`, which builds `nolte-styles.zip` and attaches it to the release.
3. `release-cd-deliver-docs.yml` publishes the updated MkDocs site.

There is no version file in the repo — the release tag *is* the version.
