#!/bin/sh
set -eu
directory=$(mktemp -d)
trap 'rm -rf "$directory"' EXIT
printf 'package probe\n\nfunc probe() {\n\t// planted by the probe\n}\n' > "$directory/probe.go"
python3 tool/comment_ban.py "$directory"
