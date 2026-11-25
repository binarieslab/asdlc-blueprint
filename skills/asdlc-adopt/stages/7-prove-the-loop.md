# Stage 7: Prove the loop by hand

**Purpose.** Evidence that the repository can be trusted with agent work, and the numbers to decide what comes next.

**Look.** The backlog, for candidates of different kinds.

**Ask.**
- 7.1 Which five real changes are done? Recommended: three small features and two bugs.
- 7.2 What is recorded for each? Recommended: the owner's minutes, the tokens used, whether verification passed first time, which checks caught a mistake, and whether anything was reverted.
- 7.3 After the first two: what counts as good enough for this repository?

**Do.** Each change runs the full path with a coding agent started by the owner: issue, tests first, implementation, `make check`, a pull request with "What to check in the app", a verification round by a fresh session, the owner's merge. After each change, every correction the owner had to make is turned into a check (back to stage 2 or 3) and recorded.

**Exit check.** Five changes merged with their numbers recorded. Every correction ended as a check. All scorecard rows pass. The scorecard is marked "ASDLC-ready" with the date.

**From the template.** The loop in the blueprint's `README.md`, "How the loop runs, day to day".
