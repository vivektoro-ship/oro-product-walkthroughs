#!/usr/bin/env python3
"""Download Figma frames as 2x PNGs into assets/<folder>/.

Usage:
    FIGMA_TOKEN=figd_xxx python3 scratchpad/pull_figma.py onboarding
    FIGMA_TOKEN=figd_xxx python3 scratchpad/pull_figma.py renewal
    FIGMA_TOKEN=figd_xxx python3 scratchpad/pull_figma.py all

Scale 2 is deliberate: the decks render 375-wide phone screens, so 2x is what
keeps them crisp on retina. Do not go below 2.

Re-running is cheap — anything already on disk is skipped.
Standard library only (same rule as the build scripts).
"""
import os
import subprocess
import sys
import urllib.error
import urllib.request

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCALE = 2
BATCH = 20  # ids per /v1/images call

# ---------------------------------------------------------------- manifests --
# Each manifest is a plain list of (node_id, output_filename) pairs.
# Filenames carry the flow order up front so the folder sorts into flow order,
# and the node id at the end so any screen can be traced back to Figma.

ONBOARDING_FILE = "YeLUqHZeddjjIEgdyUFAu4"   # Oro User App — Master
RENEWAL_FILE = "pPxGbxwFHMA4HXumFt5qTs"      # March–April 26

# Onboarding — happy path only (top row of each sub-section of section
# 1504:45302 "Onboarding", page "Module 1 - Onboarding & Homepage").
ONBOARDING_SECTIONS = [
    ("mobile", [
        "1504:33724", "1504:33694", "1504:34215", "1504:34310", "1504:33754",
        "1504:34169", "1504:34582", "2123:40791", "2123:40822", "2123:40881",
    ]),
    ("city", [
        "1504:34907", "1504:35162",
    ]),
    ("email", [
        "1504:35253", "1504:35427", "1504:35513", "1504:35595", "1504:35853",
    ]),
    ("liveliness", [
        "1504:36015", "1504:36129", "1504:36029", "1504:36045", "1504:36061",
        "1504:36156",
    ]),
    ("identity", [
        "1504:37467", "1504:37290", "1504:37314", "1504:37322",
    ]),
    ("father", [
        "1504:28379", "1504:28349",
    ]),
    ("pan", [
        "1504:44126", "1504:44174", "1504:44222", "1504:44272",
    ]),
    ("personal", [
        "1504:45076", "1504:45105", "1504:45222", "1504:28408", "1504:28544",
        "1504:28494", "1504:28451", "1504:32022", "1504:32822", "1504:33261",
        "1504:33222", "1504:33239",
    ]),
    ("address", [
        "1504:30451", "1504:30487", "1504:30627", "1504:30797", "1504:31361",
        "1504:31551",
    ]),
    ("bank", [
        "1504:29659", "1504:29682", "1504:29764", "1504:29880", "1504:29900",
    ]),
    ("nominee", [
        "1504:29340", "1504:29365", "1504:29405", "1504:29489", "1504:29617",
        "1504:29530", "1504:29091",
    ]),
]

# Renewal — main row of section 6260:81538 "eSign flow swap", page "User App",
# left to right. The not-yet-onboarded side branch (6252:76235 … 6252:76450,
# 13 screens) is deliberately dropped: it duplicates the onboarding flow.
RENEWAL_NODES = [
    "6252:75650", "6252:75976", "6252:75459", "6252:75264", "6252:74404",
    "6252:74496", "6252:74639", "6252:74834", "6252:76631", "6252:75575",
    "6252:77223", "6252:77260", "6252:77280", "6252:77332", "6252:75475",
    "6252:75366", "6252:75172", "6252:75029", "6252:76781", "6252:77349",
    "6252:77395", "6252:76923", "6252:76887", "6252:76899", "6252:76966",
    "6252:80608", "6252:76757", "6252:76946", "6252:76990", "6252:78415",
    "6252:77467", "6252:77950", "6252:77700", "6252:78195",
]


def slug(node_id):
    return node_id.replace(":", "-")


def onboarding_manifest():
    out = []
    for si, (name, nodes) in enumerate(ONBOARDING_SECTIONS, start=1):
        for i, nid in enumerate(nodes, start=1):
            out.append((nid, "s%02d-%s-%02d-%s.png" % (si, name, i, slug(nid))))
    return out


def renewal_manifest():
    return [(nid, "r%02d-%s.png" % (i, slug(nid)))
            for i, nid in enumerate(RENEWAL_NODES, start=1)]


JOBS = {
    "onboarding": (ONBOARDING_FILE, onboarding_manifest, "assets/onboarding"),
    "renewal": (RENEWAL_FILE, renewal_manifest, "assets/renewal"),
}


# ------------------------------------------------------------------- figma ---
def token():
    tok = os.environ.get("FIGMA_TOKEN", "").strip()
    if not tok:
        sys.exit(
            "FIGMA_TOKEN is not set.\n"
            "Create a personal access token at Figma → Settings → Security →\n"
            "Personal access tokens, then run:\n\n"
            "    export FIGMA_TOKEN=figd_your_token_here\n"
            "    python3 scratchpad/pull_figma.py onboarding\n"
        )
    return tok


def get_json(url, tok):
    req = urllib.request.Request(url, headers={"X-Figma-Token": tok})
    with urllib.request.urlopen(req, timeout=180) as r:
        import json
        return json.load(r)


def image_urls(file_key, node_ids, tok):
    """Resolve node ids -> rendered PNG urls, batched."""
    urls = {}
    for i in range(0, len(node_ids), BATCH):
        batch = node_ids[i:i + BATCH]
        url = ("https://api.figma.com/v1/images/%s?ids=%s&format=png&scale=%d"
               % (file_key, ",".join(batch), SCALE))
        print("  resolving %d ids (%d/%d)…"
              % (len(batch), min(i + BATCH, len(node_ids)), len(node_ids)))
        try:
            data = get_json(url, tok)
        except urllib.error.HTTPError as e:
            sys.exit("Figma API %s on %s\n%s"
                     % (e.code, url, e.read().decode("utf-8", "replace")[:500]))
        if data.get("err"):
            sys.exit("Figma API error: %s" % data["err"])
        urls.update(data.get("images") or {})
    return urls


def download(url, dest):
    with urllib.request.urlopen(url, timeout=300) as r:
        body = r.read()
    with open(dest, "wb") as f:
        f.write(body)
    return len(body)


def compress(paths):
    if not paths:
        return
    from shutil import which
    if not which("pngquant"):
        print("  note: pngquant not on PATH — skipping compression "
              "(brew install pngquant)")
        return
    print("  compressing %d file(s) with pngquant…" % len(paths))
    subprocess.run(["pngquant", "--quality=65-90", "--force", "--ext", ".png"]
                   + paths, check=False)


def folder_size(d):
    return sum(os.path.getsize(os.path.join(d, f)) for f in os.listdir(d)
               if os.path.isfile(os.path.join(d, f)))


def pull(job):
    file_key, manifest_fn, rel_out = JOBS[job]
    manifest = manifest_fn()
    outdir = os.path.join(HOME, rel_out)
    os.makedirs(outdir, exist_ok=True)

    print("\n== %s == %d frame(s) -> %s" % (job, len(manifest), rel_out))
    todo = [(nid, fn) for nid, fn in manifest
            if not os.path.exists(os.path.join(outdir, fn))]
    skipped = len(manifest) - len(todo)
    if not todo:
        print("  everything already downloaded (%d skipped)" % skipped)
        print("  folder: %.1f MB" % (folder_size(outdir) / 1024 / 1024))
        return

    urls = image_urls(file_key, [nid for nid, _ in todo], token())

    got, missing, fresh = 0, [], []
    for nid, fn in todo:
        url = urls.get(nid)
        if not url:
            missing.append(nid)
            continue
        dest = os.path.join(outdir, fn)
        download(url, dest)
        fresh.append(dest)
        got += 1
        print("  %-42s %s" % (fn, nid))

    compress(fresh)

    print("  downloaded %d | skipped %d | folder %.1f MB"
          % (got, skipped, folder_size(outdir) / 1024 / 1024))
    if missing:
        print("  !! %d node id(s) returned NO image — check these in Figma:"
              % len(missing))
        for nid in missing:
            print("       %s" % nid)


if __name__ == "__main__":
    args = sys.argv[1:] or ["all"]
    jobs = list(JOBS) if args == ["all"] else args
    bad = [j for j in jobs if j not in JOBS]
    if bad:
        sys.exit("unknown job(s): %s — pick from: %s, all"
                 % (", ".join(bad), ", ".join(JOBS)))
    token()  # fail fast before any work
    for j in jobs:
        pull(j)
