---
name: Bug
about: The product does not do what its spec says, or something is visibly broken.
title: ""
labels: bug
---

<!-- A bug sits under the issue that fixes it. Write it so an agent can reproduce it without asking. -->

## What happened

What the user did and what they saw. Screenshots, logs or the error report's link.

## What should happen

The expected behavior, with the requirement ID it breaks (`FEATURE-NNN` in `feature-map/`). If no spec covers it, say so: the fix adds the rule.

## Steps to reproduce

1. Signed in as <role>, on <platform and version>, against <environment>:
2. ...

## Impact

Who is affected, how often, and whether there is a workaround.

## Technical context

What is known about the cause: the screen, the endpoint, the status code, a recent change. Link the docs of the code involved.

## Acceptance criteria

- [ ] The steps above show the expected behavior.
- [ ] A test that fails before the fix and passes after it, named for the scenario.
- [ ] The spec or the docs updated if they were wrong or silent.

## Test scenario

```
Given ...
When ...
Then ...
```
