#!/bin/bash
# Copies this project (OneDrive) into the git working copy and pushes it to GitHub.
#   ./sync_to_github.sh "short message about what changed"
# The git copy lives OUTSIDE OneDrive (by default ~/Desktop/code/<folder-name>-git) because .git does not belong in a syncing folder.
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DST="${GIT_COPY:-$HOME/Desktop/code/$(basename "$SRC")-git}"   # override with GIT_COPY=/path/to/clone
[ -d "$DST/.git" ] || { echo "Git copy not found at $DST" >&2; exit 1; }
MSG="${1:-Update lessons}"
rsync -a --delete --exclude='.DS_Store' --exclude='seedance video/output/*.mp4' --exclude='.git' --exclude='.claude' --exclude='__pycache__' --exclude='.gitignore' --exclude='README.md' "$SRC"/ "$DST"/
cd "$DST"
git add -A
if git diff --cached --quiet; then echo "Nothing new to commit."; exit 0; fi
git commit -q -m "$MSG"
git push -q origin main
echo "Pushed: $(git log --oneline | head -1)"
git remote get-url origin
