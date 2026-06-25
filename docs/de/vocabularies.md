# Vokabulare

Das Paket liefert zwei Vokabular-Gruppen. Consumer aktivieren sie pro Gruppe über die `Vocab`-Direktive in ihrer eigenen `.vale.ini`:

```ini
Vocab = technical
```

oder, für Repos, die zusätzlich ESPHome dokumentieren:

```ini
Vocab = technical, esphome
```

Vale lädt jede aufgeführte Gruppe aus `styles/config/vocabularies/<name>/accept.txt` innerhalb des entpackten Pakets. Die im Archiv mitgelieferte `.vale.ini` setzt `Vocab = technical` als minimale Grundlinie; alles darüber hinaus ist optional.

## `technical`

Das Standard-Vokabular für die meisten Repos — eine kuratierte, stetig wachsende Liste von Begriffen, die ein gewöhnliches englisches Wörterbuch sonst als Tippfehler markieren würde. Die folgenden Beispiele sind repräsentativ, nicht vollständig; maßgeblich ist die Datei [`technical/accept.txt`](https://github.com/nolte/vale-style/blob/main/src/styles/config/vocabularies/technical/accept.txt) im Repo. Sie gliedert sich in einige lose Familien:

- **Werkzeuge, Produkte und Marken** — `Ansible`, `ESPHome`, `MkDocs`, `Renovate`, `Trivy`, `Probot`, `Vite`, `Vue`, `Tauri`, `Bun`, `ESLint`, `mypy`, `Pyright`, `Vitest`, `npm`, `Tailwind`, `Mantine`, `Figma`, `Jira`, `Supabase`, `Vercel`, `Claude`, `Anthropic`, `gh-plumbing`, `nolte`.
- **Begriffe aus Software-Engineering, CI/CD und Security** — `CI`, `CLIs`, `PRs`, `MRs`, `ADRs`, `Dockerfiles`, `docstrings`, `frontmatter`, `runbooks`, `hotfixes`, `automerge`, `rebase`, `cron`, `lockfiles`, `monorepos`, `worktrees`, `devcontainer`, `CVEs`, `GHSAs`, `SHAs`, `attestation`, `idempotency`, `typecheck`.
- **Begriffe zu Benennung, Lebenszyklus und Workflow** — `namespaced`, `dogfooding`, `onboarding`, `rollout`, `vendoring`, `toolchain`, `subprojects`, `triages`, `dispatchable`, `invocable`, `auditable`, `overridable`, `operationalize`, `scaffold`, `retarget`, `autofix`, `autolink`, `bikeshedding`.
- **Eigennamen aus den Bereichen Schreiben und Barrierefreiheit** — Nachnamen und Autoritäten, die in Specs zu Lesbarkeit, Lektorat und Accessibility zitiert werden: `Flesch`, `Kincaid`, `Strunk`, `Zinsser`, `Kissane`, `Matuschak`, `Carliner`, dazu Begriffe der Farbwahrnehmung wie `protan`, `deutan`, `tritan`.
- **Shell- und Runtime-Kürzel, die Wörterbücher ablehnen** — `dotfile`, `untrusted`, `env`, `config`, `repo`, `cwd`, `stderr`, `stdout`, `venv`, `gitignored`, `untracked`, `unversioned`, `greppable`, `skimmable`, `READMEs`, `PDFs`, `NFRs`.

## `esphome`

ESPHome-spezifische Begriffe. Optional: zusammen mit `technical` aktivieren, wenn deine Doku die ESPHome-Gerätekonfiguration behandelt.

- **Hardware-Bezeichner** — `ESP8285`, `HLW8012`, `SP111`, `NOUS`, `A1T`, `Gosund`.
- **GPIO-Pins** — die Regex `GPIO(0[0-9]|[1-3][0-9])` akzeptiert jeden zweistelligen Pin-Namen mit führender Null von `GPIO00` bis `GPIO39`, sodass sowohl ESP8266- als auch ESP32-Pin-Referenzen sauber durch den Lint laufen. Das bloße `GPIO` wird separat akzeptiert.
- **YAML-Konfigurationsschlüssel** — `baud_rate`, `status_led`, `restore_mode`, `restore_from_flash`, `early_pin_init`, `turn_on_action`, `turn_off_action`.
- **Domänenbegriffe** — `automations`, `Datetime`, `dBm`, `hostname`, `hostnames`, `LED`, `LEDs`.

## Wie Einträge gematcht werden

Jede Zeile in `accept.txt` ist eine **Regex**, kein wörtlicher String. Das ist eine Vale-Konvention — nutze sie, um verwandte Formen in einem Eintrag zusammenzufassen, statt jede Variante einzeln aufzulisten.

| Eintrag | Trifft auf |
| --- | --- |
| `ESPHome` | `ESPHome` |
| `[Aa]llowlist` | `allowlist`, `Allowlist` |
| `[hH]ostnames?` | `hostname`, `hostnames`, `Hostname`, `Hostnames` |
| `LEDs?` | `LED`, `LEDs` |
| `GPIO(0[0-9]|[1-3][0-9])` | `GPIO00`–`GPIO39` |

Halte Einträge **standardmäßig case-sensitiv**: schreibe `[Aa]llowlist` statt `(?i)allowlist`, damit das Vokabular ungewollte Schreibweisen in anderer Groß-/Kleinschreibung weiterhin markiert. Verwende für Produkt- oder Markennamen gar keine Bracket-Klasse — nutze die kanonische Schreibweise des jeweiligen Herstellers (`MkDocs`, `Probot`, `Claude`, `npm`, `mypy`, `Vitest`, `Pyright`), damit abweichende Schreibweisen im Text markiert bleiben.

## Das Glossar synchron halten

Jeder Begriff, den ein Vokabular akzeptiert, ist auf der Seite [Glossar](glossary.md) definiert — auf Englisch und auf Deutsch. Ein Coverage-Gate erzwingt das: `scripts/check_glossary_coverage.py` (über `task glossary:check`) expandiert jede `accept.txt`-Regex zu den Formen, die sie akzeptiert, und schlägt fehl, wenn eine davon in `docs/en/glossary.md` oder `docs/de/glossary.md` fehlt. Der Check läuft als pre-commit-Hook, sodass ein Pull Request, der einen Begriff hinzufügt, ohne ihn zu definieren, vor dem Merge auffällt.

Um einen Begriff hinzuzufügen:

1. Füge den Regex-Eintrag der richtigen `accept.txt`-Gruppe hinzu.
2. Führe `task glossary:stubs` aus, um in beiden Glossar-Dateien einen `TODO`-Platzhalter für den neuen Begriff zu gerüsten.
3. Ersetze jeden Platzhalter durch eine echte Definition — oder einen kurzen Einordnungssatz bei einer Marke — und verschiebe ihn in die passende Subsektion.
4. Führe `task glossary:check` aus, bis er erfolgreich durchläuft.

Ein paar akzeptierte Formen sind in der Definition eines Geschwister-Eintrags dokumentiert (zum Beispiel `severities` unter `severity`) oder sind Muster statt einzelner Lemmata (der Pin-Bereich `GPIO(0[0-9]|[1-3][0-9])`). Diese werden in `scripts/glossary_aliases.yml` festgehalten, statt eine eigene Glossar-Zeile zu bekommen.

Die vollständigen Pflegeregeln, denen dieses Paket folgt, stehen in der [Spec „Vocabulary and Style Curation“](https://github.com/nolte/vale-style/blob/main/spec/vocabulary-and-style-curation/en.md).
