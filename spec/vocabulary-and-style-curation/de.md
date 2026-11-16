# Pflege von Vocabularies und Styles

Status: Entwurf

## Kontext

Dieses Repository erzeugt genau ein Artefakt, `nolte-styles.zip`, das nachgelagerte Projekte als Vale-`Packages`-Eintrag konsumieren. Jede Änderung an einem Vocabulary oder Style wirkt sich beim nächsten Release auf jedes konsumierende Repo aus. Ohne dokumentierten Pflegeprozess treten diese wiederkehrenden Probleme auf:

- Einträge sammeln sich stückweise, überschneiden sich zwischen Gruppen oder überdecken echte Tippfehler, die Vale melden sollte.
- Die Vocabulary-Gruppen auf der Platte driften gegen die Beschreibung in `README.md` und `docs/vocabularies.md` — so geschehen, als `claude-shared` in der Doku auftauchte, obwohl es bereits wieder in `technical` aufgegangen war.
- Das Verzeichnis `src/styles/nolte-styles/` ist über `BasedOnStyles` bereits eingebunden, enthält aber nur eine `.keep`-Datei; unklar bleibt, unter welchen Bedingungen die erste echte Regel dort landen darf.
- Ein Begriff kann von einem Vocabulary akzeptiert sein, ohne je für Leser definiert zu werden: Das Glossar (`docs/en/glossary.md` und `docs/de/glossary.md`) driftet stillschweigend hinter `accept.txt` her — so geschehen, als in einem PR hinzugefügte Einträge im nächsten nur teilweise abgedeckt wurden.
- Ein Eintrag kann korrekte Prosa in jedem Consumer brechen: Vale macht aus jedem `accept.txt`-Eintrag eine `Vale.Terms`-Ersetzung, die jeden Treffer ohne Beachtung der Groß-/Kleinschreibung meldet, der von der akzeptierten Form abweicht. v0.2.0 lieferte `REST` und `mS` aus, die die gewöhnlichen Wörter „rest" und „ms" meldeten, sowie die kollidierenden Paare `kamerplanter` / `Kamerplanter('?s)?` und `[Tt]odo` / `TODOs?`, bei denen ein Eintrag eine Form meldet, die der andere akzeptiert (nolte/vale-style#40). Dieselbe Ersetzung meldete großgeschriebene Satzanfänge kleingeschriebener Einträge (`cron` meldete „Cron jobs run nightly.") und großgeschriebene gewöhnliche Wörter (`MRs` meldete „Mrs"). Das eigene `vale .` dieses Repos blieb grün, weil seine Doku diese Wörter nie in Prosa verwendet.

Diese Spec definiert den Pflegeprozess, damit das ausgelieferte Paket über alle Consumer hinweg ein konsistentes Lint-Signal erzeugt und damit die Dokumentation in diesem Repo stets zum veröffentlichten Artefakt passt.

## Ziele

- Jeder Vocabulary-Gruppe einen eindeutigen, dokumentierten Scope geben, damit jeder Begriff genau eine richtige Heimat hat.
- Eintrags-Konventionen (Regex-Form, Groß-/Kleinschreibung, Zusammenfassen verwandter Formen) festhalten, die ein Reviewer ohne Raten prüfen kann.
- Den Stand auf der Platte, `README.md` und `docs/vocabularies.md` strukturell synchron halten — eine Gruppe existiert in allen drei Quellen oder in keiner.
- Beschreiben, wie eigene Regel-YAMLs unter `src/styles/nolte-styles/` landen können, ohne dass weitere Schema-Änderungen nötig werden.
- Das Paket im eigenen Repo dogfooden, damit Vocabulary-Regressionen lokal auffallen, bevor ein Release gezogen wird.
- Garantieren, dass jeder akzeptierte Begriff für Leser definiert ist: Jeder `accept.txt`-Eintrag hat in beiden Sprachen einen passenden Glossar-Eintrag, automatisch erzwungen, damit ein Begriff nie undefiniert ausgeliefert wird.
- Garantieren, dass das Akzeptieren eines Begriffs `Vale.Terms` nie korrekte Prosa melden lässt: Kein Eintrag meldet eine Form, die das Vocabulary akzeptiert, und kein Eintrag erzwingt eine Schreibweise bei einem gewöhnlichen englischen Wort, es sei denn, das ist eine festgehaltene Entscheidung.

## Nicht-Ziele

- Schreiben konkreter Vale-Regel-YAMLs. Sobald die erste Regel landet, bekommt sie eine eigene Spec.
- Vorgaben für Consumer-seitige `.vale.ini`-Einstellungen wie `MinAlertLevel` oder `IgnoredScopes`.
- Automatisieren der Release-Kadenz. Das Veröffentlichen eines GitHub-Releases löst bereits den bestehenden Archiv-Workflow aus; diese Spec ändert diesen Ablauf nicht.
- Definition von Vocabularies für fremde Domänen. Neue Gruppen entstehen über diesen Prozess und werden nicht hier aufgezählt.

## Anforderungen

- **MUSS [MUST]**
  - Jede Vocabulary-Gruppe MUSS unter `src/styles/config/vocabularies/<gruppe>/accept.txt` liegen, ein Eintrag pro Zeile.
  - Jeder Eintrag MUSS ein gültiger Vale-Regex sein. Literale Strings sind gültige Regex und damit erlaubt.
  - Einträge MÜSSEN standardmäßig groß-/kleinschreibungssensitiv sein (z. B. `[Aa]llowlist`, nicht `(?i)allowlist`), damit das Vocabulary falsche Schreibungen weiterhin moniert. Ein vorangestelltes `(?i)`-Flag ist nur dort erlaubt, wo der schreibungssensitive Eintrag `Vale.Terms` ein gewöhnliches englisches Wort melden ließe (z. B. `(?i)PRs?`, `(?i)MUSTs`).
  - Einträge für Produkt- oder Markennamen MÜSSEN die vom Hersteller veröffentlichte kanonische Schreibweise verwenden (z. B. `MkDocs`, `Probot`, `Claude`, `Dependabot`, `Vitest`) und DÜRFEN KEINE Klammer-Klasse wie `[Pp]robot` benutzen, weil Klammer-Klassen abweichende Schreibweisen in Prosa stillschweigend akzeptieren. Für generische englische Wörter, deren Anfangsbuchstabe legitim mit der Satzposition variiert, bleiben Klammer-Klassen korrekt (z. B. `[Aa]llowlist`, `[Ff]rontend`), ebenso für ein Projekt, dessen eigener kanonischer Name kleingeschrieben ist, damit der Name trotzdem einen Satz eröffnen kann (z. B. `[Kk]amerplanter('?s)?`, `[Nn]pm`, `[Mm]ypy`).
  - Jeder Eintrag, der sich auf ein Produkt oder eine Marke bezieht, MUSS vor dem Einchecken gegen die kanonische Upstream-Quelle geprüft werden (README, Logo oder offizieller Styleguide des Projekts). Die PR-Beschreibung MUSS die geprüfte Quelle nennen, damit ein Reviewer die Entscheidung nachvollziehen kann; dasselbe gilt für jede Casing-Änderung und jedes Entfernen.
  - Jeder Commit, der eine Vocabulary-Gruppe hinzufügt oder entfernt, MUSS im selben Commit `docs/vocabularies.md` und den Abschnitt „Available vocabularies" in `README.md` aktualisieren.
  - `src/.vale.ini` (im Archiv ausgeliefert) und die Repo-Root-`.vale.ini` (für Dogfooding) DÜRFEN nur Gruppen referenzieren, die auf der Platte existieren.
  - `accept.txt`-Dateien DÜRFEN ausschließlich Regex-Einträge enthalten — keine Leerzeilen, keine Kommentarzeilen —, weil Vale jede Zeile als Muster interpretiert.
  - Jeder Begriff, den irgendeine `accept.txt` akzeptiert, MUSS in `docs/en/glossary.md` und `docs/de/glossary.md` einen passenden Eintrag haben. Da Einträge Regex sind, „passt" ein Glossar-Eintrag, wenn sein lesbares Lemma auf eine der literalen Formen normalisiert, die der Regex akzeptiert (Kleinschreibung, abschließendes Plural- oder Possessiv-`s` zusammengefasst). Ein Lemma zählt nur dann als Glossar-Eintrag, wenn es auf einer Begriffszeile einer Definitionsliste steht (einer Zeile, die am linken Rand beginnt und deren nächste nicht leere Zeile eine `:`-Definition ist) oder im eigens dafür vorgesehenen Abschnitt zu Beugungs- und Possessivformen unter `### Beugungs- und Possessivformen`; ein Begriff, der an anderer Stelle im Fließtext nur erwähnt wird, erfüllt die Abdeckung nicht. Ein Begriff, dessen einzige Dokumentation in die Definition eines Geschwister-Eintrags gefaltet ist (z. B. `severities` unter `severity`), MUSS in `scripts/glossary_aliases.yml` festgehalten werden, damit das Mapping explizit ist; ein Muster-Eintrag, der kein eigenständiges Lemma ist (z. B. ein numerischer Pin-Bereich), DARF nur über einen begründeten Eintrag in der `ignore`-Liste dieser Datei ausgenommen werden.
  - Der Coverage-Check `scripts/check_glossary_coverage.py` (über `task glossary:check`) MUSS vor dem Merge einer Änderung erfolgreich laufen. Er läuft als `local`-pre-commit-Hook und damit auch im CI-pre-commit-Job, sodass ein ohne Glossar-Eintrag hinzugefügter `accept.txt`-Begriff den PR fehlschlagen lässt, statt stillschweigend ausgeliefert zu werden.
  - Eine literale Form, die ein Eintrag akzeptiert, DARF NICHT von `Vale.Terms` der Vocabularies gemeldet werden, die sie akzeptieren. Das gilt für jede Gruppe allein und für alle Gruppen gemeinsam aktiviert, weil ein Consumer jede Kombination aktivieren kann.
  - Ein Eintrag, dessen akzeptierte Form ein reines kleingeschriebenes Wort ist, MUSS [MUST] diese Form auch mit großem Anfangsbuchstaben akzeptieren (`[Cc]ron`, nicht `cron`), weil `Vale.Terms` keinen Satzanfang erkennt und dort „Cron" melden würde. Formen mit gemischter Schreibung oder Unterstrich (`pH`, `arXiv`, `baud_rate`) behalten ihre exakte Schreibweise.
  - Ein Eintrag DARF `Vale.Terms` NICHT die Klein- oder Großschreibung eines gewöhnlichen englischen Worts melden lassen, also eines Worts, das `Vale.Spelling` ohne jedes Vocabulary akzeptiert. Die einzige Ausnahme ist eine erzwungene Schreibweise, die mit einer einzeiligen Begründung in `scripts/vocab_terms_allow.yml` festgehalten ist; ein Allowlist-Eintrag, der kein Wort mehr erzwingt oder keinen existierenden Eintrag nennt, ist selbst ein Verstoß.
  - Der Vale.Terms-Check `scripts/check_vocab_terms.py` (über `task vocab:check`) MUSS vor dem Merge einer Änderung erfolgreich laufen. Er läuft als `local`-pre-commit-Hook `vocab-terms` und damit auch im CI-pre-commit-Job.
- **SOLLTE [SHOULD]**
  - Verwandte Formen SOLLTEN in einem einzigen Regex-Eintrag zusammengefasst werden (`[Hh]ostnames?`, `CLIs?`, `[Aa]gents?`) statt einzeln gelistet, es sei denn, die zusammengefasste Form ließe `Vale.Terms` ein gewöhnliches Wort melden.
  - Vor dem Hinzufügen eines Begriffs SOLLTE der Autor prüfen, ob ein aktuelles englisches Wörterbuch den Begriff noch als Tippfehler meldet — Begriffe, die Vales Basiswörterbuch bereits kennt, gehören nicht in eine `accept.txt`.
  - Ein Begriff SOLLTE in die engstmögliche passende Gruppe: `technical` ist der Default für projektübergreifende Terminologie, `esphome` für ESPHome-spezifische Hardware- und Config-Begriffe; eine neue Gruppe SOLLTE nur entstehen, wenn eine klar umrissene Domäne sie rechtfertigt.
  - Die Repo-Root-`.vale.ini` SOLLTE dieselben Vocabularies aktivieren, die sie ausliefert, damit lokale `vale .`-Läufe die Paket-Assets selbst ausüben.
  - Das Entfernen eines Begriffs aus einem Vocabulary SOLLTE von einem kurzen Check bekannter Consumer-Repos begleitet werden, um überraschende Lint-Fehler beim nächsten `vale sync` zu vermeiden.
  - Ein Eintrag, der den Vale.Terms-Check nicht besteht, SOLLTE mit der engsten wirksamen Abhilfe korrigiert werden, in dieser Reihenfolge: den Eintrag streichen, wenn `Vale.Spelling` seine Formen schon ohne ihn akzeptiert, einschließlich der Possessivform mit `'s`, die Vale sonst nur für Vocabulary-Einträge akzeptiert (`REST` und `REST's` bestehen; `LIX's` nicht, daher bleibt `LIX` als `(?i)LIX`); nur die Form behalten, die akzeptiert werden muss (den Plural `LEDs`, da `LED` ohne Eintrag besteht); kollidierende Einträge zu einem Muster zusammenführen (`(TODO|[Tt]odo)s?`); oder ein vorangestelltes `(?i)`-Flag ergänzen (`(?i)MUSTs`).
  - Beim Hinzufügen eines Vocabulary-Begriffs SOLLTE der Autor `task glossary:stubs` ausführen, um die fehlenden Glossar-Einträge zu gerüsten, und dann jeden `TODO`-Platzhalter in beiden Sprachdateien durch eine echte Definition (oder einen kurzen Einordnungssatz bei einer Marke) ersetzen, bevor der PR geöffnet wird.
- **KANN [MAY]**
  - Einträge KÖNNEN innerhalb einer Gruppe alphabetisch sortiert werden, wenn das die Review erleichtert; weder Vale noch der Build hängen von der Reihenfolge ab.
  - Eigene Vale-Regel-YAMLs KÖNNEN unter `src/styles/nolte-styles/` hinzugefügt werden; die ausgelieferte `src/.vale.ini` listet `nolte-styles` bereits in `BasedOnStyles`, neue Regeln aktivieren sich also automatisch im nächsten Release.
  - Eine neue Vocabulary-Gruppe KANN im selben PR eingeführt werden, der ihren ersten Consumer in der eigenen Doku dieses Repos hinzufügt, um zu zeigen, dass die Gruppe durchgängig ausgeübt wird.

## Akzeptanzkriterien

- [ ] Jede in `src/.vale.ini` und der Repo-Root-`.vale.ini` referenzierte Gruppe existiert als Verzeichnis unter `src/styles/config/vocabularies/`.
- [ ] `docs/vocabularies.md` beschreibt genau die auf der Platte vorhandenen Gruppen — kein überzähliger, kein fehlender Abschnitt.
- [ ] Die Liste „Available vocabularies" in `README.md` nennt dieselben Gruppen, in derselben Reihenfolge, wie `docs/vocabularies.md`.
- [ ] Jede `accept.txt` im Repo enthält ausschließlich nicht-leere Zeilen und keine Kommentare.
- [ ] Jeder Produkt- oder Markennamen-Eintrag in jeder `accept.txt` trifft die kanonische Upstream-Schreibweise (keine Klammer-Klasse für Marken, außer für ein Projekt mit kleingeschriebenem kanonischem Namen), und der einführende oder ändernde PR nennt die geprüfte Upstream-Quelle.
- [ ] `vale sync && vale .` läuft im Repo-Root erfolgreich, ausschließlich mit den Vocabularies, die dieses Paket ausliefert.
- [ ] Das über den Abschnitt „Build the archive locally" in `README.md` gebaute Archiv entpackt zur dort dokumentierten Struktur, inklusive `.vale.ini`.
- [ ] Das Hinzufügen einer neuen Regeldatei unter `src/styles/nolte-styles/` erfordert keine Änderung an `src/.vale.ini`.
- [ ] `task glossary:check` läuft erfolgreich: Jeder `accept.txt`-Begriff über alle Gruppen ist in `docs/en/glossary.md` und `docs/de/glossary.md` abgedeckt, wobei jedes Nicht-Lemma-Muster und jede in ein Geschwister gefaltete Variante in `scripts/glossary_aliases.yml` festgehalten ist.
- [ ] Der Glossar-Coverage-Check läuft als pre-commit-Hook (und damit im CI-pre-commit-Job) und lässt den Build bei jedem nicht abgedeckten Begriff fehlschlagen.
- [ ] `task vocab:check` läuft erfolgreich: Für jede Gruppe allein und alle Gruppen gemeinsam wird weder eine akzeptierte Form noch der großgeschriebene Satzanfang einer kleingeschriebenen akzeptierten Form von `Vale.Terms` gemeldet, und jeder Eintrag, der einem gewöhnlichen englischen Wort eine Schreibweise aufzwingt, ist in `scripts/vocab_terms_allow.yml` festgehalten.
- [ ] Der Vale.Terms-Check läuft als pre-commit-Hook `vocab-terms` (und damit im CI-pre-commit-Job) und lässt den Build bei jeder Kollision und jeder nicht festgehaltenen erzwungenen Schreibweise fehlschlagen.

## Offene Fragen

- Soll alphabetisches Sortieren innerhalb einer `accept.txt` zu einem MUSS werden, damit Diff-Reviews mechanisch laufen?
- Wenn die erste echte `nolte-styles`-Regel hinzukommt: eigene Spec fürs Regel-Autoring oder diese Spec erweitern?
- Ist eine Removal-Policy nötig — etwa ein Grep über bekannte Consumer-Repos vor dem Streichen eines Begriffs — oder reicht das Release-Changelog als Signal?
- Wie wird eine brandneue Vocabulary-Gruppe validiert? Reicht ein einziger Consumer innerhalb der eigenen Doku als Bedarfsnachweis, oder sollte zuerst ein externer Consumer identifiziert sein?
- Sollten in ein Geschwister gefaltete Varianten (ein Begriff, der in der Definition eines anderen Eintrags dokumentiert und in `scripts/glossary_aliases.yml` gemappt ist) irgendwann eigene Glossar-Zeilen bekommen, oder ist das Alias-Mapping ihre dauerhafte Heimat?
- Sollte ein Consumer-Korpus-Check (bekannte Consumer-Repos vor dem Veröffentlichen mit einem Release-Kandidaten linten) den Vale.Terms-Check ergänzen, der nur belegt, was das Vocabulary mit den Wörtern macht, die es selbst listet, nicht mit der übrigen Prosa eines Consumers?
