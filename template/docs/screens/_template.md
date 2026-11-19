# Screen name

**Folder:** `src/.../screens/<name>/`
**Reached from:** every screen or event that opens this one, each linked to its doc.

## Purpose

Two or three sentences: what the user comes here to do. Link the feature-map spec whose rules this screen implements, for example [AUTH](../../feature-map/features/sign-in.md).

## States

One bullet per state the screen renders, with the data it carries and exactly what the user sees in it, copy included:

- `Idle(email)`: the form, with the last email address filled in (AUTH-002).
- `Loading`: the request is in flight; the button shows a busy state (AUTH-007).
- `Refused`: "The email or password you entered is incorrect." with "Try again" (AUTH-004).

## Data flow

What runs when the screen opens and after each user action, in order: which use case, which repository, which endpoint, which cache. Name what is loaded again after a successful write.

## User actions

| Action | What happens |
|---|---|
| Taps "Sign in" | ... |

## Navigation

Where each outcome leads, and whether the screen is pushed, replaced or closed.

## Backend contract

The source of truth for the request and response shapes this screen relies on, taken from the code that calls them:

| Method and path | Request | Response | Status codes and what the app does with each |
|---|---|---|---|

## Notes and edge cases

Why the screen is built the way it is: the decisions behind it, with their date and issue, and the edge cases a reader would not guess from the code. This is where the explanation a comment would have carried belongs.
