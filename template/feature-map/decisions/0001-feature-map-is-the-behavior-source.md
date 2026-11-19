---
status: accepted
date: YYYY-MM-DD
decision-makers: [{{OWNER_NAME}}]
---

# The feature map is the source of truth for product behavior

## Context

Product rules tend to end up in many places: issue threads, a roadmap, code comments, the backend's documentation, and the heads of the people who built the feature. Each of those places loses them over time, and an agent that starts a session from the repository sees none of them.

When the same product ships on more than one platform, one feature can be built on some platforms and not yet on others. Agents and the people who review their work need one place that says what a feature should do and where it exists.

## Decision

- `feature-map/` in this repository holds one spec per feature: behavior, limits, the contract it relies on, analytics, and its status per platform.
- Product decisions are recorded in `feature-map/decisions/`. Research and plans that led to them are kept as received in `feature-map/reference/`.
- `docs/` describes how the code runs and links to the specs; it does not restate product rules.
- Rules carry stable requirement IDs (`AUTH-004`). Code never cites them, because comments are banned; tests and pull requests do.
- `feature-map/scripts/check.py` checks the map, and `make lint` and `make test` run it.

## Consequences

- A behavior change updates its spec in the same pull request as the code. The `docs-updated` check accepts a change under `feature-map/` as documentation, and the pull request template asks for the platform status.
- An issue that changes behavior names the requirement IDs it adds or changes, so the agent that builds it and the agent that verifies it work from the same rules.
- Writing a spec costs time up front. It pays back every time an agent reads it instead of guessing.
