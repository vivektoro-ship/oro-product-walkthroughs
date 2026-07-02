#!/usr/bin/env python3
import base64, json, os

ASSETS = "/Users/pragadeesh-oro/assets"
OUT = "/Users/pragadeesh-oro/customer-app-offer-creation.html"

steps = [
    ("1-home.png",
     "Homepage — Get Oro Offer",
     "Customer taps Get Oro Offer on the app homepage to start a takeover offer."),
    ("2-choose-type.png",
     "Choose Offer Type",
     "Customer selects Takeover (vs Fresh) to begin the pledge-card flow."),
    ("3-upload.png",
     "Pledge Card Upload",
     "Customer captures or uploads a pledge card image — one card at a time."),
    ("4-fetching.png",
     "AI OCR Extraction",
     "AI OCR extracts lender, borrower, pledge card number, net gold weight, release amount."),
    ("5-fetched.png",
     "Review Extracted Fields",
     "Mandatory review — customer confirms or corrects the extracted fields. Cannot be skipped."),
    ("6-confirmation.png",
     "Add Card or Proceed",
     "Customer adds another pledge card or proceeds to generate the offer."),
    ("7-plans-loading.png",
     "Generating Plans",
     "System generates all eligible plans and assigns an Offer ID."),
    ("8-plans-created.png",
     "Plans Created",
     "Paginated plan list: name, lender, LTV, rate, indicative amount, tenure. Filters: High LTV / Low Interest / Zero Processing Fee. No plan pre-selected or locked."),
]

data = []
for fn, title, caption in steps:
    with open(os.path.join(ASSETS, fn), "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    data.append({"img": "data:image/png;base64," + b64, "title": title, "caption": caption})

steps_json = json.dumps(data)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Customer App — Takeover Offer Creation</title>
<style>
  :root{
    --bg:#0E0E0E; --bg2:#141414; --surface:#1C1C1C; --surface2:#222;
    --gold:#E5A93D; --gold-bright:#F0B440; --ink:#F4ECDD; --muted:#9c917c;
    --line:rgba(229,169,61,.30);
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;min-height:100%}
  body{display:flex;flex-direction:column;align-items:center;padding:28px 16px 56px}
  .wrap{width:100%;max-width:560px}

  /* progress bar */
  .pbar{height:4px;width:100%;background:#2a2a2a;border-radius:99px;overflow:hidden;margin-bottom:26px}
  .pbar > i{display:block;height:100%;background:linear-gradient(90deg,var(--gold),var(--gold-bright));
    border-radius:99px;transition:width .35s ease}

  header{text-align:center;margin-bottom:22px}
  header h1{font-size:22px;letter-spacing:.2px;color:var(--gold-bright);font-weight:700}
  header p{font-size:13px;color:var(--muted);margin-top:6px}

  /* phone frame */
  .stage{display:flex;flex-direction:column;align-items:center}
  .phone{width:340px;max-width:88vw;background:var(--surface);
    border:1px solid var(--line);border-radius:30px;padding:12px;
    box-shadow:0 18px 50px rgba(0,0,0,.55), inset 0 0 0 1px rgba(255,255,255,.02)}
  .screen{position:relative;border-radius:20px;overflow:hidden;background:var(--bg2);
    min-height:120px;display:flex;align-items:flex-start;justify-content:center}
  .screen img{display:block;width:100%;height:auto;opacity:0;transition:opacity .3s ease}
  .screen img.on{opacity:1}

  .meta{margin-top:20px;text-align:center;max-width:380px}
  .step-no{font-size:12px;letter-spacing:1.4px;text-transform:uppercase;color:var(--gold);font-weight:600}
  .meta h2{font-size:18px;margin-top:8px;color:var(--ink);font-weight:650}
  .meta p{font-size:14px;line-height:1.55;color:var(--muted);margin-top:10px}

  /* controls */
  .controls{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:24px}
  button.nav{appearance:none;border:1px solid var(--line);background:var(--surface);
    color:var(--ink);font-size:14px;font-weight:600;padding:11px 22px;border-radius:12px;
    cursor:pointer;transition:.18s;min-width:104px}
  button.nav:hover:not(:disabled){border-color:var(--gold);color:var(--gold-bright)}
  button.nav.primary{background:linear-gradient(180deg,var(--gold-bright),var(--gold));
    color:#1a1404;border-color:transparent}
  button.nav.primary:hover{filter:brightness(1.07)}
  button.nav:disabled{opacity:.32;cursor:not-allowed}

  .dots{display:flex;gap:9px;justify-content:center;margin-top:22px;flex-wrap:wrap}
  .dot{width:11px;height:11px;border-radius:50%;background:#3a3a3a;border:none;cursor:pointer;
    padding:0;transition:.2s}
  .dot:hover{background:#5a5a5a}
  .dot.active{background:var(--gold-bright);box-shadow:0 0 0 3px rgba(240,180,64,.18)}

  .hint{margin-top:26px;font-size:12px;color:#5f5949;text-align:center}
  kbd{background:#222;border:1px solid #333;border-radius:5px;padding:1px 6px;font-size:11px;color:var(--muted)}
</style>
</head>
<body>
<div class="wrap">
  <div class="pbar"><i id="pbar"></i></div>

  <header>
    <h1>Customer App — Takeover Offer Creation</h1>
    <p>The happy-path flow: from app homepage to a generated list of eligible takeover plans.</p>
  </header>

  <div class="stage">
    <div class="phone">
      <div class="screen"><img id="shot" alt=""></div>
    </div>

    <div class="meta">
      <div class="step-no" id="stepno">Step 1 of 8</div>
      <h2 id="title"></h2>
      <p id="caption"></p>
    </div>

    <div class="controls">
      <button class="nav" id="prev">&larr; Back</button>
      <button class="nav primary" id="next">Next &rarr;</button>
    </div>

    <div class="dots" id="dots"></div>
    <div class="hint">Use <kbd>&larr;</kbd> <kbd>&rarr;</kbd> arrow keys to navigate</div>
  </div>
</div>

<script>
  // ---- Dynamic workflow: add a screen by adding one entry here ----
  const STEPS = __STEPS__;

  let i = 0;
  const shot = document.getElementById('shot');
  const stepno = document.getElementById('stepno');
  const title = document.getElementById('title');
  const caption = document.getElementById('caption');
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const dots = document.getElementById('dots');
  const pbar = document.getElementById('pbar');

  STEPS.forEach((_, idx) => {
    const d = document.createElement('button');
    d.className = 'dot';
    d.setAttribute('aria-label', 'Go to step ' + (idx+1));
    d.addEventListener('click', () => go(idx));
    dots.appendChild(d);
  });

  function render(){
    const s = STEPS[i];
    shot.classList.remove('on');
    // swap source then fade in
    const tmp = new Image();
    tmp.onload = () => { shot.src = s.img; shot.alt = s.title; requestAnimationFrame(()=>shot.classList.add('on')); };
    tmp.src = s.img;
    if (tmp.complete) tmp.onload();

    stepno.textContent = 'Step ' + (i+1) + ' of ' + STEPS.length;
    title.textContent = s.title;
    caption.textContent = s.caption;
    prev.disabled = (i === 0);
    next.disabled = (i === STEPS.length - 1);
    pbar.style.width = (((i+1)/STEPS.length)*100) + '%';
    [...dots.children].forEach((d,idx)=>d.classList.toggle('active', idx===i));
  }
  function go(n){ i = Math.max(0, Math.min(STEPS.length-1, n)); render(); }

  prev.addEventListener('click', ()=>go(i-1));
  next.addEventListener('click', ()=>go(i+1));
  document.addEventListener('keydown', e=>{
    if(e.key==='ArrowRight') go(i+1);
    else if(e.key==='ArrowLeft') go(i-1);
  });

  render();
</script>
</body>
</html>
"""

html = html.replace("__STEPS__", steps_json)
with open(OUT, "w") as f:
    f.write(html)
print("WROTE", OUT, os.path.getsize(OUT), "bytes")
