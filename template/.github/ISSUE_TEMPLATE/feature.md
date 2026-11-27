---
name: Feature
about: A new capability, or a change to what the product does. Detailed enough that an agent can build and verify it without asking.
title: ""
labels: enhancement
---

<!-- Every detail left out is a decision the agent makes for you. Fill in every section; write "none" where nothing applies. -->

## Product

**Why:** the problem or need, and why now.

**Who it is for:** the roles and the situation they are in.

**What changes for them:**
- As a <role> I can ...

**What it is not:** what this issue deliberately does not do.

**Expected effect:** what should change if this works (revenue, retention, cost, support load), and how that will be measured after release.

**When to remove it:** the result that would mean this is switched off or deleted.

## User experience

- Where it starts and the screens or flows involved, linked to `docs/screens/`.
- Every state: empty, loading, success, each error, offline.
- The exact copy, in every supported language.
- Accessibility: labels, touch targets, large text, dark mode.

## Technical context

- Feature-map spec: `feature-map/features/<slug>.md`, and the requirement IDs this adds or changes.
- Repositories, modules and screens affected.
- API contract: method, path, request, response and status codes, with a link to the contract.
- Data: what is stored, cached or migrated, and for how long.
- Analytics events and their properties.
- Platforms: where this ships, and any deliberate difference.

## Acceptance criteria

- [ ] WHEN ... THEN ... (`FEATURE-NNN`)
- [ ] IF ... THEN ... (`FEATURE-NNN`)

## Test scenarios

One or more per criterion, error paths included. These become the tests before any code is written.

```
Given ...
When ...
Then ...
```

## Out of scope

## Open questions

Each one is answered before the build starts. Until then the issue carries `needs:human`.
