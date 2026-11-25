# Stage 1: One green command

**Purpose.** One command tells anyone, human or agent, whether the repository is healthy. It is the same locally and in CI.

**Look.** Which checks exist, how long they take, which fail today, and whether CI can be bypassed.

**Ask.**
- 1.1 What is the command called? (Recommended: `make check`, which runs the template's `make lint` and `make test`.)
- 1.2 Which linter and formatter? Prefer what the repository already uses.
- 1.3 For each failing or flaky test: fix now, set aside with an issue, or delete?
- 1.4 Where does CI run? A public repository uses GitHub-hosted runners only.
- 1.5 What is the time limit for the command? A slow check stops being run.

**Do.** The command, its CI workflow, and the agreed test clean-up.

**Exit check.** The command passes on a clean checkout. A deliberately broken test makes it fail locally and in CI.

**From the template.** `Makefile` (`make lint`, `make test`, and `make check`, which runs both), `tool/lint.sh`, `.github/workflows/ci.yml`.
