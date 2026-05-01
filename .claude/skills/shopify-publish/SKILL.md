# /shopify-publish — Publish Funnel Pages to Shopify

Uploads images to Shopify CDN, rewrites image paths, and publishes both funnel pages as live Shopify pages. Handles the full deployment in one shot.

**Trigger:** type `/shopify-publish` in Claude Code

---

## What This Does

1. Asks four questions (store, token, funnel folder, product photo)
2. Runs `scripts/shopify-deploy.py` which:
   - Uploads all presell images (`r1.png`–`r5.png`) to Shopify CDN
   - Uploads the product photo to Shopify CDN
   - Rewrites all local image paths in the HTML to CDN URLs
   - Publishes `presell-v2.html` as a live Shopify page (no-header template)
   - Publishes `offer-v2.html` as a live Shopify page (no-header template)
3. Returns both live URLs

---

## Step 1 — Load Credentials and Ask for Remaining Inputs

**Read credentials from `.env`** in the funnel folder:
```bash
cat "[FUNNEL_DIR]/.env" 2>/dev/null || echo "not found"
```

If `.env` exists and contains `SHOPIFY_STORE` and `SHOPIFY_TOKEN`, set:
- `STORE` = value of `SHOPIFY_STORE`
- `TOKEN` = value of `SHOPIFY_TOKEN`

If `.env` is missing or incomplete, tell the user:
> "I couldn't find your Shopify credentials in `.env`. Please give me your store domain (e.g. `matandvics.myshopify.com`) and your API access token (starts with `shpat_`) and I'll save them for future use."

Save whatever they provide:
```
SHOPIFY_STORE=yourstore.myshopify.com
SHOPIFY_TOKEN=shpat_xxxxxxxxxxxx
```

Then ask for the remaining inputs:

> "Got your Shopify credentials. Three more things:
> 1. The path to your funnel folder (the folder containing `presell-v2.html` and `offer-v2.html`)
> 2. The path to your product photo (the image for the offer page hero)
> 3. What you'd like the page URL slugs to be, e.g. `cotton-socks-guide` and `mat-vics-socks`"

Wait for answers. Set:
- `FUNNEL_DIR` = path to funnel folder
- `PRODUCT_PHOTO` = path to product photo file
- `PRESELL_SLUG` = URL slug for presell page
- `OFFER_SLUG` = URL slug for offer page

---

## Step 2 — Check Prerequisites

Before running the deploy script:

**Check the no-header template exists:**
```bash
curl -s "https://[STORE]/admin/api/2026-01/themes.json" \
  -H "X-Shopify-Access-Token: [TOKEN]" | python3 -c "
import sys, json
themes = json.load(sys.stdin)['themes']
theme_id = next(t['id'] for t in themes if t['role'] == 'main')
print(theme_id)"
```

Then check for the template:
```bash
curl -s "https://[STORE]/admin/api/2026-01/themes/[THEME_ID]/assets.json?asset[key]=templates/page.no-header.liquid" \
  -H "X-Shopify-Access-Token: [TOKEN]"
```

If the response contains `"errors"` or is empty — the one-time setup hasn't been done. Tell the user:
> "The no-header template isn't installed on your store yet. Follow Step 2 of `methodology/going-live.md` first, then come back and run `/shopify-publish` again."

Stop here until the template exists.

**Check required files exist:**
- `[FUNNEL_DIR]/presell-v2.html` — must exist
- `[FUNNEL_DIR]/offer-v2.html` — must exist
- `[FUNNEL_DIR]/generated_images/r1.png` through `r5.png` — all must exist and be >10KB
- `[PRODUCT_PHOTO]` — must exist

If any are missing, tell the user specifically which file is missing and stop.

**Check Meta Pixel is configured:**
```bash
grep -c "YOUR_PIXEL_ID" "[FUNNEL_DIR]/presell-v2.html" "[FUNNEL_DIR]/offer-v2.html"
```

If either file still contains `YOUR_PIXEL_ID`, stop and tell the user:
> "Your funnel pages still have the placeholder pixel ID `YOUR_PIXEL_ID`. Before publishing, tell me your Meta Pixel ID and I'll swap it in. You can find it in Meta Business Suite → Events Manager — it's the 15–16 digit number under your pixel name."

Once they give you the ID (e.g. `1234567890123456`), replace all occurrences in both files:
```python
import re
from pathlib import Path
pixel_id = "USER_PROVIDED_ID"
for f in ["[FUNNEL_DIR]/presell-v2.html", "[FUNNEL_DIR]/offer-v2.html"]:
    p = Path(f)
    p.write_text(p.read_text().replace("YOUR_PIXEL_ID", pixel_id))
print("Pixel ID updated in both pages.")
```

Then continue with deployment.

---

## Step 3 — Run the Deploy Script

Credentials are read from `.env` automatically. Run:

```bash
python3 [FUNNEL_DIR]/scripts/shopify-deploy.py \
  --funnel-dir "[FUNNEL_DIR]" \
  --product-photo "[PRODUCT_PHOTO]" \
  --presell-slug "[PRESELL_SLUG]" \
  --offer-slug "[OFFER_SLUG]"
```

The script (see `scripts/shopify-deploy.py`) handles everything. Watch its output — it prints progress at each step.

---

## Step 4 — Verify and Report

After the script completes, open both pages and confirm:

```bash
curl -s -o /dev/null -w "%{http_code}" "https://[STORE]/pages/[PRESELL_SLUG]"
curl -s -o /dev/null -w "%{http_code}" "https://[STORE]/pages/[OFFER_SLUG]"
```

Both should return `200`.

Tell the user:
- Presell live at: `https://[STORE]/pages/[PRESELL_SLUG]`
- Offer page live at: `https://[STORE]/pages/[OFFER_SLUG]`
- Point your Meta ads at the presell URL

---

## Updating Pages After They're Live

To push an update to a page that's already live, run `/shopify-publish` again. The deploy script checks if each page already exists (by slug) and uses PUT instead of POST — it updates in place rather than creating a duplicate.
