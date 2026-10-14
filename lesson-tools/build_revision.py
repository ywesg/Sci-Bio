#!/usr/bin/env python3
"""Builds the 'Revision Questions' page for each topic (not Practical Skills).
Section A: about 10 multiple-choice questions (correct letter cycles A-D).
Section B: short-answer and free-response questions. The student writes an answer, clicks 'Check against the mark scheme' and sees which
marking points were detected (they can tick/untick to mark themselves) plus a model answer. If window.AI_MARKING.url is set
(ai-marking-config.js), an 'Ask the AI tutor' button appears and sends only {page, qid, answer} to that service.
Content lives in rev_data_*.py files (see rev_data_sample.py for the format). Usage: python3 build_revision.py"""
import html, json, random, re
import lesson_kit as L
from lesson_kit import mcq as _mcq_base, page

_cnt = [0]
_mcq_plain = _mcq_base


def mcq_cycle(n, q, opts, ans, expl):
    others = [i for i in range(len(opts)) if i != ans]
    random.Random(n * 17 + sum(ord(c) for c in q)).shuffle(others)
    target = _cnt[0] % len(opts)
    _cnt[0] += 1
    order = others[:target] + [ans] + others[target:]
    return _mcq_plain(n, q, [opts[i] for i in order], target, expl)


def pt(text, *groups):
    """A marking point: text shown to the student, then regex groups (all groups must match, case-insensitive)."""
    return {"t": text, "re": list(groups)}


def sb_block(i, qid, q, marks, g3=False):
    tag = ' <span class="g3-badge small">Extended</span>' if g3 else ""
    return ('<div class="sb" data-id="%s" data-marks="%d">\n  <p class="q">%d. %s%s <span class="marks">[%d mark%s]</span></p>\n'
            '  <textarea rows="%d" aria-label="Your answer to question %d" placeholder="Write your answer here. Do not type your name or any personal details."></textarea>\n'
            '  <div class="row print-hide"><button type="button" class="sb-check">Check against the mark scheme</button>'
            '<button type="button" class="sb-ai" hidden>Ask the AI tutor for feedback</button></div>\n'
            '  <div class="sb-out print-hide" hidden></div>\n</div>\n') % (qid, marks, i, q, tag, marks, "" if marks == 1 else "s", 3 + marks, i)


CSS = """<style>
  .sb { border: 1px solid #cbd5e1; border-radius: 10px; padding: 1rem 1.1rem; margin: 1.2rem 0; background: #f8fafc; }
  .sb .q { font-weight: 600; margin-top: 0; }
  .sb .marks { color: #475569; font-weight: 500; white-space: nowrap; }
  .sb textarea { width: 100%; box-sizing: border-box; min-height: 7rem; padding: 0.6rem; border: 1px solid #94a3b8; border-radius: 8px; font: inherit; resize: vertical; background: #fff; }
  .sb .row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.6rem; }
  .sb button { min-height: 2.75rem; padding: 0 1rem; border: 0; border-radius: 8px; background: #0f766e; color: #fff; font-weight: 700; cursor: pointer; }
  .sb button.sb-ai { background: #7c3aed; }
  .sb button:disabled { opacity: .6; cursor: wait; }
  .sb-out { margin-top: 0.8rem; padding: 0.8rem 1rem; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; }
  .sb-out ul { list-style: none; padding: 0; margin: 0.4rem 0; }
  .sb-out li { margin: 0.35rem 0; }
  .sb-out label { cursor: pointer; }
  .sb-score { font-weight: 800; color: #134e4a; }
  .sb-note { color: #475569; font-size: 0.9rem; }
  .sb-ai-out { margin-top: 0.6rem; padding: 0.6rem 0.8rem; border-left: 4px solid #7c3aed; background: #f5f3ff; border-radius: 4px; }
  .sb details { margin-top: 0.5rem; }
  .sa-score { position: sticky; top: 0; z-index: 3; background: #f0fdfa; border: 1px solid #99f6e4; border-radius: 8px; padding: 0.4rem 0.8rem; font-weight: 700; color: #134e4a; margin: 0.6rem 0; }
  .g3-badge.small { font-size: 0.65rem; padding: 0.1rem 0.55rem; margin-left: 0.4rem; }
  @media print { .sb { background: #fff; page-break-inside: avoid; } .sb textarea { min-height: 9rem; border: 1px solid #000; } .sa-score { display: none; } }
</style>
"""

JS = r"""
(function () {
  // ---- Section A running score
  const mcqs = document.querySelectorAll('.checkpoint[data-type=mcq]'), sc = document.getElementById('sa-score');
  function tally() { let ok = 0, tried = 0; mcqs.forEach(b => { const f = b.querySelector('.feedback'); if (f.classList.contains('correct')) { ok++; tried++; } else if (f.classList.contains('incorrect')) tried++; }); if (sc) sc.textContent = 'Section A: ' + ok + ' correct out of ' + mcqs.length + ' (' + tried + ' attempted)'; }
  mcqs.forEach(b => new MutationObserver(tally).observe(b.querySelector('.feedback'), { attributes: true, attributeFilter: ['class'] })); tally();
  // ---- Section B
  const norm = s => s.toLowerCase().replace(/[²]/g, '2').replace(/[×✕]/g, 'x').replace(/(\d),(\d{3})/g, '$1$2').replace(/\s+/g, ' ');
  const cfg = window.AI_MARKING || {}, page = location.pathname.split('/').pop().replace('.html', '');
  document.querySelectorAll('.sb').forEach(box => {
    const id = box.dataset.id, marks = +box.dataset.marks, Q = SB[id], ta = box.querySelector('textarea'), out = box.querySelector('.sb-out'), btn = box.querySelector('.sb-check'), ai = box.querySelector('.sb-ai');
    if (cfg.url) { ai.hidden = false; const pn = document.createElement('p'); pn.className = 'sb-note print-hide'; pn.textContent = 'The AI tutor sends the text of your answer to an outside AI service (BytePlus) to be marked. Do not type your name or any personal details.'; ai.parentNode.insertAdjacentElement('afterend', pn); }
    function score() { const n = out.querySelectorAll('input.pt:checked').length; out.querySelector('.sb-score').textContent = 'Your mark: ' + Math.min(n, marks) + ' out of ' + marks; }
    btn.addEventListener('click', () => {
      const a = norm(ta.value);
      if (a.trim().length < 3) { out.hidden = false; out.innerHTML = '<p>Write your answer in the box first, then check it.</p>'; return; }
      let h = '<p class="sb-note">The checker looks for key words. It can miss a correct answer that is worded differently, so tick or untick each point yourself.</p><ul>';
      Q.pts.forEach((p, i) => { const hit = p.re.every(r => new RegExp(r, 'i').test(a)); h += '<li><label><input type="checkbox" class="pt"' + (hit ? ' checked' : '') + '> ' + p.t + '</label></li>'; });
      h += '</ul><p class="sb-score"></p><details><summary>Show the model answer</summary><div>' + Q.model + '</div></details><div class="sb-ai-out" hidden></div>';
      out.hidden = false; out.innerHTML = h; out.querySelectorAll('input.pt').forEach(c => c.addEventListener('change', score)); score();
    });
    ai.addEventListener('click', async () => {
      const a = ta.value.trim(); if (a.length < 3) { out.hidden = false; out.innerHTML = '<p>Write your answer first.</p>'; return; }
      if (out.hidden) btn.click();
      const box2 = box.querySelector('.sb-ai-out'); box2.hidden = false; box2.textContent = 'The AI tutor is reading your answer...'; ai.disabled = true;
      try {
        const r = await fetch(cfg.url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ page: page, qid: id, answer: a.slice(0, 1200) }) });
        const d = await r.json(); if (!r.ok) throw new Error(d.error || 'The marking service is busy. Try again in a minute.');
        box2.innerHTML = '<strong>AI tutor: ' + (typeof d.score === 'number' ? d.score + ' out of ' + (d.max || marks) + '. ' : '') + '</strong>' + (d.feedback ? String(d.feedback).replace(/</g, '&lt;') : '') + '<div class="sb-note">AI feedback can be wrong. Compare it with the model answer.</div>';
      } catch (e) { box2.textContent = 'Sorry, the AI tutor could not mark this answer (' + e.message + '). Use the mark scheme above.'; }
      ai.disabled = false;
    });
  });
})();
"""


def build(t):
    """t: dict(file, title, topic, chapter, g3, intro, mcq=[(q,opts,ans,expl)], sb=[dict(id,q,marks,model,pts,g3?)])"""
    _cnt[0] = 0
    b = '<script src="ai-marking-config.js"></script>\n<p>%s</p>\n' % t["intro"]
    b += CSS
    b += '<h2 id="section-a">Section A: Multiple choice (%d questions)</h2>\n<p>Choose the best answer. You can check each answer and try again.</p>\n<div class="sa-score print-hide" id="sa-score" aria-live="polite"></div>\n' % len(t["mcq"])
    for i, (q, opts, ans, expl) in enumerate(t["mcq"], 1):
        b += mcq_cycle(i, q, opts, ans, expl)
    b += '<h2 id="section-b">Section B: Short answer and free response (%d questions)</h2>\n' % len(t["sb"])
    b += '<p>Write your answer in the box and check it against the mark scheme. Use full sentences and show your working in calculations, with units. The mark scheme shows which points earn marks.</p>\n'
    for i, q in enumerate(t["sb"], 1):
        b += sb_block(i, q["id"], q["q"], q["marks"], q.get("g3", False))
    sbj = {q["id"]: {"pts": q["pts"], "model": q["model"]} for q in t["sb"]}
    for q in t["sb"]:
        assert sum(1 for _ in q["pts"]) >= q["marks"], q["id"]
    js = "const SB = %s;\n" % json.dumps(sbj, ensure_ascii=False) + JS
    page(t["file"], "Revision Questions: " + t["short"], "Section A: multiple choice &middot; Section B: short answer and free response", b, js, badge=t.get("g3", False), topic=t["topic"])
    # config + script tag are added by build_all()


def build_all():
    import glob, importlib, os
    here = os.path.dirname(os.path.abspath(__file__))
    for f in sorted(glob.glob(os.path.join(here, "rev_data_*.py"))):
        for t in importlib.import_module(os.path.basename(f)[:-3]).TOPICS:
            build(t)


if __name__ == "__main__":
    build_all()
