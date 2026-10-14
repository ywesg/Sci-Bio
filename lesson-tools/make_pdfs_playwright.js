// Makes a PDF of every lesson with Playwright (an alternative to make_pdfs.sh). Run from the project folder: node lesson-tools/make_pdfs_playwright.js
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, '..', 'lessons'), b = await chromium.launch();
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html') && !['index.html', 'lesson-template.html'].includes(f))) {
    const p = await b.newPage(); await p.goto('file://' + path.join(dir, f), { waitUntil: 'networkidle' }); await p.waitForTimeout(800);
    const out = path.join(dir, f.replace('.html', '.pdf'));
    await p.pdf({ path: out, format: 'A4', margin: { top: '14mm', bottom: '14mm', left: '14mm', right: '14mm' }, printBackground: true });
    console.log(f, Math.round(fs.statSync(out).size / 1024) + ' KB'); await p.close();
  }
  await b.close();
})();
