# /dtc-ad-generate — Mat & Vic's Ad Image Generator

Generates ad concept images for a presell funnel using fal-ai/nano-banana-2. Outputs a review grid where you mark keeps and rejects, then re-runs rejects until the batch is approved.

Works for any funnel — existing or new. Asks two questions at startup to locate the right files.

**Trigger:** type `/dtc-ad-generate` in Claude Code

---

## Prerequisites

Before running for the first time:

```bash
pip install fal-client
export FAL_KEY=your_key_here
```

Get your FAL_KEY at [fal.ai/dashboard](https://fal.ai/dashboard).

---

## What This Produces

```
[funnel-folder]/
├── generate_ad_images.py          — NB2 generation script
├── generated_images/
│   └── ad-concepts/
│       ├── c01.png … c20.png      — latest images (overwritten on regen)
│       └── c01_[timestamp].png    — timestamped originals
├── ad-review.html                 — approval grid
└── artifacts/
    └── ad-concepts.json           — approved manifest (written at finalise)
```

---

## Step 1: Ask Two Questions

Ask both at once before doing anything else:

> "Two quick questions:
> 1. Which funnel are we generating ads for? Give me the folder name (e.g. `funnel`, `magnesium-funnel`, `sleep-v2`). I'll look for it relative to your project root.
> 2. Where is your swipe library? Default is `swipe-file` — just press enter to use that."

Wait for both answers. Set:
- `FUNNEL_DIR` = the folder name they gave (e.g. `funnel`)
- `SWIPE_DIR` = their answer, or `swipe-file` if they just confirmed the default

Every path in this skill resolves from these two values. Never assume a path.

---

## Step 2: Preflight Checks

Run all four checks. Show PASS or FAIL for each.

```bash
# Funnel folder exists?
ls [FUNNEL_DIR]/

# Swipe library exists?
ls [SWIPE_DIR]/ad-formats.json

# fal-client installed?
python3 -c "import fal_client" 2>&1

# FAL_KEY set?
python3 -c "import os; print(bool(os.environ.get('FAL_KEY','')))"
```

**If funnel folder missing:**
> "I can't find a folder called `[FUNNEL_DIR]` in your project. Check the spelling — what folders do you have here? Run `ls` to see."
> Stop. Wait for correction.

**If swipe library missing:**
> "Swipe library not found at `[SWIPE_DIR]/ad-formats.json`. Is it in a different location?"
> Stop. Wait for correction.

**If fal-client missing:**
> "Run `pip install fal-client` then try again."
> Stop. Wait for confirmation.

**If FAL_KEY empty:**
> "Run `export FAL_KEY=your_key_here` in your terminal (get your key at fal.ai/dashboard), then try again."
> Stop. Wait for confirmation.

Also check `.env` in the project root as FAL_KEY fallback:
```bash
grep FAL_KEY .env 2>/dev/null
```

---

## Step 3: Load Strategy

Look for `[FUNNEL_DIR]/artifacts/locked-decisions.md`.

**If it exists:** read it and extract:
- Villain
- Avatar (their problem in their own words)
- 5 Reasons (villain's specific failure modes)
- Presell headline
- Product URL

**If it does not exist:** scan for other funnel artifacts in `[FUNNEL_DIR]/`:
- `presell-v2.html` or `presell.html` — grep for H1 headline, villain language, reason H3s
- `artifacts/presell-intro.md`, `artifacts/five-reasons.md` — extract strategy if present

If enough can be reconstructed, save it as `[FUNNEL_DIR]/artifacts/locked-decisions.md` before continuing.

**If nothing can be found:**
> "I can't find a strategy for this funnel. Two options:
> 1. Point me to the presell page or strategy file and I'll extract it.
> 2. Give me the strategy directly — villain, headline, 5 reasons (one per line), avatar (one sentence), product URL.
>
> Which do you prefer?"

---

## Step 4: Check for Existing Script

Check if `[FUNNEL_DIR]/generate_ad_images.py` already exists.

**If it exists:**
> "I found an existing generation script at `[FUNNEL_DIR]/generate_ad_images.py` with [N] prompts. Use this, or generate fresh concepts for this run?"

Wait for their answer. If they say use existing, skip to Step 6 (Run Generation). If fresh, continue to Step 5.

**If it does not exist:** continue to Step 5.

---

## Step 5: Propose Concepts — One Confirmation Gate

Read `[SWIPE_DIR]/ad-formats.json`. For each concept, pick a swipe by format_type that matches the visual register needed.

Propose 20 concepts as a readable list in chat. For each show:

```
**#01 — UGC Close-Crop (Reason 1: [reason name])**
Format: [visual register]
Swipe: ID [N] — [filename] ([format_type])
Why it fits: [one line]
```

Rules:
- Cover all 5 reasons — at least one concept per reason
- Vary visual registers — no two concepts should feel the same
- Each concept uses a different swipe ID
- Headline-only rule: the presell headline is the ONLY text that appears in any image. No sub-copy, no fabricated claims.
- No product name in any image
- No price in any image (exception: whiteboard/notepad prop formats where handwritten numbers are part of the physical scene)

Say: "Here are 20 concepts — confirm or swap any before I build prompts and generate."

One round of feedback. Then lock and continue.

---

## Step 6: Write NB2 Prompts + Generation Script

For each confirmed concept, write a JSON prompt string:

```python
json.dumps({
    "style": "...",
    "lighting": "...",
    "scene": "...",
    "primary_object": {
        "description": "...",
        "[unique_contextual_key]": "..."
    },
    "supporting_objects": [],
    "energy": "...",
    "headline_overlay": {          # omit if format has no text overlay
        "text": "[exact presell headline]",
        "placement": "...",
        "weight": "heavy/black"
    },
    "constraints": {
        "[unique_contextual_key_for_this_image]": true,
        "[another_unique_key]": "specific value"
    }
})
```

**Critical rules:**
1. Constraint keys must be specific to that image — `heel_damage_must_be_visible_in_sock` not `NOT_clean_sock`
2. Headline overlay text = presell headline verbatim, nothing else
3. People are atmosphere, not subject — describe photographic register and energy, not demographics
4. Editorial register, not lifestyle/brand
5. Aspect ratio: 4:5 for all images

Write the full `[FUNNEL_DIR]/generate_ad_images.py` script. Output dir: `[FUNNEL_DIR]/generated_images/ad-concepts/`. FAL_KEY must read from environment — never hardcode it:

```python
FAL_KEY = os.environ.get("FAL_KEY", "")
if not FAL_KEY:
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("FAL_KEY="):
                FAL_KEY = line.split("=", 1)[1].strip()
                break
if not FAL_KEY:
    print("ERROR: FAL_KEY not set. Run: export FAL_KEY=your_key_here")
    sys.exit(1)
os.environ["FAL_KEY"] = FAL_KEY
```

---

## Step 7: Run Generation

```bash
cd [FUNNEL_DIR] && python3 generate_ad_images.py --ids all
```

Print progress per image. On failure, note `FAILED: cNN — [error]` and continue. At the end: "Generated X/20 images. Failed: [list]."

---

## Step 8: Build Review HTML

Build `[FUNNEL_DIR]/ad-review.html`.

**Layout:** 2-column grid (desktop), 1-column (mobile).

**Each card:**
- Generated image (full width)
- Concept name + format badge + which reason it hits
- Swipe reference thumbnail (side by side with generated image)
- Two toggle buttons: **✓ Keep** (green) / **✗ Regenerate** (red)

**Bottom of page:**
- Live summary bar: "X kept, Y to regenerate, Z undecided"
- "Copy regen IDs" button — copies the exact CLI command (e.g. `python3 generate_ad_images.py --ids c03,c07`)
- "Export JSON" button — downloads `review-selections.json`

**Image paths** (root-relative from project root):
- Generated: `/[FUNNEL_DIR]/generated_images/ad-concepts/cNN.png`
- Swipe refs: `/[SWIPE_DIR]/images/[filename]`

After building, open it:
```bash
open -a "Google Chrome" [absolute path to [FUNNEL_DIR]/ad-review.html]
```

Tell the user: "Review grid is open. Mark keeps and rejects, then copy the regen IDs and paste them back here."

---

## Step 9: Re-Run Rejects

User pastes the regenerate command. Run it:

```bash
cd [FUNNEL_DIR] && python3 generate_ad_images.py --ids c03,c07,c12
```

Rebuild the review HTML with updated images. Open again. Repeat until approved.

---

## Step 10: Finalise

When approved, save `[FUNNEL_DIR]/artifacts/ad-concepts.json`:

```json
[
  {
    "id": "c01",
    "concept": "01 — [concept name]",
    "format_type": "[format]",
    "reason": 1,
    "swipe_file": "[filename]",
    "image_path": "/[FUNNEL_DIR]/generated_images/ad-concepts/c01.png",
    "status": "approved"
  }
]
```

Tell the user:
- Approved images: `[FUNNEL_DIR]/generated_images/ad-concepts/`
- Concept manifest: `[FUNNEL_DIR]/artifacts/ad-concepts.json`
