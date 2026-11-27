# Stage 2: Constraints in code

**Purpose.** The strongest layer. After this stage an agent cannot break a company value or an architectural rule without a check failing.

**Look.**
- The real module structure and who imports whom.
- Where the stage 0 patterns occur and how often.
- APIs in this stack that are easy to misuse, with a count of each.
- The current dependency list: direct dependencies, one list per ecosystem.
- **Run every rule you are about to propose against the repository first.** Report the number of places that fail it, by directory. A rule the code already breaks needs the "existing places" ask below.
- Whether the linter in use can express each rule. If it cannot, say so in the ask.
- **The comment rule's reach.** Run the comment checker over the whole repository and report the total by directory. The template's `tool/comment_ban.py` reads Dart, Swift, Kotlin, Scala, Java, Go, JavaScript and TypeScript, C, C++, Objective-C, C#, Rust, Python and Ruby. It does not read HTML, CSS, templates such as `.astro` or `.vue`, Markdown, YAML or shell. If most of this repository's source is in a type it cannot read, say so before the owner decides.
- Deliberate fake credentials in tests and fixtures. A secrets scan will flag them.

**Ask.** Two rounds.

Round one:
- 2.1 **Boundaries.** Here is the module map I found. Which modules may depend on which? What is forbidden? A Confirm line if the repository's own docs already state the direction.
- 2.2 **Narrowed APIs.** Here are the APIs agents commonly misuse in this stack, with how often each appears here. Which are forbidden outright, and which are allowed only in named places?
- 2.3 **Comments.** Ban all comments, or allow named exceptions (licence headers, documentation of a library's public interface)? And which directories does the ban cover? Recommend the product's source; agent skills and vendored code are usually left out.
- 2.4 **Confirm** the dependency allow-list: the current direct dependencies. Any new one fails the check until the owner records a decision for it.
- 2.5 **Secrets.** Which scanner runs in the check command, and which files holding deliberate fake credentials go on a named list the owner approves?

Round two, with the draft pull request:
- 2.6 **Clean-up**, for each pattern marked "remove" in 0.3: remove now, or forbid new uses and open an issue? Leave it out, with a Confirm line, if nothing was marked.
- 2.7 **Existing places.** For each new rule that existing code fails: fix now, list the places in a named baseline, or narrow the rule?
- 2.8 **Confirm** the lint messages. Each says what to do instead. Show the three that matter most; the full list is in the pull request.
- 2.9 **Approval** for the exact files on protected paths: the lint configuration, the check tools, the workflow, the agent settings and the hook.
- 2.10 **Fact:** the owner's GitHub login, if 0.5 does not have it. The `owner-approval` job needs it.

**Do.** The rules, the dependency gate, the scanner, and the agreed clean-up, all added to the stage 1 command. Lint configuration and CI configuration become protected paths. The comment approval list is the owner's: never write to `tool/approved_comments.txt` and never run `--write-approved`. Propose the comments to approve in the pull request; the owner runs the command. Add `__pycache__/` to `.gitignore` before the first run of a Python tool.

**Exit check.** For each rule, a deliberate violation fails the check command with a message that says what to do instead. Adding an unlisted dependency fails. A planted fake secret fails. Each of these ran through the stage 1 command, not through the tool on its own.

| Profile | Note |
| --- | --- |
| `api` | Boundaries follow the layers: the domain depends on nothing outward. |
| `web-app` | The same layering. Browser storage, logging and raw HTML insertion are the usual narrowed APIs. |
| `apple-app`, `android-app`, `flutter-app` | The same layering, plus: user-facing text only through the localisation mechanism, never inline. |
| `library` | The public interface is a boundary. A change to it fails a check until it is recorded. |
| `web-static` | Every page exists in every supported language; a missing translation fails the build. Assets loaded from another host are a narrowed API. |

**From the template.** `tool/comment_ban.py` with `tool/tests/` and `tool/approved_comments.txt`, the comment ban line of `tool/lint.sh`, `.claude/settings.json`, `.claude/hooks/protect-lint-rules.sh`, `.github/workflows/lint-rules.yml`, `.github/dependabot.yml`, `docs/architecture/code-style-and-lint.md`. Each only where the repository has no equivalent.
- Replace `{{OWNER_LOGIN}}` in `lint-rules.yml` and in `code-style-and-lint.md`, and `{{ANALYZER_CONFIG}}`, `{{ANALYZE_COMMAND}}` and `{{FORMAT_CHECK_COMMAND}}` in `code-style-and-lint.md`.
- The protected paths are written three times: the `PROTECTED` pattern in `lint-rules.yml`, the deny list in `settings.json`, and `paths` in the hook. Set all three to decision 0.2. They name `tool/`; a repository that keeps its tools elsewhere changes that in all three.
- The hook needs `jq`. Without it the hook warns and lets every command through. Check that `jq` is installed where agents run, and tell the owner if it is not.
- After changing the hook, try it: a redirect into each check script and into the lint configuration must be refused.
- The owner creates the `lint-rules-approved` label.
- The template has no dependency gate, secrets scan or boundary rule. Those are built for the repository's stack in this stage, with their own tests.
