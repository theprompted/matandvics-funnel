# Funnel Styling Reference

Complete CSS and layout spec for presell and offer page HTML. Apply this every time a funnel page is built or modified.

---

## Fonts

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap" rel="stylesheet">
```

Body font: `Assistant, sans-serif`

---

## Color Palette

| Variable | Value | Use |
|---|---|---|
| Primary (teal) | `#108474` | CTA buttons, callout borders, links, badges |
| Dark | `#121212` | Secondary CTA background, dark sections |
| Text | `#1a1a1a` | Body copy |
| Muted | `#666` | Kicker, meta text |
| Light bg | `#f9f9f7` | Page background |
| Card bg | `#ffffff` | Card surfaces |
| Border | `#e8e8e8` | Dividers, card borders |
| Placeholder | `#f5f5f5` | Image placeholder background |

---

## Global Reset + Base

```css
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Assistant', sans-serif;
  font-size: 18px;
  line-height: 1.7;
  color: #1a1a1a;
  background: #f9f9f7;
}

img { max-width: 100%; display: block; }
a { color: #108474; }
```

---

## Presell Page Layout

```css
.presell-wrapper {
  max-width: 760px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}
```

### Kicker
```css
.kicker {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #666;
  margin-bottom: 16px;
}
```

### H1
```css
h1 {
  font-size: clamp(28px, 5vw, 42px);
  font-weight: 700;
  line-height: 1.2;
  color: #1a1a1a;
  margin-bottom: 20px;
}
```

### Thesis line (italic)
```css
.thesis {
  font-size: 20px;
  font-style: italic;
  color: #444;
  border-left: 3px solid #108474;
  padding-left: 16px;
  margin-bottom: 32px;
}
```

### Body paragraphs
```css
p {
  margin-bottom: 1.2em;
}
```

### Reason H3 headlines
```css
h3 {
  font-size: 22px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 48px 0 16px;
}
```

### Teal callout box (definition box, things-to-check items)
```css
.callout {
  border-left: 4px solid #108474;
  background: #f0faf8;
  padding: 16px 20px;
  margin: 24px 0;
  border-radius: 0 8px 8px 0;
}

.callout p {
  margin: 0;
  font-size: 16px;
  color: #1a1a1a;
}
```

### Presell CTA button
```css
.cta-button {
  display: inline-block;
  background: #108474;
  color: #fff;
  text-decoration: none;
  font-size: 18px;
  font-weight: 700;
  padding: 18px 36px;
  border-radius: 8px;
  margin: 32px 0 12px;
}

.cta-button:hover {
  background: #0d6e61;
}

.cta-reassurance {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}
```

---

## Offer Page Layout

```css
.offer-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px 80px;
}

.narrow {
  max-width: 760px;
  margin: 0 auto;
}
```

### Hero section
```css
.hero {
  text-align: center;
  padding: 60px 20px 40px;
}

.hero h1 {
  font-size: clamp(26px, 4vw, 38px);
  font-weight: 700;
  max-width: 760px;
  margin: 0 auto 24px;
}

.star-rating {
  color: #f5a623;
  font-size: 22px;
  margin-bottom: 8px;
}

.review-count {
  font-size: 14px;
  color: #666;
  margin-bottom: 32px;
}
```

### Buy button (offer page)
```css
.buy-button {
  display: inline-block;
  background: #108474;
  color: #fff;
  text-decoration: none;
  font-size: 18px;
  font-weight: 700;
  padding: 18px 48px;
  border-radius: 8px;
}

.buy-button:hover {
  background: #0d6e61;
}
```

### Credibility bar
```css
.credibility-bar {
  display: flex;
  justify-content: center;
  gap: 32px;
  padding: 24px 20px;
  background: #fff;
  border-top: 1px solid #e8e8e8;
  border-bottom: 1px solid #e8e8e8;
  flex-wrap: wrap;
}

.credibility-item {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  text-align: center;
}
```

### Promo banner (mid-page, NOT top)
```css
.promo-banner {
  background: #108474;
  color: #fff;
  text-align: center;
  padding: 14px 20px;
  font-size: 15px;
  font-weight: 600;
}
```

### Testimonial grid
```css
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin: 32px 0;
}

.testimonial-card {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  padding: 24px;
}

.testimonial-quote {
  font-size: 16px;
  color: #333;
  margin-bottom: 16px;
  line-height: 1.6;
}

.testimonial-author {
  font-size: 14px;
  font-weight: 600;
  color: #666;
}

@media (max-width: 640px) {
  .testimonials-grid { grid-template-columns: 1fr; }
}
```

### Bundle cards
```css
.bundle-section {
  padding: 60px 20px;
}

.bundle-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  max-width: 960px;
  margin: 0 auto;
}

.bundle-card {
  background: #fff;
  border: 2px solid #e8e8e8;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  position: relative;
}

.bundle-card.popular {
  border-color: #108474;
}

.popular-badge {
  position: absolute;
  top: -14px;
  left: 50%;
  transform: translateX(-50%);
  background: #108474;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  padding: 4px 14px;
  border-radius: 20px;
  white-space: nowrap;
}

.bundle-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 8px;
}

.bundle-price {
  font-size: 28px;
  font-weight: 700;
  color: #108474;
  margin-bottom: 20px;
}

.bundle-cta {
  display: block;
  background: #108474;
  color: #fff;
  text-decoration: none;
  font-weight: 700;
  padding: 14px 20px;
  border-radius: 8px;
  font-size: 16px;
}

.bundle-card:not(.popular) .bundle-cta {
  background: #121212;
}

@media (max-width: 768px) {
  .bundle-grid { grid-template-columns: 1fr; }
}
```

### Second CTA section (dark background, bottom of offer page)
```css
.cta-section-dark {
  background: #121212;
  color: #fff;
  text-align: center;
  padding: 60px 20px;
}

.cta-section-dark h2 {
  font-size: clamp(24px, 4vw, 36px);
  font-weight: 700;
  margin-bottom: 24px;
}
```

### Back link to presell
```css
.back-link {
  display: inline-block;
  font-size: 14px;
  color: #666;
  text-decoration: none;
  padding: 12px 0;
}

.back-link:hover {
  color: #108474;
}
```

---

## Responsive Breakpoints

| Breakpoint | Behavior |
|---|---|
| `max-width: 768px` | Bundle grid stacks to 1 column |
| `max-width: 640px` | Testimonials stack to 1 column |
| `max-width: 480px` | Credibility bar stacks vertically |

Always include viewport meta:
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

---

## HTML Page Shell

Use this structure for both presell and offer pages:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>[Page title]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    /* paste all relevant CSS here — no external stylesheets */
  </style>
</head>
<body>
  <!-- page content -->
</body>
</html>
```

All CSS is inline in a `<style>` block. No external stylesheet files. No CDN CSS frameworks.
