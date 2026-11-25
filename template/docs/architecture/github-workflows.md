# GitHub workflows

The workflows in `.github/workflows/`, the rules every one of them follows, the labels and checks the process relies on, and how a merge turns into a deployment. The workflows belong to the owner: a pull request that changes them waits for the `lint-rules-approved` label ([who may change the lint rules](code-style-and-lint.md#who-may-change-the-lint-rules)).

## The workflows

| File | Starts when | Job | `timeout-minutes` |
|---|---|---|---|
| `ci.yml` | a pull request targets `main` or `release/**` | `lint` | 15 |
| | | `build_and_test`, after `lint` | 25 |
| `docs.yml` | a pull request is opened, updated, reopened, labelled or unlabelled | `docs-updated` | 5 |
| `lint-rules.yml` | the same, and when its description is edited (`pull_request_target`) | `owner-approval` | 5 |
| {{deploy.yml}} | {{a push to `main`, or a version tag}} | {{deploy}} | {{...}} |

`lint` runs `tool/lint.sh` and then `make asdlc-verify`, and `build_and_test` runs `make test`. `docs-updated` and `owner-approval` are described in [code style and lint](code-style-and-lint.md).

## Rules every workflow follows

- **Every job has a `timeout-minutes`.** Without one, a hung job runs for GitHub's default of 360 minutes, and six hours of a macOS runner can use up a month of Actions minutes. Set each limit well above the slowest successful run of its job, so only a hung job reaches it, and raise a limit rather than remove it.
- **A new push cancels the run it replaces.** `ci.yml` has a `concurrency` group per workflow and branch with `cancel-in-progress: true`.
- **A deploy that is running is never cancelled.** A deploy workflow uses one group per environment with `cancel-in-progress: false`.
- **Every action is pinned to a commit.** A `uses:` line reads `owner/repo@<40 character commit> # vX.Y.Z`. A tag can be moved, a commit can't. To pin an action, take the commit with `gh api repos/<owner>/<repo>/commits/<tag> --jq .sha`.
- **Dependabot proposes the updates.** `.github/dependabot.yml` opens one pull request a month with every action update grouped. It changes `.github/workflows/`, so it waits for the `lint-rules-approved` label like any workflow change.

## Setting up the toolchain

`ci.yml` sets up Flutter as its example. For another stack, replace the "Set up the toolchain" step in both jobs:

| Stack | Step |
|---|---|
| Flutter | `subosito/flutter-action`, with the Flutter version pinned |
| Node and TypeScript | `actions/setup-node` with `cache: npm`, then `npm ci` |
| Go | `actions/setup-go` with `go-version-file: go.mod` |
| Swift | a `macos-latest` runner and `xcodebuild` or `swift build`; pick the Xcode version with `sudo xcode-select -s` |
| Kotlin and Android | `actions/setup-java` with `distribution: temurin`, then the Gradle wrapper |
| Python | `actions/setup-python` with the version pinned |

Pin each one to a commit like every other action.

## Labels

| Label | Who adds it | Meaning |
|---|---|---|
| `docs-not-needed` | the agent or a person, with the reason in the description | the pull request changes code but nothing that needs documenting |
| `lint-rules-approved` | the owner only, never an agent | the owner approves a change to a protected file |
| `needs:human` | anyone | the issue has a question only the owner can answer; work on it waits |

Create them once:

```bash
gh label create docs-not-needed --description "Code change with nothing to document" --color c5def5
gh label create lint-rules-approved --description "The owner approves a change to the lint rules" --color b60205
gh label create needs:human --description "Waiting for an answer from the owner" --color fbca04
```

## Statuses and required checks

The verification round sets a commit status named `agent-verdict` on the pull request's head (see `.claude/agents/verifier.md`): `pending` while it runs, `success` only when every step passed in the app and every gate is green, `failure` otherwise. It points at the verdict comment.

Required status checks are set by the owner in the repository settings (a ruleset or branch protection on `main` and `release/*`): `lint`, `build_and_test`, `docs-updated`, `owner-approval` and, once verification rounds run on every pull request, `agent-verdict`. Until then the checks run but block nothing.

## Deploying

{{How a merge becomes a release: which workflow deploys what, to which environment, triggered by what (a push to `main`, a version tag, a manual dispatch), where its secrets live, and how to roll back.}}
