#!/usr/bin/env bash
# Make a copy of a video with its last frame held for extra seconds (e.g. so viewers can read the final state).
# Runs locally with macOS's own video framework: no API call, no cost. The original is not changed.
# Usage: ./hold_last_frame.sh VIDEO.mp4 [SECONDS]      (default 2 seconds; output is VIDEO_hold.mp4)
set -euo pipefail
cd "$(dirname "$0")"
SRC="${1:?Usage: ./hold_last_frame.sh VIDEO.mp4 [SECONDS]}"
SECS="${2:-2}"
[ -f "$SRC" ] || { echo "Not found: $SRC" >&2; exit 2; }
[[ "$SECS" =~ ^[0-9]+$ ]] && [ "$SECS" -ge 1 ] && [ "$SECS" -le 30 ] || { echo "SECONDS must be 1-30" >&2; exit 2; }
DST="${SRC%.*}_hold.mp4"
[ ! -e "$DST" ] || { echo "$DST already exists; move it first." >&2; exit 2; }
swift tools/hold_last_frame.swift "$SRC" "$DST" $(( SECS * 24 )) 2>/dev/null
echo "Saved: $DST"
