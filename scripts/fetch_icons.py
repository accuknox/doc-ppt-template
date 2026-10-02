# -*- coding: utf-8 -*-
"""
Pull icons into assets/icons/ by name. Three open-source sets:

  brand  Devicon (MIT), full-color logos.  Name: <slug>-original or <slug>-plain
         e.g. java-original, kubernetes-plain. Browse https://devicon.dev
  si-    Simple Icons (CC0), one-color logos for brands Devicon lacks.
         Name: si-<slug>, e.g. si-vmware, si-okta. Browse https://simpleicons.org
  ui     Tabler Icons (MIT), outline UI glyphs. Name: <name>, e.g. key, shield-lock.
         Browse https://tabler.io/icons

Usage:
  py -3.11 scripts/fetch_icons.py brand java-original go-original
  py -3.11 scripts/fetch_icons.py brand si-okta si-splunk
  py -3.11 scripts/fetch_icons.py ui shield-lock cloud-lock
  py -3.11 scripts/fetch_icons.py --list      # print what is already here

Existing files are kept. A miss prints the name, so try the other set or the
-plain variant. Simple Icons draws one-color shapes in black, and _aksvg tints them navy.
"""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "assets", "icons")
DEVICON = "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/{slug}/{name}.svg"
SIMPLE  = "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg"
TABLER  = "https://cdn.jsdelivr.net/npm/@tabler/icons@latest/icons/outline/{name}.svg"


def fetch(url, dest):
    # curl, not urllib: Python on some machines here carries an expired CA root.
    r = subprocess.run(["curl", "-s", "-f", "-L", "-o", dest, url], capture_output=True)
    if r.returncode != 0 and os.path.exists(dest):
        os.remove(dest)
    return r.returncode == 0


def main(argv):
    if not argv or argv[0] == "--list":
        for kind in ("brand", "ui"):
            d = os.path.join(ROOT, kind)
            names = sorted(f[:-4] for f in os.listdir(d) if f.endswith(".svg"))
            print(f"{kind} ({len(names)}): " + " ".join(names))
        return 0
    kind, names = argv[0], argv[1:]
    if kind not in ("brand", "ui"):
        print("first argument is brand or ui"); return 2
    os.makedirs(os.path.join(ROOT, kind), exist_ok=True)
    misses = 0
    for n in names:
        dest = os.path.join(ROOT, kind, n + ".svg")
        if os.path.exists(dest):
            print("have", n); continue
        if kind == "ui":
            url = TABLER.format(name=n)
        elif n.startswith("si-"):
            url = SIMPLE.format(slug=n[3:])
        else:
            url = DEVICON.format(slug=n.split("-", 1)[0], name=n)
        ok = fetch(url, dest)
        print(("got " if ok else "MISS ") + n)
        misses += 0 if ok else 1
    return 1 if misses else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
