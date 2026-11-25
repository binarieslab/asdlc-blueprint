# Stage 3: Verify the real product

**Purpose.** An agent can prove that a feature works for a user, and the owner can see the proof without running anything.

Verification has two parts, and this stage sets up both:

- **Journeys.** Scripted tests that drive the real product through the flows that matter most. They run from a command and in CI, the same way every time.
- **The verification round.** An agent that did not build the change opens the product built from the pull request and does each step a user would, keeping the evidence of each. The template's `verify-app` skill says how to build, start and drive the product; the `verifier` agent decides what to check and posts the verdict.

**Look.**
- How the product can be started and driven without a human, and whether that can run where you work.
- Which test accounts and test data exist.
- What the company's values require here: design, accessibility, languages.
- Whether the flow that earns money can run locally at all. If it cannot (billing switched off outside production, a store purchase), say so and name the closest flow that can.
- Whether the repository already has a verification skill or a verifier. If so it is kept, and this stage fills its gaps.

**Ask.** Two rounds.

Round one:
- 3.1 **Decision.** Which three to five flows get a journey? Start with the one that earns money or the one whose failure would lose a user.
- 3.2 **Decision.** How is the product driven? Propose the stack's own tooling first. A new tool is a dependency and needs its own decision.
- 3.3 **Fact.** Which test accounts and test data are used, and where do they live outside the repository? Production data is never an option.
- 3.7 **Decision.** What evidence is kept, and where: screenshots, a recording, a request and response log?

Round two:
- 3.4 **Accessibility.** Which automated accessibility check runs in each journey, and what does it have to pass?
- 3.5 **Languages.** Which languages are verified, and does a missing or untranslated string fail the run?
- 3.6 **Design.** Where do designs live, and must a feature's issue link the design it implements?

For a profile with no screens, 3.4 and 3.6 are Confirm lines that mark the rows `not applicable`, with what stands in their place (see the table).

**Do.** The agreed journeys, behind one command that the stage 1 command or CI runs. Then fill in the verification skill with the build, start, sign-in and evidence commands, each tried once by hand, and one file under its `features/` for every screen or endpoint a journey reaches.

**Exit check.** One journey runs from the command with nobody at the keyboard and produces its evidence. A deliberately broken flow fails it. An accessibility violation and a missing translation each fail it, where those rows apply. One verification round on a trivial pull request posts a verdict with the evidence of each step.

| Profile | Candidate tooling, to be confirmed against current documentation before proposing | Rows that differ |
| --- | --- | --- |
| `api` | HTTP flows against the locally started service | No screens: accessibility and design are `not applicable`. The evidence of a step is the request and the response, not a screenshot. The language row applies only if responses are localised. |
| `web-static`, `web-app` | A browser automation tool against a local build | All rows apply. |
| `apple-app` | XCUITest on a simulator, including its accessibility audit | All rows apply. |
| `android-app` | Instrumented UI tests on an emulator | All rows apply. |
| `flutter-app` | `integration_test` on a simulator and an emulator, with Flutter's accessibility guideline checks | All rows apply. |
| `library` | Contract tests of the public interface; property-based tests for parsing, cryptography and round-trips | No screens, as for `api`. |

**From the template.** `.claude/skills/verify-app/`, `.claude/agents/verifier.md`, `TESTING_STRATEGY.md`, each only where the repository has no equivalent. Replace `{{PROJECT_NAME}}`, `{{GITHUB_OWNER}}`, `{{REPO}}`, `{{TEST_ACCOUNTS_FILE}}` and `{{DEV_ENVIRONMENT}}`.
