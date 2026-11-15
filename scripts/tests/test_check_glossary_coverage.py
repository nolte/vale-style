"""Regression tests for scripts/check_glossary_coverage.py.

Run with ``task glossary:test`` (``python3 -m unittest discover -s scripts/tests``).
Stdlib only, so the gate needs no extra dependency.
"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import check_glossary_coverage as cgc  # noqa: E402


class ExpandRegexTest(unittest.TestCase):
    def test_literal(self):
        self.assertEqual(cgc.expand_regex("MkDocs"), {"MkDocs"})

    def test_case_class_and_optional_suffix(self):
        self.assertEqual(
            cgc.expand_regex("[Aa]gents?"),
            {"Agent", "Agents", "agent", "agents"},
        )

    def test_class_range(self):
        self.assertEqual(cgc.expand_regex("v[1-3]"), {"v1", "v2", "v3"})

    def test_group_alternatives_and_optional_group(self):
        self.assertEqual(
            cgc.expand_regex("[Dd]eduplicat(e|ed)?"),
            {"Deduplicat", "Deduplicate", "Deduplicated",
             "deduplicat", "deduplicate", "deduplicated"},
        )
        self.assertEqual(cgc.expand_regex("Anthropic('s)?"), {"Anthropic", "Anthropic's"})

    def test_unterminated_group_raises(self):
        with self.assertRaises(ValueError):
            cgc.expand_regex("foo(bar")

    def test_escaped_punctuation_is_literal(self):
        self.assertEqual(cgc.expand_regex(r"node\.js"), {"node.js"})
        self.assertEqual(cgc.expand_regex(r"C\+\+"), {"C++"})
        # An escaped "?" is a literal, not the optional quantifier.
        self.assertEqual(cgc.expand_regex(r"why\?"), {"why?"})
        # A real "?" after an escaped atom still makes that atom optional.
        self.assertEqual(cgc.expand_regex(r"back\.?end"), {"back.end", "backend"})

    def test_escapes_inside_a_class(self):
        self.assertEqual(cgc.expand_regex(r"[\.]x"), {".x"})
        self.assertEqual(cgc.expand_regex(r"a[x\-z]"), {"ax", "a-", "az"})
        self.assertEqual(cgc.expand_regex(r"[a\]]b"), {"ab", "]b"})

    def test_unsupported_or_dangling_escape_raises(self):
        for pattern in (r"\d+", "foo\\"):
            with self.subTest(pattern=pattern), self.assertRaises(ValueError):
                cgc.expand_regex(pattern)

    def test_escaped_entry_is_covered_by_its_literal(self):
        keys = cgc.candidate_keys(r"[Nn]ode\.js")
        covered = cgc.glossary_keys("`Node.js`\n:   A JavaScript runtime.\n", "### x")
        self.assertTrue(keys & covered)

    def test_expansion_cap(self):
        with self.assertRaises(cgc.ExpansionTooLarge):
            cgc.expand_regex("[a-z][a-z][a-z]")


class NormalizationTest(unittest.TestCase):
    def test_normalize_key(self):
        self.assertEqual(cgc.normalize_key("Anthropic's"), "anthropic")
        self.assertEqual(cgc.normalize_key("PNGs"), "png")
        self.assertEqual(cgc.normalize_key("s"), "s")

    def test_display_lemma_prefers_shortest_lowercase(self):
        self.assertEqual(cgc.display_lemma("[Aa]gents?"), "agent")
        self.assertEqual(cgc.display_lemma("Anthropic('s)?"), "Anthropic")


class CorpusTest(unittest.TestCase):
    """The shipped vocabularies are fully covered in both glossaries."""

    def test_real_corpus_passes(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = cgc.check()
        self.assertEqual(code, 0, out.getvalue())


class TempRepo:
    """Point the checker at a throwaway vocabulary + glossary pair."""

    def __init__(self, accept: dict[str, str], en: str, de: str):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.vocab = root / "vocab"
        for group, body in accept.items():
            (self.vocab / group).mkdir(parents=True)
            (self.vocab / group / "accept.txt").write_text(body, encoding="utf-8")
        self.en = root / "en.md"
        self.de = root / "de.md"
        self.en.write_text(en, encoding="utf-8")
        self.de.write_text(de, encoding="utf-8")
        self.aliases = root / "aliases.yml"
        self.aliases.write_text("aliases: {}\nignore: []\n", encoding="utf-8")

    def __enter__(self):
        self._saved = (cgc.VOCAB_ROOT, cgc.ALIASES_PATH, cgc.REPO_ROOT,
                       {k: dict(v) for k, v in cgc.GLOSSARIES.items()})
        cgc.VOCAB_ROOT = self.vocab
        cgc.ALIASES_PATH = self.aliases
        cgc.REPO_ROOT = self.vocab.parent
        cgc.GLOSSARIES["en"]["path"] = self.en
        cgc.GLOSSARIES["de"]["path"] = self.de
        return self

    def __exit__(self, *exc):
        cgc.VOCAB_ROOT, cgc.ALIASES_PATH, cgc.REPO_ROOT, glossaries = self._saved
        for k, v in glossaries.items():
            cgc.GLOSSARIES[k] = v
        self._tmp.cleanup()


def run_quiet(fn):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = fn()
    return code, out.getvalue()


EN_HEAD = "# Glossary\n\n## `technical` vocabulary\n\n"
DE_HEAD = "# Glossar\n\n## Vokabular `technical`\n\n"


class GapReportingTest(unittest.TestCase):
    def test_gap_is_reported_per_language(self):
        with TempRepo({"technical": "[Ff]oo\nbar\n"},
                      EN_HEAD + "`foo`\n:   Foo.\n",
                      DE_HEAD + "`foo`\n:   Foo.\n\n`bar`\n:   Bar.\n"):
            code, out = run_quiet(cgc.check)
        self.assertEqual(code, 1)
        self.assertIn("✗ en.md: 1 accept.txt term(s) without a glossary entry:", out)
        self.assertIn("[technical] bar  (lemma: bar)", out)
        self.assertIn("✓ de.md: all 2 vocabulary terms covered", out)

    def test_each_glossary_is_read_once(self):
        with TempRepo({"technical": "bar\n"}, EN_HEAD, DE_HEAD):
            reads = []
            original = Path.read_text

            def counting(self, *a, **kw):
                reads.append(self.name)
                return original(self, *a, **kw)

            Path.read_text = counting
            try:
                run_quiet(cgc.write_stubs)
            finally:
                Path.read_text = original
        self.assertEqual(reads.count("en.md"), 1)
        self.assertEqual(reads.count("de.md"), 1)


class CoveredLemmaTest(unittest.TestCase):
    HEADING = "### Inflected and possessive forms"

    def keys(self, text):
        return cgc.glossary_keys(text, self.HEADING)

    def test_definition_term_lines_count(self):
        text = "`foo`\n:   Foo.\n\n`MUSTs` / `SHOULDs`\n\n:   Keywords.\n"
        self.assertEqual(self.keys(text), {"foo", "must", "should"})

    def test_prose_mention_does_not_count(self):
        text = ("## `technical` vocabulary\n\n"
                "Terms such as `superset` appear below.\n\n"
                "`foo`\n:   Unlike a `superset`, see `git commit`.\n")
        self.assertEqual(self.keys(text), {"foo"})

    def test_definition_continuation_line_does_not_count(self):
        text = "`foo`\n:   First.\n    see `bar`\n:   Second.\n"
        self.assertEqual(self.keys(text), {"foo"})

    def test_allowlisted_prose_block_counts_until_next_heading(self):
        text = (self.HEADING + "\n\nForms: `commit's`, `rebased`.\n\n"
                "## `esphome` vocabulary\n\nIntro with `later`.\n")
        self.assertEqual(self.keys(text), {"commit", "rebased"})

    def test_other_heading_is_not_allowlisted(self):
        text = "### Some other forms\n\nForms: `commit's`.\n"
        self.assertEqual(self.keys(text), set())

    def test_real_glossaries_carry_the_configured_heading(self):
        for lang, cfg in cgc.GLOSSARIES.items():
            with self.subTest(lang=lang):
                lines = cfg["path"].read_text(encoding="utf-8").splitlines()
                self.assertIn(cfg["covering_prose_heading"], lines)


class StubWritingTest(unittest.TestCase):
    def test_stub_lands_in_existing_group_section(self):
        with TempRepo({"technical": "bar\n"}, EN_HEAD + "`foo`\n:   Foo.\n", DE_HEAD):
            run_quiet(cgc.write_stubs)
            text = cgc.GLOSSARIES["en"]["path"].read_text(encoding="utf-8")
            self.assertIn("`bar`\n:   TODO: define", text)
            self.assertEqual(text.count("## `technical` vocabulary"), 1)
            code, _ = run_quiet(cgc.check)
        self.assertEqual(code, 0)

    def test_new_group_gets_a_localized_heading_and_self_heals(self):
        with TempRepo({"technical": "foo\n", "esphome": "bar\n"},
                      EN_HEAD + "`foo`\n:   Foo.\n",
                      DE_HEAD + "`foo`\n:   Foo.\n"):
            run_quiet(cgc.write_stubs)
            en = cgc.GLOSSARIES["en"]["path"].read_text(encoding="utf-8")
            de = cgc.GLOSSARIES["de"]["path"].read_text(encoding="utf-8")
            self.assertIn("\n## `esphome` vocabulary\n", en)
            self.assertIn("\n## Vokabular `esphome`\n", de)
            self.assertNotIn("vocabulary", de)
            # A second gap in the same new group lands under the existing
            # section instead of creating a duplicate heading.
            accept = cgc.VOCAB_ROOT / "esphome" / "accept.txt"
            accept.write_text("bar\nbaz\n", encoding="utf-8")
            run_quiet(cgc.write_stubs)
            de = cgc.GLOSSARIES["de"]["path"].read_text(encoding="utf-8")
        self.assertEqual(de.count("## Vokabular `esphome`"), 1)
        self.assertIn("`baz`\n:   TODO: definieren", de)


if __name__ == "__main__":
    unittest.main()
