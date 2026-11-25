# Stage 5: Safety boundary

**Purpose.** What an agent must never do is impossible, not merely forbidden.

**Look.** Who and what can merge today; which tokens exist and what they can do; what a session on the agent's machine can reach; where personal data could reach an agent (error reports, logs, test fixtures).

**Ask.**
- 5.1 **The merge gate.** How is it made technically impossible for an agent to merge? The options depend on the plan and on whether the agent has an identity separate from the owner; set them out with their cost.
- 5.2 **Protected paths.** How is a change to a protected path forced to wait for the owner?
- 5.3 **Tokens.** For each role an agent will play, the smallest set of rights. Confirm each.
- 5.4 **Personal data.** Which fields are removed from error reports and logs before an agent may read them? Confirm: agents work with test data only.
- 5.5 **Reach.** Confirm what the agent's environment cannot reach: production systems, the stores, signing keys, the owner's own files.

**Do.** The agreed repository rules and scrubbing. Token creation stays with the owner.

**Exit check.** Acting with the agent's rights: a merge is refused, a push to the default branch is refused, and a change to lint or CI configuration cannot land without the owner. A sample error report shows no personal data.

**From the template.** The `owner-approval` job in `.github/workflows/lint-rules.yml`, the deny list in `.claude/settings.json`, the hook, and `docs/architecture/github-workflows.md`. Keep the three lists of protected paths identical.
