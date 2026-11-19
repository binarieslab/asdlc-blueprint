#!/bin/sh
set -eu
cd "$(dirname "$0")/.."

python3 tool/comment_ban.py --approved tool/approved_comments.txt .

{{ANALYZE_COMMAND}}

{{FORMAT_CHECK_COMMAND}}
