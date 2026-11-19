---
id: FEATURE
title: Feature name
status:
  ios: planned
  android: planned
  web: planned
  backend: planned
last_verified: YYYY-MM-DD
related: []
---

# Feature name

## Product

Plain language, no technical terms. Someone who has never seen the code should understand the feature from this section alone.

**Why it exists:** the user's problem or need, in one or two sentences.

**Who it is for:** which roles, in which situation.

**What people can do:**
- As a member I can ...
- As an admin I can ...

**What it is not:** what people should not expect from it.

---

The sections below describe the behavior in detail for development.

## Scope

What belongs to this feature, and what explicitly does not (link the spec that owns it instead).

## Rules

| ID | Rule | Applies to |
|---|---|---|
| FEATURE-001 | WHEN ... the app SHALL ... | App |
| FEATURE-002 | IF ... THEN the backend SHALL ... | Backend |

Write one observable behavior per row. Start with WHEN (an event), WHILE (a state) or IF ... THEN (an unwanted case) where it helps; plain sentences are fine otherwise. "App" means every client platform; a rule decided but not built yet names its issue, for example `App (planned in #25)`.

## Limits and constants

| Name | Value | Where it is enforced |
|---|---|---|

## Flow

Short numbered steps from the user's action to the result. Only when the order matters.

## States and errors

| Situation | What the user sees | HTTP status (if any) |
|---|---|---|

## API contract

Endpoints, with the request and response fields that matter here, and a link to the section of the backend's contract ({{API_CONTRACT_URL}}). Do not copy what is already there in full.

## Analytics

| Kind | Name | When |
|---|---|---|

## Platform differences

| Topic | iOS | Android | Web | Backend | Reason |
|---|---|---|---|---|---|

## Open questions

Unresolved conflicts between spec, code and other docs, and product questions not decided yet. Each with the date found.

## Implementation

| Platform | Entry points |
|---|---|
| App | `src/...`; how it works: [docs/...](../../docs/README.md) |
| Backend | `<backend repository>/...` |
