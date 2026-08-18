# -*- coding: utf-8 -*-
"""
Azure Cloud Security and AI Security Posture Report, AccuKnox branded.

Rebuilds the source draft ("Indigo PoC _ Draft.pptx", a Google Slides export at
13.33 x 7.5 in) on the AccuKnox master template at 10 x 5.625 in. Every data point
from the source deck is kept. The source deck holds no pictures and no charts, so
every visual here is a native PowerPoint shape, table or text box, all editable.

Changes on top of the source:
  - AccuKnox master layouts, palette, logo and Space Grotesk throughout.
  - Two part dividers, so the CSPM report and the AI report read as one deck.
  - The rainbow bar palette is replaced with the brand ramp. Blue for volume,
    red for High-severity, green for good news.
  - Slide 23 of the source repeated the same four-step chain on all four cards.
    The chain now appears once, at the top of the slide.
  - Em dashes, pipes in headings and semicolons are rewritten as plain sentences.
  - The empty last slide of the source is dropped.

Build:   py -3.11 scripts/build_indigo_azure_posture.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_Indigo_Azure_Posture_Report.pptx -Out output/render/indigo
"""
import os, shutil, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import *          # noqa: F401,F403  brand palette + shape helpers

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "PPT Template.pptx")
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_Indigo_Azure_Posture_Report.pptx")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_COVER, L_DIV, L_STD = prs.slide_layouts[0], prs.slide_layouts[2], prs.slide_layouts[4]
xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try: prs.part.drop_rel(sid.get(qn('r:id')))
    except Exception: pass
    xml_slides.remove(sid)

SRC_CSPM = "Source: Cloud Findings, active and not ignored, Azure subscription scope"
SRC_AI   = "Source: confirmed AI asset inventory, active AI findings, Azure"
SRC_TOX  = "Source: confirmed AI toxic-combination analysis, same-asset finding relationships"

# severity ramp, built only from brand hues
S_HIGH, S_MED, S_LOW, S_CRIT = RED, SECOND, GREEN, RED
BADGE = {"crit": (RED_LT, RED), "high": (LAV, PURPLE),
         "med": (GREY_BG, MUTE), "ok": (GREEN_LT, GREEN_DK)}


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


def divider(part, title, sub):
    s = prs.slides.add_slide(L_DIV); blank_footer(s)
    box(s, 0.86, 1.72, 8.3, 0.32, text=part.upper(), size=13, color=SECOND, bold=True)
    box(s, 0.82, 2.08, 8.4, 1.00, text=title, size=30, color=WHITE, bold=True,
        anchor=MSO_ANCHOR.TOP)
    box(s, 0.86, 3.18, 0.12, 0.62, fill=PRIMARY)
    box(s, 1.10, 3.16, 7.9, 0.66, text=sub, size=12.5, color=NAVY_TXT,
        anchor=MSO_ANCHOR.MIDDLE)
    return s


def panel(s, x, y, w, h, head=None, fill=WHITE, line=GREY_BD):
    """White rounded card. Returns the y where content should start."""
    box(s, x, y, w, h, fill=fill, line=line, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
    if head:
        box(s, x + 0.20, y + 0.09, w - 0.40, 0.24, text=head.upper(), size=8.0,
            color=GREY_TX, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        return y + 0.38
    return y + 0.14


def metric(s, x, y, w, value, label, sub=None, accent=PRIMARY, vsize=17, h=0.94):
    box(s, x, y, w, h, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, x + 0.10, y + 0.13, 0.055, h - 0.26, fill=accent)
    box(s, x + 0.24, y + 0.07, w - 0.34, 0.38, text=value, size=vsize, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0)
    box(s, x + 0.24, y + 0.45, w - 0.32, 0.22, text=label.upper(), size=6.6,
        color=NAVY, bold=True, anchor=MSO_ANCHOR.TOP, ml=0)
    if sub:
        box(s, x + 0.24, y + 0.65, w - 0.32, h - 0.70, text=sub, size=6.5,
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


def bar_row(s, x, y, w, label, value, maxv, color=PRIMARY, lw=1.55, vw=0.60,
            h=0.28, lsize=8.2, bar_h=0.115):
    """Label on the left, track and bar in the middle, value on the right."""
    box(s, x, y, lw, h, text=label, size=lsize, color=NAVY,
        anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0.04)
    tx = x + lw + 0.08
    tw = w - lw - vw - 0.16
    ty = y + (h - bar_h) / 2
    box(s, tx, ty, tw, bar_h, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    frac = 0.0 if maxv <= 0 else value / float(maxv)
    box(s, tx, ty, max(tw * frac, 0.07), bar_h, fill=color,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    box(s, x + w - vw, y, vw, h, text="{:,}".format(value), size=8.2, color=NAVY,
        bold=True, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE,
        ml=0, mr=0, wrap=False)


def bar_wide(s, x, y, w, label, value, maxv, color=RED, lsize=8.2, vw=0.72,
             bar_h=0.115, note=None):
    """Long label above the bar, for names that will not fit a left column."""
    box(s, x, y, w - vw, 0.20, text=label, size=lsize, color=NAVY,
        anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0.04)
    box(s, x + w - vw, y, vw, 0.20, text=note or "{:,}".format(value), size=8.2,
        color=NAVY, bold=True, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE,
        ml=0, mr=0, wrap=False)
    ty = y + 0.21
    box(s, x, ty, w, bar_h, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    frac = 0.0 if maxv <= 0 else value / float(maxv)
    box(s, x, ty, max(w * frac, 0.07), bar_h, fill=color,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)


def stackbar(s, x, y, w, h, segs, legend_y=None, lsize=8.2):
    """segs = [(label, value, color)]. Draws one stacked bar plus a dot legend."""
    total = float(sum(v for _, v, _ in segs))
    cx = x
    for lab, v, col in segs:
        sw = w * v / total
        box(s, cx, y, sw, h, fill=col)
        cx += sw
    if legend_y is not None:
        step = w / len(segs)
        for i, (lab, v, col) in enumerate(segs):
            dot(s, x + i * step, legend_y + 0.055, 0.10, col)
            box(s, x + i * step + 0.16, legend_y, step - 0.20, 0.22,
                text="{} {:,}".format(lab, v), size=lsize, color=NAVY,
                anchor=MSO_ANCHOR.MIDDLE, ml=0)


def note(s, x, y, w, h, head, body, accent=PRIMARY, tint=GREY_BG,
         hsize=9.0, bsize=7.6):
    box(s, x, y, w, h, fill=tint, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    dot(s, x + 0.17, y + 0.145, 0.11, accent)
    box(s, x + 0.38, y + 0.04, w - 0.54, 0.26, text=head, size=hsize, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.38, y + 0.28, w - 0.54, h - 0.33, text=body, size=bsize,
        color=MUTE, anchor=MSO_ANCHOR.TOP, ml=0)


def stackrow(s, x, y, w, h, key, val, accent=PRIMARY, ksize=8.6, vsize=7.4,
             tint=None):
    """Bold key above a muted value, with a left accent bar."""
    if tint:
        box(s, x, y, w, h, fill=tint, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
    box(s, x + 0.05, y + 0.03, 0.05, h - 0.06, fill=accent)
    b = box(s, x + 0.20, y + 0.01, w - 0.28, h - 0.02, anchor=MSO_ANCHOR.MIDDLE,
            ml=0, mr=0.02)
    para(b, key, size=ksize, color=NAVY, bold=True, first=True, space_after=1)
    para(b, val, size=vsize, color=MUTE, space_after=0)


def badge(s, x, y, w, h, text, kind="crit", size=7.0):
    f, c = BADGE[kind]
    return pill(s, x, y, w, h, text, fill=f, tcolor=c, size=size, bold=True)


def chainbox(s, x, y, w, h, head, sub, accent=RED, tint=RED_LT, hsize=8.6,
             ssize=7.0):
    box(s, x, y, w, h, fill=tint, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, y + 0.03, 0.055, h - 0.06, fill=accent)
    b = box(s, x + 0.16, y + 0.03, w - 0.24, h - 0.06, anchor=MSO_ANCHOR.MIDDLE,
            ml=0, mr=0.02)
    para(b, head, size=hsize, color=NAVY, bold=True, first=True, space_after=1)
    para(b, sub, size=ssize, color=MUTE, space_after=0)


def chain(s, x, y, w, h, steps, gap=0.30, tail=None, tail_kind="crit"):
    """steps = [(head, sub, accent, tint)]. Arrows are drawn between boxes."""
    tw = 0.92 if tail else 0.0
    n = len(steps)
    bw = (w - gap * (n - 1) - (tw + 0.24 if tail else 0)) / n
    cx = x
    for i, (head, sub, accent, tint) in enumerate(steps):
        chainbox(s, cx, y, bw, h, head, sub, accent=accent, tint=tint)
        cx += bw
        if i < n - 1:
            arrow(s, cx + (gap - 0.26) / 2, y + (h - 0.26) / 2, color=accent)
            cx += gap
    if tail:
        badge(s, cx + 0.24, y + (h - 0.26) / 2, tw, 0.26, tail, kind=tail_kind)


def zero_tile(s, x, y, w, h, value, label, color=GREEN_DK, fill=GREEN_LT):
    b = box(s, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
            radius=0.06, anchor=MSO_ANCHOR.MIDDLE)
    para(b, value, size=16, color=color, bold=True, align=PP_ALIGN.CENTER,
         first=True, space_after=1)
    para(b, label, size=7.0, color=MUTE, align=PP_ALIGN.CENTER, space_after=0)


def risk_col(t, ci, size=7.2):
    """Recolor a risk column of an _akdeck table into brand severity badges."""
    kind = {"CRITICAL": "crit", "HIGH": "high", "HIGH/CRIT": "crit",
            "MED/HIGH": "high", "MEDIUM": "med"}
    for ri in range(1, len(t.rows)):
        c = t.cell(ri, ci)
        f, col = BADGE[kind.get(c.text_frame.text.strip().upper(), "med")]
        c.fill.solid(); c.fill.fore_color.rgb = f
        for p in c.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                r.font.color.rgb = col; r.font.bold = True; r.font.size = Pt(size)


def row_heights(t, h, head=None):
    t.rows[0].height = Inches(head or h)
    for r in list(t.rows)[1:]:
        r.height = Inches(h)


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
            for r in p.runs:
                r.font.size = Pt(size)


# =================================================================== 1. COVER
# Layout 0 carries the lockup, the badge groups and the screenshots. Only the
# title and the three scope numbers belong here. The assessment basis moves to
# the first content slide.
cover_slide(prs, "Azure Cloud Security\nand AI Posture Report", scope=[
    ("30", "Azure subscriptions"),
    ("11,221", "Cloud assets"),
    ("31,439", "Active findings")])

# =================================================================== 2. DIVIDER
divider("Part 1", "Cloud Security Posture Management",
        "30 Azure subscriptions, 11,221 assets and 31,439 active findings, "
        "read through exposure and attack paths.")

# =================================================================== 3. EXEC
s = std("Executive Risk Snapshot", "Posture volume, exposure and compound risk",
        "A short view of where the confirmed Azure footprint carries risk today.",
        SRC_CSPM)
metrics(s, 1.48, [
    ("31,439", "Active CSPM findings", "Across 30 subscriptions", PRIMARY),
    ("10,144", "High findings", "32.3% of total", S_HIGH),
    ("412", "Internet exposure", "Confirmed High findings", S_HIGH),
    ("5", "Toxic combinations", "High-confidence paths", PURPLE),
    ("0", "Critical findings", "None returned by CSPM", GREEN)])
cy = panel(s, CX, 2.60, 4.50, 2.48, "Finding severity distribution")
stackbar(s, 0.62, cy + 0.04, 4.06, 0.20,
         [("High", 10144, S_HIGH), ("Medium", 13353, S_MED), ("Low", 7942, S_LOW)],
         legend_y=cy + 0.32)
box(s, 0.62, cy + 0.66, 2.0, 0.46, text="74.7%", size=25, color=PRIMARY, bold=True,
    anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0)
box(s, 0.62, cy + 1.12, 4.06, 0.26,
    text="of active findings are Medium or High severity", size=8.6, color=NAVY, ml=0)
box(s, 0.62, cy + 1.44, 4.06, 0.56,
    text="The estate needs broad risk reduction. Drive remediation by "
         "exploitability and attack paths rather than raw finding volume.",
    size=8.6, color=MUTE, ml=0)
cy = panel(s, 5.10, 2.60, 4.50, 2.48, "Priority risk signals")
note(s, 5.28, cy + 0.02, 4.14, 0.64, "External attack surface",
     "412 confirmed Internet-exposed workloads, plus Internet-open management "
     "protocols.", accent=RED, tint=RED_LT)
note(s, 5.28, cy + 0.70, 4.14, 0.64, "Data protection concentration",
     "Storage and block storage dominate High finding volume. Several controls "
     "affect public access and encryption.", accent=PRIMARY, tint=GREY_BG)
note(s, 5.28, cy + 1.38, 4.14, 0.64, "Identity and trust blast radius",
     "Confirmed toxic paths involve domain-controller and Root CA systems "
     "exposed through permissive NSGs.", accent=PURPLE, tint=LAV)

# =================================================================== 4. ASSETS
s = std("Azure Asset Footprint", "What the assessment covered",
        "The estate is dominated by network, compute and block-storage assets, "
        "the primary security control surface.", SRC_CSPM)
cy = panel(s, CX, 1.48, 5.20, 3.60, "Important asset distribution")
ASSETS = [("Networking", 3385), ("Compute", 2325), ("Block Storage", 2219),
          ("Resource Management", 903), ("Host", 710), ("Object Storage", 264),
          ("Serverless", 249), ("Key management", 169), ("Database", 106),
          ("AI + Machine Learning", 34)]
for i, (lab, v) in enumerate(ASSETS):
    bar_row(s, 0.60, cy + 0.02 + i * 0.315, 4.80, lab, v, 3385,
            color=PRIMARY if i < 3 else (SECOND if i < 6 else PURPLE), lw=1.50)
b = box(s, 5.78, 1.48, 3.82, 0.82, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, anchor=MSO_ANCHOR.MIDDLE)
para(b, "11,221", size=26, color=PRIMARY, bold=True, align=PP_ALIGN.CENTER,
     first=True, space_after=1)
para(b, "TOTAL CONFIRMED AZURE ASSETS", size=7.6, color=MUTE,
     align=PP_ALIGN.CENTER, space_after=0)
note(s, 5.78, 2.42, 3.82, 0.68, "Network plane",
     "3,385 networking assets make connectivity, segmentation and logging a "
     "major attack-surface concern.", accent=PRIMARY, tint=GREY_BG)
note(s, 5.78, 3.16, 3.82, 0.68, "Workload plane",
     "Compute and host assets represent 3,035 workloads where exposure and "
     "hardening drive exploitability.", accent=SECOND, tint=LAV)
note(s, 5.78, 3.90, 3.82, 0.68, "Data plane",
     "2,483 block and object storage assets create concentrated public-access "
     "and encryption risk.", accent=PURPLE, tint=LAV)
box(s, 5.78, 4.64, 3.82, 0.42,
    text="Coverage note: IAM and Cloud Account categories returned 0 assets in "
         "the queried distribution, despite account-level CSPM findings.",
    size=7.0, color=GREY_TX, italic=True, ml=0)

# =================================================================== 5. SEVERITY
s = std("Severity and Risk Concentration", "Where the High findings sit",
        "High findings concentrate in storage and compute controls, which gives "
        "a narrow remediation surface with broad impact.", SRC_CSPM)
cy = panel(s, CX, 1.48, 3.55, 3.60, "Severity volume")
for i, (lab, v, col) in enumerate([("High", 10144, S_HIGH),
                                   ("Medium", 13353, S_MED),
                                   ("Low", 7942, S_LOW)]):
    bar_row(s, 0.58, cy + 0.04 + i * 0.34, 3.20, lab, v, 13353, color=col,
            lw=0.85, vw=0.70)
box(s, 0.58, cy + 1.14, 3.20, 0.30, fill=GREEN_LT,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
box(s, 0.72, cy + 1.14, 3.00, 0.30, text="0 confirmed Critical findings",
    size=8.4, color=GREEN_DK, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
note(s, 0.58, cy + 1.56, 3.20, 1.50, "Compound-risk override",
     "Severity alone understates risk. Confirmed toxic combinations raise "
     "several High controls to Critical remediation priority.",
     accent=PURPLE, tint=LAV, bsize=8.0)
cy = panel(s, 4.20, 1.48, 5.40, 3.60, "High findings by asset category")
HIGHCAT = [("Block Storage", 4247), ("Compute", 3672), ("Object Storage", 1258),
           ("Host", 761), ("Networking", 83), ("AI + Machine Learning", 51),
           ("Key management", 31), ("Database", 22)]
for i, (lab, v) in enumerate(HIGHCAT):
    bar_row(s, 4.40, cy + 0.02 + i * 0.26, 5.00, lab, v, 4247, color=S_HIGH,
            lw=1.55, vw=0.62)
box(s, 4.40, cy + 2.14, 1.30, 0.42, text="90.5%", size=22, color=S_HIGH,
    bold=True, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0)
box(s, 5.72, cy + 2.14, 3.68, 0.42,
    text="of all High findings sit in Block Storage, Compute and Object Storage.",
    size=8.4, color=NAVY, anchor=MSO_ANCHOR.MIDDLE, ml=0)
note(s, 4.40, cy + 2.60, 5.00, 0.58, "Technical interpretation",
     "Fix the systemic controls first: private access by default, encryption at "
     "host, BYOK and CMK, and exposure guardrails. Do policy cleanup after.",
     accent=PRIMARY, tint=GREY_BG, bsize=7.8)

# =================================================================== 6. TOP HIGH
s = std("Highest-Volume High Findings", "The controls behind the volume",
        "The top controls point to data-protection and exposure weaknesses, "
        "followed by compute hardening gaps.", SRC_CSPM)
cy = panel(s, CX, 1.48, 5.30, 3.60, "Top High findings")
TOPHIGH = [("VM Disk Snapshot Public Access Disabled", 3413),
           ("VM Disk Public Access", 1778),
           ("Attached Disk Volumes BYOK Encryption Enabled", 1773),
           ("Blob Container CMK Encrypted", 1064),
           ("Internet Exposure", 384),
           ("VM Encryption At Host", 316),
           ("Premium SSD Disabled", 234),
           ("OpenAI Account CMK Encrypted", 39)]
for i, (lab, v) in enumerate(TOPHIGH):
    bar_wide(s, 0.60, cy + 0.02 + i * 0.395, 4.80, lab, v, 3413,
             color=S_HIGH if i != 4 else RED)
cy = panel(s, 5.88, 1.48, 3.72, 3.60, "Technical interpretation")
for i, (h, b, acc, tn) in enumerate([
        ("Storage exposure",
         "Disk and snapshot controls are the largest single source of High "
         "findings. Fix them as a platform baseline.", RED, RED_LT),
        ("Encryption posture",
         "BYOK and CMK controls show real gaps across block and object storage, "
         "which affects data governance.", PRIMARY, GREY_BG),
        ("Internet reachability",
         "Internet Exposure is lower volume but far higher exploitability. It "
         "must override volume-based ranking.", RED, RED_LT),
        ("AI data controls",
         "OpenAI and ML workspaces also show CMK and logging gaps, which "
         "creates governance risk for AI workloads.", PURPLE, LAV)]):
    note(s, 6.06, cy + 0.02 + i * 0.78, 3.36, 0.72, h, b, accent=acc, tint=tn)

# =================================================================== 7. EXPOSURE
s = std("External Exposure Surface", "Internet reachability and open ports",
        "Permissive NSG rules and publicly reachable administrative services "
        "amplify Internet reachability.", SRC_CSPM)
metrics(s, 1.48, [
    ("412", "Internet exposure", "Confirmed findings", RED),
    ("11", "Open all ports", "NSG rules to *", RED),
    ("24", "Open SSH", "TCP 22 to *", RED),
    ("10", "Open RDP", "TCP 3389 to *", RED),
    ("11", "Open SMB", "TCP 445 to *", RED)], h=0.86, vsize=16)
cy = panel(s, CX, 2.52, 4.60, 2.56, "Public and Internet exposure signals")
EXPO = [("VM Disk Snapshot public access", 3590), ("VM Disk Public Access", 2078),
        ("Internet Exposure", 412), ("Key Vault Public Access", 13),
        ("Public Blob Containers", 4), ("SQL Server Public Access", 1)]
for i, (lab, v) in enumerate(EXPO):
    bar_row(s, 0.58, cy + 0.02 + i * 0.30, 4.24, lab, v, 3590, color=S_HIGH,
            lw=1.90, vw=0.60, lsize=7.8)
cy = panel(s, 5.10, 2.52, 4.50, 2.56, "Control-plane gaps that raise exploitability")
for i, (h, b, acc, tn) in enumerate([
        ("Network observability",
         "956 NSG Flow Log gaps and 954 NSG Log Analytics gaps cut visibility "
         "into attacker movement and egress.", PRIMARY, GREY_BG),
        ("VNET and load-balancer logging",
         "VNET logging gaps and 124 load-balancer Log Analytics gaps reduce "
         "forensic depth for exposed services.", SECOND, LAV),
        ("Key management exposure",
         "13 public Key Vault findings, plus missing private endpoints and "
         "restrictive defaults, widen secret-store reach.", RED, RED_LT)]):
    note(s, 5.28, cy + 0.02 + i * 0.70, 4.14, 0.64, h, b, accent=acc, tint=tn)

# =================================================================== 8. EXPOSED
s = std("High-Risk Publicly Exposed Assets", "Confirmed asset to network relationships",
        "These systems are where exposure carries immediate attack-path meaning.",
        SRC_CSPM)
ROWS = [["ASSET", "TYPE", "CONFIRMED EXPOSURE AND RELATIONSHIP", "RISK"],
        ["ZPW-IGA-DC01", "Azure VM",
         "Internet-exposed via NSG ZPWIGADC01nsg882. The related NSG has all ports open to *", "CRITICAL"],
        ["ZPW-IGA-DC02", "Azure VM",
         "Internet-exposed via NSG ZPW-IGA-DC02-nsg. All ports open to *", "CRITICAL"],
        ["ZPW-DEV-DC01", "Azure VM",
         "Internet-exposed via ZPW-DEV-DC01-NSG. All ports open to *", "CRITICAL"],
        ["IGROOTCA", "Azure VM",
         "Internet-exposed via IGROOTCA-NSG. SMB TCP 445 open to *", "CRITICAL"],
        ["AzureCloud-OpenShiftBastionHost", "Azure VM",
         "Internet-exposed. RDP TCP 3389 open to *", "HIGH/CRIT"],
        ["ocpintprdclu2-kgz68-master-2", "Azure VM",
         "Internet-exposed through public load balancer ocpintprdclu2-kgz68", "HIGH"],
        ["ZPW-MFT-PGWS01", "Azure VM", "Internet-exposed. RDP and SSH open to *", "HIGH"],
        ["ZPW-MFT-PGWS02", "Azure VM", "Internet-exposed. RDP and SSH open to *", "HIGH"],
        ["medical-records", "Storage", "Public blob access and no CMK encryption", "CRITICAL"],
        ["KEYVAULT-CIAM-PRD", "Key Vault",
         "Public access, no private endpoint, default network allows all networks", "CRITICAL"]]
t = table(s, CX, 1.50, CW, 3.52, ROWS, colw=[2.30, 0.95, 4.90, 1.05],
          hsize=8.0, bsize=7.4)
row_heights(t, 0.30, head=0.26)
risk_col(t, 3)
table_grid(t)

# =================================================================== 9. TOXIC
s = std("Toxic Combination Matrix", "Five confirmed multi-control paths",
        "Each row is a place where separate posture failures combine into "
        "materially higher risk.", SRC_CSPM)
ROWS = [["ID", "TOXIC COMBINATION", "CONFIRMED RELATIONSHIP",
         "POTENTIAL BLAST RADIUS", "RISK"],
        ["TC-01", "Internet-exposed DCs plus all ports open",
         "VM exposure names the same NSG, with all protocols and all ports open to *",
         "Identity compromise, lateral movement", "CRITICAL"],
        ["TC-02", "Internet-exposed Root CA plus SMB open",
         "IGROOTCA is exposed through IGROOTCA-NSG. TCP 445 is open to *",
         "Trust and certificate infrastructure compromise", "CRITICAL"],
        ["TC-03", "Public Key Vault plus no private endpoint",
         "The same Key Vault has public access, no private endpoint, an all-network default and a logging gap",
         "Secrets, keys and certificates", "CRITICAL"],
        ["TC-04", "Public medical-records container plus no CMK",
         "The same storage container is public and is not CMK-encrypted",
         "Sensitive data exposure and governance", "CRITICAL"],
        ["TC-05", "Internet-facing OpenShift bastion plus RDP",
         "VM exposure names the NSG. RDP 3389 is open to *. Hardening and logging gaps are present",
         "Pivot into OpenShift and internal workloads", "HIGH/CRIT"]]
t = table(s, CX, 1.50, CW, 3.50, ROWS, colw=[0.62, 2.05, 3.40, 2.13, 1.00],
          hsize=8.0, bsize=7.4)
row_heights(t, 0.62, head=0.28)
risk_col(t, 4)
table_grid(t)

# =================================================================== 10. PATHS 1
s = std("Identity and Trust Plane Attack Paths", "TC-01 and TC-02 in detail",
        "Confirmed exposure chains show how Internet reachability meets "
        "high-value identity and trust infrastructure.", SRC_CSPM)
for i, (tc, name, steps) in enumerate([
        ("TC-01", "Domain-controller attack path", [
            ("Internet", "Untrusted source", RED, RED_LT),
            ("NSG wildcard rule", "All protocols and ports to *", RED, RED_LT),
            ("DC-named Azure VM", "ZPW-IGA-DC01 and 02, ZPW-DEV-DC01", RED, RED_LT),
            ("Identity plane", "Credential and directory compromise", PURPLE, LAV)]),
        ("TC-02", "Root CA and PKI trust-path exposure", [
            ("Internet", "Untrusted source", RED, RED_LT),
            ("IGROOTCA-NSG", "SMB TCP 445 to *", RED, RED_LT),
            ("IGROOTCA", "Root CA-associated VM", RED, RED_LT),
            ("PKI and trust plane", "Certificates and signing trust", PURPLE, LAV)])]):
    y = 1.48 + i * 1.42
    panel(s, CX, y, CW, 1.30)
    badge(s, 0.58, y + 0.14, 0.62, 0.24, tc, kind="high", size=7.6)
    box(s, 1.30, y + 0.12, 5.0, 0.28, text=name, size=10.5, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
    chain(s, 0.58, y + 0.48, 8.84, 0.70, steps, gap=0.26, tail="CRITICAL")
note(s, CX, 4.36, CW, 0.72, "Security implication",
     "The network path is explicitly confirmed to the named high-value systems, "
     "which raises blast radius. Treat these as connected exposures rather than "
     "isolated misconfigurations.", accent=RED, tint=RED_LT, bsize=8.2)

# =================================================================== 11. PATHS 2
s = std("Secrets and Sensitive Data Attack Paths", "TC-03 and TC-04 in detail",
        "Public service endpoints combine with weak network isolation, "
        "encryption or logging controls.", SRC_CSPM)
for i, (tc, name, kind, rows, impact) in enumerate([
        ("TC-03", "KEYVAULT-CIAM-PRD", "Key Vault", [
            ("Public Key Vault endpoint", "Secrets, keys and certificates"),
            ("No private endpoint", "No private-only service path"),
            ("Default access is all networks", "Broad network reachability"),
            ("Logging gap", "Key Vault Log Analytics is not enabled")],
         "Reduced detection, plus secret exposure risk"),
        ("TC-04", "medical-records", "Storage container", [
            ("Public blob container", "Reachable object data named medical-records"),
            ("No CMK control", "Customer-managed key is absent"),
            ("Sensitive-data context", "Asset naming implies high sensitivity"),
            ("Public exposure", "Internet-accessible object data")],
         "Data exposure, plus weaker key governance")]):
    x = 0.40 + i * 4.70
    panel(s, x, 1.48, 4.50, 3.10)
    badge(s, x + 0.18, 1.62, 0.62, 0.24, tc, kind="high", size=7.6)
    box(s, x + 0.90, 1.60, 2.60, 0.28, text=name, size=11, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
    badge(s, x + 3.48, 1.62, 0.84, 0.24, "CRITICAL", kind="crit")
    box(s, x + 0.18, 1.88, 4.14, 0.22, text=kind.upper(), size=7.2, color=GREY_TX,
        bold=True, ml=0)
    for j, (h, b) in enumerate(rows):
        stackrow(s, x + 0.18, 2.16 + j * 0.52, 4.14, 0.48, h, b,
                 accent=RED if j == 0 else PRIMARY,
                 tint=RED_LT if j == 0 else GREY_BG)
    box(s, x + 0.18, 4.28, 4.14, 0.24, text="Potential impact: " + impact,
        size=7.6, color=RED, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)

# =================================================================== 12. CONCENTRATION
s = std("Risk Concentration by Subscription and Region", "Where to send the effort",
        "A small subset of subscriptions, and Central India, account for most of "
        "the observed CSPM risk.", SRC_CSPM)
cy = panel(s, CX, 1.48, 4.50, 2.66, "Top subscriptions by High findings")
SUBS = [("9bc57f1e...154a48", 2782), ("732df2de...febec5", 1183),
        ("f6941c4a...be380", 952), ("26da838f...1d873", 793),
        ("d2ac0e93...9576d3", 693)]
for i, (lab, v) in enumerate(SUBS):
    bar_row(s, 0.58, cy + 0.04 + i * 0.33, 4.14, lab, v, 2782, color=S_HIGH,
            lw=1.45, vw=0.62, lsize=8.0)
box(s, 0.58, cy + 1.76, 4.14, 0.30,
    text="Top account: 2,782 High findings and 7,065 total active findings.",
    size=8.0, color=MUTE, italic=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
cy = panel(s, 5.10, 1.48, 4.50, 2.66, "Findings by region")
REG = [("centralindia", 27526), ("southindia", 3035), ("global", 367),
       ("eastus", 220), ("eastus2", 126), ("swedencentral", 81)]
for i, (lab, v) in enumerate(REG):
    bar_row(s, 5.28, cy + 0.02 + i * 0.30, 4.14, lab, v, 27526, color=PRIMARY,
            lw=1.30, vw=0.72, lsize=8.0)
note(s, CX, 4.24, CW, 0.84, "Regional hotspot and ranking rule",
     "Central India carries 27,526 total findings and 9,105 High findings, which "
     "makes it the primary remediation domain. Pair account volume with "
     "toxic-combination context. A lower-volume account can still outrank a "
     "larger one when it holds exposed crown-jewel assets.",
     accent=PRIMARY, tint=GREY_BG, bsize=8.2)

# =================================================================== 13. COMPLIANCE
s = std("Compliance Impact and Remediation Priorities", "Failed mappings and the plan",
        "Failed framework mappings show the control themes. Remediation is ranked "
        "by attack-path impact rather than mapping volume.", SRC_CSPM)
cy = panel(s, CX, 1.48, 4.30, 3.60, "Top failed compliance mappings")
COMP = [("DPDP Act India + RBI CSF", 6264), ("RBI IT Framework + RBI CSF", 4062),
        ("Azure CIS v3.0 + RBI CSF", 2290), ("Azure CIS v3.0 + CIS v2.0.0", 2073),
        ("DPDP Act India", 1319), ("DPDP + Azure CIS v3.0 + RBI CSF", 1272)]
for i, (lab, v) in enumerate(COMP):
    bar_wide(s, 0.58, cy + 0.02 + i * 0.44, 3.94, lab, v, 6264, color=PURPLE)
box(s, 0.58, cy + 2.70, 3.94, 0.42,
    text="Note: compliance data represents failed finding and control mappings. "
         "It is not a complete pass percentage.",
    size=7.4, color=GREY_TX, italic=True, ml=0)
cy = panel(s, 5.00, 1.48, 4.60, 3.60, "Prioritized remediation plan")
PLAN = [("P0", "Break confirmed attack paths",
         "Restrict NSGs to approved sources and ports. Remove public access from "
         "the DC, Root CA, Key Vault and storage paths.", RED),
        ("P1", "Reduce external exposure",
         "Remove unnecessary public IP and service exposure. Close RDP, SSH and "
         "SMB. Enforce private endpoints and restrictive defaults.", PRIMARY),
        ("P1", "Close data-protection gaps",
         "Enforce CMK and BYOK where required, disk encryption at host, and "
         "private storage access.", PRIMARY),
        ("P2", "Restore observability",
         "Enable NSG, VNET, load-balancer and Key Vault diagnostics, with central "
         "Log Analytics integration.", SECOND),
        ("P2", "Baseline identity controls",
         "Enable managed identities where applicable. Standardize "
         "identity-centric workload hardening.", SECOND)]
for i, (p, h, b, acc) in enumerate(PLAN):
    y = cy + 0.02 + i * 0.63
    pill(s, 5.18, y + 0.10, 0.46, 0.24, p, fill=acc, tcolor=WHITE, size=7.6)
    box(s, 5.74, y + 0.04, 3.66, 0.24, text=h, size=9.2, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, 5.74, y + 0.27, 3.66, 0.34, text=b, size=7.6, color=MUTE, ml=0)

# =================================================================== 14. BOUNDARIES
s = std("Data Confidence and Assessment Boundaries", "Evidence versus gaps",
        "The report separates confirmed evidence from context that was not "
        "available or not validated.", SRC_CSPM)
cy = panel(s, CX, 1.48, 4.50, 2.86, "Evidence used")
EV = [("Cloud provider", "Azure"), ("Source", "Cloud Findings"),
      ("Filters", "Active, not ignored, azure_subscription"),
      ("Confirmed Azure accounts", "30 with active findings"),
      ("Toxic-combination rule",
       "Same asset or finding explicitly naming the related NSG or load balancer")]
for i, (k, v) in enumerate(EV):
    stackrow(s, 0.58, cy + 0.02 + i * 0.48, 4.14, 0.44, k, v, accent=GREEN,
             tint=GREEN_LT)
cy = panel(s, 5.10, 1.48, 4.50, 2.86, "Not confidently available or validated")
NA = [("Public IP addresses", "Not returned in the queried CSPM fields"),
      ("Excessive IAM and privilege escalation", "No confirmed Azure findings retrieved"),
      ("Secret-scan and container-secret findings", "No active Azure findings in the queried data"),
      ("Total onboarded Azure subscriptions",
       "36 filter values exist. Only 30 carry confirmed active CSPM findings"),
      ("Compliance score", "Mappings available. No complete pass or fail percentage returned")]
for i, (k, v) in enumerate(NA):
    stackrow(s, 5.28, cy + 0.02 + i * 0.48, 4.14, 0.44, k, v, accent=RED,
             tint=RED_LT)
note(s, CX, 4.44, CW, 0.64, "Reporting principle",
     "Only confirmed evidence supports the attack-path assertions. Missing "
     "context is surfaced rather than inferred.",
     accent=PRIMARY, tint=GREY_BG, bsize=8.2)

# =================================================================== 15. AI COVER
s = prs.slides.add_slide(L_DIV); blank_footer(s)
box(s, 0.70, 0.86, 8.6, 0.30, text="PART 2  ·  AI AND ML SECURITY POSTURE",
    size=12, color=SECOND, bold=True)
box(s, 0.70, 1.20, 0.12, 0.50, fill=PRIMARY)
box(s, 0.94, 1.18, 4.8, 1.10, text="Azure AI Security\nPosture Report", size=30,
    color=WHITE, bold=True, anchor=MSO_ANCHOR.TOP)
box(s, 0.70, 2.42, 4.9, 0.62,
    text="AI asset inventory, exposure, security findings and reporting "
         "confidence across the confirmed Azure AI and ML estate.",
    size=11.5, color=NAVY_TXT)
box(s, 0.70, 3.18, 3.0, 0.24, text="CONFIRMED SCOPE", size=9.5, color=SECOND,
    bold=True, anchor=MSO_ANCHOR.MIDDLE)
for i, (num, l1, l2) in enumerate([
        ("34", "AI and ML assets", "Inventory-confirmed"),
        ("164", "Active AI findings", "Across 34 assets"),
        ("24", "Public network access", "Confirmed endpoints")]):
    cx = 0.70 + i * 1.72
    box(s, cx, 3.48, 1.62, 0.42, text=num, size=23, color=WHITE, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0)
    box(s, cx, 3.92, 1.62, 0.44, text=l1 + "\n" + l2, size=8, color=NAVY_TXT,
        anchor=MSO_ANCHOR.TOP, ml=0)
box(s, 5.86, 1.16, 3.44, 3.24, fill=NAVY_DK, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
    radius=0.05)
box(s, 6.06, 1.30, 3.04, 0.24, text="AI POSTURE SIGNAL SUMMARY", size=8,
    color=SECOND, bold=True, anchor=MSO_ANCHOR.MIDDLE)
for i, (num, lab, sub, col) in enumerate([
        ("24", "Exposure", "Assets with public network access", RED),
        ("51", "Severity", "High-severity AI findings", RED),
        ("41", "Data", "Data-security findings", PRIMARY),
        ("2", "Platform", "Azure ML and Databricks", SECOND)]):
    y = 1.62 + i * 0.68
    box(s, 6.06, y, 0.055, 0.56, fill=col)
    box(s, 6.24, y, 0.78, 0.56, text=num, size=18, color=WHITE, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0)
    b = box(s, 7.02, y, 2.10, 0.56, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    para(b, lab, size=9.5, color=WHITE, bold=True, first=True, space_after=1)
    para(b, sub, size=7.4, color=NAVY_TXT, space_after=0)
box(s, 0.70, 4.56, 8.6, 0.30,
    text="Assessment basis: confirmed AI asset inventory, active findings, and no "
         "unvalidated account-level asset counts",
    size=8, color=GREY_TX, italic=True, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 16. AI EXEC
s = std("Executive AI Risk Snapshot", "AI volume, severity and exposure",
        "A short view of the confirmed Azure AI and ML footprint.", SRC_AI)
metrics(s, 1.48, [
    ("34", "Active AI assets", "34 of 34 have active findings", PRIMARY),
    ("27", "Assets with High findings", "79.4% of the AI estate", S_HIGH),
    ("24", "Public network access", "70.6% of the AI estate", S_HIGH),
    ("2", "AI platform types", "Azure ML and Databricks", SECOND),
    ("0", "Critical findings", "None confirmed", GREEN)])
cy = panel(s, CX, 2.60, 4.50, 2.48, "Finding severity distribution")
stackbar(s, 0.62, cy + 0.04, 4.06, 0.20,
         [("High", 51, S_HIGH), ("Medium", 96, S_MED), ("Low", 17, S_LOW)],
         legend_y=cy + 0.32)
box(s, 0.62, cy + 0.66, 2.0, 0.46, text="89.6%", size=25, color=PRIMARY, bold=True,
    anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0)
box(s, 0.62, cy + 1.12, 4.06, 0.26,
    text="of AI findings are Medium or High severity", size=8.6, color=NAVY, ml=0)
box(s, 0.62, cy + 1.44, 4.06, 0.56,
    text="Risk concentrates in Azure Machine Learning controls: public access, "
         "customer-managed encryption, diagnostics and monitoring.",
    size=8.6, color=MUTE, ml=0)
cy = panel(s, 5.10, 2.60, 4.50, 2.48, "Priority risk signals")
note(s, 5.28, cy + 0.02, 4.14, 0.64, "Public network exposure",
     "24 AI assets have public network access enabled. No separate Internet "
     "Exposure finding was returned.", accent=RED, tint=RED_LT)
note(s, 5.28, cy + 0.70, 4.14, 0.64, "Data protection concentration",
     "All 34 assets carry data-security findings. 41 data-security findings were "
     "confirmed across the AI estate.", accent=PRIMARY, tint=GREY_BG)
note(s, 5.28, cy + 1.38, 4.14, 0.64, "Platform concentration",
     "27 of 34 assets are Azure Machine Learning workspaces, and all 27 carry "
     "High-severity findings.", accent=PURPLE, tint=LAV)

# =================================================================== 17. AI ASSETS
s = std("AI Asset Footprint", "Platform and region spread",
        "The confirmed AI estate is entirely Azure. It concentrates in Machine "
        "Learning workspaces deployed mainly in southindia.", SRC_AI)
cy = panel(s, CX, 1.48, 5.20, 1.42, "AI service and platform distribution")
for i, (lab, v, pct) in enumerate([("Azure Machine Learning Workspace", 27, "79.4%"),
                                   ("Azure Databricks Workspace", 7, "20.6%")]):
    bar_row(s, 0.60, cy + 0.06 + i * 0.42, 4.20, lab, v, 27,
            color=PRIMARY if i == 0 else SECOND, lw=2.35, vw=0.44)
    box(s, 4.90, cy + 0.06 + i * 0.42, 0.60, 0.28, text=pct, size=7.6,
        color=GREY_TX, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
cy = panel(s, CX, 3.00, 5.20, 2.08, "Regional asset distribution")
for i, (lab, v, pct) in enumerate([("southindia", 22, "64.7%"),
                                   ("centralindia", 10, "29.4%"),
                                   ("eastus2", 2, "5.9%")]):
    bar_row(s, 0.60, cy + 0.06 + i * 0.36, 4.20, lab, v, 22, color=PRIMARY,
            lw=1.40, vw=0.44)
    box(s, 4.90, cy + 0.06 + i * 0.36, 0.60, 0.28, text=pct, size=7.6,
        color=GREY_TX, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
box(s, 0.60, cy + 1.20, 4.80, 0.42,
    text="Coverage note: unique AI asset counts by account, subscription or "
         "project were absent from the inventory output. They are not inferred here.",
    size=7.2, color=GREY_TX, italic=True, ml=0)
b = box(s, 5.78, 1.48, 3.82, 0.78, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, anchor=MSO_ANCHOR.MIDDLE)
para(b, "34", size=26, color=PRIMARY, bold=True, align=PP_ALIGN.CENTER,
     first=True, space_after=1)
para(b, "TOTAL CONFIRMED AI AND ML ASSETS", size=7.6, color=MUTE,
     align=PP_ALIGN.CENTER, space_after=0)
for i, (h, b2, acc, tn) in enumerate([
        ("Platform concentration",
         "79.4% of AI assets are Azure Machine Learning workspaces.", PRIMARY, GREY_BG),
        ("Regional concentration",
         "64.7% of AI assets sit in southindia.", SECOND, LAV),
        ("Finding coverage",
         "34 of 34 confirmed AI assets carry at least one active finding.",
         RED, RED_LT)]):
    note(s, 5.78, 2.40 + i * 0.90, 3.82, 0.82, h, b2, accent=acc, tint=tn,
         bsize=8.0)

# =================================================================== 18. AI SEVERITY
s = std("AI Severity and Risk Concentration", "Which controls carry the weight",
        "High-severity impact is broad across Azure ML workspaces. Medium and Low "
        "findings touch the full AI estate.", SRC_AI)
cy = panel(s, CX, 1.48, 3.40, 3.60, "Severity volume")
for i, (lab, v, col) in enumerate([("High", 51, S_HIGH), ("Medium", 96, S_MED),
                                   ("Low", 17, S_LOW)]):
    bar_row(s, 0.58, cy + 0.04 + i * 0.34, 3.06, lab, v, 96, color=col,
            lw=0.85, vw=0.52)
box(s, 0.58, cy + 1.14, 3.06, 0.30, fill=GREEN_LT,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
box(s, 0.72, cy + 1.14, 2.86, 0.30, text="0 confirmed Critical findings", size=8.4,
    color=GREEN_DK, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
note(s, 0.58, cy + 1.56, 3.06, 1.06, "Coverage interpretation",
     "High severity touches 27 unique assets. Medium and Low each touch all 34.",
     accent=PURPLE, tint=LAV, bsize=8.0)
cy = panel(s, 4.06, 1.48, 5.54, 3.60, "Top AI findings")
AIF = [("ML Workspace CMK Encrypted, southindia", 22),
       ("ML Workspace Public Access Disabled, southindia", 22),
       ("Monitor Resource SKU, southindia", 22),
       ("ML Workspace High Business Impact Enabled, southindia", 22),
       ("ML Workspace Has Tags, southindia", 16),
       ("ML Workspace Diagnostic Logs, southindia", 14),
       ("Databricks Managed Services CMK, centralindia", 7),
       ("Databricks Diagnostic Logs, centralindia", 7),
       ("Databricks Managed Disk CMK, centralindia", 7)]
for i, (lab, v) in enumerate(AIF):
    bar_wide(s, 4.26, cy + 0.00 + i * 0.305, 5.14, lab, v, 22, color=S_HIGH,
             lsize=7.8, vw=0.46, bar_h=0.095)
box(s, 4.26, cy + 2.78, 1.20, 0.36, text="89.6%", size=20, color=S_HIGH,
    bold=True, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0)
box(s, 5.50, cy + 2.78, 3.90, 0.36,
    text="of all AI findings are Medium or High severity.", size=8.2, color=NAVY,
    anchor=MSO_ANCHOR.MIDDLE, ml=0)

# =================================================================== 19. AI EXPOSURE
s = std("AI Exposure and Data Security", "Public access and control patterns",
        "Public network access is the dominant exposure signal. Data-security "
        "controls affect the whole AI estate.", SRC_AI)
metrics(s, 1.48, [
    ("24", "Public network access", "24 confirmed findings", RED),
    ("0", "Internet exposure findings", "None separately confirmed", GREEN),
    ("0", "IAM and identity findings", "None confirmed", GREEN),
    ("41", "Data-security findings", "Across 34 unique assets", PRIMARY)], h=0.90)
cy = panel(s, CX, 2.56, 4.90, 2.52, "Exposure interpretation")
for i, (h, b, acc, tn) in enumerate([
        ("Public endpoint enabled",
         "24 unique AI assets have public network access enabled, based on "
         "confirmed ML Workspace findings.", RED, RED_LT),
        ("Public access is not Internet Exposure",
         "No AI-specific finding named Internet Exposure was returned. Public "
         "network reachability is reported on its own.", PRIMARY, GREY_BG),
        ("Identity scope boundary",
         "No confirmed AI IAM or identity posture findings came back from the "
         "available dataset.", PURPLE, LAV)]):
    note(s, 0.58, cy + 0.02 + i * 0.70, 4.54, 0.64, h, b, accent=acc, tint=tn)
cy = panel(s, 5.50, 2.56, 4.10, 2.52, "Data security control patterns")
for i, (lab, v) in enumerate([("ML Workspace CMK encryption", 22),
                              ("Databricks Managed Services CMK", 7),
                              ("Databricks Managed Disk CMK", 7),
                              ("Diagnostic logging and monitoring", 21)]):
    bar_wide(s, 5.68, cy + 0.02 + i * 0.36, 3.74, lab, v, 22, color=PRIMARY,
             lsize=7.8, vw=0.42, bar_h=0.10)
box(s, 5.68, cy + 1.52, 3.74, 0.56, fill=GREY_BG,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, 5.84, cy + 1.52, 0.70, 0.56, text="34", size=20, color=PRIMARY, bold=True,
    anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0)
box(s, 6.56, cy + 1.52, 2.72, 0.56,
    text="unique AI assets carry data-security findings", size=8.2, color=NAVY,
    anchor=MSO_ANCHOR.MIDDLE, ml=0)

# =================================================================== 20. PLATFORM
s = std("AI Platform Risk Profile", "Azure ML against Databricks",
        "Azure Machine Learning is most of the AI estate and carries the whole "
        "confirmed High-affected asset population.", SRC_AI)
cy = panel(s, CX, 1.48, 4.60, 2.86, "Platform posture comparison")
for i, (name, acc, vals) in enumerate([
        ("Azure Machine Learning Workspace", PRIMARY,
         [("27", "Unique assets"), ("141", "Total findings"), ("27", "High-affected")]),
        ("Azure Databricks Workspace", SECOND,
         [("7", "Unique assets"), ("23", "Total findings"), ("0", "High-affected")])]):
    y = cy + 0.02 + i * 1.20
    box(s, 0.58, y, 0.055, 0.26, fill=acc)
    box(s, 0.74, y - 0.02, 3.98, 0.30, text=name, size=10, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
    for j, (num, lab) in enumerate(vals):
        bx = 0.58 + j * 1.42
        b = box(s, bx, y + 0.32, 1.32, 0.66, fill=GREY_BG,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06,
                anchor=MSO_ANCHOR.MIDDLE)
        para(b, num, size=16, color=acc, bold=True, align=PP_ALIGN.CENTER,
             first=True, space_after=1)
        para(b, lab, size=7.0, color=MUTE, align=PP_ALIGN.CENTER, space_after=0)
box(s, 0.58, cy + 2.20, 4.24, 0.24,
    text="Estate split: Azure ML is 79.4% of assets, Databricks is 20.6%.",
    size=8.0, color=MUTE, italic=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
cy = panel(s, 5.10, 1.48, 4.50, 2.86, "Security-domain coverage")
DOM = [("Public and network exposure", 24), ("Data-security affected assets", 34),
       ("High-affected AI assets", 27), ("Medium-affected AI assets", 34),
       ("Low-affected AI assets", 34), ("IAM and identity affected assets", 0)]
for i, (lab, v) in enumerate(DOM):
    bar_row(s, 5.28, cy + 0.02 + i * 0.38, 4.14, lab, v, 34,
            color=GREEN if v == 0 else (S_HIGH if v >= 34 else PRIMARY),
            lw=2.20, vw=0.42, lsize=7.8)
note(s, CX, 4.44, CW, 0.64, "Priority",
     "Reduce public network access first, then strengthen encryption and logging "
     "controls on the Azure ML workspaces.", accent=PRIMARY, tint=GREY_BG,
     bsize=8.2)

# =================================================================== 21. AI CONC
s = std("AI Account and Regional Concentration", "Where the AI findings cluster",
        "AI finding volume sits mostly in one account. Asset inventory clusters "
        "in southindia.", SRC_AI)
cy = panel(s, CX, 1.48, 4.86, 3.10, "AI finding-count distribution by account")
ACCT = [("a92dc17c-b0fa-4467-8a8e-f22fb83e00b6", 129),
        ("f794fc5a-2254-4f9f-9d2d-15df759d9c81", 16),
        ("39d61d1c-1c17-45dd-a5e4-e413978b6ce5", 8),
        ("8fb6b24d-d917-4b1c-9b70-9902d901057c", 4),
        ("9ed1625e-4449-4bbd-8be0-412ab1422640", 4),
        ("7ed6f55e-4387-4290-a46e-4a9cd4b4e7f4", 3)]
for i, (lab, v) in enumerate(ACCT):
    bar_wide(s, 0.58, cy + 0.02 + i * 0.36, 4.50, lab, v, 129, color=S_HIGH,
             lsize=7.8, vw=0.42, bar_h=0.10)
box(s, 0.58, cy + 2.24, 4.50, 0.30,
    text="The top account contributes 129 of 164 active AI findings, or 78.7%.",
    size=8.0, color=MUTE, italic=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
cy = panel(s, 5.46, 1.48, 4.14, 1.60, "Unique AI assets by region")
for i, (lab, v) in enumerate([("southindia", 22), ("centralindia", 10),
                              ("eastus2", 2)]):
    bar_row(s, 5.64, cy + 0.04 + i * 0.34, 3.78, lab, v, 22, color=PRIMARY,
            lw=1.30, vw=0.42, lsize=8.0)
note(s, 5.46, 3.24, 4.14, 0.66, "Regional concentration",
     "22 of 34 assets, or 64.7%, sit in southindia.", accent=SECOND, tint=LAV,
     bsize=8.0)
note(s, 5.46, 3.98, 4.14, 0.86, "Account inventory boundary",
     "Unique AI asset counts by account, subscription or project could not be "
     "validated from the inventory output. The account view here is "
     "finding-count distribution only.", accent=RED, tint=RED_LT, bsize=7.8)

# =================================================================== 22. AI VALID
s = std("AI Data Validation and Reporting Boundaries", "What the counts do and do not say",
        "Every count below keeps the source-data boundary. No account-level asset "
        "relationship is inferred.", SRC_AI)
cy = panel(s, CX, 1.48, 5.10, 2.86, "Validation notes")
VAL = [("Inventory basis", "34 unique AI asset IDs in the confirmed inventory output"),
       ("Account limitation", "Account, subscription and project were absent from the inventory output"),
       ("Account view", "The account distribution here is active AI finding-count distribution only"),
       ("Public endpoint basis", "24 public-network-access assets come from confirmed ML Workspace findings"),
       ("Internet exposure", "No separate AI-specific Internet Exposure findings were returned"),
       ("Identity scope", "No confirmed AI IAM or identity findings were returned")]
for i, (k, v) in enumerate(VAL):
    stackrow(s, 0.58, cy + 0.02 + i * 0.40, 4.74, 0.36, k, v, accent=PRIMARY,
             tint=GREY_BG, ksize=8.2, vsize=7.0)
cy = panel(s, 5.70, 1.48, 3.90, 2.86, "Key count-based highlights")
KEY = [("34", "Total AI and ML assets discovered", PRIMARY),
       ("27", "Azure Machine Learning workspaces", PRIMARY),
       ("7", "Azure Databricks workspaces", SECOND),
       ("27", "AI assets with High findings", S_HIGH),
       ("24", "AI assets with public network access", S_HIGH),
       ("0", "Critical AI findings confirmed", GREEN),
       ("0", "AI IAM and identity findings confirmed", GREEN)]
for i, (num, lab, col) in enumerate(KEY):
    y = cy + 0.02 + i * 0.34
    box(s, 5.88, y, 0.62, 0.32, text=num, size=13, color=col, bold=True,
        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0, mr=0)
    box(s, 6.58, y, 2.84, 0.32, text=lab, size=8.0, color=NAVY,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
note(s, CX, 4.46, CW, 0.62, "Reporting principle",
     "Only confirmed tenant data appears here. Unsupported values stay "
     "unreported.", accent=PRIMARY, tint=GREY_BG, bsize=8.2)

# =================================================================== 23. AI TOXIC
s = std("AI Toxic Combinations, Executive View", "Same-asset risk combinations",
        "Five high-confidence combinations are confirmed. No complete multi-hop "
        "path to identity, data, models or storage was proven.", SRC_TOX)
metrics(s, 1.46, [
    ("5", "Toxic combinations", "All include High controls", RED),
    ("4", "Start at public access", "Azure ML workspace exposure", RED),
    ("5", "High-risk combinations", "High findings involved", RED),
    ("0", "Multi-hop paths", "No downstream target proven", GREEN),
    ("0", "Privileged identity paths", "No privileged role confirmed", GREEN)],
    h=0.86, vsize=16)
ROWS = [["PRIMARY AI ASSET", "CONFIRMED WEAKNESS STACK", "RISK", "HOPS"],
        ["whatsapp-chat", "Public access, no CMK, no diagnostics", "HIGH", "1"],
        ["6eskai-innov8", "Public access, no CMK, HBI disabled, Basic SKU", "HIGH", "1"],
        ["6e-enterprise", "Public access, no CMK, no diagnostics", "HIGH", "1"],
        ["AI-Foundry-NP-EA", "Public access, no CMK, HBI disabled", "HIGH", "1"],
        ["6e-openai-Non-prod-southindia-3",
         "No CMK, no managed identity, no diagnostics", "MED/HIGH", "1"]]
t = table(s, CX, 2.46, CW, 1.86, ROWS, colw=[2.60, 4.55, 1.10, 0.95],
          hsize=8.0, bsize=8.0)
row_heights(t, 0.31, head=0.27)
risk_col(t, 2, size=7.4)
center_col(t, 3)
table_grid(t)
note(s, CX, 4.42, 4.50, 0.66, "Confirmed",
     "Public or API entry, plus same-asset configuration findings.",
     accent=GREEN, tint=GREEN_LT, bsize=8.0)
note(s, 5.10, 4.42, 4.50, 0.66, "Not confirmed",
     "Privileged identities, datasets, model endpoints, credentials, storage or "
     "lateral movement.", accent=RED, tint=RED_LT, bsize=8.0)

# =================================================================== 24. ML PATHS
s = std("Public Azure ML Toxic Combination Paths", "Four confirmed combinations",
        "Four paths start with public network access, then stack encryption, "
        "logging and governance weaknesses on the same workspace.")
panel(s, CX, 1.46, CW, 0.74)
chain(s, 0.58, 1.54, 8.84, 0.58, [
    ("Internet", "Untrusted source", RED, RED_LT),
    ("Public ML workspace", "Public network access enabled", RED, RED_LT),
    ("Weakness stack", "Encryption, logging and governance gaps", PRIMARY, GREY_BG),
    ("Downstream", "Not confirmed by the dataset", MUTE, GREY_BG)], gap=0.26)
ML = [("whatsapp-chat", ["PUBLIC", "NO CMK", "NO LOGS", "HBI + MONITORING GAPS"]),
      ("6eskai-innov8", ["PUBLIC", "NO CMK", "NO LOGS", "HBI DISABLED + BASIC SKU"]),
      ("6e-enterprise", ["PUBLIC", "NO CMK", "NO LOGS", "HBI DISABLED + BASIC SKU"]),
      ("AI-Foundry-NP-EA", ["PUBLIC", "NO CMK", "NO LOGS", "HBI DISABLED + BASIC SKU"])]
for i, (name, tags) in enumerate(ML):
    x = 0.40 + (i % 2) * 4.70
    y = 2.28 + (i // 2) * 1.24
    panel(s, x, y, 4.50, 1.16)
    dot(s, x + 0.20, y + 0.15, 0.11, RED)
    box(s, x + 0.40, y + 0.05, 2.70, 0.28, text=name, size=10.5, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    badge(s, x + 3.60, y + 0.09, 0.70, 0.24, "HIGH", kind="crit")
    box(s, x + 0.40, y + 0.30, 3.90, 0.20, text="azure_machine_learning_workspace",
        size=7.0, color=GREY_TX, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    cx = x + 0.20
    for tag, w in zip(tags, [0.66, 0.74, 0.76, 1.68]):
        badge(s, cx, y + 0.54, w, 0.25, tag, kind="crit", size=6.4)
        cx += w + 0.08
    box(s, x + 0.20, y + 0.84, 4.14, 0.28,
        text="Potential impact: a publicly reachable workspace with weaker data "
             "protection and detection.", size=7.0, color=MUTE, italic=True, ml=0)
note(s, CX, 4.74, CW, 0.52, "Evidence boundary",
     "All four paths rest on the public-workspace finding and same-asset control "
     "findings. No identity, dataset, model endpoint, storage or credential "
     "relationship was confirmed.", accent=PRIMARY, tint=GREY_BG, bsize=7.6)

# =================================================================== 25. GOVERNANCE
s = std("AI Governance Toxic Combination and Risk Patterns", "The fifth combination",
        "Combination five affects an Azure OpenAI and Cognitive account. The "
        "aggregate view shows recurring encryption, identity and logging gaps.")
cy = panel(s, CX, 1.46, 4.30, 2.96, "Toxic combination 5, Azure OpenAI and Cognitive")
box(s, 0.58, cy, 2.60, 0.28, text="6e-openai-Non-prod-southindia-3", size=9.5,
    color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
badge(s, 3.32, cy + 0.02, 1.20, 0.24, "MEDIUM / HIGH", kind="high", size=6.8)
box(s, 0.58, cy + 0.28, 3.94, 0.20, text="azure_cognitive_account", size=7.0,
    color=GREY_TX, anchor=MSO_ANCHOR.MIDDLE, ml=0)
for i, (sev, name, desc, kind) in enumerate([
        ("HIGH", "OpenAI Account CMK Encrypted",
         "The account is not encrypted with a customer-managed key", "crit"),
        ("MEDIUM", "OpenAI Account Managed Identity Enabled",
         "Managed identity is not enabled", "high"),
        ("MEDIUM", "OpenAI Account Diagnostic Logging Enabled",
         "Diagnostic logs are not enabled", "high")]):
    y = cy + 0.54 + i * 0.62
    badge(s, 0.58, y + 0.02, 0.66, 0.22, sev, kind=kind, size=6.6)
    box(s, 1.32, y, 3.20, 0.24, text=name, size=8.6, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, 1.32, y + 0.24, 3.20, 0.28, text=desc, size=7.4, color=MUTE, ml=0)
box(s, 0.58, cy + 2.24, 3.94, 0.34,
    text="Public exposure, privileged identity, model deployment, dataset and "
         "credential relationships were not confirmed for this asset.",
    size=7.0, color=GREY_TX, italic=True, ml=0)
cy = panel(s, 4.98, 1.46, 4.62, 2.96, "Aggregate confirmed patterns")
AGG = [("Public Azure ML workspace plus CMK gap", "24 findings", "crit"),
       ("Azure ML workspace plus diagnostics disabled", "19 findings", "med"),
       ("Azure ML workspace plus HBI disabled", "27 findings", "med"),
       ("Azure OpenAI or Cognitive plus CMK disabled", "82 findings", "crit"),
       ("Azure OpenAI or Cognitive plus no managed identity", "40 findings", "high"),
       ("Azure OpenAI or Cognitive plus diagnostics disabled", "75 findings", "med")]
for i, (lab, cnt, kind) in enumerate(AGG):
    y = cy + 0.04 + i * 0.40
    box(s, 5.16, y, 0.05, 0.32, fill=BADGE[kind][1])
    box(s, 5.32, y, 3.20, 0.32, text=lab, size=8.0, color=NAVY,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, 8.54, y, 0.88, 0.32, text=cnt, size=8.0, color=BADGE[kind][1],
        bold=True, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0,
        wrap=False)
box(s, CX, 4.50, 2.10, 0.26, text="WHAT WAS NOT CONFIRMED", size=8.0,
    color=GREY_TX, bold=True, anchor=MSO_ANCHOR.MIDDLE)
for i, lab in enumerate(["complete multi-hop paths", "privileged identity paths",
                         "dataset and data-source paths",
                         "model-endpoint exposure paths",
                         "credential exposure paths"]):
    zero_tile(s, 0.40 + i * 1.86, 4.78, 1.74, 0.54, "0", lab)

# =================================================================== 26. CLOSING
# Layout 1 carries the lockup, the "Certified by" row and www.AccuKnox.com.
closing_slide(prs)

prs.save(OUT)
print("saved:", os.path.abspath(OUT), "slides:", len(prs.slides._sldIdLst))
