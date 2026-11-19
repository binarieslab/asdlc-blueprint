#!/bin/sh
block() {
	echo "Blocked: this command would change or approve the lint rules ($1). Only the repository owner does that; ask the owner instead. See docs/architecture/code-style-and-lint.md." >&2
	exit 2
}

command -v jq >/dev/null 2>&1 || { echo "protect-lint-rules: jq not found, lint-rule protection for shell commands is off" >&2; exit 0; }
command=$(jq -r '.tool_input.command // empty')
[ -z "$command" ] && exit 0

case "$command" in
	*--write-approved*) block "approving comments" ;;
	*lint-rules-approved*)
		echo "$command" | grep -Eq '(--add-label|--label|[[:space:]]-l)([[:space:]]+|=)[^[:space:]]*lint-rules-approved' && block "adding the lint-rules-approved label"
		echo "$command" | grep -Eq '(^|[^[:alnum:]])(gh[[:space:]]+api|curl)[[:space:]]' && echo "$command" | grep -q '/labels' && block "adding the lint-rules-approved label"
		;;
esac

paths='tool(/|[[:space:]]|$)|feature-map/scripts|analysis_options\.yaml|\.swiftlint\.yml|\.swift-format|eslint\.config\.|\.eslintrc|\.golangci\.ya?ml|detekt\.yml|ruff\.toml|\.github/workflows|\.claude/settings\.json|\.claude/hooks'

checks='python3?[[:space:]]+(\./)?(tool/comment_ban\.py|feature-map/scripts/check\.py|-m[[:space:]]+unittest[[:space:]]+discover[[:space:]]+-s[[:space:]]+tool/tests)'
rest=$(printf '%s\n' "$command" | sed -E "s#$checks##g")

protected="(^|[[:space:]=./\"'])($paths)"
printf '%s\n' "$rest" | grep -Eq "$protected" || exit 0

redirect_into_protected=">{1,2}[[:space:]]*[^[:space:]]*($paths)"
printf '%s\n' "$rest" | grep -Eq "$redirect_into_protected" && block "redirect"

writers='(^|[[:space:];&|(`])(tee|sed[[:space:]]+-i|perl|python3?|ruby|node|awk|mv|cp|rm|rmdir|truncate|touch|chmod|ln|install|dd|patch|ed|ex|vi|vim|nano|git[[:space:]]+(checkout|restore|apply|reset|stash|mv|rm|am|cherry-pick|revert))([[:space:]]|$)'
printf '%s\n' "$rest" | grep -Eq "$writers" && block "a write to a protected path"

exit 0
