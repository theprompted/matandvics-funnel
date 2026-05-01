# Mat & Vic's — Funnel Package

Everything needed to build, generate images for, and publish your DTC advertorial funnel.

---

## Setup (one time)

**1. Install Claude Code:**
→ [claude.ai/code](https://claude.ai/code)

**2. Open this folder in Claude Code.**
Open the `matandvics-funnel` folder as your project. All skills are pre-installed.

**3. Install dependencies:**
```bash
pip3 install requests fal-client
```

**4. Set your FAL API key** (only needed for image generation):
```bash
export FAL_KEY=your_key_here
```
Get your key at [fal.ai/dashboard](https://fal.ai/dashboard).

---

## Skills

Type any of these in Claude Code to run them:

### `/dtc-funnel-generate`
Builds a complete advertorial funnel from scratch — research, copy, review, HTML.
Produces `presell-v2.html` and `offer-v2.html` ready to publish.

### `/dtc-ad-generate`
Generates 50 ad image concepts for the funnel using fal.ai.
Builds a review grid, lets you mark Keep / Regenerate, re-runs rejects.

### `/shopify-publish`
Publishes the funnel to your Shopify store.
Uploads images to CDN, rewrites paths, creates live pages — no manual steps.

---

## Typical Workflow

1. `/dtc-funnel-generate` — build the funnel
2. `/dtc-ad-generate` — generate ad images  
3. Replace placeholder testimonials in both HTML files with real customer quotes
4. Have your product photo ready
5. `/shopify-publish` — go live

---

## What's in This Folder

```
matandvics-funnel/
├── .claude/
│   └── skills/
│       ├── dtc-funnel-generate/   — funnel build skill
│       ├── dtc-ad-generate/       — ad image generation skill
│       └── shopify-publish/       — Shopify deployment skill
├── funnel/
│   ├── artifacts/                 — research, copy drafts, QA reports
│   ├── generated_images/          — funnel + ad images
│   ├── generate_ad_images.py      — ad image generation script
│   ├── presell-v2.html            — education page (built by skill)
│   └── offer-v2.html              — offer page (built by skill)
├── scripts/
│   └── shopify-deploy.py          — deployment script (called by /shopify-publish)
├── methodology/
│   ├── funnel-styling.md          — CSS spec for both pages
│   ├── reviewer-persona.md        — copy review standards
│   └── going-live.md              — Shopify setup guide
└── swipe-file/
    ├── ad-formats.json            — ad concept reference library
    └── images/                    — swipe reference thumbnails
```

---

## Going Live on Shopify

Before running `/shopify-publish` you need a one-time Shopify setup.
See `methodology/going-live.md` for the full guide — it takes about 10 minutes.
