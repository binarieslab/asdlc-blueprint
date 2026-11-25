# ASDLC scorecard

The state of this repository against the ASDLC blueprint. A row passes only with evidence: a command and its output, a link to a pull request, or a refused action.

Profile: 
ASDLC-ready since: 

## Statuses

| Status | Meaning |
| --- | --- |
| (empty) | Open. Nothing is built yet. |
| `built, not run` | The check is written, but its exit check has not run: say where it has to run. |
| `waiting for owner` | Only the owner can do the step. Give the date agreed. |
| `passed, not merged` | The exit check ran on a branch. Name the branch. It becomes `passed` when the owner merges. |
| `passed` | The exit check ran through the stage's own command, and the change is merged. |
| `accepted, not verified` | The owner accepted an earlier pass without evidence. It blocks stage 7. |
| `not applicable` | The row does not apply to this profile. Give the reason. |

## Rows

| Stage | Row | Status | Evidence |
| --- | --- | --- | --- |
| 0 | Profile, protected paths and the owner's constraints confirmed | | |
| 1 | One command runs lint, the tests, and the build where the stack has one | | |
| 1 | The same command gates every merge in CI | | |
| 2 | Module boundaries are enforced by a check | | |
| 2 | Narrowed and forbidden APIs fail the check | | |
| 2 | The comment rule fails the check | | |
| 2 | A new dependency fails the check | | |
| 2 | A committed secret fails the check | | |
| 2 | Patterns marked "remove" are gone or forbidden for new code | | |
| 3 | A journey runs on the real product with no human present | | |
| 3 | An accessibility violation fails verification | | |
| 3 | A missing translation fails verification | | |
| 3 | The agreed journeys exist, the money flow first | | |
| 3 | A verification round posts a verdict with the evidence of each step | | |
| 4 | A change that breaks a shipped version fails a test | | |
| 4 | A feature that has reached users can be switched off in the agreed way | | |
| 4 | Rollback has been performed once | | |
| 4 | No agent session can read signing keys, store credentials or deploy tokens | | |
| 5 | An agent cannot merge or push to the default branch | | |
| 5 | A change to a protected path waits for the owner | | |
| 5 | Error reports show no personal data | | |
| 6 | `AGENTS.md` is at most 120 lines and duplicates no check | | |
| 6 | Every journey has a feature-map entry | | |
| 6 | The feature issue template asks for the expected effect | | |
| 7 | Five changes merged, with minutes and tokens recorded | | |
| 7 | Every correction became a check | | |

No row is left empty at the end: a row that does not apply is `not applicable` with the reason.

## Known gaps

What was found on the way and is not a stage's to fix, with where it was found and what the owner decided.

| Found in stage | Gap | Owner's decision |
| --- | --- | --- |
