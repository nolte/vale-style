# Pflege von Vocabularies und Styles

Status: Entwurf

## Kontext

Dieses Repository erzeugt genau ein Artefakt, `nolte-styles.zip`, das nachgelagerte Projekte als Vale-`Packages`-Eintrag konsumieren. Jede Änderung an einem Vocabulary oder Style wirkt sich beim nächsten Release auf jedes konsumierende Repo aus. Ohne dokumentierten Pflegeprozess treten drei wiederkehrende Probleme auf:

- Einträge sammeln sich stückweise, überschneiden sich zwischen Gruppen oder überdecken echte Tippfehler, die Vale melden sollte.
- Die Vocabulary-Gruppen auf der Platte driften gegen die Beschreibung in `README.md` und `docs/vocabularies.md` — so geschehen, als `claude-shared` in der Doku auftauchte, obwohl es bereits wieder in `technical` aufgegangen war.
- Das Verzeichnis `src/styles/nolte-styles/` ist über `BasedOnStyles` bereits eingebunden, enthält aber nur eine `.keep`-Datei; unklar bleibt, unter welchen Bedingungen die erste echte Regel dort landen darf.

Diese Spec definiert den Pflegeprozess, damit das ausgelieferte Paket über alle Consumer hinweg ein konsistentes Lint-Signal erzeugt und damit die Dokumentation in diesem Repo stets zum veröffentlichten Artefakt passt.

## Ziele

- Jeder Vocabulary-Gruppe einen eindeutigen, dokumentierten Scope geben, damit jeder Begriff genau eine richtige Heimat hat.
- Eintrags-Konventionen (Regex-Form, Groß-/Kleinschreibung, Zusammenfassen verwandter Formen) festhalten, die ein Reviewer ohne Raten prüfen kann.
- Den Stand auf der Platte, `README.md` und `docs/vocabularies.md` strukturell synchron halten — eine Gruppe existiert in allen drei Quellen oder in keiner.
- Beschreiben, wie eigene Regel-YAMLs unter `src/styles/nolte-styles/` landen können, ohne dass weitere Schema-Änderungen nötig werden.
- Das Paket im eigenen Repo dogfooden, damit Vocabulary-Regressionen lokal auffallen, bevor ein Release gezogen wird.

## Nicht-Ziele

- Schreiben konkreter Vale-Regel-YAMLs. Sobald die erste Regel landet, bekommt sie eine eigene Spec.
- Vorgaben für Consumer-seitige `.vale.ini`-Einstellungen wie `MinAlertLevel` oder `IgnoredScopes`.
- Automatisieren der Release-Kadenz. Das Veröffentlichen eines GitHub-Releases löst bereits den bestehenden Archiv-Workflow aus; diese Spec ändert diesen Ablauf nicht.
- Definition von Vocabularies für fremde Domänen. Neue Gruppen entstehen über diesen Prozess und werden nicht hier aufgezählt.

## Anforderungen

- **MUSS [MUST]**
  - Jede Vocabulary-Gruppe MUSS unter `src/styles/config/vocabularies/<gruppe>/accept.txt` liegen, ein Eintrag pro Zeile.
  - Jeder Eintrag MUSS ein gültiger Vale-Regex sein. Literale Strings sind gültige Regex und damit erlaubt.
  - Einträge MÜSSEN standardmäßig groß-/kleinschreibungssensitiv sein (z. B. `[Pp]robot`, nicht `(?i)probot`), damit das Vocabulary falsche Schreibungen weiterhin moniert.
  - Jeder Commit, der eine Vocabulary-Gruppe hinzufügt oder entfernt, MUSS im selben Commit `docs/vocabularies.md` und den Abschnitt „Available vocabularies" in `README.md` aktualisieren.
  - `src/.vale.ini` (im Archiv ausgeliefert) und die Repo-Root-`.vale.ini` (für Dogfooding) DÜRFEN nur Gruppen referenzieren, die auf der Platte existieren.
  - `accept.txt`-Dateien DÜRFEN ausschließlich Regex-Einträge enthalten — keine Leerzeilen, keine Kommentarzeilen —, weil Vale jede Zeile als Muster interpretiert.
- **SOLLTE [SHOULD]**
  - Verwandte Formen SOLLTEN in einem einzigen Regex-Eintrag zusammengefasst werden (`LEDs?`, `[Hh]ostnames?`, `CLIs?`) statt einzeln gelistet.
  - Vor dem Hinzufügen eines Begriffs SOLLTE der Autor prüfen, ob ein aktuelles englisches Wörterbuch den Begriff noch als Tippfehler meldet — Begriffe, die Vales Basiswörterbuch bereits kennt, gehören nicht in eine `accept.txt`.
  - Ein Begriff SOLLTE in die engstmögliche passende Gruppe: `technical` ist der Default für projektübergreifende Terminologie, `esphome` für ESPHome-spezifische Hardware- und Config-Begriffe; eine neue Gruppe SOLLTE nur entstehen, wenn eine klar umrissene Domäne sie rechtfertigt.
  - Die Repo-Root-`.vale.ini` SOLLTE dieselben Vocabularies aktivieren, die sie ausliefert, damit lokale `vale .`-Läufe die Paket-Assets selbst ausüben.
  - Das Entfernen eines Begriffs aus einem Vocabulary SOLLTE von einem kurzen Check bekannter Consumer-Repos begleitet werden, um überraschende Lint-Fehler beim nächsten `vale sync` zu vermeiden.
- **KANN [MAY]**
  - Einträge KÖNNEN innerhalb einer Gruppe alphabetisch sortiert werden, wenn das die Review erleichtert; weder Vale noch der Build hängen von der Reihenfolge ab.
  - Eigene Vale-Regel-YAMLs KÖNNEN unter `src/styles/nolte-styles/` hinzugefügt werden; die ausgelieferte `src/.vale.ini` listet `nolte-styles` bereits in `BasedOnStyles`, neue Regeln aktivieren sich also automatisch im nächsten Release.
  - Eine neue Vocabulary-Gruppe KANN im selben PR eingeführt werden, der ihren ersten Consumer in der eigenen Doku dieses Repos hinzufügt, um zu zeigen, dass die Gruppe durchgängig ausgeübt wird.

## Akzeptanzkriterien

- [ ] Jede in `src/.vale.ini` und der Repo-Root-`.vale.ini` referenzierte Gruppe existiert als Verzeichnis unter `src/styles/config/vocabularies/`.
- [ ] `docs/vocabularies.md` beschreibt genau die auf der Platte vorhandenen Gruppen — kein überzähliger, kein fehlender Abschnitt.
- [ ] Die Liste „Available vocabularies" in `README.md` nennt dieselben Gruppen, in derselben Reihenfolge, wie `docs/vocabularies.md`.
- [ ] Jede `accept.txt` im Repo enthält ausschließlich nicht-leere Zeilen und keine Kommentare.
- [ ] `vale sync && vale .` läuft im Repo-Root erfolgreich, ausschließlich mit den Vocabularies, die dieses Paket ausliefert.
- [ ] Das über den Abschnitt „Build the archive locally" in `README.md` gebaute Archiv entpackt zur dort dokumentierten Struktur, inklusive `.vale.ini`.
- [ ] Das Hinzufügen einer neuen Regeldatei unter `src/styles/nolte-styles/` erfordert keine Änderung an `src/.vale.ini`.

## Offene Fragen

- Soll alphabetisches Sortieren innerhalb einer `accept.txt` zu einem MUSS werden, damit Diff-Reviews mechanisch laufen?
- Wenn die erste echte `nolte-styles`-Regel hinzukommt: eigene Spec fürs Regel-Autoring oder diese Spec erweitern?
- Ist eine Removal-Policy nötig — etwa ein Grep über bekannte Consumer-Repos vor dem Streichen eines Begriffs — oder reicht das Release-Changelog als Signal?
- Wie wird eine brandneue Vocabulary-Gruppe validiert? Reicht ein einziger Consumer innerhalb der eigenen Doku als Bedarfsnachweis, oder sollte zuerst ein externer Consumer identifiziert sein?
