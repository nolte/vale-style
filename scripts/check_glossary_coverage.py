#!/usr/bin/env python3
"""Glossary-coverage gate.

Every term a Vale vocabulary accepts (``src/styles/config/vocabularies/<group>/
accept.txt``) must have a matching glossary entry in *both* ``docs/en/glossary.md``
and ``docs/de/glossary.md``, so a term added in a PR can never silently ship
without being defined.

``accept.txt`` entries are Vale regexes, not plain lemmas (``[Aa]gents?``,
``Anthropic('s)?``, ``[Dd]eduplicat(e|es|ed|ing|ion)?``). Rather than guess a
single lemma per entry, this checker *expands* each regex to the bounded set of
literal strings it can match, normalizes each candidate to a comparison key
(lowercase, trailing ``'s``/``s`` stripped), and treats the entry as covered if
any candidate key appears as a backtick-wrapped lemma in the glossary. Glossary
lemmas are normalized the same way, so ``Anthropic('s)?`` matches ``Anthropic``
and ``PNGs?('s)?`` matches ``PNGs``.

Hard cases that are not single lemmas (e.g. the ``GPIO(0[0-9]|[1-3][0-9])`` pin
range) are handled via ``scripts/glossary_aliases.yml``.

Usage::

    python scripts/check_glossary_coverage.py            # verify, exit 1 on any gap
    python scripts/check_glossary_coverage.py --write-stubs   # scaffold TODO stubs

Run it through ``task glossary:check`` / ``task glossary:stubs``.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_ROOT = REPO_ROOT / "src" / "styles" / "config" / "vocabularies"
ALIASES_PATH = Path(__file__).resolve().parent / "glossary_aliases.yml"

# Language code -> glossary file, the TODO placeholder written into stubs, the
# localized subsection heading new stubs land under, and the localized heading a
# brand-new group section is created with. Existing group headings are located
# by regex (see _group_section) rather than a literal, so either language's form
# is found; `group_heading` only decides how a missing section is written.
GLOSSARIES = {
    "en": {
        "path": REPO_ROOT / "docs" / "en" / "glossary.md",
        "placeholder": "TODO: define",
        "subheading": "### Uncovered terms (TODO: categorise + define)",
        "group_heading": "## `{group}` vocabulary",
    },
    "de": {
        "path": REPO_ROOT / "docs" / "de" / "glossary.md",
        "placeholder": "TODO: definieren",
        "subheading": "### Nicht abgedeckte Begriffe (TODO: einsortieren + definieren)",
        "group_heading": "## Vokabular `{group}`",
    },
}

# Guard against a pathological regex expanding to an enormous literal set.
EXPANSION_CAP = 5000

BACKTICK_TOKEN = re.compile(r"`([^`]+)`")


class ExpansionTooLarge(Exception):
    """Raised when a regex would expand past EXPANSION_CAP literals."""


# --------------------------------------------------------------------------- #
# Regex expansion: a small recursive-descent expander for the subset of regex
# syntax that appears in accept.txt — literals, escaped punctuation (\\. \\+),
# [..] classes (with x-y ranges), (..|..) groups, and a trailing `?` quantifier
# on any of those.
# --------------------------------------------------------------------------- #

def _unescape(body: str) -> list[tuple[str, bool]]:
    """Split ``body`` into ``(char, was_escaped)`` pairs, resolving ``\\x`` escapes.

    Only escaped punctuation (``\\.``, ``\\+``, ``\\?``, ...) is a literal; an
    escaped letter or digit is a regex shorthand (``\\d``, ``\\w``, ``\\b``) outside
    the expandable subset, so it raises ValueError and the caller falls back.
    """
    chars: list[tuple[str, bool]] = []
    i = 0
    while i < len(body):
        if body[i] == "\\":
            if i + 1 >= len(body):
                raise ValueError(f"dangling escape in {body!r}")
            if body[i + 1].isalnum():
                raise ValueError(f"unsupported escape \\{body[i + 1]} in {body!r}")
            chars.append((body[i + 1], True))
            i += 2
        else:
            chars.append((body[i], False))
            i += 1
    return chars


def _expand_class(body: str) -> set[str]:
    tokens = _unescape(body)
    chars: set[str] = set()
    i = 0
    while i < len(tokens):
        # An unescaped "-" between two characters is a range; "\\-" is literal.
        if i + 2 < len(tokens) and tokens[i + 1] == ("-", False):
            for code in range(ord(tokens[i][0]), ord(tokens[i + 2][0]) + 1):
                chars.add(chr(code))
            i += 3
        else:
            chars.add(tokens[i][0])
            i += 1
    return chars


def _cap(strings: set[str]) -> set[str]:
    if len(strings) > EXPANSION_CAP:
        raise ExpansionTooLarge
    return strings


def _class_end(pattern: str, start: int) -> int:
    """Index of the ``]`` closing the class opened at ``start``, skipping ``\\]``."""
    i = start + 1
    while i < len(pattern):
        if pattern[i] == "\\":
            i += 2
            continue
        if pattern[i] == "]":
            return i
        i += 1
    raise ValueError(f"unterminated class in {pattern!r}")


def expand_regex(pattern: str) -> set[str]:
    """Expand a (restricted) Vale-vocab regex to the set of literals it matches.

    Supports literals, ``\\``-escaped punctuation, ``[..]`` classes with ``x-y``
    ranges, ``(..|..)`` groups, and a trailing ``?`` on any atom. Raises ExpansionTooLarge if the product
    blows past EXPANSION_CAP, or ValueError on syntax outside this subset; the
    caller falls back to a mechanical single-key stem in that case.
    """

    pos = 0

    def parse_sequence(stop: set[str]) -> set[str]:
        nonlocal pos
        results = {""}
        while pos < len(pattern) and pattern[pos] not in stop:
            atom = parse_atom()
            # Optional quantifier on the atom just parsed.
            if pos < len(pattern) and pattern[pos] == "?":
                pos += 1
                atom = atom | {""}
            results = _cap({prefix + suffix for prefix in results for suffix in atom})
        return results

    def parse_atom() -> set[str]:
        nonlocal pos
        ch = pattern[pos]
        if ch == "(":
            pos += 1  # consume '('
            alternatives: set[str] = set()
            while True:
                alternatives |= parse_sequence({"|", ")"})
                if pos >= len(pattern):
                    raise ValueError(f"unterminated group in {pattern!r}")
                if pattern[pos] == "|":
                    pos += 1  # consume '|', parse next alternative
                    continue
                break
            pos += 1  # consume ')'
            return _cap(alternatives)
        if ch == "\\":
            # Escaped character: \\. -> "." (see _unescape for what is allowed).
            ((literal, _escaped),) = _unescape(pattern[pos:pos + 2])
            pos += 2
            return {literal}
        if ch == "[":
            end = _class_end(pattern, pos)
            chars = _expand_class(pattern[pos + 1:end])
            pos = end + 1  # consume past ']'
            return _cap(chars)
        if ch in "|)]":
            raise ValueError(f"unexpected {ch!r} in {pattern!r}")
        # Literal character.
        pos += 1
        return {ch}

    result = parse_sequence(set())
    if pos != len(pattern):
        raise ValueError(f"trailing input in {pattern!r}")
    return result


# --------------------------------------------------------------------------- #
# Normalization
# --------------------------------------------------------------------------- #

def normalize_key(token: str) -> str:
    """Lowercase and strip a trailing possessive/plural ``s`` for comparison."""
    token = token.strip().lower()
    if token.endswith("'s") and len(token) > 2:
        return token[:-2]
    if token.endswith("s") and len(token) > 1:
        return token[:-1]
    return token


def display_lemma(pattern: str) -> str:
    """Best-effort readable lemma for a stub.

    Derived from the regex's own expansion: the shortest literal the pattern
    matches, preferring a lowercase leading letter so ``[Aa]gents?`` -> "agent"
    while ``Anthropic('s)?`` -> "Anthropic". Deriving from the expansion (rather
    than hand-stripping the regex) guarantees the stub lemma is a real literal —
    never leftover regex syntax like ``Jinja2?`` or ``virtualis(e|ed)`` — so a
    written stub is covered on the next run instead of being re-emitted. Falls
    back to a mechanical strip only when the pattern can't be expanded. Imperfect
    by design — the stub is a TODO the author refines.
    """
    try:
        literals = {lit for lit in expand_regex(pattern) if lit}
    except (ExpansionTooLarge, ValueError):
        literals = set()
    if literals:
        shortest = min(len(lit) for lit in literals)
        best = sorted(lit for lit in literals if len(lit) == shortest)
        for lemma in best:
            if lemma[:1].islower():
                return lemma
        return best[0]
    return _mechanical_lemma(pattern)


def _mechanical_lemma(pattern: str) -> str:
    """Fallback lemma derivation for patterns ``expand_regex`` can't expand."""
    s = pattern
    # Leading case class [Aa] -> lowercase first letter.
    m = re.match(r"^\[([A-Za-z])[A-Za-z]\]", s)
    if m:
        s = m.group(1).lower() + s[m.end():]
    # Trailing optional group/class/char.
    appended = ""
    m = re.search(r"\(([^)]*)\)\?$", s)
    if m:
        first_alt = m.group(1).split("|")[0]
        if first_alt == "e":
            appended = "e"
        s = s[:m.start()]
    else:
        s = re.sub(r"\[[^\]]*\]\?$", "", s)
        s = re.sub(r"[A-Za-z]\?$", "", s)
    return s + appended


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #

def load_overrides() -> tuple[dict[str, str], set[str]]:
    data = yaml.safe_load(ALIASES_PATH.read_text(encoding="utf-8")) or {}
    aliases = data.get("aliases") or {}
    ignore = set(data.get("ignore") or [])
    return aliases, ignore


def candidate_keys(pattern: str) -> set[str]:
    """The set of normalized comparison keys an accept.txt entry can match."""
    try:
        literals = expand_regex(pattern)
    except (ExpansionTooLarge, ValueError):
        # Fall back to a single mechanical stem key.
        literals = {display_lemma(pattern)}
    return {normalize_key(lit) for lit in literals if lit}


def parse_vocabularies(aliases: dict[str, str], ignore: set[str]) -> list[dict]:
    """One record per accept.txt entry across all vocabulary groups."""
    entries: list[dict] = []
    for accept in sorted(VOCAB_ROOT.glob("*/accept.txt")):
        group = accept.parent.name
        for raw in accept.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line in ignore:
                continue
            if line in aliases:
                keys = {normalize_key(aliases[line])}
            else:
                keys = candidate_keys(line)
            entries.append({
                "raw": line,
                "group": group,
                "keys": keys,
                "lemma": aliases.get(line) or display_lemma(line),
            })
    return entries


def glossary_keys(text: str) -> set[str]:
    """Normalized keys of every backtick lemma in a glossary's text.

    A lemma is any backtick token on a line that is *not* a definition body
    (definition lines start with ``:``). That captures definition-list terms,
    multi-token term lines (``MUSTs`` / ``SHOULDs``), and prose paragraphs that
    list inflected forms, while ignoring backtick tokens inside definitions
    (``git commit``, ``--sref``) that would otherwise mask a real gap.
    """
    keys: set[str] = set()
    for raw in text.splitlines():
        if raw.lstrip().startswith(":"):
            continue
        for token in BACKTICK_TOKEN.findall(raw):
            keys.add(normalize_key(token))
    return keys


# --------------------------------------------------------------------------- #
# Checking & reporting
# --------------------------------------------------------------------------- #

def find_gaps(entries: list[dict], covered: set[str]) -> list[dict]:
    return [e for e in entries if not (e["keys"] & covered)]


def compute_gaps() -> tuple[list[dict], list[tuple[dict, str, list[dict]]]]:
    """Shared load -> parse -> per-language gap pipeline.

    Returns the vocabulary entries and, per glossary, ``(cfg, text, gaps)``.
    Each glossary file is read exactly once; the text is handed on so the stub
    writer doesn't re-read it.
    """
    aliases, ignore = load_overrides()
    entries = parse_vocabularies(aliases, ignore)
    per_glossary = []
    for cfg in GLOSSARIES.values():
        text = cfg["path"].read_text(encoding="utf-8")
        per_glossary.append((cfg, text, find_gaps(entries, glossary_keys(text))))
    return entries, per_glossary


def check() -> int:
    entries, per_glossary = compute_gaps()
    exit_code = 0
    for cfg, _text, gaps in per_glossary:
        rel = cfg["path"].relative_to(REPO_ROOT)
        if gaps:
            exit_code = 1
            print(f"✗ {rel}: {len(gaps)} accept.txt term(s) without a glossary entry:")
            for e in sorted(gaps, key=lambda e: (e["group"], e["raw"])):
                print(f"    [{e['group']}] {e['raw']}  (lemma: {e['lemma']})")
        else:
            print(f"✓ {rel}: all {len(entries)} vocabulary terms covered")
    if exit_code:
        print(
            "\nAdd the missing entries (try `task glossary:stubs` to scaffold them), "
            "or record a justified exemption in scripts/glossary_aliases.yml.",
            file=sys.stderr,
        )
    return exit_code


def write_stubs() -> int:
    _entries, per_glossary = compute_gaps()
    total_written = 0
    for cfg, text, gaps in per_glossary:
        path = cfg["path"]
        if not gaps:
            print(f"✓ {path.relative_to(REPO_ROOT)}: nothing to stub")
            continue
        path.write_text(_append_stubs(text, gaps, cfg), encoding="utf-8")
        total_written += len(gaps)
        print(f"+ {path.relative_to(REPO_ROOT)}: scaffolded {len(gaps)} stub(s)")
    if total_written:
        print(
            "\nStubs landed under a 'TODO: categorise + define' subsection per group. "
            "Move each entry into the right subsection, replace the placeholder with a "
            "real definition (or a brief placement note for a brand), then re-run "
            "`task glossary:check`."
        )
    return 0


def _group_section(text: str, group: str) -> re.Match | None:
    """Locate a group's `## ` heading, language-independently.

    Matches both ``## `technical` vocabulary`` (en) and ``## Vokabular
    `technical``` (de) — any level-2 heading carrying the backticked group name.
    """
    return re.search(rf"^## .*`{re.escape(group)}`.*$", text, re.MULTILINE)


def _append_stubs(text: str, gaps: list[dict], cfg: dict) -> str:
    """Return ``text`` with missing lemmas under a TODO subsection per group."""
    placeholder, subheading = cfg["placeholder"], cfg["subheading"]
    by_group: dict[str, list[dict]] = {}
    for e in gaps:
        by_group.setdefault(e["group"], []).append(e)

    for group, group_gaps in by_group.items():
        lemmas = sorted({e["lemma"] for e in group_gaps}, key=str.lower)
        block = "\n".join(f"`{lemma}`\n:   {placeholder}\n" for lemma in lemmas)
        subsection = f"{subheading}\n\n{block}"
        match = _group_section(text, group)
        if match is None:
            # Group section absent entirely; append a fresh one at the end.
            heading = cfg["group_heading"].format(group=group)
            text = text.rstrip() + f"\n\n{heading}\n\n{subsection}\n"
            continue
        # Insert before the next `## ` section, or at end of file.
        nxt = text.find("\n## ", match.end())
        insert_at = len(text) if nxt == -1 else nxt + 1
        text = text[:insert_at].rstrip() + "\n\n" + subsection + "\n\n" + text[insert_at:]
    return text.rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-stubs",
        action="store_true",
        help="Scaffold TODO stub entries for uncovered terms instead of just checking.",
    )
    args = parser.parse_args(argv)
    return write_stubs() if args.write_stubs else check()


if __name__ == "__main__":
    raise SystemExit(main())
