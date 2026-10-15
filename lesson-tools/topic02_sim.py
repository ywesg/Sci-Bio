"""Particle simulator for Topic 2: particles move at random and we watch the NET movement.
Modes:  free  - one dissolved substance, no membrane (diffusion in water)
        two   - two substances either side of a permeable membrane (each diffuses independently)
        osmo  - sucrose + water either side of a partially permeable membrane (only water passes; liquid levels change)
Use: sim("sim1", "free", "title", "intro") on the page and SIM_CSS + SIM_JS once. Hidden in print (the static figures print instead)."""

SIM_CSS = """<style>
  .sim { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.1rem; margin: 1.25rem 0; }
  .sim h3 { margin-top: 0; color: #134e4a; font-size: 1.08rem; }
  .sim canvas { display: block; width: 100%; height: auto; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; touch-action: pan-y; }
  .sim .btns { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.6rem 0; }
  .sim .btns button { min-height: 2.6rem; padding: 0 1rem; border: 1px solid #94a3b8; border-radius: 999px; background: #fff; color: #134e4a; font: 700 0.95rem "Source Sans 3", system-ui, sans-serif; cursor: pointer; }
  .sim .btns button.go { background: #0f766e; border-color: #0f766e; color: #fff; }
  .sim .read { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.5rem; margin-top: 0.4rem; }
  .sim .read div { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.4rem 0.7rem; font-size: 0.92rem; color: #475569; }
  .sim .read b { display: block; font-size: 1.2rem; color: #134e4a; }
  .sim .status { margin: 0.6rem 0 0; padding: 0.5rem 0.8rem; border-radius: 8px; background: #f0fdfa; border: 1px solid #99f6e4; font-weight: 600; color: #134e4a; }
  .sim .key { font-size: 0.9rem; color: #475569; margin: 0.4rem 0 0; }
  .sim .key i { display: inline-block; width: 0.8em; height: 0.8em; border-radius: 50%; vertical-align: -0.05em; margin: 0 0.25em 0 0.6em; }
  @media print { .sim { display: none !important; } }
</style>
"""


def sim(sid, mode, title, intro, key):
    reads = {"free": [("Particles on the left", "l0"), ("Particles on the right", "r0")],
             "two": [("Yellow: left | right", "y"), ("Blue: left | right", "b")],
             "osmo": [("Water molecules in A", "wl"), ("Water molecules in B", "wr")]}[mode]
    return ('<div class="sim print-hide" id="%s" data-mode="%s">\n  <h3>%s</h3>\n  <p>%s</p>\n'
            '  <canvas width="720" height="300" aria-label="Animation of moving particles"></canvas>\n  <p class="key">%s</p>\n'
            '  <div class="btns"><button type="button" class="go" data-act="play">&#9654; Start</button><button type="button" data-act="reset">&#8634; Start again</button></div>\n'
            '  <div class="read">%s<div>Time (steps)<b data-r="t">0</b></div></div>\n  <p class="status" aria-live="polite">Press Start.</p>\n</div>\n'
            % (sid, mode, title, intro, key, "".join('<div>%s<b data-r="%s">-</b></div>' % r for r in reads)))


SIM_JS = r"""
document.querySelectorAll('.sim').forEach(function (box) {
  var mode = box.dataset.mode, cv = box.querySelector('canvas'), ctx = cv.getContext('2d');
  var W = cv.width, H = cv.height, MID = W / 2, P = [], run = false, t = 0, raf = null;
  var playB = box.querySelector('[data-act=play]'), st = box.querySelector('.status');
  var lvl = [H, H];            // osmo: liquid surface height (y of surface) on each side
  var COL = { a: '#3b82f6', y: '#eab308', s: '#f97316', w: '#60a5fa' };
  function add(n, x0, x1, kind, r) { for (var i = 0; i < n; i++) P.push({ x: x0 + Math.random() * (x1 - x0), y: 20 + Math.random() * (H - 40), vx: 0, vy: 0, k: kind, r: r }); }
  function reset() {
    P = []; t = 0;
    if (mode === 'free') add(140, 8, 70, 'a', 4.5);
    if (mode === 'two') { add(70, 8, MID - 8, 'y', 4.5); add(70, MID + 8, W - 8, 'a', 4.5); }
    if (mode === 'osmo') { add(24, 8, MID - 10, 's', 8); add(6, MID + 10, W - 8, 's', 8); add(170, 8, MID - 8, 'w', 2.6); add(170, MID + 8, W - 8, 'w', 2.6); }
    lvl = [70, 70];
    draw(); readout();
  }
  function side(p) { return p.x < MID ? 0 : 1; }
  function top(s) { return mode === 'osmo' ? lvl[s] + 6 : 6; }
  function step() {
    var sucr = [0, 0], wat = [0, 0];
    if (mode === 'osmo') P.forEach(function (p) { if (p.k === 's') sucr[side(p)]++; else wat[side(p)]++; });
    P.forEach(function (p) {
      var sp = p.k === 's' ? 1.2 : 3;
      p.vx = 0.86 * p.vx + (Math.random() - 0.5) * sp; p.vy = 0.86 * p.vy + (Math.random() - 0.5) * sp;
      var s0 = side(p), nx = p.x + p.vx, ny = p.y + p.vy;
      var crosses = (mode !== 'free') && ((p.x < MID) !== (nx < MID));
      if (crosses) {
        var pore = (ny % 36) > 12 && (ny % 36) < 30;   // gaps in the membrane
        var ok = pore && (mode === 'two' || p.k === 'w');
        if (ok && mode === 'osmo') {  // water held around sucrose molecules is not free to cross
          var free = Math.max(0.08, 1 - 4 * sucr[s0] / Math.max(1, wat[s0]));
          ok = Math.random() < free;
        }
        if (!ok) { p.vx = -p.vx; nx = p.x; }
      }
      p.x = nx; p.y = ny;
      var s = side(p), lo = top(s) + p.r, hi = H - 6 - p.r;
      var xl = (mode !== 'free' && s === 1) ? MID + 0.01 : 6 + p.r, xr = (mode !== 'free' && s === 0) ? MID - 0.01 : W - 6 - p.r;
      if (mode !== 'free' && crosses) { xl = 6 + p.r; xr = W - 6 - p.r; }
      if (p.x < xl) { p.x = xl; p.vx = Math.abs(p.vx); } if (p.x > xr) { p.x = xr; p.vx = -Math.abs(p.vx); }
      if (p.y < lo) { p.y = lo; p.vy = Math.abs(p.vy); } if (p.y > hi) { p.y = hi; p.vy = -Math.abs(p.vy); }
    });
    if (mode === 'osmo') {   // liquid level follows the number of water molecules on each side
      [0, 1].forEach(function (s) { var target = H - 6 - (H - 76) * wat[s] / 170 * 0.98; lvl[s] += (Math.max(16, target) - lvl[s]) * 0.05; });
    }
  }
  function draw() {
    ctx.clearRect(0, 0, W, H);
    if (mode === 'osmo') {
      ctx.fillStyle = '#e0f2fe'; ctx.fillRect(6, lvl[0], MID - 6, H - 6 - lvl[0]); ctx.fillRect(MID, lvl[1], W - 6 - MID, H - 6 - lvl[1]);
      ctx.strokeStyle = '#0369a1'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(6, lvl[0]); ctx.lineTo(MID, lvl[0]); ctx.moveTo(MID, lvl[1]); ctx.lineTo(W - 6, lvl[1]); ctx.stroke();
      ctx.setLineDash([5, 4]); ctx.strokeStyle = '#94a3b8'; ctx.beginPath(); ctx.moveTo(6, 70); ctx.lineTo(W - 6, 70); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = '#475569'; ctx.font = 'bold 16px Source Sans 3, sans-serif'; ctx.fillText('A', 14, 24); ctx.fillText('B', W - 26, 24);
      ctx.font = '13px Source Sans 3, sans-serif'; ctx.fillText('starting level', W / 2 + 10, 64);
    } else { ctx.fillStyle = '#e0f2fe'; ctx.fillRect(6, 6, W - 12, H - 12); }
    ctx.strokeStyle = '#3f3f46'; ctx.lineWidth = 3; ctx.strokeRect(4, 4, W - 8, H - 8);
    if (mode !== 'free') {   // membrane with gaps
      ctx.strokeStyle = mode === 'osmo' ? '#0f766e' : '#475569'; ctx.lineWidth = 4;
      for (var y = 0; y < H; y += 36) { ctx.beginPath(); ctx.moveTo(MID, Math.max(6, y - 6)); ctx.lineTo(MID, Math.min(H - 6, y + 12)); ctx.stroke(); }
    } else {
      ctx.setLineDash([4, 6]); ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(MID, 6); ctx.lineTo(MID, H - 6); ctx.stroke(); ctx.setLineDash([]);
    }
    P.forEach(function (p) { ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fillStyle = COL[p.k]; ctx.fill(); if (p.r > 3) { ctx.lineWidth = 1; ctx.strokeStyle = 'rgba(0,0,0,0.35)'; ctx.stroke(); } });
  }
  function count(k) { var c = [0, 0]; P.forEach(function (p) { if (p.k === k) c[side(p)]++; }); return c; }
  function setR(k, v) { var e = box.querySelector('[data-r="' + k + '"]'); if (e) e.textContent = v; }
  function readout() {
    setR('t', Math.round(t / 40));
    var msg;
    if (mode === 'free') {
      var c = count('a'); setR('l0', c[0]); setR('r0', c[1]);
      msg = c[0] - c[1] > 14 ? 'Net movement from left to right: down the concentration gradient.' : 'About the same on both sides. The particles still move, but there is no net movement now.';
    } else if (mode === 'two') {
      var y = count('y'), b = count('a'); setR('y', y[0] + ' | ' + y[1]); setR('b', b[0] + ' | ' + b[1]);
      msg = (Math.abs(y[0] - y[1]) > 12 || Math.abs(b[0] - b[1]) > 12) ? 'Yellow particles move net to the right, blue ones net to the left. Each substance moves down its own concentration gradient.' : 'Both substances are now evenly spread on both sides: no net movement.';
    } else {
      var w = count('w'); setR('wl', w[0]); setR('wr', w[1]);
      msg = t < 200 ? 'Only the small water molecules fit through the membrane. The big sucrose molecules cannot.' :
        (lvl[0] < lvl[1] - 10 ? 'Net movement of water from B to A: the level in A rises and the level in B falls. This is osmosis.' : 'Water molecules are crossing in both directions...');
    }
    st.textContent = msg;
  }
  function loop() { if (!run) return; for (var i = 0; i < (mode === 'free' ? 10 : 6); i++) { step(); t++; } draw(); if (t % 40 === 0) readout(); raf = requestAnimationFrame(loop); }
  playB.addEventListener('click', function () { run = !run; playB.innerHTML = run ? '&#10074;&#10074; Pause' : '&#9654; Start'; if (run) loop(); });
  box.querySelector('[data-act=reset]').addEventListener('click', function () { reset(); st.textContent = run ? '' : 'Press Start.'; });
  reset();
});
"""
