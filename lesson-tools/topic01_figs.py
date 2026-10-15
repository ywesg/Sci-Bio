"""SVG drawings for Topic 1 (Cell Structure and Organisation). Used by build_topic01.py.
Every clickable part is wrapped in <g class="part" data-part="key"> and every label in <g class="lbl" data-part="key">."""

FONT = 'font-family="Source Sans 3, system-ui, sans-serif" font-size="16" fill="#1f2937"'


def lbl(key, text, tx, ty, x2, y2, anchor="end"):
    """A label with a leader line from the text to the point (x2, y2)."""
    x1 = tx + (6 if anchor == "end" else -6)
    return ('<g class="lbl" data-part="%s"><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#334155" stroke-width="1.4"/>'
            '<circle cx="%d" cy="%d" r="2.4" fill="#334155"/><text x="%d" y="%d" text-anchor="%s" %s>%s</text></g>'
            % (key, x1, ty - 5, x2, y2, x2, y2, tx, ty, anchor, FONT, text))


# colours follow the textbook slides: cream cytoplasm, lilac nucleus with pink chromosomes, blue mitochondria, red ribosomes, brown cell wall
CYTO = "#fbf3c6"
LINE = "#3f3f46"


def mito(x, y, rot, rx=22, ry=11):
    """A bean-shaped mitochondrion (light blue, with folded inner membrane)."""
    n = 6
    xs = [-0.62 * rx + i * (1.24 * rx / (n - 1)) for i in range(n)]
    zig = " ".join("%s %s" % (round(xx, 1), round((0.42 if i % 2 else -0.42) * ry, 1)) for i, xx in enumerate(xs))
    return ('<g transform="translate(%s %s) rotate(%s)"><path d="M%s 0 C%s %s %s %s 0 %s C%s %s %s %s %s 0 C%s %s %s %s 0 %s C%s %s %s %s %s 0 Z" '
            'fill="#b9d8f2" stroke="#2563a8" stroke-width="%s"/>'
            '<polyline points="%s" fill="none" stroke="#2563a8" stroke-width="%s" stroke-linejoin="round"/></g>'
            % (x, y, rot,
               -rx, -rx, -ry * 1.25, -rx * 0.35, -ry * 1.1, -ry * 0.85, rx * 0.35, -ry * 0.6, rx, -ry * 1.3, rx,
               rx, ry * 1.3, rx * 0.35, ry * 1.1, ry * 0.95, -rx * 0.35, ry * 0.7, -rx, ry * 1.25, -rx,
               2.2 if rx > 15 else 1.6, zig, 1.5 if rx > 15 else 1.1))


def chloro(x, y, rot):
    """A chloroplast: green oval with dark stacks inside."""
    return ('<g transform="translate(%s %s) rotate(%s)"><ellipse rx="16" ry="8.5" fill="#cfe6bd" stroke="#3f7d32" stroke-width="2"/>'
            '<path d="M-9 -2h5M-3 2h6M4 -3h5M-6 4h4M2 -6h4" stroke="#1f2937" stroke-width="2"/></g>' % (x, y, rot))


def ribos(pts):
    return "".join('<circle cx="%d" cy="%d" r="2.2" fill="#e11d48"/>' % p for p in pts)


def nucleus_round(cx, cy, r):
    """Lilac nucleus with pink chromosome threads and a dark blue nucleolus."""
    k = r / 44.0
    return ('<circle cx="%s" cy="%s" r="%s" fill="#ebe3f6" stroke="%s" stroke-width="2.2"/>'
            '<path d="M%s %s q%s %s %s 0 t%s 0 t%s 0 M%s %s q%s %s %s 0 t%s 0 M%s %s q%s %s %s %s t%s %s M%s %s q%s %s %s 0 t%s 0" fill="none" stroke="#db2777" stroke-width="1.5"/>'
            '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#1f5fa8"/>'
            % (cx, cy, r, LINE,
               cx - 28 * k, cy - 14 * k, 6 * k, -9 * k, 12 * k, 12 * k, 12 * k,
               cx - 24 * k, cy + 6 * k, 6 * k, 8 * k, 12 * k, 12 * k,
               cx + 4 * k, cy - 30 * k, 5 * k, 8 * k, 2 * k, 14 * k, 2 * k, 14 * k,
               cx - 14 * k, cy + 22 * k, 5 * k, -8 * k, 10 * k, 10 * k,
               cx + 14 * k, cy + 10 * k, 9 * k, 7 * k))


# ------------------------------------------------------------------ typical animal and plant cells, laid out like the textbook diagrams
ANIMAL_VB = (780, 340)
PLANT_VB = (780, 330)
ANIMAL_OUTLINE = ("M262 52 C300 28 370 20 430 24 C478 28 506 52 512 92 C518 132 502 162 508 202 C514 252 482 302 412 314 "
                  "C342 326 272 320 232 298 C192 276 182 232 192 192 C200 152 214 92 262 52 Z")


def chrom(cx, cy, k):
    """A tangle of pink chromosome threads inside a nucleus."""
    return ('<path d="M%s %s q%s %s %s %s t%s %s t%s %s M%s %s q%s %s %s %s t%s %s M%s %s q%s %s %s %s t%s %s t%s %s '
            'M%s %s q%s %s %s %s t%s %s" fill="none" stroke="#e0218a" stroke-width="%s" stroke-linecap="round"/>'
            % (cx - 26 * k, cy - 14 * k, 6 * k, -12 * k, 14 * k, -4 * k, 12 * k, 6 * k, 12 * k, -8 * k,
               cx - 30 * k, cy + 4 * k, 8 * k, 10 * k, 16 * k, 2 * k, 14 * k, -6 * k,
               cx - 12 * k, cy - 26 * k, 10 * k, 12 * k, 4 * k, 22 * k, 10 * k, 10 * k, 10 * k, 18 * k,
               cx + 4 * k, cy - 6 * k, 10 * k, -10 * k, 18 * k, -2 * k, 4 * k, 16 * k, 1.6 if k > 0.7 else 1.2))


def bracket(x, y0, y1, text):
    return ('<path d="M%d %d q10 0 10 10 V%d q0 8 8 8 q-8 0 -8 8 V%d q0 10 -10 10" fill="none" stroke="#1f2937" stroke-width="1.4"/>'
            '<text x="%d" y="%d" %s font-weight="700">%s</text>' % (x, y0, (y0 + y1) / 2 - 8, y1 - 10, x + 26, (y0 + y1) / 2 + 5, FONT, text))


def animal_cell(labels=True, w=640):
    vw, vh = ANIMAL_VB
    s = ['<svg viewBox="0 0 %d %d" width="%d" role="img" aria-label="Diagram of a typical animal cell">' % (vw, vh, w)]
    s.append('<g class="part" data-part="cytoplasm"><path d="%s" fill="%s"/></g>' % (ANIMAL_OUTLINE, CYTO))
    s.append('<g class="part" data-part="cell-membrane"><path d="%s" fill="none" stroke="%s" stroke-width="2.4"/>'
             '<path d="%s" fill="none" stroke="transparent" stroke-width="14"/></g>' % (ANIMAL_OUTLINE, LINE, ANIMAL_OUTLINE))
    s.append('<g class="part" data-part="nucleus"><circle cx="370" cy="160" r="46" fill="#ebe3f6" stroke="%s" stroke-width="2.2"/>%s'
             '<ellipse cx="378" cy="190" rx="10" ry="9" fill="#1f5fa8" stroke="#0f2f5a" stroke-width="1.5"/></g>' % (LINE, chrom(370, 156, 1.1)))
    for x, y, r in ((340, 62, -8), (462, 84, 20), (478, 178, 80), (300, 214, 92), (372, 282, 0)):
        s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(x, y, r, 15, 8))
    for cx, cy, r in ((392, 40, 5), (272, 106, 6), (436, 96, 5), (498, 126, 6), (282, 238, 6), (380, 262, 5), (420, 254, 5),
                      (492, 246, 5), (310, 290, 4), (320, 296, 4)):
        s.append('<g class="part" data-part="vacuole-a"><circle cx="%d" cy="%d" r="%d" fill="#fff" stroke="%s" stroke-width="1.6"/></g>' % (cx, cy, r, LINE))
    s.append('<g class="part" data-part="ribosomes">%s</g>' % ribos([(306, 74), (310, 86), (250, 132), (274, 160), (252, 172), (262, 208), (338, 234), (366, 236),
                                                                       (390, 226), (418, 212), (444, 194), (470, 218), (500, 160), (476, 152), (448, 118),
                                                                       (420, 290), (450, 272), (330, 126), (420, 110)]))
    if labels:
        s.append(lbl("cell-membrane", "cell membrane", 196, 42, 280, 42))
        s.append(lbl("chromosome", "chromosome", 196, 140, 356, 140))
        s.append(lbl("nuclear-membrane", "nuclear membrane", 196, 178, 327, 178))
        s.append(lbl("cytoplasm", "cytoplasm", 196, 232, 248, 232))
        s.append(lbl("mitochondrion", "mitochondrion", 548, 90, 476, 86, "start"))
        s.append(lbl("nucleus", "nucleus", 548, 146, 416, 146, "start"))
        s.append(lbl("ribosomes", "ribosome", 548, 216, 470, 218, "start"))
        s.append(lbl("vacuole-a", "vacuole", 548, 256, 497, 248, "start"))
        s.append(bracket(650, 62, 270, "organelles"))
    s.append("</svg>")
    return "".join(s)


PLANT_WALL = ("M196 74 C204 52 222 46 252 46 H544 C572 44 586 54 588 82 C590 140 586 210 590 268 C592 292 578 302 548 302 H230 "
              "C202 302 186 292 188 264 C190 200 184 130 196 74 Z")
PLANT_MEMB = ("M210 82 C216 64 230 60 254 60 H542 C562 58 574 66 574 86 C576 140 572 210 576 264 C578 282 566 288 546 288 H232 "
              "C212 288 202 280 202 262 C204 200 200 132 210 82 Z")
PLANT_VAC = ("M246 104 C262 94 288 108 312 98 C336 90 356 106 380 100 C400 96 412 108 428 120 C446 132 470 128 486 134 "
             "C502 142 496 162 504 180 C512 200 498 214 506 232 C512 250 494 258 470 254 C440 250 412 262 380 256 "
             "C350 250 320 262 290 256 C262 252 240 260 236 238 C232 216 248 200 240 176 C232 150 230 120 246 104 Z")


def plant_cell(labels=True, w=640, sap_text=False):
    vw, vh = PLANT_VB
    s = ['<svg viewBox="0 0 %d %d" width="%d" role="img" aria-label="Diagram of a typical plant cell">' % (vw, vh, w)]
    s.append('<g class="part" data-part="cell-wall"><path fill-rule="evenodd" d="%s %s" fill="#b8693f" stroke="%s" stroke-width="2"/></g>' % (PLANT_WALL, PLANT_MEMB, LINE))
    s.append('<g class="part" data-part="cytoplasm"><path d="%s" fill="%s"/></g>' % (PLANT_MEMB, CYTO))
    s.append('<g class="part" data-part="cell-membrane"><path d="%s" fill="none" stroke="%s" stroke-width="2"/>'
             '<path d="%s" fill="none" stroke="transparent" stroke-width="10"/></g>' % (PLANT_MEMB, LINE, PLANT_MEMB))
    s.append('<g class="part" data-part="vacuole-p"><path d="%s" fill="#fff" stroke="%s" stroke-width="2"/>' % (PLANT_VAC, LINE)
             + ('<text x="370" y="185" text-anchor="middle" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-style="italic" fill="#64748b">cell sap</text>' if sap_text else '') + '</g>')
    s.append('<g class="part" data-part="nucleus"><ellipse cx="522" cy="100" rx="30" ry="25" fill="#ebe3f6" stroke="%s" stroke-width="2.2"/>%s'
             '<ellipse cx="503" cy="104" rx="6" ry="5" fill="#1f5fa8" stroke="#0f2f5a" stroke-width="1.2"/></g>' % (LINE, chrom(526, 100, 0.62)))
    for x, y, r, rx in ((292, 80, 0, 22), (382, 80, 0, 22), (226, 214, 80, 20), (380, 276, 0, 22), (486, 276, 0, 18)):
        s.append('<g class="part" data-part="chloroplast"><ellipse cx="%d" cy="%d" rx="%d" ry="11" transform="rotate(%d %d %d)" fill="#cfe6bd" stroke="%s" stroke-width="2"/></g>' % (x, y, rx, r, x, y, LINE))
    for x, y, r in ((222, 132, 75), (556, 196, 80), (434, 276, 0)):
        s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(x, y, r, 14, 8))
    s.append('<g class="part" data-part="ribosomes">%s</g>' % ribos([(250, 72), (330, 74), (346, 86), (440, 72), (466, 86), (230, 100), (216, 172), (222, 248),
                                                                       (262, 272), (300, 276), (318, 266), (412, 284), (526, 260), (556, 238), (560, 150),
                                                                       (550, 134), (536, 140), (466, 120)]))
    if labels:
        s.append(lbl("cell-membrane", "cell membrane", 170, 118, 206, 118))
        s.append(lbl("cytoplasm", "cytoplasm", 170, 170, 222, 170))
        s.append(lbl("cell-wall", "cell wall", 170, 226, 192, 226))
        s.append('<g class="lbl" data-part="nuclear-membrane"><line x1="440" y1="30" x2="497" y2="88" stroke="#334155" stroke-width="1.4"/><circle cx="497" cy="88" r="2.4" fill="#334155"/>'
                 '<text x="440" y="22" text-anchor="middle" %s>nuclear membrane</text></g>' % FONT)
        s.append('<g class="lbl" data-part="chromosome"><line x1="574" y1="30" x2="530" y2="94" stroke="#334155" stroke-width="1.4"/><circle cx="530" cy="94" r="2.4" fill="#334155"/>'
                 '<text x="574" y="22" text-anchor="middle" %s>chromosome</text></g>' % FONT)
        s.append(lbl("nucleus", "nucleus", 616, 100, 552, 100, "start"))
        s.append(lbl("ribosomes", "ribosome", 616, 138, 562, 136, "start"))
        s.append(lbl("mitochondrion", "mitochondrion", 616, 198, 566, 196, "start"))
        s.append(lbl("vacuole-p", "vacuole", 616, 232, 470, 230, "start"))
        s.append(lbl("chloroplast", "chloroplast", 616, 272, 498, 276, "start"))
        s.append('<text x="616" y="292" %s>(containing chlorophyll)</text>' % FONT.replace('font-size="16"', 'font-size="14"'))
    s.append("</svg>")
    return "".join(s)


INFO = {
    "cell-wall": ("Cell wall", "Made of cellulose. Protects the cell from injury and gives it a fixed shape. It is fully permeable. Plant cells only."),
    "cell-membrane": ("Cell membrane", "Controls the movement of substances into and out of the cell. It is partially permeable: it lets only small, soluble substances through. In all cells."),
    "cytoplasm": ("Cytoplasm", "The site of cellular activities (most chemical reactions happen here). It contains the organelles. In all cells."),
    "nucleus": ("Nucleus", "Controls cell activities such as cell division, growth and repair. Contains chromosomes made of DNA, which carries hereditary information. In all cells (except a few, such as red blood cells)."),
    "vacuole-p": ("Large central vacuole", "Stores cell sap (water with dissolved sugar, mineral salts and amino acids). Plant cells usually have one large, permanent vacuole."),
    "vacuole-a": ("Small vacuole", "Stores substances such as water and food. Animal cells have small, temporary vacuoles, often many of them."),
    "mitochondrion": ("Mitochondrion (plural: mitochondria)", "The site of aerobic respiration: releases energy from food for the cell. Seen only with an electron microscope. In all cells."),
    "ribosomes": ("Ribosomes", "The site of protein synthesis (they make proteins). Tiny dots: seen only with an electron microscope. In all cells."),
    "chloroplast": ("Chloroplast", "Contains the green pigment chlorophyll, which absorbs light for photosynthesis (how plants make food). Only in some plant cells, e.g. leaf cells."),
}
INFO_ANIMAL = {k: INFO[k] for k in ("cell-membrane", "cytoplasm", "nucleus", "vacuole-a", "mitochondrion", "ribosomes")}
INFO_PLANT = {k: INFO[k] for k in ("cell-wall", "cell-membrane", "cytoplasm", "nucleus", "vacuole-p", "chloroplast", "mitochondrion", "ribosomes")}


# ------------------------------------------------------------------ what you see under a light microscope
def field(kind):
    """A circular field of view under a light microscope: 'onion' (iodine), 'cheek' (methylene blue) or 'leaf' (pondweed leaf, no stain)."""
    clip = '<defs><clipPath id="fv-%s"><circle cx="120" cy="120" r="112"/></clipPath></defs>' % kind
    bg = {"onion": "#fef9c3", "cheek": "#eff6ff", "leaf": "#f7fee7"}[kind]
    s = ['<svg viewBox="0 0 240 240" width="240" role="img" aria-label="%s">' % {
        "onion": "Onion epidermis cells under a light microscope: brick-shaped cells with walls and a nucleus each",
        "cheek": "Human cheek cells under a light microscope: flat, irregular cells with a central nucleus",
        "leaf": "Pondweed leaf cells under a light microscope: box-shaped cells packed with green chloroplasts"}[kind], clip]
    s.append('<g clip-path="url(#fv-%s)"><rect width="240" height="240" fill="%s"/>' % (kind, bg))
    if kind in ("onion", "leaf"):
        w, h = (64, 30) if kind == "onion" else (40, 34)
        for row in range(-1, 9):
            off = (row % 2) * w / 2
            for col in range(-1, 6):
                x, y = col * w + off, row * h
                s.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="3"/>'
                         % (x, y, w, h, "#fde68a" if kind == "onion" else "#ecfccb", "#a16207" if kind == "onion" else "#4d7c0f"))
                if kind == "onion":
                    s.append('<ellipse cx="%.1f" cy="%.1f" rx="6" ry="5" fill="#92400e"/>' % (x + 18 + (col * 13 + row * 7) % 30, y + h / 2))
                else:
                    for i in range(7):
                        a, b = (i * 37 + row * 11 + col * 5) % 30, (i * 19 + col * 7) % 22
                        s.append('<ellipse cx="%.1f" cy="%.1f" rx="4" ry="2.6" fill="#16a34a"/>' % (x + 5 + a, y + 6 + b))
    else:
        cells = [(70, 70), (160, 60), (120, 140), (45, 165), (190, 160), (110, 215), (200, 230)]
        for i, (x, y) in enumerate(cells):
            pts = " ".join("%.1f,%.1f" % (x + r * __import__("math").cos(t), y + r * __import__("math").sin(t))
                           for t, r in [(k * 0.785 + i * 0.3, 42 + ((k * 7 + i * 5) % 11)) for k in range(8)])
            s.append('<polygon points="%s" fill="#dbeafe" stroke="#3b82f6" stroke-width="2" stroke-linejoin="round" opacity="0.9"/>' % pts)
            s.append('<circle cx="%d" cy="%d" r="7" fill="#1d4ed8"/>' % (x + 3, y - 2))
    s.append('</g><circle cx="120" cy="120" r="112" fill="none" stroke="#0f172a" stroke-width="6"/></svg>')
    return "".join(s)


# ------------------------------------------------------------------ specialised cells
def red_blood_cell():
    """Surface view and side view, laid out and labelled as in the textbook."""
    F2 = FONT
    return ('<svg viewBox="0 0 560 330" width="520" role="img" aria-label="Red blood cell. Surface view: a round red disc with a darker, thinner centre. Side view: a biconcave shape, thinner in the centre, with cytoplasm containing haemoglobin">'
            '<defs><radialGradient id="rbc" cx="50%%" cy="50%%" r="50%%"><stop offset="0" stop-color="#b91c1c"/><stop offset="0.45" stop-color="#d42a1e"/><stop offset="0.75" stop-color="#ee4b2b"/><stop offset="1" stop-color="#f15a2e"/></radialGradient></defs>'
            '<path d="M220 70 C222 34 262 22 300 26 C342 30 368 50 364 82 C360 112 330 126 292 124 C250 122 218 104 220 70 Z" fill="url(#rbc)" stroke="#7f1d1d" stroke-width="2"/>'
            '<line x1="190" y1="72" x2="286" y2="72" stroke="#1f2937" stroke-width="1.4"/><text x="184" y="56" text-anchor="end" %s>thinner</text><text x="184" y="76" text-anchor="end" %s>central</text><text x="184" y="96" text-anchor="end" %s>portion</text>'
            '<text x="292" y="152" text-anchor="middle" %s>Surface view</text>'
            '<path d="M222 222 C222 204 250 202 270 212 C282 218 290 220 298 220 C306 220 314 218 326 212 C346 202 372 204 372 222 C372 240 346 242 326 232 C314 226 306 224 298 224 C290 224 282 226 270 232 C250 242 222 240 222 222 Z" fill="#e3342f" stroke="#7f1d1d" stroke-width="2"/>'
            '<line x1="190" y1="222" x2="298" y2="222" stroke="#1f2937" stroke-width="1.4"/><text x="184" y="206" text-anchor="end" %s>thinner</text><text x="184" y="226" text-anchor="end" %s>central</text><text x="184" y="246" text-anchor="end" %s>portion</text>'
            '<line x1="352" y1="222" x2="398" y2="222" stroke="#1f2937" stroke-width="1.4"/><text x="404" y="206" %s>cytoplasm</text><text x="404" y="226" %s>containing</text><text x="404" y="246" %s>haemoglobin</text>'
            '<text x="298" y="290" text-anchor="middle" %s>Side view to show</text><text x="298" y="310" text-anchor="middle" %s>its biconcave shape</text>'
            '</svg>') % ((F2,) * 12)


def muscle_cell():
    """A bundle of striated muscle cells with many nuclei and many mitochondria, as drawn in the textbook."""
    s = ['<svg viewBox="0 0 580 250" width="580" role="img" aria-label="Muscle cells: long striped cylinders with many nuclei, many mitochondria and contractile protein fibres">']
    fibres = [(70, 30), (50, 72), (70, 114)]           # (left x, top y) of three overlapping cylinders, back to front
    nuclei = [[(150, 50), (300, 46), (440, 52)], [(120, 92), (250, 96), (400, 90)], [(170, 132), (320, 138), (460, 134)]]
    mitos = [[(220, 44, 20), (370, 50, -15)], [(180, 96, -10), (330, 90, 25), (470, 96, 0)], [(110, 140, 10), (250, 132, -20), (400, 140, 15)]]
    for k, (x0, y0) in enumerate(fibres):
        x1, h = 510, 44
        s.append('<path d="M%d %d H%d a14 %d 0 0 1 0 %d H%d Z" fill="#f4a493" stroke="#7f1d1d" stroke-width="2"/>' % (x0, y0, x1, h / 2, h, x0))
        for x in range(x0 + 16, x1 + 6, 11):
            s.append('<path d="M%d %d q4 %d 0 %d" fill="none" stroke="#b4473a" stroke-width="1.3"/>' % (x, y0 + 2, h / 2, h - 4))
        s.append('<ellipse cx="%d" cy="%d" rx="9" ry="%d" fill="#d9574a" stroke="#7f1d1d" stroke-width="2"/>' % (x0, y0 + h / 2, h / 2))
        for (nx, ny) in nuclei[k]:
            s.append('<ellipse cx="%d" cy="%d" rx="17" ry="6" fill="#e07a68" stroke="#9f3a2c" stroke-width="1.5"/>' % (nx, ny))
        for (mx, my, r) in mitos[k]:
            s.append('<g transform="translate(%d %d) rotate(%d)"><path d="M-8 2 q8 -8 16 -2" fill="none" stroke="#7e3f98" stroke-width="6" stroke-linecap="round"/></g>' % (mx, my, r))
    lab = lambda t, x, pts: (''.join('<line x1="%d" y1="212" x2="%d" y2="%d" stroke="#1f2937" stroke-width="1.4"/><circle cx="%d" cy="%d" r="2.3" fill="#1f2937"/>' % (x, px, py, px, py) for px, py in pts)
                             + '<text x="%d" y="232" text-anchor="middle" %s>%s</text>' % (x, FONT, t))
    s.append(lab("nucleus", 120, [(170, 136)]))
    s.append(lab("mitochondrion", 280, [(250, 134)]))
    s.append(lab("protein fibres", 450, [(422, 150), (478, 152)]))
    s.append("</svg>")
    return "".join(s)


def root_hair_cell():
    """Root hair cell drawn as in the textbook: a cell with a long, narrow extension; the vacuole runs into the extension."""
    outer = "M150 30 Q150 18 162 18 H186 Q198 18 198 30 V96 C290 104 380 76 450 74 C500 72 530 66 556 58 C530 82 492 92 452 98 C380 106 300 124 198 126 V190 Q198 202 186 202 H162 Q150 202 150 190 Z"
    inner = "M162 30 H186 V104 C290 112 380 86 450 84 C486 82 510 78 530 72 C506 84 484 88 452 90 C380 96 300 116 186 118 V190 H162 Z"
    s = ['<svg viewBox="0 0 580 250" width="580" role="img" aria-label="Root hair cell: a cell with a long, narrow extension; the vacuole extends into it and the nucleus is near the base">']
    s.append('<path d="%s" fill="#d6a07a" stroke="#7c4a2a" stroke-width="2"/>' % outer)
    s.append('<path d="%s" fill="#fbe8cc" stroke="#7c4a2a" stroke-width="1.2"/>' % inner)
    s.append('<ellipse cx="156" cy="132" rx="3.5" ry="8" fill="#e11d74"/>')
    s.append('<line x1="176" y1="60" x2="226" y2="34" stroke="#1f2937" stroke-width="1.4"/><circle cx="176" cy="60" r="2.3" fill="#1f2937"/><text x="232" y="38" %s>vacuole</text>' % FONT)
    s.append('<line x1="96" y1="132" x2="154" y2="132" stroke="#1f2937" stroke-width="1.4"/><text x="90" y="137" text-anchor="end" %s>nucleus</text>' % FONT)
    s.append('<path d="M206 150 V158 H556 V150 M381 158 V172" fill="none" stroke="#1f2937" stroke-width="1.4"/><text x="381" y="192" text-anchor="middle" %s>long and narrow extension</text>' % FONT)
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ drag-and-drop labelling targets for the two diagrams
def inner(svg):
    """The inside of an <svg>...</svg> string (for L.labeller)."""
    return svg[svg.index(">") + 1:svg.rindex("</svg>")]


ANIMAL_TARGETS = [
    dict(key="cell-membrane", label="cell membrane", pt=(280, 42), box=(196, 37), side="l"),
    dict(key="chromosome", label="chromosome", pt=(356, 140), box=(196, 135), side="l"),
    dict(key="nuclear-membrane", label="nuclear membrane", pt=(327, 178), box=(196, 173), side="l"),
    dict(key="cytoplasm", label="cytoplasm", pt=(248, 232), box=(196, 227), side="l"),
    dict(key="mitochondrion", label="mitochondrion", pt=(476, 86), box=(548, 85), side="r"),
    dict(key="nucleus", label="nucleus", pt=(416, 146), box=(548, 141), side="r"),
    dict(key="ribosomes", label="ribosome", pt=(470, 218), box=(548, 205), side="r"),
    dict(key="vacuole", label="vacuole", pt=(497, 248), box=(548, 252), side="r"),
]
PLANT_TARGETS = [
    dict(key="cell-membrane", label="cell membrane", pt=(206, 118), box=(170, 113), side="l"),
    dict(key="cytoplasm", label="cytoplasm", pt=(222, 170), box=(170, 165), side="l"),
    dict(key="cell-wall", label="cell wall", pt=(192, 226), box=(170, 221), side="l"),
    dict(key="nuclear-membrane", label="nuclear membrane", pt=(497, 88), box=(420, 22), side="c"),
    dict(key="chromosome", label="chromosome", pt=(530, 94), box=(600, 22), side="c"),
    dict(key="nucleus", label="nucleus", pt=(552, 100), box=(616, 98), side="r"),
    dict(key="ribosomes", label="ribosome", pt=(562, 136), box=(616, 140), side="r"),
    dict(key="mitochondrion", label="mitochondrion", pt=(566, 196), box=(616, 194), side="r"),
    dict(key="vacuole", label="vacuole", pt=(470, 230), box=(616, 234), side="r"),
    dict(key="chloroplast", label="chloroplast", pt=(498, 276), box=(616, 276), side="r"),
]


def photo(img, iw, ih, targets, width=500, margin=180):
    """An image placed between two label margins, for L.labeller. targets use points in the image's own pixels;
    boxes are placed beside the image on the side given, spread out so they do not overlap.
    Returns (svg_inner, vw, vh, targets in viewBox units)."""
    s = width / float(iw)
    vw, vh = width + 2 * margin, ih * s + 20
    out = []
    for side in ("l", "r"):
        ts = sorted([t for t in targets if t["side"] == side], key=lambda t: t["pt"][1])
        last = -99
        for t in ts:
            px, py = margin + t["pt"][0] * s, 10 + t["pt"][1] * s
            by = max(py, last + 44, 22)
            last = by
            out.append(dict(t, pt=(round(px), round(py)), box=(margin - 10 if side == "l" else margin + width + 10, round(by))))
    svg = '<image href="img/%s" x="%d" y="10" width="%d" height="%d"/>' % (img, margin, width, round(ih * s))
    return svg, vw, round(vh), out


def liver_and_root_hair():
    """Fig. for the structured question: A = liver cell, B = root hair cell (not to scale)."""
    s = ['<svg viewBox="0 0 640 250" width="640" role="img" aria-label="A: a liver cell, roughly six-sided, with a central nucleus, many mitochondria and small vacuoles. '
         'B: a root hair cell with a cell wall, a large vacuole and a long, narrow extension.">']
    s.append('<path d="M60 70 L150 40 L240 70 L250 165 L160 205 L70 175 Z" fill="%s" stroke="%s" stroke-width="2.6"/>' % (CYTO, LINE))
    s.append(nucleus_round(155, 122, 27))
    for x, y, r in ((100, 85, 20), (200, 80, -25), (215, 150, 30), (100, 160, -15), (130, 70, 5), (190, 180, 10), (85, 125, 80), (232, 115, 85)):
        s.append(mito(x, y, r, 12, 5.5))
    for x, y in ((120, 100), (195, 125)):
        s.append('<circle cx="%d" cy="%d" r="5" fill="#fff" stroke="%s" stroke-width="1.5"/>' % (x, y, LINE))
    s.append('<text x="155" y="238" text-anchor="middle" %s font-weight="700">A</text>' % FONT)
    s.append('<g transform="translate(196 40) scale(0.72)">'
             '<path d="M150 30 Q150 18 162 18 H186 Q198 18 198 30 V96 C290 104 380 76 450 74 C500 72 530 66 556 58 C530 82 492 92 452 98 C380 106 300 124 198 126 V190 Q198 202 186 202 H162 Q150 202 150 190 Z" fill="#d6a07a" stroke="#7c4a2a" stroke-width="2.5"/>'
             '<path d="M162 30 H186 V104 C290 112 380 86 450 84 C486 82 510 78 530 72 C506 84 484 88 452 90 C380 96 300 116 186 118 V190 H162 Z" fill="#fbe8cc" stroke="#7c4a2a" stroke-width="1.5"/>'
             '<ellipse cx="156" cy="132" rx="3.5" ry="8" fill="#e11d74"/></g>')
    s.append('<text x="460" y="238" text-anchor="middle" %s font-weight="700">B</text>' % FONT)
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ small pictures of specialised cells (lesson 1.2, differentiation)
def mini_rbc():
    s = ['<svg viewBox="0 0 200 150" role="img" aria-label="Red blood cells: red discs, darker and thinner in the middle">'
         '<defs><radialGradient id="mrbc" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#9f1239"/><stop offset="0.5" stop-color="#c81e1e"/><stop offset="1" stop-color="#e11d2e"/></radialGradient></defs>']
    for x, y, rx, ry, r in ((60, 50, 30, 24, -15), (130, 40, 34, 27, 10), (155, 100, 24, 20, 30), (85, 112, 26, 21, -5), (35, 100, 16, 22, 0)):
        s.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" transform="rotate(%d %d %d)" fill="url(#mrbc)" stroke="#7f1d1d" stroke-width="1.5"/>' % (x, y, rx, ry, r, x, y))
        s.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" transform="rotate(%d %d %d)" fill="#7f1d1d" opacity="0.35"/>' % (x, y, rx * 0.45, ry * 0.45, r, x, y))
    s.append('</svg>')
    return "".join(s)


def mini_nerve():
    return ('<svg viewBox="0 0 200 150" role="img" aria-label="Nerve cell: a cell body with a nucleus, many short branches and one long fibre">'
            '<g fill="none" stroke="#e05a6d" stroke-linecap="round">'
            '<path d="M100 60 L72 30 L60 12 M72 30 L52 34 M100 60 L130 26 L138 8 M130 26 L152 22 M88 70 L48 66 L28 56 M48 66 L34 80 M112 70 L150 64 L176 52 M150 64 L168 80" stroke-width="5"/>'
            '<path d="M100 82 C102 104 96 120 100 146 M100 120 L84 140 M101 128 L116 146" stroke-width="6"/></g>'
            '<path d="M76 66 C78 48 122 46 126 64 C130 82 118 92 100 92 C82 92 74 84 76 66 Z" fill="#f4a3ae" stroke="#be3a4d" stroke-width="2"/>'
            '<circle cx="101" cy="70" r="10" fill="#7e3f98" stroke="#4c1d95" stroke-width="1.5"/></svg>')


def mini_intestine():
    s = ['<svg viewBox="0 0 200 150" role="img" aria-label="Intestinal cells: rounded cells side by side, each with a nucleus and tiny finger-like folds on the top surface">']
    for i, x in enumerate((20, 75, 130)):
        for k in range(6):
            fx = x + 6 + k * 8
            s.append('<rect x="%d" y="34" width="5" height="20" rx="2.5" fill="#f59e0b" stroke="#b45309" stroke-width="1"/>' % fx)
        s.append('<path d="M%d 52 H%d Q%d 52 %d 64 V122 Q%d 134 %d 134 H%d Q%d 134 %d 122 V64 Q%d 52 %d 52 Z" fill="#fbbf24" stroke="#b45309" stroke-width="2"/>'
                 % (x + 8, x + 44, x + 52, x + 52, x + 52, x + 40, x + 12, x, x, x, x + 8))
        s.append('<ellipse cx="%d" cy="98" rx="14" ry="12" fill="#c2410c" stroke="#7c2d12" stroke-width="1.5"/>' % (x + 26))
    s.append('</svg>')
    return "".join(s)


def mini_root_hair():
    return ('<svg viewBox="140 10 430 200" role="img" aria-label="Root hair cell: a cell with a long, narrow extension">'
            '<path d="M150 30 Q150 18 162 18 H186 Q198 18 198 30 V96 C290 104 380 76 450 74 C500 72 530 66 556 58 C530 82 492 92 452 98 C380 106 300 124 198 126 V190 Q198 202 186 202 H162 Q150 202 150 190 Z" fill="#d6a07a" stroke="#7c4a2a" stroke-width="3"/>'
            '<path d="M162 30 H186 V104 C290 112 380 86 450 84 C486 82 510 78 530 72 C506 84 484 88 452 90 C380 96 300 116 186 118 V190 H162 Z" fill="#fbe8cc" stroke="#7c4a2a" stroke-width="2"/>'
            '<ellipse cx="156" cy="132" rx="4" ry="9" fill="#e11d74"/></svg>')
