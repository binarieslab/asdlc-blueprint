# AGENTS.md: {{PROJECT_NAME}}

This file is the contract for every agent, human or AI, that works in this repository. Read it completely before changing anything. Each section below says what to write in it; replace that guidance with your project's facts and keep the headings.

## What this is

{{One paragraph: what the product does, for whom, and on which platforms. Name the other repositories this one talks to, and where their contract lives ({{API_CONTRACT_URL}}). Say what an agent must never invent here, for example: "This repository is client-only. Do not invent backend behavior; read the backend's contract for the endpoint, method and shapes before assuming one."}}

- Stack: {{language, framework and version; state management; dependency injection; navigation}}
- Environments: {{development at {{DEV_ENVIRONMENT}}, production at ...}}. Agents work against development only.

## Rules a tool enforces

`make lint` fails when you break these, and CI runs it first on every pull request ([docs/architecture/code-style-and-lint.md](docs/architecture/code-style-and-lint.md)).

- **No comments in code, tests included.** The only exceptions are analyzer and formatter directives with rule names only. What a comment would have said goes into `docs/` (how the code works and why) or the feature map (what the product does). A test's description carries its scenario, so no `// Given / When / Then` markers.
- **Layers and banned APIs.** {{The dependency rules between layers or modules, and the APIs that may only be used through one wrapper, as a tool checks them.}}
- **Analyzer and formatter clean**, the tests and `tool/` included.
- **Documentation is part of the change.** A pull request that changes code without touching the docs fails `docs-updated` unless it is labelled `docs-not-needed`.
- **The feature map stays consistent.** `make lint` and `make test` run `feature-map/scripts/check.py`, which fails on a spec without a status per platform, a status that differs from `feature-map/INDEX.md`, a duplicate requirement ID or a broken link.

**Never change the lint rules.** `tool/`, `feature-map/scripts/`, the analyzer configuration ({{ANALYZER_CONFIG}}), `.github/workflows/`, `.claude/settings.json` and `.claude/hooks/` belong to the owner. If a rule or a workflow has to change, say so and let the owner do it. Claude Code blocks these writes, and a pull request that touches them waits until the owner adds the `lint-rules-approved` label, which agents never add.

## Where work is tracked

On GitHub, never in files in this repository. Every task is an issue on the [{{BOARD_NAME}}]({{BOARD_URL}}) board, written from one of the templates in `.github/ISSUE_TEMPLATE/`. A release has a milestone and a release issue whose sub-issues are its tasks in build order, and a bug sits under the issue that fixes it.

- A pull request names the issue it closes and lists the decisions it took in its description.
- A decision that still holds once the work is done goes into the docs of the code it shapes (`docs/`, the feature map) in the same pull request.
- A question for the owner gets `needs:human` on its issue, and the work it blocks waits for the answer. Don't guess and build both the code and the test around the same unverified assumption.

## How a change is built and checked

A pull request is checked in the running app, with CI's tests beside it. It is not a code review: nobody reads the diff for findings. The owner reads one verdict and merges. The six steps:

1. **Gather.** The issue says what to build: the product context, the user's side, the technical context and the acceptance criteria. Read it, the feature-map spec it names, the contract of every endpoint the change calls, and the docs of every screen and capability it touches, before writing code. If the issue leaves the expected behavior unclear, ask on the issue with `needs:human`.
2. **Test, then implement.** Turn the acceptance criteria into tests first, as the [testing strategy](TESTING_STRATEGY.md) describes: the scenarios of each criterion, error paths included, citing their requirement IDs. Then write the code until they pass. The pull request's description lists "What to check in the app" (below).
3. **Check.** Two checks run side by side on the pull request's head:
   - CI runs `make lint` and `make test`. That is the check on the logic.
   - The app check. An agent that didn't build the change (`.claude/agents/verifier.md`) opens the app built from that head against development, writes its own list of steps from the issue's acceptance criteria, compares it with the description's, then does every step as a user would and keeps a screenshot of each.
4. **Verdict.** One comment on the pull request, each step with PASS, FAIL or "couldn't check" and its evidence, plus the `agent-verdict` status, which is `success` only when every step passed. A finding is one thing only: the app doesn't do what the issue says, or something is visibly broken on the way there.
5. **Loop.** A FAIL comes back through the pull request, with what was done, what was expected and what the app showed. The builder fixes it on the branch, with a test where the cause is logic, and the new head gets a new check. A finding too big for this round becomes a new issue. After three rounds the findings go to the owner.
6. **Learn.** The verdict marks each finding "this change" or "project". A project finding comes from something the docs don't say, or say wrongly. Its fix changes them in the same pull request, so the next change starts from them: a rule goes into this file, how the code works goes into `docs/` and the feature map, and how to reach or drive a screen goes into the verification skill's `features/`. The next check confirms that the docs changed.

The builder runs [the Gate](#the-gate) before pushing, and never runs or posts the check on their own pull request. The owner merges everything.

### What to check in the app

Every pull request's description has a section with this title. It is the list the app check does, and the owner can do by hand:

- Each step says what a user does and what they should see.
- There is at least one step for each acceptance criterion of the issue.
- Each step names the role to sign in as, or "signed out". The development test accounts are: {{the roles that have a test account}}.
- Each step names where it runs: {{the iOS simulator, an Android emulator, or the browser}}.

A change with nothing to see in the app (documents, tests, tooling) says in a step or two what to check instead.

## Documentation: read before working on a screen or feature

- `feature-map/` documents **what the product does**: one spec per feature with its rules (requirement IDs such as `AUTH-004`), its status per platform, and the decision records behind them. Start at `feature-map/INDEX.md`; `feature-map/AGENTS.md` says how to write and keep a spec. A change in behavior updates its spec and status in the same pull request, and tests cite requirement IDs in their descriptions.
- `docs/` documents **how the code runs**, screen by screen and capability by capability. Start at `docs/README.md`. Before touching a screen or a cross-cutting capability, read its doc.

These docs are a snapshot, not a live view. If you change a screen's states, its data flow or a backend contract, or add or remove a screen, update the matching doc and its index in the same change. Treat a doc that contradicts the code as a bug in the doc, not evidence the code is wrong, and verify against the source before trusting either.

## Architecture

{{The layers or modules, as a tree, with what each one may depend on and which tool enforces it. Then the pattern every new piece follows, for example the files a new screen consists of and where it is wired in. Keep the details in docs/README.md and link to it.}}

```
src/
├── domain/          {{...}}
├── data/            {{...}}
├── presentation/    {{...}}
└── core/            {{...}}
```

## Conventions

{{The rules a reviewer would otherwise repeat in every pull request, one bullet each. For example:}}

- One public type per file; the file is named after it.
- Every use case, repository and data source is named for the single thing it does.
- Don't add a new dependency injection framework, router or state-management library; extend the existing pattern.
- Never hardcode a user-facing string; add it to every language's translation file.

## Testing

[TESTING_STRATEGY.md](TESTING_STRATEGY.md) is the full charter: what is worth testing, the pattern per layer with an example file to copy, and the UI and journey tests. The short version:

- Tests come before the implementation for any logic with a branch, a mapping, a cache rule or an orchestration.
- Tests mirror the source tree.
- Test descriptions read as the scenario and cite the requirement ID they prove.
- Do not weaken, skip or delete a test to make it pass.

## The Gate

Before considering any change done, all of the following pass:

```
make lint      # feature map check, comment ban, analyzer, format check
make test      # feature map check, the tests, the lint tool's own tests
make check     # both, in that order
```

{{Name any generation step that has to run first, such as code generation or translations, and that its output is committed with the change.}}

## Commands

- `make lint`: the feature map check, then `tool/lint.sh`
- `make test`: the feature map check, then the tests and the tool tests
- `make check`: `make lint`, then `make test`
- `make feature-map`: the feature map check alone
- `make asdlc-verify`: the scorecard check, which CI runs on every pull request
- {{`make run`, `make build`, `make deploy`, and anything else an agent needs}}
