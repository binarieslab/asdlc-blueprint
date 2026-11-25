# Stage 4: Release safety

**Purpose.** A change cannot hurt users who are already running a shipped version, and a bad release can be withdrawn or switched off.

**Look.** How the product is built, signed, submitted and deployed today; which versions are in users' hands; where credentials and signing keys are stored; how data schemas change.

**Ask.**
- 4.1 **Compatibility.** How many shipped app versions must the API keep serving? What is the oldest supported version, and how is an older one told to update?
- 4.2 **Contract.** What is the source of truth for the interface between API and apps, and how is it tested against the requests of shipped versions?
- 4.3 **Feature flags.** How is a feature switched off after release without a new store submission? Is there a mechanism already, or is a minimal one needed? New features default to off.
- 4.4 **Data changes.** Confirm the rule: additive first, remove only after no shipped version needs the old shape.
- 4.5 **Submission.** Confirm: submission to the stores is done by the owner. Is phased release the default?
- 4.6 **Rollback.** For what is deployed directly (API, websites): how is the previous version restored, and has that been tried?
- 4.7 **Credentials.** Signing keys and store credentials are not readable by any account an agent runs under. Where do they live, and does deployment use short-lived credentials?

**Do.** The contract test, the flag default, the rollback note, and whatever 4.7 requires.

**Exit check.** A change that breaks a shipped version's request fails a test. A feature can be switched off without a release. The rollback has been performed once. An agent session cannot read a signing key.

| Profile | Note |
| --- | --- |
| `api` | This stage matters most here. Apps cannot be recalled. |
| `apple-app`, `android-app`, `flutter-app` | The app tolerates fields it does not know and the absence of fields it does not need. |
| `library` | Version numbers follow the public interface: a breaking change is a major version. |
| `web-static` | Rollback is redeploying the previous build. |

**From the template.** None. The template does not cover release safety yet; everything in this stage is built for the repository.
