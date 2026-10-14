# Lessons learned

Notes from building a full Physics lesson site (about 75 lesson pages, 12 revision pages, intro videos for seven topics) with this toolkit.

## Content and design
- **Write each lesson by script first, then edit by hand.** The generators are a first draft only. Once a lesson is hand-edited, never re-run its builder over it.
- **Every lesson must print.** The pages have print styles; `make_pdfs.sh` uses headless Chrome. Check the PDF of a new page type before building a whole chapter.
- **Syllabus fit matters more than breadth.** Check each lesson against your exam board's syllabus and drop anything outside it. Mark lessons that only some classes study with the badge so other students can skip them.
- **Show the picture, add the labels yourself.** For realistic illustrations, generate a label-free photo-style image with Seedream, then add chips/captions in HTML. AI text inside images is unreliable.
- **Accessibility:** big touch targets, visible focus, alt text on images, captions/subtitles on videos, colour is never the only signal.
- **Multiple choice answers should not all be "B".** `build_revision.py` cycles the correct letter A-D.
- **Keyword mark schemes need forgiving regexes.** Test that each model answer scores full marks, and that sentence breaks and plurals do not break a match. Tell students the checker can miss correct wordings, so they tick/untick points themselves.

## Seedance (AI video)
- **Cost:** about 40,000 tokens for 4 s at 480p without sound; about 77,000 for 8 s at 480p with sound. 720p costs roughly 2.2x more. Draft at 480p.
- **Filter:** scenes that look like famous films can be rejected with "OutputVideoSensitiveContentDetected". In our experience a rejected run was not billed (the console showed only the successful runs). Use original characters and real-world settings with a sci-fi/lab look; redesign the whole scene rather than tweaking words.
- **Real faces:** do not use photos of real people (students, staff) as input frames. Seedance rejects them and it keeps student data out of a third-party service.
- **Describe the camera and lens.** Ask for "natural rectilinear lens, no fisheye, no vignette, image fills the whole frame". The word "porthole" once produced a fisheye frame with black corners. Ask for plain clothing with no flags or badges.
- **Do not trust the physics/biology.** AI video can get the science wrong (a pool ball that never hit another ball and balls that appeared from nowhere; a ball floating in the air above the sea). Check at least 12 frames across the clip, track every object, and reject clips that teach the wrong thing.
- **Check the audio.** AI video cannot count words or guarantee a clip ends after the last word. Measure the speech timing (we looked at energy in the 300-3000 Hz band per 50 ms) and set the subtitle start from it. A subtitle that does not match the spoken words is worse than none: regenerate instead.
- **Say when the line is spoken** in the prompt ("speaking after about four seconds") and shorten any lead-in so the whole sentence fits in 8 s.
- **Compress every video** before deploying: a 4-5 MB clip becomes 1-1.5 MB with the bundled tool (`seedance_video.sh` does it automatically into `compressed/`). Keep mono audio mono.
- **Autoplay with sound is usually blocked** by browsers. The intro block tries sound, and falls back to muted with a "Click for sound" button (it restarts the video). Subtitles are a separate toggle.
- **Track your token package.** `token_budget.sh` adds up runs made through this folder, but it cannot see runs from other computers or the console. Compare with the console now and then and update `token-budget.json`.

## Netlify
- **Credits:** the personal plan gives 1,000 credits a month; a production deploy costs about 15 credits and bandwidth costs credits too. When credits run out, production deploys are paused until the monthly reset ("Forbidden" from the CLI/API). Batch deploys, and keep media small.
- **Functions:** the plain digest deploy removes functions. Use the CLI deploy in `deploy.sh` (it deploys a draft with the function, then promotes it).
- **Secrets:** on the free plan environment variables cannot be marked secret, so the AI key is visible to anyone with access to the Netlify site. Use a separate, model-restricted key with a token limit.
- **Token:** keep the Netlify token outside any cloud-synced folder.

## AI marking
- Choose the model by testing it on your own subject: we compared four models on 26 cases and the "best" on paper failed trick and no-working cases. See `ai-marking/README.md`.
- Switch thinking off, keep answers short, look up the scheme on the server, rate-limit per device and per day, and set a hard token limit in the provider console.
- Tell students not to type personal details, and check your school's rules before sending answers to an outside service.

## Working with Claude on a project like this
- Give each topic's first lesson one memorable intro video; ask for a few variants and keep the best.
- Ask for the previews to be sent as files and give clear yes/no decisions ("use this version", "regenerate with bigger waves").
- Batch the deploys, and sync to GitHub only when the work is in a good state.
