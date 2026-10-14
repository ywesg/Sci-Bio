#!/bin/bash
# Shows how much of the Seedance token package is used.
#   ./token_budget.sh            full report
#   ./token_budget.sh --brief    one line (the video script prints this after every run)
# Method: baseline_used (from the ModelArk console, see token-budget.json) + the tokens of every video made
# through this folder after the baseline time (read from output/*_response.json).
# It cannot see usage from other computers, so re-check the console now and then and update baseline_used
# and baseline_epoch (or ask Claude to).
cd "$(dirname "$0")"
python3 - "${1:-}" <<'PY'
import json, glob, sys, time
cfg = json.load(open("token-budget.json"))
added, runs = 0, 0
imgs = 0
for f in glob.glob("output/*_response.json"):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if d.get("status") == "succeeded" and d.get("created_at", 0) > cfg["baseline_epoch"]:
        added += d.get("usage", {}).get("total_tokens", 0); runs += 1
for f in glob.glob("images/*_response.json"):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if d.get("created", 0) > cfg["baseline_epoch"]:
        imgs += 1          # images are billed per image, so they are counted here but NOT added to the token package
used = cfg["baseline_used"] + added
limit = cfg["limit"]; left = limit - used; pct = used / limit * 100
flag = ""
for w in sorted(cfg.get("warn_at", []), reverse=True):
    if used >= w * limit:
        flag = "  *** WARNING: %d%% of the package is used. Tell Claude before more videos are made. ***" % round(w * 100); break
if used >= limit: flag = "  *** PACKAGE USED UP ***"
if sys.argv[1] == "--brief":
    print("Token package: %s of %s used (%.1f%%), %s left.%s" % (format(used, ","), format(limit, ","), pct, format(left, ","), flag))
else:
    print("Seedance token package")
    print("  Limit:                     %s" % format(limit, ","))
    print("  Baseline (console):        %s" % format(cfg["baseline_used"], ","))
    print("  Added since baseline:      %s  (%d video%s)" % (format(added, ","), runs, "" if runs == 1 else "s"))
    print("  Used:                      %s  (%.1f%%)" % (format(used, ","), pct))
    print("  Left:                      %s" % format(left, ","))
    print("  Images made since baseline: %d (billed per image, not counted against the token package)" % imgs)
    print("  Rough room for:            ~%d x 6 s 480p drafts (58k each) or ~%d x 6 s 720p (131k each)" % (max(left // 58000, 0), max(left // 131000, 0)))
    if flag: print(flag)
PY
