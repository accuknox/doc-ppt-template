# -*- coding: utf-8 -*-
"""Cover and closing slides for the AI security comparison matrix PDF.

The body pages render from HTML in build_ai_matrix.py. This script builds only
the two fixed template slides, layout 0 and layout 1, so the PDF opens and
closes on the real AccuKnox artwork.

Usage:  py -3.11 scripts/build_ai_matrix_covers.py <out.pptx> ["Cover\nTitle"]
"""
import os
import sys

from pptx import Presentation
from pptx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import cover_slide, closing_slide  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "PPT Template.pptx")
OUT = sys.argv[1]

prs = Presentation(SRC)
lst = prs.slides._sldIdLst
for sid in list(lst):
    prs.part.drop_rel(sid.get(qn("r:id")))
    lst.remove(sid)

# An optional second argument replaces the title. Write line breaks in it as a literal \n.
TITLE = (sys.argv[2].replace("\\n", "\n") if len(sys.argv) > 2
         else "AccuKnox vs Palo Alto,\nCrowdStrike and Varonis\nAI Security")
cover_slide(prs, TITLE, tsize=23, y=1.95, h=1.50)
closing_slide(prs)
prs.save(OUT)
print(OUT)
