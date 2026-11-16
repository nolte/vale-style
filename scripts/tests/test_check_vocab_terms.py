"""Regression tests for scripts/check_vocab_terms.py.

Run with ``task glossary:test`` (``python3 -m unittest discover -s scripts/tests``).
They drive the real ``vale`` binary against fixture vocabularies, because the
property under test is Vale's own Vale.Terms behaviour; without ``vale`` on
``PATH`` they are skipped (the pre-commit hook installs it).
"""

from __future__ import annotations

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import check_vocab_terms as cvt  # noqa: E402


@unittest.skipUnless(shutil.which("vale"), "vale binary not on PATH")
class VocabTermsCheckTest(unittest.TestCase):
    def run_check(self, groups: dict[str, list[str]], allow: dict[str, str] | None = None):
        """Run check() against fixture vocabularies; return (exit code, stderr)."""
        with tempfile.TemporaryDirectory() as tmp:
            styles = Path(tmp) / "styles"
            vocab_root = styles / "config" / "vocabularies"
            for group, entries in groups.items():
                (vocab_root / group).mkdir(parents=True)
                (vocab_root / group / "accept.txt").write_text("\n".join(entries) + "\n")
            allow_path = Path(tmp) / "allow.yml"
            if allow is not None:
                allow_path.write_text(
                    "allow:\n" + "".join(f"  {k!r}: {v}\n" for k, v in allow.items())
                )
            err = io.StringIO()
            with mock.patch.multiple(
                cvt, VOCAB_ROOT=vocab_root, STYLES_PATH=styles, ALLOW_PATH=allow_path
            ), contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                code = cvt.check()
            return code, err.getvalue()

    def test_clean_vocabulary_passes(self):
        code, err = self.run_check({"fx": ["GitHub", "LEDs", "[Kk]amerplanter('?s)?"]})
        self.assertEqual(code, 0, err)

    def test_self_collision_fails(self):
        code, err = self.run_check({"fx": ["kamerplanter", "Kamerplanter('?s)?"]})
        self.assertEqual(code, 1)
        self.assertIn("accepted form 'kamerplanter'", err)

    def test_case_class_vs_uppercase_collision_fails(self):
        code, err = self.run_check({"fx": ["[Tt]odo", "TODOs?"]})
        self.assertEqual(code, 1)
        self.assertIn("accepted form 'TODO'", err)

    def test_ordinary_word_forcing_fails(self):
        code, err = self.run_check({"fx": ["REST", "mS"]})
        self.assertEqual(code, 1)
        self.assertIn("ordinary word 'rest'", err)
        self.assertIn("ordinary word 'ms'", err)

    def test_digit_tokens_are_not_dictionary_words(self):
        code, err = self.run_check({"fx": ["ESP8285", "GPIO(0[0-9]|[1-3][0-9])"]})
        self.assertEqual(code, 0, err)

    def test_case_insensitive_entry_does_not_force(self):
        code, err = self.run_check({"fx": ["(?i)REST"]})
        self.assertEqual(code, 0, err)

    def test_allowlisted_forcing_passes(self):
        code, err = self.run_check({"fx": ["Renovate"]}, allow={"Renovate": "brand casing"})
        self.assertEqual(code, 0, err)

    def test_stale_allowlist_entry_fails(self):
        code, err = self.run_check({"fx": ["GitHub"]}, allow={"GitHub": "brand casing"})
        self.assertEqual(code, 1)
        self.assertIn("no longer forces any word", err)

    def test_unknown_allowlist_entry_fails(self):
        code, err = self.run_check({"fx": ["GitHub"]}, allow={"Gone": "removed"})
        self.assertEqual(code, 1)
        self.assertIn("is not an accept.txt entry", err)

    def test_cross_group_collision_fails(self):
        code, err = self.run_check({"a": ["kamerplanter"], "b": ["Kamerplanter"]})
        self.assertEqual(code, 1)
        self.assertIn("a, b: accepted form 'kamerplanter'", err)

    def test_sentence_initial_lowercase_form_fails(self):
        code, err = self.run_check({"fx": ["cron"]})
        self.assertEqual(code, 1)
        self.assertIn("sentence-initial 'Cron' of accepted form 'cron'", err)

    def test_sentence_initial_case_class_passes(self):
        code, err = self.run_check({"fx": ["[Cc]ron", "arXiv", "baud_rate"]})
        self.assertEqual(code, 0, err)

    def test_capitalised_ordinary_word_forcing_fails(self):
        code, err = self.run_check({"fx": ["MRs"]})
        self.assertEqual(code, 1)
        self.assertIn("entry 'MRs' makes Vale.Terms flag the ordinary word 'Mrs'", err)

    def test_forcing_is_attributed_to_the_reporting_entry(self):
        code, err = self.run_check({"fx": ["Bun", "BUN"]}, allow={"Bun": "brand casing"})
        self.assertEqual(code, 1)
        self.assertIn("entry 'BUN' makes Vale.Terms flag", err)

if __name__ == "__main__":
    unittest.main()
