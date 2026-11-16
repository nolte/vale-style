#!/usr/bin/env python3
"""Vale.Terms collision gate.

Vale turns every ``accept.txt`` entry into a ``Vale.Terms`` substitution: a
case-insensitive match that is not the exact accepted form gets flagged. Three
entry shapes turn that against the prose consumers write (issue #40):

1. **Self-collision** — an accepted form is flagged by the very vocabulary that
   accepts it, because another entry also matches it case-insensitively
   (``kamerplanter`` vs ``Kamerplanter('?s)?``; ``TODO`` vs ``[Tt]odo``).
2. **Sentence-initial forcing** — a lowercase entry flags its own form at the
   start of a sentence (``cron`` flags "Cron jobs run nightly.").
3. **Ordinary-word forcing** — the lowercase or capitalised form of an entry is
   an ordinary dictionary word, so ``Vale.Terms`` "corrects" correct prose
   (``REST`` flags "the rest of", ``MRs`` flags "Mrs Smith").

This checker enumerates the class rather than known sites: it expands *every*
entry of *every* group to its literal forms (via ``expand_regex`` from the
glossary checker) and lints, with the shipped vocabularies,

- every accepted form,
- the sentence-initial variant of every plain lowercase form, and
- the lowercase and capitalised variants of every form.

It fails on any accepted form or sentence-initial variant that ``Vale.Terms``
flags, and on any variant that ``Vale.Spelling`` accepts without the
vocabulary (a dictionary word) but ``Vale.Terms`` flags with it, unless the
entry that forces it is recorded as deliberate in ``scripts/vocab_terms_allow.yml``.
Each finding names the entry that ``Vale.Terms`` itself reports. Allowlist
entries that no longer force anything, or no longer exist, fail too, so the
list cannot rot.

Every vocabulary group is checked on its own and all groups together, since a
consumer may enable any combination. Requires the ``vale`` binary on ``PATH``;
``task vocab:check`` runs it through the pre-commit hook, which pins Vale.

Usage::

    python scripts/check_vocab_terms.py
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
import check_glossary_coverage as cgc  # noqa: E402
from check_glossary_coverage import ExpansionTooLarge, expand_regex  # noqa: E402

VOCAB_ROOT = cgc.VOCAB_ROOT
STYLES_PATH = VOCAB_ROOT.parent.parent
ALLOW_PATH = Path(__file__).resolve().parent / "vocab_terms_allow.yml"
# Vale.Spelling skips tokens with digits, so "passes spelling" only means
# "is a dictionary word" for purely alphabetic tokens.
WORD = re.compile(r"[A-Za-z][a-z]*(?:['-][a-z]+)*")
# A plain lowercase word: the only shape whose sentence-initial capital is
# ordinary prose. Mixed-case (pH, arXiv) and snake_case forms keep their casing.
LOWER_WORD = re.compile(r"[a-z]+(?:['-][a-z]+)*")
TERMS_MESSAGE = re.compile(r"Use '(.+)' instead of '")


def load_vocabularies() -> dict[str, list[str]]:
    """Group name -> its accept.txt entries, in file order."""
    groups: dict[str, list[str]] = {}
    for group, entry in cgc.iter_accept_entries(VOCAB_ROOT):
        groups.setdefault(group, []).append(entry)
    return groups


def load_allowlist() -> dict[str, str]:
    """accept.txt entry -> reason its casing is deliberately enforced."""
    if not ALLOW_PATH.exists():
        return {}
    data = yaml.safe_load(ALLOW_PATH.read_text(encoding="utf-8")) or {}
    return {str(k): str(v) for k, v in (data.get("allow") or {}).items()}


def entry_forms(entry: str) -> set[str]:
    """Literal forms an entry accepts, as written (a (?i) flag only drops case forcing)."""
    return {form for form in expand_regex(entry) if form}


def run_vale(workdir: Path, vocabs: list[str], tokens: list[str], *, terms: bool) -> dict[str, list[tuple[str, str]]]:
    """Lint one token per paragraph; return token -> [(check, message), ...]."""
    vocab_line = f"Vocab = {', '.join(vocabs)}\n" if vocabs else ""
    terms_line = "" if terms else "Vale.Terms = NO\n"
    (workdir / ".vale.ini").write_text(
        f"StylesPath = {STYLES_PATH}\nMinAlertLevel = suggestion\n{vocab_line}"
        f"[*.md]\nBasedOnStyles = Vale\n{terms_line}",
        encoding="utf-8",
    )
    # Blank lines between tokens make each its own paragraph, so line 2N-1 is
    # token N, with no sentence-level interaction between tokens.
    doc = workdir / "tokens.md"
    doc.write_text("".join(f"{token}\n\n" for token in tokens), encoding="utf-8")
    proc = subprocess.run(
        ["vale", "--config", str(workdir / ".vale.ini"), "--output=JSON", str(doc)],
        capture_output=True,
        text=True,
        cwd=workdir,
    )
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"vale failed ({proc.returncode}): {proc.stderr.strip()}")
    alerts: dict[str, list[tuple[str, str]]] = {}
    for file_alerts in (json.loads(proc.stdout or "{}") or {}).values():
        for alert in file_alerts:
            token = tokens[(alert["Line"] - 1) // 2]
            alerts.setdefault(token, []).append((alert["Check"], alert["Message"]))
    return alerts


def forcing_entries(alerts: list[tuple[str, str]], accepted: dict[str, str]) -> list[str]:
    """The entries Vale.Terms names in a token's alerts.

    Vale quotes either the raw entry or, when the token matches it, the
    accepted form it would substitute; map the latter back to its entry.
    """
    entries = set(accepted.values())
    found = []
    for check, message in alerts:
        if check == "Vale.Terms" and (match := TERMS_MESSAGE.match(message)):
            named = match.group(1)
            found.append(named if named in entries else accepted.get(named, named))
    return found


def scope_tokens(entries: list[str]) -> tuple[dict[str, str], dict[str, tuple[str, str]], dict[str, str]]:
    """Split one scope's expanded entries into the three token roles.

    Returns (accepted form -> entry, sentence-initial variant -> (form, entry),
    dictionary-word candidate -> entry it was derived from).
    """
    accepted: dict[str, str] = {}
    for entry in entries:
        for form in sorted(entry_forms(entry)):
            accepted.setdefault(form, entry)
    sentence: dict[str, tuple[str, str]] = {}
    candidates: dict[str, str] = {}
    for form, entry in accepted.items():
        if LOWER_WORD.fullmatch(form):
            initial = form[0].upper() + form[1:]
            if initial not in accepted:
                sentence.setdefault(initial, (form, entry))
        for variant in (form.lower(), form.lower().capitalize()):
            if variant not in accepted and variant not in sentence and WORD.fullmatch(variant):
                candidates.setdefault(variant, entry)
    return accepted, sentence, candidates


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
    plans = [(vocabs, scope_tokens([e for g in vocabs for e in vocabularies[g]])) for vocabs in scopes]

    forcing: dict[str, str] = {}
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        # Whether a token is a dictionary word does not depend on the scope:
        # lint the union once, without any vocabulary.
        union = sorted({token for _, (_, _, candidates) in plans for token in candidates})
        misspelled = {
            token
            for token, alerts in run_vale(workdir, [], union, terms=False).items()
            if any(check == "Vale.Spelling" for check, _ in alerts)
        }
        for vocabs, (accepted, sentence, candidates) in plans:
            label = ", ".join(vocabs)
            tokens = [*accepted, *sentence, *candidates]
            alerts = run_vale(workdir, vocabs, tokens, terms=True)
            for form, entry in accepted.items():
                for by in forcing_entries(alerts.get(form, []), accepted):
                    problems.append(
                        f"{label}: accepted form {form!r} (entry {entry!r}) is flagged by Vale.Terms via {by!r}"
                    )
            for initial, (form, entry) in sentence.items():
                for by in forcing_entries(alerts.get(initial, []), accepted):
                    problems.append(
                        f"{label}: sentence-initial {initial!r} of accepted form {form!r} "
                        f"(entry {entry!r}) is flagged by Vale.Terms via {by!r}"
                    )
            for word in candidates:
                if word in misspelled:
                    continue
                for by in forcing_entries(alerts.get(word, []), accepted):
                    forcing.setdefault(by, word)

    for entry, word in sorted(forcing.items()):
        if entry not in allow:
            problems.append(
                f"entry {entry!r} makes Vale.Terms flag the ordinary word {word!r}; "
                f"rewrite it or record the casing in {ALLOW_PATH.name}"
            )
    for entry in sorted(allow):
        if entry not in all_entries:
            problems.append(f"{ALLOW_PATH.name}: {entry!r} is not an accept.txt entry")
        elif entry not in forcing:
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
