#!/usr/bin/env python3
"""Builds lessons/index.html (the home page): the pixel-art banner, the G2/G3 switch, the 'Jump to' chips and one card per lesson.

To publish a new lesson or topic: add it to TOPICS below, then run
    python3 build_index.py && python3 add_navigation.py
Only topics listed here appear on the site, so a topic stays hidden until you add it.
Set g3=True on a topic or a lesson that only G3 classes study: it gets a 'G3 only' tag and is hidden when a student picks G2.
"""
import html, os, random

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "lessons", "index.html")

SITE_TITLE = "Ms Emily's Biology Lessons"
SUBTITLE = "&gt; G2 + G3 SCIENCE (BIOLOGY) // K224 &middot; K225 &middot; K327 &middot; K328"

# (file name without .html, number as in the textbook (or ""), title, line under the title, g3 only?)
TOPICS = [
    dict(id="cells", name="Cell Structure and Organisation", g3=False, lessons=[
        ("cells-1-1-what-are-cells", "1.1", "What Are Cells?", "Syllabus refs (G2 &amp; G3): 1a, 1b, 1c", False),
        ("cells-1-2-cell-adaptations", "1.2", "How Are Cells Adapted to Their Functions?", "Syllabus refs (G2 &amp; G3): 1d", False),
        ("revision-01-cells", "", "Revision Questions", "Section A: multiple choice &middot; Section B: short answer and free response", False),
    ]),
]

# ------------------------------------------------------------------ pixel-art banner (320 x 110 "pixels", drawn as SVG rectangles)
W, H = 320, 110
PAL = {
    "K": "#052e16", "G": "#22c55e", "D": "#15803d", "L": "#bbf7d0", "W": "#ffffff", "B": "#0f172a", "R": "#166534",
    "P": "#f9a8d4", "H": "#fdf2f8", "N": "#7c3aed", "O": "#ddd6fe", "M": "#fb923c", "Q": "#9d174d",
    "Y": "#fde047", "V": "#c084fc", "C": "#fef3c7", "S": "#ef4444", "T": "#a16207",
}
FROG = ["...KKK....KKK...",
        "..KWWBK..KWWBK..",
        "..KWBBK..KWBBK..",
        ".KGGGGGGGGGGGGK.",
        "KGGGGGGGGGGGGGGK",
        "KGGRRRRRRRRRRGGK",
        "KGGGGGGGGGGGGGGK",
        ".KGGLLLLLLLLGGK.",
        "KGGKLLLLLLLLKGGK",
        "KGGKGLLLLLLGKGGK",
        "KDDGKGGGGGGKGDDK",
        ".KKK.KKKKKK.KKK."]
CELL = [".....QQQQQQ.....",
        "...QQPPPPPPQQ...",
        "..QPHHPPPPPPPQ..",
        ".QPHPPPPPPNNPPQ.",
        ".QPPPPPPPNNONPQ.",
        "QPPWBPPWBPNNNPPQ",
        "QPPWBPPWBPPPPPPQ",
        "QPPPPPPPPPPPMPPQ",
        "QPPPSPPSPPPMMPPQ",
        ".QPPPSSPPPPPPPQ.",
        ".QPPPPPPPPPPPPQ.",
        "..QQPPPPPPPPQQ..",
        "....QQQQQQQQ...."]
BUTTERFLY = ["VV.K.VV",
             "VYVKVYV",
             ".VVKVV.",
             "VVVKVVV",
             ".V...V."]
MUSHROOM = ["..SSSS..",
            ".SSWSSS.",
            "SSSSSWSS",
            "SWSSSSSS",
            "..CCCC..",
            "..CCCC..",
            ".CCCCCC."]


def sprite(rows, x0, y0, pal=PAL):
    """Draws an ASCII sprite, merging runs of the same colour on each row."""
    out = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            c = row[x]
            if c == ".":
                x += 1
                continue
            n = 1
            while x + n < len(row) and row[x + n] == c:
                n += 1
            out.append('<rect x="%d" y="%d" width="%d" height="1" fill="%s"/>' % (x0 + x, y0 + y, n, pal[c]))
            x += n
    return "".join(out)


def ridge(seed, base, amp, step, smooth):
    """A stepped hill outline: a list of heights, one per `step` columns."""
    r = random.Random(seed)
    h, vals, v = base, [], 0
    for _ in range(W // step + 2):
        v = v * smooth + r.uniform(-amp, amp)
        h = max(base - 3 * amp, min(base + 3 * amp, h + v))
        vals.append(round(h))
    return vals


def hill(vals, step, fill, edge=None):
    d = "M0 %d" % H
    for i, y in enumerate(vals):
        d += " V%d H%d" % (y, (i + 1) * step)
    d += " V%d Z" % H
    s = ""
    if edge:
        s += '<path d="%s" fill="%s"/>' % (d, edge)
        d2 = "M0 %d" % H
        for i, y in enumerate(vals):
            d2 += " V%d H%d" % (y + 2, (i + 1) * step)
        d2 += " V%d Z" % H
        s += '<path d="%s" fill="%s"/>' % (d2, fill)
    else:
        s += '<path d="%s" fill="%s"/>' % (d, fill)
    return s


def disc(cx, cy, r, fill, opacity=1):
    s = ""
    for y in range(-r, r + 1):
        w = int((r * r - y * y) ** 0.5 + 0.35)
        s += '<rect x="%d" y="%d" width="%d" height="1" fill="%s"%s/>' % (cx - w, cy + y, 2 * w + 1, fill, "" if opacity == 1 else ' opacity="%s"' % opacity)
    return s


def dome(cx, base, r):
    """A glass biodome with plants inside."""
    s = ""
    for y in range(0, r + 1):
        w = int((r * r - y * y) ** 0.5 + 0.35)
        s += '<rect x="%d" y="%d" width="%d" height="1" fill="#a5f3fc" opacity="0.55"/>' % (cx - w, base - y, 2 * w + 1)
    for y in range(0, r + 1, 4):                       # pane lines
        w = int((r * r - y * y) ** 0.5 + 0.35)
        s += '<rect x="%d" y="%d" width="%d" height="1" fill="#e0f2fe"/>' % (cx - w, base - y, 2 * w + 1)
    for x in range(-r + 4, r, 5):
        hgt = int((r * r - x * x) ** 0.5)
        s += '<rect x="%d" y="%d" width="1" height="%d" fill="#e0f2fe" opacity="0.8"/>' % (cx + x, base - hgt, hgt)
    for i, x in enumerate(range(cx - r + 3, cx + r - 2, 3)):   # plants inside
        hh = 3 + (i * 7) % 6
        s += '<rect x="%d" y="%d" width="2" height="%d" fill="%s"/>' % (x, base - hh, hh, "#16a34a" if i % 2 else "#4ade80")
    s += '<rect x="%d" y="%d" width="%d" height="2" fill="#94a3b8"/>' % (cx - r - 1, base + 1, 2 * r + 3)
    return s


def tree(x, base, h, seed):
    r = random.Random(seed)
    s = '<rect x="%d" y="%d" width="3" height="%d" fill="#3f2a1d"/>' % (x, base - h, h)
    for i in range(5):
        cx, cy, rr = x + 1 + r.randint(-5, 5), base - h + r.randint(-3, 5), r.randint(4, 7)
        s += disc(cx, cy, rr, "#14532d" if i % 2 else "#166534")
    s += disc(x - 1, base - h - 1, 3, "#22c55e", 0.55)
    return s


def banner():
    s = ['<svg class="scene" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMax slice" shape-rendering="crispEdges" aria-hidden="true" focusable="false">' % (W, H)]
    bands = ["#1e1048", "#2e1065", "#4c1d95", "#6b21a8", "#86198f", "#a21caf", "#c026d3", "#db2777", "#f472b6", "#f9a8d4", "#fbcfe8", "#d9f99d"]
    for i, c in enumerate(bands):                      # sky in pixel bands, with a dotted edge like old games
        y = int(i * 62 / len(bands))
        s.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y, W, 62 - y + 2, c))
        if i:
            s.append('<path d="%s" fill="%s"/>' % ("".join("M%d %dh1v1h-1z" % (x, y - 1) for x in range(i % 2, W, 2)), c))
    r = random.Random(7)
    for _ in range(45):                                # stars (some twinkle)
        x, y = r.randint(0, W - 1), r.randint(0, 26)
        s.append('<rect class="%s" x="%d" y="%d" width="1" height="1" fill="#fff"/>' % ("tw" if r.random() < 0.35 else "", x, y))
    s.append(disc(262, 56, 17, "#fef9c3", 0.18))       # setting sun with halo rings
    s.append(disc(262, 56, 12, "#fef9c3", 0.35))
    s.append(disc(262, 56, 8, "#fefce8"))
    s.append(hill(ridge(3, 58, 1.2, 4, 0.6), 4, "#115e59", "#2dd4bf"))
    s.append(tree(30, 72, 20, 1) + tree(60, 76, 14, 2) + tree(205, 74, 17, 3) + tree(300, 74, 22, 4))
    s.append(hill(ridge(11, 72, 1.1, 3, 0.5), 3, "#15803d", "#4ade80"))
    s.append(dome(276, 80, 15))
    s.append(hill(ridge(23, 84, 0.8, 4, 0.4), 4, "#166534", "#86efac"))
    s.append(hill(ridge(41, 96, 0.5, 5, 0.3), 5, "#14532d", "#4ade80"))
    for x in range(3, W, 11):                          # grass tufts
        s.append('<rect x="%d" y="%d" width="1" height="2" fill="#86efac"/><rect x="%d" y="%d" width="1" height="3" fill="#4ade80"/>' % (x, 99 + x % 3, x + 2, 98 + x % 3))
    s.append('<g class="mush">%s%s</g>' % (sprite(MUSHROOM, 104, 91), sprite([r_.replace("S", "Y") for r_ in MUSHROOM], 113, 93)))
    s.append('<rect class="shadow" x="128" y="103" width="18" height="1" fill="#052e16" opacity="0.45"/>')
    s.append('<g class="frog">%s</g>' % sprite(FROG, 129, 91))
    s.append('<rect class="shadow" x="164" y="103" width="18" height="1" fill="#052e16" opacity="0.45"/>')
    s.append('<g class="blob">%s</g>' % sprite(CELL, 165, 90))
    s.append('<g class="fly f1">%s</g><g class="fly f2">%s</g>' % (sprite(BUTTERFLY, 100, 64), sprite([r_.replace("V", "M") for r_ in BUTTERFLY], 222, 58)))
    for i, (x, y) in enumerate([(40, 86), (88, 80), (196, 88), (240, 84), (150, 78), (310, 90)]):
        s.append('<rect class="ff ff%d" x="%d" y="%d" width="1" height="1" fill="#fef08a"/>' % (i % 3, x, y))
    s.append("</svg>")
    return "".join(s)


CSS = r"""
:root { --ink: #1f2937; --deep: #134e4a; --teal: #0f766e; --pink: #db2777; --line: #cbd5e1; --cream: #fffdf7; --card: #f7fbfa; --muted: #475569; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--cream); color: var(--ink); font-family: "Source Sans 3", system-ui, sans-serif; line-height: 1.55; }
a { color: inherit; }
.hero { position: relative; height: clamp(300px, 42vw, 440px); overflow: hidden; background: #2e1065; border-bottom: 5px solid #2dd4bf; }
.hero .scene { position: absolute; inset: 0; width: 100%; height: 100%; }
.hero .titles { position: absolute; left: 0; right: 0; top: clamp(0.8rem, 3vw, 2rem); text-align: center; padding: 0 1rem; z-index: 2; }
.hero h1 { margin: 0; font-family: "Silkscreen", "Press Start 2P", monospace; font-weight: 700; line-height: 0.95; color: #d9f99d; letter-spacing: 0.03em;
  text-shadow: 0.06em 0.06em 0 #db2777, 0 0 0.35em rgba(74, 222, 128, 0.75); }
.hero h1 .small { display: block; font-size: clamp(1.3rem, 3.6vw, 2.6rem); color: #a5f3fc; text-shadow: 0.07em 0.07em 0 #7e22ce, 0 0 0.35em rgba(34, 211, 238, 0.7); margin-bottom: 0.15em; }
.hero h1 .big { display: block; font-size: clamp(2.1rem, 7.2vw, 5.4rem); }
.hero .sub { display: inline-block; margin: 0.9rem 0 0; padding: 0.25rem 0.8rem; background: rgba(46, 16, 101, 0.62); border-radius: 4px; font-family: "Space Mono", ui-monospace, monospace; font-weight: 700; color: #cffafe; letter-spacing: 0.14em; font-size: clamp(0.7rem, 1.6vw, 1.05rem); text-shadow: 0 1px 0 #3b0764; }
.tw { animation: tw 2.6s steps(2) infinite; }
.ff { animation: ff 3s ease-in-out infinite; } .ff1 { animation-delay: -1s; } .ff2 { animation-delay: -2s; }
.fly { animation: fly 1.2s steps(2) infinite; } .f2 { animation-delay: -0.6s; }
@keyframes tw { 50% { opacity: 0.15; } }
@keyframes ff { 0%, 100% { opacity: 0.1; transform: translateY(0); } 50% { opacity: 1; transform: translateY(-3px); } }
@keyframes fly { 50% { transform: translateY(-2px); } }
/* intro: the frog hops in from the left, the cell rolls in from the right, then the title switches on */
.play .frog { animation: hopin 2.2s steps(22) both; }
.play .blob { animation: rollin 2.2s steps(22) both, bob 1.6s steps(2) 2.2s infinite; }
.play .titles { animation: flick 1.4s steps(1) 0.4s both; }
.blob { animation: bob 1.6s steps(2) infinite; }
@keyframes hopin { 0% { transform: translate(-150px, 0); } 10% { transform: translate(-135px, -6px); } 20% { transform: translate(-120px, 0); } 30% { transform: translate(-100px, -7px); } 40% { transform: translate(-80px, 0); }
  50% { transform: translate(-62px, -6px); } 60% { transform: translate(-44px, 0); } 70% { transform: translate(-28px, -5px); } 80% { transform: translate(-12px, 0); } 90% { transform: translate(-4px, -3px); } 100% { transform: translate(0, 0); } }
@keyframes rollin { 0% { transform: translateX(170px); } 100% { transform: translateX(0); } }
@keyframes bob { 50% { transform: translateY(-1px); } }
@keyframes flick { 0% { opacity: 0; } 15% { opacity: 1; } 25% { opacity: 0.2; } 35% { opacity: 1; } 45% { opacity: 0.4; } 55%, 100% { opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .tw, .ff, .fly, .blob, .play .frog, .play .blob, .play .titles { animation: none !important; } }

main { max-width: 960px; margin: 0 auto; padding: 1.6rem 1rem 3rem; }
.mono { font-family: "Space Mono", ui-monospace, monospace; font-size: 0.85rem; color: var(--muted); }
.intro-row { display: flex; flex-wrap: wrap; align-items: center; gap: 0.6rem 1.2rem; }
.btn-ghost { min-height: 2.75rem; padding: 0 1.1rem; border: 1px solid #64748b; border-radius: 999px; background: #fff; color: var(--deep); font: 600 1rem "Chakra Petch", system-ui, sans-serif; cursor: pointer; }
.btn-ghost:hover { background: #f0fdfa; border-color: var(--teal); }
.level { display: flex; flex-wrap: wrap; align-items: center; gap: 0.6rem; margin: 1.6rem 0 0.4rem; }
.level button { min-height: 3.2rem; padding: 0 1.4rem; border-radius: 999px; border: 1px solid #94a3b8; background: #fff; color: var(--deep); font: 700 1.1rem "Chakra Petch", system-ui, sans-serif; cursor: pointer; }
.level button[aria-pressed="true"] { background: var(--deep); border-color: var(--deep); color: #fff; }
.jump { display: flex; flex-wrap: wrap; align-items: center; gap: 0.6rem; margin: 1rem 0 0.5rem; }
.jump a { display: inline-block; padding: 0.65rem 1.1rem; border: 1px solid var(--line); border-radius: 999px; background: #fff; color: var(--deep); text-decoration: none; font: 600 1rem "Chakra Petch", system-ui, sans-serif; }
.jump a:hover, .level button:hover { border-color: var(--teal); background: #f0fdfa; }
.level button[aria-pressed="true"]:hover { background: #115e59; }
.topic { margin-top: 2.6rem; scroll-margin-top: 1rem; }
.topic h2 { margin: 0 0 1.2rem; padding-left: 0.9rem; border-left: 7px solid var(--pink); color: var(--deep); font: 700 clamp(1.5rem, 3.4vw, 2rem)/1.15 "Rajdhani", system-ui, sans-serif; text-transform: uppercase; letter-spacing: 0.06em; }
.lesson-list { list-style: none; padding: 0; margin: 0; }
.lesson-list li { margin: 0 0 1.1rem; }
.lesson-list a.card { display: block; padding: 1rem 1.6rem; border: 1px solid #dbe4ee; border-left: 6px solid #2dd4bf; border-radius: 10px; background: var(--card); text-decoration: none; transition: background 0.15s, transform 0.15s; }
.lesson-list a.card:hover { background: #ecfdf5; transform: translateX(3px); }
.card .t { display: block; color: var(--deep); font: 700 1.2rem/1.3 "Chakra Petch", system-ui, sans-serif; }
.card .s { display: block; color: var(--muted); margin-top: 0.2rem; }
.g3t { display: inline-block; margin-left: 0.5rem; padding: 0.1rem 0.6rem; border-radius: 999px; background: linear-gradient(135deg, #c2185b, #c2410c); color: #fff; font: 800 0.75rem system-ui, sans-serif; vertical-align: middle; }
a.pdf { display: inline-flex; align-items: center; gap: 0.4rem; margin: 0.45rem 0 0 0.6rem; color: #1d4ed8; font-weight: 700; font-size: 0.95rem; text-decoration: none; }
a.pdf:hover { text-decoration: underline; }
a.pdf::before { content: ""; width: 12px; height: 15px; background: linear-gradient(#e2e8f0, #cbd5e1); border-radius: 2px; box-shadow: inset 0 -3px 0 #94a3b8; }
body[data-level="g2"] .g3-only { display: none !important; }
.g2-note { display: none; }
body[data-level="g2"] .g2-note { display: block; }
footer { max-width: 960px; margin: 0 auto; padding: 1.5rem 1rem 2.5rem; border-top: 1px solid var(--line); }
:focus-visible { outline: 3px solid var(--teal); outline-offset: 2px; }
@media (max-width: 560px) { .lesson-list a.card { padding: 0.9rem 1rem; } .level button { padding: 0 1rem; font-size: 1rem; } }
"""

JS = r"""
(function () {
  var KEY = 'bio-level', body = document.body;
  function set(level) {
    body.dataset.level = level;
    document.querySelectorAll('.level button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.level === level ? 'true' : 'false'); });
    try { localStorage.setItem(KEY, level); } catch (e) {}
  }
  var saved = 'g3';
  try { saved = localStorage.getItem(KEY) || 'g3'; } catch (e) {}
  set(saved);
  document.querySelectorAll('.level button').forEach(function (b) { b.addEventListener('click', function () { set(b.dataset.level); }); });
  var hero = document.querySelector('.hero');
  document.getElementById('replay').addEventListener('click', function () { hero.classList.remove('play'); void hero.offsetWidth; hero.classList.add('play'); });
})();
"""


def build():
    e = html.escape
    jump = "".join('<a href="#%s"%s>%s</a>' % (t["id"], ' class="g3-only"' if t["g3"] else "", e(t["name"])) for t in TOPICS)
    secs = ""
    for t in TOPICS:
        tag = ' <span class="g3t">G3 only</span>' if t["g3"] else ""
        secs += '<section class="topic%s" id="%s">\n<h2>%s%s</h2>\n<ul class="lesson-list">\n' % (" g3-only" if t["g3"] else "", t["id"], e(t["name"]), tag)
        for f, num, title, sub, g3 in t["lessons"]:
            g = g3 or t["g3"]
            secs += ('  <li%s><a class="card" href="%s.html"><span class="t">%s%s%s</span><span class="s">%s</span></a>'
                     '<a class="pdf" href="%s.pdf" target="_blank" rel="noopener">Printable version (PDF)</a></li>\n'
                     % (' class="g3-only"' if g3 else "", f, num + " " if num else "", e(title), ' <span class="g3t">G3 only</span>' if g else "", sub, f))
        secs += "</ul>\n</section>\n"
    page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>%(title)s</title>
<meta name="description" content="Interactive Biology lesson notes for G2 and G3 SEC Science (Biology), with printable PDFs and revision questions.">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' shape-rendering='crispEdges'%%3E%%3Crect x='3' y='2' width='10' height='12' fill='%%23f9a8d4'/%%3E%%3Crect x='2' y='4' width='12' height='8' fill='%%23f9a8d4'/%%3E%%3Crect x='8' y='5' width='4' height='4' fill='%%237c3aed'/%%3E%%3C/svg%%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Silkscreen:wght@400;700&family=Space+Mono:wght@400;700&family=Rajdhani:wght@600;700&family=Chakra+Petch:wght@500;600;700&family=Source+Sans+3:wght@400;600;700&display=swap">
<style>%(css)s</style>
</head>
<body data-level="g3">
<header class="hero play">
%(svg)s
<div class="titles"><h1><span class="small">Ms Emily's</span><span class="big">Biology Lessons</span></h1><p class="sub">%(subtitle)s</p></div>
</header>
<main>
<div class="intro-row"><button type="button" class="btn-ghost" id="replay">&#9654; Replay intro</button>
<span class="mono">Biology &middot; Lesson notes &middot; Every lesson has a printable PDF: use the link under each lesson, or the button at the top of the lesson page.</span></div>
<div class="level" role="group" aria-label="Choose your course"><span class="mono">I am studying</span>
<button type="button" data-level="g3" aria-pressed="true">G3: all lessons</button>
<button type="button" data-level="g2" aria-pressed="false">G2: hide G3-only lessons</button></div>
<p class="mono g2-note">G2 view: lessons and topics marked &ldquo;G3 only&rdquo; are hidden.</p>
<nav class="jump" aria-label="Topics"><span class="mono">Jump to</span>%(jump)s</nav>
%(secs)s</main>
<footer><p class="mono">%(title)s &middot; Follows the 2027 SEC G2 and G3 Science (Biology) syllabuses. New topics appear here as they are released.</p></footer>
<script>%(js)s</script>
</body>
</html>
""" % dict(title=SITE_TITLE, css=CSS, svg=banner(), subtitle=SUBTITLE, jump=jump, secs=secs, js=JS)
    open(OUT, "w", encoding="utf-8").write(page)
    print("wrote lessons/index.html (%d topics, %d KB)" % (len(TOPICS), len(page) // 1024))


if __name__ == "__main__":
    build()
