---
status: accepted
date: YYYY-MM-DD
decision-makers: [{{OWNER_NAME}}]
---

# No sign-in with third-party providers

This record is an example of the format. Replace it with your own decisions.

## Context

Signing in with Google or Apple is convenient for users, but each provider adds a dependency, a review requirement in the app stores, and an account-linking problem when the same person later signs in with a password.

## Decision

Accounts sign in with an email address and a password only. There is no sign-in with Google, Apple or any other provider.

## Consequences

- [Sign-in](../features/sign-in.md) says so under "What it is not", and agents do not add a provider without a new decision that supersedes this one.
- Users depend on their password manager, so the sign-in form supports autofill.
