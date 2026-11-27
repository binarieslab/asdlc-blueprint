from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asdlc_verify
from asdlc_verify import parse_scorecard, record_problems

HEADER = "# ASDLC scorecard\n\nProfile: api\nASDLC-ready since: {ready}\n\n"
STATUS_TABLE = "## Statuses\n\n| Status | Meaning |\n| --- | --- |\n| `passed` | It ran. |\n\n"
ROWS_TABLE = "## Rows\n\n| Stage | Row | Status | Evidence |\n| --- | --- | --- | --- |\n"
GAPS_TABLE = "\n## Known gaps\n\n| Found in stage | Gap | Owner's decision |\n| --- | --- | --- |\n| 0 | An audit finding | Later |\n"


def scorecard_text(rows: list[tuple[str, str, str, str]], ready: str = "") -> str:
    lines = "".join(f"| {stage} | {name} | {status} | {evidence} |\n" for stage, name, status, evidence in rows)
    return HEADER.format(ready=ready) + STATUS_TABLE + ROWS_TABLE + lines + GAPS_TABLE


def run_tool(directory: Path, rows, checks=None, ready: str = "", extra: list[str] | None = None) -> tuple[int, str]:
    scorecard = directory / "scorecard.md"
    scorecard.write_text(scorecard_text(rows, ready), encoding="utf-8")
    arguments = ["--scorecard", str(scorecard), "--root", str(directory), "--checks", str(directory / "checks.json")]
    if checks is not None:
        (directory / "checks.json").write_text(json.dumps({"checks": checks}), encoding="utf-8")
    output = StringIO()
    with redirect_stdout(output), redirect_stderr(StringIO()):
        code = asdlc_verify.main(arguments + (extra or []))
    return code, output.getvalue()


class ParsingTests(unittest.TestCase):
    def test_only_the_rows_table_is_read(self):
        text = scorecard_text([("1", "One command", "`passed`", "make check, exit 0"), ("2", "Comments", "", "")])
        scorecard = parse_scorecard(text)
        self.assertEqual([row.name for row in scorecard.rows], ["One command", "Comments"])
        self.assertEqual(scorecard.rows[0].status, "passed")
        self.assertEqual(scorecard.rows[1].status, "")

    def test_the_ready_date_is_read(self):
        self.assertEqual(parse_scorecard(scorecard_text([], ready="2026-12-01")).ready_since, "2026-12-01")
        self.assertEqual(parse_scorecard(scorecard_text([])).ready_since, "")


class RecordTests(unittest.TestCase):
    def problems(self, rows, ready: str = "") -> list[str]:
        return record_problems(parse_scorecard(scorecard_text(rows, ready)))

    def test_open_rows_are_not_a_problem(self):
        self.assertEqual(self.problems([("1", "One command", "", "")]), [])

    def test_an_unknown_status_is_reported(self):
        problems = self.problems([("1", "One command", "yes", "it works")])
        self.assertEqual(len(problems), 1)
        self.assertIn('"yes" is not a status', problems[0])

    def test_a_status_without_evidence_is_reported(self):
        problems = self.problems([("1", "One command", "`passed`", "")])
        self.assertIn("has no evidence", problems[0])

    def test_a_row_named_twice_is_reported(self):
        problems = self.problems([("1", "One command", "", ""), ("1", "One command", "", "")])
        self.assertIn("appears twice", problems[0])

    def test_no_rows_at_all_is_reported(self):
        self.assertIn("no rows found", self.problems([])[0])

    def test_ready_holds_when_every_row_passed_or_does_not_apply(self):
        rows = [("1", "One command", "`passed`", "make check"), ("3", "Design", "`not applicable`", "no screens")]
        self.assertEqual(self.problems(rows, ready="2026-12-01"), [])

    def test_ready_with_a_row_that_is_not_done_is_reported(self):
        rows = [("1", "One command", "`passed`", "make check"), ("4", "Rollback", "`waiting for owner`", "tonight")]
        problems = self.problems(rows, ready="2026-12-01")
        self.assertEqual(len(problems), 1)
        self.assertIn('row "Rollback" is waiting for owner', problems[0])

    def test_ready_with_an_open_row_is_reported(self):
        problems = self.problems([("2", "Comments", "", "")], ready="2026-12-01")
        self.assertIn('row "Comments" is open', problems[0])


class RunTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_a_missing_scorecard_fails(self):
        output = StringIO()
        with redirect_stdout(output), redirect_stderr(StringIO()):
            code = asdlc_verify.main(["--scorecard", str(self.directory / "none.md")])
        self.assertEqual(code, 1)
        self.assertIn("not found", output.getvalue())

    def test_a_scorecard_with_no_checks_file_passes(self):
        code, output = run_tool(self.directory, [("1", "One command", "`passed`", "make check")])
        self.assertEqual((code, output), (0, ""))

    def test_a_passing_check_on_a_passed_row_passes(self):
        checks = [{"row": "One command", "run": "exit 0", "expect": "pass"}]
        code, _ = run_tool(self.directory, [("1", "One command", "`passed`", "make check")], checks)
        self.assertEqual(code, 0)

    def test_a_check_that_should_pass_and_fails_is_reported(self):
        checks = [{"row": "One command", "run": "exit 3", "expect": "pass"}]
        code, output = run_tool(self.directory, [("1", "One command", "`passed`", "make check")], checks)
        self.assertEqual(code, 1)
        self.assertIn("should pass and exited 3", output)

    def test_a_check_that_should_fail_and_passes_is_reported(self):
        checks = [{"row": "Comments", "run": "exit 0", "expect": "fail"}]
        code, output = run_tool(self.directory, [("2", "Comments", "`passed`", "planted comment")], checks)
        self.assertEqual(code, 1)
        self.assertIn("should fail and passed", output)

    def test_a_check_that_fails_as_expected_passes(self):
        checks = [{"row": "Comments", "run": "echo 'comment not allowed'; exit 1", "expect": "fail", "contains": "comment not allowed"}]
        code, _ = run_tool(self.directory, [("2", "Comments", "`passed, not merged`", "branch stage-2")], checks)
        self.assertEqual(code, 0)

    def test_a_failure_without_the_expected_text_is_reported(self):
        checks = [{"row": "Comments", "run": "echo 'something else'; exit 1", "expect": "fail", "contains": "comment not allowed"}]
        code, output = run_tool(self.directory, [("2", "Comments", "`passed`", "planted comment")], checks)
        self.assertEqual(code, 1)
        self.assertIn('did not print "comment not allowed"', output)

    def test_a_command_that_does_not_exist_is_not_a_failure_that_counts(self):
        checks = [{"row": "Comments", "run": "no-such-command-asdlc", "expect": "fail"}]
        code, output = run_tool(self.directory, [("2", "Comments", "`passed`", "planted comment")], checks)
        self.assertEqual(code, 1)
        self.assertIn("could not be started", output)

    def test_a_check_for_a_row_that_has_not_passed_is_not_run(self):
        marker = self.directory / "ran"
        checks = [{"row": "Comments", "run": f"touch {marker}", "expect": "pass"}]
        code, _ = run_tool(self.directory, [("2", "Comments", "`built, not run`", "branch stage-2")], checks)
        self.assertEqual(code, 0)
        self.assertFalse(marker.exists())

    def test_no_run_checks_the_records_and_runs_nothing(self):
        marker = self.directory / "ran"
        checks = [{"row": "One command", "run": f"touch {marker}", "expect": "pass"}]
        code, _ = run_tool(self.directory, [("1", "One command", "`passed`", "make check")], checks, extra=["--no-run"])
        self.assertEqual(code, 0)
        self.assertFalse(marker.exists())

    def test_a_check_runs_in_the_root(self):
        (self.directory / "present.txt").write_text("x", encoding="utf-8")
        checks = [{"row": "One command", "run": "test -f present.txt", "expect": "pass"}]
        code, _ = run_tool(self.directory, [("1", "One command", "`passed`", "make check")], checks)
        self.assertEqual(code, 0)

    def test_a_check_for_a_row_the_scorecard_does_not_have_is_reported(self):
        checks = [{"row": "A row that was renamed", "run": "exit 0", "expect": "pass"}]
        code, output = run_tool(self.directory, [("1", "One command", "`passed`", "make check")], checks)
        self.assertEqual(code, 1)
        self.assertIn('no scorecard row is called "A row that was renamed"', output)

    def test_a_check_that_runs_too_long_is_reported(self):
        checks = [{"row": "One command", "run": "sleep 5", "expect": "pass", "timeout": 1}]
        code, output = run_tool(self.directory, [("1", "One command", "`passed`", "make check")], checks)
        self.assertEqual(code, 1)
        self.assertIn("did not finish in time", output)

    def test_a_malformed_check_is_reported(self):
        checks = [{"row": "One command", "run": "exit 0", "expect": "maybe"}, {"row": "One command"}]
        code, output = run_tool(self.directory, [("1", "One command", "`passed`", "make check")], checks)
        self.assertEqual(code, 1)
        self.assertIn('"expect" must be "pass" or "fail"', output)
        self.assertIn('needs a "row" and a "run" command', output)

    def test_a_checks_file_that_is_not_json_is_reported(self):
        (self.directory / "checks.json").write_text("{not json", encoding="utf-8")
        code, output = run_tool(self.directory, [("1", "One command", "`passed`", "make check")])
        self.assertEqual(code, 1)
        self.assertIn("not valid JSON", output)

    def test_ready_fails_when_a_check_no_longer_holds(self):
        checks = [{"row": "Comments", "run": "exit 0", "expect": "fail"}]
        rows = [("1", "One command", "`passed`", "make check"), ("2", "Comments", "`passed`", "planted comment")]
        code, output = run_tool(self.directory, rows, checks, ready="2026-12-01")
        self.assertEqual(code, 1)
        self.assertIn("its check no longer holds", output)


if __name__ == "__main__":
    unittest.main()
