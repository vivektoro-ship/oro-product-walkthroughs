# Onboarding Deck — Reusable Template Spec

A handoff for building **interactive, self-contained "screen-by-screen" onboarding decks** from
Figma frames. Built first for the **Oro Customer App — Takeover Offer Creation** flow. Everything
below is generic enough to re-skin for any app flow; the Oro specifics are called out as examples.

> **Goal of the template:** point it at a list of Figma node IDs + one line of copy per screen, and
> it produces a single `.html` file (and optionally a hosted link) that walks a viewer through the
> flow one screen at a time inside a phone frame.

---

## 1. What this deliverable is

- **One self-contained `.html` file.** No external dependencies — fonts and screenshots are all
  base64-embedded. It must open offline and be shareable as a single file (Figma asset URLs expire,
  so never hot-link them).
- **Audience / voice:** written **to the customer in second person ("you / your")** — it's the
  customer's own journey through the app, *not* a field agent instructing a customer, and *not* an
  engineering spec. No jargon (no "OCR", "LTV", "tenure", "paginated", "extract", "happy path").
- **Interactive:** one screen at a time in a phone frame, one-line plain-language explainer beneath,
  Back/Next + clickable numbered step dots + "Step N of 8", progress bar, keyboard arrows, and
  swipe on touch devices.

---

## 2. Source of truth (Figma)

- **File:** `https://www.figma.com/design/zarJnV0HTbJIVL7JLshfIw/offers-user-app`
- **File key:** `zarJnV0HTbJIVL7JLshfIw`
- **Page:** "Ready for Engineering"
- Pull frames via the **Figma MCP**: `get_metadata` to confirm a node (check it's a **375-wide**
  mobile frame and the name matches), then `get_screenshot` (PNG, `maxDimension: 1600`).
- `get_screenshot` returns a short-lived URL — `curl` it down to `./assets/`, then base64-embed.
  Do **not** keep the Figma URL in the HTML.

### Canonical flow spine (happy path only — skip error / edit / delete / variant frames)

| # | Node ID  | Frame name                              | Screen |
|---|----------|-----------------------------------------|--------|
| 1 | 15-5609  | offer/home/home-screen--default         | Home   |
| 2 | 1-25097  | offer/choose-offer-type--default        | Choose type |
| 3 | 1-25378  | offer/pledgecard-upload--default        | Upload card |
| 4 | 1-27235  | offer/pledgecard-upload--fetching       | Reading card |
| 5 | 1-27283  | offer/pledgecard-upload--fetched        | Review details |
| 6 | 1-25864  | offer/pledgecard-upload--confirmation   | Add / continue |
| 7 | 1-27259  | offer/plans--loading                    | Preparing offers |
| 8 | 1-21271  | takeover/plans--created                 | Plans list |

If a node ID drifts, fall back to matching by frame **name**.

---

## 3. Design system (the "skin")

Direction: **dark warm editorial**, derived from the c-meal aesthetic (https://c-meal.netlify.app/)
— inverted to dark per the client's request. Serif-forward, paper/print feel, gold accent.

### Color tokens (CSS variables)
```
--paper:#15110B;      /* page background, warm near-black           */
--paper-deep:#1E1A13; /* phone bezel / surfaces                     */
--rule:#383026;       /* hairline rules / borders                   */
--rule-soft:#2A241B;  /* fainter rules                              */
--ink:#F4ECDD;        /* primary text, warm off-white               */
--ink-soft:#C9BEA6;   /* body captions                              */
--ink-faded:#8C8069;  /* labels / metadata                          */
--gold:#E0A93D;       /* accent: headings em, progress, active, CTA */
--gold-soft:#C99A3A;
--warning:#D2683F;
```
> The original c-meal **light** palette (if a light variant is ever wanted): paper `#F5EFE3`,
> paper-deep `#EFE7D6`, rule `#D4C9B3`, ink `#1A1612`, ink-soft `#3A322A`, ink-faded `#6B5F50`,
> gold `#9C7322`. (Dark mode is just these flipped + the gold brightened for contrast.)

### Type roles (the four faces — keep these)
| Role | Family | Used for |
|------|--------|----------|
| Display | **Fraunces** (600, +italic) | masthead `<h1>`, step `<h2>` (italic gold accent word) |
| Body | **Source Serif 4** (400/600) | captions, dek |
| Didone numerals | **Bodoni Moda** (700) | the big figure number ("01") |
| Mono/labels | **JetBrains Mono** (600) | tracked uppercase kickers, buttons, step dots, progress meta |

- Fonts are **base64 @font-face data URIs**, latin subset only, weights actually used. The CSP on
  hosted Artifacts blocks font CDNs, and the file must be offline-capable — so **never** `<link>` to
  Google Fonts. Inline them.
- Letter-spacing: tight on display (`-0.02em`), wide on mono labels (`0.18–0.24em`, uppercase).

---

## 4. Architecture — DATA-DRIVEN (the core idea)

The whole UI renders from **one JS array**. Adding/removing/reordering a screen = editing one entry.

```js
const STEPS = [
  { img: "data:image/png;base64,…", title: "Start on the home screen",
    caption: "Open the Oro app and tap “Get Oro Offer”…" },
  // …one object per screen
];
```

A small controller reads `STEPS` and wires everything:
- renders the current `img` into the phone frame (with a fade on change),
- sets `title`, `caption`, "Step N of total", the big figure number, progress-bar width,
- builds the numbered step-dot row, and the active/done states,
- navigation: Back/Next buttons (disabled at ends), clickable dots, `ArrowLeft`/`ArrowRight`,
  and **touch swipe** (horizontal delta > 50px, and more horizontal than vertical).

Nothing about the count is hardcoded — `total = STEPS.length` drives labels, dots, and progress.

---

## 5. Copy rules (important — this is where it adds value)

- **Voice:** the app speaking to the customer. "We read your card for you", "See your plans",
  "Take your time and compare." Use "you / your", never "the customer / they".
- **Plain words a first-time reader gets instantly.** Keep domain terms people know
  (pledge card, lender, gold weight, interest rate, loan amount); translate everything internal:
  - OCR / "AI extraction" → "the app reads your card automatically and fills in the details"
  - LTV / "indicative amount" → "loan amount" / "biggest loan"
  - tenure → "how long it runs"
  - Offer ID → "an offer number so you can track it"
  - "mandatory review" → "this step can't be skipped"
- One short sentence or two per screen. Friendly, active, concrete.

Current 8-step copy is in `customer-app-offer-creation.html` (the `STEPS` array) — reuse as the
reference tone.

---

## 6. Mobile / accessibility

- `<meta viewport … viewport-fit=cover>`, `theme-color` = `--paper`, iOS web-app meta tags.
- Under 760px: single centered column; phone scales to screen (`88vw` on very small);
  **Back/Next become a fixed bottom bar** with `env(safe-area-inset-bottom)` padding (thumb reach,
  clears the iPhone home indicator).
- `overflow-x:hidden` on body; images `width:100%`; text stays zoomable (`-webkit-text-size-adjust:100%`).
- Swipe to navigate; keyboard arrows; visible focus; respect `prefers-reduced-motion` for the fade.
- **Distribution on mobile:** publish via the **Artifact** tool → private claude.ai URL, openable on
  any device, "Add to Home Screen" for full-screen. Redeploys to the **same URL** on edit.

---

## 7. Build pipeline (how to regenerate)

1. **Confirm + export** each node: `get_metadata` (verify 375-wide + name) → `get_screenshot`
   (`maxDimension:1600`, PNG) → `curl` to `./assets/<n>-<slug>.png`.
2. **Embed fonts:** fetch the Google Fonts `css2` URL with a desktop User-Agent, keep only the
   **latin** `@font-face` block per weight (the one whose `unicode-range` starts `U+0000-00FF`),
   download each woff2, base64 into a `@font-face { src:url(data:font/woff2;base64,…) }` fragment.
3. **Assemble** with a small Python build script: read PNGs → base64 → build the `STEPS` JSON, inline
   the fonts CSS + token CSS + controller JS into one HTML template, write
   `customer-app-offer-creation.html`. (Build script lives in the scratchpad as `build2.py`; the font
   embed step as `fonts/embed_fonts.py`.)
4. **Verify:** counts (`@font-face` == 4–6, `data:image/png` == #steps, `"title":` == #steps),
   `grep` for 0 external `https?://` refs, 0 leftover template placeholders, and no jargon words in
   the visible copy. Open in a browser.
5. **Host (optional):** strip `<!DOCTYPE>/<html>/<head>/<body>` to a body-only file (keep `<title>`,
   `<style>`, content, `<script>`) and publish with the Artifact tool.

---

## 8. Known fragile spots ("it breaks and keeps breaking" — harden these)

These are the likely culprits and how to make them robust when templatizing:

1. **File size (~1.35 MB).** Source Serif 4 latin subset is heavy (~240 KB across two weights), and
   8 PNGs add ~600 KB. Symptoms: slow load on mobile data, occasional host/preview choke.
   *Fixes:* drop unused font weights; consider one body weight only; compress/resize PNGs
   (the screens are displayed ≤360px wide — they don't need 1600px source); or `pngquant` them.
2. **Base64 inside a Python/JS template string.** A stray unescaped quote or an f-string brace in the
   embedded data can corrupt the file. *Fix:* build `STEPS` with `json.dumps`, inject via a single
   `.replace("__STEPS__", json)` (not f-strings around the blob); same for the fonts CSS.
3. **Artifact = body-only.** The hosting tool wraps your content in its own `<head>`. Publishing a
   full `<!DOCTYPE>…</html>` document can render wrong. *Fix:* publish the stripped body-only variant
   (step 7.5). Keep the full document as the downloadable file.
4. **Fixed bottom nav overlap.** The mobile fixed control bar can cover the footer/last dots if body
   padding-bottom is too small. *Fix:* keep `padding-bottom: calc(96px + env(safe-area-inset-bottom))`.
5. **Smart quotes / em-dashes in copy** get `\uXXXX`-escaped by `json.dumps` — fine in output, but
   don't grep for them as plain ASCII when verifying.
6. **Figma asset URLs expire.** Re-export if a rebuild is days later; never rely on a saved URL.

---

## 9. To turn this into a template

Parameterize:
- `STEPS_SOURCE`: list of `{ nodeId, slug, title, caption }` (copy authored in the §5 voice).
- `figmaFileKey`, `page`.
- `theme`: the §3 token block (ship dark + light presets).
- `fonts`: the four-role map (display/body/didone/mono) → Google Fonts families + weights to embed.
- `header`: masthead kicker, `<h1>` (with the italic accent word), dek, footer line.

Everything else (controller JS, layout CSS, build/verify steps) stays fixed. A new deck =
new screenshots + new `STEPS` copy + optional re-skin.

---

## 10. Current artifacts in this workspace

- `customer-app-offer-creation.html` — the finished dark, mobile-ready, customer-voice deck (8 steps).
- `assets/` — the 8 source PNGs + `build.py`.
- Hosted (private) Artifact: `https://claude.ai/code/artifact/bf7a5272-0e65-4adc-b30c-6c1017f00882`
- Scratchpad build scripts: `build2.py`, `fonts/embed_fonts.py`, `fonts/fonts_embedded.css`.
