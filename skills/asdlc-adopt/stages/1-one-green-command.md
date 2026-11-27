# Stage 1: One green command

**Purpose.** One command tells anyone, human or agent, whether the repository is healthy. It is the same locally and in CI.

**Look.**
- Which checks exist, what the repository's own definition of done names, how long each takes, and which fail today.
- Whether every step can fail the command. A loop without `set -e`, or a step whose exit code is dropped, hides errors.
- Whether CI runs that same command, and whether CI can be bypassed. The required checks on the default branch are in the owner's constraints from stage 0; if they are still unknown, ask for them now as a Fact.
- How long the command takes on a clean checkout.

**Ask.** One round. If the commands run only on the owner's machine, 1.3 and 1.5 wait for the output; say so, and ask them when it is there.
- 1.1 **Decision.** What does the command run, and what is it called? Recommend the repository's own definition of done where there is one: lint, the tests, and the build where the stack has one. Keep an existing name; `make check` is the template's name and can be an alias. Never leave two commands that claim to be the gate. If the product ships on a platform whose build the command does not run, make that a Decision of its own: add the build, or record why not.
- 1.2 **Decision.** Which linter and formatter? If an analyzer and a formatter are already configured and nothing suggests changing them, this is a Confirm line. Otherwise prefer what the repository already uses and always offer "a small script of our own, no dependency" as an option: any package is a decision for that exact package. Name the rules that would be switched on, and how many places fail each today.
- 1.3 **Decision**, for each failing or flaky test: fix now, set aside with an issue, or replace. If none fails, say so in a Confirm line.
- 1.4 **Approval** for the exact workflow, `Makefile` and `tool/` files you will change or add, with a Confirm line for where CI runs. A public repository uses GitHub-hosted runners only. Keep the existing CI jobs and add to them. Name the checks the owner has to set as required: the gate's own, and `asdlc-verify`.
- 1.5 **Confirm** the time limit, proposed from the time you measured. A slow check stops being run.

**Do.** The command, its CI workflow, the scorecard check with its own workflow, and the agreed test clean-up. Formatting the whole repository is a mechanical change: its own pull request, proven by a command. For a site or an app, compare the build output before and after with whitespace removed, name what differs, and let the owner decide whether that is enough. Protected files are left unformatted unless the Approval names them.

**Exit check.** `make asdlc-verify` passes, and the `asdlc-verify` workflow runs it on a pull request. The command passes on a clean checkout. A deliberately broken test makes it fail locally and in CI, and so does a deliberate lint violation. The CI half is `built, not run` until a CI run exists; give the owner the steps to prove it.

| Profile | Note |
| --- | --- |
| `api` | The command includes the build of every deployable unit and the infrastructure tests, if the definition of done names them. |
| `web-static`, `web-app` | With no tests yet, the production build is the test step. Say so in the scorecard row. |

**From the template.** `Makefile`, `tool/lint.sh`, `.github/workflows/ci.yml`, each only where the repository has no equivalent. At this stage:
- **Always, whatever the repository already has:** `tool/asdlc_verify.py` with its tests in `tool/tests/`, `tool/asdlc_checks.json`, `tool/probes/`, the `asdlc-verify` target, and the workflow `.github/workflows/asdlc-verify.yml`, which runs `make asdlc-verify` on every pull request. Add the target to the `Makefile` the repository has; if it has none, create one with this target. If the repository keeps its tools in another folder than `tool/`, put these there and change the paths in the target and in the checks file. The workflow sets up no toolchain: add the stack's set-up step to it once a check needs the stack's tools, on the cheapest runner that can run them. The checks file ships with a probe for the template's comment ban; it runs once that row passes, and is removed if the repository keeps a comment checker of its own. From this stage on, each exit check that can run by itself gets an entry there.
- From `tool/lint.sh`, bring the analyzer and format lines only. Its comment ban line belongs to stage 2.
- From the `Makefile`, bring `lint`, `test` and `check` without the `feature-map` prerequisite, which belongs to stage 6. If the repository already runs a feature map check, keep it.
- Replace `{{ANALYZE_COMMAND}}`, `{{FORMAT_CHECK_COMMAND}}` and `{{TEST_COMMAND}}`.
- In `ci.yml`, replace the Flutter toolchain step in both jobs with the stack's own. The template's `docs/architecture/github-workflows.md` lists the step for other stacks.
