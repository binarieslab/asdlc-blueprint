# feature-map: agent instructions

This folder is the source of truth for **what** each {{PROJECT_NAME}} feature does: product rules, flows, limits, edge cases, the contract it relies on, analytics and its status per platform. It contains no code.

**How** a feature is implemented stays with the code: [`docs/`](../docs/README.md) for this repository, and the other repository's own documentation for anything it owns (for example the backend's endpoint contract at {{API_CONTRACT_URL}}). Specs link to both.

## Reading

1. Open [INDEX.md](INDEX.md). One row per feature: ID, one-line summary, status per platform, spec file.
2. Open only the spec you need in `features/`. Each file is self-contained and stays under roughly 400 lines.
3. Terms are defined once in [GLOSSARY.md](GLOSSARY.md). Rules that apply to every feature (roles, privacy, languages, accessibility) are in [principles.md](principles.md).
4. A decision with its reasoning is in [decisions/](decisions/); a spec links to it instead of repeating it.
5. [reference/](reference/) holds documents kept as received. They are background, not rules.

Paths to code in this repository are written from the repository root (`src/...`). Paths to another repository are written as `<repository>/...`, and links to its contract point at its documentation on GitHub, because it is not checked out next to this one.

## When the spec and the code disagree

Do not silently pick one. Either the code has a bug or the spec is stale. Say which you think it is, and record it under "Open questions" in the spec if it is not resolved in the same change. Where the owning service's contract and anything else disagree about the contract, the contract wins.

## Writing and changing specs

- **Product section first.** Every spec starts with a "Product" section in plain language: why it exists, for whom, what people can do as "As a member I can ..." stories, and what it is not. No technical terms there; the detailed rules follow below it.
- **Behavior, not implementation.** Describe what a user, the app or the backend observes. No class names in requirements. Class and file names belong in the "Implementation" table at the end of a spec.
- **One feature per file**, named `features/<slug>.md`, started from [features/_template.md](features/_template.md).
- **Exact values.** "120 days", "25 MB", "HTTP 403 `insufficient_role`", never "a few" or "a while". Put numbers in tables.
- **Each fact lives in one place.** Link to another spec instead of repeating it. Details already in another repository's contract are summarized and linked, not copied in full.
- **Platform differences go in the "Platform differences" table**, not in separate prose per platform.
- **Plain English and plain Markdown.**
- Keep `last_verified` in the frontmatter current whenever you check a spec against the code.
- Update [INDEX.md](INDEX.md) when you add a spec or change a status; the check compares the two.

### Status

Each spec has a status per platform. The platforms are the keys of `status` in [features/_template.md](features/_template.md); the check reads them from there, so changing the platforms means changing the template, every spec and the status column of INDEX.md together.

| Value | Meaning |
|---|---|
| `implemented` | Built and released on that platform. |
| `in-progress` | Partly built. |
| `planned` | Decided and scheduled, not built. |
| `n/a` | The feature does not exist on that platform by design; the "Platform differences" table says why. |

A rule that is decided but not built yet, in a spec whose platform status is `implemented`, says so in its "Applies to" column with the issue that builds it, for example `App (planned in #25)`. A known bug is the same: the rule says what should happen, and the note names the bug's issue. A bug without an issue says `App (bug, no issue yet; see Open questions)` until one is filed. Every rule without such a note is built. When the issue ships, remove the note in the same pull request.

"App" in an "Applies to" column means every client platform. Name the platforms when a rule holds for only some of them.

### Requirement IDs

- Every rule has an ID: `<FEATURE-ID>-<three digits>`, for example `AUTH-012`. The feature ID is the `id` in the spec's frontmatter.
- IDs are never reused or renumbered. A rule that no longer applies is marked `**Removed YYYY-MM-DD:**` and stays in the table.
- New rules take the next free number, wherever they sit in the table.
- Comments are banned in code, so code never cites an ID in a comment. Tests cite IDs in their test or group description, and pull requests cite them in their description. Changing the meaning of an existing ID is a breaking change: add a new ID instead.

### Frontmatter

```yaml
---
id: AUTH                 # upper case, unique
title: Sign-in
status:
  ios: implemented       # planned | in-progress | implemented | n/a
  android: implemented
  web: planned
  backend: implemented
last_verified: 2026-11-19
related: [SESSION]       # IDs of other features, each with a row in INDEX.md
---
```

## Changing behavior

A change to product behavior updates the spec here **in the same pull request** as the code change. If only some platforms change, set the other platforms' status or add a row to "Platform differences" so the gap is visible. The pull request template asks for it.

## Decisions

A decision record in `decisions/` is short: frontmatter (`status`, `date`, `decision-makers`), then Context, Decision and Consequences. Start from [decisions/_template.md](decisions/_template.md) and number records in order (`0007-...`). A record that no longer holds gets `status: superseded` and a link to the record that replaces it; it is never deleted. Where a decision's date is not known, `date` says `unknown` and the record names its source.

## Checks

```
python3 feature-map/scripts/check.py
```

Validates frontmatter, requirement ID format and uniqueness, INDEX.md coverage and statuses, `related` IDs and relative links inside this repository. `make lint` and `make test` run it, so CI runs it with the tests. Standard library only, no dependencies.
