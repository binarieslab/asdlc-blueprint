# ASDLC Blueprint

A blueprint for an **agentic software development lifecycle**: the documents, checks and agent instructions that take a piece of work from a detailed GitHub issue to a merged pull request, with AI agents doing the building and the checking, and a person deciding what gets merged.

It accompanies the engineering note **[Agentic Software Development, Part 1: From Issue to Merge](https://binarieslab.com/en/rfc/2026-11-19-agentic-software-development-part-1/)** ([auf Deutsch](https://binarieslab.com/de/rfc/2026-11-19-agentic-software-development-part-1/)), which explains why the process looks like this. The files here are distilled from the setup of a production Flutter app at [Binaries Lab](https://binarieslab.com), made stack-agnostic, with its product details replaced by examples.

## The idea in one paragraph

An agent writes code far faster than a person, but it carries none of the knowledge an experienced engineer brings to a three-line ticket. So everything that used to be implicit becomes explicit and checkable. A detailed issue says where to go. Lint rules, technical documentation, a decision log and tests written first narrow the path the agent can take. A second agent with a fresh context checks, in the running app, that it arrived.

## The foundation

The blueprint is built on one observation from Lauren Tan's talk ["All Code Is Slop (Except Mine)"](https://ai.engineer/talks/O_zcc6Xl12g-all-code-is-slop-except-mine): you can trust an agent's work only as far as its environment makes wrong work impossible or visible. She ranks the means from strongest to weakest, and the blueprint spends its effort in that order:

1. **The codebase itself**: an API or a module boundary that makes the mistake impossible to write.
2. **Deterministic checks**: lint rules, types, the compiler and tests, which fail the same way every time.
3. **Verification of the running product**, with the evidence kept.
4. **Written rules**, which an agent may or may not follow.
5. **Human review**, kept for what the others cannot decide.

Two habits follow. Every correction becomes a check, and a new line of prose is the last resort. And the loop for one change is made trustworthy by hand before any of it is automated, because automating a loop that produces poor changes only produces more of them.

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

Two things. [`skills/asdlc-adopt/`](skills/asdlc-adopt/) is a skill that walks an agent and a repository's owner through the adoption together, stage by stage: the agent inspects and proposes, the owner decides, and each stage ends in a check that passes or fails. [`template/`](template/) holds everything that ends up in your repository:

```
template/
├── AGENTS.md                      the contract every agent reads first
├── CLAUDE.md                      points Claude Code at AGENTS.md
├── TESTING_STRATEGY.md            what to test, test-first, journeys, snapshots
├── Makefile                       make lint, make test, make check, make feature-map, make asdlc-verify
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
│   ├── asdlc_verify.py            checks the scorecard and runs the checks behind its passed rows
│   ├── asdlc_checks.json          those checks, one per scorecard row
│   ├── probes/                    checks that break a rule on purpose to see the guard catch it
│   └── tests/                     the tools' own tests
├── .claude/
│   ├── settings.json              denies edits to the lint rules
│   ├── hooks/protect-lint-rules.sh  blocks shell writes and self-approval
│   ├── agents/verifier.md         runs a verification round, posts the verdict
│   └── skills/verify-app/         how to build, start and drive the app
└── .github/
    ├── ISSUE_TEMPLATE/            feature and bug, detailed enough for an agent
    ├── pull_request_template.md   with "What to check in the app" and "Decisions"
    ├── dependabot.yml
    └── workflows/                 ci, asdlc-verify, docs-updated, owner-approval
```

## Get it

Download the [zip of `main`](https://github.com/binarieslab/asdlc-blueprint/archive/refs/heads/main.zip), or clone it and copy the template into your repository, hidden files included:

```bash
git clone --depth 1 https://github.com/binarieslab/asdlc-blueprint.git
cp -R asdlc-blueprint/template/. path/to/your-repository/
```

Then follow [ADOPTING.md](ADOPTING.md): replace the `{{PLACEHOLDERS}}`, wire in your stack's analyzer and tests, create the labels, and write your first specs.

### Or adopt it with an agent

Copying everything at once puts the written rules in before the checks that back them. The adoption skill brings the pieces in one stage at a time, strongest layer first, and asks you for every decision on the way:

```bash
mkdir -p ~/.claude/skills
cp -R asdlc-blueprint/skills/asdlc-adopt ~/.claude/skills/
```

Then start a Claude Code session in your repository and say: "Use the asdlc-adopt skill on this repository." It keeps a scorecard and a record of your decisions in `docs/asdlc/`, so a later session continues where the last one stopped.

A repository is ASDLC-ready when every row of that scorecard has passed or does not apply. `make asdlc-verify` keeps the claim honest afterwards: CI runs it on every pull request, and it fails when a passed row's check no longer holds.

The skill was shaped by test runs on three repositories of different kinds: a backend API, a web app with accounts, and a static site. In each run one agent followed the skill and a second agent played the owner, once as an engaged owner, once answering in fragments from a phone, and once pressing for shortcuts. Stages 0 to 5 were exercised that way. After the revision that followed, the skill was run once more, on a Flutter app, with a third agent as referee. Stages 6 and 7 have not been test-driven yet.

## How the loop runs, day to day

1. **Write the issue** from the feature or bug template and put it on your GitHub Project board. Anything unclear gets `needs:human` and an answer before the build starts.
2. **Start a Claude Code session** in the repository: "Work on #42." The agent reads `AGENTS.md`, the issue, the spec and the docs, writes the tests from the acceptance criteria, implements until they pass, runs `make lint` and `make test`, and opens a pull request with "What to check in the app".
3. **CI runs** the lint, the tests, `docs-updated` and `owner-approval`.
4. **Start a second, fresh session** to run a verification round: "Run a verification round on pull request #57 as `.claude/agents/verifier.md` describes." It builds the head, uses the app like a user, posts the verdict and sets the `agent-verdict` status.
5. **A FAIL goes back** to the builder's session through the pull request; a finding too big for it becomes a new issue. A finding about missing or wrong docs is fixed in the docs, so the next change starts from them.
6. **You read the verdict and merge.** Your deployment workflow takes it from there.

## What this does not cover yet

This is the first part of the lifecycle: one flow, from an issue to a merged pull request. Work entering from other places, such as a bug reported by a backend service, a customer email or a prompt, and a router that turns each one into an issue, is the next part. Deployment is left to your stack.

The adoption skill also asks for things the template has no files for yet: a gate on new dependencies, a secrets scan, enforced module boundaries, and release safety (compatibility with shipped versions, feature flags, rollback). Those are built for each repository's stack during the adoption.

## Contributing

Issues and pull requests are welcome, especially reports from adopting the blueprint in a stack it doesn't cover yet. Please read the [Code of Conduct](CODE_OF_CONDUCT.md) first. Changes to the template keep its own rules: no comments in its code, and `python3 template/feature-map/scripts/check.py` and the comment ban's tests pass.

## License

[MIT](LICENSE). Use it, change it, and make it your own.
