# Vocabularies

The package ships two vocabulary groups. Consumers opt in per group via the `Vocab` directive in their own `.vale.ini`:

```ini
Vocab = technical
```

or, for repos that also document ESPHome:

```ini
Vocab = technical, esphome
```

Vale loads each listed group from `styles/config/vocabularies/<name>/accept.txt` inside the unpacked package. The shipped `.vale.ini` inside the archive sets `Vocab = technical` as a minimal baseline; anything beyond that is opt-in.

## `technical`

The default vocabulary for most repos — a curated, steadily growing list of terms that a plain English dictionary would otherwise flag as misspellings. The examples below are representative, not exhaustive; the authoritative list is [`technical/accept.txt`](https://github.com/nolte/vale-style/blob/main/src/styles/config/vocabularies/technical/accept.txt) in the repo. It clusters into a handful of loose families:

- **Tools, products, and brands** — `Ansible`, `ESPHome`, `MkDocs`, `Renovate`, `Trivy`, `Probot`, `Vite`, `Vue`, `Tauri`, `Bun`, `ESLint`, `mypy`, `Pyright`, `Vitest`, `npm`, `Tailwind`, `Mantine`, `Figma`, `Jira`, `Supabase`, `Vercel`, `Claude`, `Anthropic`, `gh-plumbing`, `nolte`.
- **Software-engineering, CI/CD, and security terms** — `CI`, `CLIs`, `PRs`, `MRs`, `ADRs`, `Dockerfiles`, `docstrings`, `frontmatter`, `runbooks`, `hotfixes`, `automerge`, `rebase`, `cron`, `lockfiles`, `monorepos`, `worktrees`, `devcontainer`, `CVEs`, `GHSAs`, `SHAs`, `attestation`, `idempotency`, `typecheck`.
- **Naming, lifecycle, and workflow words** — `namespaced`, `dogfooding`, `onboarding`, `rollout`, `vendoring`, `toolchain`, `subprojects`, `triages`, `dispatchable`, `invocable`, `auditable`, `overridable`, `operationalize`, `scaffold`, `retarget`, `autofix`, `autolink`, `bikeshedding`.
- **Proper names from the writing and accessibility domains** — surnames and authorities cited in readability, editorial, and a11y specs: `Flesch`, `Kincaid`, `Strunk`, `Zinsser`, `Kissane`, `Matuschak`, `Carliner`, plus colour-vision terms like `protan`, `deutan`, `tritan`.
- **Shell and runtime shorthands dictionaries reject** — `dotfile`, `untrusted`, `env`, `config`, `repo`, `cwd`, `stderr`, `stdout`, `venv`, `gitignored`, `untracked`, `unversioned`, `greppable`, `skimmable`, `READMEs`, `PDFs`, `NFRs`.

## `esphome`

ESPHome-specific terms. Opt-in: activate alongside `technical` when your docs cover ESPHome device configuration.

- **Hardware identifiers** — `ESP8285`, `HLW8012`, `SP111`, `NOUS`, `A1T`, `Gosund`.
- **GPIO pins** — the regex `GPIO(0[0-9]|[1-3][0-9])` accepts any zero-padded two-digit pin name from `GPIO00` through `GPIO39`, so ESP8266 and ESP32 pin references both lint clean. Bare `GPIO` is accepted separately.
- **YAML config keys** — `baud_rate`, `status_led`, `restore_mode`, `restore_from_flash`, `early_pin_init`, `turn_on_action`, `turn_off_action`.
- **Domain words** — `automations`, `Datetime`, `dBm`, `hostname`, `hostnames`, `LED`, `LEDs`.

## How entries are matched

Each line in `accept.txt` is a **regex**, not a literal string. This is a Vale convention — take advantage of it to collapse related forms into one entry instead of listing every variant.

| Entry | Matches |
| --- | --- |
| `ESPHome` | `ESPHome` |
| `[Aa]llowlist` | `allowlist`, `Allowlist` |
| `[hH]ostnames?` | `hostname`, `hostnames`, `Hostname`, `Hostnames` |
| `LEDs?` | `LED`, `LEDs` |
| `GPIO(0[0-9]|[1-3][0-9])` | `GPIO00`–`GPIO39` |

Keep entries **case-sensitive by default**: write `[Aa]llowlist` rather than `(?i)allowlist`, so the vocabulary still flags unintended cross-case variants. For product or brand names, do not use a bracket-class entry at all — use the canonical casing the upstream publishes (`MkDocs`, `Probot`, `Claude`, `npm`, `mypy`, `Vitest`, `Pyright`) so off-brand casings in prose stay flagged.

## Keeping the glossary in sync

Every term a vocabulary accepts is defined on the [Glossary](glossary.md) page, in both English and German. A coverage gate enforces this: `scripts/check_glossary_coverage.py` (run via `task glossary:check`) expands each `accept.txt` regex to the forms it accepts and fails if any is missing from `docs/en/glossary.md` or `docs/de/glossary.md`. The check runs as a pre-commit hook, so a pull request that adds a term without defining it is caught before merge.

To add a term:

1. Add the regex entry to the right `accept.txt` group.
2. Run `task glossary:stubs` to scaffold a `TODO` placeholder for the new term in both glossary files.
3. Replace each placeholder with a real definition — or a short placement note for a brand — and move it into the matching subsection.
4. Run `task glossary:check` until it passes.

A few accepted forms are documented inside a sibling entry's definition (for example `severities` under `severity`) or are patterns rather than single lemmas (the `GPIO(0[0-9]|[1-3][0-9])` pin range). Those are recorded in `scripts/glossary_aliases.yml` instead of getting their own glossary line.

See the [Vocabulary and Style Curation spec](https://github.com/nolte/vale-style/blob/main/spec/vocabulary-and-style-curation/en.md) for the full maintenance rules this package follows.
