# Adopting the blueprint

A checklist for bringing the blueprint into a repository, in the order that works. Most of it is a day of work for one repository; the specs and the docs grow from there with every change.

There are two ways to adopt. This checklist is the one you follow by hand. The other is the [`asdlc-adopt` skill](skills/asdlc-adopt/SKILL.md), which has an agent do the work with you: it brings the pieces in one stage at a time, checks first and written rules last, asks you for each decision, and keeps a scorecard. Both use the same template.

## 1. Copy the template

```bash
cp -R asdlc-blueprint/template/. path/to/your-repository/
cd path/to/your-repository
chmod +x tool/lint.sh tool/comment_ban.py feature-map/scripts/check.py .claude/hooks/protect-lint-rules.sh
echo "__pycache__/" >> .gitignore
```

If the repository already has an `AGENTS.md`, a `CLAUDE.md`, a `Makefile` or a pull request template, merge the blueprint's sections into yours rather than overwriting them.

## 2. Replace the placeholders

```bash
grep -rnE '(^|[^$])\{\{' AGENTS.md CLAUDE.md TESTING_STRATEGY.md Makefile docs feature-map tool .claude .github
```

The pattern skips GitHub's own `${{ ... }}` expressions in the workflows.

| Placeholder | What it becomes | Example |
|---|---|---|
| `{{PROJECT_NAME}}` | the product's name | `Acme` |
| `{{GITHUB_OWNER}}` and `{{REPO}}` | the repository on GitHub | `acme-inc` and `acme-ios` |
| `{{OWNER_LOGIN}}` | the GitHub login of the person who approves lint rule changes | `octocat` |
| `{{OWNER_NAME}}` | the decision-maker named in decision records | `Ada` |
| `{{BOARD_NAME}}` and `{{BOARD_URL}}` | the GitHub Project where every task lives | `Acme Delivery` |
| `{{API_CONTRACT_URL}}` | where the backend's endpoint contract lives | the backend's `README.md` on GitHub |
| `{{DEV_ENVIRONMENT}}` | the development backend agents may talk to | `https://dev.api.example.com` |
| `{{ANALYZE_COMMAND}}` and `{{FORMAT_CHECK_COMMAND}}` | in `tool/lint.sh`; the table in `docs/architecture/code-style-and-lint.md` lists them per stack | `flutter analyze` |
| `{{TEST_COMMAND}}` | in the `Makefile` | `flutter test` |
| `{{ANALYZER_CONFIG}}` | the analyzer's configuration file, which agents may not change | `analysis_options.yaml` |
| `{{TEST_ACCOUNTS_FILE}}` | where the development test accounts live, outside the repository | `~/.config/acme/dev-test-accounts.env` |
| `{{LANGUAGES}}` and `{{DEFAULT_LANGUAGE}}` | in `feature-map/principles.md` | `English and German`, `English` |

Text between `{{` and `}}` that is a sentence rather than a name is guidance: replace it with your project's facts. `AGENTS.md`, `docs/README.md` and the verification skill have the most of it.

## 3. Wire in your stack

- **`tool/lint.sh`**: the analyzer and the format check for your stack, warnings treated as errors.
- **`Makefile`**: the test command in `test`. Add the commands an agent needs to build and run the app.
- **`.github/workflows/ci.yml`**: replace the Flutter setup step with your stack's (see `docs/architecture/github-workflows.md`), pinned to a commit.
- **`.github/workflows/docs.yml`**: set `CODE` to the folders that hold your code and `GENERATED` to your generated files.
- **Protected paths**: `.claude/settings.json`, `.claude/hooks/protect-lint-rules.sh` and `lint-rules.yml` protect the common analyzer configurations of several stacks. Keep yours, remove the rest if you like, and keep the three lists the same.
- **Comment ban**: in `tool/comment_ban.py`, add your generated files to `GENERATED_FILES`, your build folders to `SKIP_DIRS`, and set `ALLOW_ONE_LINE_DOC` if you want one short doc line on public interfaces.

## 4. Run the comment ban once

```bash
python3 tool/comment_ban.py --full .
```

In an existing code base this reports every comment there is. Move what each one explains into `docs/` or the feature map, then delete the comments, so the check passes on the whole repository and new code starts at zero. Record the starting count under Baseline in `docs/architecture/code-style-and-lint.md`. Approve a comment one by one only where there is no other way.

## 5. Set up GitHub

These are the owner's steps; agents never do them.

1. Create the labels (`docs/architecture/github-workflows.md` has the commands): `docs-not-needed`, `lint-rules-approved`, `needs:human`.
2. Create a GitHub Project for the organization or the user, with a Status field (for example Todo, In progress, In review, Done), and add the repository's issues to it. Put its link in `AGENTS.md`.
3. Make `lint`, `build_and_test`, `docs-updated` and `owner-approval` required status checks on `main` (a ruleset or branch protection). Add `agent-verdict` once verification rounds run on every pull request.
4. Install `jq` wherever agents run, so the hook can read the commands it checks.

## 6. Write the first documents

1. **`AGENTS.md`**: what the project is, its architecture, its conventions, and its commands.
2. **`feature-map/`**: replace the example sign-in spec and decision with your own. Start with the features you change most; a spec is written fully the first time an issue touches its feature. Keep `features/_template.md`'s `status` keys in line with your platforms; the check reads them from there.
3. **`docs/`**: the architecture overview in `docs/README.md` first, then one screen or capability doc each time a change touches one.
4. **`TESTING_STRATEGY.md`**: fill in the per-layer table as each kind of test lands.
5. **`.claude/skills/verify-app/`**: the build, start and screenshot commands that work for your app, tried once by hand, and the test accounts file for each role.

## 7. Run the first loop

Pick a small issue, write it from the template, and run the loop from the [README](README.md#how-the-loop-runs-day-to-day): one session builds, a fresh session verifies, you merge. Every "project" finding in the verdict is a gap in the docs; fixing it there is how the setup gets better with each change.
