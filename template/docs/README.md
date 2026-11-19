# {{PROJECT_NAME}}: how it works

This folder documents **how the application actually runs**: screen by screen, capability by capability, and the engineering rules that keep the code base in shape. It is written for anyone, human or AI agent, who changes the code or builds on it.

**What** the product does, rule by rule, is in the [feature map](../feature-map/README.md). This folder explains **how** the code does it and **why** it is built that way. Where the two overlap, docs link to the spec instead of restating the rule.

- **[`screens/`](screens/)**: one doc per screen. Its states, exactly what it loads and saves and in which order, what the user can do, how you get to it and away from it, and the backend contract it relies on. Start here for "what does this screen do". Start a new one from [screens/_template.md](screens/_template.md).
- **[`features/`](features/)**: one doc per capability that spans several screens or has no screen of its own (session handling, deep links, localization, push notifications, analytics). Start here for "how does X work end to end". Start a new one from [features/_template.md](features/_template.md).
- **[`architecture/`](architecture/)**: how the code base itself is built and kept in shape.

A backend or library repository has no screens: replace `screens/` with what its users touch, for example `endpoints/` or `modules/`, one doc each.

## How the code is built

Describe the architecture in a few paragraphs and one tree: the layers or modules, what each one may depend on, and where a new piece of code goes. Keep it short; the rules that a tool enforces are listed in [code style and lint](architecture/code-style-and-lint.md).

```
src/
├── domain/          {{what lives here and what it may import}}
├── data/            {{...}}
├── presentation/    {{...}}
└── core/            {{the composition root: wiring, navigation, configuration}}
```

## Screens

| Screen | What it is for |
|---|---|
| {{[login](screens/login.md)}} | {{Sign in with email and password}} |

## Features

| Feature | Covers |
|---|---|
| {{[session](features/session.md)}} | {{Tokens on every request, refresh, sign-out}} |

## Engineering

| Doc | Covers |
|---|---|
| [architecture/code-style-and-lint](architecture/code-style-and-lint.md) | The comment ban, the analyzer and formatter, the feature map check, who may change the lint rules, and the docs-updated check |
| [architecture/github-workflows](architecture/github-workflows.md) | The workflows, their time limits, pinned actions, Dependabot, labels and required checks |

## Keeping these docs true

These docs are a snapshot, not a live view. A change to a screen's states, its data flow or a backend contract, or a new or removed screen, updates the matching doc and this index in the same pull request; the `docs-updated` check fails a code change that touches no documentation. Treat a doc that contradicts the code as a bug in the doc, not as evidence that the code is wrong, and verify against the source before trusting either.

A decision that still holds once its work is done goes into the doc of the code it shapes, with its date and the issue or pull request where it was taken. That is where the explanation a code comment would have carried lives.
