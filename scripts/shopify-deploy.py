#!/usr/bin/env python3
"""
Publish funnel pages to Shopify.

Usage:
  python3 shopify-deploy.py \
    --store yourstore.myshopify.com \
    --token shpat_xxx \
    --funnel-dir /path/to/funnel \
    --product-photo /path/to/photo.jpg \
    --presell-slug cotton-socks-guide \
    --offer-slug mat-vics-socks

What it does:
  1. Uploads presell images (r1-r5) and product photo to Shopify CDN
  2. Rewrites local image paths in HTML to CDN URLs
  3. Publishes presell and offer pages (creates or updates)
"""

import argparse
import base64
import json
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip3 install requests")
    sys.exit(1)


def load_env(funnel_dir):
    """Load SHOPIFY_STORE and SHOPIFY_TOKEN from .env in funnel_dir."""
    env = {}
    env_path = Path(funnel_dir) / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def api(method, store, token, path, **kwargs):
    url = f"https://{store}/admin/api/2026-01/{path}"
    headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}
    r = getattr(requests, method)(url, headers=headers, **kwargs)
    if r.status_code not in (200, 201):
        print(f"  ERROR {r.status_code}: {r.text[:300]}")
        return None
    return r.json()


def get_theme_id(store, token):
    data = api("get", store, token, "themes.json")
    if not data:
        return None
    for t in data["themes"]:
        if t["role"] == "main":
            return t["id"]
    return None


def upload_image(store, token, theme_id, local_path, asset_key):
    """Upload a local image to the Shopify theme CDN. Returns CDN URL or None."""
    with open(local_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    data = api("put", store, token, f"themes/{theme_id}/assets.json",
               json={"asset": {"key": asset_key, "attachment": encoded}})
    if data and "asset" in data:
        return data["asset"]["public_url"]
    return None


def get_page_id_by_handle(store, token, handle):
    """Return existing page ID if handle already exists, else None."""
    data = api("get", store, token, f"pages.json?handle={handle}&limit=1")
    if data and data.get("pages"):
        return data["pages"][0]["id"]
    return None


def publish_page(store, token, title, handle, body_html):
    """Create or update a Shopify page. Returns page URL."""
    existing_id = get_page_id_by_handle(store, token, handle)
    payload = {
        "page": {
            "title": title,
            "handle": handle,
            "body_html": body_html,
            "template_suffix": "no-header",
            "published": True,
        }
    }
    if existing_id:
        print(f"  Page '{handle}' exists — updating (id {existing_id})")
        payload["page"]["id"] = existing_id
        data = api("put", store, token, f"pages/{existing_id}.json", json=payload)
    else:
        print(f"  Page '{handle}' not found — creating")
        data = api("post", store, token, "pages.json", json=payload)

    if data and "page" in data:
        return f"https://{store}/pages/{handle}"
    return None


def main():
    parser = argparse.ArgumentParser(description="Deploy funnel pages to Shopify")
    parser.add_argument("--store")
    parser.add_argument("--token")
    parser.add_argument("--funnel-dir", required=True)
    parser.add_argument("--product-photo", required=True)
    parser.add_argument("--presell-slug", required=True)
    parser.add_argument("--offer-slug", required=True)
    args = parser.parse_args()

    funnel = Path(args.funnel_dir)

    # --- Load credentials: args override .env ---
    env = load_env(args.funnel_dir)
    store = args.store or env.get("SHOPIFY_STORE")
    token = args.token or env.get("SHOPIFY_TOKEN")

    if not store or not token:
        print("ERROR: Shopify credentials not found.")
        print("  Either pass --store and --token, or save them to .env:")
        print("    SHOPIFY_STORE=yourstore.myshopify.com")
        print("    SHOPIFY_TOKEN=shpat_xxxxxxxxxxxx")
        sys.exit(1)

    presell_html = funnel / "presell-v2.html"
    offer_html = funnel / "offer-v2.html"
    product_photo = Path(args.product_photo)

    # --- Validate inputs ---
    missing = []
    for p in [presell_html, offer_html, product_photo]:
        if not p.exists():
            missing.append(str(p))
    for i in range(1, 6):
        img = funnel / "generated_images" / f"r{i}.png"
        if not img.exists() or img.stat().st_size < 10_000:
            missing.append(str(img))
    if missing:
        print("ERROR: Missing required files:")
        for m in missing:
            print(f"  {m}")
        sys.exit(1)

    # --- Get theme ID ---
    print("Getting active theme ID...")
    theme_id = get_theme_id(store, token)
    if not theme_id:
        print("ERROR: Could not get theme ID. Check your store domain and token.")
        sys.exit(1)
    print(f"  Theme ID: {theme_id}")

    # --- Upload presell images ---
    print("\nUploading presell images to CDN...")
    image_url_map = {}
    for i in range(1, 6):
        local = funnel / "generated_images" / f"r{i}.png"
        asset_key = f"assets/funnel-r{i}.png"
        print(f"  Uploading r{i}.png...")
        url = upload_image(store, token, theme_id, local, asset_key)
        if not url:
            print(f"  ERROR: Failed to upload r{i}.png")
            sys.exit(1)
        image_url_map[f"generated_images/r{i}.png"] = url
        print(f"  OK: {url}")

    # --- Upload product photo ---
    print(f"\nUploading product photo ({product_photo.name})...")
    ext = product_photo.suffix.lower()
    asset_key = f"assets/funnel-product-photo{ext}"
    product_cdn_url = upload_image(store, token, theme_id, product_photo, asset_key)
    if not product_cdn_url:
        print("ERROR: Failed to upload product photo")
        sys.exit(1)
    print(f"  OK: {product_cdn_url}")

    # --- Rewrite presell HTML ---
    print("\nRewriting image paths in presell-v2.html...")
    presell_content = presell_html.read_text(encoding="utf-8")
    for local_path, cdn_url in image_url_map.items():
        presell_content = presell_content.replace(local_path, cdn_url)
    replaced = sum(1 for url in image_url_map.values() if url in presell_content)
    print(f"  {replaced}/5 image paths rewritten")

    # --- Rewrite offer HTML ---
    print("Rewriting image paths in offer-v2.html...")
    offer_content = offer_html.read_text(encoding="utf-8")
    # Replace product photo placeholder div with actual img tag
    placeholder_pattern = r'<div[^>]*>Add product photo here</div>'
    img_tag = (
        f'<img src="{product_cdn_url}" '
        f'alt="Product photo" '
        f'style="width:100%;border-radius:12px;">'
    )
    offer_content_new = re.sub(placeholder_pattern, img_tag, offer_content)
    if offer_content_new == offer_content:
        print("  Note: product photo placeholder not found — may already have an image tag")
    else:
        offer_content = offer_content_new
        print(f"  Product photo placeholder replaced with CDN URL")

    # --- Publish presell ---
    print(f"\nPublishing presell page as '{args.presell_slug}'...")
    presell_url = publish_page(
        store, token,
        title="Cotton Socks Guide",
        handle=args.presell_slug,
        body_html=presell_content,
    )
    if not presell_url:
        print("ERROR: Failed to publish presell page")
        sys.exit(1)
    print(f"  Live at: {presell_url}")

    # --- Publish offer ---
    print(f"\nPublishing offer page as '{args.offer_slug}'...")
    offer_url = publish_page(
        store, token,
        title="Mat & Vic's Socks",
        handle=args.offer_slug,
        body_html=offer_content,
    )
    if not offer_url:
        print("ERROR: Failed to publish offer page")
        sys.exit(1)
    print(f"  Live at: {offer_url}")

    # --- Done ---
    print("\n" + "=" * 50)
    print("PUBLISHED")
    print(f"  Presell:    {presell_url}")
    print(f"  Offer page: {offer_url}")
    print()
    print("Point your Meta ads at the presell URL.")
    print("=" * 50)


if __name__ == "__main__":
    main()
