# Stage 4: Release safety

**Purpose.** A change cannot hurt users who are already running a shipped version, and a bad release can be withdrawn or switched off.

In this stage a **release** is whatever puts a new version in users' hands. For a store app it is a store submission. For an API or a website it is a deploy.

**Look.**
- What the repository's own docs already say about releases, compatibility and rollback, and which questions they leave open. Propose nothing that contradicts them without saying so.
- How the product is built, signed, submitted and deployed today, and whether a merge deploys by itself.
- Which versions are in users' hands, and who else loads what this repository publishes.
- Where the real requests of shipped versions can be had. They often live in the app repositories, not here.
- How data schemas change.
- Which credential names the place you work in can see. List names only, never values.

**Ask.** Two rounds.

Round one:
- 4.1 **Compatibility.** Which shipped versions must keep working? What is the oldest supported one, and how is an older one told to update?
- 4.2 **Contract.** What is the source of truth for the interface, and how is it tested against the requests of shipped versions? If those requests live in another repository, ask as a Fact where to get them.
- 4.3 **Feature flags.** How is a feature switched off after it has reached users? Is there a mechanism already, or is a minimal one needed? New features default to off. Say for each option what the switch costs: a setting changed at run time, or a deploy.
- 4.7 **Credentials.** Signing keys, store credentials and deploy tokens are not readable by any account an agent runs under. Ask as a Fact where they live and whether deployment uses short-lived credentials. Name the ones you could see.

In the same round, as Confirm lines:
- 4.4 **Data changes.** Additive first; remove only after no shipped version needs the old shape.
- 4.5 **Submission.** Submission to the stores is done by the owner; phased release is the default. `not applicable` where nothing goes through a store.

Round two, with the draft pull request:
- 4.6 **Rollback.** How is the previous version restored, and has that been tried? You write the steps; the owner performs them. Ask for the date.
- 4.8 **Approval** for the exact protected files: infrastructure, the deploy workflow, the agent settings.

**Do.** The contract test, the flag mechanism or its default, the rollback steps, and whatever 4.7 requires. You never perform a production rollback or a deploy, and you never hold the credentials for one.

**Exit check.**
- A change that breaks a shipped version's request fails a test. Break it on purpose and show the failure.
- A feature can be switched off in the way 4.3 decided, shown once on a development environment.
- The rollback has been performed once, by the owner. Until then the row is `waiting for owner`.
- An agent session cannot read a signing key or a deploy credential. The evidence is two things: a script that lists the credential names visible in the agent's environment and finds none of the forbidden ones, and a fresh agent session that is asked to read a key file and is refused.

| Profile | Note |
| --- | --- |
| `api` | This stage matters most here. Apps cannot be recalled. A flag that needs a deploy passes; a flag that needs a store submission does not. |
| `apple-app`, `android-app`, `flutter-app` | The app tolerates fields it does not know and the absence of fields it does not need. A flag is switched without a store submission. |
| `library` | Version numbers follow the public interface: a breaking change is a major version. |
| `web-app` | The shipped version is a browser tab that was open during a deploy, and the API version the app was built against. 4.5 is `not applicable`. A flag in a static file needs a deploy: that passes only if the owner accepts it in 4.3; a switch at run time needs a store the page reads, which usually touches protected paths. |
| `web-static` | The shipped versions are whatever loads what this site publishes: script bundles, feeds, public URLs and redirects. The contract test checks their names and shapes. 4.4 and 4.5 are `not applicable`. 4.3 may be "not applicable, rollback instead": rollback is redeploying the previous build. |

**From the template.** None. The template does not cover release safety yet; everything in this stage is built for the repository.
