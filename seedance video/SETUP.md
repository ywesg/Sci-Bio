# Seedance kit — setup

This folder makes short videos for the HTML lessons with **Seedance 2.5** (BytePlus ModelArk).
You give it a prompt file and, if you like, a first and last frame.

Everything the scripts need is in this folder **except the API key**, which lives in `~/seedance-key.txt`, outside OneDrive.

---

## Where things go

This folder (`seedance video/`) sits inside the starter kit next to `lessons/`, exactly as shipped. Keep that layout.

```
your-project/
  lessons/                    <- the HTML lessons
  seedance video/             <- this kit
    seedance_video.sh  image_gen.py  token_budget.sh  hold_last_frame.sh
    tools/                    <- Swift helpers (video compression, hold last frame)
    prompts/                  <- one .txt file per video
    refs/                     <- first/last frame images (optional)
    output/                   <- finished videos (created on first run)
    compressed/               <- small web copies (created automatically)

~/seedance-key.txt            <- the API key: in your home folder, NOT in the project folder
```

**Why the key is outside the project:** if the project folder is in OneDrive, Google Drive or Dropbox, everything in it is uploaded to the cloud and to every device on that account, and school IT can see it. Anyone who gets the key can spend on your ModelArk account. The scripts read `~/seedance-key.txt` automatically.

---

## Steps

### 2. Make sure Python 3 and Pillow are available

In Terminal:

```bash
python3 --version
```

If macOS offers to install the "command line developer tools", click **Install**, wait, then run it again. Python 3.9 or newer is fine. The developer tools also give you `swift`, which `hold_last_frame.sh` uses.

```bash
python3 -m pip install --user Pillow
```

### 3. Create an API key

1. In the ModelArk console, create a **new** API key for this computer. Use a separate key for each computer so each can be revoked on its own.
2. Make sure the model `dreamina-seedance-2-5-260628` is **activated** on whichever account the key belongs to. A new account starts with nothing activated.
3. If the key is billed to a school account, check that's allowed.

Copy the key in the browser, then:

```bash
pbpaste > ~/seedance-key.txt && chmod 600 ~/seedance-key.txt
```

### 4. Make the scripts runnable

```bash
cd path/to/your-project/seedance\ video && chmod +x *.sh
```



### 5. Test without spending anything

```bash
./seedance_video.sh --prompt-file prompts/example_demo.txt --dry-run
```

You should see `DRY RUN: POST https://ark.ap-southeast.bytepluses.com/...` and `No API call made.`

### 6. First real video (a cheap draft)

```bash
./seedance_video.sh --prompt-file prompts/example_demo.txt
```

That's 4 s at 480p, about **40,000 tokens**. It polls every 15 s and saves to `output/`.

---

## Using it

| What you want | Command |
|---|---|
| Video from a prompt only | `./seedance_video.sh --prompt-file prompts/NAME.txt` |
| Start from a picture | `... --first refs/start.jpg` |
| Start and end on pictures | `... --first refs/start.jpg --last refs/end.jpg` |
| Final quality | `... --resolution 720p` (or `1080p`) |
| Longer | `... --duration 6` (4–30 s) |
| Portrait or square (prompt-only) | `... --ratio 9:16` or `--ratio 1:1` |
| With generated sound | `... --audio` |
| Check before paying | add `--dry-run` |
| Hold the final frame 2 s longer | `./hold_last_frame.sh output/VIDEO.mp4 2` (free, runs locally) |
| Script stopped while waiting | `./seedance_video.sh --fetch TASK_ID --name NAME` (no new charge) |

Images can be JPEG, PNG or iPhone HEIC. The script shrinks them, matches the last frame to the first, and strips all metadata (including GPS) before sending. The originals aren't changed.

**Workflow that worked:** draft at 480p, change one thing in the prompt at a time, and only run 720p once a draft looks right. Each run is a fresh random take, so the final won't copy the draft exactly.

**Putting a video in a lesson:** copy the MP4 (and a poster image) into `lessons/intro/` and use `lesson_kit.intro_video(...)` (see ../lesson-tools/build_sample_lesson.py).

**Writing prompts:** say "locked-off static camera" if the camera shouldn't move, and give a timeline ("0–1 seconds: …, 1–3 seconds: …"). See `prompts/example_demo.txt`.

### Costs seen so far (Seedance 2.5, no audio)

| Video | Tokens |
|---|---|
| 4 s, 480p | 39,820 |
| 6 s, 480p | 59,525 |
| 6 s, 720p | 131,322 |

Cost goes up roughly with seconds × pixels. Audio and reference inputs add more.

### Seedance rules worth knowing

- Real human faces in input images are rejected, so **don't use photos of students or staff** as frames. That also keeps student data out of a third-party service.
- First/last-frame mode can't be mixed with reference images, video or audio. This script only uses first/last frames.
- Image limits: 300–6000 px per side, aspect ratio 0.4–2.5. The script checks these.

---
