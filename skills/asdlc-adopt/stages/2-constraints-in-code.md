# Stage 2: Constraints in code

**Purpose.** The strongest layer. After this stage an agent cannot break a company value or an architectural rule without a check failing.

**Look.** The real module structure and who imports whom; where the stage 0 patterns occur and how often; APIs in this stack that are easy to misuse; the current dependency list.

**Ask.**
- 2.1 **Boundaries.** Here is the module map I found. Which modules may depend on which? What is forbidden?
- 2.2 **Narrowed APIs.** Here are the APIs agents commonly misuse in this stack, with how often each appears here. Which are forbidden outright, and which are allowed only in named places?
- 2.3 **Comments.** Ban all comments, or allow named exceptions (licence headers, documentation of a library's public interface)?
- 2.4 **Dependencies.** The current list becomes the allow-list. Confirm it. Any new dependency fails the check until the owner records a decision for it.
- 2.5 **Secrets.** Which scanner runs in the check command?
- 2.6 **Clean-up.** For each pattern marked "remove" in 0.3: remove now, or forbid new uses and open an issue?
- 2.7 **Lint messages.** Each new rule's message says what to do instead. Review the wording.

**Do.** The rules, the dependency gate, the scanner, and the agreed clean-up. Lint configuration and CI configuration become protected paths.

**Exit check.** For each rule, a deliberate violation fails the check command with a message that says what to do instead. Adding an unlisted dependency fails. A planted fake secret fails.

| Profile | Note |
| --- | --- |
| `api` | Boundaries follow the layers: the domain depends on nothing outward. |
| `apple-app`, `android-app`, `flutter-app` | The same layering, plus: user-facing text only through the localisation mechanism, never inline. |
| `library` | The public interface is a boundary. A change to it fails a check until it is recorded. |
| `web-static` | Every page exists in every supported language; a missing translation fails the build. |

**From the template.** `tool/comment_ban.py` with `tool/tests/` and `tool/approved_comments.txt`, `.claude/settings.json`, `.claude/hooks/protect-lint-rules.sh`, `.github/workflows/lint-rules.yml`, `.github/dependabot.yml`, `docs/architecture/code-style-and-lint.md`. The template has no dependency gate, secrets scan or boundary rule; those are built for the repository's stack in this stage.
