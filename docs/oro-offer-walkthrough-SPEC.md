# Oro Offer — Multi-Platform Walkthrough Deck

**Product spec for review**
Author: Pragadeesh · Reviewer: **Sreekesh** · Status: Draft for review · Last updated: 2026-06-26

---

## 1. Summary

A single, self-contained HTML file that walks a viewer, screen by screen, through **every Oro Offer flow across all four surfaces** — Customer App, Partner App, Admin (Loan Ops), and Ringmaster (Calling Team). It is an onboarding / stakeholder-walkthrough artifact, not production UI: each flow plays back real Figma screenshots inside a device frame with a one-line plain-language explainer, Back/Next, numbered steps, progress bar, keyboard arrows, swipe, and deep-linkable URLs.

One file. No dependencies. Opens offline. Fonts and all ~123 screenshots are base64-embedded.

**Deliverable:** `/Users/pragadeesh-oro/oro-offer-walkthrough.html` (9.49 MB)

---

## 2. Goals / non-goals

**Goals**
- Give anyone (PM, design, ops, leadership, new joiners) a guided tour of every offer surface without Figma access or a running app.
- Keep all four surfaces in one place so the same offer journey can be compared across Customer / Partner / Admin / Ringmaster.
- Stay faithful to the live Figma designs (real screenshots, real labels, correct sequence).
- Be shareable as a single file that works offline and on mobile.

**Non-goals**
- Not production code or a component library.
- Not a clickable prototype of the apps themselves — it's a narrated screenshot walkthrough.
- Not a spec of the offer feature's business logic (that lives in the iPRDs — ENG-2186, ENG-2456, ENG-2732, etc.).

---

## 3. What's in it (content)

4 platform groups · 25 flows · 123 screens.

| Platform | Viewport | Flows | Screens |
|---|---|--:|--:|
| Customer App | mobile (phone frame) | 8 | 37 |
| Partner App | mobile (phone frame) | 6 | 39 |
| Admin · Loan Ops | desktop (browser frame) | 3 | 9 |
| Ringmaster · Calling Team | desktop (browser frame) | 8 | 38 |

**Customer App** (`cx-*`): Shift existing loan (takeover) · Get a new loan (fresh) · Change your offer · Share · Book a visit · Track a visit · Profile/offers/visits · Error states.

**Partner App** (`px-*`): Create takeover offer · Import an existing offer · Modify · Share · Create fresh offer · Edit fresh offer.

**Admin · Loan Ops** (`admin-*`): Review a takeover offer · Review a fresh offer · Legacy offers.

**Ringmaster · Calling Team** (`ringmaster-*`): Find an offer · Create takeover on a call (13) · Create fresh on a call · Add pledge cards · Import pledge cards · Edit takeover options · Edit fresh options · Change fresh value.

---

## 4. Voice & copy rules

Each screen has a one-line caption. Voice is **surface-specific** and deliberate:

- **Customer App** — the app speaking to the customer in second person ("you / your"). Plain words only; **no jargon** (no OCR / LTV / tenure / extract / indicative / mandatory). Domain terms a customer knows are fine (pledge card, gold weight, interest rate).
- **Partner App** — the app speaking to the partner who is acting *for* the customer ("Enter the customer's mobile number…"). Same jargon ban as Customer.
- **Admin · Loan Ops** — third person about Loan Ops ("Loan Ops opens the Offers list…"). Internal terms are allowed and clearer (pledge card, plan, LTV, offer ID, activity log). Offers are non-binding, so copy never implies Loan Ops *approves* anything — only locate / review / share / manage.
- **Ringmaster · Calling Team** — third person about the calling agent ("The agent enters the customer's mobile number…"). Internal terms allowed. No "you", no approval language.

The jargon ban is **enforced only on Customer + Partner copy**; Admin and Ringmaster may use internal vocabulary.

---

## 5. Architecture

### 5.1 Data-driven: one `DECK` array drives everything

```js
const DECK = [
  { platform: "Customer App",            viewport: "mobile",  flows: [ … ] },
  { platform: "Partner App",             viewport: "mobile",  flows: [ … ] },
  { platform: "Admin · Loan Ops",        viewport: "desktop", flows: [ … ] },
  { platform: "Ringmaster · Calling Team", viewport: "desktop", flows: [ … ] },
];
// flow:  { name, slug, kicker, blurb, steps: [ { img, title, caption }, … ] }
```

Three levels: **Platform → Flow → Step.** The index, group headers, flow cards, step dots, "Screen N of M", and progress bar are all derived from `DECK` — nothing is hardcoded. Adding a screen, flow, or whole platform = editing data, not markup.

### 5.2 Two render paths (per-platform `viewport`)

- **`viewport: "mobile"`** → the original **phone frame** (375-wide, rounded bezel, notch). Used by Customer and Partner.
- **`viewport: "desktop"`** → a **browser-window frame** (traffic-light dots + address bar) shown **large**: the frame breaks out of the reading column to `min(96vw, 1440px)`, centered on the viewport (full-bleed technique), with the screenshot at full width — effectively near 1:1 so console text is readable. Used by Admin and Ringmaster. Source screenshots are exported at high res (~2048 / native 1440–1920px) to stay sharp at this size.

The controller branches on the active flow's viewport (propagated from its platform group) to pick the frame. Desktop screens get **tap/click-to-zoom**: a full-screen overlay (up to 1920px, scroll + pinch) for reading dense tables, plus the wide frame stays horizontally scrollable on small screens.

### 5.3 Navigation & deep-linking

- Landing = an **index** with one labelled section per platform; each section is a grid of flow cards (number, name, blurb, screen count).
- Click a flow → the step-through view scoped to that flow (frame + one-line explainer + Back/Next + numbered dots + progress bar). "← All flows" returns to the index.
- **The URL hash is the single source of truth.** Slugs are prefixed per platform (`cx-`, `px-`, `admin-`, `ringmaster-`). `#ringmaster-takeover/2` is shareable and deep-links to screen 2 of that flow; the browser **Back button works** because every step/flow change is a hash change.
- Keyboard arrows, touch swipe (mobile), and Esc-to-close-zoom (desktop) are wired.

### 5.4 Skin

Dark warm-editorial ("c-meal inverted") palette; four font roles embedded as latin-only base64 `@font-face` (Fraunces display, Source Serif 4 body, Bodoni Moda numerals, JetBrains Mono labels — one weight each). Tokens, progress hairline, dots, and captions are shared across both render paths.

---

## 6. Build pipeline (how it's regenerated)

1. **Discover live in Figma** via the Figma MCP: `get_metadata` on the "Ready for engineering" canvas → enumerate every frame → keep only true screens (mobile = 375-wide; desktop = ≥1200-wide), drop component cards / popovers / variant dupes (`--v2…v5`, `--delete`, `--dropdown`, option sheets, repeated loading/error states). **Resolve frames by NAME, not ID** (IDs drift between design revisions).
2. **Match flows by section path** (`<surface>/offer/<flow>/<screen>--state`), pick the canonical happy-path frame per family.
3. **Read the iPRD** for sequence + correct labels (ENG-2186 Partner, ENG-2456 Admin, ENG-2732 Ringmaster).
4. **Export** each kept node with `get_screenshot` — mobile at `maxDimension ~760`, desktop at `~2048` — `curl` the short-lived URL to `assets/`, then **`pngquant`** every PNG (flat UI compresses well) and base64-embed. **No hot-linked Figma URLs** (they expire).
5. **Assemble** with a small Python build script per group: it reads the existing HTML's `DECK` (so prior groups' embedded images are reused **byte-for-byte, never re-pulled**), appends the new group, and injects `DECK` + fonts into the HTML template via string replace.

Each platform was added as an incremental layer (Customer → Partner → Admin → Ringmaster) without altering earlier screenshots or copy.

---

## 7. Verification (run on every build)

- `data:image/png` count == total screens across all groups == `"caption"` count == `"title"` count (currently 123).
- **0** external `http(s)://` references — fully self-contained (fonts + images inline); 0 leaked Figma URLs.
- 0 leftover template placeholders.
- Jargon blocklist absent from Customer + Partner copy.
- Embedded fonts = 4 latin `@font-face` blocks.
- JS controller passes `node --check` and a stubbed-DOM smoke run that routes into both a mobile flow (phone frame shown) and a desktop flow (browser frame shown, correct address bar) — confirming the viewport branch fires.

---

## 8. Known limitations & open questions (for Sreekesh)

1. **File size: 9.49 MB.** Works great as a downloaded/local file (opens offline in any browser), but this **exceeds the claude.ai Artifact hosting limit** and is slow over the network. The Ringmaster group alone adds ~4.9 MB (38 dense high-res desktop screens).
   - *Decision needed:* host it or keep it as a shared file? If hosting matters, options are (a) split Ringmaster's 5 secondary manage/edit flows into a second file, keeping the 3 primary create/listing flows; or (b) drop desktop source to ~1280px + quantize harder (~40% smaller, slightly softer text).
2. **Ringmaster scope = 8 flows.** The live Figma had drifted well beyond the iPRD's single 3-frame "Edit" flow — it now has separate manage sections (add-pc, import-pc, edit-options, fresh edit-options, modify-value). I built one flow per live section. *Is that the right granularity, or should the 5 manage/edit flows be merged into ~2 ("Edit a takeover offer" / "Edit a fresh offer")?*
3. **Happy-path only.** Error/empty/loading variants are dropped except where they're a meaningful step (e.g. Customer App has a dedicated "If something goes wrong" flow; Ringmaster keeps the OCR-loading and PC-pending states). *Confirm error coverage is sufficient.*
4. **Copy is mine, not design-signed-off.** Captions were authored from the screens + iPRDs. *Worth a copy pass, especially the Ringmaster/Admin internal-term phrasing.*
5. **Snapshot in time.** Screenshots reflect Figma as of this build; any design change needs a re-export of the affected frames (pipeline §6 makes this cheap — re-run one group's build script).

---

## 9. Sources

- Spec / design system: `CUSTOMER-APP-DECK-TEMPLATE.md`
- Figma files: offers-user-app (`zarJnV0HTbJIVL7JLshfIw`), px-app-oro-offer (`flPHXmpw3rYLQ2jp0slSyt`), admin-offers (`Zoiv8nXNrMBYKxyzbEQxMK`), ringmaster-offers (`rUb45qKfaQA2E68zFzeFdn`)
- iPRDs: ENG-2186 (Partner), ENG-2456 (Admin), ENG-2732 (Ringmaster) — all under ENG-1014 (Takeover Engine Revamp)
