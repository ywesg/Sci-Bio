#!/usr/bin/env python3
"""Topic 2: Movement of Substances (G2 and G3 have the same syllabus outcomes: 2a diffusion, 2b osmosis).
First drafts of lessons 2.1 and 2.2 (numbered as in the textbook). Figures in topic02_figs.py, particle animations in topic02_sim.py.
Run: python3 build_topic02.py && python3 add_navigation.py
Once a lesson has been edited by hand, do not run this script over it again (comment out its build call below)."""
import lesson_kit as L
import topic02_figs as F
import topic02_sim as S

TOPIC = "Movement of Substances"
REFS = "Syllabus refs (G2 &amp; G3): "
JS = L.SORT_JS + L.LABEL_JS + S.SIM_JS
C = "https://commons.wikimedia.org/wiki/File:"

CSS = S.SIM_CSS + """<style>
  .defn { border: 1px solid #fbcfe8; background: #fdf2f8; border-radius: 10px; padding: 0.8rem 1.1rem; margin: 1rem 0; }
  .defn strong:first-child { color: #9d174d; }
  details.ans { margin: 0.4rem 0 0.6rem; } details.ans summary { cursor: pointer; color: #0f766e; font-weight: 700; }
  details.ans div { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.5rem 0.8rem; margin-top: 0.3rem; }
  .figrow { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0.8rem; align-items: end; }
  .figrow .illus svg { width: 100%; height: auto; }
  .cellcmp td svg { width: 100%; max-width: 220px; height: auto; display: block; margin: 0.3rem auto; }
  .cellcmp td { vertical-align: top; }
  .rbcrow { display: flex; align-items: center; justify-content: center; gap: 0.3rem; margin-top: 0.5rem; }
  .cellcmp .rbcrow svg { width: 72px; height: auto; margin: 0; } .rbcrow b { color: #2563eb; font-size: 1.3rem; }
  .sidebox { border-left: 4px solid #84cc16; background: #f7fee7; padding: 0.5rem 1rem; margin: 1rem 0; border-radius: 0 8px 8px 0; }
  .sidebox h4 { margin: 0.2rem 0; color: #3f6212; }
  @media print { details.ans div { display: block; } }
</style>
"""


def answers(*qa):
    """Observation and discussion questions with answers hidden behind 'Show answer'."""
    h = "<ol>"
    for q, a in qa:
        h += '<li>%s<details class="ans print-hide"><summary>Show answer</summary><div>%s</div></details></li>' % (q, a)
    return h + "</ol>"


LO21 = '''<div class="practical"><h3>Learning outcomes</h3><ul>
<li>Define diffusion and describe its role in nutrient uptake and gaseous exchange in plants and humans.</li>
<li>Describe the factors that affect the rate of diffusion.</li></ul></div>
'''
LO22 = '''<div class="practical"><h3>Learning outcomes</h3><ul>
<li>Define osmosis, investigate and describe the effects of osmosis on plant and animal tissues.</li>
<li>Discuss the factors that affect the rate of osmosis.</li></ul></div>
'''


# ================================================================== Lesson 2.1 What Is Diffusion? (2a)
def lesson1():
    b = LO21
    b += '<h2>Trigger activity</h2>\n'
    b += ('<p>Someone sprays perfume at one end of a room. A few moments later, a person at the other end can smell it. '
          '<strong>How did the perfume get there, when nobody carried it?</strong></p>\n')
    b += L.fig(F.perfume(), "Perfume particles spread out from where they are crowded to where there are fewer of them.", "2.1")
    b += ('<p>The perfume particles are always moving about at random, bumping into air particles. Near the bottle there are many perfume particles; '
          'far away there are few. So, overall, more particles move <em>away</em> from the bottle than towards it. The perfume spreads until it is evenly mixed in the air.</p>\n')

    b += '<h2>What is diffusion?</h2>\n'
    b += ('<p>The difference in concentration between two regions is called a <strong>concentration gradient</strong>. '
          'Particles spread from the region of higher concentration to the region of lower concentration: we say they move <strong>down the concentration gradient</strong>.</p>\n')
    b += ('<p class="defn"><strong>Diffusion</strong> is the net movement of particles (atoms, molecules or ions) from a region where they are at a higher concentration '
          'to a region where they are at a lower concentration, that is, down a concentration gradient.</p>\n')
    b += ('<p class="keyidea"><strong>Key idea:</strong> the <strong>steeper</strong> the concentration gradient (the bigger the difference in concentration), '
          'the <strong>faster</strong> the rate of diffusion.</p>\n')
    b += ('<p><strong>Why &ldquo;net&rdquo;?</strong> Each particle moves at random, in any direction. Some particles even move back towards the crowded region. '
          'The <em>net</em> movement is the overall result: more particles go one way than the other.</p>\n')
    b += S.sim("sim-free", "free", "Example 1: diffusion in water",
               "Blue particles of a substance start crowded on the left. Press <strong>Start</strong> and watch the numbers on each side.",
               '<i style="background:#3b82f6"></i>particles of a dissolved substance')

    b += ('<div class="practical"><h3>Practical: diffusion of a dissolved substance in water</h3>'
          '<p><strong>Aim:</strong> to investigate how a dissolved substance spreads through water.</p>'
          '<p><strong>Procedure</strong></p><ol>'
          '<li>Gently drop one crystal of <strong>copper(II) sulfate</strong> into a gas jar filled with water. Cover the jar.</li>'
          '<li>Leave the jar to stand, without shaking it, for a few days.</li>'
          '<li>Observe how the colour of the water changes.</li></ol>')
    b += L.fig(F.gas_jars(), "The copper(II) sulfate crystal dissolves, and the blue colour slowly spreads through all the water.", "2.2")
    b += '<p><strong>Observation and discussion</strong></p>'
    b += answers(
        ("Use the idea of a concentration gradient to explain why the blue colour slowly spreads through the water.",
         "At first, copper(II) sulfate particles are at a high concentration near the crystal and a low concentration in the rest of the water. "
         "The particles diffuse down this concentration gradient, from the bottom of the jar to the top, so the blue colour spreads."),
        ("When does diffusion stop?",
         "When the copper(II) sulfate particles are evenly spread through the water (the colour is the same everywhere). "
         "There is no concentration gradient any more, so there is no <em>net</em> movement. The particles are still moving at random."))
    b += '</div>\n'
    b += ('<p>In the practical, the copper(II) sulfate particles moved from the region of higher concentration around the crystal to regions of lower concentration in the water. '
          'The solute diffused until it was evenly spread, forming a solution.</p>\n'
          '<p>If <strong>more than one substance</strong> is dissolved in the same liquid, each one diffuses on its own, down its own concentration gradient. '
          'The particles of one substance do not affect the diffusion of the other.</p>\n')
    b += L.video("lxHMJaXOzP4", "Video: What is diffusion? How does it work?", "YouTube: Cognito",
                 "Watch from the start to the end of the section on factors. Ignore the part about temperature: our textbook does not include it in this lesson.")

    b += '<h2>Diffusion across a membrane</h2>\n'
    b += ('<p>A <strong>permeable membrane</strong> lets both the solvent (water) and the solutes (the dissolved substances) pass through it. '
          'In Fig. 2.3, a permeable membrane divides a beaker into two halves:</p>\n'
          '<ul><li>the <strong>left</strong> side has a higher concentration of <strong>potassium nitrate</strong> (yellow);</li>'
          '<li>the <strong>right</strong> side has a higher concentration of <strong>copper(II) sulfate</strong> (blue).</li></ul>\n')
    b += L.fig(F.membrane_beakers(), "Potassium nitrate and copper(II) sulfate particles diffusing through a permeable membrane.", "2.3")
    b += ('<p>So the potassium nitrate particles diffuse across the membrane to the right, and the copper(II) sulfate particles diffuse across to the left. '
          'In the end, the concentration of each substance is the <strong>same on both sides</strong> of the membrane.</p>\n')
    b += S.sim("sim-two", "two", "See it happen: two substances, one membrane",
               "The grey line is a permeable membrane with gaps. Both kinds of particle can pass through the gaps.",
               '<i style="background:#eab308"></i>potassium nitrate <i style="background:#3b82f6"></i>copper(II) sulfate')
    b += S.sim("sim-starch", "starch", 'Example 4: starch and iodine in Visking tubing <span class="g3-badge">G3 only</span>',
               "Visking tubing is a <strong>partially permeable membrane</strong>. The tubing holds <strong>starch solution</strong> and stands in brown <strong>iodine solution</strong>. "
               "Iodine turns <strong>blue-black</strong> when it meets starch.",
               '<i style="background:#e5e7eb;border:1px solid #64748b"></i>starch molecule (large) <i style="background:#92400e"></i>iodine molecule (small)',
               only="Only the small iodine molecules can pass through the tubing. Starch molecules are too large to pass through.", extra_class=" g3-only", height=380)

    b += '<h2>Quick check</h2>\n'
    b += L.mcq("Q1", "Which statement describes diffusion?", [
        "Net movement of particles from a region of lower concentration to a region of higher concentration",
        "Net movement of particles from a region of higher concentration to a region of lower concentration",
        "Movement of water only, through a partially permeable membrane",
        "Movement of particles only through a membrane"], 1,
        "Diffusion is net movement down a concentration gradient: from higher to lower concentration. It can happen with or without a membrane.")
    b += L.mcq("Q2", "Region X has a high concentration of a substance and region Y has a low concentration. In which direction is the net movement of the substance?", [
        "From Y to X", "From X to Y", "There is no movement", "Equally in both directions"], 1,
        "Net movement is down the concentration gradient: from the higher concentration (X) to the lower concentration (Y).")
    b += L.mcq("Q3", "A crystal of copper(II) sulfate is left in a gas jar of water. After many days the water is evenly blue. Which is correct?", [
        "The copper(II) sulfate particles have stopped moving.", "There is no net movement, but the particles are still moving.",
        "The particles are now moving towards the bottom of the jar.", "The water has turned into copper(II) sulfate."], 1,
        "Once the concentration is the same everywhere there is no net movement, but the particles keep moving at random.")
    b += L.mcq("Q4", "A beaker is divided by a permeable membrane. The left side has more potassium nitrate; the right side has more copper(II) sulfate. What happens?", [
        "Only potassium nitrate moves.", "Potassium nitrate moves to the right and copper(II) sulfate moves to the left.",
        "Both substances move to the left.", "Nothing moves, because they block each other."], 1,
        "Each substance diffuses down its own concentration gradient, independently of the other.")

    b += '<h2>Factors that affect the rate of diffusion</h2>\n'
    b += ('<p>How fast a substance diffuses depends on three factors:</p>\n'
          '<div class="flow"><span>1. concentration gradient</span><span>2. diffusion distance</span><span>3. surface area to volume ratio</span></div>\n')
    b += ('<h3>1. Concentration gradient</h3>\n<p>The <strong>steeper</strong> the concentration gradient (the bigger the difference in concentration between the two regions), '
          'the <strong>faster</strong> the rate of diffusion. When there is no concentration gradient, there is no net diffusion.</p>\n')
    b += ('<h3>2. Diffusion distance</h3>\n<p>The distance a substance has to travel is the <strong>diffusion distance</strong>. '
          'The <strong>shorter</strong> the diffusion distance, the less time the substance needs to get there, so the <strong>faster</strong> the rate of diffusion.</p>\n')
    b += '<h3>3. Surface area to volume ratio</h3>\n'
    b += ('<p>Substances enter and leave a cell through its surface (the cell membrane), so the rate of diffusion depends on the cell&rsquo;s <strong>surface area</strong>. '
          'For two cells with the same volume, the one with the larger surface area takes substances in faster. '
          'Comparing a cell&rsquo;s surface area with its volume gives its <strong>surface area to volume ratio</strong> (SA&nbsp;:&nbsp;V).</p>\n'
          '<p class="keyidea">The <strong>greater</strong> the surface area to volume ratio, the <strong>faster</strong> the rate of diffusion into and out of the cell.</p>\n'
          '<p>As a cell gets bigger, its volume grows faster than its surface area, so its SA&nbsp;:&nbsp;V gets smaller. This is why cells are usually small, '
          'and why a large organism is made of many small cells rather than one giant cell.</p>\n'
          '<p class="more-links"><strong>Try it again:</strong> the shape builder and the agar-cube experiment on SA&nbsp;:&nbsp;V are in '
          '<a href="cells-1-2-cell-adaptations.html#surface-area-to-volume-ratio">Lesson 1.2</a>.</p>\n')
    b += L.calc("A", "Cube X has sides of 1 cm: surface area 6 cm&sup2;, volume 1 cm&sup3;. Cube Y has sides of 3 cm: surface area 54 cm&sup2;, volume 27 cm&sup3;. "
                "Work out the SA : V of cube Y (as a number : 1).", 2, 0.01, ": 1",
                "54 : 27 = 2 : 1. Cube X has 6 : 1, so the smaller cube has the greater SA : V, and substances diffuse into it relatively faster.")
    b += L.sorter("sort-rate", "Try it: faster or slower diffusion?", "Choose a button for each change.", ["Faster", "Slower"], [
        ("The concentration gradient becomes steeper", 0, "A bigger difference in concentration means a faster rate."),
        ("The diffusion distance is longer", 1, "Particles take longer to travel further."),
        ("The cell has a larger surface area to volume ratio", 0, "More surface for each unit of volume, so substances move in and out faster."),
        ("The concentrations on both sides become equal", 1, "No concentration gradient: no net diffusion."),
        ("The diffusion distance becomes shorter", 0, "Particles have less distance to travel."),
        ("The cell grows much bigger", 1, "Its SA : V becomes smaller."),
    ])

    b += '<h2>Diffusion in living things</h2>\n'
    b += ('<p>The cell membrane is <strong>partially permeable</strong>: it lets some substances through but not others. '
          'Small molecules such as <strong>oxygen</strong>, <strong>carbon dioxide</strong>, <strong>glucose</strong> and <strong>amino acids</strong> can pass through; large molecules such as proteins cannot. '
          'Living things use diffusion to take in what they need and get rid of what they do not. Notice how each example has a <strong>short diffusion distance</strong> or a <strong>large surface area</strong>.</p>\n')
    b += '<h3>In humans</h3>\n'
    b += ('<p><strong>1. Gas exchange in the lungs.</strong> The air in the lungs has a high concentration of oxygen, and the blood arriving there has a low concentration. '
          'Oxygen diffuses from the air space, through a very thin wall, into the red blood cells. Carbon dioxide diffuses the other way, from the blood into the air space, and is breathed out. '
          'The wall is only <strong>one cell thick</strong>, so the diffusion distance is short and diffusion is fast.</p>\n')
    b += L.fig(F.alveolus(), "Gas exchange between an air space in the lung and the blood.", "2.4")
    b += L.labeller("lab-alv", F.alveolus(labels=False), F.ALV_VB[0], F.ALV_VB[1], F.ALV_TARGETS, "Gas exchange in the lungs.",
                    extra=["cell wall", "chloroplast"], title="Label gas exchange in the lungs.", width=680)
    b += ('<p><strong>2. Absorption of digested food in the small intestine.</strong> After digestion, there is a high concentration of small food molecules, such as '
          '<strong>glucose</strong> and <strong>amino acids</strong>, inside the small intestine, and a lower concentration in the blood. '
          'They diffuse through the lining of the small intestine into the blood capillaries, and the blood carries them around the body. '
          'The lining is one cell thick (short diffusion distance) and has many tiny folds (large surface area).</p>\n'
          '<p class="keyidea">Glucose and amino acids are <strong>solutes</strong>: substances dissolved in another substance (the <strong>solvent</strong>). Together they make a <strong>solution</strong>.</p>\n')
    b += L.fig(F.intestine(), "Absorption of digested food by diffusion in the small intestine.", "2.5")
    b += '<h3>In plants</h3>\n'
    b += ('<p><strong>1. Gas exchange through the stomata.</strong> Leaves have tiny pores called <strong>stomata</strong> (one is a <strong>stoma</strong>), mostly on the underside. '
          'In the light, leaf cells use carbon dioxide for <strong>photosynthesis</strong>, so the concentration of carbon dioxide inside the leaf is low. '
          '<strong>Carbon dioxide</strong> diffuses from the air <strong>into</strong> the leaf through the stomata. Photosynthesis makes <strong>oxygen</strong>, so its concentration inside the leaf is high, '
          'and oxygen diffuses <strong>out</strong> of the leaf through the stomata.</p>\n')
    b += L.fig(F.leaf_stomata(), "Carbon dioxide diffuses into a leaf and oxygen diffuses out through a stoma.", "2.6")
    b += ('<figure class="pic cellphoto"><img src="img/stoma-sem.jpg" alt="Electron micrograph of a leaf surface showing one stoma: an oval pore between two curved guard cells" loading="lazy">'
          '<figcaption>A real stoma on a tomato leaf (scanning electron micrograph, colour added). The pore is between two guard cells.</figcaption></figure>\n'
          '<p class="credit">Image: <a href="%sTomato_leaf_stomate_1-color.jpg">Photohound</a>, public domain, via Wikimedia Commons.</p>\n' % C)
    b += ('<p><strong>2. Root hair cell.</strong> A root hair cell has a <strong>long, narrow protrusion</strong> (the root hair) that grows out between the soil particles. '
          'This gives the cell a <strong>large surface area to volume ratio</strong>, so substances diffuse into it faster. '
          'Oxygen diffuses in from the air spaces in the soil (and carbon dioxide diffuses out). '
          'Mineral salts dissolved in the soil water can also diffuse in when their concentration in the soil is higher than in the cell. (Water enters by osmosis: see Lesson 2.2.)</p>\n')
    b += L.fig(F.root_hair_gas(), "A root hair cell: its long, narrow protrusion gives a large surface area for diffusion.", "2.7")
    b += ('<div class="sidebox"><h4>Big idea: systems</h4><p>Living things depend on diffusion to exchange gases and take in nutrients. '
          'You will meet these examples again in the topics on nutrition, transport and respiration.</p></div>\n')

    b += '<h2>Check your understanding</h2>\n'
    b += L.mcq(1, "Which change makes diffusion faster?", [
        "A shallower concentration gradient", "A longer diffusion distance", "A smaller surface area to volume ratio", "A steeper concentration gradient"], 3,
        "The steeper the concentration gradient, the faster the rate of diffusion.")
    b += L.mcq(2, "Why are most cells very small?", [
        "Small cells have a smaller surface area to volume ratio.", "Small cells have a larger surface area to volume ratio, so substances can move in and out fast enough.",
        "Small cells do not need oxygen.", "Small cells have no cell membrane."], 1,
        "A small cell has a large SA : V, so substances can enter and leave it quickly enough to keep it alive.")
    b += L.mcq(3, "In the lungs, in which direction does oxygen diffuse?", [
        "From the blood into the air space", "From the air space into the blood", "It does not move", "From the red blood cells into the air space"], 1,
        "Oxygen is at a higher concentration in the air space than in the blood, so it diffuses into the blood.")
    b += L.mcq(4, "How do glucose and amino acids get from the small intestine into the blood?", [
        "By diffusion into the blood capillaries", "By photosynthesis", "By breathing", "They stay in the small intestine"], 0,
        "Digested food such as glucose and amino acids diffuses through the lining of the small intestine into the blood capillaries.")
    b += L.mcq(5, "In the light, which gases diffuse into and out of a leaf through the stomata?", [
        "Oxygen in, carbon dioxide out", "Carbon dioxide in, oxygen out", "Nitrogen in, oxygen out", "Water in, glucose out"], 1,
        "Photosynthesis uses carbon dioxide (low concentration inside the leaf) and makes oxygen (high concentration inside), so carbon dioxide diffuses in and oxygen diffuses out.")
    b += L.mcq(6, "How does the long, narrow protrusion of a root hair cell help it?", [
        "It gives the cell a fixed shape.", "It gives a large surface area to volume ratio, so substances diffuse in faster.", "It makes food by photosynthesis.", "It stops water entering the cell."], 1,
        "A long, narrow protrusion gives a large surface area for diffusion.")
    b += L.mcq(7, "Which substance cannot pass through a cell membrane?", ["Oxygen", "Carbon dioxide", "Glucose", "Protein"], 3,
               "The cell membrane is partially permeable. Proteins are large molecules and cannot pass through.")
    L.page("movement-2-1-diffusion", "2.1 What Is Diffusion?", REFS + "2a", CSS + L.LABEL_CSS + b, JS, topic=TOPIC)


# ================================================================== Lesson 2.2 What Is Osmosis? (2b)
def lesson2():
    b = LO22
    b += '<h2>Osmosis</h2>\n'
    b += ('<p>The cell membrane is a <strong>partially permeable membrane</strong>: it lets some substances through but not others. '
          'In Fig. 2.8, a partially permeable membrane separates the two arms of a U-tube. The membrane lets <strong>water</strong> molecules through, '
          'but <strong>not sucrose</strong> molecules. (Sucrose is cane sugar, the sugar you use at home.)</p>\n')
    b += ('<div class="figrow"><div class="illus">%s</div><div class="illus">%s</div></div>\n<p class="fig-caption"><strong>Fig. 2.8</strong> &mdash; Experiment to show osmosis.</p>\n'
          % (F.utube(), F.utube(after=True)))
    b += ('<p>Compared with arm B, arm A has:</p><ul><li><strong>more</strong> sucrose molecules per unit volume;</li><li><strong>fewer</strong> water molecules per unit volume.</li></ul>\n'
          '<p>After some time, the level in arm A <strong>rises</strong> and the level in arm B <strong>falls</strong>. Why?</p>\n'
          '<ul><li>Sucrose molecules are too large to pass through the tiny pores of the membrane, so they cannot move from A to B.</li>'
          '<li>Water molecules move from B to A, because solution B has more water molecules per unit volume than solution A. '
          '(A <strong>dilute</strong> solution has more water molecules per unit volume than a <strong>concentrated</strong> solution.)</li></ul>\n'
          '<p>Water keeps moving until both arms have the same solute concentration (the same number of solute molecules per unit volume).</p>\n'
          '<p class="keyidea">The diffusion of <strong>water molecules</strong> across a <strong>partially permeable membrane</strong> is called <strong>osmosis</strong>.</p>\n'
          '<div class="sidebox"><h4>Link to Chemistry</h4><p>The <strong>concentration</strong> of a solution is the amount of solute dissolved in a unit volume of the solution.</p></div>\n')
    b += S.sim("sim-utube", "utube", "Example 2: osmosis in a U-tube",
               "The two arms hold sucrose solutions. The green dashed line at the bottom is a <strong>partially permeable membrane</strong>. "
               "Choose the concentrations, press <strong>Start</strong> and watch the water levels.",
               '<i style="background:#f97316"></i>sucrose molecule <i style="background:#60a5fa"></i>water molecule',
               presets=["A: 10% &middot; B: 5%", "A: 5% &middot; B: 10%", "A: 5% &middot; B: 5%"],
               only="Only water molecules can pass through the membrane. Sucrose molecules are too large to pass through.", height=325)

    b += ('<div class="practical"><h3>Practical: demonstrating osmosis</h3>'
          '<p><strong>Aim:</strong> to show osmosis using dialysis tubing (Visking tubing), which is a partially permeable membrane.</p>'
          '<p><strong>Procedure</strong></p><ol>'
          '<li>Tie a knot in one end of a piece of dialysis tubing.</li>'
          '<li>Fill a boiling tube halfway with distilled water.</li>'
          '<li>Use a pipette to fill the dialysis tubing halfway with sucrose solution. If any spills, rinse the outside of the tubing with distilled water.</li>'
          '<li>Set up the apparatus as in Fig. 2.9. The liquid levels inside and outside the tubing must be the same. Hold the tubing in place with a paper clip and mark the level on the outside of the boiling tube.</li>'
          '<li>Set up a second boiling tube in the same way, but with distilled water both inside the tubing and in the boiling tube.</li>'
          '<li>After 20 minutes, observe the liquid levels inside and outside the tubing in each set-up.</li></ol>')
    b += ('<div class="figrow"><div class="illus">%s<p class="fig-caption">At the start</p></div><div class="illus">%s<p class="fig-caption">After 20 minutes</p></div></div>\n'
          '<p class="fig-caption"><strong>Fig. 2.9</strong> &mdash; Set-up to demonstrate osmosis.</p>\n' % (F.dialysis(), F.dialysis(after=True)))
    b += '<p><strong>Observation and discussion</strong></p>'
    b += answers(
        ("What do you notice about the dialysis tubing after 20 minutes? Explain your observation.",
         "The tubing swells and becomes firm, and the liquid level inside it rises. The distilled water outside has a higher water potential than the sucrose solution inside. "
         "Water molecules move into the tubing by osmosis, through the partially permeable tubing. Sucrose molecules are too large to move out."),
        ("What is the purpose of the second set-up (distilled water inside and outside)?",
         "It is a <strong>control</strong>. With no difference in water potential, the level does not change. "
         "This shows that the rise in the first set-up is caused by the sucrose solution (the water potential gradient), not by the tubing itself."))
    b += '</div>\n'
    b += S.sim("sim-bag", "bag", "Example 3: Visking tubing becomes turgid or flaccid",
               "The Visking tubing holds a sucrose solution. Choose what the tubing stands in, then press <strong>Start</strong>.",
               '<i style="background:#f97316"></i>sucrose molecule <i style="background:#60a5fa"></i>water molecule',
               presets=["Outside: distilled water", "Outside: concentrated sucrose solution"],
               only="Only water molecules can pass through the tubing. Sucrose molecules are too large to pass through.", height=380)

    b += '<h2>What is water potential?</h2>\n'
    b += ('<p>When we talk about osmosis we use the term <strong>water potential</strong>. Water potential is a measure of how likely water molecules are to move from one place to another.</p>\n'
          '<ul><li>Water molecules tend to move from a <strong>dilute</strong> solution (less solute) to a <strong>more concentrated</strong> solution.</li>'
          '<li>So a <strong>dilute</strong> solution has a <strong>higher</strong> water potential than a concentrated solution. Pure (distilled) water has the highest water potential of all.</li>'
          '<li>When a partially permeable membrane separates two solutions with different water potentials, a <strong>water potential gradient</strong> is set up. '
          'Water molecules move from the region of higher water potential to the region of lower water potential: <strong>down</strong> the water potential gradient.</li></ul>\n')
    b += L.fig(F.wp_container(), "A water potential gradient across a partially permeable membrane.", "2.10")
    b += L.fig(F.wp_graph(), "Water moves from a dilute solution (higher water potential) to a concentrated solution (lower water potential).", "2.11")
    b += ('<p class="defn"><strong>Osmosis</strong> is the net movement of water molecules from a region of higher water potential to a region of lower water potential, '
          'through a partially permeable membrane.</p>\n')
    b += ('<p class="common"><strong>Common mistakes:</strong> in osmosis it is the <em>water</em> that moves, not the solute. '
          'More solute means <em>lower</em> water potential. Always mention the <em>partially permeable membrane</em> in your answer.</p>\n')
    b += L.video("vCJVXYmXkzM", "Video: Osmosis", "YouTube: Cognito",
                 "This video talks about &ldquo;water concentration&rdquo;. In our course we say <strong>water potential</strong>: a higher water concentration means a higher water potential.")

    # ---- plant cells
    b += '<h2>What happens to plant cells in different solutions?</h2>\n'
    b += '<p>The cell sap in the vacuole of a plant cell is a solution. Whether water goes in or out depends on the water potential of the solution outside the cell.</p>\n'
    b += ('<table class="cellcmp"><tr><th></th><th>Plant cell in a solution of <strong>higher</strong> water potential (e.g. distilled water)</th>'
          '<th>Plant cell in a solution of <strong>lower</strong> water potential (e.g. concentrated sugar solution)</th></tr>'
          '<tr><th>Water potential of cell sap compared with the solution outside</th><td>Lower than the solution outside.</td><td>Higher than the solution outside.</td></tr>'
          '<tr><th>Movement of water by osmosis</th><td>Water molecules <strong>enter</strong> the cell through the partially permeable cell membrane.</td>'
          '<td>Water molecules <strong>leave</strong> the vacuole and cytoplasm through the partially permeable cell membrane.</td></tr>'
          '<tr><th>What happens to the cell</th><td>The vacuole gets bigger and pushes the cytoplasm against the cell wall. The cell does <strong>not burst</strong>, because the strong, '
          'inelastic cell wall protects it. The pressure of the water in the vacuole is the <strong>turgor pressure</strong>.%s</td>'
          '<td>The vacuole gets smaller. The cytoplasm shrinks and the cell membrane pulls away from the cell wall. This is called <strong>plasmolysis</strong>; the cell is <strong>plasmolysed</strong>.%s</td></tr>'
          '<tr><th>Result</th><td>The cell swells and becomes <strong>turgid</strong> (its firmness is called <strong>turgor</strong>).</td>'
          '<td>The cell shrinks and becomes <strong>flaccid</strong> (limp).</td></tr></table>\n'
          % (F.plant_cell("turgid"), F.plant_cell("plasmolysed")))
    b += '<p class="fig-caption">Blue arrows: the direction water moves by osmosis. Cell drawings not to scale.</p>\n'
    b += ('<p>A plasmolysed cell can recover. If it is put back into water (or a solution of higher water potential) soon enough, water enters by osmosis and the cell becomes turgid again.</p>\n')
    b += ('<div class="two-col">'
          '<figure class="pic"><img src="img/red-onion-plasmolysis-lm.jpg" alt="Red onion epidermis cells under a microscope; in many cells the purple contents have shrunk away from the cell wall" loading="lazy">'
          '<figcaption>Red onion cells in a concentrated salt solution. Look for cells where the coloured contents have shrunk away from the cell wall: these cells are <strong>plasmolysed</strong>.</figcaption></figure>'
          '<figure class="pic"><img src="img/rhoeo-plasmolysis-lm.jpg" alt="Close-up of four plant cells; in each one the pink vacuole and cytoplasm have shrunk into a rounded shape, leaving clear space next to the cell wall" loading="lazy">'
          '<figcaption>Close-up of plasmolysed cells. The pink vacuole has shrunk and the cell membrane has pulled away from the cell wall. The clear gaps are filled with the outside solution.</figcaption></figure></div>\n'
          '<p class="credit">Images: <a href="%sPlasmolysis_of_red_onion_(Allium_cepa)_cells.jpg">Tr&#432;&#417;ng Minh Kh&#7843;i</a>, CC BY 4.0; '
          '<a href="%sRhoeo_Discolor_-_Plasmolysis.jpg">Mnolf</a>, CC BY-SA 3.0; via Wikimedia Commons.</p>\n' % (C, C))
    b += L.labeller("lab-plasmo", F.plasmo_inner(), F.PLASMO_VB[0], F.PLASMO_VB[1], F.PLASMO_TARGETS, "A plasmolysed plant cell.",
                    title="Label a plasmolysed plant cell.", width=520)

    # ---- animal cells
    b += '<h2>What happens to animal cells in different solutions?</h2>\n'
    b += ('<table class="cellcmp"><tr><th></th><th>Animal cell in a solution of <strong>higher</strong> water potential</th><th>Animal cell in a solution of <strong>lower</strong> water potential</th></tr>'
          '<tr><th>Water potential of cytoplasm compared with the solution outside</th><td>Lower than the solution outside.</td><td>Higher than the solution outside.</td></tr>'
          '<tr><th>Movement of water by osmosis</th><td>Water molecules move <strong>into</strong> the cell.</td><td>Water molecules move <strong>out of</strong> the cell.</td></tr>'
          '<tr><th>What happens to the cell</th><td>The cell swells and may <strong>burst</strong>. Unlike a plant cell, it has no cell wall to protect it.'
          '<div class="rbcrow">%s<b>&rarr;</b>%s<b>&rarr;</b>%s</div><p class="fig-caption">normal &rarr; swells &rarr; bursts</p></td>'
          '<td>The cell shrinks and spikes appear on its surface. This is called <strong>crenation</strong>. The cell becomes dehydrated and will die if it stays there.'
          '<div class="rbcrow">%s<b>&rarr;</b>%s</div><p class="fig-caption">normal &rarr; crenated (shrunken, with spikes)</p></td></tr></table>\n'
          % (F.rbc("normal"), F.rbc("swollen"), F.rbc("burst"), F.rbc("normal"), F.rbc("crenated")))
    b += ('<p><strong>In a solution with the same water potential</strong> as its cytoplasm, a cell does not change size or shape. '
          'Water molecules move in and out at the same rate, so there is <strong>no net movement</strong> of water. This is why medical drips and eye drops are made with the same water potential as body fluids.</p>\n')
    b += ('<figure class="pic"><img src="img/rbc-osmosis-lm.jpg" alt="Three microscope photos of red blood cells side by side: left, shrunken cells with spiky edges; middle, normal disc-shaped cells; right, swollen round cells" loading="lazy">'
          '<figcaption>Real red blood cells (light micrographs). <strong>Left:</strong> in a solution of lower water potential: crenated, with spikes. '
          '<strong>Middle:</strong> in a solution of the same water potential: normal discs. <strong>Right:</strong> in a solution of higher water potential: swollen and round.</figcaption></figure>\n'
          '<p class="credit">Image: <a href="%sHuman_Erythrocytes_OsmoticPressure_PhaseContrast_Plain.svg">Zephyris</a>, CC BY-SA 3.0, via Wikimedia Commons.</p>\n' % C)
    b += L.sorter("sort-cells", "Try it: what happens to the cell?", "Choose what happens in each case.", ["Becomes turgid", "Plasmolysed", "Bursts", "Crenated", "No change"], [
        ("Onion cell placed in distilled water", 0, "Water enters by osmosis; the cell wall stops it bursting, so it becomes turgid."),
        ("Onion cell placed in concentrated salt solution", 1, "Water leaves by osmosis and the cell membrane pulls away from the cell wall."),
        ("Red blood cell placed in distilled water", 2, "Water enters by osmosis and there is no cell wall, so the cell bursts."),
        ("Red blood cell placed in concentrated salt solution", 3, "Water leaves by osmosis; the cell shrinks and grows spikes."),
        ("Red blood cell placed in a solution with the same water potential as its cytoplasm", 4, "No net movement of water, so the cell keeps its shape."),
    ])

    # ---- turgor
    b += '<h2>Why is turgor important to plants?</h2>\n'
    b += ('<p><strong>Support.</strong> Turgor keeps soft plant parts firm. Young stems and the leaves of non-woody plants stay firm and upright because of the turgor pressure in their cells. '
          'If the cells lose too much water, they lose turgor, become flaccid, and the plant <strong>wilts</strong>.</p>\n')
    b += L.fig(F.wilting(), "Turgor pressure keeps a young plant upright; losing turgor makes it wilt.", "2.12")
    b += ('<p><strong>Movement.</strong> Changes in turgor make some plant parts move. For example, a stoma (a tiny pore in a leaf) opens and closes '
          'when its two <strong>guard cells</strong> gain or lose turgor.</p>\n')
    b += ('<figure class="pic cellphoto"><img src="img/stoma-sem.jpg" alt="Electron micrograph of a leaf surface showing one stoma: an oval pore between two curved guard cells" loading="lazy">'
          '<figcaption>A stoma on a tomato leaf (scanning electron micrograph, colour added). When the two guard cells around the pore become turgid, the stoma opens.</figcaption></figure>\n'
          '<p class="credit">Image: <a href="%sTomato_leaf_stomate_1-color.jpg">Photohound</a>, public domain, via Wikimedia Commons.</p>\n' % C)
    b += ('<p><strong>Too much fertiliser.</strong> Plasmolysed cells die if they stay plasmolysed for too long. If too much fertiliser is added around a plant, '
          'the <strong>soil solution</strong> (the thin layer of water around soil particles, with dissolved mineral salts) becomes very concentrated. '
          'Its water potential becomes lower than that of the root cells, so water moves <strong>out</strong> of the roots by osmosis. '
          'The roots cannot absorb water while the leaves keep losing water by evaporation, so the plant wilts and will die unless the soil solution is diluted with water.</p>\n')

    # ---- factors and the potato practical (pages not yet seen: check against the textbook)
    b += '<h2>Factors that affect the rate of osmosis</h2>\n'
    b += ('<p>Osmosis is the diffusion of water, so it is affected by the same kinds of factors as diffusion:</p>\n'
          '<ul><li><strong>Water potential gradient:</strong> the bigger the difference in water potential across the membrane, the faster the rate of osmosis.</li>'
          '<li><strong>Distance:</strong> the shorter the distance the water molecules must travel, the faster the rate.</li>'
          '<li><strong>Surface area to volume ratio:</strong> the larger the SA&nbsp;:&nbsp;V of the cell or tissue, the faster water moves in or out.</li></ul>\n')
    b += ('<div class="practical"><h3>Practical: effect of osmosis on plant tissue</h3>'
          '<ol><li>Cut potato strips of the same size (for example 5 cm long), without skin. Measure the length (or mass) of each strip.</li>'
          '<li>Put one strip into each of: distilled water, a dilute sucrose solution and a concentrated sucrose solution.</li>'
          '<li>After 30 minutes, take the strips out, blot them dry and measure them again. Feel how firm or soft they are.</li></ol>'
          '<p><strong>Results:</strong> in distilled water the strip gets <strong>longer</strong> and firm (water enters the cells by osmosis; the cells become turgid). '
          'In the concentrated solution it gets <strong>shorter</strong> and soft (water leaves the cells by osmosis; the cells become flaccid or plasmolysed). '
          'Work out the <strong>percentage change</strong> so strips of different starting sizes can be compared.</p>'
          '<p class="formula">percentage change = (final length &minus; starting length) &divide; starting length &times; 100%</p></div>\n')
    b += L.calc("A", "A potato strip was 5.0 cm long. After 30 minutes in a concentrated sucrose solution it was 4.6 cm long. Work out the percentage change in length (use a minus sign for a decrease).",
                -8, 0.05, "%", "(4.6 &minus; 5.0) &divide; 5.0 &times; 100 = &minus;8%. The strip lost water by osmosis because the solution had a lower water potential than the potato cells.")

    b += '<h2>Check your understanding</h2>\n'
    b += L.mcq(1, "Which is the correct definition of osmosis?", [
        "The net movement of solute molecules from a region of higher water potential to a region of lower water potential",
        "The net movement of water molecules from a region of higher water potential to a region of lower water potential, through a partially permeable membrane",
        "The net movement of water molecules from a region of lower water potential to a region of higher water potential, through a partially permeable membrane",
        "The movement of any particles through a fully permeable membrane"], 1,
        "Osmosis: water molecules, from higher to lower water potential, through a partially permeable membrane.")
    b += L.mcq(2, "Which solution has the highest water potential?", ["Distilled water", "5% sucrose solution", "10% sucrose solution", "20% sucrose solution"], 0,
               "Pure water has the highest water potential. The more solute, the lower the water potential.")
    b += L.mcq(3, "In the U-tube experiment (Fig. 2.8), why does the level in arm A rise?", [
        "Sucrose moves from B to A.", "Water moves from A to B.", "Water moves from B to A by osmosis.", "Sucrose molecules grow bigger."], 2,
        "B has the higher water potential. Water moves from B to A through the partially permeable membrane; sucrose is too big to cross.")
    b += L.mcq(4, "A plant cell is placed in distilled water. Why does it not burst?", [
        "Its vacuole shrinks.", "Its strong, inelastic cell wall stops it from bursting.", "Water cannot enter a plant cell.", "Its cell membrane is fully permeable."], 1,
        "Water enters by osmosis and the cell becomes turgid, but the cell wall withstands the turgor pressure.")
    b += L.mcq(5, "What is plasmolysis?", [
        "When a red blood cell bursts", "When the cytoplasm shrinks and the cell membrane pulls away from the cell wall",
        "When a plant cell swells and becomes turgid", "When spikes form on a red blood cell"], 1,
        "Plasmolysis happens to plant cells that lose water by osmosis in a solution of lower water potential.")
    b += L.mcq(6, "Red blood cells are put into a concentrated salt solution. What will happen?", [
        "They swell and burst.", "They become turgid.", "They shrink and become crenated.", "Nothing."], 2,
        "The solution has a lower water potential than the cytoplasm, so water leaves by osmosis and the cells shrink with spikes (crenation).")
    b += L.mcq(7, "A farmer adds far too much fertiliser to the soil. Why might the crop wilt?", [
        "The soil solution has a lower water potential than the root cells, so water leaves the roots by osmosis.",
        "The fertiliser blocks the stomata.", "The soil solution has a higher water potential than the root cells.", "The roots take in too much water."], 0,
        "A concentrated soil solution has a low water potential, so water moves out of the roots by osmosis and the plant cannot replace the water lost from its leaves.")
    b += L.mcq(8, "In the dialysis tubing practical, why is a second set-up with distilled water inside and outside the tubing used?", [
        "To make the experiment faster", "As a control, to show that the change is caused by the sucrose solution", "To kill bacteria", "To measure the temperature"], 1,
        "With no water potential gradient, the level does not change. This shows the sucrose solution causes the change.")
    L.page("movement-2-2-osmosis", "2.2 What Is Osmosis?", REFS + "2b", CSS + L.LABEL_CSS + b, JS, topic=TOPIC)


if __name__ == "__main__":
    lesson1()
    lesson2()
