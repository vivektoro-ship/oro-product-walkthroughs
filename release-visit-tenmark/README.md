# Release Visit Revamp — Tenmark Gold Loans (ENG-4953)

Single-page walkthrough prototype. Plain HTML, CSS and JS in `index.html`, no build step, no
dependencies except Google Fonts. Deploys as a static file.

## Running it

Open `index.html`, or serve the folder: `python3 -m http.server 8899`.

## Structure

Two paths behind the pill toggle. Steps 1-18 are shared: the visit landing, self-pickup, the
code, the live photo and the whole gold verification. Regular then runs to eSign, handover and
completion (31 steps including the four-step mismatch branch). Third party forks after
verification into identity, documents, CORE approval and handover (35 steps including the
three-step rejection branch).

Failure branches are dashed in the step rail and turn red when selected. Arrow keys move
between steps, clicking either device advances, and step 22 of the third party path has a
selector swapping the document set between death case, customer missing, abroad and sick.

CORE steps replace the right-hand phone with a browser frame.

## Screens

77 keys, each a 2x PNG in `screens/` named exactly as the key, mapped to its Figma node id in
the `SCREENS` object at the top of the script. File key: `T5JDdFqTJVi2pgTGeCzU3S`.

Two are deliberately never designed and always render a placeholder:

- `px-flag-reason` — the flag-reason picker
- `tp-rejected-px` — what the agent sees on a rejected third party release

Anything else that fails to load shows a striped placeholder naming the path it looked for.

Screens taller than the 312x640 device scroll inside it, with no scrollbar drawn.
