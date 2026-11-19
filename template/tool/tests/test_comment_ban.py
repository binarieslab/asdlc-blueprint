from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import comment_ban
from comment_ban import LANGUAGES, check_source


def reported(source: str, language: str) -> list[tuple[int, str]]:
    return [(comment.line, comment.text.strip()) for comment in check_source(source, LANGUAGES[language])]


class LineCommentTests(unittest.TestCase):
    def test_a_line_comment_is_reported_with_its_line(self):
        source = "final a = 1;\nfinal b = 2; // the second value\n"
        self.assertEqual(reported(source, "dart"), [(2, "// the second value")])

    def test_a_comment_marker_inside_a_string_is_not_a_comment(self):
        source = 'const url = "https://example.com/path";\nconst s = \'/* not */\';\n'
        self.assertEqual(reported(source, "javascript"), [])

    def test_an_escaped_quote_does_not_end_the_string(self):
        source = 'let s = "a \\" // still the string";\n'
        self.assertEqual(reported(source, "swift"), [])

    def test_an_unterminated_string_ends_at_the_line_break(self):
        source = 'val s = "open\n// a real comment\n'
        self.assertEqual(reported(source, "kotlin"), [(2, "// a real comment")])

    def test_a_python_hash_comment_is_reported(self):
        self.assertEqual(reported("x = 1  # explain x\n", "python"), [(1, "# explain x")])

    def test_a_hash_inside_a_python_string_is_not_a_comment(self):
        self.assertEqual(reported('tag = "#release"\nother = f"{tag}#1"\n', "python"), [])


class BlockCommentTests(unittest.TestCase):
    def test_a_block_comment_is_reported_once_at_its_first_line(self):
        source = "int a;\n/* first\n   second */\nint b;\n"
        self.assertEqual(reported(source, "c"), [(2, "/* first\n   second */")])

    def test_nested_block_comments_end_at_the_outer_closer(self):
        source = "/* outer /* inner */ still outer */\nlet x = 1\n"
        self.assertEqual(len(reported(source, "swift")), 1)
        self.assertEqual(reported(source, "swift")[0][0], 1)

    def test_lines_after_a_block_comment_keep_their_numbers(self):
        source = "/*\n\n*/\nconst a = 1; // here\n"
        self.assertEqual(reported(source, "javascript")[-1], (4, "// here"))


class StringTests(unittest.TestCase):
    def test_a_python_docstring_with_a_hash_is_a_string(self):
        source = 'def f():\n    """Returns # of items."""\n    return 1\n'
        self.assertEqual(reported(source, "python"), [])

    def test_a_go_raw_string_ignores_backslashes_and_markers(self):
        source = "var p = `C:\\path // not a comment`\n"
        self.assertEqual(reported(source, "go"), [])

    def test_a_javascript_template_literal_spans_lines(self):
        source = "const t = `line one\n// still the template\n`;\n"
        self.assertEqual(reported(source, "javascript"), [])

    def test_a_dart_raw_string_ends_at_its_quote_after_a_backslash(self):
        source = "final p = r'C:\\';\nfinal q = 1; // after\n"
        self.assertEqual(reported(source, "dart"), [(2, "// after")])

    def test_a_rust_lifetime_does_not_open_a_string(self):
        source = "fn f<'a>(x: &'a str) {}\n// a comment\n"
        self.assertEqual(reported(source, "rust"), [(2, "// a comment")])


class AllowedTests(unittest.TestCase):
    def test_analyzer_and_formatter_directives_are_allowed(self):
        source = "\n".join(
            [
                "// ignore: avoid_print",
                "// ignore_for_file: type=lint, unused_import",
                "// swiftlint:disable:next force_cast",
                "// eslint-disable-next-line no-console",
                "//go:build linux",
                "// @ts-expect-error",
            ]
        )
        for language in ("dart", "swift", "javascript", "go"):
            self.assertEqual(reported(source, language), [], language)

    def test_a_directive_followed_by_prose_is_reported(self):
        self.assertEqual(len(reported("// ignore: avoid_print because we debug here\n", "dart")), 1)

    def test_a_shebang_and_an_encoding_line_are_allowed(self):
        source = "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nimport os\n"
        self.assertEqual(reported(source, "python"), [])

    def test_a_shebang_after_the_first_line_is_reported(self):
        self.assertEqual(len(reported("import os\n#!/bin/sh\n", "python")), 1)

    def test_doc_comments_are_reported_while_one_line_docs_are_off(self):
        self.assertEqual(len(reported("/// Reads the session.\nabstract class S {}\n", "dart")), 1)

    def test_a_single_short_doc_comment_is_allowed_when_one_line_docs_are_on(self):
        original = comment_ban.ALLOW_ONE_LINE_DOC
        comment_ban.ALLOW_ONE_LINE_DOC = True
        try:
            self.assertEqual(reported("/// Reads the session.\nabstract class S {}\n", "dart"), [])
            self.assertEqual(len(reported("/// One.\n/// Two.\nabstract class S {}\n", "dart")), 2)
            self.assertEqual(len(reported("/// " + "x" * 100 + "\nabstract class S {}\n", "dart")), 1)
        finally:
            comment_ban.ALLOW_ONE_LINE_DOC = original


class CommandLineTests(unittest.TestCase):
    def run_main(self, arguments: list[str]) -> tuple[int, str]:
        output = StringIO()
        with redirect_stdout(output), redirect_stderr(StringIO()):
            status = comment_ban.main(arguments)
        return status, output.getvalue()

    def test_a_clean_tree_passes_and_a_comment_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, "a.ts").write_text("export const a = 1;\n", encoding="utf-8")
            Path(folder, "b.g.dart").write_text("// generated\n", encoding="utf-8")
            self.assertEqual(self.run_main([folder])[0], 0)
            Path(folder, "c.go").write_text("package c // why\n", encoding="utf-8")
            status, output = self.run_main([folder])
            self.assertEqual(status, 1)
            self.assertIn("c.go:1: comment not allowed: // why", output)

    def test_skipped_folders_are_not_scanned(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, "node_modules").mkdir()
            Path(folder, "node_modules", "x.js").write_text("// vendor\n", encoding="utf-8")
            self.assertEqual(self.run_main([folder])[0], 0)

    def test_an_approved_comment_passes(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder, "a.swift")
            source.write_text("let a = 1 // approved one\n", encoding="utf-8")
            approved = Path(folder, "approved.txt")
            file = comment_ban.display_path(source)
            approved.write_text(
                "# header\n" + file + "\t" + json.dumps("// approved one") + "\n",
                encoding="utf-8",
            )
            self.assertEqual(self.run_main(["--approved", str(approved), folder])[0], 0)

    def test_write_approved_records_every_reported_comment(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, "a.kt").write_text("val a = 1 // one\nval b = 2 // two\n", encoding="utf-8")
            approved = Path(folder, "approved.txt")
            self.assertEqual(self.run_main(["--approved", str(approved), "--write-approved", folder])[0], 0)
            self.assertEqual(len(approved.read_text(encoding="utf-8").splitlines()), 3)
            self.assertEqual(self.run_main(["--approved", str(approved), folder])[0], 0)


if __name__ == "__main__":
    unittest.main()
