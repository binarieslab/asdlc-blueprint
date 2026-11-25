# Stage 0: Baseline

**Purpose.** Know what is there before anything changes. This stage changes no file except the two records it creates.

**Look.**
- The stack, and the commands to build, lint, test and run, each one executed.
- What exists of: lint rules, tests by kind (unit, snapshot, integration, UI) with run time and flaky tests, CI, deploy, docs, analytics and error reporting.
- The third-party dependencies in use.
- The risky areas: payments and purchases, sign-in and accounts, personal data, signing and release configuration, CI and lint configuration, and any interface other software depends on (an API consumed by apps, a library's public interface).
- Patterns an agent must not copy: workarounds, deprecated APIs, dead code, stale TODOs. Give file paths.

**Ask.**
- 0.1 Which profile is this repository?
- 0.2 Which paths are **protected paths**, where every change needs the owner's explicit yes? Propose the list from the risky areas. The template already protects the lint rules, the workflows and the agent settings.
- 0.3 For each "must not copy" pattern: is it intentional, to be removed, or to be kept but forbidden for new code?
- 0.4 Which platforms and versions must keep working?

**Do.** Create `docs/asdlc/scorecard.md` and `docs/asdlc/decisions.md` from this skill's `templates/` folder, in one pull request. Nothing else.

**Exit check.** The owner has confirmed the profile and the protected paths, and both files exist.

**From the template.** None yet. Create the two records from this skill's `templates/` folder.
