#!/bin/bash
# Makes a printable PDF of every lesson in lessons/ using headless Chrome and each page's print styles.
# The PDF is saved next to the lesson, e.g. lessons/force-04-pressure.pdf, and deploy.sh uploads it.
#   ./make_pdfs.sh              # all lessons
#   ./make_pdfs.sh force-04     # only lessons whose file name starts with this
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lessons"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || { echo "Error: Google Chrome not found at $CHROME" >&2; exit 1; }
PROFILE="$(mktemp -d)"
trap 'rm -rf "$PROFILE"' EXIT
shopt -s nullglob
count=0
for f in "$DIR"/${1:-}*.html; do
  name="$(basename "$f" .html)"
  case "$name" in index|lesson-template) continue ;; esac
  rm -f "$DIR/$name.pdf"
  # Chrome writes the PDF but may not exit by itself, so start it, wait for the file, then stop it.
  "$CHROME" --headless=new --disable-gpu --no-sandbox --user-data-dir="$PROFILE" \
    --no-pdf-header-footer --virtual-time-budget=3000 \
    --print-to-pdf="$DIR/$name.pdf" "file://$f" >/dev/null 2>&1 &
  pid=$!
  for _ in $(seq 1 60); do
    if [ -s "$DIR/$name.pdf" ]; then sleep 1; break; fi
    sleep 1
  done
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  [ -s "$DIR/$name.pdf" ] || { echo "Failed: $name" >&2; exit 1; }
  echo "  $name.pdf ($(du -k "$DIR/$name.pdf" | cut -f1) KB)"
  count=$((count + 1))
done
echo "Made $count PDF(s)."
