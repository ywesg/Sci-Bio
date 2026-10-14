# AI marking for the Revision Questions (Section B), optional

Students write an answer, press *Check against the mark scheme* and tick the points found (this works with no AI at all). If you also deploy the
marking function, a purple *Ask the AI tutor for feedback* button appears and the answer is marked by an AI model.

## How it works
- `functions/mark.mjs` is a Netlify Function at `/.netlify/functions/mark`. The browser sends only `{page, qid, answer}`. The question, marking points and
  model answer are looked up on the server in `functions/scheme.json`, so the endpoint cannot be used as a general chatbot.
- `scheme.json` is generated from your revision data: `python3 lesson-tools/build_ai_scheme.py` (`deploy.sh` runs it for you).
- `lessons/ai-marking-config.js` holds the address: `window.AI_MARKING = { url: "/.netlify/functions/mark" };`. Set `url` to `""` to switch the button off.
- Limits in the function: 30 answers per device per hour and a daily total (set `DAILY_LIMIT_TOTAL`). Answers that try to instruct the marker are scored 0.
  The counters live in memory, so they are approximate and reset when the function restarts. The real hard ceiling is a token limit set in the provider console.

## Set-up checklist
1. Pick a provider. We used **BytePlus ModelArk** with DeepSeek-V4.1-Flash (model id `deepseek-v4-1-flash-260910`; activate it in the Ark console first).
   The function also supports the **Anthropic API** (`PROVIDER=anthropic`); this is billed separately from a claude.ai chat subscription.
2. Create a **separate API key just for marking**, restricted to that one model, and set a token usage limit on it in the provider console.
3. In Netlify > Site configuration > Environment variables set: `ARK_API_KEY`, `ARK_MODEL`, `SUBJECT` (e.g. Biology), `ALLOWED_ORIGIN` (your site address),
   `HOURLY_LIMIT_PER_IP` (30), `DAILY_LIMIT_TOTAL` (e.g. 600). On Netlify's free plan these cannot be made "secret"; they are normal variables, so use a restricted key.
4. Install the Netlify CLI outside the project (see `deploy.sh`: it looks in `~/.local/netlify-cli` with Node 22) so `deploy.sh` can deploy the pages **and** the function together.
   The plain API deploy in `deploy.sh` cannot include functions and would DELETE a live marking function.
5. Check your school allows students' answers to be sent to an outside AI service. The page already tells students not to type names or personal details.

## What we found when choosing a model (26 test cases: full marks, partial, wrong, wrong method, no working, reworded, misconceptions, and tricks)
| Model | In range | Notes |
|---|---|---|
| DeepSeek-V4.1-Flash | 26 of 26 | about 1.4 s, about 364 input and 70 output tokens per marking |
| DeepSeek-V4-Flash GA | 24 of 26 | gave full marks to a trick answer and to an answer with no working |
| Seed 2.1 Turbo | 24 of 26 | under-marked two full answers |
| GLM-5.3 Flash | 24 of 26 | under-marked two full answers |

Always send `thinking: {"type": "disabled"}` (the function does): with thinking on, one answer took up to 106 s and thousands of extra tokens with no better marks.
About 430 tokens per marking means a 5,000,000-token limit is roughly 11,000 markings. Re-test with your own subject's questions before trusting any model.
