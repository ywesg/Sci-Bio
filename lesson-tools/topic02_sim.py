"""Particle simulators for Topic 2: particles move at random and we watch the NET movement.
Modes:  mix    - red and blue particles, no membrane: each spreads down its own concentration gradient (Example 1)
        two    - two substances either side of a permeable membrane with gaps (Fig. 2.3)
        utube  - U-tube, sucrose solutions of different concentration, partially permeable membrane: only water crosses, levels change (Example 2)
        bag    - Visking tubing of sucrose solution in distilled water or in concentrated sucrose: turgid or flaccid (Example 3)
        starch - Visking tubing of starch solution in iodine solution: iodine moves in, inside turns blue-black (Example 4, G3)
Use: sim(id, mode, title, intro, key, presets) on the page and SIM_CSS + SIM_JS once. Hidden in print (the static figures print instead).
The status line 'locks' once the end state is reached, so it does not flicker while particles keep moving at random."""
import html

SIM_CSS = """<style>
  .sim { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.1rem; margin: 1.25rem 0; }
  .sim h3 { margin-top: 0; color: #134e4a; font-size: 1.08rem; }
  .sim canvas { display: block; width: 100%; height: auto; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; touch-action: pan-y; }
  .sim .btns { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.6rem 0; }
  .sim .btns button { min-height: 2.6rem; padding: 0 1rem; border: 1px solid #94a3b8; border-radius: 999px; background: #fff; color: #134e4a; font: 700 0.95rem "Source Sans 3", system-ui, sans-serif; cursor: pointer; }
  .sim .btns button.go { background: #0f766e; border-color: #0f766e; color: #fff; }
  .sim .btns button[aria-pressed="true"] { background: #134e4a; border-color: #134e4a; color: #fff; }
  .sim .presets { margin: 0.5rem 0 0; }
  .sim .read { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.5rem; margin-top: 0.4rem; }
  .sim .read div { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.4rem 0.7rem; font-size: 0.92rem; color: #475569; }
  .sim .read b { display: block; font-size: 1.2rem; color: #134e4a; }
  .sim .status { margin: 0.6rem 0 0; padding: 0.5rem 0.8rem; border-radius: 8px; background: #f0fdfa; border: 1px solid #99f6e4; font-weight: 600; color: #134e4a; }
  .sim .status.end { background: #dcfce7; border-color: #86efac; }
  .sim .key { font-size: 0.9rem; color: #475569; margin: 0.4rem 0 0; }
  .sim .key i { display: inline-block; width: 0.8em; height: 0.8em; border-radius: 50%; vertical-align: -0.05em; margin: 0 0.25em 0 0.6em; }
  .sim .only { margin: 0.5rem 0 0; padding: 0.45rem 0.8rem; border-left: 4px solid #f97316; background: #fff7ed; font-weight: 600; color: #7c2d12; }
  @media print { .sim { display: none !important; } }
</style>
"""

READS = {"mix": [("Red: left | right", "r"), ("Blue: left | right", "b")],
         "two": [("Yellow: left | right", "y"), ("Blue: left | right", "b")],
         "utube": [("Water molecules in A", "wa"), ("Water molecules in B", "wb")],
         "bag": [("Water molecules inside the tubing", "wi"), ("Water molecules outside", "wo")],
         "starch": [("Iodine inside the tubing", "ii"), ("Iodine outside", "io")]}


def sim(sid, mode, title, intro, key, presets=None, only=None, height=320, extra_class=""):
    """presets: list of button labels (the first is chosen at the start). only: a highlighted note under the intro."""
    pre = ""
    if presets:
        pre = ('  <div class="btns presets" role="group" aria-label="Choose the set-up">%s</div>\n'
               % "".join('<button type="button" data-preset="%d" aria-pressed="%s">%s</button>' % (i, "true" if i == 0 else "false", p) for i, p in enumerate(presets)))
    return ('<div class="sim print-hide%s" id="%s" data-mode="%s">\n  <h3>%s</h3>\n  <p>%s</p>\n%s%s'
            '  <canvas width="720" height="%d" aria-label="%s"></canvas>\n  <p class="key">%s</p>\n'
            '  <div class="btns"><button type="button" class="go" data-act="play">&#9654; Start</button><button type="button" data-act="reset">&#8634; Start again</button></div>\n'
            '  <div class="read">%s<div>Time (steps)<b data-r="t">0</b></div></div>\n  <p class="status" aria-live="polite">Press Start.</p>\n</div>\n'
            % (extra_class, sid, mode, title, intro, '  <p class="only">%s</p>\n' % only if only else "", pre, height,
               html.escape("Animation of moving particles: " + title, quote=True), key,
               "".join('<div>%s<b data-r="%s">-</b></div>' % r for r in READS[mode])))


SIM_JS = r"""
document.querySelectorAll('.sim').forEach(function (box) {
  var mode = box.dataset.mode, cv = box.querySelector('canvas'), ctx = cv.getContext('2d');
  var W = cv.width, H = cv.height, MID = W / 2, P = [], run = false, t = 0, preset = 0, done = false, steady = 0, cnt;
  var playB = box.querySelector('[data-act=play]'), st = box.querySelector('.status');
  var COL = { r: '#ef4444', a: '#3b82f6', y: '#eab308', s: '#f97316', w: '#60a5fa', i: '#92400e' };
  var R = Math.random;
  function setR(k, v) { var e = box.querySelector('[data-r="' + k + '"]'); if (e) e.textContent = v; }
  function lr(a) { return a[0] + ' | ' + a[1]; }
  function count() {   // counts by kind and side (side 0/1); for one-chamber modes the side is left/right of the middle
    cnt = {};
    P.forEach(function (p) { var s = D.sides === 1 ? (p.x < MID ? 0 : 1) : p.s; (cnt[p.k] = cnt[p.k] || [0, 0])[s]++; });
    ['r', 'a', 'y', 's', 'w', 'i', 'st'].forEach(function (k) { cnt[k] = cnt[k] || [0, 0]; });
  }
  function free(s) { return Math.max(0.08, 1 - 4 * cnt.s[s] / Math.max(1, cnt.w[s])); }   // water held by sucrose is not free to cross
  function add(n, s, k, r, x0, x1, y0, y1) {
    for (var i = 0; i < n; i++) {
      for (var j = 0; j < 400; j++) { var x = x0 + R() * (x1 - x0), y = y0 + R() * (y1 - y0); if (D.geom(s, x, y, r)) break; }
      P.push({ x: x, y: y, vx: 0, vy: 0, k: k, r: r, s: s });
    }
  }
  function lerp(c1, c2, f) { var a = [1, 3, 5].map(function (i) { return parseInt(c1.substr(i, 2), 16); }), b = [1, 3, 5].map(function (i) { return parseInt(c2.substr(i, 2), 16); });
    return 'rgb(' + a.map(function (v, i) { return Math.round(v + (b[i] - v) * f); }).join(',') + ')'; }
  function box2(x, y, w, h, fill) { ctx.fillStyle = fill; ctx.fillRect(x, y, w, h); }
  var LBL = [];   // labels are drawn after the particles, with a white outline, so they stay readable
  function label(txt, x, y, al) { LBL.push([txt, x, y, al || 'left']); }
  function drawLabels() { ctx.font = 'bold 15px Source Sans 3, sans-serif'; ctx.lineJoin = 'round';
    LBL.forEach(function (l) { ctx.textAlign = l[3]; ctx.lineWidth = 4; ctx.strokeStyle = 'rgba(255,255,255,0.9)'; ctx.strokeText(l[0], l[1], l[2]); ctx.fillStyle = '#334155'; ctx.fillText(l[0], l[1], l[2]); });
    ctx.textAlign = 'left'; LBL = []; }

  // ---------------------------------------------------------------- the modes
  var inBox = function (x, y, r) { return x > 6 + r && x < W - 6 - r && y > 6 + r && y < H - 6 - r; };
  var MODES = {
    mix: { sides: 1,
      init: function () { add(70, 0, 'r', 4.5, 8, MID - 8, 8, H - 8); add(70, 0, 'a', 4.5, MID + 8, W - 8, 8, H - 8); },
      geom: function (s, x, y, r) { return inBox(x, y, r); },
      draw: function () { box2(6, 6, W - 12, H - 12, '#e0f2fe'); ctx.setLineDash([4, 6]); ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(MID, 6); ctx.lineTo(MID, H - 6); ctx.stroke(); ctx.setLineDash([]);
        label('left', 14, 24); label('right', W - 14, 24, 'right'); },
      read: function () { setR('r', lr(cnt.r)); setR('b', lr(cnt.a));
        return [Math.abs(cnt.r[0] - cnt.r[1]) <= 8 && Math.abs(cnt.a[0] - cnt.a[1]) <= 8,
          'Red particles move net to the right and blue particles move net to the left. Each moves down its own concentration gradient.',
          'Both colours are now evenly spread on both sides. The particles keep moving, but there is no net movement.']; } },
    two: { sides: 2,
      init: function () { add(70, 0, 'y', 4.5, 8, MID - 8, 8, H - 8); add(70, 1, 'a', 4.5, MID + 8, W - 8, 8, H - 8); },
      geom: function (s, x, y, r) { return inBox(x, y, r) && (s === 0 ? x < MID : x > MID); },
      cross: function (p, x, y) { var m = y % 36; return m > 12 && m < 30; },
      draw: function () { box2(6, 6, W - 12, H - 12, '#e0f2fe'); ctx.strokeStyle = '#475569'; ctx.lineWidth = 4;
        for (var y = 0; y < H; y += 36) { ctx.beginPath(); ctx.moveTo(MID, Math.max(6, y - 6)); ctx.lineTo(MID, Math.min(H - 6, y + 12)); ctx.stroke(); } },
      read: function () { setR('y', lr(cnt.y)); setR('b', lr(cnt.a));
        return [Math.abs(cnt.y[0] - cnt.y[1]) <= 8 && Math.abs(cnt.a[0] - cnt.a[1]) <= 8,
          'Yellow particles move net to the right, blue ones net to the left. Each substance moves down its own concentration gradient.',
          'Both substances are now evenly spread on both sides of the membrane. The particles keep moving, but there is no net movement.']; } },
    utube: { sides: 2,
      // arms: A x 170-290, B x 430-550; channel at the bottom y 230-300; partially permeable membrane at x = 360
      init: function () { var su = [[24, 12], [12, 24], [12, 12]][preset]; this.lvl = [100, 100]; this.w0 = 170;
        add(su[0], 0, 's', 8, 170, 360, 110, 300); add(su[1], 1, 's', 8, 360, 550, 110, 300);
        add(this.w0, 0, 'w', 2.6, 170, 360, 110, 300); add(this.w0, 1, 'w', 2.6, 360, 550, 110, 300); },
      geom: function (s, x, y, r) { var L = this.lvl;
        if (y < L[s] + r || y > 300 - r) return false;
        var arm = s === 0 ? (x > 170 + r && x < 290 - r) : (x > 430 + r && x < 550 - r);
        var ch = y > 230 + r && x > 170 + r && x < 550 - r && (s === 0 ? x < 360 : x > 360);
        return arm || ch; },
      cross: function (p) { return p.k === 'w' && R() < free(p.s); },
      after: function () { var self = this; [0, 1].forEach(function (s) { var tg = 100 - 1.1 * (cnt.w[s] - self.w0); tg = Math.max(30, Math.min(205, tg)); self.lvl[s] += (tg - self.lvl[s]) * 0.04; });
        P.forEach(function (p) { if (p.y < self.lvl[p.s] + p.r) p.y = self.lvl[p.s] + p.r + 0.5; }); },
      draw: function () { var L = this.lvl;
        box2(170, L[0], 120, 300 - L[0], '#e0f2fe'); box2(430, L[1], 120, 300 - L[1], '#e0f2fe'); box2(170, 230, 380, 70, '#e0f2fe');
        ctx.strokeStyle = '#3f3f46'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(170, 14); ctx.lineTo(170, 300); ctx.lineTo(550, 300); ctx.lineTo(550, 14);
        ctx.moveTo(290, 14); ctx.lineTo(290, 230); ctx.lineTo(430, 230); ctx.lineTo(430, 14); ctx.stroke();
        ctx.strokeStyle = '#0369a1'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(170, L[0]); ctx.lineTo(290, L[0]); ctx.moveTo(430, L[1]); ctx.lineTo(550, L[1]); ctx.stroke();
        ctx.setLineDash([5, 4]); ctx.strokeStyle = '#94a3b8'; ctx.beginPath(); ctx.moveTo(150, 100); ctx.lineTo(570, 100); ctx.stroke();
        ctx.strokeStyle = '#0f766e'; ctx.lineWidth = 4; ctx.setLineDash([7, 5]); ctx.beginPath(); ctx.moveTo(360, 230); ctx.lineTo(360, 300); ctx.stroke(); ctx.setLineDash([]);
        var pc = [['10%', '5%'], ['5%', '10%'], ['5%', '5%']][preset];
        label('A: ' + pc[0] + ' sucrose', 230, 24, 'center'); label('B: ' + pc[1] + ' sucrose', 490, 24, 'center');
        label('starting level', 575, 104); label('partially permeable membrane', 360, 318, 'center'); },
      read: function () { setR('wa', cnt.w[0]); setR('wb', cnt.w[1]); var L = this.lvl;
        if (preset === 2) return [t > 3000, 'Both arms have the same concentration, so the same water potential. Water molecules cross both ways at the same rate.',
          'The levels stay the same: no net movement of water, because there is no water potential gradient.'];
        var hi = preset === 0 ? 'A' : 'B', lo = preset === 0 ? 'B' : 'A', d = Math.abs(L[0] - L[1]);
        return [d > 100 && t > 3000, t < 200 ? 'Only the small water molecules can pass through the membrane. The sucrose molecules are too large.' :
          'Net movement of water from ' + lo + ' (higher water potential) to ' + hi + ' (lower water potential): the level in ' + hi + ' rises.',
          'Osmosis: water has moved from ' + lo + ' to ' + hi + '. The level in ' + hi + ' has risen and the level in ' + lo + ' has fallen. The sucrose molecules stayed where they were.']; } },
    bag: { sides: 2,
      // side 0 = inside the Visking tubing (an ellipse that swells or shrinks), side 1 = the beaker outside
      init: function () { this.f = 1; var out = preset === 0 ? 0 : 125;
        add(14, 0, 's', 7, 250, 470, 90, 290); add(110, 0, 'w', 2.6, 250, 470, 90, 290); this.w0 = 110;
        add(out, 1, 's', 7, 30, 690, 40, 310); add(520, 1, 'w', 2.6, 30, 690, 40, 310); },
      ell: function (x, y, d) { var f = this.f, rx = 105 * f - d, ry = 95 * Math.sqrt(f) - d; return Math.pow((x - 360) / rx, 2) + Math.pow((y - 190) / ry, 2); },
      geom: function (s, x, y, r) { if (s === 0) return this.ell(x, y, r >= 7 ? r : 0) <= 1; return x > 26 + r && x < W - 26 - r && y > 40 + r && y < H - 10 - r && this.ell(x, y, 0) > 1; },
      cross: function (p) { return p.k === 'w' && R() < free(p.s); },
      after: function () { var self = this, tg = Math.sqrt(cnt.w[0] / this.w0); tg = Math.max(0.6, Math.min(1.35, tg)); this.f += (tg - this.f) * 0.03;
        P.forEach(function (p) {   // keep particles on their own side as the tubing changes size
          var k = 0;
          if (p.s === 0) while (!self.geom(0, p.x, p.y, p.r) && k++ < 20) { p.x = 360 + (p.x - 360) * 0.95; p.y = 190 + (p.y - 190) * 0.95; }
          else { while (self.ell(p.x, p.y, 0) <= 1.02 && k++ < 40) { p.x = 360 + (p.x - 360) * 1.04 + 0.1; p.y = 190 + (p.y - 190) * 1.04; }
            p.x = Math.min(Math.max(p.x, 27 + p.r), W - 27 - p.r); p.y = Math.min(Math.max(p.y, 41 + p.r), H - 11 - p.r); }
        }); },
      draw: function () { var f = this.f, rx = 105 * f, ry = 95 * Math.sqrt(f), wavy = f < 0.88;
        box2(26, 40, W - 52, H - 50, preset === 0 ? '#e0f2fe' : '#fde7c8');
        ctx.strokeStyle = '#3f3f46'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(22, 14); ctx.lineTo(22, H - 6); ctx.lineTo(W - 22, H - 6); ctx.lineTo(W - 22, 14); ctx.stroke();
        ctx.beginPath(); for (var a = 0; a <= 6.30; a += 0.05) { var w = wavy ? 1 + 0.05 * Math.sin(a * 14) : 1, x = 360 + rx * w * Math.cos(a), y = 190 + ry * w * Math.sin(a); a ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
        ctx.fillStyle = '#cffafe'; ctx.fill(); ctx.strokeStyle = '#0369a1'; ctx.lineWidth = 3; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(352, 190 - ry); ctx.lineTo(348, 10); ctx.moveTo(368, 190 - ry); ctx.lineTo(372, 10); ctx.stroke();
        label('Visking tubing: sucrose solution', 360 + rx + 12, 190 - 0.6 * ry);
        label(preset === 0 ? 'outside: distilled water' : 'outside: concentrated sucrose solution', 36, H - 16); },
      read: function () { setR('wi', cnt.w[0]); setR('wo', cnt.w[1]);
        if (preset === 0) return [this.f > 1.25, 'Water molecules move into the tubing by osmosis, from the distilled water (higher water potential) to the sucrose solution (lower water potential).',
          'The tubing has swollen and become firm: it is turgid. Water entered by osmosis; the sucrose molecules are too large to leave.'];
        return [this.f < 0.8, 'Water molecules move out of the tubing by osmosis, from the sucrose solution inside (higher water potential) to the concentrated solution outside (lower water potential).',
          'The tubing has shrunk and become soft and wrinkled: it is flaccid. Water left by osmosis.']; } },
    starch: { sides: 2,
      init: function () { this.f = 1; add(16, 0, 'st', 9, 250, 470, 90, 290); add(120, 1, 'i', 3.2, 30, 690, 40, 310); },
      ell: function (x, y, d) { return Math.pow((x - 360) / (105 - d), 2) + Math.pow((y - 190) / (95 - d), 2); },
      geom: function (s, x, y, r) { if (s === 0) return this.ell(x, y, r >= 7 ? r : 0) <= 1; return x > 26 + r && x < W - 26 - r && y > 40 + r && y < H - 10 - r && this.ell(x, y, 0) > 1; },
      cross: function (p) { return p.k === 'i'; },   // iodine is small enough to pass; starch is too large
      draw: function () { var g = Math.min(1, cnt.i[0] / 14);
        box2(26, 40, W - 52, H - 50, '#f2c57c');
        ctx.strokeStyle = '#3f3f46'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(22, 14); ctx.lineTo(22, H - 6); ctx.lineTo(W - 22, H - 6); ctx.lineTo(W - 22, 14); ctx.stroke();
        ctx.beginPath(); ctx.ellipse(360, 190, 105, 95, 0, 0, 6.2832); ctx.fillStyle = lerp('#f8fafc', '#1e1b4b', g); ctx.fill(); ctx.strokeStyle = '#0369a1'; ctx.lineWidth = 3; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(352, 95); ctx.lineTo(348, 10); ctx.moveTo(368, 95); ctx.lineTo(372, 10); ctx.stroke();
        COL.st = lerp('#e5e7eb', '#312e81', g);
        label('inside: starch solution', 476, 120); label('outside: iodine solution (brown)', 36, H - 16); },
      read: function () { setR('ii', cnt.i[0]); setR('io', cnt.i[1]);
        return [cnt.i[0] >= 14, 'Iodine molecules are small, so they diffuse into the tubing. Starch molecules are too large to get out.',
          'Inside the tubing has turned blue-black: iodine diffused in and reacted with the starch. Outside stays brown, because no starch moved out.']; } }
  };
  var D = MODES[mode];

  // ---------------------------------------------------------------- engine
  function reset() { P = []; t = 0; done = false; steady = 0; COL.st = '#e5e7eb'; D.init(); count(); draw(); readout(); st.textContent = 'Press Start.'; st.classList.remove('end'); }
  function step() {
    count();
    P.forEach(function (p) {
      var sp = p.r >= 7 ? 1.2 : 3;
      p.vx = 0.86 * p.vx + (R() - 0.5) * sp; p.vy = 0.86 * p.vy + (R() - 0.5) * sp;
      var nx = p.x + p.vx, ny = p.y + p.vy;
      if (D.geom(p.s, nx, ny, p.r)) { p.x = nx; p.y = ny; return; }
      var o = 1 - p.s;
      if (D.sides === 2 && D.geom(o, nx, ny, p.r) && D.cross(p, nx, ny)) { p.s = o; p.x = nx; p.y = ny; return; }
      if (D.geom(p.s, nx, p.y, p.r)) { p.x = nx; p.vy = -p.vy; } else if (D.geom(p.s, p.x, ny, p.r)) { p.y = ny; p.vx = -p.vx; } else { p.vx = -p.vx; p.vy = -p.vy; }
    });
    if (D.after) D.after();
  }
  function draw() {
    ctx.clearRect(0, 0, W, H); LBL = []; D.draw();
    if (mode === 'mix' || mode === 'two') { ctx.strokeStyle = '#3f3f46'; ctx.lineWidth = 3; ctx.strokeRect(4, 4, W - 8, H - 8); }
    P.forEach(function (p) { ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fillStyle = COL[p.k]; ctx.fill(); if (p.r > 3) { ctx.lineWidth = 1; ctx.strokeStyle = 'rgba(0,0,0,0.35)'; ctx.stroke(); } });
    drawLabels();
  }
  function readout() {
    setR('t', Math.round(t / 40)); count();
    var r = D.read();
    if (!done && t > 0) { steady = r[0] ? steady + 1 : 0; if (steady >= 3) done = true; }   // lock the end message once it has held for a moment
    if (t === 0) return;
    st.textContent = done ? r[2] : r[1]; st.classList.toggle('end', done);
  }
  function loop() { if (!run) return; for (var i = 0; i < 6; i++) { step(); t++; } draw(); if (t % 48 === 0) readout(); requestAnimationFrame(loop); }
  playB.addEventListener('click', function () { run = !run; playB.innerHTML = run ? '&#10074;&#10074; Pause' : '&#9654; Start'; if (run) loop(); });
  box.querySelector('[data-act=reset]').addEventListener('click', reset);
  box.querySelectorAll('[data-preset]').forEach(function (b) { b.addEventListener('click', function () {
    preset = +b.dataset.preset; box.querySelectorAll('[data-preset]').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); reset(); }); });
  reset();
});
"""
