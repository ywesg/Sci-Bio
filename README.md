# Ms Emily's Biology Lessons

Interactive lesson notes for G2 and G3 SEC Science (Biology), built with the lesson-site starter kit below.

## How this site is put together
- `lesson-tools/build_index.py` writes the home page (`lessons/index.html`): the pixel-art banner, the G2/G3 switch and one card per lesson.
  **A topic only appears on the site once it is listed in `TOPICS` there.** Mark G3-only topics or lessons with `g3=True`; students who pick "G2" do not see them.
- `lesson-tools/build_topic01.py` (+ `topic01_figs.py` for the drawings) builds Topic 1 lessons 1.1 and 1.2. Lesson numbers follow the textbook.
- `lesson-tools/rev_data_01_cells.py` holds the Topic 1 revision questions (`python3 build_revision.py`). A structured question uses `stem` (text + figure) on its first part and `part="(a)"`, `"(b)"`... on each part.
- Drag-and-drop labelling: `L.labeller(...)` in `lesson_kit.py` (diagrams), and `topic01_figs.photo(...)` to place labels on a photo. Micrographs in `lessons/img/` come from Wikimedia Commons; each has a credit line under it (keep these).
- After any change: `cd lesson-tools && python3 build_index.py && python3 add_navigation.py`, then remake the PDFs
  (`./make_pdfs.sh` on a Mac with Chrome, or `node lesson-tools/make_pdfs_playwright.js` where Playwright is installed).
- Publishing: Netlify is linked to this GitHub repo and publishes the `lessons/` folder (see `netlify.toml`). Every push to `main` is a new deploy, which uses Netlify credits, so batch changes.
- The AI tutor button is off (`lessons/ai-marking-config.js` has an empty `url`).

---

# Lesson site starter kit

The reusable tools behind a teacher-made, interactive HTML lesson website (built first for a Physics course, now packaged for a new subject such as Biology).
It contains **no physics lessons, images or videos**: only the tools, a blank template and small samples.

What you get:
- **Lesson pages**: one HTML page per lesson, with built-in multiple-choice and number-answer questions, picture labels, SVG diagrams, YouTube embeds and a printable PDF version.
- **Revision Questions pages**: Section A multiple choice (answers cycle A-D) and Section B free response, checked against a keyword mark scheme the student can tick/untick, with an optional **AI tutor** button.
- **Intro videos** made with Seedance (BytePlus), played at the top of a lesson with sound, subtitles and a "Click for sound" fallback; scripts also compress them for the web.
- **Realistic labelled pictures** with Seedream (image generation script).
- **Deploy**: one command to publish to Netlify; one to make PDFs; one to back up to GitHub.

## Folder map
```
lessons/                 The website. index.html (home), lesson-template.html (blank hand-written lesson), ai-marking-config.js, img/ (pictures), intro/ (videos)
lesson-tools/            Python builders (NOT published)
  lesson_kit.py            page shell + question/picture/video helpers. Set SUBJECT at the top.
  lesson_style.html        the shared CSS for every lesson
  intro_video_block.html   template for the intro video (used by lesson_kit.intro_video)
  build_sample_lesson.py   a worked example of a lesson built with the kit
  build_revision.py        builds Revision Questions pages from rev_data_*.py   (see rev_data_sample.py for the format)
  build_ai_scheme.py       writes the AI marking scheme from the revision data
  add_navigation.py        adds "On this page" and Previous/Next links in index order
ai-marking/              Optional AI tutor: Netlify Function + README (read it before turning it on)
seedance video/          Video + image generation scripts, token tracker and SETUP.md
make_pdfs.sh  deploy.sh  sync_to_github.sh   publishing scripts (read the comments at the top of each)
LESSONS-LEARNED.md       What worked and what went wrong. Please read before you start.
```

## Quick start (macOS)
1. Put this folder somewhere (a OneDrive/Dropbox folder is fine for the files; see "Git" below). Open Terminal in it.
2. Check the tools: `python3 --version` (3.9+). Google Chrome must be installed for the PDF script.
3. Try the sample: `cd lesson-tools && python3 build_sample_lesson.py && python3 build_revision.py && python3 add_navigation.py`, then open `lessons/index.html` in a browser.
4. Make it yours: set `SUBJECT` in `lesson_kit.py`; edit `lessons/index.html` (keep its structure: `<h2>Chapter</h2><ul class="lesson-list"><li><a href="file.html">1. Title</a></li>...</ul>`); write lessons either by hand (copy `lessons/lesson-template.html`) or with `lesson_kit`.
   A good pattern: build a chapter's first draft with a script, then edit the HTML by hand and do NOT re-run the builder over the edited file.
5. After adding a lesson to `index.html`, run `python3 lesson-tools/add_navigation.py` (safe to re-run).
6. PDFs: `./make_pdfs.sh`. Publish: see below.

## Publishing to Netlify
1. Create a Netlify site (a plain static site; drag-drop one file first if you need the site to exist). Put its name in `netlify-site.txt` (copy `netlify-site.txt.example`).
2. Make a Netlify Personal Access Token and save it OUTSIDE the project: `pbpaste > ~/.netlify_token && chmod 600 ~/.netlify_token`.
3. `./deploy.sh --dry-run`, then `./deploy.sh`. Only `lessons/` is uploaded. Needs `jq` (`brew install jq`).
4. Netlify's free plan is credit-based. Each production deploy costs credits and so does bandwidth (big videos!). Batch your deploys and compress videos. See LESSONS-LEARNED.md.

## Git / GitHub (backup and sharing)
Keep the `.git` folder out of any cloud-synced folder. `sync_to_github.sh` copies the project to a separate clone (`~/Desktop/code/<folder>-git` by default, or set `GIT_COPY`), commits and pushes.
One-time: create a PRIVATE GitHub repo, `git clone` it to that path, copy `.gitignore` into it, then run `./sync_to_github.sh "message"`.
Never commit API keys or tokens (the scripts read them from `~/seedance-key.txt` and `~/.netlify_token`, outside the project).

## Things to replace before you publish
- `SUBJECT`, `BADGE` text, `lessons/index.html` title/colours, the "Back to ... lessons" wording.
- The sample revision data and sample lesson (delete `rev_data_sample.py` and the sample pages when you have real ones).
- Anything that mentions a school or syllabus code. Check what your school allows (AI-generated media, sending student answers to an AI service, hosting student-facing content publicly).
