# Glossary

Every term this package's vocabularies accept, defined. Entries are grouped into the same families as the [Vocabularies](vocabularies.md) page and shown by their readable lemma — the underlying `accept.txt` entry is often a regex that also covers plurals and other inflections (see [how matching works](vocabularies.md#how-entries-are-matched)). Brand and product names carry a short placement note rather than a full definition.

## `technical` vocabulary

### Tools, products, and brands

`Ansible`
:   Automation and configuration-management tool that needs no agent on managed hosts.

`Anthropic`
:   AI-safety company that builds the Claude models.

`asdf`
:   Version manager that handles multiple language runtimes through one CLI.

`Astro`
:   Web framework for content-driven sites that ships minimal client-side JavaScript.

`Atlassian`
:   Software vendor behind Jira, Confluence, and Bitbucket.

`Bun`
:   Fast all-in-one JavaScript runtime, bundler, and package manager.

`chezmoi`
:   Cross-machine dotfile manager.

`Claude`
:   Anthropic's family of large language models.

`Contentful`
:   API-first headless content-management system.

`cookiecutter`
:   Project-scaffolding tool that renders a template from a set of answers.

`dayjs`
:   Minimalist JavaScript date/time library.

`Dependabot`
:   GitHub bot that opens pull requests to update dependencies.

`Deque`
:   Accessibility-tooling company behind the axe testing engine.

`DOMPurify`
:   Client-side HTML sanitiser that strips XSS-prone markup.

`Eleventy`
:   Static-site generator, also written "11ty".

`ESLint`
:   Extensible linter for JavaScript and TypeScript.

`ESPHome`
:   Framework that builds firmware for ESP-based devices, commonly with Home Assistant.

`Figma`
:   Browser-based collaborative interface-design tool.

`gh-plumbing`
:   nolte's shared repository of reusable GitHub Actions workflows and Probot configurations.

`godoc`
:   Go's documentation generator.

`Grammarly`
:   Commercial writing assistant and grammar checker.

`Graphviz`
:   Graph-visualisation toolkit driven by the DOT language.

`Inkbot`
:   Third-party design studio/brand referenced in the project's asset specs.

`Jira`
:   Atlassian's issue- and project-tracking tool.

`JUnit`
:   Java unit-testing framework whose XML report format is a CI standard.

`Mailchimp`
:   Email-marketing and newsletter platform.

`Mantine`
:   React component and hooks library.

`Midjourney`
:   Generative-AI image service.

`MkDocs`
:   Static-site generator for project documentation, used here with the Material theme.

`MUI`
:   Material UI, a React component library implementing Material Design.

`mypy`
:   Static type checker for Python.

`nginx`
:   High-performance web server and reverse proxy.

`nolte`
:   The GitHub account that publishes this package.

`notistack`
:   React library for stacking snackbar notifications.

`npm`
:   Default package manager and registry for Node.js.

`Numonic`
:   Third-party brand referenced in the project's specs.

`Probot`
:   Framework for building GitHub Apps; backs the shared settings and labelling bots.

`Pyright`
:   Microsoft's static type checker for Python.

`Recharts`
:   React charting library built on D3.

`Renovate`
:   Automated dependency-update tool, configured here via a shared preset.

`Shiki`
:   Syntax highlighter that uses TextMate grammars and editor themes.

`Skywork`
:   Third-party AI model/service referenced in the project.

`Supabase`
:   Open-source backend platform built on PostgreSQL.

`Tailwind`
:   Utility-first CSS framework.

`Taskfile`
:   Configuration file for the go-task task runner (`task`).

`Tauri`
:   Framework for building desktop apps with a web frontend and a Rust core.

`textstat`
:   Python library that computes readability metrics.

`Trivy`
:   Open-source security and vulnerability scanner.

`typedoc`
:   Documentation generator for TypeScript.

`Ulanzi`
:   Consumer-hardware brand, e.g. the smart pixel-clock used in some configs.

`Vercel`
:   Hosting and deployment platform, originator of Next.js.

`Vite`
:   Fast frontend build tool and development server.

`Vitest`
:   Vite-native unit-testing framework.

`vtracer`
:   Tool that traces raster images into SVG vectors.

`Vue`
:   Progressive JavaScript framework for building user interfaces.

`Webheads`
:   Third-party brand/community referenced in the project.

`Zod`
:   TypeScript-first schema declaration and validation library.

`zsh`
:   The Z shell, an interactive Unix shell.

### Software-engineering, CI/CD, security, and documentation terms

`AC`
:   Acceptance criterion — a condition a change must meet to count as done (plural ACs).

`addon`
:   A component that extends a host application.

`ADR`
:   Architecture Decision Record — a short note capturing one architectural choice and its rationale.

`affordance`
:   A design cue that signals how an element can be used.

`agentic`
:   Describing software, typically LLM-driven, that pursues goals autonomously.

`agent`
:   An autonomous program that performs tasks on a user's behalf.

`allowlist`
:   An explicit set of permitted entities; the inclusive counterpart to a denylist.

`API`
:   Application Programming Interface — a defined contract between software components.

`async`
:   Asynchronous — not blocking the caller while an operation completes.

`attestable`
:   Able to be cryptographically attested.

`attestation`
:   A signed claim about an artifact's origin or integrity, such as build provenance.

`auditability`
:   The degree to which a system's actions can be reviewed after the fact.

`auditable`
:   Able to be reviewed and checked against a record.

`autofix`
:   An automatically applied fix for a lint or build finding.

`autofocus`
:   HTML attribute that focuses an input when the page loads.

`automerge`
:   Merging a pull request automatically once all required checks pass.

`backend`
:   The server-side portion of an application.

`backlink`
:   A link pointing back to a page that references it.

`bluetooth`
:   Short-range wireless connectivity standard.

`boolean`
:   A value that is either true or false.

`bundler`
:   A tool that combines source modules into deployable bundles.

`callout`
:   A visually set-off note or admonition in documentation.

`CI`
:   Continuous Integration — automatically building and testing every change.

`CLI`
:   Command-Line Interface.

`closeable`
:   Able to be closed, e.g. a releasable resource.

`conformant`
:   Adhering to a specification or standard.

`cron`
:   Time-based job scheduler; also the syntax for its schedules.

`CSP`
:   Content Security Policy — an HTTP header constraining what a page may load.

`CTA`
:   Call To Action — a prompt urging the reader to take a step.

`CVE`
:   Common Vulnerabilities and Exposures — a public identifier for a security flaw.

`debounce`
:   To delay handling of rapid repeated events until they settle.

`dedup`
:   Short for deduplicate.

`deduplicate`
:   To remove duplicate entries.

`denylist`
:   An explicit set of blocked entities; the counterpart to an allowlist.

`devcontainer`
:   A container-defined, reproducible development environment.

`diataxis`
:   A documentation framework splitting docs into tutorials, how-tos, reference, and explanation.

`dialog`
:   A modal or non-modal window prompting for input or confirmation.

`diffable`
:   Able to be compared line-by-line as a diff.

`Dockerfile`
:   A text recipe describing how to build a container image.

`docstring`
:   An inline documentation string embedded in source code.

`enum`
:   Enumeration — a type with a fixed set of named values.

`favicon`
:   The small icon a browser shows for a site.

`focusable`
:   Able to receive keyboard focus.

`formatter`
:   A tool that rewrites code to a consistent style.

`frontend`
:   The client-side, user-facing part of an application.

`frontmatter`
:   The metadata block, often YAML, at the top of a Markdown file.

`geoblocking`
:   Restricting access to content by geographic region.

`gerund`
:   A verb's `-ing` form used as a noun.

`GHSA`
:   GitHub Security Advisory identifier.

`Guillemets`
:   Angle-shaped quotation marks (« »).

`HMAC`
:   Hash-based Message Authentication Code — a keyed integrity and authenticity check.

`hoc`
:   Higher-Order Component — a React function that wraps a component to add behaviour.

`hotfix`
:   An urgent fix applied directly to a released version.

`idempotency`
:   The property that repeating an operation yields the same result as doing it once.

`idempotently`
:   In an idempotent manner.

`implementor`
:   One who implements a specification, also spelled "implementer".

`inlining`
:   Substituting a definition directly at its use site.

`inspectable`
:   Able to be examined at runtime or via tooling.

`lede`
:   The opening of an article that states its core point; plural ledes.

`lockfile`
:   A file pinning exact resolved dependency versions.

`lookup`
:   A retrieval of a value by key.

`lossy`
:   Discarding some information, as in lossy compression.

`memoise`
:   To cache a function's result for repeated identical inputs.

`mergeable`
:   Able to be merged without conflict.

`misclassification`
:   Assigning something to the wrong category.

`mitigation`
:   A measure that reduces a risk's likelihood or impact.

`monorepo`
:   A single repository holding many projects.

`MR`
:   Merge Request — GitLab's term for a pull request.

`MUSTs` / `SHOULDs`
:   Pluralised RFC 2119 requirement keywords.

`Newswire`
:   A service that distributes news copy to outlets.

`NFR`
:   Non-Functional Requirement — a quality constraint such as performance or security.

`OAuth`
:   Open standard for delegated authorization.

`OQ`
:   Open Question — an unresolved point recorded in a spec.

`parseable`
:   Able to be parsed.

`postcondition`
:   A condition guaranteed to hold after an operation.

`preload`
:   To fetch a resource ahead of when it is needed.

`PR`
:   Pull Request — a proposed change submitted for review and merge.

`px`
:   CSS pixel unit.

`PYSEC`
:   Identifier for a Python-ecosystem security advisory.

`queryable`
:   Able to be queried.

`querystring`
:   The `key=value` portion of a URL after `?`.

`reachability`
:   Whether a node or state can be reached from another.

`rebase`
:   To replay commits onto a new base; also rebases, rebasing.

`reflog`
:   A log of where Git references have pointed (`git reflog`).

`reusable`
:   Able to be used again in another context.

`runbook`
:   A documented procedure for operating or recovering a system.

`runtime`
:   The environment in which a program executes; plural runtimes.

`sandboxing`
:   Isolating code so it cannot affect the host beyond a permitted boundary.

`scannability`
:   How easily text can be skimmed by eye.

`SemVer`
:   Semantic Versioning — the `MAJOR.MINOR.PATCH` version scheme.

`severity`
:   The graded impact level of a finding or incident; plural severities.

`SHA`
:   Secure Hash Algorithm; commonly a Git commit hash.

`SLA`
:   Service-Level Agreement.

`snackbar`
:   A brief, non-blocking notification shown at a screen edge.

`sref`
:   Midjourney's style-reference parameter (`--sref`).

`SRE`
:   Site Reliability Engineering, or a Site Reliability Engineer.

`Subresource`
:   A resource a page loads in addition to itself, as in Subresource Integrity.

`stylers`
:   Components or tools that apply visual styling.

`symbolication`
:   Mapping memory addresses in a crash back to source symbols.

`teardown`
:   Cleanup run after a test or process.

`thresholding`
:   Applying a cut-off value to classify or filter.

`tooltip`
:   A small hint shown on hover or focus.

`typecheck`
:   To verify a program against its type rules.

`unparseable`
:   Not able to be parsed.

`validator`
:   A component that checks input against rules.

`viewport`
:   The visible region of a page in the browser.

`wordmark`
:   A logo rendered as styled text.

`worktree`
:   A linked working directory of a Git repository.

`YAML`
:   YAML Ain't Markup Language — a human-readable data-serialisation format.

### Naming, lifecycle, and workflow words

`achievability`
:   Whether a goal is realistically attainable — the "A" in SMART.

`autoallow`
:   To permit automatically without manual approval.

`autodetect`
:   To detect automatically without explicit configuration.

`autolink`
:   To turn a reference into a hyperlink automatically.

`autoload`
:   To load automatically on demand.

`automatable`
:   Able to be automated.

`auto-tag`
:   To apply a tag automatically.

`bikeshedding`
:   Spending disproportionate effort on trivial details.

`browsable`
:   Able to be browsed.

`bypassable`
:   Able to be bypassed.

`definitionally`
:   By definition.

`disambiguation`
:   Resolving which of several meanings is intended.

`discoverability`
:   How easily something can be found.

`dispatchable`
:   Able to be dispatched, i.e. routed to a handler.

`dogfood`
:   To use one's own product internally; dogfooding.

`favouriting`
:   Marking an item as a favourite.

`invocable`
:   Able to be invoked, also "invokable".

`kebab`
:   As in kebab-case — lowercase words joined by hyphens.

`linkability`
:   How readily items can be linked to one another.

`mandatoriness`
:   The degree to which something is mandatory.

`namespace`
:   A named scope that keeps identifiers distinct; namespaced.

`onboarding`
:   Bringing a new user, contributor, or repository up to speed.

`operationalize`
:   To turn a concept into a concrete, runnable procedure.

`overridable`
:   Able to be overridden.

`rebalancing`
:   Redistributing load or allocation.

`recalibrated`
:   Adjusted back to a correct reference.

`rephrase`
:   To express again in different words.

`repointing`
:   Redirecting a reference to a new target.

`repurpose`
:   To adapt something for a new use.

`retarget`
:   To change the intended target.

`retconning`
:   Retroactively changing established facts.

`reviewability`
:   How readily a change can be reviewed.

`revisitable`
:   Able to be revisited.

`roadmap`
:   A planned sequence of future work; plural roadmaps.

`rollout`
:   The staged release of a change.

`routable`
:   Able to be routed to a destination.

`scaffold`
:   To generate a starting skeleton of files; scaffolding.

`slugification`
:   Converting a string into a URL-safe slug.

`subagent`
:   An agent dispatched by another agent.

`subfolder`
:   A nested folder.

`submodule`
:   A repository embedded within another (a Git submodule).

`subproject`
:   A project nested within a larger one.

`subroot`
:   A nested root directory within a tree.

`subtask`
:   A task that is part of a larger one.

`toolchain`
:   The set of tools used to build and ship software.

`triage`
:   To sort items by priority; triaged, triaging, triages.

`triggerer`
:   The actor or event that triggers something.

`underperforming`
:   Performing below expectation.

`unreviewed`
:   Not yet reviewed.

`untriaged`
:   Not yet triaged.

`upgrader`
:   A tool or actor that performs upgrades.

`upstreamed`
:   Contributed back to the upstream source.

`vectorise`
:   To convert to a vector representation.

`vendor`
:   To copy a dependency's source into the repository; vendored, vendoring.

`virtualise`
:   To create a virtual version of something.

`prepended`
:   Added to the beginning.

### Proper names — writing, readability, and accessibility sources

These surnames are accepted because they appear as cited authors or sources in the project's readability, editorial-style, and accessibility specs; the three colour-vision terms come from the accessibility domain.

`Bamberger`
:   Co-originator, with Vanecek, of German-language readability research.

`Carliner`
:   Saul Carliner, a technical-communication author.

`Chissom`
:   Co-author of the Flesch–Kincaid grade-level study.

`Desrosiers`
:   Surname cited as a source in the readability/writing specs.

`Fishburne`
:   Co-author of the Flesch–Kincaid grade-level study.

`Flesch`
:   Rudolf Flesch, originator of the Flesch Reading Ease score.

`Kalzumeus`
:   The blog and handle of software writer Patrick McKenzie.

`Kincaid`
:   J. P. Kincaid, co-creator of the Flesch–Kincaid readability metric.

`Kissane`
:   Erin Kissane, a content-strategy author.

`Lannon`
:   John Lannon, a technical-writing textbook author.

`Matuschak`
:   Andy Matuschak, known for work on notes and knowledge tools.

`Stockton`
:   Surname cited as a source in the writing/readability specs.

`Strunk`
:   William Strunk Jr., co-author of "The Elements of Style".

`Vanecek`
:   Co-originator, with Bamberger, of German-language readability research.

`Zinsser`
:   William Zinsser, author of "On Writing Well".

`deutan`
:   Colour-vision deficiency affecting green perception (the deuteranopia family).

`protan`
:   Colour-vision deficiency affecting red perception (the protanopia family).

`tritan`
:   Colour-vision deficiency affecting blue perception (the tritanopia family).

### Shell and runtime shorthands

`basename`
:   The final component of a file path.

`config`
:   Short for configuration; plural configs.

`cwd`
:   Current working directory.

`deps`
:   Short for dependencies.

`DMs`
:   Direct messages.

`dotfile`
:   A hidden configuration file whose name begins with a dot.

`env`
:   Short for environment, or an environment variable.

`gitignored`
:   Excluded from Git tracking via `.gitignore`.

`greppable`
:   Easy to search with grep.

`Lc`
:   Short token accepted for spelling; appears in the project's specs.

`lowercased`
:   Converted to lowercase.

`PDFs`
:   Portable Document Format files.

`PNGs`
:   Portable Network Graphics files.

`READMEs`
:   The plural of README.

`repo`
:   Short for repository; plural repos.

`skimmable`
:   Easy to skim.

`stderr`
:   Standard error stream.

`stdout`
:   Standard output stream.

`untracked`
:   Not tracked by version control.

`untrusted`
:   Not granted trust.

`unversioned`
:   Not under version control, or lacking a version.

`venv`
:   A Python virtual environment.

`virtualenv`
:   A Python virtual-environment tool or environment.

### Inflected and possessive forms

A few entries exist only so the spell-checker accepts an inflected or possessive form and carry no meaning beyond their base word: `commit's`, `criteria's`, `else's`, `maintainer's`, `README's`, and `navigations`.

## `esphome` vocabulary

### Hardware identifiers

`ESP8285`
:   A compact controller chip with built-in flash, used in some smart plugs.

`HLW8012`
:   A power-metering sensor IC used in smart plugs.

`SP111`
:   An ESPHome-compatible smart-plug model.

`NOUS`
:   A smart-home hardware brand, e.g. the A1T plug.

`A1T`
:   A NOUS smart-plug model.

`Gosund`
:   A smart-home device brand.

### GPIO pins

`GPIO`
:   General-Purpose Input/Output pin.

`GPIO00`–`GPIO39`
:   Zero-padded two-digit pin names matched by the regex `GPIO(0[0-9]|[1-3][0-9])`, covering both ESP8266 and ESP32 pins.

### YAML configuration keys

`baud_rate`
:   Serial communication speed.

`status_led`
:   Pin configured to show device status.

`restore_mode`
:   How a switch's state is restored after boot.

`restore_from_flash`
:   Whether state is persisted to and restored from flash.

`early_pin_init`
:   Whether pins are initialised early during boot.

`turn_on_action`
:   Automation run when an entity turns on.

`turn_off_action`
:   Automation run when an entity turns off.

### Domain words

`automations`
:   Rules that trigger actions on events or conditions.

`Datetime`
:   A combined date-and-time value or type.

`dBm`
:   Decibel-milliwatts; a signal-strength unit, e.g. Wi-Fi RSSI.

`hostname`
:   A device's network name; plural hostnames.

`LED`
:   Light-Emitting Diode; plural LEDs.
