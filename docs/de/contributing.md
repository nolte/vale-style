# Mitwirken

Die Pflegeregeln für dieses Paket sind in der [Spec „Vocabulary and Style Curation“](https://github.com/nolte/vale-style/blob/main/spec/vocabulary-and-style-curation/en.md) festgehalten. Diese Seite ist das Kochbuch auf Aufgaben-Ebene — die Begründung hinter diesen Schritten steht in der Spec.

## Einen Begriff zu einem Vokabular hinzufügen

1. Wähle die engste passende Gruppe: projektübergreifende Begriffe gehören in `src/styles/config/vocabularies/technical/accept.txt`; ESPHome-spezifische Hardware, GPIO-Pins oder YAML-Schlüssel in `src/styles/config/vocabularies/esphome/accept.txt`. Lege eine neue Gruppe nur an, wenn eine klar abgegrenzte Domäne es rechtfertigt — und aktualisiere im selben PR `docs/en/vocabularies.md`, `docs/de/vocabularies.md` und die Liste in der `README.md`.
2. Bestätige vor dem Hinzufügen, dass ein aktuelles englisches Wörterbuch den Begriff weiterhin markiert. Wörter, die Vales Basis-Wörterbuch bereits kennt, gehören nicht in `accept.txt`.
3. Füge den Begriff in einer eigenen Zeile hinzu. Bevorzuge eine **Regex, die Varianten zusammenfasst** (`LEDs?`, `[Hh]ostnames?`, `GPIO(0[0-9]|[1-3][0-9])`) gegenüber mehreren wörtlichen Einträgen.
4. Halte Einträge case-sensitiv, sofern der Begriff nicht wirklich jede Schreibweise treffen soll — das Vokabular dient zugleich als sanfter Hinweis auf die korrekte Schreibweise.
5. `accept.txt`-Dateien enthalten ausschließlich Regex-Einträge: keine Leerzeilen, keine Kommentarzeilen, weil Vale jede Zeile als Muster behandelt.

## Eine Vale-Regel hinzufügen

Das Verzeichnis `src/styles/nolte-styles/` ist die Heimat für eigene Vale-Regel-YAMLs. Die mitgelieferte `src/.vale.ini` führt `nolte-styles` bereits in `BasedOnStyles`, daher:

- Lege eine neue Regeldatei unter `src/styles/nolte-styles/<RuleName>.yml` ab (gemäß [Vales Regelformat](https://vale.sh/docs/topics/styles/)).
- Eine Änderung an `src/.vale.ini` ist nicht nötig — neue Regeln werden im nächsten Release automatisch aktiv.
- Heute enthält das Verzeichnis nur eine `.keep`-Datei; die erste echte Regel bekommt vor dem Landen ihre eigene Spec unter `spec/`.

## Änderungen lokal testen

Baue das Paket-Zip genauso wie CI und richte dann ein Testprojekt auf das lokale Zip aus:

```sh
mkdir -p ./build/nolte-styles
cp -R src/* ./build/nolte-styles/
cp -R src/.vale.ini ./build/nolte-styles/.vale.ini
(cd ./build && zip -r nolte-styles.zip nolte-styles)
```

Das explizite zweite `cp` ist erforderlich: `cp -R src/*` schließt die mit Punkt beginnende `.vale.ini` nicht ein.

Ersetze in einem Consumer-Projekt vorübergehend die `Packages =`-URL durch den lokalen Pfad:

```ini
Packages = ./path/to/build/nolte-styles.zip
```

Führe dann `vale sync && vale .` gegen ein Beispiel-Dokument aus, das deinen neuen Begriff oder deine neue Regel abdeckt.

Dieses Repo nutzt zudem seine eigenen Assets per Dogfooding: die `.vale.ini` im Wurzelverzeichnis zeigt auf `src/styles` und aktiviert `technical, esphome`, sodass `vale .` im Repo-Wurzelverzeichnis das eigene Markdown des Pakets mit dessen eigenen Vokabularen lintet.

## Pre-commit

Installiere die Hooks einmalig:

```sh
pip install -r requirements-dev.txt
pre-commit install
```

Sie führen `check-yaml`, `end-of-file-fixer` und `trailing-whitespace` aus — dieselben Hooks, die CI über den wiederverwendbaren Pre-commit-Workflow aus `nolte/gh-plumbing` ausführt. Überspringe sie nicht.

## Release-Ablauf

Releases werden über GitHub Releases veröffentlicht:

1. Release-Drafter pflegt einen Release-Entwurf auf `main`, während PRs gemergt werden.
2. Das Veröffentlichen des Entwurfs löst `.github/workflows/release-cd-archive.yml` aus, das `nolte-styles.zip` baut und an das Release anhängt.
3. `release-cd-deliver-docs.yml` veröffentlicht die aktualisierte MkDocs-Seite.

Es gibt keine Versionsdatei im Repo — der Release-Tag *ist* die Version.
