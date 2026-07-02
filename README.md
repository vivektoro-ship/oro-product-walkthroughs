# Oro Walkthrough Decks — Handoff (for Vivek)

Everything needed to view, edit, and rebuild the interactive walkthrough decks.

Each deck is **one self-contained `.html` file** — fonts and all screenshots are base64-embedded,
so it opens offline (double-click) and deploys as a static file (Netlify).

---

## 1. What's in this folder

```
walkthrough-handoff/
├── README.md                         ← you are here
├── oro-offer-walkthrough.html        ← the 6 final decks (edit these / rebuilt here)
├── oro-beagle-cx-walkthrough.html
├── oro-takeover-cx-walkthrough.html
├── oro-elr-cx-walkthrough.html
├── oro-universal-takeover-walkthrough.html
├── oro-beagle-universal-walkthrough.html
├── assets/                           ← source screenshots (PNG), one subfolder per section
│   ├── flows/ px/ ringmaster/ admin/ offer-current/   (offer deck)
│   ├── beagle/ beagle-px/ beagle-admin/ beagle-queues/ (beagle deck)
│   ├── takeover/ takeover-px/ takeover-admin/ takeover-loans/ (takeover deck)
│   └── elr/ elr-px/                                   (elr deck)
├── scratchpad/                       ← the build toolkit
│   ├── build_*.py                    ← one script per deck/section (see §5)
│   ├── template_*.html               ← HTML shells (skin + controller)
│   └── fonts.css                     ← the 4 embedded webfonts (base64)
└── docs/                             ← original spec + design template
```

---

## 2. Two ways to make changes

### A) Quick copy tweaks — edit the HTML directly (works for EVERY deck)
Every deck's content lives in **one JavaScript array** near the bottom of the file:

```js
const DECK = [ { platform, kicker, viewport, flows:[ { name, slug, kicker, blurb,
                 steps:[ { img, title, caption }, … ] } ] } ];
```

To change wording: open the `.html`, search for the caption/title text, edit it, save. Done.
Everything on screen (index cards, step dots, "Screen N of M", progress bar) is derived from this
array — nothing else to touch.

> The `img` values are long `data:image/png;base64,…` strings. Leave those alone when editing copy.

### B) Structural changes — edit the build script and rebuild (recommended)
To add / remove / reorder screens, or swap images, edit the matching `build_*.py` (they hold the
copy and the screen order in plain Python), then run it. See §4–§5.

---

## 3. The data model

- **Platform** = a group shown as a labelled section on the landing page (e.g. "Customer App").
  - `viewport: "mobile"` → renders in the **phone frame** (375-wide screens).
  - `viewport: "desktop"` → renders in the **browser-window frame**, shown large (admin screens).
- **Flow** = one card on the landing page → a step-through (Back/Next, numbered dots, progress).
- **Step** = one screen: `{ img, title, caption }`.
- **Deep links**: the URL hash is `#<flow-slug>` or `#<flow-slug>/<step>` (e.g. `#px-takeover/3`).
  Slugs must stay unique within a deck; the browser Back button works off the hash.

**Universal decks only** (`oro-universal-takeover…`, `oro-beagle-universal…`): each *step* also
carries `actor` ("Customer"/"Partner"/"Admin") and its own `viewport`, so the frame switches
phone⇄browser per screen and an actor badge shows who's acting. The controller reads per-step
`viewport` first, falling back to the flow's.

---

## 4. Rebuilding (Python 3, macOS)

Run any script from this folder. Paths are relative to the script, so no editing needed:

```bash
cd walkthrough-handoff
python3 scratchpad/build_beagle.py          # example
```

Each script: reads PNGs from `assets/…`, base64-embeds them, injects the `DECK` + `fonts.css`
into its `template_*.html`, and writes the `.html` to this folder. It prints the size + a
per-flow screen count.

**Dependencies:** Python 3 (standard library only). `pngquant` is only needed if you re-pull
new screenshots and want to compress them (`brew install pngquant`); rebuilding from the existing
PNGs needs nothing extra.

---

## 5. Which script builds what  (⚠️ append-scripts read the existing HTML — run in order)

| Deck | Scripts, in order |
|---|---|
| **Beagle** (gold loan) | `build_beagle.py` → `build_beagle_px.py` → `build_beagle_admin.py` → `build_beagle_queues.py` |
| **Takeover** (BRL) | `build_takeover.py` → `build_takeover_px.py` → `build_takeover_admin.py` → `build_takeover_loans.py` |
| **ELR** | `build_elr.py` → `build_elr_px.py` |
| **Universal – takeover** | `build_universal.py` *(reads the takeover + elr + beagle decks)* |
| **Universal – beagle** | `build_beagle_universal.py` *(reads the beagle deck)* |
| **Offer – "What Changes"** | `build_offer_whatchanges.py` *(appends the current-state section to the offer deck)* |

- `build_<deck>.py` **creates** the deck (first group). The others **append** a group and are
  **idempotent** — safe to re-run; each replaces its own group rather than duplicating.
- Because the append-scripts read the current `.html`, keep the deck files in place.
- **Offer deck** (`oro-offer-walkthrough.html`): its main groups were assembled earlier; today the
  only script for it is `build_offer_whatchanges.py` (the "What Changes" current-state section).
  For other offer edits, use method **A** (edit the DECK directly) — its screenshots are in
  `assets/flows` (customer), `assets/px` (partner), `assets/admin` (loan-ops),
  `assets/ringmaster`, and `assets/offer-current` (What Changes).

---

## 6. Re-pulling screenshots from Figma (only if the designs changed)

The scripts embed PNGs already sitting in `assets/`. To refresh a screen from Figma:
1. In the Figma MCP / Desktop, `get_screenshot` the frame (mobile `maxDimension ~760`,
   desktop `~2048`), download the PNG.
2. `pngquant --quality=65-90 <file>` to compress.
3. Replace the PNG in the right `assets/<section>/` folder (keep the filename), then rerun the
   deck's build script.

**Note on the "What Changes" screens** (`assets/offer-current/sel/`): these were padded with a
white top/bottom margin so the phone-frame's rounded corner doesn't clip the title (the source
frames sit flush to the edge). If you replace one, re-pad it (≈90px top / 55px bottom, fill
`#F8F8F8`) — a Pillow one-liner, ask if needed — then rerun `build_offer_whatchanges.py`.

---

## 7. Sanity checks after any rebuild

Open the file in a browser (index renders, each flow steps through, deep links + Back work), and:

```bash
F=oro-beagle-cx-walkthrough.html
grep -o 'data:image/png;base64' $F | wc -l   # == total screens
grep -o '"caption":' $F | wc -l               # == same number
grep -oE 'https?://[^" )]+' $F | grep -v data: | wc -l   # must be 0 (fully self-contained)
```

`data:image/png` count == `"caption"` count == total screens, and **zero** external URLs.

---

## 8. Good to know

- **Self-contained:** no external fonts/images/scripts — works offline and on any static host.
- **Netlify:** drop this folder (or just the `.html` files) in; each file is its own page. Hash
  deep-links need no redirect rules. (Sizes: offer ≈9.6 MB, takeover ≈9.4 MB — fine for Netlify.)
- **Skin:** dark warm-paper + gold, four embedded fonts (Fraunces / Source Serif 4 / Bodoni Moda /
  JetBrains Mono). Tokens are the `:root{…}` block at the top of each file's `<style>`.
- **Voice:** customer flows speak to the customer ("you"); partner/admin flows are written for
  those operators. Keep customer copy jargon-free.
- `docs/CUSTOMER-APP-DECK-TEMPLATE.md` — the original design/build spec.
  `docs/oro-offer-walkthrough-SPEC.md` — product spec for the offer deck.
