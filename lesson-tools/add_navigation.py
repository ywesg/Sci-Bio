#!/usr/bin/env python3
"""Adds an 'On this page' contents bar and Previous/Next links to every lesson, in the order the lessons appear in lessons/index.html.
Safe to run again after adding a lesson (add the lesson to index.html first). The styles come from lesson_style.html (already in every page built with lesson_kit).
Index format it reads:   <h2>Chapter name</h2><ul class="lesson-list"><li><a href="file-name.html">1. Lesson title</a></li> ... </ul>"""
import re, glob, html, os

LESSONS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lessons"))
os.chdir(LESSONS)
index = open("index.html", encoding="utf-8").read()
order = []
for m in re.finditer(r"<h2[^>]*>(.*?)</h2>\s*<ul class=\"lesson-list\">(.*?)</ul>", index, re.S):
    chapter = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    for li in re.finditer(r'<li[^>]*><a[^>]*href="([A-Za-z0-9-]+)\.html">(.*?)</a>', m.group(2), re.S):
        inner = re.sub(r'<span class="(s|g3t)">.*?</span>', "", li.group(2), flags=re.S)   # drop the line under the title and the G3 tag
        title = re.sub(r"^\d+(\.\d+)*\.?\s+", "", html.unescape(re.sub(r"<[^>]+>", "", inner))).strip()
        order.append({"file": li.group(1), "title": title, "chapter": chapter})


def slug(t, used):
    s = re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", t)).lower()).strip("-")[:40] or "section"
    base, n = s, 2
    while s in used:
        s = "%s-%d" % (base, n); n += 1
    used.add(s)
    return s


def link(cur, tgt, cls):
    if tgt is None:
        return ""
    label = "Previous" if cls == "prev" else "Next"
    if tgt["chapter"] != cur["chapter"]:
        label += " chapter: " + tgt["chapter"]
    label = ("← " + label) if cls == "prev" else (label + " →")
    return '<a class="%s" href="%s.html"><span class="dir">%s</span><span class="t">%s</span></a>' % (cls, tgt["file"], html.escape(label), html.escape(tgt["title"]))


def process(f):
    name = f[:-5]
    s = o = open(f, encoding="utf-8").read()
    if '<nav class="toc' not in s and "<main>" in s:
        used = set(re.findall(r'id="([^"]+)"', s))
        heads = []

        def addid(m):
            attrs, inner = m.group(1), m.group(2)
            if 'id="' in attrs:
                hid = re.search(r'id="([^"]+)"', attrs).group(1)
            else:
                hid = slug(inner, used); attrs += ' id="%s"' % hid
            heads.append((hid, re.sub(r"<[^>]+>", "", inner).strip()))
            return "<h2%s>%s</h2>" % (attrs, inner)
        i = s.index("<main>")
        s = s[:i] + re.sub(r"<h2([^>]*)>(.*?)</h2>", addid, s[i:], flags=re.S)
        if len(heads) >= 3:
            toc = '<nav class="toc print-hide" aria-label="On this page"><strong>On this page</strong>%s</nav>\n' % "".join('<a href="#%s">%s</a>' % h for h in heads)
            m = re.search(r'<p class="print-hide"><a class="pdf-btn".*?</p>\n?', s, re.S)
            if m:
                s = s[:m.end()] + toc + s[m.end():]
    cur_i = next((i for i, l in enumerate(order) if l["file"] == name), None)
    s = re.sub(r'<nav class="lesson-nav.*?</nav>\n', "", s, flags=re.S)       # rebuilt each run so links follow the index order
    if cur_i is not None:
        cur = order[cur_i]
        links = link(cur, order[cur_i - 1] if cur_i > 0 else None, "prev") + link(cur, order[cur_i + 1] if cur_i + 1 < len(order) else None, "next")
        if links:
            s = s.replace('<p class="back-bottom', '<nav class="lesson-nav print-hide" aria-label="Lesson navigation">%s</nav>\n<p class="back-bottom' % links, 1)
    if s != o:
        open(f, "w", encoding="utf-8").write(s)
    return s != o


changed = [f for f in sorted(glob.glob("*.html")) if f not in ("index.html", "lesson-template.html") and process(f)]
print("lessons updated:", len(changed))
