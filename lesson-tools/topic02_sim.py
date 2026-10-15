"""Particle simulators for Topic 2: particles move at random and we watch the NET movement.
Modes:  free   - one dissolved substance starting crowded on the left, no membrane (Example 1)
        mix    - red and blue particles, no membrane: each spreads down its own concentration gradient (Example 1)
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

READS = {"free": [("Particles on the left", "l0"), ("Particles on the right", "r0")],
         "mix": [("Red: left | right", "r"), ("Blue: left | right", "b")],
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
            '  <div class="read">%s<div>Time<b data-r="t">0 s</b></div></div>\n  <p class="status" aria-live="polite">Press Start.</p>\n</div>\n'
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
      var a = R() * 6.2832; P.push({ x: x, y: y, vx: Math.cos(a), vy: Math.sin(a), k: k, r: r, s: s });
    }
  }
  function lerp(c1, c2, f) { var a = [1, 3, 5].map(function (i) { return parseInt(c1.substr(i, 2), 16); }), b = [1, 3, 5].map(function (i) { return parseInt(c2.substr(i, 2), 16); });
    return 'rgb(' + a.map(function (v, i) { return Math.round(v + (b[i] - v) * f); }).join(',') + ')'; }
  function box2(x, y, w, h, fill) { ctx.fillStyle = fill; ctx.fillRect(x, y, w, h); }
  var LBL = [];   // labels are drawn after the particles, with a white outline, so they stay readable
  function label(txt, x, y, al, px, py) { LBL.push([txt, x, y, al || 'left', px, py]); }
  function drawLabels() { ctx.font = 'bold 15px Source Sans 3, sans-serif'; ctx.lineJoin = 'round';
    LBL.forEach(function (l) { if (l[4] !== undefined) { ctx.strokeStyle = '#334155'; ctx.lineWidth = 1.3; ctx.beginPath(); ctx.moveTo(l[1] - 4, l[2] - 5); ctx.lineTo(l[4], l[5]); ctx.stroke(); ctx.beginPath(); ctx.arc(l[4], l[5], 2.5, 0, 6.2832); ctx.fillStyle = '#334155'; ctx.fill(); }
      ctx.textAlign = l[3]; ctx.lineWidth = 4; ctx.strokeStyle = 'rgba(255,255,255,0.9)'; ctx.strokeText(l[0], l[1], l[2]); ctx.fillStyle = '#334155'; ctx.fillText(l[0], l[1], l[2]); });
    ctx.textAlign = 'left'; LBL = []; }

  // ---------------------------------------------------------------- the modes
  var inBox = function (x, y, r) { return x > 6 + r && x < W - 6 - r && y > 6 + r && y < H - 6 - r; };
  // Visking tubing: a long, tilted tube in a beaker of liquid, tied at both ends, hanging from a string (like the textbook picture)
  var TB = { cx: 330, cy: 205, a: 135, b: 52, th: -0.3, f: 1 };
  function tubeE(x, y, d) { var dx = x - TB.cx, dy = y - TB.cy, c = Math.cos(TB.th), s = Math.sin(TB.th), u = dx * c + dy * s, v = -dx * s + dy * c;
    var bb = TB.b * TB.f - d, aa = TB.a * Math.sqrt(TB.f) - d; return (u * u) / (bb * bb) + (v * v) / (aa * aa); }
  function tubeGeom(s, x, y, r) { if (s === 0) return tubeE(x, y, r >= 7 ? r : 0) <= 1; return x > 184 + r && x < 476 - r && y > 52 + r && y < 366 - r && tubeE(x, y, 0) > 1; }
  function tubeW(lx, ly) { var c = Math.cos(TB.th), s = Math.sin(TB.th); return [TB.cx + lx * c - ly * s, TB.cy + lx * s + ly * c]; }   // tube coordinates -> canvas
  function drawBeaker(fill) {
    box2(184, 50, 292, 318, fill);
    ctx.strokeStyle = '#3f3f46'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(172, 20); ctx.lineTo(180, 26); ctx.lineTo(180, 360); ctx.quadraticCurveTo(180, 370, 190, 370);
    ctx.lineTo(470, 370); ctx.quadraticCurveTo(480, 370, 480, 360); ctx.lineTo(480, 20); ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,0.7)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(462, 70); ctx.lineTo(462, 340); ctx.stroke(); }
  function drawTube(fill, wavy) {
    var bb = TB.b * TB.f, aa = TB.a * Math.sqrt(TB.f), top = tubeW(0, -aa);
    ctx.strokeStyle = '#78350f'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(top[0], top[1] - 8); ctx.lineTo(top[0] - 4, 6); ctx.stroke();   // string
    ctx.save(); ctx.translate(TB.cx, TB.cy); ctx.rotate(TB.th); ctx.beginPath();
    for (var a = 0; a <= 6.30; a += 0.04) { var w = wavy ? 1 + 0.07 * Math.sin(a * 18) : 1, x = bb * w * Math.cos(a), y = aa * Math.sin(a); a ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.closePath(); ctx.fillStyle = fill; ctx.fill(); ctx.strokeStyle = '#1d4ed8'; ctx.lineWidth = 3; ctx.stroke();
    [-1, 1].forEach(function (e) {   // tied ends
      ctx.fillStyle = fill; ctx.beginPath(); ctx.moveTo(-7, e * (aa - 2)); ctx.lineTo(0, e * (aa + 9)); ctx.lineTo(7, e * (aa - 2)); ctx.fill(); ctx.strokeStyle = '#1d4ed8'; ctx.lineWidth = 2; ctx.stroke();
      ctx.strokeStyle = '#78350f'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-8, e * aa); ctx.lineTo(8, e * aa); ctx.stroke();
      ctx.lineWidth = 1.6; ctx.beginPath(); ctx.ellipse(-7, e * (aa + 5), 4, 6, 0.5, 0, 6.2832); ctx.ellipse(7, e * (aa + 5), 4, 6, -0.5, 0, 6.2832); ctx.stroke(); });
    ctx.restore(); }
  function keepSides() {   // keep every particle on its own side of the tubing as the tubing changes size
    P.forEach(function (p) { var k = 0;
      if (p.s === 0) while (!tubeGeom(0, p.x, p.y, p.r) && k++ < 25) { p.x = TB.cx + (p.x - TB.cx) * 0.94; p.y = TB.cy + (p.y - TB.cy) * 0.94; }
      else { while (tubeE(p.x, p.y, 0) <= 1 && k++ < 40) { p.x = TB.cx + (p.x - TB.cx) * 1.02 + 0.1; p.y = TB.cy + (p.y - TB.cy) * 1.02; }
        if (!tubeGeom(1, p.x, p.y, p.r)) { p.x = Math.min(Math.max(p.x, 185 + p.r), 475 - p.r); p.y = Math.min(Math.max(p.y, 53 + p.r), 365 - p.r); } } }); }

  var MODES = {
    free: { sides: 1,
      init: function () { add(140, 0, 'a', 4.5, 8, 70, 8, H - 8); },
      geom: function (s, x, y, r) { return inBox(x, y, r); },
      draw: function () { box2(6, 6, W - 12, H - 12, '#e0f2fe'); ctx.setLineDash([4, 6]); ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(MID, 6); ctx.lineTo(MID, H - 6); ctx.stroke(); ctx.setLineDash([]); },
      read: function () { setR('l0', cnt.a[0]); setR('r0', cnt.a[1]);
        return [Math.abs(cnt.a[0] - cnt.a[1]) <= 16,
          'Net movement from left to right: the particles move down the concentration gradient.',
          'About the same on both sides. The particles keep moving, but there is no net movement now.']; } },
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
      cross: function (p, x, y) { var m = y % 36; return m > 8 && m < 34; },
      draw: function () { box2(6, 6, W - 12, H - 12, '#e0f2fe'); ctx.strokeStyle = '#475569'; ctx.lineWidth = 4;
        for (var y = 0; y < H; y += 36) { ctx.beginPath(); ctx.moveTo(MID, Math.max(6, y - 2)); ctx.lineTo(MID, Math.min(H - 6, y + 8)); ctx.stroke(); } },
      read: function () { setR('y', lr(cnt.y)); setR('b', lr(cnt.a));
        return [Math.abs(cnt.y[0] - cnt.y[1]) <= 12 && Math.abs(cnt.a[0] - cnt.a[1]) <= 12,
          'Yellow particles move net to the right, blue ones net to the left. Each substance moves down its own concentration gradient.',
          'Both substances are now evenly spread on both sides of the membrane. The particles keep moving, but there is no net movement.']; } },
    utube: { sides: 2,
      // arms: A x 170-290, B x 430-550; channel at the bottom y 230-300; partially permeable membrane at x = 360
      init: function () { var su = [[28, 14], [14, 28], [14, 14]][preset]; this.lvl = [100, 100]; this.w0 = 170;
        add(su[0], 0, 's', 8, 170, 360, 110, 300); add(su[1], 1, 's', 8, 360, 550, 110, 300);
        add(this.w0, 0, 'w', 2.6, 170, 360, 110, 300); add(this.w0, 1, 'w', 2.6, 360, 550, 110, 300); },
      geom: function (s, x, y, r) { var L = this.lvl;
        if (y < L[s] + r || y > 300 - r) return false;
        var arm = s === 0 ? (x > 170 + r && x < 290 - r) : (x > 430 + r && x < 550 - r);
        var ch = y > 230 + r && x > 170 + r && x < 550 - r && (s === 0 ? x < 360 : x > 360);
        return arm || ch; },
      cross: function (p) { return p.k === 'w' && R() < free(p.s); },
      after: function () { var self = this; [0, 1].forEach(function (s) { var tg = preset === 2 ? 100 : 100 - 1.4 * (cnt.w[s] - self.w0);   // equal concentrations: no net movement, levels stay put
           tg = Math.max(30, Math.min(205, tg)); self.lvl[s] += (tg - self.lvl[s]) * 0.01; });
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
        if (preset === 2) return [t > 600, 'Both arms have the same concentration, so the same water potential. Water molecules cross both ways at the same rate.',
          'The levels stay the same: no net movement of water, because there is no water potential gradient.'];
        var hi = preset === 0 ? 'A' : 'B', lo = preset === 0 ? 'B' : 'A', d = Math.abs(L[0] - L[1]);
        return [d > 55 && t > 600, t < 150 ? 'Only the small water molecules can pass through the membrane. The sucrose molecules are too large.' :
          'Net movement of water from ' + lo + ' (higher water potential) to ' + hi + ' (lower water potential): the level in ' + hi + ' rises.',
          'Osmosis: water has moved from ' + lo + ' to ' + hi + '. The level in ' + hi + ' has risen and the level in ' + lo + ' has fallen. The sucrose molecules stayed where they were.']; } },
    bag: { sides: 2,
      // side 0 = inside the Visking tubing (it swells or shrinks with the water inside), side 1 = the beaker outside
      init: function () { TB.f = 1; this.w0 = 75;
        add(9, 0, 's', 7, 200, 460, 60, 360); add(this.w0, 0, 'w', 2.6, 200, 460, 60, 360);
        add(preset === 0 ? 0 : 72, 1, 's', 7, 184, 476, 52, 366); add(300, 1, 'w', 2.6, 184, 476, 52, 366); },
      geom: tubeGeom,
      cross: function (p) { return p.k === 'w' && R() < 0.22 * free(p.s); },
      after: function () { var tg = Math.sqrt(cnt.w[0] / this.w0); tg = Math.max(0.6, Math.min(1.22, tg)); TB.f += (tg - TB.f) * 0.03; keepSides(); },
      draw: function () { var aa = TB.a * Math.sqrt(TB.f), bb = TB.b * TB.f;
        drawBeaker(preset === 0 ? '#9cc7f0' : '#a9c4e8'); drawTube('#fbefd9', TB.f < 0.88);
        var edge = tubeW(bb, -aa * 0.35), mid = tubeW(0, aa * 0.25);
        label('Visking tubing', 498, 96, 'left', edge[0], edge[1]); label('sucrose solution', 498, 210, 'left', mid[0], mid[1]);
        label(preset === 0 ? 'distilled water' : 'concentrated', 498, 300, 'left', 455, 320); if (preset) label('sucrose solution', 498, 320);
        label('beaker', 498, 360, 'left', 480, 345); },
      read: function () { setR('wi', cnt.w[0]); setR('wo', cnt.w[1]);
        if (preset === 0) return [TB.f > 1.16, 'Water molecules move into the tubing by osmosis, from the distilled water (higher water potential) to the sucrose solution (lower water potential).',
          'The tubing has swollen and become firm: it is turgid. Water entered by osmosis; the sucrose molecules are too large to leave.'];
        return [TB.f < 0.8, 'Water molecules move out of the tubing by osmosis, from the sucrose solution inside (higher water potential) to the concentrated solution outside (lower water potential).',
          'The tubing has shrunk and become soft and wrinkled: it is flaccid. Water left by osmosis.']; } },
    starch: { sides: 2,
      init: function () { TB.f = 1; add(12, 0, 'st', 9, 200, 460, 60, 360); add(110, 1, 'i', 3.2, 184, 476, 52, 366); },
      geom: tubeGeom,
      cross: function (p) { return p.k === 'i' && R() < 0.25; },   // iodine is small enough to pass; starch is too large
      draw: function () { var g = Math.min(1, cnt.i[0] / 24), aa = TB.a, bb = TB.b;
        drawBeaker('#e8b45c'); drawTube(lerp('#fbefd9', '#1e1b4b', g), false);
        COL.st = lerp('#e5e7eb', '#312e81', g);
        var edge = tubeW(bb, -aa * 0.35), mid = tubeW(0, aa * 0.25);
        label('Visking tubing', 498, 96, 'left', edge[0], edge[1]); label('starch solution', 498, 210, 'left', mid[0], mid[1]);
        label('iodine solution', 498, 300, 'left', 455, 320); label('(brown)', 498, 320); },
      read: function () { setR('ii', cnt.i[0]); setR('io', cnt.i[1]);
        return [cnt.i[0] >= 22, 'Iodine molecules are small, so they diffuse into the tubing. Starch molecules are too large to get out.',
          'Inside the tubing has turned blue-black: iodine diffused in and reacted with the starch. Outside stays brown, because no starch moved out.']; } }
  };
  var D = MODES[mode];

  // ---------------------------------------------------------------- engine
  function reset() { P = []; t = 0; done = false; steady = 0; COL.st = '#e5e7eb'; D.init(); count(); draw(); readout(); st.textContent = 'Press Start.'; st.classList.remove('end'); }
  function step() {
    count();
    P.forEach(function (p) {
      // calm motion: each particle glides at a steady, slow speed and slowly changes direction at random
      var sp = p.r >= 7 ? 0.5 : 1.3, a = (R() - 0.5) * 0.3, c = Math.cos(a), sn = Math.sin(a);
      var vx = p.vx * c - p.vy * sn, vy = p.vx * sn + p.vy * c, m = Math.hypot(vx, vy) || 1;
      p.vx = vx / m * sp; p.vy = vy / m * sp;
      var nx = p.x + p.vx, ny = p.y + p.vy;
      if (D.geom(p.s, nx, ny, p.r)) { p.x = nx; p.y = ny; return; }
      var o = 1 - p.s;
      if (D.sides === 2 && D.geom(o, nx, ny, p.r)) {   // at the membrane: cross, or bounce straight back (no sliding along it)
        if (D.cross(p, nx, ny)) { p.s = o; p.x = nx; p.y = ny; } else { p.vx = -p.vx; p.vy = -p.vy; }
        return; }
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
    setR('t', Math.round(t / 60) + ' s'); count();
    var r = D.read();
    if (!done && t > 0) { steady = r[0] ? steady + 1 : 0; if (steady >= 3) done = true; }   // lock the end message once it has held for a moment
    if (t === 0) return;
    st.textContent = done ? r[2] : r[1]; st.classList.toggle('end', done);
  }
  function loop() { if (!run) return; step(); t++; draw(); if (t % 30 === 0) readout(); requestAnimationFrame(loop); }
  playB.addEventListener('click', function () { run = !run; playB.innerHTML = run ? '&#10074;&#10074; Pause' : '&#9654; Start'; if (run) loop(); });
  box.querySelector('[data-act=reset]').addEventListener('click', reset);
  box.querySelectorAll('[data-preset]').forEach(function (b) { b.addEventListener('click', function () {
    preset = +b.dataset.preset; box.querySelectorAll('[data-preset]').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); reset(); }); });
  reset();
});
"""
