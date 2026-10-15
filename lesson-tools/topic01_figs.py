"""SVG drawings for Topic 1 (Cell Structure and Organisation). Used by build_topic01.py.
Every clickable part is wrapped in <g class="part" data-part="key"> and every label in <g class="lbl" data-part="key">."""

FONT = 'font-family="Source Sans 3, system-ui, sans-serif" font-size="16" fill="#1f2937"'


def lbl(key, text, tx, ty, x2, y2, anchor="end"):
    """A label with a leader line from the text to the point (x2, y2)."""
    x1 = tx + (6 if anchor == "end" else -6)
    return ('<g class="lbl" data-part="%s"><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#334155" stroke-width="1.4"/>'
            '<circle cx="%d" cy="%d" r="2.4" fill="#334155"/><text x="%d" y="%d" text-anchor="%s" %s>%s</text></g>'
            % (key, x1, ty - 5, x2, y2, x2, y2, tx, ty, anchor, FONT, text))


def mito(x, y, rot, rx=24, ry=11):
    s = rx / 24.0
    return ('<g transform="translate(%s %s) rotate(%s)"><ellipse rx="%s" ry="%s" fill="#fed7aa" stroke="#c2410c" stroke-width="2.4"/>'
            '<path d="M%s 0 l%s -%s l%s %s l%s -%s l%s %s l%s -%s l%s %s" fill="none" stroke="#c2410c" stroke-width="1.5" stroke-linejoin="round"/></g>'
            % (x, y, rot, rx, ry, -15 * s, 5 * s, ry * 0.55, 5 * s, ry * 1.1, 5 * s, ry * 1.1, 5 * s, ry * 1.1, 5 * s, ry * 1.1, 5 * s, ry * 0.55))


def chloro(x, y, rot):
    return ('<g transform="translate(%s %s) rotate(%s)"><ellipse rx="15" ry="7.5" fill="#4ade80" stroke="#15803d" stroke-width="2"/>'
            '<path d="M-8 -3v6M-3 -4v8M2 -4v8M7 -3v6" stroke="#166534" stroke-width="1.6"/></g>' % (x, y, rot))


def ribos(pts):
    return "".join('<circle cx="%d" cy="%d" r="2.3" fill="#1e293b"/>' % p for p in pts)


# ------------------------------------------------------------------ typical animal cell
ANIMAL_OUTLINE = "M122 160 C114 98 178 52 255 56 C330 60 382 100 386 160 C390 222 348 272 262 276 C178 280 128 232 122 160 Z"


def animal_cell(labels=True, w=560):
    s = ['<svg viewBox="0 0 560 320" width="%d" role="img" aria-label="Diagram of a typical animal cell">' % w]
    s.append('<g class="part" data-part="cytoplasm"><path d="%s" fill="#fde7ef"/></g>' % ANIMAL_OUTLINE)
    s.append('<g class="part" data-part="cell-membrane"><path d="%s" fill="none" stroke="#be185d" stroke-width="4"/>'
             '<path d="%s" fill="none" stroke="transparent" stroke-width="14"/></g>' % (ANIMAL_OUTLINE, ANIMAL_OUTLINE))
    s.append('<g class="part" data-part="nucleus"><circle cx="238" cy="165" r="44" fill="#ede9fe" stroke="#6d28d9" stroke-width="3"/>'
             '<path d="M210 150 q8 -10 16 0 t16 0M214 182 q8 8 16 0 t16 2M256 176 q6 -8 10 2" fill="none" stroke="#a78bfa" stroke-width="2"/>'
             '<circle cx="250" cy="155" r="11" fill="#8b5cf6"/></g>')
    s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(318, 112, -20))
    s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(330, 210, 25))
    s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(182, 234, -30))
    for cx, cy, r in ((168, 118, 11), (362, 130, 8), (300, 252, 9)):
        s.append('<g class="part" data-part="vacuole-a"><circle cx="%d" cy="%d" r="%d" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/></g>' % (cx, cy, r))
    s.append('<g class="part" data-part="ribosomes">%s</g>' % ribos([(290, 88), (299, 94), (200, 92), (190, 86), (150, 175), (158, 186), (280, 238), (270, 248),
                                                                       (349, 160), (343, 168), (215, 252), (226, 258), (322, 244), (330, 250), (290, 150)]))
    if labels:
        s.append(lbl("cell-membrane", "cell membrane", 100, 104, 131, 109))
        s.append(lbl("vacuole-a", "small vacuole", 100, 146, 158, 123))
        s.append(lbl("cytoplasm", "cytoplasm", 100, 205, 165, 196))
        s.append(lbl("mitochondrion", "mitochondrion", 412, 96, 340, 104, "start"))
        s.append(lbl("nucleus", "nucleus", 412, 172, 282, 167, "start"))
        s.append(lbl("ribosomes", "ribosomes", 412, 244, 326, 247, "start"))
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ typical plant cell
def plant_cell(labels=True, w=560, sap_text=True):
    s = ['<svg viewBox="0 0 560 320" width="%d" role="img" aria-label="Diagram of a typical plant cell">' % w]
    s.append('<g class="part" data-part="cell-wall"><path fill-rule="evenodd" d="M144 30 h252 a14 14 0 0 1 14 14 v232 a14 14 0 0 1 -14 14 h-252 a14 14 0 0 1 -14 -14 v-232 a14 14 0 0 1 14 -14 Z '
             'M150 42 h240 a8 8 0 0 1 8 8 v220 a8 8 0 0 1 -8 8 h-240 a8 8 0 0 1 -8 -8 v-220 a8 8 0 0 1 8 -8 Z" fill="#d9f99d" stroke="#3f6212" stroke-width="2"/></g>')
    s.append('<g class="part" data-part="cytoplasm"><rect x="142" y="42" width="256" height="236" rx="8" fill="#f7fee7"/></g>')
    s.append('<g class="part" data-part="cell-membrane"><rect x="143.5" y="43.5" width="253" height="233" rx="7" fill="none" stroke="#be185d" stroke-width="2.6"/>'
             '<rect x="143.5" y="43.5" width="253" height="233" rx="7" fill="none" stroke="transparent" stroke-width="9"/></g>')
    s.append('<g class="part" data-part="vacuole-p"><rect x="186" y="86" width="174" height="158" rx="30" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>'
             + ('<text x="273" y="170" text-anchor="middle" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-style="italic" fill="#1e40af">cell sap</text>' if sap_text else '') + '</g>')
    s.append('<g class="part" data-part="nucleus"><ellipse cx="164" cy="165" rx="16" ry="30" fill="#ede9fe" stroke="#6d28d9" stroke-width="2.6"/><circle cx="166" cy="160" r="6" fill="#8b5cf6"/></g>')
    for x, y, r in ((210, 63, 0), (268, 61, 0), (326, 63, 0), (379, 120, 90), (379, 215, 90), (232, 262, 0), (300, 262, 0), (164, 98, 90), (164, 232, 90)):
        s.append('<g class="part" data-part="chloroplast">%s</g>' % chloro(x, y, r))
    s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(378, 260, -40, 11, 5.5))
    s.append('<g class="part" data-part="mitochondrion">%s</g>' % mito(199, 261, 10, 11, 5.5))
    s.append('<g class="part" data-part="ribosomes">%s</g>' % ribos([(240, 74), (247, 79), (297, 76), (366, 88), (372, 92), (265, 250), (156, 124), (153, 204),
                                                                       (345, 252), (368, 238), (375, 242), (180, 60)]))
    if labels:
        s.append(lbl("cell-wall", "cell wall", 108, 64, 136, 70))
        s.append(lbl("nucleus", "nucleus", 108, 170, 148, 165))
        s.append(lbl("cell-membrane", "cell membrane", 108, 270, 143, 262))
        s.append(lbl("cytoplasm", "cytoplasm", 428, 72, 352, 74, "start"))
        s.append(lbl("chloroplast", "chloroplast", 428, 124, 387, 120, "start"))
        s.append(lbl("vacuole-p", "vacuole (cell sap)", 428, 170, 345, 165, "start"))
        s.append(lbl("ribosomes", "ribosomes", 428, 238, 375, 240, "start"))
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
    return ('<svg viewBox="0 0 560 250" width="560" role="img" aria-label="Red blood cell: surface view showing a disc with a paler centre, and side view showing a biconcave shape that is thinner in the middle">'
            '<defs><radialGradient id="rbc" cx="50%%" cy="50%%" r="50%%"><stop offset="0" stop-color="#fca5a5"/><stop offset="0.45" stop-color="#f87171"/><stop offset="1" stop-color="#b91c1c"/></radialGradient></defs>'
            '<circle cx="130" cy="125" r="72" fill="url(#rbc)" stroke="#991b1b" stroke-width="2.5"/>'
            '<line x1="130" y1="38" x2="130" y2="105" stroke="#334155" stroke-width="1.4"/><text x="130" y="30" text-anchor="middle" %s>no nucleus; full of haemoglobin</text>'
            '<text x="130" y="232" text-anchor="middle" %s font-weight="700">surface view</text>'
            '<g transform="translate(400 125)"><path d="M-95 0 C-95 -38 -58 -34 -32 -16 C-14 -5 14 -5 32 -16 C58 -34 95 -38 95 0 C95 38 58 34 32 16 C14 5 -14 5 -32 16 C-58 34 -95 38 -95 0 Z" fill="#ef4444" stroke="#991b1b" stroke-width="2.5"/></g>'
            '<line x1="400" y1="62" x2="400" y2="118" stroke="#334155" stroke-width="1.4"/><text x="400" y="54" text-anchor="middle" %s>thin centre</text>'
            '<line x1="318" y1="178" x2="330" y2="150" stroke="#334155" stroke-width="1.4"/><text x="318" y="194" text-anchor="middle" %s>thicker edge</text>'
            '<text x="400" y="232" text-anchor="middle" %s font-weight="700">side view (cut through): biconcave disc</text>'
            '</svg>') % ((FONT,) * 5)


def muscle_cell():
    s = ['<svg viewBox="0 0 580 210" width="580" role="img" aria-label="Muscle cell: a long cell with many nuclei, many mitochondria and long protein fibres">']
    s.append('<rect x="30" y="60" width="520" height="90" rx="40" fill="#fecdd3" stroke="#be123c" stroke-width="2.5"/>')
    for y in range(72, 142, 9):
        s.append('<line x1="62" y1="%d" x2="518" y2="%d" stroke="#fb7185" stroke-width="2"/>' % (y, y))
    for x in (110, 250, 390, 500):
        s.append('<ellipse cx="%d" cy="70" rx="20" ry="7" fill="#7c3aed" stroke="#4c1d95" stroke-width="1.5"/>' % x)
    for i, x in enumerate(range(80, 520, 42)):
        s.append(mito(x, 128 if i % 2 else 100, 0, 12, 5.5))
    s.append('<line x1="250" y1="30" x2="250" y2="63" stroke="#334155" stroke-width="1.4"/><text x="250" y="24" text-anchor="middle" %s>many nuclei</text>' % FONT)
    s.append('<line x1="416" y1="185" x2="376" y2="131" stroke="#334155" stroke-width="1.4"/><circle cx="376" cy="131" r="2.4" fill="#334155"/>'
             '<line x1="424" y1="185" x2="456" y2="131" stroke="#334155" stroke-width="1.4"/><circle cx="456" cy="131" r="2.4" fill="#334155"/>'
             '<text x="420" y="202" text-anchor="middle" %s>many mitochondria</text>' % FONT)
    s.append('<line x1="150" y1="185" x2="160" y2="117" stroke="#334155" stroke-width="1.4"/><text x="150" y="202" text-anchor="middle" %s>protein fibres (contract)</text>' % FONT)
    s.append("</svg>")
    return "".join(s)


def root_hair_cell():
    s = ['<svg viewBox="0 -6 580 286" width="580" role="img" aria-label="Root hair cell: a cell with a long, narrow extension growing out between soil particles; water and mineral salts enter the root hair">']
    s.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#0284c7"/></marker></defs>')
    s.append('<rect x="0" y="-6" width="242" height="286" fill="#f1f5f9"/><rect x="242" y="-6" width="338" height="286" fill="#fefce8"/>')
    for x, y, r in ((300, 34, 16), (380, 34, 18), (470, 32, 18), (560, 74, 17), (330, 125, 22), (430, 130, 24), (520, 130, 20), (270, 235, 18), (380, 200, 22), (560, 205, 16)):
        s.append('<circle cx="%d" cy="%d" r="%d" fill="#d6b88b" stroke="#a16207" stroke-width="1.5"/>' % (x, y, r))
    s.append('<path d="M50 105 H195 Q205 62 262 58 H520 a16 16 0 0 1 0 32 H268 Q236 92 236 125 V178 a12 12 0 0 1 -12 12 H50 a12 12 0 0 1 -12 -12 V117 a12 12 0 0 1 12 -12 Z" '
             'fill="#fef3c7" stroke="#a16207" stroke-width="2.5"/>')
    s.append('<rect x="58" y="120" width="160" height="56" rx="16" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>')
    s.append('<ellipse cx="300" cy="74" rx="15" ry="8" fill="#ede9fe" stroke="#6d28d9" stroke-width="2"/>')
    for x in (340, 425, 515):
        s.append('<path d="M%d 22 V48" stroke="#0284c7" stroke-width="3" marker-end="url(#ar)"/>' % x)
    s.append('<text x="425" y="8" text-anchor="middle" font-family="Source Sans 3, system-ui, sans-serif" font-size="14" font-weight="700" fill="#0369a1">water and mineral salts</text>')
    s.append('<line x1="138" y1="160" x2="138" y2="226" stroke="#334155" stroke-width="1.4"/><text x="138" y="242" text-anchor="middle" %s>vacuole (cell sap)</text>' % FONT)
    s.append('<line x1="300" y1="82" x2="300" y2="168" stroke="#334155" stroke-width="1.4"/><text x="300" y="184" text-anchor="middle" %s>nucleus</text>' % FONT)
    s.append('<line x1="470" y1="90" x2="470" y2="236" stroke="#334155" stroke-width="1.4"/><text x="575" y="252" text-anchor="end" %s>long, narrow extension (root hair)</text>' % FONT)
    s.append('<text x="16" y="30" %s font-weight="700">inside the root</text><text x="252" y="272" %s font-weight="700">soil</text>' % (FONT, FONT))
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ drag-and-drop labelling targets for the two diagrams
def inner(svg):
    """The inside of an <svg>...</svg> string (for L.labeller)."""
    return svg[svg.index(">") + 1:svg.rindex("</svg>")]


ANIMAL_TARGETS = [
    dict(key="cell-membrane", label="cell membrane", pt=(131, 109), box=(100, 96), side="l"),
    dict(key="vacuole", label="vacuole", pt=(158, 123), box=(100, 150), side="l"),
    dict(key="cytoplasm", label="cytoplasm", pt=(165, 196), box=(100, 205), side="l"),
    dict(key="mitochondrion", label="mitochondrion", pt=(340, 104), box=(412, 96), side="r"),
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
    s.append('<path d="M60 70 L150 40 L240 70 L250 165 L160 205 L70 175 Z" fill="#fde7ef" stroke="#be185d" stroke-width="3"/>')
    s.append('<circle cx="155" cy="122" r="27" fill="#ede9fe" stroke="#6d28d9" stroke-width="2.5"/><circle cx="160" cy="116" r="7" fill="#8b5cf6"/>')
    for x, y, r in ((100, 85, 20), (200, 80, -25), (215, 150, 30), (100, 160, -15), (130, 70, 5), (190, 180, 10), (85, 125, 80), (232, 115, 85)):
        s.append(mito(x, y, r, 12, 5.5))
    for x, y in ((120, 100), (195, 125)):
        s.append('<circle cx="%d" cy="%d" r="5" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>' % (x, y))
    s.append('<text x="155" y="238" text-anchor="middle" %s font-weight="700">A</text>' % FONT)
    s.append('<g transform="translate(300 40)">'
             '<path d="M10 60 H130 Q140 30 180 28 H320 a12 12 0 0 1 0 24 H184 Q160 54 160 80 V140 a10 10 0 0 1 -10 10 H10 a10 10 0 0 1 -10 -10 V70 a10 10 0 0 1 10 -10 Z" fill="#fef3c7" stroke="#a16207" stroke-width="5"/>'
             '<path d="M10 60 H130 Q140 30 180 28 H320 a12 12 0 0 1 0 24 H184 Q160 54 160 80 V140 a10 10 0 0 1 -10 10 H10 a10 10 0 0 1 -10 -10 V70 a10 10 0 0 1 10 -10 Z" fill="none" stroke="#fde68a" stroke-width="1.5"/>'
             '<rect x="18" y="74" width="126" height="62" rx="14" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>'
             '<ellipse cx="200" cy="40" rx="12" ry="7" fill="#ede9fe" stroke="#6d28d9" stroke-width="2"/></g>')
    s.append('<text x="460" y="238" text-anchor="middle" %s font-weight="700">B</text>' % FONT)
    s.append("</svg>")
    return "".join(s)
