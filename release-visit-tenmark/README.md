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

The `SCREENS` map at the top of the script holds `{frame, node}` per filename. Every `node`
is currently `null`: the frames do not exist in Figma file `T5JDdFqTJVi2pgTGeCzU3S` yet
(checked 2026-08-28 — that file has one page, `Admin`, with no `release-visit` frames), and
ENG-4953 has no Figma link on it. Paste real ids into that map as the frames are drawn; the
export table turns each row from red to black as its id lands.

## Flow

Two paths behind the pill toggle: regular release (17 steps) and third party release (11).
Failure branches — wrong code, mismatch, third party rejected — are dashed in the step rail
and turn red when selected. Arrow keys move between steps.

Content is taken from ENG-4953: state machine names, the seven flag reasons, the four third
party categories and their document counts, and the locked decisions.
