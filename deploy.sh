#!/bin/bash
# Deploys everything in lessons/ to the lessons Netlify site.
#
# Uploads a whole folder (HTML lessons plus any videos/images next to them).
#
# One-time setup:
#   1. Save your Netlify Personal Access Token OUTSIDE OneDrive (this folder syncs to the cloud):
#        pbpaste > ~/.netlify_token && chmod 600 ~/.netlify_token
#   2. Put the site's name or ID in netlify-site.txt next to this script (not a secret), e.g.
#        echo "my-subject-lessons.netlify.app" > netlify-site.txt
#
# Every time after that:
#   ./deploy.sh            # deploy
#   ./deploy.sh --dry-run  # list what would be uploaded, call nothing

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$DIR/lessons"
SITE_FILE="$DIR/netlify-site.txt"
TOKEN_FILE="${NETLIFY_TOKEN_FILE:-$HOME/.netlify_token}"
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

[ -d "$SRC_DIR" ] || { echo "Error: $SRC_DIR not found." >&2; exit 1; }
[ -f "$SRC_DIR/index.html" ] || { echo "Error: lessons/index.html is missing (it is the site's home page)." >&2; exit 1; }
[ -f "$SITE_FILE" ] || { echo "Error: $SITE_FILE not found. Put the Netlify site name or ID in it." >&2; exit 1; }
SITE_ID="$(tr -d '[:space:]' < "$SITE_FILE")"

# Files to publish. Skips hidden files and the blank starter template.
FILES=()
while IFS= read -r f; do FILES+=("$f"); done < <(
  cd "$SRC_DIR" && find . -type f ! -name '.*' ! -name 'lesson-template.html' | sed 's|^\./||' | sort
)

# Build {"/path": "sha1", ...} and a sha1<TAB>path map.
MANIFEST='{}'
MAP_FILE="$(mktemp)"
trap 'rm -f "$MAP_FILE"' EXIT
for f in "${FILES[@]}"; do
  sha="$(shasum "$SRC_DIR/$f" | awk '{print $1}')"
  MANIFEST="$(jq -c --arg p "/$f" --arg s "$sha" '. + {($p): $s}' <<<"$MANIFEST")"
  printf '%s\t%s\n' "$sha" "$f" >> "$MAP_FILE"
done

echo "Site: $SITE_ID"
echo "Files (${#FILES[@]}):"
printf '  %s\n' "${FILES[@]}"

if [ "$DRY_RUN" = 1 ]; then
  echo "DRY RUN: no API call made."
  exit 0
fi

if [ -n "${NETLIFY_AUTH_TOKEN:-}" ]; then
  TOKEN="$NETLIFY_AUTH_TOKEN"
elif [ -f "$TOKEN_FILE" ]; then
  TOKEN="$(tr -d '[:space:]' < "$TOKEN_FILE")"
else
  echo "Error: no Netlify token. Set NETLIFY_AUTH_TOKEN or create $TOKEN_FILE." >&2
  echo "Get one at: https://app.netlify.com/user/applications#personal-access-tokens" >&2
  exit 1
fi

# If the Netlify command-line tool is installed (outside OneDrive, in ~/.local/netlify-cli) and the AI marking function exists, deploy the
# pages AND the function together. The plain API deploy below cannot include functions and would DELETE the marking service.
CLI="$HOME/.local/netlify-cli/node_modules/.bin/netlify"
NODE_BIN="$(ls -d "$HOME"/.local/node-v22*/bin 2>/dev/null | head -1)"
if [ -x "$CLI" ] && [ -d "$DIR/ai-marking/functions" ]; then
  echo "Deploying pages and the AI marking function with the Netlify CLI..."
  command -v python3 >/dev/null 2>&1 && python3 "$DIR/lesson-tools/build_ai_scheme.py" || true
  STAGE="$(mktemp -d)"
  rsync -a --exclude 'lesson-template.html' --exclude '.*' --exclude '*_t.html' "$SRC_DIR/" "$STAGE/"
  # Deploy as a draft, then promote it to production through the API. (A direct `--prod` deploy is refused with "Forbidden" while a Netlify account is frozen
  # for running out of credits; promoting a draft was our workaround. It works normally too.)
  OUT="$(PATH="$NODE_BIN:$PATH" NETLIFY_AUTH_TOKEN="$TOKEN" "$CLI" deploy --dir "$STAGE" --functions "$DIR/ai-marking/functions" --site "$SITE_ID" --message "deploy.sh" --json 2>&1 || true)"
  DID="$(printf '%s' "$OUT" | jq -r '.deploy_id // empty' 2>/dev/null || true)"
  if [ -z "$DID" ]; then echo "Deploy failed:" >&2; printf '%s\n' "$OUT" | tail -5 >&2; rm -rf "$STAGE"; exit 1; fi
  CODE="$(curl -s -o /dev/null -w '%{http_code}' -X POST -H "Authorization: Bearer $TOKEN" "https://api.netlify.com/api/v1/sites/$SITE_ID/deploys/$DID/restore")"
  if [ "$CODE" != "200" ]; then echo "Could not publish deploy $DID (HTTP $CODE)." >&2; rm -rf "$STAGE"; exit 1; fi
  rm -rf "$STAGE"
  case "$SITE_ID" in *.*) echo "Live at: https://${SITE_ID#https://}" ;; *) echo "Live at: https://$SITE_ID.netlify.app (if the site name differs, check the Netlify dashboard)" ;; esac
  exit 0
fi
echo "WARNING: Netlify CLI not found, so only the pages are deployed. If the AI marking function is live, this deploy REMOVES it." >&2

# Digest-based deploy: send paths + sha1s, then upload only what Netlify says it needs.
RESPONSE="$(curl -s -w '\n%{http_code}' -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d "{\"files\":$MANIFEST}" \
  "https://api.netlify.com/api/v1/sites/$SITE_ID/deploys")"
HTTP_CODE="$(tail -n1 <<<"$RESPONSE")"
BODY="$(sed '$d' <<<"$RESPONSE")"
if [ "$HTTP_CODE" != "200" ] && [ "$HTTP_CODE" != "201" ]; then
  echo "Deploy creation failed (HTTP $HTTP_CODE):" >&2
  echo "$BODY" >&2
  exit 1
fi

DEPLOY_ID="$(jq -r '.id' <<<"$BODY")"
REQUIRED="$(jq -r '.required[]?' <<<"$BODY")"
UPLOADED=0
for sha in $REQUIRED; do
  # The same content can sit at several paths; upload each one.
  while IFS=$'\t' read -r _ path; do
    code="$(curl -s -o /dev/null -w '%{http_code}' -X PUT \
      -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/octet-stream" \
      --data-binary "@$SRC_DIR/$path" \
      "https://api.netlify.com/api/v1/deploys/$DEPLOY_ID/files/$(jq -rn --arg p "$path" '$p|@uri' | sed 's/%2F/\//g')")"
    if [ "$code" != "200" ] && [ "$code" != "201" ]; then
      echo "Upload failed for $path (HTTP $code)." >&2
      exit 1
    fi
    UPLOADED=$((UPLOADED + 1))
  done < <(awk -F'\t' -v s="$sha" '$1==s' "$MAP_FILE")
done

echo "Uploaded $UPLOADED file(s) (unchanged files were skipped)."
echo "Live at: $(jq -r '.ssl_url // .url' <<<"$BODY")"
