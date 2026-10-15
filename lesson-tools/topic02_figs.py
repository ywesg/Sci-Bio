"""SVG drawings for Topic 2 (Movement of Substances). Used by build_topic02.py.
Our own drawings in the site style (not copied from the textbook). Each function returns an <svg> string;
functions with labels=False return the drawing only, for the drag-and-drop labeller (see the *_TARGETS lists)."""
import random

FONT = 'font-family="Source Sans 3, system-ui, sans-serif" font-size="15" fill="#1f2937"'
SMALL = 'font-family="Source Sans 3, system-ui, sans-serif" font-size="13" fill="#334155"'
HALO = 'paint-order="stroke" stroke="#fff" stroke-width="4" stroke-linejoin="round"'
LINE = "#3f3f46"
WATER = "#dbeafe"
BLUE = "#2563eb"     # copper(II) sulfate particles / water molecules
YELLOW = "#eab308"   # potassium nitrate particles
ORANGE = "#f97316"   # sucrose molecules
CYTO = "#fbf3c6"
WALL = "#a16207"

ARROW_DEFS = ('<defs><marker id="%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
              '<path d="M0 0L10 5L0 10z" fill="%s"/></marker></defs>')


def svg(vw, vh, body, label, w=None):
    st = ' style="max-width:%dpx"' % w if w else ""
    return '<svg viewBox="0 0 %d %d" role="img" aria-label="%s"%s>%s</svg>' % (vw, vh, label, st, body)


def lbl(text, tx, ty, x2, y2, anchor="end"):
    """A label with a leader line from the text to the point (x2, y2)."""
    x1 = tx + (6 if anchor == "end" else -6)
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#334155" stroke-width="1.3"/><circle cx="%d" cy="%d" r="2.3" fill="#334155"/>'
            '<text x="%d" y="%d" text-anchor="%s" %s>%s</text>' % (x1, ty - 5, x2, y2, x2, y2, tx, ty, anchor, FONT, text))


def text(x, y, t, anchor="middle", attrs=FONT, weight=""):
    w = ' font-weight="700"' if weight else ""
    lines = t.split("\n")
    if len(lines) == 1:
        return '<text x="%s" y="%s" text-anchor="%s" %s%s>%s</text>' % (x, y, anchor, attrs, w, t)
    return ('<text x="%s" y="%s" text-anchor="%s" %s%s>' % (x, y, anchor, attrs, w)
            + "".join('<tspan x="%s" dy="%s">%s</tspan>' % (x, 0 if i == 0 else "1.15em", l) for i, l in enumerate(lines)) + "</text>")


def arrow(x1, y1, x2, y2, mid, colour="#be185d", w=3):
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" marker-end="url(#%s)"/>' % (x1, y1, x2, y2, colour, w, mid)


def dots(rng, n, x0, x1, y0, y1, r, fill, stroke="none"):
    return "".join('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s"/>' % (rng.uniform(x0, x1), rng.uniform(y0, y1), r, fill, stroke) for _ in range(n))


# ================================================================== 2.1 Diffusion
def perfume():
    """Perfume particles spreading through a room: crowded near the bottle, fewer far away."""
    rng = random.Random(21)
    b = ARROW_DEFS % ("ap", "#be185d")
    b += '<rect x="10" y="10" width="620" height="230" rx="6" fill="#fffbeb" stroke="%s" stroke-width="2"/>' % LINE
    b += '<rect x="30" y="170" width="130" height="10" fill="#a16207"/><rect x="40" y="180" width="8" height="58" fill="#a16207"/><rect x="142" y="180" width="8" height="58" fill="#a16207"/>'
    b += '<rect x="78" y="128" width="34" height="42" rx="6" fill="#fbcfe8" stroke="#9d174d" stroke-width="2"/><rect x="88" y="116" width="14" height="13" fill="#9d174d"/>'
    # particles: density falls with distance from the bottle
    pts = ""
    for _ in range(170):
        x = 95 + abs(rng.gauss(0, 150))
        y = rng.uniform(25, 225)
        if x < 615 and not (25 < x < 165 and y > 112):
            pts += '<circle cx="%.0f" cy="%.0f" r="3.2" fill="#db2777" opacity="0.85"/>' % (x, y)
    b += pts
    # person sniffing
    b += '<circle cx="560" cy="120" r="24" fill="#fde68a" stroke="%s" stroke-width="2"/><path d="M536 122 l-9 6 l9 3" fill="#fde68a" stroke="%s" stroke-width="2"/>' % (LINE, LINE)
    b += '<path d="M520 240 q40 -80 80 0" fill="#93c5fd" stroke="%s" stroke-width="2"/>' % LINE
    b += arrow(200, 45, 470, 45, "ap")
    b += text(335, 36, "net movement of perfume particles", attrs=SMALL + " " + HALO)
    b += text(95, 100, "higher\nconcentration", attrs=SMALL + " " + HALO, weight=1)
    b += text(440, 222, "lower concentration", attrs=SMALL + " " + HALO, weight=1)
    return svg(640, 250, b, "Perfume particles spread from a bottle, where they are crowded, across the room to a person far away", 640)


def gas_jar(stage, x=0):
    """One gas jar of water with a copper(II) sulfate crystal. stage 0: just dropped in, 1: after a day, 2: after a few days."""
    gid = "cu%d" % stage
    stops = {0: [(0, 0), (0.80, 0), (0.93, 0.25), (1, 0.8)],
             1: [(0, 0.02), (0.35, 0.08), (0.75, 0.35), (1, 0.7)],
             2: [(0, 0.32), (1, 0.36)]}[stage]
    g = ('<defs><linearGradient id="%s" x1="0" y1="0" x2="0" y2="1">' % gid
         + "".join('<stop offset="%s" stop-color="#1d4ed8" stop-opacity="%s"/>' % s for s in stops) + '</linearGradient></defs>')
    b = g + '<g transform="translate(%s 0)">' % x
    b += '<rect x="30" y="50" width="110" height="200" fill="%s"/><rect x="30" y="50" width="110" height="200" fill="url(#%s)"/>' % (WATER, gid)
    b += '<path d="M24 28 V250 q0 8 8 8 H138 q8 0 8 -8 V28" fill="none" stroke="%s" stroke-width="3"/>' % LINE
    b += '<rect x="18" y="20" width="134" height="8" rx="2" fill="#cbd5e1" stroke="%s" stroke-width="1.5"/>' % LINE   # cover
    b += '<rect x="10" y="258" width="150" height="8" rx="2" fill="#f59e0b"/>'
    if stage < 2:
        s = 12 if stage == 0 else 7
        b += '<path d="M%s 250 l%s -%s l%s %s z" fill="#1d4ed8" stroke="#1e3a8a" stroke-width="1"/>' % (85 - s, s, s * 1.6, s, s * 1.6)
    b += '</g>'
    return b


def gas_jars():
    b = ""
    caps = ["Day 0: crystal dropped in", "After 1 day", "After a few days"]
    for i in range(3):
        b += gas_jar(i, 10 + i * 200)
        b += text(95 + i * 200, 292, caps[i], weight=1)
    return svg(610, 305, b, "Three gas jars of water. On day 0 a blue copper(II) sulfate crystal sits at the bottom. After one day the blue colour has spread upwards, darkest at the bottom. After a few days the whole jar is evenly pale blue", 610)


def membrane_beakers():
    """Two solutes diffusing in opposite directions through a permeable membrane (before and after)."""
    rng = random.Random(23)
    b = ARROW_DEFS % ("am", "#334155") + ARROW_DEFS % ("ay", "#ca8a04") + ARROW_DEFS % ("ab", BLUE)

    def beaker(x, before):
        h = '<g transform="translate(%d 0)">' % x
        h += '<rect x="20" y="60" width="240" height="190" fill="%s"/>' % WATER
        h += '<path d="M14 40 V246 q0 10 10 10 H256 q10 0 10 -10 V40" fill="none" stroke="%s" stroke-width="3"/>' % LINE
        h += '<line x1="140" y1="30" x2="140" y2="252" stroke="#475569" stroke-width="2.5" stroke-dasharray="9 6"/>'
        if before:
            h += dots(rng, 26, 30, 130, 70, 242, 5, YELLOW, "#a16207") + dots(rng, 26, 150, 250, 70, 242, 5, "#3b82f6", "#1e40af")
            for y in (95, 175):
                h += arrow(60, y, 205, y, "ay", "#ca8a04")
            for y in (135, 215):
                h += arrow(220, y, 75, y, "ab", BLUE)
        else:
            h += dots(rng, 13, 30, 130, 70, 242, 5, YELLOW, "#a16207") + dots(rng, 13, 150, 250, 70, 242, 5, YELLOW, "#a16207")
            h += dots(rng, 13, 30, 130, 70, 242, 5, "#3b82f6", "#1e40af") + dots(rng, 13, 150, 250, 70, 242, 5, "#3b82f6", "#1e40af")
        return h + "</g>"

    b += beaker(10, True) + beaker(400, False)
    b += arrow(305, 150, 375, 150, "am", "#334155", 4)
    b += text(80, 22, "LEFT", attrs=SMALL, weight=1) + text(210, 22, "RIGHT", attrs=SMALL, weight=1)
    b += text(470, 22, "LEFT", attrs=SMALL, weight=1) + text(600, 22, "RIGHT", attrs=SMALL, weight=1)
    b += text(150, 282, "(a) At the start", weight=1) + text(540, 282, "(b) Later: no net movement", weight=1)
    # key
    b += ('<circle cx="40" cy="306" r="5" fill="%s" stroke="#a16207"/><text x="52" y="311" %s>potassium nitrate particle</text>'
          '<circle cx="250" cy="306" r="5" fill="#3b82f6" stroke="#1e40af"/><text x="262" y="311" %s>copper(II) sulfate particle</text>'
          '<line x1="470" y1="298" x2="470" y2="314" stroke="#475569" stroke-width="2.5" stroke-dasharray="5 3"/><text x="482" y="311" %s>permeable membrane</text>'
          % (YELLOW, SMALL, SMALL, SMALL))
    return svg(690, 322, b, "Beaker (a): potassium nitrate particles on the left and copper(II) sulfate particles on the right of a permeable membrane, with arrows showing each moving to the other side. Beaker (b): both kinds of particle evenly spread on both sides", 690)


def alveolus(labels=True):
    """Gas exchange in the lungs, close-up: air space, thin wall, blood capillary with red blood cells."""
    rng = random.Random(25)
    b = ARROW_DEFS % ("ao", "#dc2626") + ARROW_DEFS % ("ac", "#111827")
    b += '<rect x="20" y="20" width="250" height="300" fill="#f8fafc"/>'                         # air space
    b += '<path d="M270 20 C262 100 278 220 270 320 L300 320 C308 220 292 100 300 20 Z" fill="#fecdd3" stroke="#9f1239" stroke-width="2"/>'   # wall
    for y in (70, 170, 270):
        b += '<ellipse cx="286" cy="%d" rx="6" ry="9" fill="#9f1239"/>' % y
    b += '<path d="M300 20 C308 100 292 220 300 320 L340 320 L340 20 Z" fill="#fff1f2"/>'        # capillary wall gap
    b += '<rect x="340" y="20" width="12" height="300" fill="#fda4af"/>'                         # capillary wall
    b += '<rect x="352" y="20" width="168" height="300" fill="#fee2e2"/>'                        # blood plasma
    for (x, y) in ((420, 70), (460, 160), (415, 250)):
        b += '<ellipse cx="%d" cy="%d" rx="38" ry="22" fill="#dc2626" stroke="#7f1d1d" stroke-width="2"/><ellipse cx="%d" cy="%d" rx="16" ry="8" fill="#ef4444"/>' % (x, y, x, y)
    b += dots(rng, 22, 40, 250, 40, 300, 4.5, "#dc2626")      # oxygen
    b += dots(rng, 6, 40, 250, 40, 300, 4.5, "#111827")       # carbon dioxide (fewer in the air)
    b += dots(rng, 14, 360, 515, 30, 310, 4.5, "#111827")
    b += arrow(150, 110, 432, 158, "ao", "#dc2626", 4)
    b += arrow(470, 230, 170, 250, "ac", "#111827", 4)
    if labels:
        b += text(130, 345, "air space in the lung", weight=1) + text(436, 345, "blood capillary", weight=1)
        b += lbl("wall of air sac (one cell thick)", 260, 375, 286, 300, "middle").replace('text-anchor="middle"', 'text-anchor="middle"')
        b += '<text x="40" y="100" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-weight="700" fill="#b91c1c" %s>oxygen diffuses into the blood</text>' % HALO
        b += '<text x="40" y="282" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-weight="700" fill="#111827" %s>carbon dioxide diffuses out</text>' % HALO
        b += ('<line x1="458" y1="70" x2="540" y2="70" stroke="#334155" stroke-width="1.3"/><text x="546" y="75" %s>red blood cell</text>' % FONT)
        b += ('<circle cx="560" cy="200" r="4.5" fill="#dc2626"/><text x="572" y="205" %s>oxygen</text>'
              '<circle cx="560" cy="226" r="4.5" fill="#111827"/><text x="572" y="231" %s>carbon dioxide</text>' % (SMALL, SMALL))
        return svg(680, 390, b, "Close-up of an air sac in the lung. Oxygen diffuses from the air space through the thin wall into a red blood cell in the capillary. Carbon dioxide diffuses the other way, from the blood into the air space", 680)
    return b


ALV_VB = (680, 360)
ALV_TARGETS = [
    dict(key="air", label="air space in the lung", pt=(110, 200), box=(110, 340), side="c"),
    dict(key="wall", label="wall of air sac", pt=(286, 300), box=(286, 340), side="c"),
    dict(key="cap", label="blood capillary", pt=(500, 300), box=(470, 340), side="c"),
    dict(key="rbc", label="red blood cell", pt=(458, 70), box=(560, 70), side="r"),
    dict(key="o2", label="oxygen", pt=(432, 158), box=(560, 170), side="r"),
    dict(key="co2", label="carbon dioxide", pt=(170, 250), box=(560, 250), side="r"),
]


def root_hair_gas():
    """A root hair cell in soil: oxygen diffuses in from air spaces, carbon dioxide diffuses out."""
    rng = random.Random(27)
    b = ARROW_DEFS % ("ro", "#dc2626") + ARROW_DEFS % ("rc", "#111827")
    b += '<rect x="0" y="0" width="600" height="300" fill="#e7d7bd"/>'
    for _ in range(26):   # soil particles
        x, y, r = rng.uniform(10, 550), rng.uniform(10, 290), rng.uniform(10, 22)
        if not (40 < y < 250 and 140 < x < 520):
            b += '<circle cx="%.0f" cy="%.0f" r="%.0f" fill="#b08962" stroke="#7c5a3a"/>' % (x, y, r)
    # epidermis cells along the bottom, one with a long root hair going up and right
    b += '<rect x="0" y="250" width="600" height="50" fill="#fef9c3" stroke="%s" stroke-width="1.5"/>' % LINE
    for x in (0, 110, 340, 450, 560):
        b += '<rect x="%d" y="250" width="110" height="50" fill="#fef3c7" stroke="%s" stroke-width="1.5"/>' % (x, LINE)
    b += ('<path d="M220 300 V250 C220 210 240 175 300 150 C360 128 430 110 520 100 Q536 104 520 116 C440 126 372 146 320 166 C276 184 262 214 262 250 V300 Z" '
          'fill="%s" stroke="%s" stroke-width="2"/>' % (CYTO, LINE))
    b += '<path d="M232 292 V252 C232 214 252 186 306 162 C360 140 420 124 500 112 C424 124 368 144 318 170 C280 188 252 216 252 292 Z" fill="#e0f2fe" opacity="0.9"/>'
    b += '<ellipse cx="300" cy="157" rx="12" ry="8" fill="#ebe3f6" stroke="%s" stroke-width="1.5"/>' % LINE
    b += dots(rng, 10, 300, 540, 30, 90, 4.5, "#dc2626")
    b += arrow(420, 40, 400, 118, "ro", "#dc2626", 4)
    b += arrow(290, 182, 200, 110, "rc", "#111827", 4)
    b += '<text x="330" y="24" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-weight="700" fill="#b91c1c" %s>oxygen diffuses into the root hair cell</text>' % HALO
    b += '<text x="20" y="96" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-weight="700" fill="#111827" %s><tspan x="20">carbon dioxide diffuses</tspan><tspan x="20" dy="1.2em">out of the root hair cell</tspan></text>' % HALO
    b += ('<line x1="470" y1="112" x2="500" y2="190" stroke="#334155" stroke-width="1.3"/><text x="506" y="204" %s text-anchor="middle" %s>root hair cell</text>' % (FONT, HALO))
    b += ('<line x1="60" y1="275" x2="60" y2="240" stroke="#334155" stroke-width="1.3"/><text x="60" y="234" %s text-anchor="middle" %s>epidermal cell of root</text>' % (SMALL, HALO))
    b += ('<line x1="160" y1="40" x2="180" y2="60" stroke="#334155" stroke-width="1.3"/><text x="150" y="36" %s text-anchor="end" %s>air space in soil</text>' % (SMALL, HALO))
    return svg(600, 300, b, "A root hair cell growing out between soil particles. Oxygen from the air spaces in the soil diffuses into the root hair cell; carbon dioxide diffuses out", 560)


# ================================================================== 2.2 Osmosis
def utube(after=False, labels=True):
    """U-tube with a partially permeable membrane at the bottom. Arm A: 10% sucrose; arm B: 5% sucrose."""
    rng = random.Random(31 + after)
    la, lb = (70, 160) if after else (110, 110)
    xa, xb, base = 85, 215, 250
    path = "M%d 40 V%d A65 65 0 0 0 %d %d V40" % (xa, base, xb, base)
    b = '<path d="%s" fill="none" stroke="%s" stroke-width="58"/>' % (path, LINE)
    b += '<path d="%s" fill="none" stroke="#fff" stroke-width="52"/>' % path
    liq = "M%d %d V%d A65 65 0 0 0 %d %d V%d" % (xa, la, base, xb, base, lb)
    b += '<path d="%s" fill="none" stroke="%s" stroke-width="52"/>' % (liq, WATER)
    b += '<line x1="150" y1="287" x2="150" y2="343" stroke="#0f766e" stroke-width="3" stroke-dasharray="6 4"/>'

    def arm(x, top, n_s, n_w):
        h = ""
        for _ in range(n_w):
            h += '<circle cx="%.0f" cy="%.0f" r="2.6" fill="%s"/>' % (x + rng.uniform(-20, 20), rng.uniform(top + 6, base + 20), BLUE)
        for _ in range(n_s):
            h += '<circle cx="%.0f" cy="%.0f" r="6" fill="%s" stroke="#9a3412"/>' % (x + rng.uniform(-18, 18), rng.uniform(top + 10, base + 15), ORANGE)
        return h
    b += arm(xa, la, 9 if after else 9, 55 if after else 38) + arm(xb, lb, 4, 30 if after else 47)
    for t in range(14):   # liquid round the bend
        a = 3.14159 * (t + 0.5) / 14
        b += '<circle cx="%.0f" cy="%.0f" r="2.6" fill="%s"/>' % (150 - 65 * __import__("math").cos(a), base + 65 * __import__("math").sin(a) + rng.uniform(-14, 14), BLUE)
    b += text(xa, 22, "A", weight=1) + text(xb, 22, "B", weight=1)
    if labels:
        b += '<g %s>' % SMALL
        if not after:
            b += lbl("10% sucrose solution", 46, 140, 70, 140) + lbl("5% sucrose solution", 254, 140, 230, 140, "start")
            b += lbl("sucrose molecule", 46, 200, xa - 6, 205) + lbl("water molecule", 254, 200, xb + 8, 205, "start")
        else:
            b += lbl("level rises", 46, 70, 70, la) + lbl("level falls", 254, 160, 230, lb, "start")
        b += lbl("partially permeable membrane", 150, 375, 150, 330, "middle")
        b += '</g>'
    b += '<text x="150" y="%d" text-anchor="middle" %s font-weight="700">%s</text>' % (400, FONT, "(b) After some time" if after else "(a) At the start")
    return '<svg viewBox="-110 0 520 410" role="img" aria-label="%s" style="max-width:380px">%s</svg>' % (
        "U-tube after osmosis: the level in arm A (10% sucrose) has risen and the level in arm B has fallen" if after else
        "U-tube at the start: arm A holds 10% sucrose solution and arm B holds 5% sucrose solution at the same level, separated at the bottom by a partially permeable membrane", b)


def dialysis(labels=True, after=False):
    """Let's Investigate: dialysis tubing of sucrose solution in a boiling tube of distilled water.
    At the start the liquid levels inside and outside the tubing are the same; after 20 minutes the level inside has risen."""
    out_lvl = 126 if after else 120          # distilled water in the boiling tube
    in_lvl = 64 if after else 120            # sucrose solution in the tubing
    w = 30 if after else 24                  # half-width of the swollen bag
    b = '<path d="M122 %d V386 a38 38 0 0 0 76 0 V%d Z" fill="%s"/>' % (out_lvl, out_lvl, WATER)
    b += '<path d="M116 40 V386 a44 44 0 0 0 88 0 V40" fill="none" stroke="%s" stroke-width="3"/>' % LINE      # boiling tube
    bag = ('M150 30 V170 C%d 196 %d 300 160 338 C%d 300 %d 196 170 170 V30 Z' % (160 - w, 160 - w, 160 + w, 160 + w))
    b += '<path d="%s" fill="#e0f2fe" stroke="#0369a1" stroke-width="2.5"/>' % bag
    b += '<clipPath id="bagclip%d"><path d="%s"/></clipPath>' % (after, bag)
    b += '<rect x="120" y="%d" width="80" height="%d" fill="#38bdf8" clip-path="url(#bagclip%d)"/>' % (in_lvl, 340 - in_lvl, after)
    b += '<path d="%s" fill="none" stroke="#0369a1" stroke-width="2.5"/>' % bag
    b += '<path d="M153 340 l7 14 l7 -14 M150 348 l10 6 l10 -6" fill="none" stroke="#0369a1" stroke-width="2.5"/>'  # knot
    b += '<path d="M146 22 h28 v18 h-28 z" fill="#e2e8f0" stroke="#475569" stroke-width="2"/>'                  # paper clip
    b += '<path d="M150 22 v-8 a6 6 0 0 1 12 0 v20" fill="none" stroke="#475569" stroke-width="2"/>'
    b += '<line x1="102" y1="120" x2="116" y2="120" stroke="#dc2626" stroke-width="3"/>'                        # level mark
    if labels:
        b += '<g %s>' % SMALL
        b += lbl("paper clip", 230, 26, 174, 26, "start") + lbl("dialysis tubing", 230, 230, 186, 230, "start")
        b += lbl("sucrose solution", 90, 260, 158, 260) + lbl("knot", 230, 352, 168, 350, "start")
        b += lbl("boiling tube", 90, 330, 116, 330) + lbl("distilled water", 230, 400, 186, 395, "start")
        b += lbl("mark: starting level", 90, 100, 104, 120)
        if after:
            b += lbl("level inside has risen", 230, 64, 170, in_lvl, "start")
        b += '</g>'
    return '<svg viewBox="-70 0 440 440" role="img" aria-label="%s" style="max-width:340px">%s</svg>' % (
        "Dialysis tubing tied in a knot at the bottom, filled with sucrose solution and held by a paper clip in a boiling tube of distilled water. " +
        ("After 20 minutes the level inside the tubing has risen well above the starting mark and the tubing has swollen." if after else
         "The liquid levels inside and outside the tubing are the same, at the marked starting level."), b)


def wp_container():
    """A container split by a partially permeable membrane: water moves from higher to lower water potential."""
    rng = random.Random(33)
    b = ARROW_DEFS % ("aw", "#dc2626")
    b += '<rect x="40" y="40" width="200" height="150" fill="#93c5fd"/><rect x="240" y="40" width="200" height="150" fill="#dbeafe"/>'
    b += '<path d="M30 20 V186 q0 14 14 14 H436 q14 0 14 -14 V20" fill="none" stroke="%s" stroke-width="3"/>' % LINE
    b += '<line x1="240" y1="14" x2="240" y2="198" stroke="#0f766e" stroke-width="3" stroke-dasharray="7 5"/>'
    b += dots(rng, 14, 55, 225, 55, 180, 6, ORANGE, "#9a3412") + dots(rng, 4, 255, 425, 55, 180, 6, ORANGE, "#9a3412")
    b += arrow(400, 230, 90, 230, "aw", "#dc2626", 4)
    b += text(245, 254, "water molecules move down a water potential gradient,\nthrough the partially permeable membrane", attrs=SMALL)
    b += text(140, 64, "more solute\nLOWER water potential", attrs=SMALL + " " + HALO, weight=1)
    b += text(340, 64, "less solute\nHIGHER water potential", attrs=SMALL + " " + HALO, weight=1)
    return svg(480, 284, b, "A container divided by a partially permeable membrane. The left side has more solute and a lower water potential; the right side has less solute and a higher water potential. An arrow shows water molecules moving from right to left", 520)


def wp_graph():
    b = ARROW_DEFS % ("ag", "#0f172a") + ARROW_DEFS % ("ad", "#dc2626")
    b += '<line x1="60" y1="270" x2="60" y2="30" stroke="#0f172a" stroke-width="2.5" marker-end="url(#ag)"/>'
    b += '<line x1="60" y1="270" x2="440" y2="270" stroke="#0f172a" stroke-width="2.5" marker-end="url(#ag)"/>'
    b += '<rect x="110" y="70" width="34" height="200" fill="#0ea5e9"/><rect x="340" y="190" width="34" height="80" fill="#0ea5e9"/>'
    b += '<line x1="146" y1="72" x2="336" y2="188" stroke="#dc2626" stroke-width="4" stroke-dasharray="8 5" marker-end="url(#ad)"/>'
    b += '<text x="40" y="160" %s text-anchor="middle" transform="rotate(-90 40 160)">water potential</text>' % FONT
    b += text(127, 292, "dilute solution", attrs=SMALL) + text(357, 292, "concentrated solution", attrs=SMALL)
    b += '<text x="250" y="116" %s fill="#b91c1c" transform="rotate(31 250 116)" text-anchor="middle">water moves down the water potential gradient</text>' % SMALL.replace('fill="#334155"', '')
    b += arrow(110, 18, 380, 18, "ag", "#0f172a", 2)
    b += text(245, 12, "direction of movement of water molecules", attrs=SMALL)
    return svg(470, 300, b, "Graph: the dilute solution has a high water potential (tall bar) and the concentrated solution a low water potential (short bar). Water moves from the dilute to the concentrated solution, down the water potential gradient", 470)


# ------------------------------------------------------------------ cells in solutions
def plant_cell(state="start", w=None):
    """A plant cell. state: start | turgid | plasmolysed. Water arrows show the direction of osmosis."""
    b = ARROW_DEFS % ("pw" + state, "#2563eb")
    b += '<rect x="30" y="30" width="240" height="140" rx="16" fill="#fff" stroke="%s" stroke-width="7"/>' % WALL   # cell wall
    if state == "plasmolysed":
        b += '<rect x="34" y="34" width="232" height="132" rx="12" fill="#e0f2fe"/>'                        # outside solution between wall and membrane
        b += '<path d="M78 62 C110 50 190 52 222 64 C240 80 238 124 220 138 C186 150 110 150 80 138 C62 124 60 76 78 62 Z" fill="%s" stroke="#15803d" stroke-width="2.5"/>' % CYTO
        b += '<ellipse cx="150" cy="100" rx="52" ry="22" fill="#cffafe" stroke="#0e7490" stroke-width="1.5"/>'
        b += '<circle cx="96" cy="100" r="11" fill="#ebe3f6" stroke="%s" stroke-width="1.5"/>' % LINE
        for (x1, y1, x2, y2) in ((150, 78, 150, 8), (150, 122, 150, 194), (204, 100, 300, 100)):
            b += arrow(x1, y1, x2, y2, "pw" + state, "#2563eb", 3)
    else:
        b += '<rect x="38" y="38" width="224" height="124" rx="11" fill="%s" stroke="#15803d" stroke-width="2.5"/>' % CYTO
        if state == "turgid":
            b += '<rect x="58" y="44" width="198" height="112" rx="9" fill="#cffafe" stroke="#0e7490" stroke-width="1.5"/>'
            b += '<ellipse cx="49" cy="100" rx="6" ry="13" fill="#ebe3f6" stroke="%s" stroke-width="1.5"/>' % LINE
        else:
            b += '<rect x="84" y="56" width="164" height="88" rx="9" fill="#cffafe" stroke="#0e7490" stroke-width="1.5"/>'
            b += '<circle cx="62" cy="100" r="12" fill="#ebe3f6" stroke="%s" stroke-width="1.5"/>' % LINE
        if state == "turgid":
            for (x1, y1, x2, y2) in ((150, 2, 150, 70), (150, 198, 150, 130), (300, 100, 236, 100)):
                b += arrow(x1, y1, x2, y2, "pw" + state, "#2563eb", 3)
    return '<svg viewBox="0 0 300 200" role="img" aria-label="%s"%s>%s</svg>' % (
        {"start": "A plant cell with a cell wall, cytoplasm lining the wall and a large central vacuole",
         "turgid": "A turgid plant cell: water has entered by osmosis, the vacuole is large and the cytoplasm is pressed against the cell wall",
         "plasmolysed": "A plasmolysed plant cell: water has left by osmosis, the vacuole has shrunk and the cytoplasm and cell membrane have pulled away from the cell wall"}[state],
        ' style="max-width:%dpx"' % w if w else "", b)


PLASMO_VB = (560, 200)
_PX = 130   # the cell is shifted right by this much inside the labeller so the label boxes fit on both sides
PLASMO_TARGETS = [dict(t, pt=(t["pt"][0] + _PX, t["pt"][1])) for t in [
    dict(key="wall", label="cell wall", pt=(268, 50), box=(450, 30), side="r"),
    dict(key="mem", label="cell membrane", pt=(222, 64), box=(450, 75), side="r"),
    dict(key="vac", label="vacuole", pt=(170, 104), box=(450, 120), side="r"),
    dict(key="sol", label="outside solution", pt=(248, 150), box=(450, 165), side="r"),
    dict(key="cyto", label="cytoplasm", pt=(80, 80), box=(110, 60), side="l"),
    dict(key="nuc", label="nucleus", pt=(96, 100), box=(110, 130), side="l"),
]]


def plasmo_inner():
    """Plasmolysed cell drawing without water arrows (for labelling)."""
    s = plant_cell("plasmolysed")
    inner = s[s.index(">") + 1:s.rindex("</svg>")]
    return '<g transform="translate(%d 0)">%s</g>' % (_PX, inner.split('<line')[0])


def rbc(state="normal", w=None):
    """A red blood cell. state: normal | swollen | burst | crenated."""
    b = ""
    if state == "normal":
        b += '<circle cx="100" cy="90" r="50" fill="#dc2626" stroke="#7f1d1d" stroke-width="2.5"/><circle cx="100" cy="90" r="22" fill="#ef4444"/>'
    elif state == "swollen":
        b += '<circle cx="100" cy="90" r="64" fill="#ef4444" stroke="#7f1d1d" stroke-width="2.5"/>'
    elif state == "burst":
        b += ('<path d="M100 26 A64 64 0 1 1 52 46 L66 58 L58 40 L74 48 Z" fill="#fca5a5" stroke="#7f1d1d" stroke-width="2.5"/>'
              '<circle cx="54" cy="30" r="4" fill="#ef4444"/><circle cx="40" cy="44" r="3" fill="#ef4444"/><circle cx="66" cy="20" r="3" fill="#ef4444"/>')
    else:   # crenated: shrunken with spikes
        import math
        pts = []
        for i in range(40):
            a = 2 * math.pi * i / 40
            r = 40 if i % 2 else 50
            pts.append("%.1f %.1f" % (100 + r * math.cos(a), 90 + r * math.sin(a)))
        b += '<path d="M%s Z" fill="#b91c1c" stroke="#7f1d1d" stroke-width="2" stroke-linejoin="round"/>' % " L".join(pts)
    return '<svg viewBox="0 0 200 180" role="img" aria-label="%s"%s>%s</svg>' % (
        {"normal": "A normal red blood cell: a red disc, paler in the middle", "swollen": "A swollen red blood cell: larger and rounder",
         "burst": "A burst red blood cell: its membrane has split open", "crenated": "A crenated red blood cell: shrunken with spikes on its surface"}[state],
        ' style="max-width:%dpx"' % w if w else "", b)


def wilting():
    """Two seedlings in jars: (a) firm and upright, (b) wilting."""
    b = ""
    for i, wilt in enumerate((False, True)):
        x = 20 + i * 250
        b += '<rect x="%d" y="150" width="140" height="110" rx="12" fill="#e2e8f0" stroke="%s" stroke-width="2.5"/>' % (x, LINE)
        b += '<rect x="%d" y="170" width="132" height="86" rx="8" fill="#d6b98c"/>' % (x + 4)
        cx = x + 70
        if not wilt:
            b += '<path d="M%d 172 C%d 130 %d 90 %d 50" fill="none" stroke="#65a30d" stroke-width="5"/>' % (cx, cx - 2, cx + 2, cx)
            b += '<path d="M%d 70 C%d 40 %d 40 %d 60 C%d 80 %d 80 %d 70 Z" fill="#84cc16" stroke="#3f6212" stroke-width="2"/>' % (cx, cx - 30, cx - 60, cx - 60, cx - 40, cx - 20, cx)
            b += '<path d="M%d 60 C%d 30 %d 30 %d 48 C%d 68 %d 68 %d 60 Z" fill="#84cc16" stroke="#3f6212" stroke-width="2"/>' % (cx, cx + 30, cx + 60, cx + 60, cx + 40, cx + 20, cx)
            b += '<path d="M%d 50 C%d 30 %d 22 %d 18 C%d 30 %d 42 %d 50 Z" fill="#a3e635" stroke="#3f6212" stroke-width="2"/>' % (cx, cx - 10, cx - 4, cx, cx + 6, cx + 6, cx)
        else:
            b += '<path d="M%d 172 C%d 130 %d 100 %d 90 C%d 80 %d 90 %d 110" fill="none" stroke="#a16207" stroke-width="5"/>' % (cx, cx - 2, cx + 4, cx + 14, cx + 24, cx + 34, cx + 38)
            b += '<path d="M%d 110 C%d 130 %d 150 %d 160 C%d 150 %d 130 %d 110 Z" fill="#a3a33a" stroke="#713f12" stroke-width="2"/>' % (cx + 38, cx + 24, cx + 30, cx + 40, cx + 50, cx + 50, cx + 38)
            b += '<path d="M%d 110 C%d 128 %d 140 %d 146 C%d 136 %d 122 %d 110 Z" fill="#b5a642" stroke="#713f12" stroke-width="2"/>' % (cx + 38, cx + 52, cx + 62, cx + 66, cx + 70, cx + 58, cx + 38)
        b += text(x + 70, 285, "(a) Turgid: firm and upright" if not wilt else "(b) Lost turgor: wilting", attrs=SMALL, weight=1)
    return svg(420, 295, b, "Two seedlings in jars of soil. (a) Its cells are turgid, so the stem and leaves are firm and upright. (b) Its cells have lost turgor, so the stem bends over and the leaves droop", 480)


def intestine():
    """Absorption in the small intestine: digested food diffuses through the one-cell-thick lining into a blood capillary."""
    rng = random.Random(41)
    b = ARROW_DEFS % ("ag2", "#15803d") + ARROW_DEFS % ("aa2", "#7c3aed")
    b += '<rect x="20" y="20" width="250" height="300" fill="#fef9c3"/>'                                        # inside the small intestine
    b += '<rect x="270" y="20" width="62" height="300" fill="#fde7e1" stroke="#9a3412" stroke-width="1.5"/>'   # lining cells
    for y in range(20, 320, 60):
        b += '<line x1="270" y1="%d" x2="332" y2="%d" stroke="#9a3412" stroke-width="1.5"/>' % (y, y)
        b += '<ellipse cx="305" cy="%d" rx="9" ry="7" fill="#ebe3f6" stroke="%s" stroke-width="1.2"/>' % (y + 30, LINE)
        for k in range(6):   # microvilli: tiny folds facing the food
            b += '<rect x="262" y="%d" width="8" height="5" rx="2.5" fill="#fde7e1" stroke="#9a3412" stroke-width="1"/>' % (y + 4 + k * 9)
    b += '<rect x="346" y="20" width="12" height="300" fill="#fda4af"/><rect x="358" y="20" width="162" height="300" fill="#fee2e2"/>'   # capillary
    for (x, y) in ((430, 80), (470, 200), (420, 280)):
        b += '<ellipse cx="%d" cy="%d" rx="36" ry="21" fill="#dc2626" stroke="#7f1d1d" stroke-width="2"/><ellipse cx="%d" cy="%d" rx="15" ry="8" fill="#ef4444"/>' % (x, y, x, y)
    for _ in range(18):
        x, y = rng.uniform(35, 250), rng.uniform(35, 305)
        b += '<polygon points="%s" fill="#16a34a"/>' % " ".join("%.1f,%.1f" % (x + 5 * __import__("math").cos(a * 1.0472), y + 5 * __import__("math").sin(a * 1.0472)) for a in range(6))
    b += dots(rng, 14, 35, 250, 35, 305, 4.5, "#7c3aed")
    b += dots(rng, 4, 370, 515, 30, 310, 4.5, "#7c3aed")
    for _ in range(4):
        x, y = rng.uniform(370, 515), rng.uniform(30, 310)
        b += '<polygon points="%s" fill="#16a34a"/>' % " ".join("%.1f,%.1f" % (x + 5 * __import__("math").cos(a * 1.0472), y + 5 * __import__("math").sin(a * 1.0472)) for a in range(6))
    b += arrow(150, 120, 420, 140, "ag2", "#15803d", 4) + arrow(150, 240, 420, 236, "aa2", "#7c3aed", 4)
    b += '<text x="34" y="106" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-weight="700" fill="#15803d" %s>glucose diffuses into the blood</text>' % HALO
    b += '<text x="34" y="226" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-weight="700" fill="#6d28d9" %s>amino acids diffuse into the blood</text>' % HALO
    b += text(140, 345, "inside the small intestine", weight=1) + text(436, 345, "blood capillary", weight=1)
    b += lbl("lining of the small intestine (one cell thick)", 300, 375, 300, 300, "middle")
    b += ('<polygon points="%s" fill="#16a34a"/><text x="572" y="205" %s>glucose</text>'
          '<circle cx="560" cy="226" r="4.5" fill="#7c3aed"/><text x="572" y="231" %s>amino acid</text>'
          % (" ".join("%.1f,%.1f" % (560 + 5 * __import__("math").cos(a * 1.0472), 200 + 5 * __import__("math").sin(a * 1.0472)) for a in range(6)), SMALL, SMALL))
    b += '<line x1="458" y1="200" x2="545" y2="150" stroke="#334155" stroke-width="1.3"/><text x="550" y="150" %s>red blood cell</text>' % FONT
    return svg(680, 390, b, "Close-up of the wall of the small intestine. Digested food, glucose and amino acids, diffuses from inside the small intestine through a lining one cell thick into a blood capillary", 680)


def leaf_stomata():
    """Section through a leaf: carbon dioxide diffuses in through a stoma for photosynthesis; oxygen diffuses out."""
    rng = random.Random(43)
    b = ARROW_DEFS % ("lc", "#111827") + ARROW_DEFS % ("lo", "#dc2626")
    b += '<rect x="0" y="0" width="520" height="380" fill="#f8fafc"/>'
    b += '<rect x="20" y="20" width="480" height="290" fill="#ecfccb"/>'
    for x in range(20, 500, 48):   # upper epidermis
        b += '<rect x="%d" y="20" width="48" height="26" fill="#f7fee7" stroke="#3f6212" stroke-width="1.5"/>' % x
    for x in range(20, 500, 30):   # palisade cells with chloroplasts
        b += '<rect x="%d" y="48" width="28" height="92" rx="8" fill="#d9f99d" stroke="#3f6212" stroke-width="1.5"/>' % (x + 1)
        for k in range(4):
            b += '<ellipse cx="%d" cy="%d" rx="4" ry="6" fill="#4d7c0f"/>' % (x + 8 + (k % 2) * 12, 62 + k * 20)
    for (x, y, rx, ry) in ((60, 175, 32, 22), (135, 200, 30, 24), (220, 172, 34, 22), (300, 205, 30, 22), (380, 172, 32, 24), (455, 200, 30, 22),
                           (50, 250, 28, 20), (125, 262, 26, 18), (205, 245, 30, 20), (450, 255, 28, 20), (395, 262, 22, 16)):
        b += '<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#d9f99d" stroke="#3f6212" stroke-width="1.5"/>' % (x, y, rx, ry)
        b += '<ellipse cx="%d" cy="%d" rx="3.5" ry="5" fill="#4d7c0f"/><ellipse cx="%d" cy="%d" rx="3.5" ry="5" fill="#4d7c0f"/>' % (x - 10, y - 4, x + 10, y + 4)
    for x in range(20, 500, 48):   # lower epidermis with a gap for the stoma
        if not 260 <= x <= 308:
            b += '<rect x="%d" y="284" width="48" height="26" fill="#f7fee7" stroke="#3f6212" stroke-width="1.5"/>' % x
    b += '<path d="M260 284 q24 -6 30 13 q-6 19 -30 13 z" fill="#bef264" stroke="#3f6212" stroke-width="2"/>'   # guard cells
    b += '<path d="M356 284 q-24 -6 -30 13 q6 19 30 13 z" fill="#bef264" stroke="#3f6212" stroke-width="2"/>'
    b += dots(rng, 7, 120, 420, 325, 370, 4.5, "#111827") + dots(rng, 3, 120, 420, 325, 370, 4.5, "#dc2626")
    b += '<path d="M300 365 C300 330 306 300 300 270 C292 240 250 220 180 150" fill="none" stroke="#111827" stroke-width="4" marker-end="url(#lc)"/>'
    b += '<path d="M330 150 C370 200 330 250 318 280 C312 300 318 330 340 362" fill="none" stroke="#dc2626" stroke-width="4" marker-end="url(#lo)"/>'
    b += '<text x="40" y="352" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-weight="700" fill="#111827" %s>carbon dioxide diffuses in</text>' % HALO
    b += '<text x="350" y="352" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-weight="700" fill="#b91c1c" %s>oxygen diffuses out</text>' % HALO
    b += '<g %s>' % SMALL
    b += lbl("upper epidermis", 530, 36, 496, 33, "start") + lbl("palisade cell (photosynthesis)", 530, 96, 496, 96, "start")
    b += lbl("air space", 530, 232, 340, 232, "start") + lbl("spongy cell", 530, 182, 482, 200, "start")
    b += lbl("guard cell", 530, 290, 352, 297, "start") + lbl("stoma (pore)", 530, 322, 312, 300, "start")
    b += '</g>'
    b += ('<circle cx="560" cy="350" r="4.5" fill="#111827"/><text x="572" y="355" %s>carbon dioxide</text>'
          '<circle cx="560" cy="372" r="4.5" fill="#dc2626"/><text x="572" y="377" %s>oxygen</text>' % (SMALL, SMALL))
    return svg(750, 385, b, "Section through a leaf. In the light, carbon dioxide from the air diffuses in through a stoma on the underside of the leaf, through the air spaces to the palisade cells, which use it in photosynthesis. Oxygen made in photosynthesis diffuses out through the stoma", 700)
