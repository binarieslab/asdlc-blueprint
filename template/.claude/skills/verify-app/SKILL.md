---
name: verify-app
description: Opens {{PROJECT_NAME}} built from a pull request's head against development, signs in with a test account for a role, and drives it like a user, keeping a screenshot of every step. Used by the verifier agent (.claude/agents/verifier.md) during a verification round; never by the session that built the change.
---

# Verify the app

How to open the app built from a pull request's head and use it as a user would. The verifier agent decides *what* to check; this skill says *how* to get there. Each section below says what to write in it; replace that guidance with the commands that work for this repository, and test them once by hand.

## Before you start

- The pull request's number, its head commit and an evidence folder outside every checkout, from the session that runs the round.
- The test accounts, one per role, in `{{TEST_ACCOUNTS_FILE}}` outside the repository, for example `~/.config/{{GITHUB_OWNER}}/dev-test-accounts.env`. Never read them aloud, print them, paste them into a comment, or take a screenshot that shows one. If the file is missing or a role has no account, every step that needs that role is "couldn't check".
- Development only. The app never talks to production during a check.

## 1. Build the head in a worktree of its own

```bash
git fetch origin pull/<n>/head
git worktree add <evidence folder>/worktree <sha>
cd <evidence folder>/worktree
{{the install and build commands, with the development configuration}}
```

Never build in the builder's checkout, and never switch its branch.

## 2. Confirm the build

Confirm that the running app is the head's build and talks only to development: {{for example, a build number or commit shown in the app's settings or about screen, or the base URL in the log}}. If either can't be confirmed, stop: every step is "couldn't check".

## 3. Start it

| Platform | Start | Screenshot |
|---|---|---|
| iOS simulator | {{`xcrun simctl boot "<device>"`, then install and launch the built `.app` with `xcrun simctl install booted <app>` and `xcrun simctl launch booted <bundle id>`}} | `xcrun simctl io booted screenshot <file>.png` |
| Android emulator | {{`emulator -avd <name>`, then `adb install -r <apk>`}} | `adb exec-out screencap -p > <file>.png` |
| Browser | {{the local server command and its address}} | a browser automation tool such as Playwright: `page.screenshot({ path: "<file>.png" })` |

Use the tools your agent has to tap, type and scroll, such as a simulator control tool or a browser tool, and read what is on screen from the accessibility tree where you can rather than from pixels.

## 4. Sign in

Sign in through the app's own sign-in screen with the account for the step's role, reading the values from the test accounts file without echoing them. Sign out before switching roles.

## 5. Do the steps

For each step: reach the screen as `features/` describes, do what the step says, wait for the result, and take a screenshot named `<round>-<step>-<pass|fail|unchecked>.png` in the evidence folder.

## 6. Clean up

Stop only what you started (the app, the simulator or emulator if you booted it, the local server), remove the worktree with `git worktree remove`, keep the evidence folder, and leave the test accounts as you found them: undo any change a step made to an account that other checks rely on.

## features/

One file per feature or area of the app: how to reach each screen, which role and test data it needs, what to wait for, and the traps a first visit falls into. Start a new one from [features/_template.md](features/_template.md). A verdict's "project" finding about how to reach or drive a screen is fixed here, in the same pull request.
