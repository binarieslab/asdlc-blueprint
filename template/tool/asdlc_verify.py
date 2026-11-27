#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

STATUSES = (
    "",
    "built, not run",
    "waiting for owner",
    "passed, not merged",
    "passed",
    "accepted, not verified",
    "not applicable",
)
DONE = ("passed", "not applicable")
RERUN = ("passed", "passed, not merged")
READY_LABEL = "ASDLC-ready since:"
ROWS_HEADING = "## Rows"
NOT_STARTED = (126, 127)
DEFAULT_TIMEOUT = 600


@dataclass(frozen=True)
class Row:
    stage: str
    name: str
    status: str
    evidence: str


@dataclass(frozen=True)
class Scorecard:
    ready_since: str
    rows: list[Row]


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_scorecard(text: str) -> Scorecard:
    ready_since = ""
    rows: list[Row] = []
    in_rows = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(READY_LABEL):
            ready_since = stripped[len(READY_LABEL):].strip()
        if stripped.startswith("## "):
            in_rows = stripped == ROWS_HEADING
            continue
        if not in_rows or not stripped.startswith("|"):
            continue
        cells = _cells(stripped)
        if len(cells) != 4 or not cells[0].isdigit():
            continue
        rows.append(Row(cells[0], cells[1], cells[2].strip("`").strip(), cells[3]))
    return Scorecard(ready_since, rows)


def record_problems(scorecard: Scorecard) -> list[str]:
    problems: list[str] = []
    if not scorecard.rows:
        problems.append(f'no rows found under "{ROWS_HEADING}"')
    seen: set[str] = set()
    for row in scorecard.rows:
        if row.name in seen:
            problems.append(f'row "{row.name}" appears twice')
        seen.add(row.name)
        if row.status not in STATUSES:
            problems.append(f'row "{row.name}": "{row.status}" is not a status the scorecard knows')
        elif row.status and not row.evidence:
            problems.append(f'row "{row.name}": status "{row.status}" has no evidence')
    if scorecard.ready_since:
        for row in scorecard.rows:
            if row.status in STATUSES and row.status not in DONE:
                shown = row.status or "open"
                problems.append(
                    f'the scorecard says ASDLC-ready since {scorecard.ready_since}, but row "{row.name}" is {shown}'
                )
    return problems


def read_checks(path: Path) -> tuple[list[dict], list[str]]:
    if not path.exists():
        return [], []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [], [f"{path}: not valid JSON ({error})"]
    checks = data.get("checks") if isinstance(data, dict) else None
    if not isinstance(checks, list):
        return [], [f'{path}: expected an object with a "checks" list']
    problems: list[str] = []
    valid: list[dict] = []
    for index, check in enumerate(checks, start=1):
        where = f"{path}: check {index}"
        if not isinstance(check, dict):
            problems.append(f"{where}: expected an object")
            continue
        if not isinstance(check.get("row"), str) or not isinstance(check.get("run"), str) or not check["run"].strip():
            problems.append(f'{where}: needs a "row" and a "run" command')
            continue
        if check.get("expect") not in ("pass", "fail"):
            problems.append(f'{where}: "expect" must be "pass" or "fail"')
            continue
        if "contains" in check and not isinstance(check["contains"], str):
            problems.append(f'{where}: "contains" must be text')
            continue
        if "timeout" in check and not (isinstance(check["timeout"], int) and check["timeout"] > 0):
            problems.append(f'{where}: "timeout" must be a number of seconds above zero')
            continue
        valid.append(check)
    return valid, problems


def run_check(check: dict, root: Path) -> str | None:
    command = check["run"]
    process = subprocess.Popen(
        command,
        shell=True,
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        start_new_session=True,
    )
    try:
        output, _ = process.communicate(timeout=check.get("timeout", DEFAULT_TIMEOUT))
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.communicate()
        return f"`{command}` did not finish in time"
    code = process.returncode
    if code in NOT_STARTED:
        return f"`{command}` could not be started (exit {code})"
    if check["expect"] == "pass" and code != 0:
        return f"`{command}` should pass and exited {code}"
    if check["expect"] == "fail" and code == 0:
        return f"`{command}` should fail and passed"
    wanted = check.get("contains")
    if wanted and wanted not in output:
        return f'`{command}` did not print "{wanted}"'
    return None


def verify(scorecard_path: Path, checks_path: Path, root: Path, run: bool) -> tuple[list[str], str]:
    if not scorecard_path.exists():
        return [f"{scorecard_path}: not found; the scorecard is created in stage 0 of the adoption"], ""
    scorecard = parse_scorecard(scorecard_path.read_text(encoding="utf-8"))
    problems = [f"{scorecard_path}: {problem}" for problem in record_problems(scorecard)]
    checks, check_problems = read_checks(checks_path)
    problems += check_problems
    rows = {row.name: row for row in scorecard.rows}
    ran = 0
    waiting = 0
    for check in checks:
        row = rows.get(check["row"])
        if row is None:
            problems.append(f'{checks_path}: no scorecard row is called "{check["row"]}"')
            continue
        if row.status not in RERUN:
            waiting += 1
            continue
        if not run:
            continue
        ran += 1
        failure = run_check(check, root)
        if failure:
            problems.append(f'row "{row.name}" is {row.status}, but its check no longer holds: {failure}')
    done = sum(1 for row in scorecard.rows if row.status in DONE)
    summary = (
        f"{len(scorecard.rows)} row(s): {done} passed or not applicable, {len(scorecard.rows) - done} not yet; "
        f"{ran} check(s) run, {waiting} waiting for their row to pass"
    )
    return problems, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Checks the ASDLC scorecard and runs again the checks behind its passed rows."
    )
    parser.add_argument("--scorecard", default="docs/asdlc/scorecard.md")
    parser.add_argument("--checks", default="tool/asdlc_checks.json")
    parser.add_argument("--root", default=".", help="the directory the checks run in")
    parser.add_argument("--no-run", action="store_true", help="check the records only, run nothing")
    arguments = parser.parse_args(argv)

    problems, summary = verify(
        Path(arguments.scorecard), Path(arguments.checks), Path(arguments.root), not arguments.no_run
    )
    for problem in problems:
        print(problem)
    if summary:
        print(summary, file=sys.stderr)
    if problems:
        print(
            "The scorecard no longer matches the repository. Fix what broke, or ask the owner to reopen the row; "
            "never edit a status to make this pass.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
