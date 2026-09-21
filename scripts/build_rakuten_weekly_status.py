# -*- coding: utf-8 -*-
"""
Rakuten weekly status report, AccuKnox branded.

Rebuilds the source draft ("Rakuten weekly status report.pptx", a 13.33 x 7.5 in
deck with one title slide and one very dense status slide) on the AccuKnox master
template at 10 x 5.625 in.

Every fact from the source is kept. Nothing is added. The one dense slide is split
into three readable slides, because the source packed two panels and a four-row
table into a single 7.5 in canvas.

Changes on top of the source:
  - AccuKnox master layouts, palette and Space Grotesk throughout.
  - Slide 1 is the AccuKnox cover layout, co-branded with the Rakuten wordmark on
    a white pill under the title. The AccuKnox lockup comes from the layout.
  - The source title slide carried an empty second title placeholder. Dropped.
  - Vertical-tab characters inside the source runs are rewritten as real breaks.
  - Semicolons, ampersands in prose and the en dash in "- P0" are rewritten.
  - "24-28th August" becomes "24 to 28 August 2026", to match the 2026 target dates.

Build:   py -3.11 scripts/build_rakuten_weekly_status.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_Rakuten_Weekly_Status.pptx -Out output/render/rakuten
"""
import os, shutil, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image as PILImage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import *                      # noqa: F401,F403  palette + primitives
from _akdeck import _ph, _move_ph, _fill_ph

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "PPT Template.pptx")
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_Rakuten_Weekly_Status.pptx")
RAK  = os.path.join(HERE, "..", "assets", "partner-logos", "rakuten.png")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_COVER, L_CLOSE, L_STD = prs.slide_layouts[0], prs.slide_layouts[1], prs.slide_layouts[4]

xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try: prs.part.drop_rel(sid.get(qn('r:id')))
    except Exception: pass
    xml_slides.remove(sid)

WEEK = "Week of 24 to 28 August 2026"


# =================================================================== helpers
def std(title, kicker, lede=None, source=None):
    """A content slide on the navy-band layout."""
    s = prs.slides.add_slide(L_STD); set_title(s, title); blank_footer(s)
    eyebrow(s, kicker, y=0.84, w=8.6)
    if lede:
        box(s, CX, 1.10, CW, 0.32, text=lede, size=10.2, color=MUTE,
            anchor=MSO_ANCHOR.MIDDLE)
    if source:
        footer_note(s, source, y=5.24, size=7.6)
    return s


def panel(s, x, y, w, h, head=None, fill=WHITE, line=GREY_BD, hcolor=GREY_TX):
    """White rounded card. Returns the y where content should start."""
    box(s, x, y, w, h, fill=fill, line=line, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
    if head:
        box(s, x + 0.20, y + 0.10, w - 0.40, 0.24, text=head.upper(), size=8.0,
            color=hcolor, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        return y + 0.40
    return y + 0.14


def metric(s, x, y, w, value, label, sub=None, accent=PRIMARY, vsize=17, h=0.94):
    box(s, x, y, w, h, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, x + 0.10, y + 0.13, 0.055, h - 0.26, fill=accent)
    box(s, x + 0.24, y + 0.09, w - 0.34, 0.38, text=value, size=vsize, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0)
    box(s, x + 0.24, y + 0.47, w - 0.32, 0.22, text=label.upper(), size=6.6,
        color=NAVY, bold=True, anchor=MSO_ANCHOR.TOP, ml=0)
    if sub:
        box(s, x + 0.24, y + 0.67, w - 0.32, h - 0.72, text=sub, size=6.5,
            color=GREY_TX, anchor=MSO_ANCHOR.TOP, ml=0)


def metrics(s, y, items, x=CX, w=CW, gap=0.12, h=0.94, vsize=17):
    n = len(items)
    cw = (w - gap * (n - 1)) / n
    for i, it in enumerate(items):
        metric(s, x + i * (cw + gap), y, cw, it[0], it[1], it[2],
               accent=it[3], vsize=vsize, h=h)


def dot(s, x, y, d, color):
    return box(s, x, y, d, d, fill=color, shape=MSO_SHAPE.OVAL,
               ml=0, mr=0, mt=0, mb=0)


_EDGES = ["L", "R", "T", "B"]


def cell_border(cell, edges="LRTB", color=GREY_BD, wpt=0.75):
    """python-pptx has no border API, so write the a:ln* elements by hand.
    They must precede the fill element, so they are inserted at the front."""
    tcPr = cell._tc.get_or_add_tcPr()
    idx = 0
    for e in _EDGES:
        tag = qn("a:ln" + e)
        for old in tcPr.findall(tag):
            tcPr.remove(old)
        if e not in edges:
            continue
        ln = tcPr.makeelement(tag, {"w": str(int(wpt * 12700)), "cap": "flat",
                                    "cmpd": "sng", "algn": "ctr"})
        fill = ln.makeelement(qn("a:solidFill"), {})
        clr = fill.makeelement(qn("a:srgbClr"), {"val": str(color)})
        fill.append(clr); ln.append(fill)
        tcPr.insert(idx, ln); idx += 1


def table_grid(t, color=GREY_BD):
    """Light grid on the body rows. The navy header needs no lines."""
    for ri in range(1, len(t.rows)):
        for ci in range(len(t.columns)):
            cell_border(t.cell(ri, ci), "LRTB", color=color)


def center_col(t, ci, size=8.0):
    for ri in range(1, len(t.rows)):
        for p in t.cell(ri, ci).text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER


def logo_pill(s, x, y, w, h, path, pad=0.10, radius=0.5, fill=WHITE):
    """A white rounded pill with a partner mark centred inside it, sized so the
    mark keeps its clear space on all four sides."""
    box(s, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)
    im = PILImage.open(path); ar = im.size[0] / im.size[1]
    ih = h - 2 * pad
    iw = ih * ar
    if iw > w - 2 * pad:
        iw = w - 2 * pad; ih = iw / ar
    pic = s.shapes.add_picture(path, Inches(x + (w - iw) / 2), Inches(y + (h - ih) / 2),
                               Inches(iw), Inches(ih))
    pic.shadow.inherit = False
    return pic


def cobrand_cover(title, subtitle, partner):
    """The AccuKnox front cover on layout 0, co-branded.

    The layout already carries the AccuKnox lockup, the three badge groups and the
    product collage, so nothing here redraws them. The only addition is the partner
    mark, on a white pill under the title, where the layout leaves clear space.
    """
    s = prs.slides.add_slide(L_COVER)
    blank_footer(s)
    ph = _ph(s, 0)
    tx, tw = _move_ph(ph, 1.84, 1.00)
    _fill_ph(ph, title, 25, WHITE, True, spacing=1.0)
    sub = _ph(s, 1)
    _move_ph(sub, 2.88, 0.34)
    _fill_ph(sub, subtitle, 10.5, NAVY_TXT, False)
    pw, phh = 1.42, 0.46
    logo_pill(s, tx + (tw - pw) / 2, 3.32, pw, phh, partner, pad=0.10)
    return s


# =================================================================== 1. cover
cobrand_cover("Rakuten Weekly\nStatus Report",
              "On-premises deployment programme, 24 to 28 August 2026",
              RAK)


# ======================================================== 2. week at a glance
s = std("Week at a Glance", WEEK,
        "Joint AccuKnox and Rakuten status on the on-premises deployment programme.")

metrics(s, 1.52, [
    ("3",      "Milestones closed",  "Prerequisites, kickoff, lab access", GREEN),
    ("1",      "Open blocker",       "Priority P0, Rakuten action",        RED),
    ("4",      "Activities planned", "Across the next two weeks",          PRIMARY),
    ("09 Sep", "Go or no-go gate",   "Deployment readiness review",        SECOND),
], h=1.10, vsize=18)

# the one P0, called out where an executive reads first
y = 2.82
box(s, CX, y, CW, 1.02, fill=RED_LT, line=RED, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
pill(s, CX + 0.18, y + 0.22, 0.52, 0.24, "P0", fill=RED, size=8.5)
box(s, CX + 0.80, y + 0.16, CW - 1.00, 0.32, size=11.5, color=NAVY, bold=True,
    text="Kiba lab availability date is not confirmed", anchor=MSO_ANCHOR.MIDDLE)
box(s, CX + 0.80, y + 0.50, CW - 1.00, 0.40, size=9.6, color=INK,
    anchor=MSO_ANCHOR.TOP,
    text="Rakuten confirmation is required on Robin cluster access and resource "
         "provisioning. The date unlocks deployment initiation.")

# the two standing facts about how the programme runs
y = 4.04
cw = (CW - 0.14) / 2
for i, (g, head, sub) in enumerate([
    ("clock",  "Weekly cadence sync",  "Every Wednesday at 12:30 PM, both sides."),
    ("key",    "Kiba access granted",  "AccuKnox users have access to the Kiba lab."),
]):
    x = CX + i * (cw + 0.14)
    box(s, x, y, cw, 0.86, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    icon(s, x + 0.20, y + 0.23, 0.42, G(g), bg=PRIMARY)
    box(s, x + 0.74, y + 0.16, cw - 0.92, 0.30, text=head, size=11, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.74, y + 0.46, cw - 0.92, 0.30, text=sub, size=9.2, color=MUTE,
        anchor=MSO_ANCHOR.TOP)

footer_note(s, "Counts are derived from this week's status review.", y=5.04, size=7.6)


# ============================================ 3. accomplishments and blockers
s = std("Progress and Open Items", WEEK,
        "What is closed, and the single item that still needs a Rakuten decision.")

LW, RW = 5.42, 3.66
PY, PH = 1.52, 3.55
ly = panel(s, CX, PY, LW, PH, head="Key accomplishments so far")
for i, (g, head, sub) in enumerate([
    ("check", "Prerequisites and POCs confirmed",
     "The initial prerequisite one-pager is delivered. POCs are finalized on both sides."),
    ("flag", "Kickoff and cadence established",
     "The deployment kickoff concluded. Pre-arb slides went out on 12 August, updated on 17 August."),
    ("key", "Kiba access provided to AccuKnox",
     "AccuKnox users have Kiba access. The weekly sync runs every Wednesday at 12:30 PM."),
]):
    yy = ly + 0.10 + i * 1.06
    icon(s, CX + 0.22, yy + 0.04, 0.42, G(g), bg=GREEN)
    box(s, CX + 0.78, yy, LW - 1.00, 0.30, text=head, size=11.6, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, CX + 0.78, yy + 0.30, LW - 1.00, 0.56, text=sub, size=9.4, color=MUTE,
        anchor=MSO_ANCHOR.TOP)
    if i < 2:
        box(s, CX + 0.78, yy + 0.92, LW - 1.00, 0.012, fill=GREY_BD)

RX = CX + LW + 0.12
ry = panel(s, RX, PY, RW, PH, head="Key blockers and dependencies",
           fill=RED_LT, line=RED, hcolor=RED)
pill(s, RX + 0.22, ry + 0.02, 0.52, 0.24, "P0", fill=RED, size=8.5)
box(s, RX + 0.22, ry + 0.36, RW - 0.44, 0.34, size=13, color=NAVY, bold=True,
    text="Kiba lab availability date", anchor=MSO_ANCHOR.TOP)
box(s, RX + 0.22, ry + 0.74, RW - 0.44, 0.62, size=10, color=INK,
    anchor=MSO_ANCHOR.TOP,
    text="Rakuten confirmation is required on Robin cluster access and resource "
         "provisioning.")
box(s, RX + 0.22, ry + 1.34, RW - 0.44, 0.012, fill=RED)
yy = ry + 1.48
for lab, val, col, vh in [("Owner", "Rakuten", NAVY, 0.24),
                          ("Target date", "03 Sep 2026", NAVY, 0.24),
                          ("Impact if late",
                           "Deployment initiation and cluster\naccess stay blocked.", RED, 0.44)]:
    box(s, RX + 0.22, yy, RW - 0.44, 0.20, text=lab.upper(), size=6.8, color=GREY_TX,
        bold=True, anchor=MSO_ANCHOR.TOP)
    box(s, RX + 0.22, yy + 0.19, RW - 0.44, vh, text=val, size=9.6, color=col,
        bold=True, anchor=MSO_ANCHOR.TOP)
    yy += 0.19 + vh + 0.08


# ================================================= 4. next activities planned
s = std("Next Activities Planned", "Upcoming two weeks",
        "Four dated milestones run from 02 September to the go or no-go gate on 09 September.")

# date strip, so the two-week shape reads before the table detail
y = 1.50
dates = [("02 Sep", "Deployment package", PRIMARY),
         ("03 Sep", "Lab access schedule", RED),
         ("04 Sep", "RTO, RPO and database", SECOND),
         ("09 Sep", "Go or no-go gate", GREEN)]
cw = CW / len(dates)
first, last = CX + cw / 2, CX + (len(dates) - 1) * cw + cw / 2
box(s, first, y + 0.255, last - first, 0.02, fill=GREY_BD)
for i, (d, lab, col) in enumerate(dates):
    cx = CX + i * cw
    dot(s, cx + cw / 2 - 0.075, y + 0.19, 0.15, col)
    box(s, cx, y - 0.06, cw, 0.24, text=d, size=10.5, color=NAVY, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
    box(s, cx, y + 0.40, cw, 0.24, text=lab, size=8, color=MUTE,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)

rows = [
    ["Planned activity or milestone", "Target date", "Ownership",
     "Expected outcome and key deliverable"],
    ["Deliver Robin.io and IPv6 deployment package", "02 Sep 2026",
     "Rakuten and AccuKnox",
     "The on-premises distribution bundle and the IPv6 networking deployment guide."],
    ["Finalize Kiba lab access schedule", "03 Sep 2026", "Joint PMs",
     "A confirmed lab availability date unlocks deployment initiation and cluster access."],
    ["Review RTO, RPO and control plane database specs", "04 Sep 2026",
     "Joint architecture",
     "PostgreSQL high availability topology and disaster recovery procedures approved."],
    ["Deployment readiness review, the go or no-go gate", "09 Sep 2026",
     "Joint project leads",
     "A formal gate review and sign-off before the on-premises cluster rollout starts."],
]
t = table(s, CX, 2.34, CW, 2.62, rows, colw=[2.86, 1.00, 1.44, 3.90],
          hsize=8.6, bsize=8.0)
table_grid(t)
center_col(t, 1)

footer_note(s, "Ownership and target dates are as agreed in the weekly sync.",
            y=5.10, size=7.6)


# ================================================================= 5. closing
closing_slide(prs)


prs.save(OUT)
print("wrote", os.path.abspath(OUT), "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
