# Going Live — Publishing Your Funnel Pages to Shopify

Your funnel is two HTML files: `presell-v2.html` (the education page) and `offer-v2.html` (the product page). This guide explains how to get them live on your Shopify store.

**Most of this is automated.** Once you complete the one-time setup below, Claude handles the actual publishing via API. You don't upload files manually or touch a terminal.

---

## Before You Publish

**1. Replace placeholder testimonials.**
Search both files for `<!-- PLACEHOLDER: replace with real customer quote -->`. Replace every instance with a real customer quote before going live. Pull from your email inbox, product reviews, or DMs.

**2. Confirm your buy button URL.**
Open `offer-v2.html` and search for your product URL. Click it in a browser and confirm it goes directly to checkout.

---

## One-Time Setup

Do this once. You never need to repeat it.

### Step 1 — Create a Custom App in Shopify

1. Go to **Shopify Admin → Settings → Apps and sales channels**
2. Click **Develop apps** (top right) — if prompted, enable custom app development
3. Click **Create an app** → name it anything (e.g. "Funnel Deploy")
4. Under **Configuration**, click **Admin API integration**
5. Enable these two scopes: `write_content`, `write_themes`
6. Click **Save** → go to **API credentials** → click **Install app**
7. Copy the **Admin API access token** — you'll only see it once, save it somewhere safe

You now have:
- Your store domain: `yourstore.myshopify.com`
- Your access token: `shpat_xxxxxxxxxxxx`

### Step 2 — Create the Headerless Template

This is a one-time API call that installs a 14-line template file in your theme. It tells Shopify to display any page assigned to it without the store's header, footer, or navigation.

Give Claude your store domain and access token and ask it to run this:

```bash
curl -s -X PUT "https://YOUR_STORE.myshopify.com/admin/api/2026-01/themes/$(curl -s 'https://YOUR_STORE.myshopify.com/admin/api/2026-01/themes.json' -H 'X-Shopify-Access-Token: YOUR_TOKEN' | python3 -c "import sys,json;print(next(t['id'] for t in json.load(sys.stdin)['themes'] if t['role']=='main'))")/assets.json" \
  -H "X-Shopify-Access-Token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "asset": {
      "key": "templates/page.no-header.liquid",
      "value": "{% layout none %}\n<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>{{ page.title }}</title>\n</head>\n<body style=\"margin:0;padding:0\">\n{{ page.content }}\n</body>\n</html>"
    }
  }'
```

Once this runs successfully, the template is installed. Done — you never touch it again.

---

## Publishing the Pages

With the one-time setup complete, tell Claude:

> "Publish my funnel pages to Shopify. My store is `yourstore.myshopify.com`, my token is `shpat_xxx`, and the funnel files are at `[path to your funnel folder]`."

Claude will:
1. Upload all images to your Shopify CDN and get back permanent URLs
2. Replace all local image paths in the HTML with those CDN URLs
3. Read `presell-v2.html` and `offer-v2.html` and publish both via API, using the `no-header` template
4. Return the live URLs: `yourstore.com/pages/cotton-socks-guide` and `yourstore.com/pages/mat-vics-socks`

No file uploads, no terminal commands, no copy-pasting HTML.

### About images

There are two types of images in your funnel:

**1. The 5 AI-generated presell images** — generated during the funnel build and saved to `generated_images/r1.png` through `r5.png`. Claude uploads these to your Shopify CDN automatically as part of publishing.

**2. Your product photo** — you need to provide this before publishing. It goes on the offer page hero. Have the image file ready on your computer and tell Claude its path when you ask it to publish.

The one-time setup needs one additional scope to enable image uploads: add `write_files` when creating your custom app (Step 1 above — enable `write_content`, `write_themes`, and `write_files`).

---

## After Going Live

**Test the full flow in an incognito window:**
1. Open your presell URL — confirm no product name or price appears anywhere
2. Confirm the layout looks correct — CSS should be fully applied
3. Click the CTA button — confirm it loads the offer page
4. On the offer page: click a buy button — confirm it goes to checkout
5. On the offer page: click "Back to the guide" — confirm it returns to the presell

**Update your ad links:**
Your Meta ads should link to the presell URL. That is the landing page for cold traffic.

---

## Updating Pages Later

Tell Claude what to change and ask it to update the live page via API. It will edit the content and push the update in the same session — no manual steps.

---

## Troubleshooting

**Page shows the store header/footer:**
The `no-header` template wasn't applied. Ask Claude to update the page's `template_suffix` to `no-header` via API.

**Page returns 404:**
The page was created but not published. Ask Claude to set `published: true` on the page via API.

**Scope error when running the API call:**
The app doesn't have the right scopes. Go back to the app in Shopify Admin, add `write_content` and `write_themes`, save, then uninstall and reinstall the app from the Dev Dashboard — scope changes only apply after reinstall.
