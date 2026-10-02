# -*- coding: utf-8 -*-
"""Crop the four screens the TCTS use-case slides add.

Each crop drops the console sidebar, which carries staff names, and the tenant
switcher. Output lands in output/assets/tcts beside the recovered deck images.

Run:  py -3.11 scripts/prep_tcts_usecase_assets.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output" / "assets" / "tcts"
AGENTZ = ROOT / "output" / "assets" / "agentz"
HELP = Path(r"D:\AccuKnox\help\docs")

CROPS = [
    # AgentZ run graph: KubeArmor alert investigation, every step Succeeded
    (AGENTZ / "tour-4-run.png", (318, 92, 1688, 690), "u2_alert_workflow.png"),
    # AgentZ traces: spans, tool calls and tokens per run
    (AGENTZ / "tour-7-prove.png", (318, 64, 1688, 560), "u10_traces.png"),
    # Collectors: ML static scan and the PII/PHI dataset scan
    (HELP / "how-to" / "image-10.png", (225, 400, 1935, 790), "u4_collectors.png"),
    # Red teaming: static or intelligent scan, categories with prompt counts
    (HELP / "getting-started" / "images" / "release-notes" / "v3.6" / "redteam-prompt-categories.png",
     (0, 0, 1923, 1560), "u5_redteam_scan.png"),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for src, box, name in CROPS:
        im = Image.open(src)
        if im.mode == "RGBA":
            flat = Image.new("RGB", im.size, "white")
            flat.paste(im, mask=im.split()[3])
            im = flat
        im = im.convert("RGB").crop(box)
        im.save(OUT / name, optimize=True)
        print(name, im.size)


if __name__ == "__main__":
    main()
