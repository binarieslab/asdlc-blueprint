# Testing strategy

The testing charter for {{PROJECT_NAME}}: what is worth testing, the pattern to follow per layer, the tests that drive the app like a user, and the rules no test may break. Tests are the strongest tool an agent has to validate its own work, so they come first: an agent turns the issue's acceptance criteria into tests before it writes the implementation. [AGENTS.md](AGENTS.md) has the short, always-loaded version of this policy.

## Test first

Before implementing new logic, a use case with a branch, a repository method with a caching or mapping rule, or a view model method with more than one resulting state, list its scenarios: the success, every error variant and the edge cases. Write them as failing tests where practical, or at least as a checklist on the issue. Then implement until they pass.

The issue's "Test scenarios" section is where this starts. If the requirements don't make the expected behavior clear ("what should happen on a 404 here?"), stop and ask on the issue with `needs:human`. Don't guess and build both the code and the test around the same unverified assumption.

Skip this for a one-line delegate with no branch and a plain data holder with no custom logic (below).

## What is worth testing

Test logic, not the computer. A unit deserves its own test when it has at least one of:

- a **conditional or branch** (an `if`, a `switch`, a short-circuit)
- a **mapping rule** (an HTTP status to a result variant, an enum to a wire string)
- a **cache or invalidation rule** (hit or miss, a forced refresh, an update after a write)
- an **orchestration** across several calls (does step 2 run only when step 1 succeeded?)
- an **edge case** (null, empty, malformed input, a boundary value)

Don't write a dedicated test for:

- a one-line delegate with no branch: nothing can go wrong that the compiler wouldn't catch, and the test of its caller exercises it anyway;
- a plain data holder whose parsing is a straight field-by-field mapping: the test of the code that decodes it exercises it; it deserves its own test once it has custom parsing;
- a test that only re-reads a value it just passed in.

## Per-layer pattern

One row per layer, each with a real file in this repository to copy. Fill it in as the first test of each kind lands.

| Layer | Pattern to copy | What good looks like |
|---|---|---|
| Use case | {{path to a test}} | One test per branch, named for the scenario, not the mechanism. Prove that a short-circuit short-circuits (the next call never happens), not only that the result is right. |
| Remote data source | {{...}} | Asserts the request (method, path, body, headers) and has one test per status code the code switches on, asserting the exact result. |
| Repository | {{...}} | Cache hit (no remote call) against cache miss against forced refresh; a successful write updates the cache; a failed call leaves it untouched. |
| View model | {{...}} | Asserts the sequence of states, not only the last one, and that nothing is saved or sent on the paths where it shouldn't be. |
| Screen (snapshot) | {{...}} | One snapshot per visually distinct state, light and dark (below). |
| Journey (UI integration) | {{...}} | The real app on a fake backend, driven like a user (below). |

## Test descriptions are the scenario

Comments are banned in tests as in the code, so the description carries the scenario, and it cites the requirement ID it proves:

```
group("AUTH-004 a refused sign-in")
  test("shows the incorrect-password message and keeps the email")
  test("returns to the form with the email filled in after Try again")
```

Blank lines separate setup, action and assertions.

## Journeys: UI integration tests

A journey runs the whole app, its real wiring and screens, with everything outside it replaced, and drives it like a user. It is the layer for behavior that only shows when the layers run together: an expired session travelling from the network layer to the sign-in screen, or a write on one screen reaching another that is already open. Everything else stays a unit test.

- **One file per flow**, in {{test/journeys/}}, written from the issue's "Test scenarios":

  ```
  Given a registered user
    and a reachable backend
  When the user signs in with a wrong password
  Then the incorrect-password message shows
    and the email is still filled in
  ```

- **The backend is a fake that answers like the real one**: the same routes, status codes and error bodies as its contract, by the caller's role, so a journey can send what the app hides and see the backend refuse it.
- **The outside world is fake**: storage, push, connectivity, biometrics, the clock and the locale are in-memory and controlled by the test.
- **Journeys run headless in `make test`**, so CI runs them on every pull request. Device-level tests ({{integration_test/, XCUITest, Espresso, Playwright}}) are slower; keep them for the few flows that need a real device or browser.

Tools by stack: Flutter widget tests over the real app, or `integration_test`; XCUITest for iOS; Espresso or Compose UI tests for Android; Playwright for the web.

## Snapshot tests

Snapshots catch what a reader can't see in a diff: a colour that disappears in dark mode, a label that overflows in a longer language. Keep the suite budgeted, not exhaustive.

- One snapshot per **visually distinct** state, meaning the rendered tree differs, not the state class. Five error states that render the same card with different text are one snapshot.
- Light and dark, one device, one language, by default. Add a second language only where its copy is long enough to break a layout.
- **A snapshot must never read the clock.** Make the current time injectable and pin it from the test, and use fixed dates in fixtures; otherwise the image fails the next day.
- Turn animations off in snapshots, so an image never captures a half-finished frame.
- After recording, run the suite again without the update flag to confirm the images are stable.

## Rules no test may break

- Do not weaken, skip or delete a test to make it pass. A failing test is either a bug in the code or a wrong expectation; say which in the pull request.
- A test never depends on the order it runs in, the network, or today's date.
- A bug fix comes with the test that would have caught it.

## Coverage baseline

{{The date, the coverage per layer then, and the gaps known. Coverage is a signal, not a goal.}}

## Backlog

{{Tests known to be missing, each with its issue, so they aren't lost.}}
