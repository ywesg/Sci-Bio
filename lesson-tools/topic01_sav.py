"""Surface area to volume ratio visuals for lesson 1.2: 3-D block drawings of shapes, cutting a cube into smaller cubes,
and a simulated agar-cube diffusion experiment. Used by build_topic01.py (HTML + JS)."""

CSS = """<style>
  .viz { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.1rem 1.25rem; margin: 1.25rem 0; }
  .viz h3 { margin-top: 0; color: #134e4a; font-size: 1.08rem; }
  .viz .btns { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.6rem 0; }
  .viz .btns button { min-height: 2.6rem; padding: 0 0.9rem; border: 1px solid #94a3b8; border-radius: 999px; background: #fff; color: #134e4a; font: 700 0.95rem "Source Sans 3", system-ui, sans-serif; cursor: pointer; }
  .viz .btns button[aria-pressed="true"] { background: #134e4a; border-color: #134e4a; color: #fff; }
  .viz .stage { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.4rem; }
  .viz .stage svg { display: block; width: 100%; height: 230px; margin: 0; }
  .viz .nums { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.5rem; margin: 0.7rem 0 0.3rem; }
  .viz .nums div { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.45rem 0.7rem; }
  .viz .nums b { display: block; font-size: 1.25rem; color: #134e4a; }
  .viz .nums span { font-size: 0.85rem; color: #475569; }
  .viz .nums .big b { color: #be185d; }
  .agar-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.6rem; align-items: end; text-align: center; }
  .agar-row svg { width: 100%; height: auto; max-height: 190px; margin: 0; }
  .agar-row .pc { font-weight: 700; color: #134e4a; }
  .agar-row .meter { height: 0.6rem; background: #fce7f3; border-radius: 999px; overflow: hidden; margin: 0.25rem 0.4rem 0; }
  .agar-row .meter i { display: block; height: 100%; width: 0; background: #0f766e; }
  .viz input[type=range] { width: 100%; accent-color: #0f766e; }
  .viz .timer { font-weight: 800; color: #134e4a; font-size: 1.1rem; }
  .cellphoto img { max-height: 380px; object-fit: contain; background: #0f172a0d; }
  .setup svg { width: 100%; max-width: 520px; height: auto; display: block; margin: 0.4rem auto; }
  @media print { .viz { background: #fff; break-inside: avoid; } .viz .btns, .viz input[type=range], .viz .play { display: none !important; } }
</style>
"""

SHAPES = """<div class="viz" id="sav">
  <h3>Try it: same volume, different shapes</h3>
  <p>Each shape is built from the same <strong>64 small cubes</strong> (volume = 64 units&sup3;). Pick a shape and look at how much surface it has.</p>
  <div class="btns print-hide" role="group" aria-label="Choose a shape">
    <button type="button" data-d="4,4,4" aria-pressed="true">Cube 4 &times; 4 &times; 4</button>
    <button type="button" data-d="8,8,1" aria-pressed="false">Flat sheet 8 &times; 8 &times; 1</button>
    <button type="button" data-d="16,2,2" aria-pressed="false">Rod 16 &times; 2 &times; 2</button>
    <button type="button" data-d="64,1,1" aria-pressed="false">Long thin strand 64 &times; 1 &times; 1</button>
  </div>
  <div class="stage"><svg id="sav-svg" role="img" aria-label="A 3-D drawing of the chosen shape made of small cubes"></svg></div>
  <div class="nums" aria-live="polite">
    <div><b id="sav-v">64</b><span>volume (units&sup3;)</span></div>
    <div><b id="sav-a">96</b><span>surface area (units&sup2;)</span></div>
    <div class="big"><b id="sav-r">1.5 : 1</b><span>SA : V ratio</span></div>
  </div>
  <p class="working" id="sav-work"></p>
  <p class="working">Same volume, but the <strong>flatter</strong> or <strong>longer and thinner</strong> the shape, the larger the surface area. That is why a red blood cell is a flattened disc and a root hair cell has a long, narrow extension.</p>
</div>
"""

CUT = """<div class="viz" id="cut">
  <h3>Try it: cut a big cube into small cubes</h3>
  <p>Start with one 3 cm cube. Cut it into 1 cm cubes. The total <strong>volume stays the same</strong>, but look what happens to the surface.</p>
  <div class="btns print-hide" role="group" aria-label="Whole or cut">
    <button type="button" data-cut="0" aria-pressed="true">One 3 cm cube</button>
    <button type="button" data-cut="1" aria-pressed="false">Cut into 27 &times; 1 cm cubes</button>
  </div>
  <div class="stage"><svg id="cut-svg" role="img" aria-label="A 3 cm cube, which can be split into 27 small 1 cm cubes"></svg></div>
  <div class="nums" aria-live="polite">
    <div><b id="cut-v">27 cm&sup3;</b><span>total volume</span></div>
    <div><b id="cut-a">54 cm&sup2;</b><span>total surface area</span></div>
    <div class="big"><b id="cut-r">2 : 1</b><span>SA : V ratio</span></div>
  </div>
  <p class="working" id="cut-work"></p>
  <p class="working"><strong>Link to cells:</strong> a large organism is made of many small cells rather than one huge cell. Each small cell has a large SA : V ratio, so substances can enter and leave it quickly enough.</p>
</div>
"""

AGAR = """<div class="viz" id="agar">
  <h3>Experiment: diffusion into agar cubes of different sizes</h3>
  <div class="setup">
    <svg viewBox="0 0 580 200" role="img" aria-label="Three pink agar cubes of 1, 2 and 3 cm placed in a beaker of dilute hydrochloric acid">
      <path d="M90 30 V170 a12 12 0 0 0 12 12 H418 a12 12 0 0 0 12 -12 V30" fill="none" stroke="#334155" stroke-width="4"/>
      <rect x="94" y="70" width="332" height="108" fill="#e0f2fe" opacity="0.8"/>
      <path d="M94 70 H426" stroke="#38bdf8" stroke-width="2"/>
      <g fill="#ec4899" stroke="#9d174d" stroke-width="2">
        <rect x="150" y="152" width="20" height="20"/><rect x="225" y="132" width="40" height="40"/><rect x="320" y="112" width="60" height="60"/>
      </g>
      <g font-family="Source Sans 3, system-ui, sans-serif" font-size="14" fill="#1f2937" text-anchor="middle">
        <text x="160" y="146">1 cm</text><text x="245" y="126">2 cm</text><text x="350" y="106">3 cm</text>
        <text x="260" y="22" font-weight="700">dilute hydrochloric acid</text>
      </g>
      <g font-family="Source Sans 3, system-ui, sans-serif" font-size="13" fill="#9d174d"><text x="440" y="140">agar with</text><text x="440" y="156">phenolphthalein</text><text x="440" y="172">(pink: alkaline)</text></g>
    </svg>
  </div>
  <ol>
    <li>Make agar containing an alkali and <strong>phenolphthalein</strong> indicator. It is <strong>pink</strong> because it is alkaline.</li>
    <li>Cut cubes of side <strong>1 cm, 2 cm and 3 cm</strong>.</li>
    <li>Place them in <strong>dilute hydrochloric acid</strong>. As the acid <strong>diffuses</strong> into the agar, the indicator turns <strong>colourless</strong>.</li>
    <li>Every few minutes, take the cubes out and <strong>cut them in half</strong> to see how far the acid has reached.</li>
  </ol>
  <p><strong>Run the experiment:</strong> press Play, or drag the time slider. You are looking at each cube cut in half: <span style="display:inline-block;width:0.9em;height:0.9em;background:#ec4899;vertical-align:middle;border-radius:2px"></span> still pink (no acid yet), <span style="display:inline-block;width:0.9em;height:0.9em;background:#fdfcf5;border:1px solid #94a3b8;vertical-align:middle;border-radius:2px"></span> colourless (acid has diffused in).</p>
  <div class="btns print-hide"><button type="button" class="play" id="agar-play">&#9654; Play</button><button type="button" id="agar-reset">Reset</button></div>
  <label class="print-hide" for="agar-t">Time in acid: <span class="timer" id="agar-time">0 min</span></label>
  <input class="print-hide" type="range" id="agar-t" min="0" max="15" step="0.1" value="0">
  <div class="stage"><div class="agar-row" id="agar-row"></div></div>
  <table>
    <tr><th>Cube side</th><th>Surface area</th><th>Volume</th><th>SA : V</th><th>Time to turn fully colourless*</th></tr>
    <tr><td>1 cm</td><td>6 cm&sup2;</td><td>1 cm&sup3;</td><td><strong>6 : 1</strong></td><td>5 min</td></tr>
    <tr><td>2 cm</td><td>24 cm&sup2;</td><td>8 cm&sup3;</td><td><strong>3 : 1</strong></td><td>10 min</td></tr>
    <tr><td>3 cm</td><td>54 cm&sup2;</td><td>27 cm&sup3;</td><td><strong>2 : 1</strong></td><td>15 min</td></tr>
  </table>
  <p class="working">*In this simple model the acid moves 1 mm into the agar every minute from every face. Real times depend on the acid and the agar, and diffusion slows down as it goes deeper, but the pattern is the same.</p>
  <p class="keyidea"><strong>Conclusion:</strong> the <strong>smallest</strong> cube has the <strong>largest SA : V ratio</strong>, so the whole of its volume is reached by diffusion first. The bigger the cube, the longer the acid takes to reach its centre.</p>
</div>
"""

JS = r"""
(function () {
  var C = 0.866, S = 0.5;
  function P(x, y, z, u) { return [((x - y) * C * u).toFixed(1), (((x + y) * S - z) * u).toFixed(1)]; }
  function poly(pts, fill) { return '<polygon points="' + pts.map(function (p) { return p.join(','); }).join(' ') + '" fill="' + fill + '" stroke="#0f766e" stroke-width="1.6" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>'; }
  function line(a, b) { return '<line x1="' + a[0] + '" y1="' + a[1] + '" x2="' + b[0] + '" y2="' + b[1] + '" stroke="#0f766e" stroke-opacity="0.55" stroke-width="1" vector-effect="non-scaling-stroke"/>'; }
  // a box of l x w x h unit cubes at (ox, oy, oz), with grid lines on the three faces you can see
  function box(ox, oy, oz, l, w, h, u, grid, col) {
    col = col || ['#99f6e4', '#5eead4', '#2dd4bf'];
    var X = ox + l, Y = oy + w, Z = oz + h, s = '', i;
    s += poly([P(ox, oy, Z, u), P(X, oy, Z, u), P(X, Y, Z, u), P(ox, Y, Z, u)], col[0]);       // top
    s += poly([P(X, oy, oz, u), P(X, Y, oz, u), P(X, Y, Z, u), P(X, oy, Z, u)], col[2]);       // right face (x = X)
    s += poly([P(ox, Y, oz, u), P(X, Y, oz, u), P(X, Y, Z, u), P(ox, Y, Z, u)], col[1]);       // left face (y = Y)
    if (grid) {
      for (i = 1; i < l; i++) { s += line(P(ox + i, oy, Z, u), P(ox + i, Y, Z, u)) + line(P(ox + i, Y, oz, u), P(ox + i, Y, Z, u)); }
      for (i = 1; i < w; i++) { s += line(P(ox, oy + i, Z, u), P(X, oy + i, Z, u)) + line(P(X, oy + i, oz, u), P(X, oy + i, Z, u)); }
      for (i = 1; i < h; i++) { s += line(P(X, oy, oz + i, u), P(X, Y, oz + i, u)) + line(P(ox, Y, oz + i, u), P(X, Y, oz + i, u)); }
    }
    return s;
  }
  function fit(svg, inner, pts) {          // set the viewBox around the drawing
    var xs = pts.map(function (p) { return +p[0]; }), ys = pts.map(function (p) { return +p[1]; });
    var x0 = Math.min.apply(0, xs), x1 = Math.max.apply(0, xs), y0 = Math.min.apply(0, ys), y1 = Math.max.apply(0, ys), pad = 14;
    svg.setAttribute('viewBox', (x0 - pad) + ' ' + (y0 - pad) + ' ' + (x1 - x0 + 2 * pad) + ' ' + (y1 - y0 + 2 * pad));
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svg.innerHTML = inner;
  }
  function corners(ox, oy, oz, l, w, h, u) { var r = []; [0, l].forEach(function (a) { [0, w].forEach(function (b) { [0, h].forEach(function (c) { r.push(P(ox + a, oy + b, oz + c, u)); }); }); }); return r; }

  // ---------- 1. same volume, different shapes
  var sv = document.getElementById('sav-svg');
  if (sv) {
    var bs = document.querySelectorAll('#sav button');
    function shape(b) {
      var d = b.dataset.d.split(',').map(Number), l = d[0], w = d[1], h = d[2], A = 2 * (l * w + l * h + w * h), V = l * w * h;
      bs.forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      fit(sv, box(0, 0, 0, l, w, h, 10, true), corners(0, 0, 0, l, w, h, 10));
      document.getElementById('sav-a').textContent = A;
      document.getElementById('sav-r').textContent = (A / V).toFixed(2).replace(/\.?0+$/, '') + ' : 1';
      document.getElementById('sav-work').textContent = 'Surface area = 2 × (' + l + '×' + w + ' + ' + l + '×' + h + ' + ' + w + '×' + h + ') = ' + A + ' units².   SA : V = ' + A + ' : ' + V + '.';
    }
    bs.forEach(function (b) { b.addEventListener('click', function () { shape(b); }); });
    shape(bs[0]);
  }

  // ---------- 2. cut a 3 cm cube into 27 small cubes
  var cv = document.getElementById('cut-svg');
  if (cv) {
    var gap = 0, target = 0, anim = null, cb = document.querySelectorAll('#cut button');
    function drawCut() {
      var s = '', all = [], cubes = [], u = 26, i, j, k;
      for (i = 0; i < 3; i++) for (j = 0; j < 3; j++) for (k = 0; k < 3; k++) cubes.push([i, j, k]);
      cubes.sort(function (a, b) { return (a[0] + a[1] + a[2]) - (b[0] + b[1] + b[2]) || a[2] - b[2]; });   // far cubes first
      if (gap < 0.01) { s = box(0, 0, 0, 3, 3, 3, u, true); all = corners(0, 0, 0, 3, 3, 3, u); }
      else cubes.forEach(function (c) { var o = c.map(function (n) { return n * (1 + gap); }); s += box(o[0], o[1], o[2], 1, 1, 1, u, false); all = all.concat(corners(o[0], o[1], o[2], 1, 1, 1, u)); });
      all = all.concat(corners(0, 0, 0, 3 + 2 * 0.9, 3 + 2 * 0.9, 3 + 2 * 0.9, u));     // keep the frame fixed while it opens up
      fit(cv, s, all);
    }
    function setCut(c) {
      cb.forEach(function (x) { x.setAttribute('aria-pressed', x.dataset.cut === String(c)); });
      document.getElementById('cut-a').textContent = c ? '162 cm²' : '54 cm²';
      document.getElementById('cut-r').textContent = c ? '6 : 1' : '2 : 1';
      document.getElementById('cut-work').textContent = c ? 'Each 1 cm cube: 6 faces × 1 cm² = 6 cm².  27 cubes × 6 cm² = 162 cm².  SA : V = 162 : 27 = 6 : 1 (three times bigger).'
                                                          : 'One 3 cm cube: 6 faces × (3 × 3) cm² = 54 cm².  Volume = 3 × 3 × 3 = 27 cm³.  SA : V = 54 : 27 = 2 : 1.';
      target = c ? 0.9 : 0; cancelAnimationFrame(anim);
      (function step() { gap += (target - gap) * 0.18; if (Math.abs(target - gap) < 0.005) gap = target; drawCut(); if (gap !== target) anim = requestAnimationFrame(step); })();
    }
    cb.forEach(function (b) { b.addEventListener('click', function () { setCut(+b.dataset.cut); }); });
    setCut(0);
  }

  // ---------- 3. agar cubes in acid (cut in half to show how far the acid has diffused)
  var row = document.getElementById('agar-row');
  if (row) {
    var sizes = [1, 2, 3], rate = 0.1, t = 0, timer = null, sl = document.getElementById('agar-t'), play = document.getElementById('agar-play');
    row.innerHTML = sizes.map(function (s) {
      return '<div><svg viewBox="0 0 170 190" role="img" aria-label="' + s + ' cm agar cube cut in half"><g id="ag' + s + '"></g></svg>' +
             '<div><strong>' + s + ' cm cube</strong> (SA : V = ' + (6 / s) + ' : 1)</div><div class="meter"><i id="agm' + s + '"></i></div><div class="pc" id="agp' + s + '"></div></div>';
    }).join('');
    function drawAgar() {
      document.getElementById('agar-time').textContent = t.toFixed(1).replace('.0', '') + ' min';
      sizes.forEach(function (s) {
        var px = 48 * s, x0 = 85 - px / 2, y0 = 170 - px, d = Math.min(rate * t, s / 2), core = s - 2 * d, cp = core * 48;
        var g = '<rect x="' + x0 + '" y="' + y0 + '" width="' + px + '" height="' + px + '" fill="#fdfcf5" stroke="#94a3b8" stroke-width="2"/>';
        if (core > 0) g += '<rect x="' + (85 - cp / 2) + '" y="' + (y0 + (px - cp) / 2) + '" width="' + cp + '" height="' + cp + '" fill="#ec4899"/>';
        if (d > 0 && core > 0) g += '<rect x="' + x0 + '" y="' + y0 + '" width="' + px + '" height="' + px + '" fill="none" stroke="#94a3b8" stroke-width="2"/>';
        g += '<text x="85" y="' + (y0 - 8) + '" text-anchor="middle" font-family="Source Sans 3, system-ui, sans-serif" font-size="13" fill="#475569">cut face</text>';
        document.getElementById('ag' + s).innerHTML = g;
        var reached = 1 - Math.pow(Math.max(core, 0) / s, 3);
        document.getElementById('agm' + s).style.width = (reached * 100) + '%';
        document.getElementById('agp' + s).textContent = core <= 0 ? 'All colourless!' : Math.round(reached * 100) + '% reached by acid';
      });
    }
    function set(v) { t = Math.max(0, Math.min(15, v)); sl.value = t; drawAgar(); }
    sl.addEventListener('input', function () { stop(); set(+sl.value); });
    function stop() { clearInterval(timer); timer = null; play.innerHTML = '&#9654; Play'; }
    play.addEventListener('click', function () {
      if (timer) { stop(); return; }
      if (t >= 15) set(0);
      play.innerHTML = '&#10074;&#10074; Pause';
      timer = setInterval(function () { set(t + 0.1); if (t >= 15) stop(); }, 60);
    });
    document.getElementById('agar-reset').addEventListener('click', function () { stop(); set(0); });
    set(0);
  }
})();
"""
