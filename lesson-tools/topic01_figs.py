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


# ------------------------------------------------------------------ typical animal cell
ANIMAL_OUTLINE = "M122 160 C114 98 178 52 255 56 C330 60 382 100 386 160 C390 222 348 272 262 276 C178 280 128 232 122 160 Z"


def animal_cell(labels=True, w=560):
    s = ['<svg viewBox="0 0 560 320" width="%d" role="img" aria-label="Diagram of a typical animal cell">' % w]
    s.append('<g class="part" data-part="cytoplasm"><path d="%s" fill="%s"/></g>' % (ANIMAL_OUTLINE, CYTO))
    s.append('<g class="part" data-part="cell-membrane"><path d="%s" fill="none" stroke="%s" stroke-width="2.6"/>'
             '<path d="%s" fill="none" stroke="transparent" stroke-width="14"/></g>' % (ANIMAL_OUTLINE, LINE, ANIMAL_OUTLINE))
    s.append('<g class="part" data-part="nucleus">%s</g>' % nucleus_round(238, 165, 44))
    s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(318, 112, -20))
    s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(330, 210, 25))
    s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(182, 234, -30))
    for cx, cy, r in ((166, 120, 7), (362, 130, 6), (300, 252, 6), (205, 90, 5), (150, 205, 5)):
        s.append('<g class="part" data-part="vacuole-a"><circle cx="%d" cy="%d" r="%d" fill="#fff" stroke="%s" stroke-width="1.8"/></g>' % (cx, cy, r, LINE))
    s.append('<g class="part" data-part="ribosomes">%s</g>' % ribos([(290, 88), (299, 94), (200, 112), (190, 106), (150, 175), (158, 186), (280, 238), (270, 248),
                                                                       (349, 160), (343, 168), (215, 252), (226, 258), (322, 244), (330, 250), (290, 150)]))
    if labels:
        s.append(lbl("cell-membrane", "cell membrane", 100, 104, 131, 109))
        s.append(lbl("vacuole-a", "vacuole", 100, 146, 160, 123))
        s.append(lbl("cytoplasm", "cytoplasm", 100, 205, 165, 196))
        s.append(lbl("mitochondrion", "mitochondrion", 412, 96, 338, 104, "start"))
        s.append(lbl("nucleus", "nucleus", 412, 172, 282, 167, "start"))
        s.append(lbl("ribosomes", "ribosome", 412, 244, 326, 247, "start"))
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ typical plant cell
VACUOLE_P = ("M196 92 C230 84 262 98 300 90 C326 86 352 92 356 108 C362 132 350 150 358 178 C364 206 354 236 330 240 "
             "C300 246 270 232 240 240 C212 246 190 236 188 212 C186 186 196 170 190 146 C184 120 176 98 196 92 Z")


def plant_cell(labels=True, w=560, sap_text=True):
    s = ['<svg viewBox="0 0 560 320" width="%d" role="img" aria-label="Diagram of a typical plant cell">' % w]
    s.append('<g class="part" data-part="cell-wall"><path fill-rule="evenodd" d="M144 30 h252 a14 14 0 0 1 14 14 v232 a14 14 0 0 1 -14 14 h-252 a14 14 0 0 1 -14 -14 v-232 a14 14 0 0 1 14 -14 Z '
             'M150 42 h240 a8 8 0 0 1 8 8 v220 a8 8 0 0 1 -8 8 h-240 a8 8 0 0 1 -8 -8 v-220 a8 8 0 0 1 8 -8 Z" fill="#b8693f" stroke="%s" stroke-width="2"/></g>' % LINE)
    s.append('<g class="part" data-part="cytoplasm"><rect x="142" y="42" width="256" height="236" rx="8" fill="%s"/></g>' % CYTO)
    s.append('<g class="part" data-part="cell-membrane"><rect x="143.5" y="43.5" width="253" height="233" rx="7" fill="none" stroke="%s" stroke-width="2"/>'
             '<rect x="143.5" y="43.5" width="253" height="233" rx="7" fill="none" stroke="transparent" stroke-width="9"/></g>' % LINE)
    s.append('<g class="part" data-part="vacuole-p"><path d="%s" fill="#fff" stroke="%s" stroke-width="2"/>' % (VACUOLE_P, LINE)
             + ('<text x="273" y="170" text-anchor="middle" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-style="italic" fill="#64748b">cell sap</text>' if sap_text else '') + '</g>')
    s.append('<g class="part" data-part="nucleus"><ellipse cx="164" cy="165" rx="17" ry="30" fill="#ebe3f6" stroke="%s" stroke-width="2.2"/>'
             '<path d="M156 150 q4 -6 8 0 t8 0 M154 168 q4 6 8 0 t8 0 M160 182 q3 -5 6 0" fill="none" stroke="#db2777" stroke-width="1.4"/>'
             '<ellipse cx="166" cy="160" rx="5" ry="4" fill="#1f5fa8"/></g>' % LINE)
    for x, y, r in ((210, 63, 0), (268, 61, 0), (326, 63, 0), (379, 120, 90), (379, 215, 90), (232, 262, 0), (300, 262, 0), (164, 98, 90), (164, 232, 90)):
        s.append('<g class="part" data-part="chloroplast">%s</g>' % chloro(x, y, r))
    s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(378, 260, -40, 11, 6))
    s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(199, 261, 10, 11, 6))
    s.append('<g class="part" data-part="ribosomes">%s</g>' % ribos([(240, 76), (247, 80), (297, 77), (366, 88), (372, 92), (265, 252), (156, 124), (153, 204),
                                                                       (345, 252), (368, 238), (375, 242), (180, 60)]))
    if labels:
        s.append(lbl("cell-wall", "cell wall", 108, 64, 136, 70))
        s.append(lbl("nucleus", "nucleus", 108, 170, 148, 165))
        s.append(lbl("cell-membrane", "cell membrane", 108, 270, 143, 262))
        s.append(lbl("cytoplasm", "cytoplasm", 428, 72, 352, 74, "start"))
        s.append(lbl("chloroplast", "chloroplast", 428, 124, 387, 120, "start"))
        s.append(lbl("vacuole-p", "vacuole", 428, 170, 345, 165, "start"))
        s.append(lbl("ribosomes", "ribosome", 428, 238, 375, 240, "start"))
        s.append(lbl("mitochondrion", "mitochondrion", 428, 280, 386, 263, "start"))
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
    dict(key="cell-membrane", label="cell membrane", pt=(131, 109), box=(100, 96), side="l"),
    dict(key="vacuole", label="vacuole", pt=(160, 123), box=(100, 150), side="l"),
    dict(key="cytoplasm", label="cytoplasm", pt=(165, 196), box=(100, 205), side="l"),
    dict(key="mitochondrion", label="mitochondrion", pt=(338, 104), box=(412, 96), side="r"),
    dict(key="nucleus", label="nucleus", pt=(282, 167), box=(412, 168), side="r"),
    dict(key="ribosomes", label="ribosomes", pt=(326, 247), box=(412, 244), side="r"),
]
PLANT_TARGETS = [
    dict(key="cell-wall", label="cell wall", pt=(136, 70), box=(108, 62), side="l"),
    dict(key="nucleus", label="nucleus", pt=(148, 165), box=(108, 165), side="l"),
    dict(key="cell-membrane", label="cell membrane", pt=(143, 262), box=(108, 268), side="l"),
    dict(key="cytoplasm", label="cytoplasm", pt=(352, 74), box=(428, 62), side="r"),
    dict(key="chloroplast", label="chloroplast", pt=(387, 120), box=(428, 112), side="r"),
    dict(key="vacuole", label="vacuole", pt=(345, 165), box=(428, 165), side="r"),
    dict(key="ribosomes", label="ribosomes", pt=(375, 240), box=(428, 222), side="r"),
    dict(key="mitochondrion", label="mitochondrion", pt=(386, 263), box=(428, 280), side="r"),
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
