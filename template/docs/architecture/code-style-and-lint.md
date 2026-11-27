# Code style and lint

Rules that matter are enforced by a tool, not by a reminder. A rule in a prompt is a request an agent may or may not follow; a check that fails is a wall it has to get past. `make lint` runs the feature map check and then `tool/lint.sh`: the comment ban, the analyzer and the format check. CI runs the same script as the first job of every pull request, and the tests run only after it passes.

```bash
make lint
```

## No comments in code

Code explains itself through names. Knowledge that does not fit in a name goes into the documentation, where it can be found, reviewed and kept current: `docs/` for how the code works and why it is built that way, `feature-map/` for what the product does. Comments drift, they multiply quickly when agents write code, and an agent copies whatever the repository already does, including a comment that justifies a workaround.

Allowed:

- **Analyzer and formatter directives**, such as `// ignore: <diagnostic>`, `// swiftlint:disable:next <rule>`, `// eslint-disable-next-line <rule>`, `//go:build`, `# noqa: E501` and `# type: ignore`, with rule names only. Prose after a directive is reported.
- **A shebang** on the first line and a Python encoding line on the first two.
- **Generated files** are skipped (`*.g.dart`, `*.pb.go`, `*.generated.*` and the others in `GENERATED_FILES`), and so are dependency and build folders (`SKIP_DIRS`).
- **Optionally, one short doc line** (`///`, at most `DOC_MAX_LENGTH` characters, 100 by default, and not next to another comment), when the owner sets `ALLOW_ONE_LINE_DOC` in the tool. It is off by default.

Not allowed, in any source file the tool knows: comments inside functions, trailing comments, block comments, doc comments, section banners, commented-out code, TODOs, and `// Given`, `// When`, `// Then` markers in tests.

Instead of a comment:

| You wanted to write | Do this instead |
|---|---|
| what a value means (`// 10 seconds because the probe has to finish first`) | name it (`probeTimeout`) and explain the number in the matching doc |
| why the code is shaped this way | the screen doc (`docs/screens/`), the capability doc (`docs/features/`) or a note in `docs/architecture/` |
| a product rule ("a parent may answer for their child") | the feature-map spec; tests may cite its requirement ID in their description |
| a reference to a vendor's or backend's documentation | the matching doc, with the link |
| a TODO or FIXME | a GitHub issue, or the open questions of the matching doc |
| what a test proves | the test's description |
| `// Given / When / Then` | the test description reads as the scenario; blank lines separate setup, action and assertions |
| a disabled block of code | delete it; git keeps it |

The check is `tool/comment_ban.py`, a Python script with no dependencies and its own tests in `tool/tests/` (`make test` runs them). It reads every source file with a known extension, skips strings so that `"https://..."` is not a comment, prints each offending comment as `path:line: comment not allowed: ...` and exits 1:

```bash
python3 tool/comment_ban.py --approved tool/approved_comments.txt .
```

| Option | Effect |
|---|---|
| `--full` | prints the whole text of each reported comment |
| `--approved <file>` | skips the comments the owner approved one by one, as `<path><TAB><JSON-quoted comment>` lines |
| `--write-approved` | owner only: records every comment reported now in the approved file |

It knows Dart, Swift, Kotlin, Scala, Java, Go, JavaScript and TypeScript, C, C++, Objective-C, C#, Rust, Python and Ruby. Its one known blind spot is a JavaScript regular expression literal ending in an escaped slash (`/a\//`), which it reads as the start of a comment; approve that line or write the pattern with `new RegExp(...)`.

`tool/approved_comments.txt` holds only its header line when the ban starts, so nothing is approved, and agents never add to it.

### Adopting it in an existing code base

The first run usually reports hundreds or thousands of comments. Don't approve them all. Move what each comment explains into `docs/` or the feature map first, then delete the comments, so the check passes on the whole repository and new code starts at zero. Record the count you started from below under Baseline.

## Layer boundaries and banned APIs

Describe the dependency rules between your layers or modules and the APIs that must go through one wrapper, and enforce them with a tool rather than a sentence. Options by stack: a small script over the import lines, `dependency-cruiser` or `eslint-plugin-boundaries` for TypeScript, `import-linter` for Python, Gradle module dependencies or Konsist for Kotlin, Swift package targets for Swift, `depguard` in golangci-lint for Go.

| Rule | Where | Reported |
|---|---|---|
| {{layer-import}} | {{src/domain/}} | {{any import outside the domain and its allowed packages}} |

## Analyzer and formatter

| Stack | Analyzer | Format check |
|---|---|---|
| Flutter or Dart | `flutter analyze` (or `dart analyze --fatal-infos`) | `dart format --output=none --set-exit-if-changed .` |
| Swift | `swiftlint --strict` | `swift-format lint --strict --recursive Sources Tests` |
| Kotlin and Android | `./gradlew detekt lint` | `./gradlew ktlintCheck` |
| TypeScript | `npx tsc --noEmit` and `npx eslint . --max-warnings 0` | `npx prettier --check .` |
| Go | `go vet ./...` and `golangci-lint run` | `test -z "$(gofmt -l .)"` |
| Python | `ruff check .` | `ruff format --check .` |

Warnings fail the check as errors do, the tests and `tool/` included. This repository uses: {{ANALYZE_COMMAND}} and {{FORMAT_CHECK_COMMAND}}.

## The scorecard check

`docs/asdlc/scorecard.md` records which parts of the agentic setup are in place, one row each, with a status and its evidence. `make asdlc-verify` keeps that record honest, and the `asdlc-verify` workflow runs it on every pull request:

```bash
make asdlc-verify
```

It fails when:

- a row has a status the scorecard does not know, or a status without evidence;
- the scorecard says "ASDLC-ready since" a date while a row is neither `passed` nor `not applicable`;
- a row is `passed` and the check behind it no longer holds.

The checks behind the rows are listed in `tool/asdlc_checks.json`. Each names a scorecard row by its exact text, a command, and whether that command is expected to `pass` or to `fail`:

```json
{
  "row": "The comment rule fails the check",
  "run": "sh tool/probes/comment_ban.sh",
  "expect": "fail",
  "contains": "comment not allowed"
}
```

A check with `"expect": "fail"` is a probe: it breaks the rule on purpose and passes only if the guard catches it. `tool/probes/comment_ban.sh` is the one to copy. A probe plants its violation in a temporary directory, or removes it again with a `trap`, so the working tree is never left changed. `contains` names text the output must show, so a probe that fails for another reason does not count; a command that cannot be started never counts. A check runs only once its row is `passed` or `passed, not merged`, so it can be written before the row passes. `timeout` sets a limit in seconds; the default is 600.

The tool is `tool/asdlc_verify.py`, a Python script with no dependencies and its own tests in `tool/tests/`. It and `tool/asdlc_checks.json` are protected like the lint rules. Run it through `make`, as the hook blocks calling a script in `tool/` directly. Not every row can have a check: a rollback that was performed, or a merge GitHub refused, stays evidence the owner looked at. And the tool cannot tell an honest edit of the scorecard from one made to get past it, so a pull request that changes a status or the ready date gets the owner's look.

## Who may change the lint rules

Agents never change the lint rules. The protected files are `tool/`, `feature-map/scripts/`, the analyzer configuration ({{ANALYZER_CONFIG}}), `.github/workflows/`, `.claude/settings.json` and `.claude/hooks/`. If a rule or a workflow has to change, the agent says so and the owner makes the change.

Two guards hold this:

- **Claude Code**, through the project's `.claude/settings.json`, for sessions started in this repository. It denies file edits to the protected paths. Its `PreToolUse` hook, `.claude/hooks/protect-lint-rules.sh`, refuses shell commands that write to them (a redirect into them, or `tee`, `sed -i`, `cp`, `mv`, `rm`, an interpreter and the like naming them), that approve comments, or that add the `lint-rules-approved` label. Agents run `gh` as the owner, so GitHub can't tell their label from the owner's; the hook is what keeps them from approving their own change. Reading the files, running `make lint` and `make test`, `git add` and `git commit` pass. The hook needs `jq`; without it, it warns and lets commands through.
- **GitHub**, through `.github/workflows/lint-rules.yml`. When a pull request changes a protected file, its `owner-approval` check fails until the owner ({{OWNER_LOGIN}}) adds the label `lint-rules-approved`. The check reads who added it, so the label counts only when the owner was the last to add it, and a push that still changes a protected file removes it again.

  The workflow runs on `pull_request_target`, which takes the workflow from the base branch rather than from the pull request, so a pull request can't loosen the gate in the same change. It reads the changed files and the label history through the API and never checks out the pull request's code, which is what makes that trigger safe here.

## Documentation is part of the change

`.github/workflows/docs.yml` fails a pull request that changes code without touching `docs/`, `feature-map/`, `README.md`, `AGENTS.md`, `CLAUDE.md` or `TESTING_STRATEGY.md`. Label it `docs-not-needed` only when there really is nothing to document, and say why in its description.

## Feature map

`feature-map/scripts/check.py` keeps the feature map consistent: every spec has its frontmatter with a status for each platform, every spec has a row in `feature-map/INDEX.md` with the same status, related IDs have a row, requirement IDs read `<FEATURE-ID>-NNN` and are unique across the map, and relative links resolve. It uses the Python standard library only. How to write a spec is in [feature-map/AGENTS.md](../../feature-map/AGENTS.md).

```bash
make feature-map
```

## Baseline

{{The date the checks were added, how many comments the comment ban reported then and in how many files, and what happened to them. Each approved exception, and when it was removed.}}
