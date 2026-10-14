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
    """Multiple choice. ans = index (from 0) of the correct option. img = (file name without .jpg, alt text)."""
    h = '<div class="checkpoint" data-type="mcq" data-answer="%d">\n  <p class="q">%d. %s</p>\n' % (ans, n, q)
    if figure:
        h += '  <div class="q-fig">%s</div>\n' % figure
    if img:
        h += '  <div class="q-fig"><img src="img/%s.jpg" alt="%s" style="display:block;margin:0 auto;max-width:460px;width:100%%;border-radius:8px"></div>\n' % (img[0], html.escape(img[1], quote=True))
    if grid:
        h += '  <div class="opt-grid">\n'
    for i, o in enumerate(opts):
        h += '  <label><input type="radio" name="q%d" value="%d"> %s</label>\n' % (n, i, o)
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
