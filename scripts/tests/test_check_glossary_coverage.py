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


class StubWritingTest(unittest.TestCase):
    def test_stub_lands_in_existing_group_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "glossary.md"
            path.write_text("# Glossary\n\n## `technical` vocabulary\n\n`foo`\n:   Foo.\n",
                            encoding="utf-8")
            gaps = [{"group": "technical", "lemma": "bar"}]
            cgc._append_stubs(path, gaps, "TODO: define", "### Uncovered")
            text = path.read_text(encoding="utf-8")
            self.assertIn("### Uncovered\n\n`bar`\n:   TODO: define", text)
            self.assertEqual(text.count("## `technical` vocabulary"), 1)


if __name__ == "__main__":
    unittest.main()
