#!/usr/bin/env python3
"""Writes ai-marking/functions/scheme.json from the revision questions: the server-side marking scheme used by the AI marking function.
Students only ever send {page, qid, answer}; the question and mark scheme come from this file, so the service cannot be used as a general chatbot."""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glob, importlib
T = []
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rev_data_*.py"))):
    T += importlib.import_module(os.path.basename(f)[:-3]).TOPICS

def txt(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h.replace("<br>", " ")))).strip()

out = {}
for t in T:
    for q in t["sb"]:
        out["%s/%s" % (t["file"], q["id"])] = {"topic": txt(t["short"]), "question": txt(q["q"]), "marks": q["marks"], "model": txt(q["model"]), "points": [txt(p["t"]) for p in q["pts"]]}
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ai-marking", "functions", "scheme.json")
json.dump(out, open(dst, "w"), ensure_ascii=False, indent=1)
print("wrote", len(out), "questions to ai-marking/functions/scheme.json")
