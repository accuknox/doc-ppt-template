# -*- coding: utf-8 -*-
"""
Rakuten status report, AccuKnox branded.

Rebuilds the source draft ("Rakuten Status Report.pptx", a 9.53 x 5.36 in Google
Slides export with a bare title slide and two dense borderless tables) on the
AccuKnox master template at 10 x 5.625 in.

Every task, owner, date and status from the source is kept. Nothing is invented.
The two workstreams keep one slide each, because the brief asked for three slides.

Changes on top of the source:
  - AccuKnox master layouts, palette and Space Grotesk throughout.
  - Slide 1 is the AccuKnox cover layout, co-branded with the Rakuten wordmark on
    a white pill under the title. The AccuKnox lockup comes from the layout.
  - Each workstream slide gains a status count strip and a completion bar, so the
    shape of the programme reads before the table detail.
  - Status cells carry the brand severity tints instead of plain uppercase text.
  - Ampersands and slashes in prose are rewritten as words. "Go/No-Go" becomes
    "go or no-go". "Rakuten/Accuknox" becomes "Rakuten and AccuKnox".
  - "Accuknox" is spelled "AccuKnox". Dates gain a leading zero and a space.

Build:   py -3.11 scripts/build_rakuten_status_report.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_Rakuten_Status_Report.pptx -Out output/render/rakuten-status
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
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_Rakuten_Status_Report.pptx")
RAK  = os.path.join(HERE, "..", "assets", "partner-logos", "rakuten.png")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_COVER, L_CLOSE, L_STD = prs.slide_layouts[0], prs.slide_layouts[1], prs.slide_layouts[4]

xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try:
        prs.part.drop_rel(sid.get(qn("r:id")))
    except Exception:
        pass
    xml_slides.remove(sid)

ASOF = "Status as of 03 September 2026"

DONE, WIP, TODO = "DONE", "IN PROGRESS", "TO DO"
TINT = {DONE: (GREEN_LT, GREEN_DK), WIP: (LAV, PURPLE), TODO: (GREY_BG, MUTE)}


# =================================================================== helpers
def std(title, kicker, lede=None):
    """A content slide on the navy-band layout."""
    s = prs.slides.add_slide(L_STD)
    set_title(s, title)
    blank_footer(s)
    eyebrow(s, kicker, y=0.84, w=5.4)
    if lede:
        box(s, CX, 1.14, CW, 0.30, text=lede, size=9.8, color=MUTE,
            anchor=MSO_ANCHOR.MIDDLE)
    return s


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
        fill.append(clr)
        ln.append(fill)
        tcPr.insert(idx, ln)
        idx += 1


def table_grid(t, color=GREY_BD):
    """Light grid on the body rows. The navy header needs no lines."""
    for ri in range(1, len(t.rows)):
        for ci in range(len(t.columns)):
            cell_border(t.cell(ri, ci), "LRTB", color=color)


def set_rows(t, head_h, row_h, pad=0.02):
    """Fix the row heights and trim the cell padding.

    PowerPoint treats a row height as a minimum, so this only holds while every
    cell stays on one line. Shrinking the vertical margins buys back the space a
    thirteen-row table needs on a 5.625 in canvas."""
    for ri, row in enumerate(t.rows):
        row.height = Inches(head_h if ri == 0 else row_h)
        for c in row.cells:
            c.margin_top = Inches(pad)
            c.margin_bottom = Inches(pad)


def center_cols(t, cols):
    for ci in cols:
        for ri in range(1, len(t.rows)):
            for p in t.cell(ri, ci).text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER


def tint_status(t, ci, size=6.8):
    """Paint the status column with the brand severity tints."""
    for ri in range(1, len(t.rows)):
        c = t.cell(ri, ci)
        label = c.text_frame.text.strip()
        bg, fg = TINT.get(label, (WHITE, NAVY))
        c.fill.solid()
        c.fill.fore_color.rgb = bg
        for p in c.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                r.font.color.rgb = fg
                r.font.bold = True
                r.font.size = Pt(size)


def count_chips(s, counts, y=0.82, h=0.28):
    """Right-aligned status counts, sitting on the eyebrow line."""
    widths = {DONE: 1.02, WIP: 1.42, TODO: 1.02}
    x = CX + CW
    for label in (TODO, WIP, DONE):
        w = widths[label]
        x -= w
        bg, fg = TINT[label]
        box(s, x, y, w, h, fill=bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
        box(s, x, y, w, h, text="%d  %s" % (counts[label], label), size=8.0,
            color=fg, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
            wrap=False, ml=0, mr=0)
        x -= 0.10


def progress_bar(s, y, counts, h=0.11):
    """One bar, three segments, in task order: done, in progress, to do."""
    total = sum(counts.values())
    box(s, CX, y, CW, h, fill=GREY_BG)
    x = CX
    for label, color in ((DONE, GREEN), (WIP, SECOND), (TODO, GREY_BD)):
        seg = CW * counts[label] / total
        box(s, x, y, seg, h, fill=color)
        x += seg


def logo_pill(s, x, y, w, h, path, pad=0.10, radius=0.5, fill=WHITE):
    """A white rounded pill with a partner mark centred inside it, sized so the
    mark keeps its clear space on all four sides."""
    box(s, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)
    im = PILImage.open(path)
    ar = im.size[0] / im.size[1]
    ih = h - 2 * pad
    iw = ih * ar
    if iw > w - 2 * pad:
        iw = w - 2 * pad
        ih = iw / ar
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


HEAD = ["Task", "Description", "Owner", "Date", "Status"]
COLW = [2.30, 3.45, 1.30, 0.75, 1.40]


def workstream(title, lede, rows, top, height, bsize=7.2, ssize=6.8, note=None,
               head_h=0.30, row_h=0.25, pad=0.02):
    counts = {DONE: 0, WIP: 0, TODO: 0}
    for r in rows:
        counts[r[4]] += 1
    s = std(title, ASOF, lede)
    count_chips(s, counts)
    progress_bar(s, 1.52, counts)
    t = table(s, CX, top, CW, height, [HEAD] + rows, colw=COLW,
              hsize=8.0, bsize=bsize, firstcol_fill=None)
    set_rows(t, head_h, row_h, pad)
    table_grid(t)
    center_cols(t, [2, 3])
    tint_status(t, 4, size=ssize)
    if note:
        footer_note(s, note, y=5.30, size=7.2)
    return s


# =================================================================== 1. cover
cobrand_cover("Rakuten and AccuKnox\nStatus Report",
              "On-premises deployment programme, Kiba and Symphony",
              RAK)


# ===================================================================== 2. Kiba
workstream(
    "Kiba Workstream",
    "Five milestones are closed. Two Rakuten actions are open before the readiness gate.",
    [
        ["Collect prerequisites", "Hardware and OS architecture one-pager",
         "AccuKnox", "07 Aug", DONE],
        ["Deployment kickoff", "Project kickoff and milestone charter",
         "Rakuten and AccuKnox", "11 Aug", DONE],
        ["Confirm POCs and cadence", "Official POCs, weekly sync on Wednesday 12:30",
         "Rakuten and AccuKnox", "11 Aug", DONE],
        ["AD prod and stage access", "Access granted to the AccuKnox team",
         "Rakuten", "25 Aug", DONE],
        ["Pre-ARB review", "Pre-ARB presentation and scope alignment",
         "Rakuten and AccuKnox", "31 Aug", DONE],
        ["Resource provisioning", "Awaiting the Rakuten Kiba lab schedule",
         "Rakuten", "01 Sep", WIP],
        ["Registry access", "Direct AccuKnox registry access requested",
         "Rakuten", "02 Sep", WIP],
        ["Deployment readiness", "Formal go or no-go readiness gate review",
         "", "", TODO],
        ["Control plane deployment", "Deploy the AccuKnox control plane",
         "AccuKnox", "", TODO],
        ["Fault tolerance and DB HA", "RTO and RPO review, PostgreSQL cluster specs",
         "", "", TODO],
        ["Automated diagnostics", "Set up the AccuKnox diagnostics suite, RINC",
         "", "", TODO],
        ["Cluster onboarding", "KubeArmor eBPF runtime and Robin daemonset",
         "", "", TODO],
        ["UAT security validation", "Run the customer test plan, generate reports",
         "", "", TODO],
    ],
    top=1.74, height=3.48, bsize=7.2, ssize=6.6,
    head_h=0.30, row_h=0.245, pad=0.018)


# ================================================================= 3. Symphony
workstream(
    "Symphony Workstream",
    "The on-premises bundle is built. Server resources and registry access are pending.",
    [
        ["Managed K8s charts", "Charts for on-premises deployment on Robin",
         "AccuKnox", "20 Aug", DONE],
        ["On-prem bundle build", "Single server install and IPv6 package guide",
         "AccuKnox", "20 Aug", DONE],
        ["Resource provisioning", "Internal ticket raised for the server build",
         "Rakuten", "01 Sep", WIP],
        ["Registry access", "Direct AccuKnox registry access requested",
         "Rakuten", "02 Sep", WIP],
        ["Deployment readiness", "Formal go or no-go readiness gate review",
         "", "", TODO],
        ["Automated diagnostics", "Set up the AccuKnox diagnostics suite, RINC",
         "", "", TODO],
        ["Cluster onboarding", "KubeArmor eBPF runtime and Robin daemonset",
         "", "", TODO],
        ["Fault tolerance and DB HA", "RTO and RPO review, PostgreSQL cluster specs",
         "", "", TODO],
        ["UAT security validation", "Run the customer test plan, generate reports",
         "", "", TODO],
    ],
    top=1.80, height=3.42, bsize=8.0, ssize=7.0,
    head_h=0.32, row_h=0.345, pad=0.03,
    note="Owners and dates for the open items follow the deployment readiness gate.")


# ================================================================== 4. closing
closing_slide(prs)


prs.save(OUT)
print("wrote", os.path.abspath(OUT), "slides:", len(prs.slides._sldIdLst))
