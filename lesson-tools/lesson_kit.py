#!/usr/bin/env python3
"""Shared pieces for building lesson pages: page shell, question helpers, picture helpers and the intro-video block.
Change SUBJECT and BADGE below for your subject. All HTML pages are written to ../lessons/.

  import lesson_kit as L
  body = L.mcq(1, "Question?", ["A", "B", "C", "D"], 0, "Why A is right") + L.calc(2, "2 + 2 = ?", 4, 0.05, "", "It is 4")
  L.page("topic-01-name", "Lesson title", "Syllabus refs: ...", body, topic="Topic name")
"""
import os, re, html

SUBJECT = "Biology"        # shown on the back link and the meta line
BADGE = "G3 only"   # badge for lessons only G3 classes study (page(..., badge=True))

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LESSONS = os.path.join(ROOT, "lessons")

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lesson_style.html"), encoding="utf-8").read()
CSS += """<style>
  .g3-badge { display: inline-block; background: linear-gradient(135deg, #c2185b, #c2410c); color: #fff; font-weight: 800; font-size: 0.72rem; padding: 0.22rem 0.8rem; border-radius: 999px; letter-spacing: 0.02em; vertical-align: middle; margin-left: 0.5rem; }
  h1 .g3-badge { font-size: 0.8rem; }
  .photo .capbar.one { grid-template-columns: 1fr; }
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&display=swap">
<style>
  /* biology site: body font, G2/G3 switch (set on the home page), shared boxes */
  body { font-family: "Source Sans 3", system-ui, sans-serif; font-size: 1.08rem; }
  .g2 .g3-only { display: none !important; }
  .keyidea { border-left: 4px solid #94a3b8; padding: 0.2rem 0 0.2rem 1rem; margin: 1rem 0; color: #334155; }
  .practical { border: 1px solid #a7f3d0; background: #f0fdf4; border-radius: 10px; padding: 0.9rem 1.2rem; margin: 1.2rem 0; }
  .practical h3 { margin: 0.2rem 0 0.4rem; color: #166534; font-size: 1.1rem; }
  .flow { display: flex; flex-wrap: wrap; align-items: center; gap: 0.4rem; margin: 1rem 0; }
  .flow span { padding: 0.45rem 0.9rem; border-radius: 999px; background: #f0fdfa; border: 1px solid #99f6e4; font-weight: 600; color: #134e4a; }
  .flow b { color: #db2777; }
  .two-col { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 0.5rem 1.2rem; align-items: start; }
  .eg-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.9rem 1.1rem; margin: 0.5rem 0; } .eg-box .q { font-weight: 700; margin-top: 0; }
  .three-col { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.5rem 1rem; align-items: start; }
  .three-col svg { width: 100%; max-width: 240px; }
  .tag-p { color: #15803d; font-weight: 700; } .tag-a { color: #be185d; font-weight: 700; } .tag-b { color: #1d4ed8; font-weight: 700; }
  /* clickable diagram (explorer) */
  .explorer { margin: 1.25rem 0; border: 1px solid #e2e8f0; border-radius: 12px; padding: 0.8rem 0.9rem 0.6rem; background: #fff; }
  .explorer svg { margin: 0.3rem auto; }
  .explorer .part, .explorer .lbl { cursor: pointer; }
  .explorer .part:hover, .explorer .lbl:hover { filter: brightness(1.06) saturate(1.2); }
  .explorer .part.on { filter: drop-shadow(0 0 3px #f59e0b) drop-shadow(0 0 2px #f59e0b); }
  .explorer .lbl.on text { fill: #b45309; }
  .explorer .part:focus, .explorer .lbl:focus { outline: none; }
  .explorer .part:focus-visible, .explorer .lbl:focus-visible { filter: drop-shadow(0 0 3px #0f766e) drop-shadow(0 0 2px #0f766e); }
  .explorer.nolabels .lbl text { visibility: hidden; }
  .ex-ctl { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; }
  .ex-ctl button { min-height: 2.6rem; padding: 0 1rem; border: 1px solid #94a3b8; border-radius: 999px; background: #fff; color: #134e4a; font-weight: 700; font-family: inherit; font-size: 0.95rem; cursor: pointer; }
  .ex-ctl button[aria-pressed="true"] { background: #134e4a; color: #fff; border-color: #134e4a; }
  .ex-q { font-weight: 700; color: #134e4a; }
  .ex-info { min-height: 3.2rem; padding: 0.6rem 0.9rem; border-radius: 8px; background: #f0fdfa; border: 1px solid #99f6e4; }
  .ex-info.ok { background: #dcfce7; border-color: #86efac; } .ex-info.no { background: #fee2e2; border-color: #fca5a5; }
  @media print { .explorer { border: none; padding: 0; } .ex-ctl, .ex-info { display: none !important; } .explorer.nolabels .lbl text { visibility: visible; } }
</style>
"""

NAV = '<p class="site-nav"><a href="index.html">&larr; Back to %s lessons</a></p>\n' % SUBJECT
BACK = '<p class="back-bottom print-hide"><a class="back-btn" href="index.html">&larr; Back to %s lessons</a></p>\n' % SUBJECT

CHECK_JS = """function checkAnswer(btn) {
  const block = btn.closest('.checkpoint');
  const feedback = block.querySelector('.feedback');
  const correctAns = block.dataset.answer;
  const tol = parseFloat(block.dataset.tol || '0.05');
  let isCorrect;

  if (block.dataset.type === 'mcq') {
    const checked = block.querySelector('input[type=radio]:checked');
    if (!checked) { showHint(feedback, 'Pick an answer first.'); return; }
    isCorrect = checked.value === correctAns;
  } else {
    const val = parseFloat(block.querySelector('input[type=text]').value);
    if (isNaN(val)) { showHint(feedback, 'Enter a number first.'); return; }
    isCorrect = Math.abs(val - parseFloat(correctAns)) <= tol;
  }

  feedback.className = 'feedback ' + (isCorrect ? 'correct' : 'incorrect');
  feedback.textContent = (isCorrect ? '\\u2713 Correct. ' : '\\u2717 Not quite. ') + feedback.dataset.explanation;
}

function showHint(feedback, text) {
  feedback.className = 'feedback hint';
  feedback.textContent = text;
}
"""


def page(fname, title, meta, body, js="", badge=False, topic=""):
    """Writes lessons/<fname>.html. meta: text after the topic on the grey line under the title."""
    b = ' <span class="g3-badge">%s</span>' % BADGE if badge else ""
    out = ['<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="color-scheme" content="light">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>%s</title>\n' % title]
    out.append('<script>try { if (localStorage.getItem("bio-level") === "g2") document.documentElement.className += " g2"; } catch (e) {}</script>\n')
    out.append(CSS)
    out.append('</head>\n<body>\n' + NAV + '<main>\n')
    out.append('<h1>%s%s</h1>\n' % (title, b))
    out.append('<p class="meta">%s &middot; %s &middot; %s</p>\n' % (SUBJECT, topic, meta))
    out.append('<p class="print-only">Name: ______________________ &nbsp; Class: ________ &nbsp; Date: ____________</p>\n')
    out.append('<p class="print-hide"><a class="pdf-btn" href="%s.pdf" target="_blank" rel="noopener">&#128196; Download printable version (PDF)</a></p>\n' % fname)
    out.append(body)
    out.append('</main>\n' + BACK)
    out.append('<script>\n' + CHECK_JS + js + '</script>\n</body>\n</html>\n')
    open(os.path.join(LESSONS, fname + ".html"), "w", encoding="utf-8").write("".join(out))
    print("wrote", fname)


# ------------------------------------------------------------------ content helpers
def photo(img, alt, chips=None, cap=None):
    """A photo-style image (lessons/img/<img>.jpg) with optional labels (chips) on the picture and a caption bar under it."""
    h = '<div class="photo">\n  <img src="img/%s.jpg" alt="%s" loading="lazy">\n' % (img, html.escape(alt, quote=True))
    if chips:
        h += '  <span class="chip l">%s</span>' % chips[0]
        if len(chips) > 1:
            h += '<span class="chip r">%s</span>' % chips[1]
        h += "\n"
    if cap:
        if isinstance(cap, str):
            h += '  <div class="capbar one"><div class="l">%s</div></div>\n' % cap
        else:
            h += '  <div class="capbar"><div class="l">%s</div><div class="r">%s</div></div>\n' % cap
    h += '</div>\n<p class="photo-note">AI-generated illustration, not to scale. The labels are added by the teacher.</p>\n'
    return h


def pic(img, alt, cap):
    return ('<figure class="pic">\n  <img src="img/%s.jpg" alt="%s" loading="lazy">\n  <figcaption>%s <em>(AI-generated illustration)</em></figcaption>\n</figure>\n'
            % (img, html.escape(alt, quote=True), cap))


def fig(svg, caption, n=None):
    """An inline SVG drawing with a caption."""
    lab = "<strong>Fig. %s</strong> &mdash; " % n if n else ""
    return '<div class="illus">%s<p class="fig-caption">%s%s</p></div>\n' % (svg, lab, caption)


def video(vid, title, credit, note=None):
    """A YouTube embed (privacy-friendly youtube-nocookie domain)."""
    h = '<div class="video-block">\n  <p>%s <span class="vid-credit">(%s)</span></p>\n' % (title, credit)
    if note:
        h += '  <p class="vid-note">%s</p>\n' % note
    h += ('  <iframe src="https://www.youtube-nocookie.com/embed/%s" title="%s" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture; web-share" '
          'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>\n</div>\n' % (vid, html.escape(title, quote=True)))
    return h


def mcq(n, q, opts, ans, expl, figure="", img=None, grid=False):
    """Multiple choice. ans = index (from 0) of the correct option. img = (file name without .jpg, alt text).
    n is shown as the question number; it can also be text such as "A" (keep it unique on the page)."""
    h = '<div class="checkpoint" data-type="mcq" data-answer="%d">\n  <p class="q">%s. %s</p>\n' % (ans, n, q)
    if figure:
        h += '  <div class="q-fig">%s</div>\n' % figure
    if img:
        h += '  <div class="q-fig"><img src="img/%s.jpg" alt="%s" style="display:block;margin:0 auto;max-width:460px;width:100%%;border-radius:8px"></div>\n' % (img[0], html.escape(img[1], quote=True))
    if grid:
        h += '  <div class="opt-grid">\n'
    for i, o in enumerate(opts):
        h += '  <label><input type="radio" name="q%s" value="%d"> %s</label>\n' % (n, i, o)
    if grid:
        h += '  </div>\n'
    h += ('  <button type="button" onclick="checkAnswer(this)">Check answer</button>\n  <div class="feedback" aria-live="polite" data-explanation="%s"></div>\n</div>\n'
          % html.escape(expl, quote=True))
    return h


def calc(n, q, ans, tol, unit, expl, figure="", img=None):
    """A question with a number as the answer. Answers within +/- tol count as correct."""
    h = '<div class="checkpoint" data-type="calculation" data-answer="%s" data-tol="%s">\n  <p class="q">%d. %s</p>\n' % (ans, tol, n, q)
    if figure:
        h += '  <div class="q-fig">%s</div>\n' % figure
    if img:
        h += '  <div class="q-fig"><img src="img/%s.jpg" alt="%s" style="display:block;margin:0 auto;max-width:460px;width:100%%;border-radius:8px"></div>\n' % (img[0], html.escape(img[1], quote=True))
    h += ('  <input type="text" inputmode="decimal" placeholder="Your answer (%s)" aria-label="Your answer in %s">\n'
          '  <button type="button" onclick="checkAnswer(this)">Check answer</button>\n  <div class="feedback" aria-live="polite" data-explanation="%s"></div>\n</div>\n'
          % (unit, unit, html.escape(expl, quote=True)))
    return h


# ------------------------------------------------------------------ intro video (autoplay with sound, subtitles, click-for-sound fallback)
_INTRO = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "intro_video_block.html"), encoding="utf-8").read()


def intro_video(prefix, mp4, poster, alt, caption, subtitle, sub_start):
    """The block for the top of a lesson: a short AI video that tries to autoplay with sound, with a subtitle that appears at sub_start
    (seconds) and a 'Subtitles' toggle. If the browser blocks sound, it plays muted with a 'Click for sound' button.
    prefix: 2-3 letters used in the element ids (unique per page). Files live in lessons/intro/."""
    s = _INTRO
    for k, v in (("@PREFIX@", prefix), ("@MP4@", mp4), ("@POSTER@", poster), ("@ALT@", html.escape(alt, quote=True)), ("@CAPTION@", caption),
                 ("@SUBTITLE_JS@", subtitle.replace("\\", "\\\\").replace("'", "\\'").replace("\u2019", "\\u2019")), ("@SUBSTART@", str(sub_start))):
        s = s.replace(k, v)
    return s


# ------------------------------------------------------------------ clickable diagram and sorting activity
def explorer(eid, svg, info, caption, prompt="Click any part of the diagram to see what it does."):
    """A diagram whose parts can be clicked. In the SVG, wrap each part in <g class="part" data-part="key"> and each label in
    <g class="lbl" data-part="key"> (several groups may share a key, e.g. many mitochondria). info = {key: (name, what it does)}.
    Students can hide the labels and play 'Quiz me' (find the named part). In print the labels always show. Needs EXPLORER_JS on the page."""
    import json
    return ('<div class="explorer" id="%s" data-info="%s">\n'
            '  <div class="ex-ctl print-hide"><button type="button" data-act="labels" aria-pressed="false">Hide labels</button>'
            '<button type="button" data-act="quiz" aria-pressed="false">Quiz me: find the part</button><span class="ex-q" aria-live="polite"></span></div>\n'
            '  %s\n  <div class="ex-info" aria-live="polite">%s</div>\n  <p class="fig-caption">%s</p>\n</div>\n'
            % (eid, html.escape(json.dumps(info), quote=True), svg, prompt, caption))


EXPLORER_JS = r"""
document.querySelectorAll('.explorer').forEach(function (ex) {
  var info = JSON.parse(ex.dataset.info), box = ex.querySelector('.ex-info'), qline = ex.querySelector('.ex-q');
  var bL = ex.querySelector('[data-act=labels]'), bQ = ex.querySelector('[data-act=quiz]');
  var quiz = null, score = 0, tries = 0, keys = Object.keys(info);
  ex.querySelectorAll('.part, .lbl').forEach(function (g) {
    g.setAttribute('tabindex', '0'); g.setAttribute('role', 'button');
    if (!g.getAttribute('aria-label')) g.setAttribute('aria-label', info[g.dataset.part][0]);
    g.addEventListener('click', function () { pick(g.dataset.part); });
    g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(g.dataset.part); } });
  });
  function light(k) { ex.querySelectorAll('.part, .lbl').forEach(function (g) { g.classList.toggle('on', g.dataset.part === k); }); }
  function show(k) { box.className = 'ex-info'; box.innerHTML = '<strong>' + info[k][0] + ':</strong> ' + info[k][1]; light(k); }
  function ask() { var k; do { k = keys[Math.floor(Math.random() * keys.length)]; } while (keys.length > 1 && k === quiz); quiz = k; qline.textContent = 'Find: ' + info[k][0] + '  (score ' + score + '/' + tries + ')'; light(null); }
  function pick(k) {
    if (!quiz) { show(k); return; }
    tries++;
    if (k === quiz) { score++; box.className = 'ex-info ok'; box.innerHTML = '✓ Yes, that is the <strong>' + info[k][0] + '</strong>. ' + info[k][1]; light(k); setTimeout(ask, 1400); }
    else { box.className = 'ex-info no'; box.innerHTML = '✗ That is the <strong>' + info[k][0] + '</strong>. Try again: find the ' + info[quiz][0] + '.'; }
    qline.textContent = 'Find: ' + info[quiz][0] + '  (score ' + score + '/' + tries + ')';
  }
  bL.addEventListener('click', function () { var on = bL.getAttribute('aria-pressed') !== 'true'; bL.setAttribute('aria-pressed', on); ex.classList.toggle('nolabels', on); bL.textContent = on ? 'Show labels' : 'Hide labels'; });
  bQ.addEventListener('click', function () {
    var on = bQ.getAttribute('aria-pressed') !== 'true'; bQ.setAttribute('aria-pressed', on);
    if (on) { score = 0; tries = 0; if (bL.getAttribute('aria-pressed') !== 'true') bL.click(); ask(); bQ.textContent = 'Stop quiz'; }
    else { quiz = null; qline.textContent = ''; bQ.textContent = 'Quiz me: find the part'; box.className = 'ex-info'; box.textContent = 'Click any part of the diagram to see what it does.'; }
  });
});
"""


def sorter(sid, title, intro, cats, items):
    """Sorting activity: each item gets one button per category. items = [(name, index of the right category, explanation)].
    Needs SORT_JS on the page. Hidden in print."""
    h = '<div class="tool sorter" id="%s">\n  <h3>%s</h3>\n  <p>%s</p>\n' % (sid, title, intro)
    for name, ans, expl in items:
        h += '  <div class="sort-item" data-ans="%d"><span class="name">%s</span>%s<span class="fb" data-expl="%s"></span></div>\n' % (
            ans, name, "".join('<button type="button" data-c="%d">%s</button>' % (i, c) for i, c in enumerate(cats)), html.escape(expl, quote=True))
    return h + '  <p class="score" aria-live="polite"></p>\n</div>\n'


SORT_JS = r"""
document.querySelectorAll('.sorter').forEach(function (s) {
  var items = s.querySelectorAll('.sort-item'), sc = s.querySelector('.score');
  function tally() { var n = s.querySelectorAll('.sort-item.right').length; sc.textContent = n + ' of ' + items.length + ' sorted correctly' + (n === items.length ? '. Well done!' : '.'); }
  items.forEach(function (it) {
    var fb = it.querySelector('.fb');
    it.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        var ok = b.dataset.c === it.dataset.ans;
        it.classList.toggle('right', ok); it.classList.toggle('wrong', !ok); fb.classList.add('show');
        fb.textContent = ok ? '✓ Correct. ' + fb.dataset.expl : '✗ Not quite. Try another button.';
        tally();
      });
    });
  });
  tally();
});
"""


# ------------------------------------------------------------------ drag-and-drop labelling
def labeller(lid, svg_inner, vw, vh, targets, caption, extra=(), title="Label the diagram", width=560):
    """Drag-and-drop labelling. svg_inner: the drawing or <image> (no text labels) in a viewBox of vw x vh.
    targets: list of dict(key, label, pt=(x, y) the part, box=(x, y) where the label box goes, side='l'|'r'|'c').
    Leader lines run from the box to the part. extra: distractor labels for the word bank.
    Students drag a label onto a box (or tap a label, then tap a box). Works with mouse, touch and keyboard.
    In print the boxes are blank and the word bank is listed, so the PDF is a labelling worksheet. Needs LABEL_JS."""
    import random
    lines = ""
    boxes = ""
    for i, t in enumerate(targets):
        (px, py), (bx, by), side = t["pt"], t["box"], t.get("side", "l")
        lines += ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#334155" stroke-width="1.5"/><circle cx="%s" cy="%s" r="3" fill="#0f172a" stroke="#fff" stroke-width="1"/>'
                  % (bx, by, px, py, px, py))
        pos = "left:%.2f%%;top:%.2f%%" % (100.0 * bx / vw, 100.0 * by / vh)
        boxes += ('<button type="button" class="drop %s" data-ans="%s" style="%s" aria-label="Empty label box %d"><span class="n">%d</span><span class="v"></span></button>'
                  % (side, t["key"], pos, i + 1, i + 1))
    words = [(t["key"], t["label"]) for t in targets] + [("x%d" % i, w) for i, w in enumerate(extra)]
    random.Random(lid).shuffle(words)
    bank = "".join('<button type="button" class="chip" data-key="%s">%s</button>' % (k, w) for k, w in words)
    return ('<div class="labeller" id="%s">\n  <p class="lab-title"><strong>%s</strong> <span class="print-hide">Drag each label into a box (or tap a label, then tap a box).</span></p>\n'
            '  <div class="bank" aria-label="Labels">%s</div>\n'
            '  <div class="lab-stage" style="max-width:%dpx"><svg viewBox="0 0 %d %d" role="img" aria-label="%s">%s%s</svg>%s</div>\n'
            '  <div class="lab-ctl print-hide"><button type="button" data-act="check">Check my labels</button><button type="button" data-act="show">Show answers</button>'
            '<button type="button" data-act="reset">Start again</button><span class="lab-score" aria-live="polite"></span></div>\n'
            '  <p class="fig-caption">%s</p>\n</div>\n'
            % (lid, title, bank, width, vw, vh, html.escape(caption, quote=True), svg_inner, lines, boxes, caption))


LABEL_CSS = """<style>
  .labeller { margin: 1.25rem 0; border: 1px solid #e2e8f0; border-radius: 12px; padding: 0.8rem 0.9rem; background: #fff; }
  .lab-title { margin: 0 0 0.5rem; }
  .bank { display: flex; flex-wrap: wrap; gap: 0.45rem; padding: 0.6rem; background: #f0fdfa; border: 1px dashed #5eead4; border-radius: 10px; min-height: 2.9rem; }
  .chip { touch-action: none; user-select: none; -webkit-user-select: none; cursor: grab; min-height: 2.4rem; padding: 0 0.85rem; border: 1px solid #0f766e; border-radius: 999px; background: #fff; color: #134e4a; font: 700 0.95rem "Source Sans 3", system-ui, sans-serif; }
  .chip.sel { background: #134e4a; color: #fff; }
  .chip.dragging { position: fixed; z-index: 50; pointer-events: none; box-shadow: 0 6px 18px rgba(0,0,0,0.25); cursor: grabbing; }
  .lab-stage { position: relative; margin: 0.8rem auto 0.3rem; }
  .lab-stage svg { display: block; width: 100%; height: auto; margin: 0; }
  .drop { position: absolute; transform: translate(-100%, -50%); min-width: 7.4em; max-width: 12em; min-height: 2em; padding: 0.15rem 0.45rem; border: 2px dashed #64748b; border-radius: 8px; background: rgba(255,255,255,0.94);
    font: 700 clamp(0.6rem, 1.7vw, 0.92rem)/1.15 "Source Sans 3", system-ui, sans-serif; color: #134e4a; cursor: pointer; text-align: left; display: flex; align-items: center; gap: 0.3rem; }
  .drop.r { transform: translate(0, -50%); } .drop.c { transform: translate(-50%, -50%); }
  .drop .n { flex: 0 0 auto; width: 1.3em; height: 1.3em; border-radius: 50%; background: #e2e8f0; color: #334155; font-size: 0.8em; display: inline-flex; align-items: center; justify-content: center; }
  .drop.filled { border-style: solid; border-color: #0f766e; }
  .drop .v { flex: 1 1 auto; min-width: 0; }
  .drop .chip { min-height: 0; padding: 0; border: 0; border-radius: 0; background: none; font: inherit; color: inherit; text-align: left; white-space: nowrap; }
  .drop .chip.sel { background: #134e4a; color: #fff; border-radius: 4px; padding: 0 0.2rem; }
  .drop.over, .drop.armed:hover { background: #ccfbf1; border-color: #0f766e; }
  .drop.ok { border-color: #16a34a; background: #dcfce7; } .drop.no { border-color: #dc2626; background: #fee2e2; }
  .lab-ctl { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; margin-top: 0.4rem; }
  .lab-ctl button { min-height: 2.6rem; padding: 0 1rem; border: 1px solid #94a3b8; border-radius: 999px; background: #fff; color: #134e4a; font-weight: 700; font-family: inherit; font-size: 0.95rem; cursor: pointer; }
  .lab-ctl button[data-act=check] { background: #0f766e; border-color: #0f766e; color: #fff; }
  .lab-score { font-weight: 700; color: #134e4a; }
  .two-col figure.pic img { height: 340px; object-fit: contain; background: #f1f5f9; }
  ul.spot { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.7rem 1rem 0.7rem 2rem; }
  .scopes img { height: 300px; object-fit: contain; background: #fff; }
  .credit { font-size: 0.8rem; color: #64748b; text-align: center; margin: 0.2rem 0 0; }
  .credit a { color: #64748b; }
  @media (max-width: 560px) { .labeller { padding: 0.7rem 0.4rem; } .lab-stage { width: 74%; } .drop { min-width: 0; width: max-content; max-width: none; padding: 0.1rem 0.25rem; font-size: 0.62rem; } .drop .n { display: none; } .drop:empty, .drop:not(.filled) { min-width: 4.6em; } }
  @media print { .labeller { border: none; padding: 0; break-inside: avoid; } .labeller .bank .chip { display: inline-block !important; min-height: 0; padding: 0.1rem 0.6rem; } .labeller .drop { display: flex !important; } .chip { cursor: default; } .drop .v { visibility: hidden; } .drop { border: 1.5px solid #000; background: #fff; } }
</style>
"""

LABEL_JS = r"""
document.querySelectorAll('.labeller').forEach(function (lab) {
  var bank = lab.querySelector('.bank'), drops = lab.querySelectorAll('.drop'), score = lab.querySelector('.lab-score'), sel = null;
  function clearMarks() { drops.forEach(function (d) { d.classList.remove('ok', 'no'); }); score.textContent = ''; }
  function chipIn(d) { return d.querySelector('.chip'); }
  function place(chip, d) {
    clearMarks();
    if (!d) { bank.appendChild(chip); }
    else { var old = chipIn(d); if (old && old !== chip) bank.appendChild(old); d.querySelector('.v').appendChild(chip); }
    drops.forEach(function (x) { x.classList.toggle('filled', !!chipIn(x)); x.setAttribute('aria-label', chipIn(x) ? 'Label box: ' + chipIn(x).textContent : 'Empty label box'); });
    select(null);
  }
  function select(c) { if (sel) sel.classList.remove('sel'); sel = c; if (c) c.classList.add('sel'); drops.forEach(function (d) { d.classList.toggle('armed', !!c); }); }
  lab.addEventListener('click', function (e) {
    var chip = e.target.closest('.chip'), d = e.target.closest('.drop');
    if (chip && !lab.dataset.dragged) {
      if (chip.parentNode.classList.contains('v') && !sel) { place(chip, null); return; }   // tap a placed label to send it back
      if (sel === chip) { select(null); return; }
      if (sel && d) { place(sel, d); return; }
      select(chip); e.stopPropagation(); return;
    }
    if (d && sel) place(sel, d);
    else if (e.target.closest('.bank') && sel && sel.parentNode.classList.contains('v')) place(sel, null);
  });
  // drag with mouse or finger
  lab.querySelectorAll('.chip').forEach(function (chip) {
    chip.addEventListener('pointerdown', function (e) {
      if (e.button) return;
      var sx = e.clientX, sy = e.clientY, moving = false, ghost = null, over = null;
      function move(ev) {
        if (!moving && Math.hypot(ev.clientX - sx, ev.clientY - sy) < 6) return;
        if (!moving) { moving = true; ghost = chip.cloneNode(true); ghost.classList.add('dragging'); document.body.appendChild(ghost); chip.style.opacity = '0.35'; }
        ghost.style.left = (ev.clientX - ghost.offsetWidth / 2) + 'px'; ghost.style.top = (ev.clientY - ghost.offsetHeight / 2) + 'px';
        var el = document.elementFromPoint(ev.clientX, ev.clientY), d = el && el.closest('.drop');
        if (d && !lab.contains(d)) d = null;
        if (over !== d) { if (over) over.classList.remove('over'); over = d; if (d) d.classList.add('over'); }
        ev.preventDefault();
      }
      function up(ev) {
        document.removeEventListener('pointermove', move); document.removeEventListener('pointerup', up); document.removeEventListener('pointercancel', up);
        if (!moving) return;
        ghost.remove(); chip.style.opacity = ''; if (over) over.classList.remove('over');
        var el = document.elementFromPoint(ev.clientX, ev.clientY), inBank = el && el.closest('.bank') === bank;
        if (over) place(chip, over); else if (inBank) place(chip, null);
        lab.dataset.dragged = '1'; setTimeout(function () { delete lab.dataset.dragged; }, 50);
      }
      document.addEventListener('pointermove', move, { passive: false }); document.addEventListener('pointerup', up); document.addEventListener('pointercancel', up);
    });
  });
  lab.querySelector('[data-act=check]').addEventListener('click', function () {
    var ok = 0, filled = 0;
    drops.forEach(function (d) { var c = chipIn(d); d.classList.remove('ok', 'no'); if (!c) return; filled++; var good = c.dataset.key === d.dataset.ans; if (good) ok++; d.classList.add(good ? 'ok' : 'no'); });
    score.textContent = ok + ' of ' + drops.length + ' correct' + (filled < drops.length ? ' (' + (drops.length - filled) + ' box' + (drops.length - filled === 1 ? '' : 'es') + ' still empty)' : '') + (ok === drops.length ? '. Excellent!' : ok < filled ? '. Move the red ones and check again.' : '. Fill the empty boxes.');
  });
  lab.querySelector('[data-act=show]').addEventListener('click', function () {
    drops.forEach(function (d) { var c = lab.querySelector('.chip[data-key="' + d.dataset.ans + '"]'); if (c) place(c, d); });
    lab.querySelector('[data-act=check]').click();
  });
  lab.querySelector('[data-act=reset]').addEventListener('click', function () { lab.querySelectorAll('.drop .chip').forEach(function (c) { bank.appendChild(c); }); place(bank.firstChild, null); bank.insertBefore(bank.lastChild, bank.firstChild); clearMarks(); });
});
"""
