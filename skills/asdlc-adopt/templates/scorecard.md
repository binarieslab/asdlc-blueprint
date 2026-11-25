# ASDLC scorecard

The state of this repository against the ASDLC blueprint. A row passes only with evidence: a command and its output, a link to a pull request, or a refused action.

Profile: 
ASDLC-ready since: 

| Stage | Row | Passes | Evidence |
| --- | --- | --- | --- |
| 0 | Profile and protected paths confirmed | | |
| 1 | One command runs lint, unit tests and build | | |
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
| 3 | A verification round posts a verdict with a screenshot per step | | |
| 4 | A change that breaks a shipped version fails a test | | |
| 4 | A released feature can be switched off without a release | | |
| 4 | Rollback has been performed once | | |
| 4 | No agent session can read signing keys or store credentials | | |
| 5 | An agent cannot merge or push to the default branch | | |
| 5 | A change to a protected path waits for the owner | | |
| 5 | Error reports show no personal data | | |
| 6 | `AGENTS.md` is at most 120 lines and duplicates no check | | |
| 6 | Every journey has a feature-map entry | | |
| 6 | The feature issue template asks for the expected effect | | |
| 7 | Five changes merged, with minutes and tokens recorded | | |
| 7 | Every correction became a check | | |

Rows that do not apply to a profile are marked "not applicable" with the reason; they are not left empty.
