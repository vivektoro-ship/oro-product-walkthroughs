# Release Visit Revamp — Tenmark Gold Loans (ENG-4953)

Single-page walkthrough prototype. Plain HTML, CSS and JS in `index.html`, no build step,
no dependencies except Google Fonts. Deploys as a static file.

## Running it

Open `index.html`, or serve the folder: `python3 -m http.server 8899`.

## Adding screens

Export each frame from Figma as a PNG into `screens/`, named exactly as the filename column
in the export table at the bottom of the page, e.g. `screens/px-pickup.png`.

Anything not yet exported keeps a striped "Not exported" placeholder showing the path it
looked for. Two screens are deliberately marked `designed:false` and always show
"Not designed": `px-flag-reason` and `cx-tp-rejected`.

## Node ids

The `SCREENS` map holds `{frame, node}` per filename, with real ids from the four
release-visit sections of `T5JDdFqTJVi2pgTGeCzU3S`:

| Section | Node | Frames |
|---|---|---|
| Regular release | `2040:50484` | 31 |
| Third party | `2055:56221` | 20 |
| cx app Release Flow | `2040:46187` | 22 |
| core changes | `2055:65382` | 13 |

Two rows stay red because the screens do not exist yet: `cx-on-hold` (what the customer sees
on a blocked visit) and `cx-tp-rejected` (what they see on a rejected third party release).

Eight exports are byte-identical pairs — the designer reused the same frame across sections
(handover photo, visit complete, waiting-for-receipt, visits listing, CORE listing, and
`item-detail--default` vs `--markings-expanded`).

## Flow

Four paths behind the pill toggle, one per Figma section: regular release (33 steps), third
party (22), customer app (14) and Tenmark CORE (13). Failure branches are dashed in the step
rail and turn red when selected. Arrow keys move between steps, and clicking either device
advances the flow.

Content is taken from ENG-4953: state machine names, the seven flag reasons, the four third
party categories and their document counts, and the locked decisions.
