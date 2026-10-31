# -*- coding: utf-8 -*-
"""
Four standalone AccuKnox product decks for Veracode: Container Security + IaC, CSPM,
DSPM, API Security. Content lives in veracode_specs.py, layout in _veracode_kit.py.

Build:   py -3.11 scripts/build_veracode_products.py [key ...]
Render:  powershell -File scripts/render.ps1 -Pptx <abs pptx> -Out <abs dir>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import google_safe
import _veracode_kit as K
import veracode_specs as V
import veracode_specs_v2  # noqa: F401  applies v2 content
import veracode_specs_v3  # noqa: F401  applies v3 content

google_safe()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, "..", "output", "veracode")
DIAG = os.path.join(HERE, "..", "work", "veracode", "diagrams")
os.makedirs(OUTD, exist_ok=True)

want = set(sys.argv[1:])
for sp in V.ALL:
    if want and sp["key"] not in want:
        continue
    import _veracode_visuals as VV
    pr = sp["problem"]
    pr["png"] = VV.svg_problem(sp["key"] + "_problem", DIAG, pr["hero"], pr["cards2"])
    so = sp["overview"]
    so["png"] = VV.svg_solution(sp["key"] + "_solution", DIAG, so["title_lines"], so["hub"], so["hub_logos"])
    t = sp["tech"]
    t["png"] = K.svg_arch(sp["key"] + "_arch", DIAG, t["cols"], t["cp_title"], t["cp_rows"])
    d = sp["deploy"]
    d["png"] = K.svg_deploy(sp["key"] + "_deploy", DIAG, d["env"], d["rows"], d["cp_lines"], d["note"])
    out = K.Deck(sp, os.path.join(OUTD, sp["file"])).build()
    print("saved", out)
