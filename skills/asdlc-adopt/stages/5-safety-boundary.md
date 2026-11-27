# Stage 5: Safety boundary

**Purpose.** What an agent must never do is impossible, not merely forbidden.

**Look.**
- The owner's constraints from stage 0: the plan, the seats, the repository's visibility, the owner's login. Read them; do not ask again.
- Who and what can merge today, and which rules protect the default branch. You usually cannot read these. Ask the owner, as a Fact at the start, to paste the ruleset or the output of the command you give.
- Which tokens exist and what they can do.
- What a session on the agent's machine can reach.
- Where personal data could reach an agent: error reports, logs, test fixtures.
- Whether the lists of protected paths agree with decision 0.2 and with each other.

**Ask.** Two rounds.

Round one:
- 5.1 **The merge gate.** How is it made technically impossible for an agent to merge? Set the options out with their cost, and only options that fit the owner's constraints. Two facts shape them: on GitHub the author of a pull request cannot approve it, and every organization member and every outside collaborator on a private repository uses a seat. With one seat, a second member is not an option, and a rule that requires an approving review blocks the owner's own pull requests if the agent works under the owner's identity. Set out what remains, for example an app identity or a token that cannot merge, and check GitHub's current documentation for each before you propose it.
- 5.2 **Protected paths.** How is a change to a protected path forced to wait for the owner?
- 5.3 **Tokens.** For each role an agent will play, the smallest set of rights. Confirm each.
- 5.4 **Personal data.** Which fields are removed from error reports and logs before an agent may read them? Confirm: agents work with test data only.
- 5.5 **Confirm** what the agent's environment cannot reach: production systems, the stores, signing keys, the owner's own files.

Round two, with the draft pull request:
- 5.6 **Approval** for the exact protected files: the workflow, the agent settings, the hook.

**Do.** The agreed repository rules and scrubbing. Creating tokens, rulesets, labels and accounts stays with the owner: write the steps as a numbered checklist, with the evidence to send back for each.

**Exit check.** Acting with the agent's rights: a merge is refused, a push to the default branch is refused, and a change to lint or CI configuration cannot land without the owner. A sample error report shows no personal data. The hook refuses a write to each check script and to the lint configuration. What needs GitHub is `waiting for owner` until the owner has sent the evidence.

**From the template.** The `owner-approval` job in `.github/workflows/lint-rules.yml`, the deny list in `.claude/settings.json`, the hook, and `docs/architecture/github-workflows.md`, each only where the repository has no equivalent.
- Keep the lists of protected paths identical: the `PROTECTED` pattern in `lint-rules.yml`, the deny list in `settings.json` and `paths` in the hook. If the repository adds a `CODEOWNERS` file, that is a fourth. Decision 0.2 is the source for all of them.
- The lists are written for the template's layout and several stacks' lint files. Rewrite them for this repository, then try the hook again.
- The hook lets every command through when `jq` is missing. Tell the owner, and offer as a Decision to make it refuse instead.
- `github-workflows.md` links to `code-style-and-lint.md`, which arrives in stage 2. Bring both, or neither.
