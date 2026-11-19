# ASDLC Blueprint

A blueprint for an **agentic software development lifecycle**: the documents, checks and agent instructions that take a piece of work from a detailed GitHub issue to a merged pull request, with AI agents doing the building and the checking, and a person deciding what gets merged.

It accompanies the engineering note **[Agentic Software Development, Part 1: From Issue to Merge](https://binarieslab.com/en/rfc/2026-11-19-agentic-software-development-part-1/)** ([auf Deutsch](https://binarieslab.com/de/rfc/2026-11-19-agentic-software-development-part-1/)), which explains why the process looks like this. The files here are distilled from the setup of a production Flutter app at [Binaries Lab](https://binarieslab.com), made stack-agnostic, with its product details replaced by examples.

## The idea in one paragraph

An agent writes code far faster than a person, but it carries none of the knowledge an experienced engineer brings to a three-line ticket. So everything that used to be implicit becomes explicit and checkable. A detailed issue says where to go. Lint rules, technical documentation, a decision log and tests written first narrow the path the agent can take. A second agent with a fresh context checks, in the running app, that it arrived.

## The six building blocks

| Step | What it does | Where it lives |
|---|---|---|
| 1. A detailed issue | Product, user and technical context, acceptance criteria and test scenarios, so the agent decides nothing silently | [`.github/ISSUE_TEMPLATE/`](template/.github/ISSUE_TEMPLATE/), [`feature-map/`](template/feature-map/) |
| 2. Lint guardrails | Rules a tool enforces, including no comments in code, which agents cannot change | [`tool/`](template/tool/), [`.claude/settings.json`](template/.claude/settings.json), [`.claude/hooks/`](template/.claude/hooks/), [`lint-rules.yml`](template/.github/workflows/lint-rules.yml) |
| 3. Technical documentation | How the repository is built: structure, modules, screens, capabilities, engineering rules | [`AGENTS.md`](template/AGENTS.md), [`docs/`](template/docs/) |
| 4. A decision log | Why it is built that way, and when: product decisions as numbered records, engineering decisions in the docs of the code they shape, and every pull request's choices in its description | [`feature-map/decisions/`](template/feature-map/decisions/), [`docs/`](template/docs/), [the PR template](template/.github/pull_request_template.md) |
| 5. Tests before code | Acceptance criteria turned into tests first, with UI journeys for the flows that matter | [`TESTING_STRATEGY.md`](template/TESTING_STRATEGY.md) |
| 6. A verdict from fresh eyes | An agent that didn't build the change uses the app like a user and posts PASS, FAIL or "couldn't check" per step; a FAIL goes back to the builder | [`.claude/agents/verifier.md`](template/.claude/agents/verifier.md), [`.claude/skills/verify-app/`](template/.claude/skills/verify-app/) |

## What's inside

Everything you copy into your repository is in [`template/`](template/):

```
template/
├── AGENTS.md                      the contract every agent reads first
├── CLAUDE.md                      points Claude Code at AGENTS.md
├── TESTING_STRATEGY.md            what to test, test-first, journeys, snapshots
├── Makefile                       make lint, make test, make feature-map
├── feature-map/                   WHAT the product does
│   ├── INDEX.md                   every feature, its status per platform
│   ├── AGENTS.md                  how to write and keep a spec
│   ├── GLOSSARY.md, principles.md
│   ├── features/                  one spec per feature, with requirement IDs (AUTH-004)
│   ├── decisions/                 numbered product decision records
│   ├── reference/                 research and plans, kept as received
│   └── scripts/check.py           checks the map: statuses, IDs, links
├── docs/                          HOW the code works, and why
│   ├── README.md                  the index and the architecture overview
│   ├── screens/_template.md       one doc per screen
│   ├── features/_template.md      one doc per cross-cutting capability
│   └── architecture/              code style and lint, GitHub workflows
├── tool/
│   ├── comment_ban.py             fails on comments in 15 languages, no dependencies
│   ├── lint.sh                    comment ban, analyzer, format check
│   └── tests/                     the comment ban's own tests
├── .claude/
│   ├── settings.json              denies edits to the lint rules
│   ├── hooks/protect-lint-rules.sh  blocks shell writes and self-approval
│   ├── agents/verifier.md         runs a verification round, posts the verdict
│   └── skills/verify-app/         how to build, start and drive the app
└── .github/
    ├── ISSUE_TEMPLATE/            feature and bug, detailed enough for an agent
    ├── pull_request_template.md   with "What to check in the app" and "Decisions"
    ├── dependabot.yml
    └── workflows/                 ci, docs-updated, owner-approval
```

## Get it

Download the [zip of `main`](https://github.com/binarieslab/asdlc-blueprint/archive/refs/heads/main.zip), or clone it and copy the template into your repository, hidden files included:

```bash
git clone --depth 1 https://github.com/binarieslab/asdlc-blueprint.git
cp -R asdlc-blueprint/template/. path/to/your-repository/
```

Then follow [ADOPTING.md](ADOPTING.md): replace the `{{PLACEHOLDERS}}`, wire in your stack's analyzer and tests, create the labels, and write your first specs.

## How the loop runs, day to day

1. **Write the issue** from the feature or bug template and put it on your GitHub Project board. Anything unclear gets `needs:human` and an answer before the build starts.
2. **Start a Claude Code session** in the repository: "Work on #42." The agent reads `AGENTS.md`, the issue, the spec and the docs, writes the tests from the acceptance criteria, implements until they pass, runs `make lint` and `make test`, and opens a pull request with "What to check in the app".
3. **CI runs** the lint, the tests, `docs-updated` and `owner-approval`.
4. **Start a second, fresh session** to run a verification round: "Run a verification round on pull request #57 as `.claude/agents/verifier.md` describes." It builds the head, uses the app like a user, posts the verdict and sets the `agent-verdict` status.
5. **A FAIL goes back** to the builder's session through the pull request; a finding too big for it becomes a new issue. A finding about missing or wrong docs is fixed in the docs, so the next change starts from them.
6. **You read the verdict and merge.** Your deployment workflow takes it from there.

## What this does not cover yet

This is the first part of the lifecycle: one flow, from an issue to a merged pull request. Work entering from other places, such as a bug reported by a backend service, a customer email or a prompt, and a router that turns each one into an issue, is the next part. Deployment is left to your stack.

## License

[MIT](LICENSE). Use it, change it, and make it your own.
