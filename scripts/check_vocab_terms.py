#!/usr/bin/env python3
"""Vale.Terms collision gate.

Vale turns every ``accept.txt`` entry into a ``Vale.Terms`` substitution: a
case-insensitive match that is not the exact accepted form gets flagged. Two
entry shapes turn that against the prose consumers write, and both shipped in
v0.2.0 (issue #40):

1. **Self-collision** — an accepted form is flagged by the very vocabulary that
   accepts it, because another entry also matches it case-insensitively
   (``kamerplanter`` vs ``Kamerplanter('?s)?``; ``TODO`` vs ``[Tt]odo``).
2. **Ordinary-word forcing** — the lowercase form of an entry is an ordinary
   dictionary word, so ``Vale.Terms`` "corrects" correct prose (``REST`` flags
   "the rest of", ``mS`` flags "40 ms").

This checker enumerates the class rather than known sites: it expands *every*
entry of *every* group to its literal forms (via ``expand_regex`` from the
glossary checker), lints those forms with the shipped vocabularies, and lints
each form's lowercase variant both with and without them. It fails on

- any accepted form that ``Vale.Terms`` flags, and
- any lowercase variant that ``Vale.Spelling`` accepts without the vocabulary
  (a dictionary word) but ``Vale.Terms`` flags with it,

unless that entry's casing is recorded as deliberate in
``scripts/vocab_terms_allow.yml``. Allowlist entries that no longer force
anything, or no longer exist, fail too, so the list cannot rot.

Every vocabulary group is checked on its own and all groups together, since a
consumer may enable any combination. Requires the ``vale`` binary on ``PATH``.

Usage::

    python scripts/check_vocab_terms.py

Run it through ``task vocab:check``.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_glossary_coverage import (  # noqa: E402
    VOCAB_ROOT,
    ExpansionTooLarge,
    expand_regex,
)

STYLES_PATH = VOCAB_ROOT.parent.parent
ALLOW_PATH = Path(__file__).resolve().parent / "vocab_terms_allow.yml"
# Vale.Spelling skips tokens with digits, so "passes spelling" only means
# "is a dictionary word" for purely alphabetic tokens.
WORD = re.compile(r"[a-z]+(?:['-][a-z]+)*")


def load_vocabularies() -> dict[str, list[str]]:
    """Group name -> its accept.txt entries, in file order."""
    return {
        accept.parent.name: [
            line.strip()
            for line in accept.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for accept in sorted(VOCAB_ROOT.glob("*/accept.txt"))
    }


def load_allowlist() -> dict[str, str]:
    """accept.txt entry -> reason its casing is deliberately enforced."""
    if not ALLOW_PATH.exists():
        return {}
    data = yaml.safe_load(ALLOW_PATH.read_text(encoding="utf-8")) or {}
    return {str(k): str(v) for k, v in (data.get("allow") or {}).items()}


def entry_forms(entry: str) -> set[str]:
    """Literal forms an entry accepts, as written (a (?i) flag only drops case forcing)."""
    return {form for form in expand_regex(entry) if form}


def run_vale(workdir: Path, vocabs: list[str], lines: list[str], *, terms: bool) -> dict[int, set[str]]:
    """Lint one token per line; return line number -> set of alerting checks."""
    vocab_line = f"Vocab = {', '.join(vocabs)}\n" if vocabs else ""
    terms_line = "" if terms else "Vale.Terms = NO\n"
    (workdir / ".vale.ini").write_text(
        f"StylesPath = {STYLES_PATH}\nMinAlertLevel = suggestion\n{vocab_line}"
        f"[*.md]\nBasedOnStyles = Vale\n{terms_line}",
        encoding="utf-8",
    )
    # Blank lines between tokens make each its own paragraph, so line N of the
    # body maps to token N without any sentence-level interaction.
    doc = workdir / "tokens.md"
    doc.write_text("".join(f"{token}\n\n" for token in lines), encoding="utf-8")
    proc = subprocess.run(
        ["vale", "--config", str(workdir / ".vale.ini"), "--output=JSON", str(doc)],
        capture_output=True,
        text=True,
        cwd=workdir,
    )
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"vale failed ({proc.returncode}): {proc.stderr.strip()}")
    alerts: dict[int, set[str]] = {}
    for file_alerts in (json.loads(proc.stdout or "{}") or {}).values():
        for alert in file_alerts:
            alerts.setdefault((alert["Line"] + 1) // 2, set()).add(alert["Check"])
    return alerts


def check_scope(workdir: Path, vocabs: list[str], entries: list[str]) -> tuple[list[str], dict[str, str]]:
    """Return (self-collision messages, forcing entry -> example word) for one Vocab set."""
    forms: list[tuple[str, str]] = []
    for entry in entries:
        forms.extend((entry, form) for form in sorted(entry_forms(entry)))
    accepted = {form for _, form in forms}

    with_vocab = run_vale(workdir, vocabs, [form for _, form in forms], terms=True)
    collisions = [
        f"{', '.join(vocabs)}: accepted form {form!r} (entry {entry!r}) is flagged by Vale.Terms"
        for index, (entry, form) in enumerate(forms, start=1)
        if "Vale.Terms" in with_vocab.get(index, set())
    ]

    variants: list[tuple[str, str]] = []
    seen: set[str] = set()
    for entry, form in forms:
        lower = form.lower()
        if lower not in accepted and lower not in seen and WORD.fullmatch(lower):
            seen.add(lower)
            variants.append((entry, lower))
    tokens = [word for _, word in variants]
    forced_with = run_vale(workdir, vocabs, tokens, terms=True)
    spelling_without = run_vale(workdir, [], tokens, terms=False)
    forcing: dict[str, str] = {}
    for index, (entry, word) in enumerate(variants, start=1):
        is_word = "Vale.Spelling" not in spelling_without.get(index, set())
        if is_word and "Vale.Terms" in forced_with.get(index, set()):
            forcing.setdefault(entry, word)
    return collisions, forcing


def check() -> int:
    if shutil.which("vale") is None:
        print("vale not found on PATH; install Vale to run this check.", file=sys.stderr)
        return 2
    vocabularies = load_vocabularies()
    allow = load_allowlist()
    problems: list[str] = []

    unexpandable = []
    for group, entries in vocabularies.items():
        for entry in entries:
            try:
                entry_forms(entry)
            except (ExpansionTooLarge, ValueError) as exc:
                unexpandable.append(f"{group}: entry {entry!r} cannot be expanded ({exc})")
    if unexpandable:
        print("Vale.Terms check cannot verify these entries:", file=sys.stderr)
        for message in unexpandable:
            print(f"  - {message}", file=sys.stderr)
        return 1

    scopes = [[group] for group in vocabularies]
    if len(vocabularies) > 1:
        scopes.append(list(vocabularies))
    all_entries = {entry for entries in vocabularies.values() for entry in entries}
    forcing_all: dict[str, str] = {}
    with tempfile.TemporaryDirectory() as tmp:
        for vocabs in scopes:
            entries = [entry for group in vocabs for entry in vocabularies[group]]
            collisions, forcing = check_scope(Path(tmp), vocabs, entries)
            problems.extend(collisions)
            for entry, word in forcing.items():
                forcing_all.setdefault(entry, word)

    for entry, word in sorted(forcing_all.items()):
        if entry not in allow:
            problems.append(
                f"entry {entry!r} makes Vale.Terms flag the ordinary word {word!r}; "
                f"rewrite it or record the casing in {ALLOW_PATH.name}"
            )
    for entry in sorted(allow):
        if entry not in all_entries:
            problems.append(f"{ALLOW_PATH.name}: {entry!r} is not an accept.txt entry")
        elif entry not in forcing_all:
            problems.append(f"{ALLOW_PATH.name}: {entry!r} no longer forces any word; drop it")

    if problems:
        print("Vale.Terms collision check failed:", file=sys.stderr)
        for message in sorted(set(problems)):
            print(f"  - {message}", file=sys.stderr)
        return 1
    print(f"Vale.Terms collision check passed ({len(all_entries)} entries, {len(scopes)} scopes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
