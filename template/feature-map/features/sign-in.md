---
id: AUTH
title: Sign-in
status:
  ios: implemented
  android: implemented
  web: planned
  backend: implemented
last_verified: 2026-11-19
related: []
---

# Sign-in

This spec is an example of the format. Replace it with your own features, or keep it as the first one if your product signs people in.

## Product

**Why it exists:** Everything in {{PROJECT_NAME}} belongs to a person. Signing in lets the same person reach their data from any device and keeps everyone else out.

**Who it is for:** Everyone with an account, on each device they use.

**What people can do:**
- As a member I can sign in with my email address and password, and let my password manager fill them in.
- As a member I can see why a sign-in failed, and try again without typing my email address again.
- As a member I can sign out of this device.

**What it is not:** There is no sign-in with Google, Apple or another provider ([decision 0002](../decisions/0002-no-third-party-sign-in.md)). Creating an account and resetting a password are separate features.

---

The sections below describe the behavior in detail for development.

## Scope

In scope: the sign-in form, the errors a sign-in can meet, staying signed in, and signing out of this device.

Owned elsewhere: creating an account, resetting a password, and deleting an account each have their own spec.

## Rules

| ID | Rule | Applies to |
|---|---|---|
| AUTH-001 | The sign-in form asks for an email address and a password. WHEN the user submits with either empty, the app SHALL show "Email is required" or "Password is required" under that field and send nothing. | App |
| AUTH-002 | The form SHALL fill in the email address last used for a successful sign-in on this device. | App |
| AUTH-003 | WHEN sign-in succeeds, the app SHALL store the token securely and open the home screen. | App |
| AUTH-004 | IF the backend refuses the email and password (`400`) THEN the app SHALL show "The email or password you entered is incorrect." with "Try again", which returns to the form with the email still filled in. | App and backend |
| AUTH-005 | IF the backend answers `500` or a status the app has no case for THEN the app SHALL show "Our servers are having trouble. Please try again later." and SHALL NOT suggest that the email or password is wrong. | App |
| AUTH-006 | IF the request never reaches the backend THEN the app SHALL say that the device is offline, keep what was typed, and SHALL NOT show the incorrect-password message. | App |
| AUTH-007 | WHILE a sign-in request is in flight, the submit button SHALL show a busy state and ignore further taps. | App |
| AUTH-008 | WHEN the user signs out, the app SHALL delete the stored token, tell the backend to end the login, and open the sign-in form. A failed call to the backend still signs the user out on the device. | App and backend |
| AUTH-009 | IF five sign-ins for the same account fail within 15 minutes THEN the backend SHALL refuse further attempts with `429` until 15 minutes after the last failure, and the app SHALL show "Too many attempts. Wait a few minutes, then try again." | App (planned in #42) and backend |

## Limits and constants

| Name | Value | Where it is enforced |
|---|---|---|
| Failed attempts before a pause | 5 within 15 minutes | Backend |
| Pause after too many attempts | 15 minutes after the last failure | Backend |

## Flow

1. The user enters an email address and a password and taps "Sign in".
2. The app checks that both are filled in (AUTH-001) and sends them.
3. The backend answers with a token, or with an error the app maps to a message (AUTH-004 to AUTH-006, AUTH-009).
4. On success the app stores the token and opens home (AUTH-003).

## States and errors

| Situation | What the user sees | HTTP status (if any) |
|---|---|---|
| Wrong email or password | "The email or password you entered is incorrect." with "Try again" | 400 |
| Too many attempts | "Too many attempts. Wait a few minutes, then try again." | 429 |
| Server failure | "Our servers are having trouble. Please try again later." | 500, or any other |
| Offline | An offline message; what was typed is kept | none |

## API contract

`POST /auth/login` with `email` and `password`; `200` returns the token. `DELETE /auth/login` ends the login. Full shapes: the backend's contract ({{API_CONTRACT_URL}}).

## Analytics

| Kind | Name | When |
|---|---|---|
| Event | `sign_in_succeeded` | AUTH-003 |
| Event | `sign_in_failed` with `reason` (`refused`, `server`, `offline`, `rate_limited`) | AUTH-004 to AUTH-006, AUTH-009 |

## Platform differences

| Topic | iOS | Android | Web | Backend | Reason |
|---|---|---|---|---|---|
| Where the token is stored | Keychain | Keystore | Browser storage the backend allows | n/a | Each platform's secure store |

## Open questions

- 2026-11-19: Should signing out on one device offer to sign out everywhere? Not decided.

## Implementation

| Platform | Entry points |
|---|---|
| App | `src/...`; how it works: [docs/features/_template.md](../../docs/features/_template.md) |
| Backend | `<backend repository>/...` |
