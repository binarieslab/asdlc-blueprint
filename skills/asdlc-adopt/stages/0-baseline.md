# Stage 0: Baseline

**Purpose.** Know what is there before anything changes. This stage changes no file except the two records it creates.

**Look.**
- The repository's own instructions and docs: `AGENTS.md`, `CLAUDE.md`, the README, the docs index.
- The stack, and the commands to build, lint, test and run. Each one is executed, or marked "not run" with the reason. Compare the commands the repository's instructions name with the targets that exist, and report any that is named but missing.
- What exists of: lint rules, tests by kind (unit, snapshot, integration, UI) with run time and flaky tests, CI, deploy, docs, analytics and error reporting.
- The third-party dependencies in use: the direct ones, counted per ecosystem with a tool.
- The risky areas: payments and purchases, sign-in and accounts, personal data, signing and release configuration, CI and lint configuration.
- What other software depends on: an API consumed by apps, a library's public interface, a script bundle or feed another site loads.
- Where the template's files would land (`Makefile`, `tool/`, `.github/workflows/`, `.claude/`), and which of them already have an equivalent here.
- Tracked files that look like credentials or signing material: keystores, certificates, `.env` files. List them by path with `git ls-files`. Never open them. They go under "Known gaps" for stages 4 and 5.
- Patterns an agent must not copy: workarounds, deprecated APIs, dead code, stale TODOs. Give file paths and a count for each.

**Ask.** One round.
- 0.1 **Confirm** the profile. Make it a Decision only if two profiles fit.
- 0.2 **Decision.** Which paths are **protected paths**, where every change needs the owner's Approval? Start from the lint and check configuration, the check tools, the `Makefile` that defines the gate, the CI workflows and the agent settings and hooks, which is where the template's files land. Add the risky areas you found. Leave `docs/asdlc/` out: every stage writes there. The owner may also mark paths **off limits**: you never open them, and no Approval covers them.
- 0.3 **Decision**, one line per pattern: intentional, to be removed, or kept but forbidden for new code. Ask about the five most copied; list the rest under "Details". If you found none, say so in a Confirm line. A removal happens in stage 2, or in a side pull request if the owner wants it sooner.
- 0.4 **Confirm** the platforms and versions that must keep working, from the repository's configuration. Name every platform the product ships on, the web included.
- 0.5 **Facts: the owner's constraints.** The GitHub plan and number of seats; whether the repository is public or private; whether the default branch is protected, which checks it requires and whether it requires signed commits; when CI last ran green and whether runs start today; the owner's GitHub login; the rule on paid services and new accounts; and where the repository's commands can run if they cannot run where you work.

**Do.** Create `docs/asdlc/scorecard.md` and `docs/asdlc/decisions.md` from this skill's `templates/` folder, in one pull request. They hold this stage's decisions, the owner's constraints from 0.5, and under "Known gaps" anything you found that is not this stage's to fix (for example dependency audit findings). Nothing else changes.

**Exit check.** The owner has confirmed the profile and the protected paths. Both files exist. The owner's constraints are recorded, and each one still unknown is listed as an open item.

**From the template.** None yet. Create the two records from this skill's `templates/` folder.
