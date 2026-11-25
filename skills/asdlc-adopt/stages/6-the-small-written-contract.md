# Stage 6: The small written contract

**Purpose.** The weakest layer, kept small. Only what no check can express is written down.

**Look.** What an agent still could not know after stages 1 to 5: the purpose of the product, its users, intent behind unusual code, where things are.

**Ask.**
- 6.1 Here is a draft `AGENTS.md` of at most 120 lines. Which rules are missing, and which can go because a check now enforces them?
- 6.2 Here is the proposed structure for the technical docs, the decision log and the feature map. How fine-grained should the feature map be?
- 6.3 **The profit rule.** Which line must every feature issue carry before it may be built: the expected effect on revenue or retention, or the cost of the defect? What is its kill criterion?
- 6.4 Which sections does the feature issue template have? The blueprint's template carries the need, the user experience, the technical context, the acceptance criteria and the test scenarios. Say what this repository adds or drops, for example the design link and the feature flag.

**Do.** `AGENTS.md`, the docs skeleton, the feature map for the journeys from stage 3, the issue templates.

**Exit check.** No rule in `AGENTS.md` duplicates a check. Each journey from stage 3 has a feature-map entry. The feature issue template asks for the expected effect, and the first issue written from it fills it in.

**From the template.** `AGENTS.md`, `CLAUDE.md`, `feature-map/`, `docs/`, `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`, `.github/workflows/docs.yml`.
