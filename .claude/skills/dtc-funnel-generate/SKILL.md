# /dtc-funnel-generate — Research-First Intake + Guided Funnel Build

Builds a complete DTC advertorial funnel: presell education page + offer page. Claude researches the market, proposes the strategy, gets one confirmation, then builds all sections in-session — one section per turn, with a dedicated reviewer and optional fix pass after each copy section.

**Trigger:** type `/dtc-funnel-generate` in Claude Code

---

## What This Produces

```
[FUNNEL_DIR]/
├── artifacts/
│   ├── market-research.md       — competitor ads, Amazon review mining, avatar language
│   ├── locked-decisions.md      — confirmed villain, thesis, coined term, 5 reasons
│   ├── reason-headlines.md      — 5 reason H3 headlines
│   ├── presell-intro.md         — header + intro block
│   ├── five-reasons.md          — all 5 reason bodies
│   ├── presell-bridge-cta.md    — coined term bridge + things to check + CTA
│   ├── education-page-copy.md   — assembled full presell markdown
│   ├── offer-page-copy.md       — full offer page markdown
│   └── congruence-qa.md         — final QA report
├── presell-v2.html              — education page (no product name, no price)
├── offer-v2.html                — product reveal + offer page
├── image-briefs.json            — NB2 prompts for presell images
└── generated_images/            — fal.ai generated images
```

---

## Step 1: Ask Two Questions

Ask both at once before doing anything else:

> "Two quick questions to get started:
> 1. What is your product name? (e.g. "Mat & Vic's Premium Socks")
> 2. What should I call your funnel folder? This is just the folder name where all the files get saved. Use something short with no spaces (e.g. `funnel`, `cotton-socks`, `summer-v2`).
>
> I'll research the market and come back with a proposed strategy before building anything."

Wait for both answers. Set:
- `PRODUCT_NAME` = their answer to Q1
- `FUNNEL_DIR` = their answer to Q2

The buy buttons on the offer page will use `YOUR_COLLECTION_URL` as a placeholder — the collection URL gets filled in at publish time via `/shopify-publish`. For most DTC Shopify stores this is a `/collections/all` or specific collection page, so customers can browse by style, length, etc.

Every path in this skill resolves from `FUNNEL_DIR`. Never assume a path.

---

## Step 2: Autonomous Research (Before Any More Questions)

With just the product URL and funnel name, run the research autonomously. Do not ask the user anything else until this is done.

**Run in parallel:**

**A. Meta Ad Library scan**
Go to `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=DE&q=[category keyword]&search_type=keyword_unordered`
- Identify who is running DTC advertorial funnels vs. brand ads
- Note the villain angles being used (what are they attacking?)
- Note the formats running (video, image, carousel)
- Note any coined terms visible in copy

**B. Amazon review mining**
Find the product's Amazon listing or a leading competitor's. Read the AI review summary and individual reviews.
- Capture verbatim language — exact words customers use to describe the problem
- Capture the before/after language ("I used to... now I...")
- Note recurring complaints about the current solution
- Note what customers praise most about the product (reveals what was missing before)

**C. Avatar segmentation**
Based on A + B, identify the avatar most in active tension — carrying a specific frustration and open to re-evaluating their current solution. Document:
- Who they are (demographic + situation)
- What they currently believe is causing their problem
- What language they use (verbatim phrases, not your paraphrase)
- What has to happen for them to buy

Save all findings to `[FUNNEL_DIR]/artifacts/market-research.md`.

---

## Step 3: Propose Strategy — One Confirmation Question

After research, propose the full strategic foundation in one message:

```
Here's what I found and what I'd recommend for your funnel:

**The villain:** [specific material/mechanism — not just "cheap socks"]
**Why it works:** [one sentence connecting villain to the research findings]

**The avatar's problem in their own words:** "[verbatim or near-verbatim from reviews]"

**The 5 reasons [villain] fails:**
1. [specific mechanism]
2. [specific mechanism]
3. [specific mechanism]
4. [specific mechanism]
5. [specific mechanism]

**Proposed coined term:** [term] — [one sentence: the natural parallel that makes it feel discovered, not invented]

**The page 1 headline:** "[5 Reasons Why X Is Y]"

Does this match your product and your customers? Any corrections before I build?
```

This is the one human gate. Incorporate any corrections and save to `[FUNNEL_DIR]/artifacts/locked-decisions.md`. Then begin building sections.

---

## Step 4: Build Sections — One Per Turn

Build each section in the current session, one turn at a time. After each copy section, run a dedicated reviewer. If the reviewer says REVISE, run a fix pass before moving to the next section.

There are 11 core sections + up to 4 conditional fix passes = up to 15 total.

When starting each section, say: "Starting Section [N] — [name]." When done: "Section [N] complete. Starting reviewer."

---

### Section 1 — Generate reason headlines

**Purpose:** Write the 5 Reason H3 headlines and confirm they all connect to the same villain.

**Input files:** `[FUNNEL_DIR]/artifacts/locked-decisions.md`

**Acceptance criteria:**
- Read locked-decisions.md — all decisions are already confirmed, do not re-litigate
- Write 5 Reason headlines in H3 format — each names a specific physical mechanism
- Verify all 5 connect to the villain named in locked-decisions.md
- Verify reading level: sixth grade. No jargon as labels.
- Save as `[FUNNEL_DIR]/artifacts/reason-headlines.md`
- Do NOT write body copy yet

---

### Section 2 — Write presell intro

**Purpose:** Write the presell header, kicker, H1, thesis sentence, and intro block painting the "before" state.

**Input files:** `[FUNNEL_DIR]/artifacts/locked-decisions.md`, `[FUNNEL_DIR]/artifacts/reason-headlines.md`

**Acceptance criteria:**
- Write: kicker ("Consumer Guide · [Category]") + H1 (listicle headline) + italic thesis sentence
- Write intro block: 4–6 short paragraphs, specific physical moments the avatar recognizes, no product mention anywhere
- End with bridge: "Here are the [N] reasons [villain] is designed to fail you."
- Save as `[FUNNEL_DIR]/artifacts/presell-intro.md`
- Self-check: grep "criterion\|criteria\|structural anchor\|engineering target" → nothing
- Self-check: product name not present anywhere

---

### Section 2R — Review presell intro

**Purpose:** Quality gate on the presell intro — read it fresh as if seeing it for the first time.

**Input files:** `[FUNNEL_DIR]/artifacts/presell-intro.md`, `[FUNNEL_DIR]/artifacts/locked-decisions.md`, `methodology/reviewer-persona.md`

**How to run:** Read all three files fresh. Apply the full reviewer persona. Then write the review.

**Acceptance criteria:**
- Apply every rule in reviewer-persona.md: zero rhetorical questions, one sentence per line, no setup phrases, show don't explain, sixth grade reading level, permission-based framing, no product name
- Context for this review: Solution-Aware presell intro. Coined term: [coinedTerm from locked-decisions.md]. No metaphor system — the coined term is the mechanism name.
- Write review to `[FUNNEL_DIR]/artifacts/review-section-2.md` with:
  - **Verdict: LOCK IT** or **Verdict: REVISE**
  - If REVISE: numbered flag list, each with section + specific issue + what to do instead
  - If LOCK IT: skip flags, proceed to Section 3

---

### Section 2F — Fix presell intro *(runs only if Section 2R verdict is REVISE)*

**Input files:** `[FUNNEL_DIR]/artifacts/presell-intro.md`, `[FUNNEL_DIR]/artifacts/review-section-2.md`

**Acceptance criteria:**
- Apply every flagged item from review-section-2.md — do not skip any flag
- Do not rewrite sections that passed — only fix what was flagged
- Save corrected version as `[FUNNEL_DIR]/artifacts/presell-intro.md` (overwrite)
- Self-check: grep "criterion\|criteria" → nothing; product name → nothing

---

### Section 3 — Write 5 reason sections

**Purpose:** Write all 5 reason bodies with image placeholders.

**Input files:** `[FUNNEL_DIR]/artifacts/locked-decisions.md`, `[FUNNEL_DIR]/artifacts/presell-intro.md`

**Acceptance criteria:**
- Write all 5 reasons: H3 headline + `[IMAGE PLACEHOLDER: r1]` + body copy
- Body copy structure per reason: mechanism → consequence → reframe (permission-based, blame the villain not the person) → 1-line italic forward tease
- Each reason names a specific physical mechanism — not a vague benefit
- Vary sentence length. One sentence per line with line breaks.
- No rhetorical questions anywhere.
- No "Here's what...", "Here's the thing...", "Let me explain..." or similar setup phrases
- Save as `[FUNNEL_DIR]/artifacts/five-reasons.md`
- Self-check: grep "criterion\|criteria\|Here's what\|Here's the thing\|Let me explain" → nothing

---

### Section 3R — Review 5 reason sections

**Input files:** `[FUNNEL_DIR]/artifacts/five-reasons.md`, `[FUNNEL_DIR]/artifacts/locked-decisions.md`, `methodology/reviewer-persona.md`

**How to run:** Read all three files fresh. Apply the full reviewer persona. Pay special attention to: no rhetorical questions, one sentence per line, forward teases create pull (not just summaries), no setup phrases, body before brain in each reason opening.

- Write review to `[FUNNEL_DIR]/artifacts/review-section-3.md`
- Verdict: LOCK IT or REVISE with specific flags

---

### Section 3F — Fix 5 reason sections *(runs only if Section 3R verdict is REVISE)*

**Input files:** `[FUNNEL_DIR]/artifacts/five-reasons.md`, `[FUNNEL_DIR]/artifacts/review-section-3.md`

- Apply every flagged item. Preserve all passing sections untouched.
- Save corrected version as `[FUNNEL_DIR]/artifacts/five-reasons.md` (overwrite)
- Self-check: grep "criterion\|criteria\|Here's what\|Here's the thing" → nothing

---

### Section 4 — Write coined term bridge + things to check + presell CTA

**Purpose:** Write the second half of the presell: coined term reveal, 5 "Things to check" spec section, existence bridge, CTA.

**Input files:** `[FUNNEL_DIR]/artifacts/locked-decisions.md`, `[FUNNEL_DIR]/artifacts/five-reasons.md`

**Acceptance criteria:**
- Write coined term bridge: introduce the coined term with its natural parallel (the thing it mirrors in the real world), then definition box (teal left-border callout, equation format)
- Write 5 "Things to check" section: headings as "Thing to check #1" (never "Criterion"), each with body + teal callout box with specific threshold/number
- Write "Does a [product] like this exist?" bridge: 2–3 paragraphs, no product name, end on intrigue
- Write final CTA: "See the [Thing] That Gets It Right →" teal button + one reassurance line below
- CTA link: `offer-v2.html` — relative link (no server required)
- Save as `[FUNNEL_DIR]/artifacts/presell-bridge-cta.md`
- Self-check: product name not present anywhere in this artifact

---

### Section 4R — Review coined term bridge + presell CTA

**Input files:** `[FUNNEL_DIR]/artifacts/presell-bridge-cta.md`, `[FUNNEL_DIR]/artifacts/locked-decisions.md`, `methodology/reviewer-persona.md`

**How to run:** Read all three files fresh. Pay special attention to: coined term feels discovered not invented, CTA pulls forward not backward, no product name anywhere.

- Write review to `[FUNNEL_DIR]/artifacts/review-section-4.md`
- Verdict: LOCK IT or REVISE with specific flags

---

### Section 4F — Fix coined term bridge + presell CTA *(runs only if Section 4R verdict is REVISE)*

**Input files:** `[FUNNEL_DIR]/artifacts/presell-bridge-cta.md`, `[FUNNEL_DIR]/artifacts/review-section-4.md`

- Apply every flagged item. Preserve passing sections untouched.
- Save corrected version as `[FUNNEL_DIR]/artifacts/presell-bridge-cta.md` (overwrite)
- Self-check: product name → nothing

---

### Section 5 — Assemble full presell + write image briefs

**Purpose:** Assemble the complete presell markdown. Write image-briefs.json.

**Input files:** `[FUNNEL_DIR]/artifacts/presell-intro.md`, `[FUNNEL_DIR]/artifacts/five-reasons.md`, `[FUNNEL_DIR]/artifacts/presell-bridge-cta.md`

**Acceptance criteria:**
- Assemble in order: kicker/H1/thesis → intro → 5 reasons → coined term bridge → things to check → existence bridge → CTA
- Save as `[FUNNEL_DIR]/artifacts/education-page-copy.md`
- Write `[FUNNEL_DIR]/image-briefs.json`: 5 entries (r1–r5), one per reason
- Each entry: id, style, lighting, scene, primary_object (description + material_detail + position), energy, constraints, negative_prompt, aspect_ratio: "3:2"
- Each prompt shows the failure mechanism — not the product, not the solution, no lifestyle, no faces above ankle
- Self-check: grep "criterion\|criteria" on assembled copy → nothing; product name → nothing

---

### Section 6 — Write offer page copy

**Purpose:** Write the full offer page in markdown. This is where the product is revealed.

**Input files:** `[FUNNEL_DIR]/artifacts/education-page-copy.md`, `[FUNNEL_DIR]/artifacts/locked-decisions.md`

**Acceptance criteria:**
- H1: plain language payoff of the presell — "This is the [product] that gets every one of those things right" (no "criterion", no "specification" as jargon)
- Write all offer page sections in order:
  1. Hero: H1 + product image + star rating + CTA button
  2. Credibility bar: 3 proof points (e.g. "Ships from Austria · 30-day trial · 4.8 stars")
  3. Promo banner: mid-page placement, NOT at page top
  4. Formula section: one block per key ingredient/layer — label as "comfort layer / tough layer / fit layer" (never "structural anchor", "engineering target", "polyamide percentage" as headings)
  5. How it solves each reason: 5 blocks, one per presell reason
  6. Testimonials: 6 placeholder quotes, each confirming a specific mechanism from the presell. Mark every one with `<!-- PLACEHOLDER: replace with real customer quote -->`. Never present fabricated quotes as real.
  7. Bundle section: 3 tiers — Trial / Most Popular / Complete. Middle card gets popular badge.
  8. Second bundle CTA at bottom (dark background)
  9. FAQ: 5–6 questions
- All buy button links: `YOUR_COLLECTION_URL` placeholder — never `href="#"`
- Back link to presell: `presell-v2.html` — relative link
- Save as `[FUNNEL_DIR]/artifacts/offer-page-copy.md`
- Self-check: grep "criterion\|criteria\|specifically engineered" → nothing; grep `href="#"` → nothing

---

### Section 6R — Review offer page copy

**Input files:** `[FUNNEL_DIR]/artifacts/offer-page-copy.md`, `[FUNNEL_DIR]/artifacts/locked-decisions.md`, `[FUNNEL_DIR]/artifacts/education-page-copy.md`, `methodology/reviewer-persona.md`

**How to run:** Read all four files fresh. Apply full reviewer persona to offer-page-copy.md. Also check congruence: every reason from education-page-copy.md must have a corresponding proof/solution named on the offer page.

- Write review to `[FUNNEL_DIR]/artifacts/review-section-6.md`
- Verdict: LOCK IT or REVISE with specific flags (include any congruence gaps)

---

### Section 6F — Fix offer page copy *(runs only if Section 6R verdict is REVISE)*

**Input files:** `[FUNNEL_DIR]/artifacts/offer-page-copy.md`, `[FUNNEL_DIR]/artifacts/education-page-copy.md`, `[FUNNEL_DIR]/artifacts/review-section-6.md`

- Apply every flagged item — including any congruence fixes
- Preserve passing sections untouched
- Save corrected version as `[FUNNEL_DIR]/artifacts/offer-page-copy.md` (overwrite)
- Self-check: grep "criterion\|criteria\|specifically engineered" → nothing; grep `href="#"` → nothing

---

### Section 7 — Build presell HTML

**Purpose:** Convert education-page-copy.md to production HTML.

**Input files:** `[FUNNEL_DIR]/artifacts/education-page-copy.md`, `methodology/funnel-styling.md`

**Acceptance criteria:**
- Read `methodology/funnel-styling.md` first — apply all CSS, font, and layout specs from it
- Convert section by section — do not rewrite, only convert
- Image placeholders: `<div class="reason-image-placeholder" data-reason="r1" style="background:#f5f5f5;height:300px;display:flex;align-items:center;justify-content:center;border-radius:8px;margin-bottom:1.5rem;color:#999;font-size:14px;">Image coming — r1.png</div>` for each reason
- CTA button: `offer-v2.html` — relative link
- viewport meta tag: `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Save as `[FUNNEL_DIR]/presell-v2.html`
- Verify: grep "criterion\|criteria" → nothing; product name → nothing; price → nothing
- Visual check: `open -a "Google Chrome" [FUNNEL_DIR]/presell-v2.html` — confirm it renders, scroll to bottom, confirm CTA button is visible

---

### Section 8 — Build offer page HTML

**Purpose:** Convert offer-page-copy.md to production HTML.

**Input files:** `[FUNNEL_DIR]/artifacts/offer-page-copy.md`, `methodology/funnel-styling.md`

**Acceptance criteria:**
- Read `methodology/funnel-styling.md` first — apply all CSS, font, and layout specs from it
- Convert section by section — do not rewrite, only convert
- Product image: embed as placeholder `<div style="background:#f5f5f5;height:400px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#999;font-size:14px;">Add product photo here</div>` if no image path was provided
- Bundle cards: 3-column desktop, stacked mobile. Middle card: popular badge + highlighted border + teal CTA. Others: dark (#121212) CTA
- All buy buttons: `href="YOUR_COLLECTION_URL"` placeholder
- Promo banner: mid-page, positioned after credibility bar — NOT at page top
- Testimonials: 6 cards, CSS grid 2-column. Each card retains its `<!-- PLACEHOLDER -->` HTML comment.
- Back link to presell: `presell-v2.html` — relative link
- viewport meta tag on page
- Save as `[FUNNEL_DIR]/offer-v2.html`
- Verify: grep `href="#"` → nothing
- Visual check: `open -a "Google Chrome" [FUNNEL_DIR]/offer-v2.html` — confirm it renders, scroll to bundle section, confirm buy buttons are visible

---

### Section 9 — Generate presell images *(requires FAL_KEY)*

**Purpose:** Run fal.ai image generation from image-briefs.json.

**Input files:** `[FUNNEL_DIR]/image-briefs.json`

**Acceptance criteria:**
- Check if `[FUNNEL_DIR]/generated_images/r1.png` through `r5.png` already exist and are >10KB — if yes, skip generation
- Check `$FAL_KEY` env var. If not set:
  ```
  env_path = Path(__file__).parent / ".env"
  ```
  Check `.env` in the project root for `FAL_KEY=`. If still not found: tell the user to run `export FAL_KEY=your_key_here` and stop.
- Write and run a generation script (`[FUNNEL_DIR]/generate_presell_images.py`). FAL_KEY reads from env — never hardcoded.
- On failure for any image: write labeled placeholder, continue. Do not block the section.
- Verify: `ls -la [FUNNEL_DIR]/generated_images/r*.png` — all 5 exist

---

### Section 10 — Embed images in presell

**Purpose:** Replace presell image placeholders with the generated images.

**Input files:** `[FUNNEL_DIR]/presell-v2.html`, `[FUNNEL_DIR]/generated_images/` directory

**Acceptance criteria:**
- Replace each `reason-image-placeholder` div with:
  `<img src="generated_images/rN.png" alt="..." style="width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,0.10);margin-bottom:1.5rem;">`
- Image placement: immediately after the H3 reason headline, before body copy paragraph
- Paths: relative to the HTML file — `generated_images/rN.png`
- Verify: grep "reason-image-placeholder" [FUNNEL_DIR]/presell-v2.html → nothing (all replaced)
- Verify: grep -c "generated_images/r" [FUNNEL_DIR]/presell-v2.html → 5

**Note on Shopify deployment:** These relative paths work for local preview. When publishing to Shopify, Claude uploads each image to the Shopify CDN first and rewrites these paths to CDN URLs before creating the page. This is handled automatically in the going-live step — see `methodology/going-live.md`.

---

### Section 11 — Congruence QA

**Purpose:** Run all QA gates. Fix failures. Output qa-report.json.

**Input files:** `[FUNNEL_DIR]/presell-v2.html`, `[FUNNEL_DIR]/offer-v2.html`, `[FUNNEL_DIR]/artifacts/locked-decisions.md`

**Run all 6 gates. Fix any failures before writing the report:**

- **Gate 1 — Presell purity:** grep for product name → nothing; grep for price → nothing
- **Gate 2 — Banned vocabulary:** grep "criterion\|criteria\|structural anchor\|engineering target\|specifically engineered" on both files → nothing
- **Gate 3 — CTA links:** presell CTA href is `offer-v2.html`; offer back link href is `presell-v2.html`; offer buy buttons use `YOUR_COLLECTION_URL` placeholder (not `href="#"`)
- **Gate 4 — Images:** 5 img tags in presell-v2.html, all src starting with `generated_images/`, all referenced files exist and are >10KB
- **Gate 5 — Required sections:** offer page has ≥6 `.testimonial-card` elements; has second CTA section (dark background at bottom); has bundle section with 3 cards
- **Gate 6 — Congruence:** every reason on the presell has a corresponding solution named on the offer page — document the mapping

Save `[FUNNEL_DIR]/artifacts/congruence-qa.md` with per-gate PASS/FAIL + detail.

Save `[FUNNEL_DIR]/qa-report.json`:
```json
{
  "generated": "[ISO timestamp]",
  "funnelDir": "[FUNNEL_DIR]",
  "gates": [
    {"id": "gate-1", "name": "Presell purity", "result": "PASS", "detail": ""},
    {"id": "gate-2", "name": "Banned vocabulary", "result": "PASS", "detail": ""},
    {"id": "gate-3", "name": "CTA links correct", "result": "PASS", "detail": ""},
    {"id": "gate-4", "name": "Images embedded", "result": "PASS", "detail": ""},
    {"id": "gate-5", "name": "Required sections present", "result": "PASS", "detail": ""},
    {"id": "gate-6", "name": "Presell/offer congruence", "result": "PASS", "detail": ""}
  ],
  "allPass": true
}
```

When all gates pass, tell the user:
- Presell: `[FUNNEL_DIR]/presell-v2.html`
- Offer page: `[FUNNEL_DIR]/offer-v2.html`
- Presell images: `[FUNNEL_DIR]/generated_images/r1.png` through `r5.png`
- Full QA report: `[FUNNEL_DIR]/artifacts/congruence-qa.md`

**Ready to publish.** To get these pages live on Shopify — including uploading images to CDN — follow `methodology/going-live.md`. Two things to have ready before publishing: your Shopify API token (from the one-time setup) and your product photo for the offer page hero.

---

## Quality Rules (Active Throughout Every Section)

These apply at every section. Never violate them:

- **No product name on the presell.** Anywhere. Including kicker, headlines, alt text.
- **No price on the presell.** Including hidden in image alt text.
- **Banned vocabulary:** `criterion`, `criteria`, `structural anchor`, `engineering target`, `specifically engineered` — grep and remove.
- **No placeholder links.** Every `href="#"` is a defect.
- **CTA links format:** relative — `offer-v2.html` and `presell-v2.html`. No server required.
- **Image paths format:** relative — `generated_images/rN.png`. No server required.
- **Reviewer sections** read the artifact fresh — no inherited context from writing it.
- **Fix sections** only apply flagged items — do not rewrite passing sections.

---

## Reviewer Persona

The reviewer persona is at `methodology/reviewer-persona.md` in this project folder.

It covers: rhetorical question detection, sentence structure rules, setup phrase kill list, permission-based framing, reading level checks, AI voice detection, body-before-brain test, forward tease quality, CTA direction, and congruence checking.

Load it in full for every reviewer section (2R, 3R, 4R, 6R).

---

## Reference

- Styling spec: `methodology/funnel-styling.md` — fonts, colors, layout, component CSS
- Reviewer persona: `methodology/reviewer-persona.md`
- Ad image generation: `/dtc-ad-generate` skill (in this same project)
- Going live: `methodology/going-live.md` — how to upload to Shopify and make pages accessible
