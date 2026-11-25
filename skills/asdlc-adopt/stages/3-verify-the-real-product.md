# Stage 3: Verify the real product

**Purpose.** An agent can prove that a feature works for a user, and the owner can see the proof without running anything.

Verification has two parts, and this stage sets up both:

- **Journeys.** Scripted tests that drive the real product through the flows that matter most. They run from a command and in CI, the same way every time.
- **The verification round.** An agent that did not build the change opens the product built from the pull request and does each step a user would, keeping a screenshot of each. The template's `verify-app` skill says how to build, start and drive the product; the `verifier` agent decides what to check and posts the verdict.

**Look.** How the product can be started and driven without a human; which test accounts and test data exist; what the company's values require here (design, accessibility, languages).

**Ask.**
- 3.1 Which three to five flows get a journey? Start with the one that earns money or the one whose failure would lose a user.
- 3.2 How is the product driven? Propose the stack's own tooling first.
- 3.3 Which test accounts and test data are used, and where do they live outside the repository? Production data is never an option.
- 3.4 **Accessibility.** Which automated accessibility check runs in each journey, and what does it have to pass?
- 3.5 **Languages.** Which languages are verified, and does a missing or untranslated string fail the run?
- 3.6 **Design.** Where do designs live, and must a feature's issue link the design it implements?
- 3.7 What evidence is kept, and where: screenshots, a recording, a log?

**Do.** The agreed journeys, behind one command. Then fill in `verify-app` with the build, start, sign-in and screenshot commands, each tried once by hand, and one file under its `features/` for every screen a journey reaches.

**Exit check.** One journey runs from the command with nobody at the keyboard and produces its evidence. A deliberately broken flow fails it. An accessibility violation and a missing translation each fail it. One verification round on a trivial pull request posts a verdict with a screenshot per step.

| Profile | Candidate tooling, to be confirmed against current documentation before proposing |
| --- | --- |
| `api` | HTTP flows against the locally started service |
| `web-static`, `web-app` | A browser automation tool against a local build |
| `apple-app` | XCUITest on a simulator, including its accessibility audit |
| `android-app` | Instrumented UI tests on an emulator |
| `flutter-app` | `integration_test` on a simulator and an emulator, with Flutter's accessibility guideline checks |
| `library` | Contract tests of the public interface; property-based tests for parsing, cryptography and round-trips |

**From the template.** `.claude/skills/verify-app/`, `.claude/agents/verifier.md`, `TESTING_STRATEGY.md`.
