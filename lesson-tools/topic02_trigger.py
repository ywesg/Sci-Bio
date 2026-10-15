"""Trigger animation for lesson 2.1: someone comes out of a toilet and the smell spreads along the corridor
until a person waiting at the other end smells it. A short cartoon on a canvas (about 15 s), with Play / Replay.
Use: HTML + JS (JS once on the page). Hidden in print."""

HTML = """<style>
  .trig { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.1rem; margin: 1.25rem 0; }
  .trig canvas { display: block; width: 100%; height: auto; border: 1px solid #e2e8f0; border-radius: 8px; }
  .trig .btns { display: flex; gap: 0.5rem; margin: 0.6rem 0 0; }
  .trig .btns button { min-height: 2.6rem; padding: 0 1rem; border: 1px solid #0f766e; border-radius: 999px; background: #0f766e; color: #fff; font: 700 0.95rem "Source Sans 3", system-ui, sans-serif; cursor: pointer; }
  .trig .trig-cap { margin: 0.6rem 0 0; padding: 0.5rem 0.8rem; border-radius: 8px; background: #f0fdfa; border: 1px solid #99f6e4; font-weight: 600; color: #134e4a; }
  .trig .trig-cap.end { background: #dcfce7; border-color: #86efac; }
  @media print { .trig { display: none !important; } }
</style>
<div class="trig print-hide" id="trig">
  <canvas width="720" height="320" aria-label="Cartoon: a person comes out of a toilet at one end of a corridor. Green smell particles spread out along the corridor until a person waiting at the far end smells them and holds their nose."></canvas>
  <p class="trig-cap" aria-live="polite">Press Play to watch.</p>
  <div class="btns"><button type="button" class="go" data-act="play">&#9654; Play</button></div>
</div>
"""

JS = r"""
(function () {
  var box = document.getElementById('trig'); if (!box) return;
  var cv = box.querySelector('canvas'), ctx = cv.getContext('2d'), W = cv.width, H = cv.height, FLOOR = 262;
  var cap = box.querySelector('.trig-cap'), btn = box.querySelector('[data-act=play]');
  var f = 0, run = false, P = [], react = -1, R = Math.random;
  var CAPS = ['Someone is using the toilet at the end of the corridor. The door is shut.',
              'The door opens. Smell particles escape into the corridor.',
              'Nobody carries the smell, but it keeps spreading along the corridor…',
              'The person at the other end can smell it! How did the smell particles get there?'];
  function person(x, shirt, mood, walk) {
    var sw = walk ? Math.sin(f * 0.25) * 9 : 0;
    ctx.strokeStyle = '#3f3f46'; ctx.lineWidth = 6; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(x - 6, FLOOR - 50); ctx.lineTo(x - 6 + sw, FLOOR - 2); ctx.moveTo(x + 6, FLOOR - 50); ctx.lineTo(x + 6 - sw, FLOOR - 2); ctx.stroke();
    ctx.fillStyle = shirt; ctx.beginPath(); ctx.roundRect ? ctx.roundRect(x - 19, FLOOR - 112, 38, 66, 12) : ctx.rect(x - 19, FLOOR - 112, 38, 66); ctx.fill();
    ctx.fillStyle = '#f2c9a0'; ctx.strokeStyle = '#3f3f46'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(x, FLOOR - 134, 21, 0, 6.2832); ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#1f2937'; ctx.lineWidth = 2;
    if (mood === 'eww') {   // screwed-up eyes, wavy mouth, hand holding the nose
      ctx.beginPath(); ctx.moveTo(x - 11, FLOOR - 141); ctx.lineTo(x - 4, FLOOR - 137); ctx.lineTo(x - 11, FLOOR - 133); ctx.moveTo(x + 11, FLOOR - 141); ctx.lineTo(x + 4, FLOOR - 137); ctx.lineTo(x + 11, FLOOR - 133); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x - 9, FLOOR - 121); for (var i = 1; i <= 6; i++) ctx.lineTo(x - 9 + i * 3, FLOOR - 121 + (i % 2 ? -3 : 0)); ctx.stroke();
      ctx.strokeStyle = shirt; ctx.lineWidth = 7; ctx.beginPath(); ctx.moveTo(x - 16, FLOOR - 100); ctx.lineTo(x - 10, FLOOR - 128); ctx.stroke();
      ctx.fillStyle = '#f2c9a0'; ctx.beginPath(); ctx.arc(x - 3, FLOOR - 129, 6, 0, 6.2832); ctx.fill(); ctx.strokeStyle = '#3f3f46'; ctx.lineWidth = 1.5; ctx.stroke();
      ctx.fillStyle = '#fff'; ctx.strokeStyle = '#334155'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(x - 62, FLOOR - 185, 34, 18, 0, 0, 6.2832); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#b91c1c'; ctx.font = 'bold 17px Source Sans 3, sans-serif'; ctx.textAlign = 'center'; ctx.fillText('Eww!', x - 62, FLOOR - 179); ctx.textAlign = 'left';
    } else {
      ctx.beginPath(); ctx.arc(x - 7, FLOOR - 138, 2.5, 0, 6.2832); ctx.arc(x + 7, FLOOR - 138, 2.5, 0, 6.2832); ctx.fill();
      ctx.beginPath(); ctx.arc(x, FLOOR - 128, 7, 0.3, 2.84); ctx.stroke();
    }
  }
  function scene() {
    var open = Math.min(1, Math.max(0, (f - 60) / 30));
    ctx.fillStyle = '#fef3c7'; ctx.fillRect(0, 0, W, FLOOR);                    // corridor wall
    ctx.fillStyle = '#cbd5e1'; ctx.fillRect(0, FLOOR, W, H - FLOOR);            // floor
    ctx.fillStyle = '#e2e8f0'; for (var x = 0; x < W; x += 60) ctx.fillRect(x, FLOOR, 2, H - FLOOR);
    ctx.fillStyle = '#334155'; ctx.fillRect(56, 76, 108, FLOOR - 76);           // door frame and the dark doorway
    ctx.fillStyle = '#e0f2fe'; ctx.fillRect(62, 82, 96, FLOOR - 82);             // inside the toilet
    ctx.fillStyle = '#fff'; ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 2;      // toilet bowl inside
    ctx.beginPath(); ctx.ellipse(110, FLOOR - 22, 26, 14, 0, 0, 6.2832); ctx.fill(); ctx.stroke(); ctx.fillRect(122, FLOOR - 70, 16, 46); ctx.strokeRect(122, FLOOR - 70, 16, 46);
    var dw = 96 * (1 - 0.82 * open);                                             // the door swings open (gets narrower)
    ctx.fillStyle = '#b45309'; ctx.fillRect(62, 82, dw, FLOOR - 82); ctx.strokeStyle = '#78350f'; ctx.strokeRect(62, 82, dw, FLOOR - 82);
    ctx.fillStyle = '#fde68a'; ctx.beginPath(); ctx.arc(62 + dw - 10, 175, 4, 0, 6.2832); ctx.fill();
    ctx.fillStyle = '#1d4ed8'; ctx.fillRect(84, 46, 52, 24); ctx.fillStyle = '#fff'; ctx.font = 'bold 16px Source Sans 3, sans-serif'; ctx.fillText('WC', 98, 64);
    ctx.fillStyle = '#a16207'; ctx.fillRect(560, FLOOR - 40, 120, 10); ctx.fillRect(568, FLOOR - 30, 8, 30); ctx.fillRect(664, FLOOR - 30, 8, 30);   // bench
  }
  function step() {
    if (f > 75 && f < 420 && R() < 0.5) { var a = R() * 2 - 1; P.push({ x: 130 + R() * 20, y: 110 + R() * 140, vx: Math.cos(a), vy: Math.sin(a) }); }
    P.forEach(function (p) {
      var a = (R() - 0.5) * 0.35, c = Math.cos(a), s = Math.sin(a), vx = p.vx * c - p.vy * s, vy = p.vx * s + p.vy * c, m = Math.hypot(vx, vy) || 1;
      p.vx = vx / m * 1.4; p.vy = vy / m * 1.4; p.x += p.vx; p.y += p.vy;
      if (p.x < 66) { p.x = 66; p.vx = Math.abs(p.vx); } if (p.x > W - 6) { p.x = W - 6; p.vx = -Math.abs(p.vx); }
      if (p.y < 20) { p.y = 20; p.vy = Math.abs(p.vy); } if (p.y > FLOOR - 6) { p.y = FLOOR - 6; p.vy = -Math.abs(p.vy); }
    });
    if (react < 0 && P.filter(function (p) { return Math.abs(p.x - 620) < 70 && p.y > FLOOR - 170; }).length >= 4) react = f;
  }
  function draw() {
    scene();
    P.forEach(function (p) { ctx.beginPath(); ctx.arc(p.x, p.y, 3.6, 0, 6.2832); ctx.fillStyle = '#84cc16'; ctx.fill(); ctx.lineWidth = 1; ctx.strokeStyle = '#3f6212'; ctx.stroke(); });
    if (f > 90 && f < 160) person(110 - (f - 90) * 2.6, '#7c3aed', 'happy', true);   // walks out and away to the left
    person(620, '#0f766e', react >= 0 ? 'eww' : 'happy', false);
    var k = f < 60 ? 0 : f < 160 ? 1 : react < 0 ? 2 : 3;
    cap.textContent = CAPS[k];
  }
  function loop() { if (!run) return; step(); f++; draw();
    if (react >= 0 && f > react + 150) { run = false; btn.innerHTML = '&#8634; Replay'; cap.classList.add('end'); return; }
    requestAnimationFrame(loop); }
  btn.addEventListener('click', function () {
    if (!run && (react >= 0 || f === 0)) { f = 0; P = []; react = -1; cap.classList.remove('end'); }
    run = !run; btn.innerHTML = run ? '&#10074;&#10074; Pause' : '&#9654; Play'; if (run) loop(); });
  draw(); cap.textContent = 'Press Play to watch.';
})();
"""
