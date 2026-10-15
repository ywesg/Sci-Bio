# Ms Emily's Biology Lessons — project notes

Live site: https://msemily-biolesson.netlify.app (Netlify publishes `lessons/` from the `main` branch on every push).
Teacher: Ms Emily (Windows user, non-technical — explain steps simply). Course: SEC G2 + G3 Science (Biology), 2027 syllabus.

## Working rules (agreed with the teacher)
- **Never push to `main` unless she says "publish".** Do all edits on the draft branch (`draft/cell-redraw`, or a new `draft/...` branch), commit and push the draft branch to keep work safe.
- To let her check: build a zip of `lessons/` and send it ("preview zip"). She extracts it and opens `lessons\index.html`. YouTube embeds show Error 153 offline; that's expected.
- On "publish": `git checkout main && git merge --ff-only <draft> && git push origin main`, then confirm the live page changed.
- Save tokens: short replies, few screenshots, batch work.
- Copyright: do not put textbook/slide images (Marshall Cavendish) on the site. Redraw in our own SVG style, or use free-licence images (Wikimedia Commons, Wellcome Collection CC BY) with a credit line under each.
- Topics appear only when added to `TOPICS` in `lesson-tools/build_index.py`. G3-only topics (9–12) get `g3=True`; release them only when she says.

## Build
```
cd lesson-tools
python3 build_index.py          # home page
python3 build_topic01.py        # Topic 1 lessons 1.1, 1.2 (figures in topic01_figs.py, SA:V visuals in topic01_sav.py)
python3 build_revision.py       # revision pages from rev_data_*.py (Section B: pt() marking points; test model answers score full marks)
python3 add_navigation.py       # contents bar + prev/next
cd .. && NODE_PATH=$(npm root -g) node lesson-tools/make_pdfs_playwright.js   # PDFs
```
Helpers in `lesson_kit.py`: `page`, `mcq`, `calc`, `video` (YouTube, with "Watch on YouTube" fallback), `labeller` (drag-and-drop labels; `ring=True` for tiny parts like ribosomes), `sorter`, `explorer`.
Lesson numbering follows her textbook (e.g. 1.1, 1.2). Put the textbook learning outcomes at the top of each lesson. She supplies notes, slides and YouTube links per topic.

## Status
- Topic 1 (Cell Structure and Organisation) done and live: 1.1 What Are Cells?, 1.2 How Are Cells Adapted to Their Functions?, Revision Questions (Q1–7).
- Open item: cell labelling diagrams are cramped on small phones (a sideways-scroll fix was proposed, not done).
- AI intro videos (BytePlus Seedance) on hold — her account approval was pending. Key would go in env var `ARK_API_KEY`, never in chat.
- Next: Topic 2 (Movement of Substances) when she sends notes + learning outcomes.
