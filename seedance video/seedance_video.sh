#!/usr/bin/env bash
# General Seedance 2.5 video generator (BytePlus ModelArk). Submits exactly one job, never retries,
# polls until done and downloads the MP4 into output/ next to this script.
#
# Usage:
#   ./seedance_video.sh --prompt-file prompts/NAME.txt [options]
#
# Options:
#   --first IMAGE       first frame (JPEG, PNG or HEIC). Without it the video is made from the prompt alone.
#   --last IMAGE        last frame. Needs --first.
#   --resolution R      480p (default, a cheap draft), 720p or 1080p.
#   --duration S        4-30 seconds, default 4.
#   --ratio R           only for prompt-only videos (no --first): 16:9 (default), 4:3, 1:1, 3:4, 9:16, 21:9.
#   --audio             let Seedance generate sound too (off by default; may cost more).
#   --name NAME         output file name prefix (default: the prompt file's name).
#   NO_COMPRESS=1       (environment variable) do not make the compressed web copy in compressed/
#   --dry-run           build the request and print it with image data shortened. No key read, no call made.
#   --fetch TASK_ID     submit nothing: keep polling a job that was already submitted and download it.
#
# Images are converted to JPEG, shrunk so the long side is at most 2048 px, and stripped of all metadata
# (including GPS location) before sending. The originals are only read.
# The API key is read from ~/seedance-key.txt (or the file named in $SEEDANCE_KEY_FILE) and passed to curl on stdin.
# It is never printed or logged. Keep the key file OUTSIDE this folder and outside OneDrive/cloud storage.
set -euo pipefail
set +x

cd "$(dirname "$0")"
FIRST=""; LAST=""; PROMPT_FILE=""; RESOLUTION="480p"; DURATION=4; RATIO="16:9"
AUDIO=false; NAME=""; DRY_RUN=0; FETCH_ID=""
while [ $# -gt 0 ]; do
  case "$1" in
    --first) FIRST="${2:-}"; shift ;;
    --last) LAST="${2:-}"; shift ;;
    --prompt-file) PROMPT_FILE="${2:-}"; shift ;;
    --resolution) RESOLUTION="${2:-}"; shift ;;
    --duration) DURATION="${2:-}"; shift ;;
    --ratio) RATIO="${2:-}"; shift ;;
    --audio) AUDIO=true ;;
    --name) NAME="${2:-}"; shift ;;
    --dry-run) DRY_RUN=1 ;;
    --fetch) FETCH_ID="${2:-}"; shift ;;
    -h|--help) sed -n '2,24p' "$0"; exit 0 ;;
    *) echo "Unknown argument: $1 (try --help)" >&2; exit 2 ;;
  esac
  shift
done

MODEL="dreamina-seedance-2-5-260628"
BASE="https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks"
KEY_FILE="${SEEDANCE_KEY_FILE:-$HOME/seedance-key.txt}"
MAX_WAIT_SECONDS=1800
mkdir -p output

if [ -z "$FETCH_ID" ]; then
  [ -n "$PROMPT_FILE" ] && [ -s "$PROMPT_FILE" ] || { echo "Give a non-empty --prompt-file (try --help)" >&2; exit 2; }
  case "$RESOLUTION" in 480p|720p|1080p) ;; *) echo "Resolution must be 480p, 720p or 1080p" >&2; exit 2 ;; esac
  if ! [[ "$DURATION" =~ ^[0-9]+$ ]] || [ "$DURATION" -lt 4 ] || [ "$DURATION" -gt 30 ]; then
    echo "Duration must be a whole number of seconds from 4 to 30" >&2; exit 2
  fi
  [ -z "$LAST" ] || [ -n "$FIRST" ] || { echo "--last needs --first as well" >&2; exit 2; }
  for f in "$FIRST" "$LAST"; do
    [ -z "$f" ] || [ -f "$f" ] || { echo "Image not found: $f" >&2; exit 2; }
  done
  [ -n "$NAME" ] || NAME=$(basename "$PROMPT_FILE" .txt)
  NAME=$(printf '%s' "$NAME" | tr -c 'A-Za-z0-9._-' '_')
fi

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

if [ -z "$FETCH_ID" ]; then
  # macOS sips reads HEIC/PNG/JPEG; Pillow then resizes and re-encodes without metadata.
  [ -z "$FIRST" ] || sips -s format jpeg "$FIRST" --out "$WORK/first_src.jpg" >/dev/null
  [ -z "$LAST" ] || sips -s format jpeg "$LAST" --out "$WORK/last_src.jpg" >/dev/null
  python3 - "$WORK" "$PROMPT_FILE" "$MODEL" "$RESOLUTION" "$DURATION" "$RATIO" "$AUDIO" <<'EOF'
import base64, json, os, sys
from PIL import Image, ImageOps
work, prompt_file, model, resolution, duration, ratio, audio = sys.argv[1:]
prompt = open(prompt_file).read().strip()

def prepare(src, dst, size=None):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        if size:                                   # match the first frame exactly
            im = ImageOps.fit(im, size, Image.LANCZOS)
        elif max(im.size) > 2048:
            scale = 2048 / max(im.size)
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        w, h = im.size
        # Seedance image limits: 300-6000 px per side, aspect ratio 0.4-2.5.
        assert min(w, h) >= 300 and 0.4 <= w / h <= 2.5, f"{src}: {w}x{h} is outside Seedance limits"
        im.save(dst, "JPEG", quality=92)           # no exif= argument, so no metadata is written
        return im.size

content = [{"type": "text", "text": prompt}]
first_src, last_src = os.path.join(work, "first_src.jpg"), os.path.join(work, "last_src.jpg")
if os.path.exists(first_src):
    size = prepare(first_src, os.path.join(work, "first.jpg"))
    print(f"First frame: {size[0]}x{size[1]}, metadata removed")
    frames = [("first.jpg", "first_frame")]
    if os.path.exists(last_src):
        with Image.open(last_src) as im:
            im = ImageOps.exif_transpose(im)
            if abs(im.width / im.height - size[0] / size[1]) > 0.02:
                print(f"Warning: last frame's shape ({im.width}x{im.height}) differs from the first; "
                      "it will be cropped to match.", file=sys.stderr)
        prepare(last_src, os.path.join(work, "last.jpg"), size)
        print(f"Last frame:  {size[0]}x{size[1]} (matched to first), metadata removed")
        frames.append(("last.jpg", "last_frame"))
    for fname, role in frames:
        b64 = base64.b64encode(open(os.path.join(work, fname), "rb").read()).decode()
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}, "role": role})
    ratio = "adaptive"                             # required for first/last-frame mode
payload = {
    "model": model,
    "content": content,
    "ratio": ratio,
    "resolution": resolution,
    "duration": int(duration),
    "generate_audio": audio == "true",
    "watermark": False,
}
body = json.dumps(payload)
assert len(body) < 64 * 1024 * 1024, "Request body is over the 64 MB limit"
open(os.path.join(work, "payload.json"), "w").write(body)
print(f"Request body: {len(body):,} bytes")
EOF

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "DRY RUN: POST $BASE"
    python3 - "$WORK/payload.json" <<'EOF'
import json, sys
p = json.load(open(sys.argv[1]))
for item in p["content"]:
    if item["type"] == "image_url":
        u = item["image_url"]["url"]
        item["image_url"]["url"] = u[:40] + f"...<shortened, {len(u):,} chars total>"
print(json.dumps(p, indent=2))
EOF
    echo "No API call made."
    exit 0
  fi
elif [ "$DRY_RUN" -eq 1 ]; then
  echo "--fetch and --dry-run can't be combined." >&2
  exit 2
fi

if [ ! -s "$KEY_FILE" ]; then
  echo "Key file missing or empty: $KEY_FILE" >&2
  exit 1
fi
ARK_API_KEY=$(tr -d '[:space:]' < "$KEY_FILE")
[ -n "$ARK_API_KEY" ] || { echo "Key file contains only whitespace: $KEY_FILE" >&2; exit 1; }
# Feed the auth header to curl as config on stdin so the key never appears in argv / ps output.
ark_curl() {
  printf 'header = "Authorization: Bearer %s"\n' "$ARK_API_KEY" | curl -sS -K - --max-time 120 "$@"
}

if [ -n "$FETCH_ID" ]; then
  TASK_ID="$FETCH_ID"
  NAME="${NAME:-fetched}"
  echo "Fetching existing task $TASK_ID (nothing new submitted)."
else
  echo "Submitting one $RESOLUTION ${DURATION}s job to $MODEL..."
  RESP=$(ark_curl -X POST "$BASE" -H "Content-Type: application/json" --data-binary "@$WORK/payload.json") || true
  TASK_ID=$(printf '%s' "$RESP" | python3 -c 'import sys,json
try: print(json.load(sys.stdin).get("id",""))
except Exception: print("")')
  if [ -z "$TASK_ID" ]; then
    echo "Submit failed (not retried): $RESP" >&2
    exit 1
  fi
  echo "Task ID: $TASK_ID   (if this script stops early: ./seedance_video.sh --fetch $TASK_ID --name $NAME)"
fi

START=$(date +%s)
while true; do
  STATUS_JSON=$(ark_curl "$BASE/$TASK_ID") || { echo "Status check failed; the job is still running. Resume with: --fetch $TASK_ID" >&2; exit 1; }
  STATUS=$(printf '%s' "$STATUS_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("status",""))')
  echo "$(date +%H:%M:%S) status: $STATUS"
  case "$STATUS" in
    succeeded)
      VIDEO_URL=$(printf '%s' "$STATUS_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin)["content"]["video_url"])')
      RES=$(printf '%s' "$STATUS_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("resolution","video"))')
      FILE="output/${NAME}_${RES}_${TASK_ID}.mp4"
      curl -sS --max-time 300 -o "$FILE" "$VIDEO_URL"
      # Keep the task record (with token usage) but drop the signed download link.
      printf '%s' "$STATUS_JSON" | python3 -c 'import sys,json
d=json.load(sys.stdin); d.get("content",{}).pop("video_url",None); print(json.dumps(d,indent=2))' > "${FILE%.mp4}_response.json"
      echo "Saved: $FILE"
      # Also make a small web copy (about 70% smaller, same picture and sound) in compressed/. Use THAT file on the website.
      # Skip with NO_COMPRESS=1. Runs locally with macOS's own video framework (no cost).
      if [ "${NO_COMPRESS:-0}" != "1" ] && [ -f tools/compress_video.swift ] && command -v swift >/dev/null 2>&1; then
        mkdir -p compressed
        CFILE="compressed/${NAME}.mp4"
        if swift tools/compress_video.swift "$FILE" "$CFILE" 1300 96 2>/dev/null | grep -q "^status 2"; then
          echo "Web copy: $CFILE ($(du -h "$CFILE" | cut -f1), original $(du -h "$FILE" | cut -f1))"
        else
          echo "(Could not make the compressed web copy; the original is in $FILE.)" >&2
        fi
      fi
      printf '%s' "$STATUS_JSON" | python3 -c 'import sys,json; print("Tokens used:", json.load(sys.stdin).get("usage",{}).get("total_tokens","?"))'
      [ -x ./token_budget.sh ] && ./token_budget.sh --brief || true
      exit 0 ;;
    failed|cancelled|expired)
      echo "Task ended: $STATUS_JSON" >&2
      exit 1 ;;
  esac
  if [ $(( $(date +%s) - START )) -gt "$MAX_WAIT_SECONDS" ]; then
    echo "Still not done after $MAX_WAIT_SECONDS s. Resume with: ./seedance_video.sh --fetch $TASK_ID --name $NAME" >&2
    exit 1
  fi
  sleep 15
done
