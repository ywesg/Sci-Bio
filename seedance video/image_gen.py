#!/usr/bin/env python3
"""Generate one image with a ModelArk Seedream model and save it in images/.
Usage: ./image_gen.py --prompt-file prompts_img/NAME.txt [--model dola-seedream-5-0-flash-260915] [--size 2304x1536] [--name NAME] [--dry-run]
The key is read from ~/seedance-key.txt (or $SEEDANCE_KEY_FILE) and is never printed. Exactly one image per run, no retries.
The response (with the token/image usage) is saved next to the image as NAME_MODEL_response.json."""
import argparse, base64, json, os, re, sys, time, urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument("--prompt-file", required=True)
ap.add_argument("--model", default="dola-seedream-5-0-flash-260915")
ap.add_argument("--size", default="2304x1536")
ap.add_argument("--name")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
prompt = open(a.prompt_file, encoding="utf-8").read().strip()
name = re.sub(r"[^A-Za-z0-9._-]", "_", a.name or os.path.splitext(os.path.basename(a.prompt_file))[0])
payload = {"model": a.model, "prompt": prompt, "size": a.size, "response_format": "url", "watermark": False}
url = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
if a.dry_run:
    print("DRY RUN: POST", url); print(json.dumps(payload, indent=2)); print("No API call made."); sys.exit(0)
key = open(os.environ.get("SEEDANCE_KEY_FILE", os.path.expanduser("~/seedance-key.txt"))).read().strip()
req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
try:
    with urllib.request.urlopen(req, timeout=300) as r:
        resp = json.load(r)
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:600]); sys.exit(1)
data = resp.get("data") or []
if not data or "url" not in data[0]:
    print("No image returned:", json.dumps(resp)[:600]); sys.exit(1)
os.makedirs("images", exist_ok=True)
stamp = time.strftime("%H%M%S")
base = "images/%s_%s_%s" % (name, a.model.replace("dola-", "").replace("-2", "_2")[:24], stamp)
with urllib.request.urlopen(data[0]["url"], timeout=120) as r, open(base + ".jpg", "wb") as f:
    f.write(r.read())
resp["data"][0].pop("url", None)
json.dump(resp, open(base + "_response.json", "w"), indent=2)
print("Saved:", base + ".jpg")
print("Usage:", json.dumps(resp.get("usage")))
