#!/usr/bin/env python3
"""Topic 1: Cell Structure and Organisation (G2 and G3, syllabus refs 1a-1d). First drafts of the two lessons (numbered as in the textbook: 1.1 and 1.2).
Run: python3 build_topic01.py && python3 add_navigation.py
Once a lesson has been edited by hand, do not run this script over it again (comment out its build call below)."""
import lesson_kit as L
import topic01_figs as F

TOPIC = "Cell Structure and Organisation"
REFS = "Syllabus refs (G2 &amp; G3): "
JS = L.EXPLORER_JS + L.SORT_JS + L.LABEL_JS


LO11 = '''<div class="practical"><h3>Learning outcomes</h3><ul>
<li>Identify and state the functions of the cell structures (including organelles) of typical plant and animal cells from diagrams, light micrographs and as seen under the light microscope using prepared slides and fresh material treated with an appropriate temporary staining technique: cell wall, cell membrane, cytoplasm, nucleus, cell vacuoles (large, sap-filled in plant cells; small, temporary in animal cells), chloroplasts.</li>
<li>Identify and state the functions of the following organelles from diagrams and electron micrographs: mitochondria, ribosomes.</li>
<li>Compare the structure of typical animal and plant cells.</li></ul></div>
'''
LO12 = '''<div class="practical"><h3>Learning outcome</h3><ul>
<li>Explain how the structures of specialised cells are adapted to their functions (e.g. muscle cell: many mitochondria to supply more energy; root hair cell: large surface area of cell membrane for greater absorption; red blood cell: lack of nucleus allowing it to transport more oxygen).</li></ul></div>
'''


C = "https://commons.wikimedia.org/wiki/File:"


def MICROGRAPHS():
    """Drag-and-drop labelling of real light and electron micrographs (Wikimedia Commons, credited)."""
    def one(lid, img, iw, ih, targets, title, caption, credit):
        svg, vw, vh, ts = F.photo(img, iw, ih, targets)
        return L.labeller(lid, svg, vw, vh, ts, caption, title=title, width=760) + '<p class="credit">%s</p>\n' % credit
    b = '<h2>Label real cells: light micrographs</h2>\n'
    b += ('<p>These are real photos taken through a light microscope. Real cells look less tidy than diagrams. '
          'Use what you know: a <strong>cell wall</strong> gives plant cells a fixed, box-like shape; a stained <strong>nucleus</strong> shows up as a dark spot; <strong>chloroplasts</strong> are green.</p>\n')
    b += one("lab-cheek", "cheek-cells-lm.jpg", 800, 828, [
        dict(key="nucleus", label="nucleus", pt=(257, 377), side="r"),
        dict(key="membrane", label="cell membrane", pt=(164, 392), side="l"),
        dict(key="cytoplasm", label="cytoplasm", pt=(192, 142), side="l")],
        "Human cheek cells (animal cells)", "Human cheek cells stained with methylene blue, light microscope.",
        'Photo: <a href="%sHuman_Cheek_Cells_(Methylene_Blue_Stain).jpg">Fritzmann2002</a>, CC BY-SA 4.0, via Wikimedia Commons.' % C)
    b += one("lab-onion", "onion-cells-lm.jpg", 650, 700, [
        dict(key="nucleus", label="nucleus", pt=(206, 411), side="l"),
        dict(key="wall", label="cell wall", pt=(210, 457), side="l"),
        dict(key="vacuole", label="vacuole", pt=(330, 445), side="r")],
        "Onion epidermis cells (plant cells)", "Onion epidermal cells, stained, light microscope. Notice: no chloroplasts.",
        'Photo: <a href="%sOnion_skin_cells_under_a_microscope.jpg">Katekor1</a>, CC BY 4.0, via Wikimedia Commons.' % C)
    b += one("lab-moss", "moss-leaf-cells-lm.jpg", 800, 510, [
        dict(key="chloroplast", label="chloroplast", pt=(192, 117), side="l"),
        dict(key="wall", label="cell wall", pt=(333, 238), side="r")],
        "Moss leaf cells (plant cells)", "Leaf cells of a moss, light microscope (no stain needed).",
        'Photo: <a href="%sBryum_capillare_leaf_cells_showing_chloroplasts.jpg">Des_Callaghan</a>, CC BY-SA 4.0, via Wikimedia Commons.' % C)
    b += '<h2>Label real cells: electron micrographs</h2>\n'
    b += ('<p>An electron microscope shows much more detail, so you can see the small organelles. Electron micrographs are black and white; '
          'colour is sometimes added afterwards to make parts easier to see.</p>\n')
    b += one("lab-liver", "liver-cell-em.jpg", 800, 712, [
        dict(key="nucleus", label="nucleus", pt=(38, 267), side="l"),
        dict(key="ribosomes", label="ribosomes", pt=(275, 525), side="l"),
        dict(key="cytoplasm", label="cytoplasm", pt=(500, 117), side="r"),
        dict(key="mitochondrion", label="mitochondrion", pt=(583, 254), side="r")],
        "Part of a liver cell (animal cell)", "Part of a liver cell, electron micrograph. The nucleus (purple) and mitochondria (green) have been coloured. The tiny dark dots are ribosomes.",
        'Image (cropped): <a href="%sHepatocito_TEM.png">Bochimoto H, Matsuno N, Ishihara Y et al.</a>, CC BY 4.0, via Wikimedia Commons.' % C)
    b += one("lab-leaf", "leaf-cell-em.jpg", 800, 607, [
        dict(key="wall", label="cell wall", pt=(208, 250), side="l"),
        dict(key="chloroplast", label="chloroplast", pt=(458, 275), side="r"),
        dict(key="vacuole", label="vacuole", pt=(583, 500), side="r")],
        "Part of a leaf cell (plant cell)", "Part of a leaf cell, electron micrograph (about 12 000 times bigger than life). The lines inside the chloroplast are where light is absorbed.",
        'Image: <a href="%sChloroplast_in_leaf_of_Anemone_sp_TEM_12000x.png">and3k and caper437</a>, CC BY-SA 3.0, via Wikimedia Commons.' % C)

    b += '<h2>Spotting mitochondria and chloroplasts</h2>\n'
    b += ('<p>In the exam you may be shown an electron micrograph and asked to name the organelle. These two are the ones to know well. '
          'They look quite different once you know what to look for.</p>\n')
    pic = lambda f, alt, cap: '<figure class="pic"><img src="img/%s" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>' % (f, alt, cap)
    b += ('<h3>Mitochondria</h3>\n<div class="two-col">%s%s</div>\n'
          % (pic("mitochondrion-round-em.jpg", "A whole round mitochondrion with a smooth double membrane and folds inside", "One whole mitochondrion cut across."),
             pic("mitochondrion-whole-em.jpg", "A whole, long, sausage-shaped mitochondrion with a smooth double membrane and many folds running across it", "One whole mitochondrion cut along its length.")))
    b += ('<ul class="spot"><li><strong>Shape:</strong> small ovals or sausages (often round when cut across).</li>'
          '<li><strong>Edge:</strong> a smooth double membrane.</li>'
          '<li><strong>Inside:</strong> many folds of the inner membrane, like shelves or fingers. The folds give a large surface for aerobic respiration.</li>'
          '<li><strong>Where:</strong> in the cytoplasm of almost every plant and animal cell. Very active cells (muscle, liver) have lots.</li></ul>\n')
    b += ('<p class="credit">Images: <a href="%sMitochondria,_mammalian_lung_-_TEM.jpg">Louisa Howard, Dartmouth Electron Microscope Facility</a> (public domain, via Wikimedia Commons); '
          '<a href="https://wellcomecollection.org/works/hd9jkrsj">Prof. R. Bellairs</a>, CC BY 4.0, Wellcome Collection.</p>\n' % C)
    b += ('<h3>Chloroplasts</h3>\n<div class="two-col">%s%s</div>\n'
          % (pic("chloroplast-whole-em.jpg", "A whole, lens-shaped chloroplast in a bean leaf cell, with long parallel membranes and dark stacks inside", "A whole chloroplast in a bean leaf cell (colour added)."),
             pic("leaf-cell-em.jpg", "A whole, lens-shaped chloroplast lying against the cell wall, with dark stacks of membranes inside", "A whole chloroplast in a leaf cell, lying against the cell wall.")))
    b += ('<ul class="spot"><li><strong>Shape:</strong> a large lens or oval, much bigger than a mitochondrion.</li>'
          '<li><strong>Inside:</strong> long, parallel membranes with dark <strong>stacks</strong> (like piles of coins). Chlorophyll is in these membranes, where light is absorbed.</li>'
          '<li><strong>Where:</strong> only in some plant cells (e.g. leaf cells), usually near the cell wall.</li></ul>\n')
    b += ('<p class="credit">Images: <a href="https://wellcomecollection.org/works/bx3dctp2">Kevin Mackenzie, University of Aberdeen</a>, CC BY 4.0, Wellcome Collection (cropped); '
          '<a href="%sChloroplast_in_leaf_of_Anemone_sp_TEM_12000x.png">and3k and caper437</a>, CC BY-SA 3.0, via Wikimedia Commons.</p>\n' % C)
    b += ('<table><tr><th>Look for&hellip;</th><th>Mitochondrion</th><th>Chloroplast</th></tr>'
          '<tr><td>Size</td><td>small</td><td>large (several times longer)</td></tr>'
          '<tr><td>Membranes inside</td><td>folds that stick in from the edge</td><td>long parallel membranes with dark stacks</td></tr>'
          '<tr><td>Found in</td><td>plant and animal cells</td><td>some plant cells only</td></tr>'
          '<tr><td>Job</td><td>aerobic respiration</td><td>photosynthesis</td></tr></table>\n')
    b += '<h3>Spot the organelle</h3>\n'
    b += L.mcq("A", "This electron micrograph shows part of an animal cell. Name the organelle labelled X. (There are many more of them in this cell.)", ["Nucleus", "Mitochondrion", "Chloroplast", "Vacuole"], 1,
               "Sausage-shaped, with a smooth double membrane and folds inside: a mitochondrion. This cell has many, so it is very active. The large dark structure on the left is the nucleus.",
               img=("q-mito-em", "An electron micrograph of part of an animal cell with many sausage-shaped organelles; an arrow labelled X points to one of them"))
    b += L.mcq("B", "Name the organelle in this electron micrograph.", ["Mitochondrion", "Vacuole", "Nucleus", "Chloroplast"], 3,
               "A large lens shape with long parallel membranes and dark stacks inside: a chloroplast.", img=("leaf-cell-em", "An electron micrograph of a whole large lens-shaped organelle with stacks of membranes, next to a cell wall"))
    b += L.mcq("C", "A student finds an organelle with stacks of membranes in an electron micrograph of a cell. What can the student conclude?", [
        "The cell is an animal cell.", "The cell is a plant cell, such as a leaf cell.", "The cell has no nucleus.", "The cell is a red blood cell."], 1,
        "Stacks of membranes mean a chloroplast, and only (some) plant cells have chloroplasts.")
    b += ('<p class="credit">Question A image: <a href="https://wellcomecollection.org/works/ku2hehbr">Dr Jeremy Skepper</a>, CC BY 4.0, Wellcome Collection (arrow added). '
          'Question B image: credited above.</p>\n')
    return b


# ================================================================== Lesson 1.1 What Are Cells? (1a, 1b, 1c)
def lesson1():
    b = LO11
    b += '<h2>Trigger activity</h2>\n'
    b += ('<p>Watch this real video taken through a microscope. A <em>Paramecium</em> is a living thing made of just <strong>one cell</strong>. '
          'As you watch, think: <strong>how can one tiny cell move, feed and stay alive on its own?</strong> What parts must it have?</p>\n')
    b += L.video("a4aZE5FQ284", "Paramecium feeding, seen under a microscope", "YouTube: Craig Smith")
    b += '<h2>What is a cell?</h2>\n'
    b += ('<p>Every living thing is made of <strong>cells</strong>, just as a building is made of bricks. Cells are the <strong>building blocks of life</strong>: the simplest structural and functional units of life. '
          'Some organisms, such as bacteria, are a single cell. You are made of about 30 trillion cells.</p>\n'
          '<p>Inside a cell there are smaller structures with special jobs, called <strong>organelles</strong> (&ldquo;little organs&rdquo;). The nucleus, mitochondria and chloroplasts are organelles.</p>\n')
    b += ('<p>All the living material of a cell is called <strong>protoplasm</strong>. It is made up of three key parts:</p>\n'
          '<div class="flow" aria-label="Parts of protoplasm"><span>cell membrane</span><b>+</b><span>cytoplasm</span><b>+</b><span>nucleus</span></div>\n')
    b += '<p class="keyidea"><strong>Key idea:</strong> structure is linked to function. Each part of a cell has a shape and make-up that suits its job.</p>\n'
    b += ('<p>In a large organism, cells are organised in levels. Similar cells work together as a <strong>tissue</strong>, tissues form an <strong>organ</strong>, '
          'organs work together in an <strong>organ system</strong>, and the systems make up the whole <strong>organism</strong>.</p>\n'
          '<div class="flow" aria-label="Levels of organisation"><span>cell</span><b>&rarr;</b><span>tissue</span><b>&rarr;</b><span>organ</span><b>&rarr;</b><span>organ system</span><b>&rarr;</b><span>organism</span></div>\n'
          '<p>For example: a muscle cell &rarr; muscle tissue &rarr; the heart &rarr; the circulatory system &rarr; you.</p>\n')

    b += '<h2>Seeing cells: light and electron microscopes</h2>\n'
    b += ('<p>Cells are too small to see with the naked eye, so we use microscopes. A photo taken through a microscope is called a <strong>micrograph</strong>.</p>\n'
          '<div class="two-col scopes">'
          '<figure class="pic"><img src="img/light-microscope.jpg" alt="A light microscope on a lab bench, with eyepieces, objective lenses, a stage and a lamp" loading="lazy">'
          '<figcaption><strong>Light microscope</strong>: the kind in your school lab. Light passes through a thin specimen.</figcaption></figure>'
          '<figure class="pic"><img src="img/electron-microscope.jpg" alt="A transmission electron microscope: a tall grey column about two metres high, with controls and a computer screen" loading="lazy">'
          '<figcaption><strong>Electron microscope</strong>: a large machine in a research lab. A beam of electrons passes through the specimen.</figcaption></figure></div>\n'
          '<p class="credit">Photos: <a href="https://commons.wikimedia.org/wiki/File:Optical_microscope_nikon_alphaphot.jpg">GcG (public domain, numbers removed)</a>; '
          '<a href="https://commons.wikimedia.org/wiki/File:Transmission_electron_microscope_(1).jpg">Gannu03, CC BY-SA 4.0</a>, via Wikimedia Commons.</p>\n'
          '<table><tr><th></th><th>Light microscope</th><th>Electron microscope</th></tr>'
          '<tr><td>Uses</td><td>light</td><td>a beam of electrons</td></tr>'
          '<tr><td>Picture</td><td>light micrograph</td><td>electron micrograph</td></tr>'
          '<tr><td>Where you meet it</td><td>the school lab</td><td>research labs (you will see its pictures)</td></tr>'
          '<tr><td>Structures you can see</td><td>cell wall, cell membrane, cytoplasm, nucleus, vacuole, chloroplasts</td><td>all of these <strong>plus</strong> the small organelles: <strong>mitochondria</strong> and <strong>ribosomes</strong></td></tr></table>\n')
    b += '<p class="common"><strong>Remember:</strong> mitochondria and ribosomes are too small to see clearly with a school light microscope. You identify them from diagrams and electron micrographs.</p>\n'
    b += ('<div class="practical"><h3>Practical: making a temporary slide of onion cells</h3><ol>'
          '<li>Peel a thin, see-through layer (the epidermis) from the inside of a piece of onion.</li>'
          '<li>Lay it flat in a drop of water on a clean glass slide. Use a mounting needle so it does not fold.</li>'
          '<li>Add a drop of <strong>iodine solution</strong>. The stain makes the nucleus and cell wall easier to see.</li>'
          '<li>Lower a cover slip <strong>slowly, at an angle</strong>, using the mounting needle. This stops air bubbles being trapped.</li>'
          '<li>Soak up extra liquid at the edge with filter paper. Look at the slide under <strong>low power</strong> first, then high power.</li></ol>'
          '<p>Animal cells (for example cheek cells) are stained with <strong>methylene blue</strong>. Follow your school&rsquo;s safety rules for this practical.</p></div>\n')
    b += L.video("3aQYc6DeWsY", "Video: How to make a wet mount of human cheek cells (stained with methylene blue)", "YouTube: Carolina Science",
                 "Watch how a temporary slide of cheek cells is made and stained. The steps are like the onion slide above.")

    b += '<h2>Label the cells</h2>\n'
    b += '<p>Drag each label to the right box. Then press <strong>Check my labels</strong>. Wrong labels turn red: move them and check again.</p>\n'
    b += L.labeller("lab-animal", F.inner(F.animal_cell(labels=False)), F.ANIMAL_VB[0], F.ANIMAL_VB[1], F.ANIMAL_TARGETS, "A typical animal cell (not to scale).",
                    extra=["cell wall", "chloroplast"], title="Label a typical animal cell.", width=760)
    b += L.labeller("lab-plant", F.inner(F.plant_cell(labels=False, sap_text=False)), F.PLANT_VB[0], F.PLANT_VB[1], F.PLANT_TARGETS, "A typical plant cell, e.g. a leaf cell (not to scale).",
                    title="Label a typical plant cell.", width=760)
    b += L.video("PzxxEVdM1xI", "Video: Introduction to the animal cell", "YouTube: Inspirit",
                 "Watch to review the parts of an animal cell and what each one does.")

    b += '<h2>Cell structures and their functions</h2>\n'
    b += ('<table><tr><th>Structure</th><th>Function</th><th>Found in</th></tr>'
          '<tr><td><strong>Cell membrane</strong></td><td>Controls the movement of substances into and out of the cell. It is <strong>partially permeable</strong>: only small, soluble substances can pass through.</td><td>plant and animal cells</td></tr>'
          '<tr><td><strong>Cell wall</strong></td><td>Protects the cell from injury and gives it a <strong>fixed shape</strong>. Made of <strong>cellulose</strong>. It is <strong>fully permeable</strong>.</td><td>plant cells only</td></tr>'
          '<tr><td><strong>Cytoplasm</strong></td><td>The site of cellular activities. Contains the organelles.</td><td>plant and animal cells</td></tr>'
          '<tr><td><strong>Nucleus</strong></td><td>Controls cell activities such as cell division, growth and repair. Contains <strong>chromosomes</strong> made of <strong>DNA</strong> (deoxyribonucleic acid), which carries hereditary information.</td><td>plant and animal cells</td></tr>'
          '<tr><td><strong>Vacuole</strong></td><td>Stores substances. Plant cell: one large central vacuole of <strong>cell sap</strong> (sugar, mineral salts, amino acids). Animal cell: small, temporary vacuoles of water and food.</td><td>plant and animal cells</td></tr>'
          '<tr><td><strong>Mitochondria</strong></td><td>The site of <strong>aerobic respiration</strong>, which releases energy for the cell.</td><td>plant and animal cells</td></tr>'
          '<tr><td><strong>Ribosomes</strong></td><td>The site of <strong>protein synthesis</strong>.</td><td>plant and animal cells</td></tr>'
          '<tr><td><strong>Chloroplasts</strong></td><td>Contain the green pigment <strong>chlorophyll</strong>, which absorbs light for <strong>photosynthesis</strong> (how plants make food).</td><td>some plant cells</td></tr></table>\n')
    b += ('<p class="common"><strong>Common mistakes:</strong> the cell <em>wall</em> is fully permeable; the cell <em>membrane</em> is partially permeable. '
          'Mitochondria <em>release</em> energy by respiration; they do not &ldquo;make&rdquo; energy. Animal cells never have a cell wall.</p>\n')


    # ---- comparing plant and animal cells (1c)
    b += '<h2>Comparing plant and animal cells</h2>\n'
    big = lambda svg: svg.replace('font-size="16"', 'font-size="21"').replace('font-size="14"', 'font-size="18"')
    b += ('<div class="illus bigcell">%s<p class="fig-caption"><strong>Animal cell</strong></p></div>'
          '<div class="illus bigcell">%s<p class="fig-caption"><strong>Plant cell</strong></p></div>\n'
          '<style>.bigcell svg { width: 100%%; max-width: 860px; height: auto; } .bigcell .fig-caption { font-size: 1.05rem; }</style>\n'
          % (big(F.animal_cell(w=860)), big(F.plant_cell(w=860)).replace('viewBox="0 0 780 330"', 'viewBox="0 0 860 330"')))
    b += '<h3>What they have in common</h3>\n'
    b += ('<p>Both plant and animal cells have a <strong>cell membrane</strong>, <strong>cytoplasm</strong>, a <strong>nucleus</strong>, '
          '<strong>mitochondria</strong>, <strong>ribosomes</strong> and <strong>vacuoles</strong>. These structures do the same jobs in both kinds of cell.</p>\n')
    b += '<h3>How they are different</h3>\n'
    b += ('<table><tr><th>Plant cell</th><th>Animal cell</th></tr>'
          '<tr><td>Cell wall <strong>present</strong> (made of cellulose)</td><td>Cell wall <strong>absent</strong></td></tr>'
          '<tr><td>Chloroplasts <strong>present</strong> (in many plant cells)</td><td>Chloroplasts <strong>absent</strong></td></tr>'
          '<tr><td>One <strong>large, central</strong> vacuole containing cell sap</td><td><strong>Numerous small</strong>, temporary vacuoles</td></tr>'
          '<tr><td>Fixed, regular shape (because of the cell wall)</td><td>No fixed shape</td></tr></table>\n')
    b += ('<p class="common"><strong>Careful:</strong> not every plant cell has chloroplasts. Root cells and onion bulb cells grow in the dark, so they have none. '
          'A cell with a cell wall but no chloroplasts can still be a plant cell. The cell wall is the surest sign.</p>\n')

    b += ''
    b += L.sorter("sort-pa", "Try it: plant only, animal only, or both?", "Choose a button for each structure.", ["Plant only", "Animal only", "Both"], [
        ("Cell wall", 0, "Only plant cells have a cellulose cell wall."),
        ("Nucleus", 2, "Both have a nucleus."),
        ("Chloroplast", 0, "Only (some) plant cells have chloroplasts."),
        ("Cell membrane", 2, "Every cell has a cell membrane, inside the wall in plant cells."),
        ("Large central vacuole with cell sap", 0, "Plant cells have one large, permanent vacuole."),
        ("Many small, temporary vacuoles", 1, "Animal cells have small, temporary vacuoles."),
        ("Mitochondria", 2, "Both kinds of cell respire, so both have mitochondria."),
        ("Ribosomes", 2, "Both kinds of cell make proteins, so both have ribosomes."),
        ("Cytoplasm", 2, "Both have cytoplasm."),
    ])


    b += '<h3>How to answer a &ldquo;compare&rdquo; question</h3>\n'
    b += ('<p>In an exam, <strong>compare</strong> means give <strong>similarities and differences</strong>. Write each difference as a matched pair, so both cells are mentioned.</p>\n'
          '<div class="two-col"><div class="eg-box"><p class="q" style="color:#991b1b">Weak answer</p><p>&ldquo;A plant cell has a cell wall and chloroplasts.&rdquo;</p>'
          '<p class="vid-note">Only one cell is described, and there is no similarity.</p></div>'
          '<div class="eg-box"><p class="q" style="color:#166534">Strong answer</p><p>&ldquo;Both cells have a nucleus, cytoplasm and a cell membrane. '
          'A plant cell has a cellulose cell wall, <em>but</em> an animal cell does not. A plant cell has one large central vacuole, <em>whereas</em> an animal cell has many small vacuoles.&rdquo;</p></div></div>\n')

    b += MICROGRAPHS()
    b += '<h2>Check your understanding</h2>\n'
    b += L.mcq(1, "Which structure controls the movement of substances into and out of a cell?", ["Cell wall", "Cell membrane", "Cytoplasm", "Nucleus"], 1,
               "The cell membrane is partially permeable and controls what enters and leaves. The cell wall is fully permeable, so it does not control this.")
    b += L.mcq(2, "Which structure contains chromosomes made of DNA?", ["Nucleus", "Ribosome", "Vacuole", "Chloroplast"], 0,
               "The nucleus contains the chromosomes. The DNA carries hereditary information.")
    b += L.mcq(3, "Where is protein made in a cell?", ["Mitochondria", "Cell sap", "Ribosomes", "Nucleus"], 2, "Ribosomes are the site of protein synthesis.")
    b += L.mcq(4, "A student looks at a cheek cell under a school light microscope. Which structure will the student NOT be able to see clearly?", ["Nucleus", "Cell membrane", "Cytoplasm", "Mitochondria"], 3,
               "Mitochondria (and ribosomes) are too small for a light microscope. They are seen in electron micrographs.")
    b += L.mcq(5, "Why is the cover slip lowered slowly, at an angle, when making a slide?", ["To stain the cells", "To stop air bubbles being trapped", "To make the cells bigger", "To kill the cells"], 1,
               "Lowering it at an angle pushes the air out, so no air bubbles hide the cells.")
    b += L.mcq(6, "Which three structures are found in plant cells but NOT in animal cells?", [
        "Cell wall, chloroplasts, large central vacuole", "Cell membrane, nucleus, cytoplasm", "Mitochondria, ribosomes, cell wall", "Chloroplasts, nucleus, ribosomes"], 0,
        "Only plant cells have a cell wall, chloroplasts and one large central vacuole.")
    b += L.mcq(7, "A cell has a cell wall and a large vacuole but no chloroplasts. Where could it come from?", [
        "A human cheek", "A plant root", "A human muscle", "A red blood cell"], 1, "The cell wall shows it is a plant cell. Root cells are in the dark, so they have no chloroplasts.")
    b += L.mcq(8, "Which statement about animal cells is correct?", [
        "They have one large central vacuole.", "They have small, temporary vacuoles.", "They have a cell wall made of cellulose.", "They have chloroplasts."], 1,
        "Animal cells have small, temporary vacuoles and no cell wall or chloroplasts.")
    b += L.mcq(9, "Why do both plant and animal cells have mitochondria?", [
        "Both need to photosynthesise.", "Both need to release energy by aerobic respiration.", "Both need a fixed shape.", "Both store cell sap."], 1,
        "All living cells need energy, which is released by aerobic respiration in mitochondria.")
    b += ('<p class="more-links"><strong>Exam practice:</strong> try the structured question comparing a <strong>liver cell</strong> and a <strong>root hair cell</strong> '
          '(Section B, question 6) on the <a href="revision-01-cells.html#q6">Revision Questions</a> page.</p>\n')
    L.page("cells-1-1-what-are-cells", "1.1 What Are Cells?", REFS + "1a, 1b, 1c", L.LABEL_CSS + b, JS, topic=TOPIC)


# ================================================================== Lesson 1.2 How Are Cells Adapted to Their Functions? (1d)
import topic01_sav as SAV


def lesson3():
    b = LO12
    b += '<h2>Why are cells specialised?</h2>\n'
    b += ('<p>In a large organism, different cells do different jobs. A <strong>specialised cell</strong> has a structure that is <strong>adapted</strong> (suited) to its function. '
          'Each one still has the usual cell parts, but some parts are changed, added or lost.</p>\n'
          '<p class="keyidea"><strong>Key idea:</strong> for every adaptation, say <strong>what the feature is</strong> and <strong>how it helps the cell do its job</strong>.</p>\n')
    b += ('<p class="keyidea"><strong>Differentiation:</strong> as an organism grows, its cells change to become <strong>specialised</strong>: '
          'each type of cell develops a structure that suits one particular job.</p>\n'
          '<p>Your body has many kinds of specialised cells, each with its own job. For example:</p>\n'
          '<ul><li><strong>red blood cells</strong> carry oxygen around the body;</li>'
          '<li><strong>nerve cells</strong> carry messages between parts of the body;</li>'
          '<li><strong>intestinal cells</strong> lining the gut absorb digested food;</li>'
          '<li><strong>root hair cells</strong> in plants absorb water and mineral salts from the soil.</li></ul>\n')
    cards = [(F.mini_rbc(), "red blood cells", "carry oxygen around the body"),
             (F.mini_nerve(), "nerve cell", "carries messages between parts of the body"),
             (F.mini_intestine(), "intestinal cells", "line the gut and absorb digested food"),
             (F.mini_root_hair(), "root hair cell", "absorbs water and mineral salts from the soil")]
    b += ('<style>.cellcards { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 0.8rem; margin: 1rem 0 0.3rem; }'
          '.cellcards figure { margin: 0; background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.6rem; text-align: center; break-inside: avoid; }'
          '.cellcards svg { width: 100%; height: 120px; margin: 0 0 0.4rem; }'
          '.cellcards figcaption { font-size: 0.95rem; line-height: 1.35; }</style>\n')
    b += '<div class="cellcards">' + "".join('<figure>%s<figcaption><strong>%s</strong><br>%s</figcaption></figure>' % c for c in cards) + '</div>\n'
    b += '<p class="photo-note">Drawings, not to scale.</p>\n'
    b += L.video("Wo4bz6hxjrA", "Video: Specialised cells explained", "YouTube: Biospeaks",
                 "Watch to see more examples of specialised cells and how their structures suit their jobs.")

    b += '<h2>Surface area to volume ratio</h2>\n'
    b += ('<p>Substances such as oxygen, water and mineral salts enter a cell through its <strong>surface</strong> (the cell membrane). '
          'The more surface a cell has for its size, the faster it can take substances in. We compare cells using the <strong>surface area to volume ratio</strong> (SA&nbsp;:&nbsp;V).</p>\n')
    b += SAV.CSS + SAV.SHAPES + SAV.CUT + SAV.AGAR

    b += '<h2>Red blood cell</h2>\n'
    b += L.fig(F.red_blood_cell(), "A red blood cell. Function: <strong>transports oxygen</strong> around the body.")
    b += ('<figure class="pic cellphoto"><img src="img/red-blood-cells-sem.jpg" alt="Many red blood cells: round discs, each dipped in the middle on both sides" loading="lazy"><figcaption><strong>Real red blood cells</strong> (scanning electron micrograph). Look for the biconcave discs: each one is dipped in the middle. Cells seen side-on look like thin bars.</figcaption></figure>'
          '<p class="credit">Image: <a href="https://wellcomecollection.org/works/sfnd37qs">David Gregory &amp; Debbie Marshall</a>, CC BY 4.0, Wellcome Collection.</p>\n')
    b += ('<table><tr><th>Adaptation</th><th>How it helps</th></tr>'
          '<tr><td>Contains <strong>haemoglobin</strong></td><td>Haemoglobin binds to oxygen, so the cell can carry oxygen around the body.</td></tr>'
          '<tr><td><strong>Circular, biconcave</strong> shape</td><td>Increases the surface area to volume ratio, so oxygen is taken in and released faster.</td></tr>'
          '<tr><td><strong>No nucleus</strong></td><td>More space to pack in haemoglobin, so it can transport more oxygen.</td></tr>'
          '<tr><td><strong>Flexible</strong></td><td>It can squeeze through narrow blood capillaries.</td></tr></table>\n')

    b += '<h2>Muscle cell</h2>\n'
    b += L.fig(F.muscle_cell(), "A muscle cell. Function: <strong>contracts and relaxes</strong> to bring about movement.")
    b += ('<figure class="pic cellphoto"><img src="img/muscle-lm.jpg" alt="Long pink muscle cells lying side by side, with fine stripes across them" loading="lazy"><figcaption><strong>Real muscle cells</strong> (light micrograph, stained pink). Each muscle cell is very long. The fine stripes across it come from the contractile protein fibres.</figcaption></figure>'
          '<p class="credit">Image: <a href="https://commons.wikimedia.org/wiki/File:Skeletal_muscle_-_longitudinal_section.jpg">Department of Histology, Jagiellonian University Medical College</a>, CC BY-SA 3.0, via Wikimedia Commons.</p>\n')
    b += ('<figure class="pic cellphoto"><img src="img/cardiac-muscle.jpg" alt="Illustration of heart muscle: the heart, then a close-up of long muscle cells, then a closer view showing green mitochondria lying between the myofibrils" loading="lazy">'
          '<figcaption><strong>Zooming in on heart muscle</strong> (illustration). The <strong>mitochondria</strong> (green) sit right next to the <strong>myofibrils</strong>, '
          'the contractile protein fibres, so the energy they release reaches the fibres quickly. Heart muscle never rests, so it is packed with mitochondria.</figcaption></figure>'
          '<p class="credit">Image: <a href="https://commons.wikimedia.org/wiki/File:Cardiac_Muscle.png">BruceBlaus (Blausen Medical)</a>, CC BY-SA 4.0, via Wikimedia Commons.</p>\n')
    b += ('<table><tr><th>Adaptation</th><th>How it helps</th></tr>'
          '<tr><td>Contains <strong>many mitochondria</strong></td><td>More aerobic respiration, so more energy is released for contraction.</td></tr>'
          '<tr><td>Has <strong>contractile protein fibres</strong></td><td>The fibres contract and relax to bring about movement.</td></tr>'
          '<tr><td>Has <strong>many nuclei</strong></td><td>Allows for cell division, growth and repair of the long cell.</td></tr></table>\n')

    b += '<h2>Root hair cell</h2>\n'
    b += L.fig(F.root_hair_cell(), "A root hair cell. Function: <strong>absorbs water and mineral salts</strong> from the soil.")
    b += ('<figure class="pic cellphoto"><img src="img/root-hair-lm.jpg" alt="Edge of a root seen under a microscope: one long, thin root hair grows out from a single cell on the surface" loading="lazy"><figcaption><strong>A real root hair</strong> (light micrograph of a lily root). The long, thin extension on the left grows out of <em>one</em> cell on the surface of the root.</figcaption></figure>'
          '<p class="credit">Image: <a href="https://commons.wikimedia.org/wiki/File:Monocot_Root_Epidermal_Root_Hair_in_Lilium_(36045152715).jpg">Berkshire Community College Bioscience Image Library</a>, CC0, via Wikimedia Commons.</p>\n')
    b += ('<table><tr><th>Adaptation</th><th>How it helps</th></tr>'
          '<tr><td><strong>Long and narrow extension</strong> (the root hair)</td><td>Increases the surface area to volume ratio, so water and mineral salts are absorbed faster.</td></tr>'
          '<tr><td>Cell sap in the vacuole has a <strong>lower water potential</strong> than the soil water</td><td>Water enters the root hair cell by <strong>osmosis</strong>. (You will learn about osmosis in Topic 2.)</td></tr>'
          '<tr><td><strong>No chloroplasts</strong></td><td>It grows underground with no light, so chloroplasts would have no use.</td></tr></table>\n')

    b += '<h2>Writing about adaptations</h2>\n'
    b += ('<p>Link the <strong>feature</strong> to its <strong>effect</strong> and the <strong>function</strong>:</p>\n'
          '<div class="flow"><span>feature</span><b>&rarr;</b><span>so that&hellip;</span><b>&rarr;</b><span>which helps the cell to&hellip;</span></div>\n'
          '<p><em>Example:</em> &ldquo;A red blood cell has <strong>no nucleus</strong>, <strong>so</strong> there is more space for haemoglobin, '
          '<strong>so</strong> it can transport more oxygen.&rdquo;</p>\n')
    b += L.sorter("sort-sc", "Try it: which cell has this adaptation?", "Choose the cell for each feature.", ["Red blood cell", "Muscle cell", "Root hair cell"], [
        ("No nucleus", 0, "Red blood cells lose their nucleus to make room for more haemoglobin."),
        ("Many mitochondria", 1, "Muscle cells need a lot of energy to contract."),
        ("Long, narrow extension into the soil", 2, "The root hair increases the surface area for absorbing water and mineral salts."),
        ("Contains haemoglobin", 0, "Haemoglobin binds to oxygen."),
        ("Contractile protein fibres", 1, "The fibres contract and relax to cause movement."),
        ("Cell sap with a lower water potential than soil water", 2, "So water enters by osmosis."),
        ("Biconcave disc shape", 0, "This increases the surface area to volume ratio."),
        ("Many nuclei", 1, "Long muscle cells have many nuclei."),
    ])

    b += '<h2>Check your understanding</h2>\n'
    b += L.mcq(1, "Why does a red blood cell have no nucleus?", ["So it can divide faster", "To make room for more haemoglobin", "So it can absorb water", "To release more energy"], 1,
               "With no nucleus there is more space for haemoglobin, so the cell can carry more oxygen.")
    b += L.mcq(2, "Muscle cells contain many mitochondria. What is the reason?", [
        "To make more proteins", "To store cell sap", "To release more energy by aerobic respiration for contraction", "To absorb more light"], 2,
        "Contraction needs energy. More mitochondria means more aerobic respiration.")
    b += L.mcq(3, "How does the long extension of a root hair cell help the plant?", [
        "It gives the cell a fixed shape.", "It increases the surface area to volume ratio for absorbing water and mineral salts.", "It carries oxygen to the leaves.", "It makes food by photosynthesis."], 1,
        "A long, narrow extension gives a much larger surface for absorption.")
    b += L.calc(4, "A cube-shaped cell has sides of 2 &micro;m. Its surface area is 24 &micro;m&sup2; and its volume is 8 &micro;m&sup3;. Work out the surface area to volume ratio (as a number : 1).", 3, 0.01, ": 1",
                "SA : V = 24 : 8 = 3 : 1.")
    b += L.mcq(5, "The biconcave shape of a red blood cell&hellip;", [
        "lets it squeeze through capillaries.", "increases its surface area to volume ratio for faster uptake of oxygen.", "gives it room for a nucleus.", "makes it contract."], 1,
        "The biconcave shape gives a larger surface area to volume ratio. (Being flexible is what lets it squeeze through capillaries.)")
    L.page("cells-1-2-cell-adaptations", "1.2 How Are Cells Adapted to Their Functions?", REFS + "1d", b, JS + SAV.JS, topic=TOPIC)


if __name__ == "__main__":
    lesson1()
    lesson3()
