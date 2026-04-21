# Contributing

## Adding a term to a vocabulary

1. Pick the right group: project-agnostic terms go in `src/styles/config/vocabularies/technical/accept.txt`; ESPHome-specific words in `src/styles/config/vocabularies/esphome/accept.txt`.
2. Add the term on its own line. Prefer a **regex that collapses variants** (`LEDs?`, `[Hh]ostnames?`) over multiple literal entries.
3. Keep entries case-sensitive unless the term really should match any casing — the vocabulary doubles as a nudge toward the correct spelling.
4. Keep lines sorted only when it helps readability; neither the build nor Vale cares about order.

## Testing changes locally

Build the package zip the same way CI does, then point a test project at the local zip:

```sh
mkdir -p ./build/nolte-styles
cp -R src/* ./build/nolte-styles/
cp -R src/.vale.ini ./build/nolte-styles/.vale.ini
(cd ./build && zip -r nolte-styles.zip nolte-styles)
```

In a consumer project, temporarily replace the `Packages =` URL with the local path:

```ini
Packages = ./path/to/build/nolte-styles.zip
```

Then run `vale sync && vale .` against a sample doc that exercises your new term.

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
