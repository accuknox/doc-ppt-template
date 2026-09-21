# -*- coding: utf-8 -*-
"""TCTS telecom AI security decks.

Three eleven-slide decks for Tata Communications Transformation Services (TCTS):
AISPM, Prompt Firewall and AI Guardrails, and Agentic AI and MCP Security.

Each deck opens on the template cover (layout 0) and closes on the template
back cover (layout 1). The nine content slides sit on the Blank layout with a
navy canvas, so the white product screens carry the light on the slide.

Facts and sources: D:\\Atharva\\AccuKnox\\HelpDocs\\references\\tcts-gtm\\research
Images: D:\\Atharva\\AccuKnox\\HelpDocs\\references\\tcts-gtm\\assets (prep_assets.py,
prep_posters.py)

Run:  py -3.11 scripts/build_tcts_ai_decks.py
"""
import shutil
import sys
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

sys.path.insert(0, str(Path(__file__).parent))
from _akdeck import (FONT, GREEN, NAVY, NAVY_DK, NAVY_TXT, PRIMARY, RED, SECOND,  # noqa: E402
                     WHITE, blank_footer, box, closing_slide, cover_slide)
from _pptx_youtube import add_youtube  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "PPT Template.pptx"
OUTDIR = ROOT / "output" / "tcts"
ASSETS = Path(r"D:\Atharva\AccuKnox\HelpDocs\references\tcts-gtm\assets\deck")
LOGO = ROOT / "assets" / "logos" / "accuknox-logo-dark-bg.png"

MED = "Space Grotesk Medium"
SEMI = "Space Grotesk SemiBold"
M = 0.55                      # side margin
SW, SH = 10.0, 5.625

CREDENTIALS = ("IDT   ·   US DoD 5G project   ·   Tata Elxsi NEURON partner   ·   "
               "5G Open Innovation Lab   ·   LF Nephio TSC member")


# ---- low-level XML helpers ------------------------------------------------
def _alpha(clr_parent, alpha):
    """Add <a:alpha> (percent) to the srgbClr under a solidFill parent."""
    clr = clr_parent.find(qn("a:solidFill")).find(qn("a:srgbClr"))
    a = etree.SubElement(clr, qn("a:alpha"))
    a.set("val", str(int(alpha * 1000)))


def fill(sp, rgb, alpha=None):
    sp.fill.solid()
    sp.fill.fore_color.rgb = rgb
    if alpha is not None:
        _alpha(sp._element.spPr, alpha)


def stroke(sp, rgb, w=0.75, alpha=None, dash=None):
    sp.line.color.rgb = rgb
    sp.line.width = Pt(w)
    if dash is not None:
        sp.line.dash_style = dash
    if alpha is not None:
        _alpha(sp._element.spPr.find(qn("a:ln")), alpha)


def shadow(sp, blur=18, dist=6, alpha=40):
    spPr = sp._element.spPr
    eff = spPr.find(qn("a:effectLst"))
    if eff is None:
        eff = etree.SubElement(spPr, qn("a:effectLst"))
    for child in list(eff):
        eff.remove(child)
    sh = etree.SubElement(eff, qn("a:outerShdw"))
    sh.set("blurRad", str(Pt(blur)))
    sh.set("dist", str(Pt(dist)))
    sh.set("dir", "5400000")
    sh.set("algn", "t")
    sh.set("rotWithShape", "0")
    clr = etree.SubElement(sh, qn("a:srgbClr"))
    clr.set("val", "000000")
    a = etree.SubElement(clr, qn("a:alpha"))
    a.set("val", str(int(alpha * 1000)))


def round_pic(pic, adj):
    geom = pic._element.spPr.find(qn("a:prstGeom"))
    geom.set("prst", "roundRect")
    av = geom.find(qn("a:avLst"))
    if av is None:
        av = etree.SubElement(geom, qn("a:avLst"))
    gd = etree.SubElement(av, qn("a:gd"))
    gd.set("name", "adj")
    gd.set("fmla", f"val {int(adj * 100000)}")


def char_spacing(sp, pts):
    for p in sp.text_frame.paragraphs:
        for r in p.runs:
            r.font._rPr.set("spc", str(int(pts * 100)))


# ---- drawing primitives ---------------------------------------------------
def text(s, x, y, w, h, value, size, color=WHITE, font=FONT, bold=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=None, cs=None):
    sp = box(s, x, y, w, h, text=value, size=size, color=color, bold=bold,
             align=align, anchor=anchor, ml=0, mr=0, mt=0, mb=0, font=font,
             spacing=spacing)
    if cs:
        char_spacing(sp, cs)
    return sp


def hline(s, x, y, w, color=WHITE, alpha=22, weight=0.75):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                Inches(x + w), Inches(y))
    stroke(ln, color, weight, alpha)
    return ln


def arrow(s, x1, y1, x2, y2, color=WHITE, alpha=55, weight=1.25, dash=None, head=True):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                Inches(x2), Inches(y2))
    stroke(ln, color, weight, alpha, dash)
    if head:
        te = etree.SubElement(ln._element.spPr.find(qn("a:ln")), qn("a:tailEnd"))
        te.set("type", "triangle")
        te.set("w", "med")
        te.set("len", "med")
    return ln


def panel(s, x, y, w, h, alpha=6, line_alpha=16, radius=0.06, color=WHITE, dash=None,
          line_color=WHITE):
    sp = box(s, x, y, w, h, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)
    if alpha:
        fill(sp, color, alpha)
    if line_alpha:
        stroke(sp, line_color, 0.75, line_alpha, dash)
    return sp


def pin(s, cx, cy, n, color, d=0.30):
    sp = box(s, cx - d / 2, cy - d / 2, d, d, text=str(n), size=11, color=WHITE,
             bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
             fill=color, line=WHITE, line_w=1.5, shape=MSO_SHAPE.OVAL,
             ml=0, mr=0, mt=0, mb=0)
    shadow(sp, blur=6, dist=2, alpha=45)
    return sp


def chip(s, x, y, label, fg=WHITE, bg=None, bg_alpha=None, line_c=None,
         line_alpha=None, size=7.5, h=0.24, w=None, dash=None, cs=0.8):
    if w is None:
        w = len(label) * (size * 0.64 + cs) / 72 + 0.22
    sp = box(s, x, y, w, h, text=label, size=size, color=fg, bold=False,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5, ml=0, mr=0, mt=0,
             mb=0, font=SEMI)
    if bg is not None:
        fill(sp, bg, bg_alpha)
    if line_c is not None:
        stroke(sp, line_c, 0.75, line_alpha, dash)
    char_spacing(sp, cs)
    return sp


def picture(s, path, x, y, w, radius=0.02, line_alpha=22, blur=22, dist=8, alpha=45):
    im = Image.open(path)
    h = w * im.height / im.width
    pic = s.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    round_pic(pic, radius)
    stroke(pic, WHITE, 0.75, line_alpha)
    shadow(pic, blur=blur, dist=dist, alpha=alpha)
    return pic, h, im.width, im.height


def link(sp, url):
    sp.click_action.hyperlink.address = url


def glow(s, x, y, w, h, color, alpha=30, soft=70):
    """A soft colored light behind a screen. Draw it before the screen."""
    sp = box(s, x, y, w, h, shape=MSO_SHAPE.OVAL)
    fill(sp, color, alpha)
    eff = sp._element.spPr.find(qn("a:effectLst"))
    if eff is None:
        eff = etree.SubElement(sp._element.spPr, qn("a:effectLst"))
    se = etree.SubElement(eff, qn("a:softEdge"))
    se.set("rad", str(Pt(soft)))
    return sp


def lines_for(value, chars_per_line):
    words, lines, cur = value.split(), 1, 0
    for wd in words:
        if cur and cur + 1 + len(wd) > chars_per_line:
            lines, cur = lines + 1, len(wd)
        else:
            cur = cur + (1 if cur else 0) + len(wd)
    return lines


# ---- slide scaffolding ----------------------------------------------------
def dark_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[7])
    blank_footer(s)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = NAVY
    s.shapes.add_picture(str(LOGO), Inches(SW - M - 1.2), Inches(0.46), width=Inches(1.2))
    return s


def title(s, value, w=7.3, size=22):
    return text(s, M, 0.40, w, 1.0, value, size, WHITE, font=MED, spacing=0.95)


def notes(s, value):
    s.notes_slide.notes_text_frame.text = value


def new_deck():
    prs = Presentation(str(TEMPLATE))
    sld_ids = prs.slides._sldIdLst
    for sld_id in list(sld_ids):
        prs.part.drop_rel(sld_id.rId)
        sld_ids.remove(sld_id)
    return prs


# ---- slide 2: hero split with the embedded video --------------------------
def hero(prs, D, acc):
    s = dark_slide(prs)
    text(s, M, 0.40, 3.8, 1.2, D["title"], 22, WHITE, font=MED, spacing=0.95)
    text(s, M, 1.66, 3.45, 1.0, D["definition"], 11, NAVY_TXT, spacing=1.12)
    for i, (value, label) in enumerate(D["facts"]):
        y = 2.95 + i * 1.12
        hline(s, M, y, 3.45, alpha=22)
        hline(s, M, y, 0.55, color=acc, alpha=None, weight=2.0)
        text(s, M, y + 0.13, 3.45, 0.42, value, 22, WHITE, font=MED)
        text(s, M, y + 0.54, 3.45, 0.42, label, 9.5, NAVY_TXT, spacing=1.05)

    vx, vy, vw = 4.55, 1.30, 4.90
    vh = vw * 9 / 16
    glow(s, vx + 0.4, vy + 0.3, vw - 0.8, vh - 0.2, acc, alpha=38, soft=60)
    halo = panel(s, vx - 0.07, vy - 0.07, vw + 0.14, vh + 0.14, alpha=None, line_alpha=22, radius=0.035)
    fill(halo, NAVY_DK)
    shadow(halo, blur=30, dist=10, alpha=40)
    pic = add_youtube(s, D["video"], str(ASSETS / D["poster"]), Inches(vx), Inches(vy),
                      Inches(vw), Inches(vh), title=D["video_title"], start=D.get("start"))
    round_pic(pic, 0.025)
    url = f"https://www.youtube.com/watch?v={D['video']}"
    if D.get("start"):
        url += f"&t={D['start']}s"
    cap = text(s, vx, vy + vh + 0.22, vw, 0.24, D["video_title"], 10, WHITE, font=SEMI)
    link(cap, url)
    sub = text(s, vx, vy + vh + 0.48, vw, 0.24,
               f"YouTube  ·  {D['duration']}  ·  {D['video_note']}", 8.5, NAVY_TXT)
    link(sub, url)
    notes(s, D["notes"])
    return s


# ---- depth slides: architecture, integrations, module map, matrix ---------
MODULES = [
    ("AI-SPM", "Security Posture Management", None),
    ("AI Guardrails", "Prompt Firewall", None),
    ("Agentic AI Security", "Sandboxing and MCP", None),
    ("AI Red Teaming", "and Pen Testing", None),
    ("AI-DR", "Detect and Respond", None),
    ("AI Model and Data", "Dataset Security", None),
    ("AI Identity Security", "SPIFFE per agent", "BETA"),
    ("AI-GRC", "Governance and Risk", "BETA"),
]


def strip_row(s, items, y, label=None, acc=None, w=None):
    """A row of short facts under a diagram, each with a leading accent tick."""
    w = w or (SW - 2 * M)
    hline(s, M, y, w, alpha=18)
    x = M
    if label:
        text(s, M, y + 0.14, 1.75, 0.22, label, 7, WHITE, font=SEMI, cs=1.2)
        x = M + 1.9
    cw = (w - (x - M)) / len(items)
    for i, item in enumerate(items):
        cx = x + i * cw
        if isinstance(item, tuple):
            head, sub = item
            text(s, cx, y + 0.12, cw - 0.2, 0.24, head, 10, WHITE, font=SEMI)
            text(s, cx, y + 0.36, cw - 0.25, 0.4, sub, 8.5, NAVY_TXT, spacing=1.05)
        else:
            text(s, cx, y + 0.12, cw - 0.2, 0.24, item, 9, NAVY_TXT)


def node_card(s, x, y, w, h, label, sub=None, accent=None, size=11, alpha=8):
    n = panel(s, x, y, w, h, alpha=alpha, line_alpha=None if accent else 35, radius=0.1)
    if accent:
        stroke(n, accent, 1.25)
    if sub:
        text(s, x + 0.14, y + 0.1, w - 0.28, 0.26, label, size, WHITE, font=SEMI)
        text(s, x + 0.14, y + 0.34, w - 0.28, h - 0.42, sub, 8.5, NAVY_TXT, spacing=1.05)
    else:
        text(s, x, y, w, h, label, size, WHITE, font=SEMI, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE, spacing=1.05)
    return n


def lanes(prs, D, acc):
    """A control plane on the left, one labelled lane per integration mode."""
    s = dark_slide(prs)
    title(s, D["title"], w=7.4)
    cx, cw = M, 1.75
    top, bot = 1.5, 4.55
    hub = panel(s, cx, top, cw, bot - top, alpha=10, line_alpha=None, radius=0.1)
    stroke(hub, acc, 1.5)
    text(s, cx + 0.12, top + 0.12, cw - 0.24, 1.0, D["hub"], 12, WHITE, font=SEMI, spacing=1.05)
    text(s, cx + 0.12, bot - 0.75, cw - 0.24, 0.6, D["hub_sub"], 8.5, NAVY_TXT, spacing=1.05)

    lane_h = (bot - top - 0.18 * (len(D["lanes"]) - 1)) / len(D["lanes"])
    tx = 5.35
    for i, (mode, target, detail) in enumerate(D["lanes"]):
        y = top + i * (lane_h + 0.18)
        mid = y + lane_h / 2
        arrow(s, cx + cw + 0.06, mid, tx - 0.06, mid, alpha=40)
        text(s, cx + cw + 0.22, mid - 0.24, 2.7, 0.22, mode, 9, WHITE, font=SEMI)
        node_card(s, tx, y, SW - M - tx, lane_h, target, detail, size=11)
    if D.get("strip"):
        strip_row(s, D["strip"], 4.7, D.get("strip_label"), acc)
    footnote(s, D["footnote"], y=5.34)
    notes(s, D["notes"])
    return s


def pipeline(prs, D, acc):
    """Five stages in a row, then the engine that feeds stages three to five."""
    s = dark_slide(prs)
    title(s, D["title"], w=7.4)
    n = len(D["stages"])
    gap = 0.22
    w = (SW - 2 * M - gap * (n - 1)) / n
    y = 1.55
    for i, (num, name, desc) in enumerate(D["stages"]):
        x = M + i * (w + gap)
        card = panel(s, x, y, w, 1.5, alpha=8, line_alpha=28, radius=0.1)
        text(s, x + 0.14, y + 0.12, w - 0.28, 0.3, num, 13, WHITE, font=MED)
        hline(s, x + 0.14, y + 0.46, 0.3, color=acc, alpha=None, weight=2.0)
        text(s, x + 0.14, y + 0.56, w - 0.28, 0.8, name, 12, WHITE, font=SEMI)
        text(s, x, y + 1.6, w, 0.9, desc, 8.5, NAVY_TXT, spacing=1.08)
        if i:
            arrow(s, x - gap + 0.02, y + 0.75, x - 0.02, y + 0.75, alpha=45)
    band_y = 3.85
    band = panel(s, M, band_y, SW - 2 * M, 0.92, alpha=10, line_alpha=None, radius=0.06)
    stroke(band, acc, 1.0)
    text(s, M + 0.22, band_y + 0.14, 2.4, 0.26, D["band"][0], 11, WHITE, font=SEMI)
    text(s, M + 0.22, band_y + 0.42, 5.6, 0.42, D["band"][1], 9, NAVY_TXT, spacing=1.05)
    text(s, SW - M - 2.4, band_y + 0.2, 2.2, 0.5, D["band"][2], 20, WHITE, font=MED,
         align=PP_ALIGN.RIGHT)
    text(s, SW - M - 2.4, band_y + 0.62, 2.2, 0.24, D["band"][3], 8.5, NAVY_TXT,
         align=PP_ALIGN.RIGHT)
    footnote(s, D["footnote"], y=5.05)
    notes(s, D["notes"])
    return s


def sandbox_arch(prs, D, acc):
    """Sources on the left, the runtime and its sandbox in the middle, the plane right."""
    s = dark_slide(prs)
    title(s, D["title"], w=7.4)
    lx, lw = M, 2.45
    for i, (label, sub) in enumerate(D["sources"]):
        y = 1.55 + i * 1.02
        node_card(s, lx, y, lw, 0.88, label, sub)
        arrow(s, lx + lw + 0.05, y + 0.44, 3.55, 2.95, alpha=35)
    mx, mw = 3.6, 3.2
    runtime = panel(s, mx, 1.5, mw, 3.0, alpha=6, line_alpha=30, radius=0.08)
    text(s, mx + 0.16, 1.6, mw - 0.32, 0.24, D["runtime"], 9, NAVY_TXT, font=SEMI, cs=0.8)
    sb = panel(s, mx + 0.18, 1.95, mw - 0.36, 2.35, alpha=9, line_alpha=None, radius=0.08)
    stroke(sb, acc, 1.5, None, MSO_LINE_DASH_STYLE.DASH)
    text(s, mx + 0.34, 2.06, mw - 0.68, 0.24, D["sandbox"], 7.5, WHITE, font=SEMI, cs=0.8)
    for i, line in enumerate(D["controls"]):
        text(s, mx + 0.34, 2.45 + i * 0.5, mw - 0.68, 0.44, "✓  " + line, 9.5, WHITE, spacing=1.05)
    rx = 7.2
    arrow(s, mx + mw + 0.05, 2.95, rx - 0.05, 2.95, alpha=40)
    node_card(s, rx, 2.35, SW - M - rx, 1.2, D["plane"][0], D["plane"][1], accent=acc)
    if D.get("strip"):
        strip_row(s, D["strip"], 4.7, D.get("strip_label"), acc)
    footnote(s, D["footnote"], y=5.34)
    notes(s, D["notes"])
    return s


def image_slide(prs, D, acc):
    """One large image, a rail of facts beside it, an optional chip row."""
    s = dark_slide(prs)
    title(s, D["title"], w=7.4)
    ix, iy, iw = D["img_x"], D["img_y"], D.get("img_w")
    if iw is None:
        im = Image.open(ASSETS / D["image"])
        iw = D["img_h"] * im.width / im.height
        ix = ix if ix is not None else (SW - iw - M)
    glow(s, ix + 0.5, iy + 0.3, max(iw - 1.0, 1.0), 2.4, acc, alpha=32, soft=60)
    pic, h, pw, ph = picture(s, ASSETS / D["image"], ix, iy, iw, radius=0.03, line_alpha=30)
    for i, (head, sub) in enumerate(D["rail"]):
        y = D.get("rail_top", 1.6) + i * D.get("rail_step", 0.86)
        hline(s, M, y, D.get("rail_w", 2.5), alpha=18)
        hline(s, M, y, 0.4, color=acc, alpha=None, weight=2.0)
        text(s, M, y + 0.12, D.get("rail_w", 2.5), 0.26, head, 11.5, WHITE, font=SEMI)
        text(s, M, y + 0.38, D.get("rail_w", 2.5) - 0.1, 0.42, sub, 9, NAVY_TXT, spacing=1.05)
    if D.get("chips"):
        label, items = D["chips"]
        cy = D.get("chips_y", 4.95)
        text(s, M, cy + 0.04, 2.1, 0.22, label, 7, WHITE, font=SEMI, cs=1.2)
        x = M + 2.2
        for item in items:
            c = chip(s, x, cy, item, fg=WHITE, bg=WHITE, bg_alpha=12, line_c=WHITE,
                     line_alpha=26, size=8, h=0.28)
            x += c.width / 914400 + 0.12
    footnote(s, D["footnote"], y=D.get("foot_y", 5.38))
    notes(s, D["notes"])
    return s


def module_map(prs, D, acc):
    """The eight modules on the left, this module's depth on the right."""
    s = dark_slide(prs)
    title(s, D["title"], w=7.4)
    cw, ch, gap = 1.55, 0.56, 0.1
    for i, (name, sub, tag) in enumerate(MODULES):
        col, row = i % 2, i // 2
        x = M + col * (cw + gap)
        y = 1.55 + row * (ch + gap)
        on = name == D["highlight"]
        card = panel(s, x, y, cw, ch, alpha=14 if on else 6, line_alpha=None if on else 18, radius=0.1)
        if on:
            stroke(card, acc, 1.5)
        text(s, x + 0.1, y + 0.07, cw - 0.2, 0.22, name, 8.5, WHITE, font=SEMI, spacing=1.0)
        text(s, x + 0.1, y + 0.28, cw - 0.2, 0.24, sub, 7, NAVY_TXT, spacing=1.0)
        if tag:
            chip(s, x + cw - 0.5, y + ch - 0.2, tag, fg=WHITE, bg=WHITE, bg_alpha=20, size=5.5,
                 h=0.15, w=0.42, cs=0.5)
    im = Image.open(ASSETS / D["image"])
    iw = D.get("img_w", 5.5)
    ix = SW - M - iw
    glow(s, ix + 0.6, D.get("img_y", 1.7) + 0.3, iw - 1.2, 1.8, acc, alpha=30, soft=60)
    picture(s, ASSETS / D["image"], ix, D.get("img_y", 1.7), iw, radius=0.03, line_alpha=30)
    strip_row(s, D["depth"], D.get("strip_y", 4.62), D.get("strip_label"), acc)
    footnote(s, D["footnote"], y=5.38)
    notes(s, D["notes"])
    return s


def matrix(prs, D, acc):
    """A support matrix drawn as a native table on the dark canvas."""
    s = dark_slide(prs)
    title(s, D["title"], w=7.4)
    cols = D["cols"]
    total = sum(w for _, w in cols)
    scale = (SW - 2 * M) / total
    y = 1.6
    x = M
    for name, w in cols:
        text(s, x, y, w * scale - 0.15, 0.22, name, 7.5, WHITE, font=SEMI, cs=1.2)
        x += w * scale
    hline(s, M, y + 0.3, SW - 2 * M, color=acc, alpha=None, weight=1.5)
    row_h = D.get("row_h", 0.68)
    for r, row in enumerate(D["rows"]):
        ry = y + 0.42 + r * row_h
        if r % 2 == 0:
            band = box(s, M - 0.12, ry - 0.08, SW - 2 * M + 0.24, row_h - 0.06,
                       shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
            fill(band, WHITE, 4)
        x = M
        for c, (cell, (_, w)) in enumerate(zip(row, cols)):
            cw2 = w * scale - 0.2
            if c == 0:
                text(s, x, ry, cw2, row_h - 0.1, cell, 10.5, WHITE, font=SEMI, spacing=1.05)
            else:
                text(s, x, ry + 0.02, cw2, row_h - 0.1, cell, 9, NAVY_TXT, spacing=1.08)
            x += w * scale
        hline(s, M, ry + row_h - 0.1, SW - 2 * M, alpha=12)
    if D.get("chips"):
        cy = y + 0.46 + len(D["rows"]) * row_h
        x = M
        for label, items in D["chips"]:
            text(s, x, cy + 0.04, 1.1, 0.22, label, 7, WHITE, font=SEMI, cs=1.2)
            x += 1.0
            for item in items:
                c = chip(s, x, cy, item, fg=WHITE, bg=WHITE, bg_alpha=12, line_c=WHITE,
                         line_alpha=26, size=8, h=0.28)
                x += c.width / 914400 + 0.12
            x += 0.45
    footnote(s, D["footnote"], y=5.38)
    notes(s, D["notes"])
    return s


# ---- demo slide: the full walkthrough, embedded as published ---------------
BEATS = {"Set up": WHITE, "In action": None, "Evidence": GREEN}


def demo(prs, D, acc):
    s = dark_slide(prs)
    title(s, D["title"], w=7.4)
    vx, vy, vw = M, 1.45, 6.1
    vh = vw * 9 / 16
    glow(s, vx + 0.5, vy + 0.4, vw - 1.0, vh - 0.4, acc, alpha=38, soft=60)
    halo = panel(s, vx - 0.07, vy - 0.07, vw + 0.14, vh + 0.14, alpha=None, line_alpha=22, radius=0.03)
    fill(halo, NAVY_DK)
    shadow(halo, blur=30, dist=10, alpha=40)
    pic = add_youtube(s, D["video"], str(ASSETS / D["poster"]), Inches(vx), Inches(vy),
                      Inches(vw), Inches(vh), title=D["video_title"])
    round_pic(pic, 0.022)
    url = f"https://www.youtube.com/watch?v={D['video']}"
    cap = text(s, vx, vy + vh + 0.2, vw, 0.24, D["video_title"], 10, WHITE, font=SEMI)
    link(cap, url)
    sub = text(s, vx, vy + vh + 0.45, vw, 0.24,
               f"YouTube  ·  {D['duration']}  ·  {D['video_note']}", 8.5, NAVY_TXT)
    link(sub, url)

    # chapters, each one opens the video at that moment
    cx, cw = 7.05, SW - M - 7.05
    text(s, cx, vy - 0.02, cw, 0.2, "CHAPTERS", 7, WHITE, font=SEMI, cs=1.4)
    rail_top, step = vy + 0.36, 0.5
    rail = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(cx + 0.05), Inches(rail_top + 0.08),
                                  Inches(cx + 0.05), Inches(rail_top + 0.08 + step * (len(D["chapters"]) - 1)))
    stroke(rail, WHITE, 0.75, 22)
    for i, (stamp, beat, label) in enumerate(D["chapters"]):
        y = rail_top + i * step
        color = BEATS[beat] or acc
        dot = box(s, cx, y + 0.03, 0.1, 0.1, shape=MSO_SHAPE.OVAL)
        fill(dot, color)
        mm, ss = stamp.split(":")
        t = text(s, cx + 0.24, y - 0.04, 0.6, 0.24, stamp, 12, WHITE, font=MED)
        l = text(s, cx + 0.24, y + 0.19, cw - 0.24, 0.2, label, 8.5, NAVY_TXT)
        for sp in (t, l):
            link(sp, f"{url}&t={int(mm) * 60 + int(ss)}s")
    # legend
    ly = rail_top + step * len(D["chapters"]) + 0.02
    for (beat, color), off in zip(BEATS.items(), (0.0, 0.72, 1.56)):
        dot = box(s, cx + off, ly + 0.06, 0.09, 0.09, shape=MSO_SHAPE.OVAL)
        fill(dot, color or acc)
        text(s, cx + off + 0.14, ly, 0.8, 0.22, beat, 8, NAVY_TXT)
    notes(s, D["notes"])
    return s


# ---- slide 3: annotated product screen ------------------------------------
def annotated(prs, D, acc):
    s = dark_slide(prs)
    title(s, D["title"])
    X, Y, W = 3.30, 1.45, 6.95
    glow(s, X + 0.6, Y + 0.5, 5.2, 3.4, acc, alpha=40, soft=80)
    main, H, iw, ih = picture(s, ASSETS / D["main"], X, Y, W, radius=0.018, line_alpha=26)

    def at_main(px, py):
        return X + px / iw * W, Y + py / ih * H

    placed = []
    for spec in D["insets"]:
        p, h, pw, ph = picture(s, ASSETS / spec["img"], spec["x"], spec["y"], spec["w"],
                               radius=0.04, line_alpha=35, blur=28, dist=10, alpha=55)
        placed.append((spec["x"], spec["y"], spec["w"], h, pw, ph))

    for n, where, px, py in D["pins"]:
        if where == "main":
            cx, cy = at_main(px, py)
        else:
            x0, y0, w0, h0, pw, ph = placed[where]
            cx, cy = x0 + px / pw * w0, y0 + py / ph * h0
        pin(s, cx, cy, n, acc)

    for i, (head, sub) in enumerate(D["rail"]):
        y = 1.62 + i * 0.9
        pin(s, M + 0.15, y + 0.14, i + 1, acc)
        text(s, 0.98, y, 2.2, 0.3, head, 12, WHITE, font=SEMI)
        text(s, 0.98, y + 0.30, 2.1, 0.56, sub, 9.5, NAVY_TXT, spacing=1.08)
    notes(s, D["notes"])
    return s


# ---- slide 4 builders: one diagram per deck -------------------------------
def use_cases(s, items, acc, y=3.98, col_w=2.78, gap=0.28):
    for i, (head, sub, tag) in enumerate(items):
        x = M + i * (col_w + gap)
        pin(s, x + 0.15, y + 0.13, i + 1, acc, d=0.28)
        text(s, x + 0.42, y, col_w - 0.42, 0.28, head, 12, WHITE, font=SEMI)
        text(s, x + 0.42, y + 0.30, col_w - 0.45, 0.5, sub, 9.5, NAVY_TXT, spacing=1.08)
        chip(s, x + 0.42, y + 0.86, tag, fg=WHITE, bg=WHITE, bg_alpha=10, line_c=WHITE,
             line_alpha=28, size=7)


def footnote(s, value, y=5.24):
    return text(s, M, y, SW - 2 * M, 0.24, value, 8, NAVY_TXT)


def estate_lane(prs, D, acc):
    """AISPM: five zones of an operator estate and the AI assets found in each."""
    s = dark_slide(prs)
    title(s, D["title"])
    # legend
    lx = SW - M - 3.05
    chip(s, lx, 1.17, "MANAGED", fg=WHITE, bg=WHITE, bg_alpha=16, size=6.8, w=0.86)
    chip(s, lx + 0.95, 1.17, "SHADOW AI, NOT APPROVED", fg=WHITE, line_c=RED, dash=MSO_LINE_DASH_STYLE.DASH,
         size=6.8, w=2.1)

    zones = D["zones"]
    zw, gap, zy, zh = 1.72, 0.075, 1.55, 1.93
    for i, (name, runs_there, assets) in enumerate(zones):
        x = M + i * (zw + gap)
        panel(s, x, zy, zw, zh, alpha=6, line_alpha=16, radius=0.05)
        text(s, x + 0.14, zy + 0.13, zw - 0.28, 0.26, name, 12, WHITE, font=SEMI)
        text(s, x + 0.14, zy + 0.42, zw - 0.28, 0.4, runs_there, 8.5, NAVY_TXT, spacing=1.05)
        for j, (asset, shadow_ai, case) in enumerate(assets):
            cy = zy + 0.95 + j * 0.44
            cw = zw - 0.28
            if shadow_ai:
                chip(s, x + 0.14, cy, asset, fg=WHITE, line_c=RED, dash=MSO_LINE_DASH_STYLE.DASH,
                     size=8, h=0.3, w=cw, cs=0.2)
            else:
                chip(s, x + 0.14, cy, asset, fg=WHITE, bg=WHITE, bg_alpha=16, size=8, h=0.3,
                     w=cw, cs=0.2)
            pin(s, x + 0.14 + cw - 0.02, cy + 0.02, case, acc, d=0.2)
    # use case 3 spans the whole estate
    by = zy + zh + 0.16
    total = 5 * zw + 4 * gap
    hline(s, M, by, total, alpha=30)
    for x in (M, M + total):
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(by - 0.08),
                                    Inches(x), Inches(by))
        stroke(ln, WHITE, 0.75, 30)
    pin(s, M + total / 2, by, 3, acc, d=0.22)

    use_cases(s, D["cases"], acc)
    footnote(s, D["footnote"])
    notes(s, D["notes"])
    return s


def firewall_session(prs, D, acc):
    """Prompt Firewall: a redrawn care-bot session with a verdict per turn."""
    s = dark_slide(prs)
    title(s, D["title"], w=7.4)
    px, py, pw, ph = M, 1.52, 5.05, 3.62
    p = panel(s, px, py, pw, ph, alpha=None, line_alpha=16, radius=0.04)
    fill(p, NAVY_DK)
    shadow(p, blur=26, dist=8, alpha=40)
    text(s, px + 0.22, py + 0.16, 3.0, 0.24, "Subscriber care bot  ·  one session", 9, NAVY_TXT)
    hline(s, px, py + 0.5, pw, alpha=12)

    colors = {"PASS": GREEN, "SANITIZE": PRIMARY, "MONITOR": SECOND, "BLOCK": RED}
    y = py + 0.68
    for who, msg, verdict in D["turns"]:
        bw = 3.3
        if who == "user":
            bx = px + pw - 0.22 - bw
            b = box(s, bx, y, bw, 0.46, text=msg, size=9.5, color=WHITE,
                    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.3, anchor=MSO_ANCHOR.MIDDLE,
                    ml=0.14, mr=0.14)
            fill(b, WHITE, 13)
            cx = bx - 0.1 - 0.9
        else:
            bx = px + 0.22
            b = box(s, bx, y, bw, 0.46, text=msg, size=9.5, color=WHITE,
                    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.3, anchor=MSO_ANCHOR.MIDDLE,
                    ml=0.14, mr=0.14)
            stroke(b, WHITE, 0.75, 25)
            cx = bx + bw + 0.1
        chip(s, cx, y + 0.11, verdict, fg=WHITE, bg=colors[verdict], size=7, w=0.9, cs=0.8)
        y += 0.62
    # session risk meter
    my = py + ph - 0.5
    text(s, px + 0.22, my - 0.02, 1.2, 0.24, "Session risk", 8.5, NAVY_TXT)
    seg_colors = [GREEN, PRIMARY, SECOND, RED]
    for i, c in enumerate(seg_colors):
        seg = box(s, px + 1.25 + i * 0.52, my + 0.04, 0.46, 0.1 + i * 0.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
                  radius=0.5)
        fill(seg, c)
    text(s, px + 3.45, my - 0.02, 1.4, 0.24, "Blocked at turn 4", 8.5, WHITE, font=SEMI,
         align=PP_ALIGN.RIGHT)

    # three use cases stacked on the right
    rx, rw = 5.95, SW - M - 5.95
    for i, (head, sub, tag) in enumerate(D["cases"]):
        yy = 1.56 + i * 1.22
        pin(s, rx + 0.15, yy + 0.13, i + 1, acc, d=0.28)
        text(s, rx + 0.42, yy, rw - 0.42, 0.28, head, 12, WHITE, font=SEMI)
        text(s, rx + 0.42, yy + 0.3, rw - 0.42, 0.5, sub, 9.5, NAVY_TXT, spacing=1.08)
        chip(s, rx + 0.42, yy + 0.84, tag, fg=WHITE, bg=WHITE, bg_alpha=10, line_c=WHITE,
             line_alpha=28, size=7)
    footnote(s, D["footnote"])
    notes(s, D["notes"])
    return s


def noc_loop(prs, D, acc):
    """Agentic: a NOC agent inside a kernel sandbox, its MCP tools, and the gates."""
    s = dark_slide(prs)
    title(s, D["title"], w=7.4)

    def node(x, y, w, h, label, sub=None, line_c=WHITE, line_alpha=40, bg_alpha=9, size=10.5):
        n = panel(s, x, y, w, h, alpha=bg_alpha, line_alpha=line_alpha, radius=0.12, line_color=line_c)
        if sub:
            text(s, x + 0.12, y + 0.08, w - 0.24, 0.24, label, size, WHITE, font=SEMI)
            text(s, x + 0.12, y + 0.32, w - 0.24, 0.24, sub, 8, NAVY_TXT)
        else:
            text(s, x, y, w, h, label, size, WHITE, font=SEMI, align=PP_ALIGN.CENTER,
                 anchor=MSO_ANCHOR.MIDDLE)
        return n

    # left column: the trigger and a blocked destination
    node(M, 1.72, 1.4, 0.62, "Cell outage", "alarm from the NOC")
    node(M, 2.92, 1.4, 0.62, "Unlisted host", "blocked by the allowlist", line_c=RED, line_alpha=95)
    # sandbox
    sx, sy, sw, sh = 2.35, 1.5, 2.55, 2.2
    sb = panel(s, sx, sy, sw, sh, alpha=5, line_alpha=None, radius=0.05)
    stroke(sb, acc, 1.25, None, MSO_LINE_DASH_STYLE.DASH)
    text(s, sx + 0.16, sy + 0.12, sw - 0.3, 0.22, "KERNEL SANDBOX  ·  eBPF AND LSM", 7.5, WHITE,
         font=SEMI, cs=0.8)
    node(sx + 0.2, sy + 0.44, sw - 0.4, 0.56, "NOC remediation agent", size=11)
    for i, ctl in enumerate(D["controls"]):
        text(s, sx + 0.22, sy + 1.16 + i * 0.3, sw - 0.4, 0.24, "✓  " + ctl, 9, WHITE)
    arrow(s, M + 1.4, 2.03, sx + 0.2, sy + 0.72)
    arrow(s, sx, 3.23, M + 1.4, 3.23, color=RED, alpha=95, weight=1.5)

    # MCP tools, each with its gate state inside the node
    mx, mw, mh = 5.4, 2.3, 0.64
    tools = D["tools"]
    for i, (name, state) in enumerate(tools):
        yy = 1.5 + i * 0.78
        gate = state != "ALLOWED"
        n = panel(s, mx, yy, mw, mh, alpha=9, line_alpha=95 if gate else 40, radius=0.12,
                  line_color=RED if gate else WHITE)
        text(s, mx + 0.16, yy + 0.09, mw - 0.3, 0.24, name, 10, WHITE, font=SEMI)
        chip(s, mx + 0.16, yy + 0.36, state, fg=WHITE, bg=RED if gate else GREEN,
             size=6.3, w=1.12 if gate else 0.74, h=0.19)
        arrow(s, sx + sw - 0.2, sy + 0.72, mx, yy + mh / 2, alpha=45)
    # network target, behind the approval gate
    node(SW - M - 1.2, 3.07, 1.2, 0.56, "RAN and core", size=10)
    arrow(s, mx + mw, 3.35, SW - M - 1.2, 3.35, dash=MSO_LINE_DASH_STYLE.DASH, alpha=60)

    use_cases(s, D["cases"], acc)
    footnote(s, D["footnote"])
    notes(s, D["notes"])
    return s


# ---- slide 5: proof --------------------------------------------------------
def proof(prs, D, acc):
    s = dark_slide(prs)
    title(s, D["title"], w=7.4)
    text(s, M, 1.34, 5.0, 1.2, D["big"], 80, WHITE, font=MED, spacing=0.9)
    text(s, M, 2.55, 4.5, 0.5, D["big_label"], 13, WHITE, spacing=1.1)
    src = text(s, M, 3.1, 4.5, 0.22, D["big_source"], 8.5, NAVY_TXT)
    link(src, D["big_url"])

    qy = 3.55
    qlines = lines_for(D["quote"], 60)
    by_y = qy + qlines * 0.2 + 0.12
    bar = box(s, M, qy + 0.03, 0.04, by_y + 0.2 - qy)
    fill(bar, acc)
    text(s, M + 0.2, qy, 4.3, qlines * 0.2 + 0.05, "“" + D["quote"] + "”", 10.5, WHITE, spacing=1.12)
    text(s, M + 0.2, by_y, 4.3, 0.22, D["quote_by"], 8.5, NAVY_TXT)

    rx, rw = 5.85, SW - M - 5.85
    for i, item in enumerate(D["right"]):
        yy = 1.42 + i * 1.62
        if item["kind"] == "stat":
            hline(s, rx, yy, rw, alpha=22)
            hline(s, rx, yy, 0.5, color=acc, alpha=None, weight=2.0)
            text(s, rx, yy + 0.12, rw, 0.55, item["value"], 32, WHITE, font=MED)
            text(s, rx, yy + 0.7, rw, 0.55, item["label"], 9.5, NAVY_TXT, spacing=1.08)
            l = text(s, rx, yy + 1.22, rw, 0.2, item["source"], 7.5, NAVY_TXT)
            link(l, item["url"])
        else:  # flow
            hline(s, rx, yy, rw, alpha=22)
            hline(s, rx, yy, 0.5, color=acc, alpha=None, weight=2.0)
            names = item["nodes"]
            nw = (rw - 0.3 * (len(names) - 1)) / len(names)
            for j, nm in enumerate(names):
                x = rx + j * (nw + 0.3)
                hl = j == 1
                n = panel(s, x, yy + 0.2, nw, 0.62, alpha=16 if hl else 8,
                          line_alpha=None if hl else 30, radius=0.12)
                if hl:
                    stroke(n, acc, 1.25)
                text(s, x + 0.04, yy + 0.2, nw - 0.08, 0.62, nm, 8.5, WHITE, font=SEMI,
                     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1.0)
                if j:
                    arrow(s, x - 0.28, yy + 0.51, x - 0.02, yy + 0.51, alpha=60)
            text(s, rx, yy + 0.92, rw, 0.4, item["label"], 9.5, NAVY_TXT, spacing=1.08)
            l = text(s, rx, yy + 1.34, rw, 0.2, item["source"], 7.5, NAVY_TXT)
            link(l, item["url"])

    hline(s, M, 4.98, SW - 2 * M, alpha=18)
    text(s, M, 5.08, 2.0, 0.22, "TELECOM TRACK RECORD", 7, WHITE, font=SEMI, cs=1.2)
    text(s, M + 1.95, 5.08, SW - 2 * M - 1.95, 0.22, CREDENTIALS, 7.5, NAVY_TXT)
    if D.get("footnote"):
        text(s, M, 5.3, SW - 2 * M, 0.22, D["footnote"], 7.5, NAVY_TXT)
    notes(s, D["notes"])
    return s


# ---- deck content -----------------------------------------------------------
AVIATION = "https://accuknox.com/case-studies/aviation"

DECKS = {
    "AISPM": {
        "file": "AccuKnox_TCTS_AISPM",
        "accent": PRIMARY,
        "cover": ("AI Security Posture\nManagement for Telecom",
                  "Find every model, agent and MCP server across the operator estate."),
        "hero": {
            "title": "Every Model, Agent and MCP Server Sits in One Live Inventory",
            "definition": ("AISPM discovers the models, agents, datasets and MCP servers "
                           "across your clouds. It then ranks each asset by risk."),
            "facts": [("Agentless", "Connects through a cloud role. No install on a VM."),
                      ("3 deploy modes", "SaaS, on-prem or fully air-gapped.")],
            "video": "rMc-fV5kzvs", "start": 35, "poster": "poster_a.jpg",
            "video_title": "Protect LLM and ML with AccuKnox AI-SPM", "duration": "2:34",
            "video_note": "The video starts at 0:35, where the console screens begin.",
            "notes": ("Source: accuknox.com/platform/ai-security (live, agentless inventory). "
                      "Help docs: how-to/aiml-overview.md (agentless cloud SDK needs a cloud role only), "
                      "how-to/aiml-saas-vs-onprem.md (air-gapped support). "
                      "The embedded video needs an internet connection in the room."),
        },
        "screen": {
            "title": "One Dashboard Lists Every AI Asset\nand Ranks Its Risk",
            "main": "a3_dashboard.png",
            "insets": [{"img": "a3_shadow_categories.png", "x": 6.62, "y": 2.92, "w": 3.1}],
            "pins": [(1, "main", 185, 232), (2, "main", 100, 490), (3, "main", 722, 636),
                     (4, 0, 600, 357)],
            "rail": [("Every AI asset, counted", "Apps, models, datasets and compute in one view."),
                     ("Agents across clouds", "Copilot Studio, AI Foundry and Bedrock agents in one list."),
                     ("Riskiest agents first", "Each agent shows its critical and high findings."),
                     ("Shadow AI by category", "Unapproved agents, SDKs, gateways and MCP servers.")],
            "notes": ("Screens: AI Security Dashboard and the Unmanaged (Shadow AI) asset view. "
                      "Knowledge-base and agent names are masked because the demo tenant carries "
                      "customer-like data."),
        },
        "depth": [
            ("lanes", {
                "title": "Four Discovery Modes Reach Cloud, VM,\nOn-Prem and SaaS AI",
                "hub": "AccuKnox control plane",
                "hub_sub": "One tenant, one inventory, one findings queue.",
                "lanes": [
                    ("Agentless cloud SDK", "Cloud AI platforms",
                     "AWS Bedrock and AgentCore, Azure AI Foundry and Copilot Studio, GCP Vertex and Agents Platform"),
                    ("Agentless VM snapshot scan", "Cloud virtual machines",
                     "Unmanaged models and inference engines running on cloud VMs"),
                    ("Agent-based VM scan", "On-prem servers and endpoints",
                     "AI agents, MCP servers, inference engines and AI gateways"),
                    ("Browser plugin", "SaaS AI apps",
                     "Claude.ai, ChatGPT, Gemini, Microsoft Copilot, GitHub Copilot"),
                ],
                "strip_label": "THE FIRST WEEK",
                "strip": [("Day 0", "Connect a cloud role."),
                          ("Minutes", "The first inventory lands."),
                          ("Hours", "Findings and shadow AI land."),
                          ("Day 7", "Air-gapped rollout done.")],
                "footnote": "Discovery modes from the AccuKnox onboarding deck, August 2026. Timings from the AI-GRC page and the Indian bank case study.",
                "notes": ("Deck B slide 14 lists the four modes and the managed and unmanaged asset types. "
                          "The shadow AI rules engine alerts when an unapproved AI app appears in cloud or on-prem."),
            }),
            ("image", {
                "title": "AccuKnox Scans the Platforms Your\nModels Already Run On",
                "image": "a5_platforms.png", "img_x": 3.45, "img_y": 1.55, "img_w": 6.0,
                "rail": [("Managed and on-prem", "Both sides of the estate land in one inventory."),
                         ("Five model formats", "Model and dataset scans run before deployment."),
                         ("Mapped to frameworks", "Findings carry OWASP LLM Top 10 and MITRE ATLAS tags.")],
                "chips": ("INCIDENTS ROUTE INTO", ["Jira", "ServiceNow", "Slack", "PagerDuty"]),
                "chips_y": 5.0,
                "footnote": "Platform grid from the AccuKnox AI security deck, June 2026. Formats and routing from accuknox.com/platform/ai-security.",
                "notes": ("The grid splits managed deployments (SageMaker, Bedrock, Google AI Studio, Azure AI Studio, "
                          "Anthropic, OpenAI, Vertex AI, Nutanix) from on-prem ones (Ollama, vLLM, NVIDIA run:ai, "
                          "Hugging Face, Nutanix, Kubeflow, NVIDIA NIM Operator)."),
            }),
            ("modules", {
                "title": "AI-SPM Is One of Eight Modules\non One Control Plane",
                "highlight": "AI-SPM",
                "image": "a6_compliance.png", "img_w": 5.5, "img_y": 1.9,
                "strip_label": "WHAT AI-SPM COVERS",
                "depth": [("Live inventory", "Models, agents, datasets and pipelines, without an agent."),
                          ("Shadow AI", "Unapproved notebooks, SDKs, gateways and MCP servers."),
                          ("Evidence", "Twelve frameworks in the selector, from OWASP LLM to RBI.")],
                "footnote": "Module set from the AccuKnox solution architecture, August 2026. Beta status from the AI-Security 2.0 launch, 23 March 2026.",
                "notes": ("The selector shows GDPR, HIPAA, HITRUST CSF, ISO 27001-2022, ISO 27017, MITRE AWS Attack "
                          "Framework, NIST 800-171, NIST SP 800-53, OWASP Top 10 for LLM v2025, PCI, RBI CSF and RBI IT "
                          "Framework Master Direction. RBI entries matter for Indian regulated buyers."),
            }),
            ("image", {
                "title": "SaaS in Minutes, On-Prem in Hours,\nAir-Gapped Either Way",
                "image": "a7_parity.png", "img_x": 0.55, "img_y": 1.55, "img_w": 8.9,
                "rail": [], "card": False,
                "chips": ("SAME ON BOTH", ["Prompt Firewall", "AI detect and respond", "Collector scanning", "Governance"]),
                "chips_y": 4.78,
                "footnote": "Deployment card from the AccuKnox AI security deck, June 2026. Air-gapped support is also in the help docs.",
                "notes": ("On-prem adds a Neo4j database, and GPUs are recommended for the Prompt Firewall. "
                          "SaaS results export to your own S3 bucket with 90-day retention."),
            }),
        ],
        "demo": {
            "title": "Watch AISPM Onboard a Cloud Account\nand Rank Its AI Risk",
            "video": "qTDQjmm8698", "poster": "poster_a_demo.jpg",
            "video_title": "AI Asset Onboarding and Overview", "duration": "3:14",
            "video_note": "Narrated walkthrough, from onboarding to findings.",
            "chapters": [
                ("0:04", "Set up", "Add a cloud account in settings"),
                ("0:33", "Set up", "Access keys or a Terraform script"),
                ("1:16", "Set up", "Turn on AI/ML assets, connect"),
                ("1:40", "In action", "Posture, risk and compliance"),
                ("2:13", "In action", "One model and its scan results"),
                ("2:45", "Evidence", "Filter findings by severity"),
            ],
            "notes": ("Published AccuKnox walkthrough, embedded unedited. Chapter times come from the video "
                      "captions. The console navigation in this recording reads AI/ML Security."),
        },
        "usecases": {
            "title": "Shadow AI Hides in the NOC,\nthe Care Desk and the Bid Team",
            "zones": [
                ("Care desk", "Care bots and agent assist",
                 [("AI agent", True, 2), ("Knowledge base", False, 2)]),
                ("Bid team", "Proposal generator on RAG",
                 [("Copilot agent", True, 2), ("Knowledge base", False, 2)]),
                ("OSS / BSS", "Order and inventory APIs",
                 [("MCP server", True, 2), ("AI SDK", True, 2)]),
                ("NOC", "Cognitive NOC, RAN prediction",
                 [("Model", False, 1), ("Notebook", True, 1)]),
                ("Telco cloud", "Inference and GPU nodes",
                 [("Inference engine", False, 1), ("AI gateway", True, 1)]),
            ],
            "cases": [
                ("Models behind the NOC", "List every model and notebook behind RAN prediction.",
                 "INTELLIGENT NOC"),
                ("Agents that read your files", "See which agents read which knowledge bases.",
                 "TOOLS AND AUTOMATION"),
                ("Evidence for the auditor", "Map findings to OWASP LLM Top 10 and NIST AI RMF.",
                 "SECURITY ADVISORY"),
            ],
            "footnote": ("EU AI Act high-risk duties start 2 December 2027 under Regulation (EU) 2026/1744. "
                         "Shadow AI categories as listed on accuknox.com/platform/ai-security."),
            "notes": ("Asset categories come from the Shadow AI view: AI agents, AI gateways, inference "
                      "engines, AI-ML libraries, AI SDKs and MCP servers. The zone contents are an "
                      "illustration of where these assets turn up, not a customer scan. "
                      "TCTS services: Intelligent NOC, Tools and Automation (Neo Automata), "
                      "Security Consulting and Advisory."),
        },
        "proof": {
            "title": "A Global Airline Inventoried\n1,500+ Models Within Days",
            "big": "1,500+",
            "big_label": "models in one live inventory across three clouds, within days",
            "big_source": "Global airline case study  ·  accuknox.com/case-studies/aviation",
            "big_url": AVIATION,
            "quote": "AccuKnox gives us the protection we need for our cloud AI infrastructure …",
            "quote_by": "Head of Cloud and AI Security, global airline",
            "right": [
                {"kind": "stat", "value": "40",
                 "label": "shadow Copilot agents discovered automatically at the same airline",
                 "source": "accuknox.com/case-studies/aviation", "url": AVIATION},
                {"kind": "stat", "value": "7 days",
                 "label": "for a fully air-gapped rollout at a top-3 Indian public sector bank, with AI-BOM covered",
                 "source": "accuknox.com/case-studies/sbom-india-bank",
                 "url": "https://accuknox.com/case-studies/sbom-india-bank"},
            ],
            "notes": ("Sources: aviation case study (1,500+ models, 40 shadow Copilot agents, quote). "
                      "Indian bank case study (7-day air-gapped deployment, five BOM types including AI-BOM). "
                      "Track record: IDT and US DoD case studies, Tata Elxsi press release (Feb 2024), "
                      "5G Open Innovation Lab press release, 5G security page (LF Nephio TSC)."),
        },
    },
    "PF": {
        "file": "AccuKnox_TCTS_Prompt_Firewall",
        "accent": RED,
        "cover": ("AI Guardrails and Prompt\nFirewall for Telecom",
                  "Inspect every prompt and reply before it reaches a subscriber."),
        "hero": {
            "title": "The Firewall Tracks Whole Conversations to Stop Slow Jailbreaks",
            "definition": ("A transparent proxy inspects every prompt and reply. It then blocks, "
                           "sanitizes or monitors each one."),
            "facts": [("14 policy types", "Prompt injection, toxicity, secrets, PII and PHI, banned topics."),
                      ("4 ways to deploy", "Browser, gateway or proxy, SDK, cloud API gateway.")],
            "video": "tlSplOfDFu4", "start": None, "poster": "poster_b.jpg",
            "video_title": "Why Every Enterprise Needs a Prompt Firewall NOW?", "duration": "2:58",
            "video_note": "Prompt and response policies, and a blocked jailbreak.",
            "notes": ("Sources: accuknox.com/solutions/prompt-firewall (14 built-in policy types, "
                      "four deployment modes, block, sanitize, monitor). accuknox.com/platform/ai-security "
                      "(conversations tracked over 5 to 15 messages). "
                      "The embedded video needs an internet connection in the room."),
        },
        "screen": {
            "title": "Policies, Verdicts and Violations\nShare One Screen",
            "main": "b3_dashboard.png",
            "insets": [{"img": "b3_blocked_chat.png", "x": 3.2, "y": 4.18, "w": 3.6}],
            "pins": [(1, "main", 330, 348), (2, "main", 1590, 461), (3, "main", 560, 462),
                     (4, 0, 1470, 32)],
            "rail": [("Coverage at a glance", "Protected apps, total queries and total violations."),
                     ("Policies that fire most", "Each policy lists its violations and severity."),
                     ("Blocked or monitored", "Each app splits its violations by action."),
                     ("The user sees the block", "The chat stops the prompt and names the policy.")],
            "notes": ("Screens: AI Security Dashboard, Prompt Firewall tab (demo data, fictional users), "
                      "and the browser extension blocking a prompt injection."),
        },
        "depth": [
            ("pipeline", {
                "title": "Five Stages Run on Every Prompt and Every Reply",
                "stages": [
                    ("01", "Normalize", "Decode unicode and homoglyph tricks before any classifier reads the text."),
                    ("02", "Classify", "Injection, jailbreak, personal data and toxicity screens run on the turn."),
                    ("03", "Contextualize", "Join the turn with session identity, history and the tool-call ledger."),
                    ("04", "Score", "Risk accumulates across the session, not one prompt at a time."),
                    ("05", "Enforce", "Allow, sanitize, block or step up. Every turn lands in the audit trail."),
                ],
                "band": ("Session context engine",
                         "A low-latency store keyed by session, agent and user. It holds identity, a rolling "
                         "summary and the cumulative risk score. Stages three to five read it.",
                         "< 50 ms", "p95 latency per request"),
                "footnote": ("Pipeline from the AccuKnox AI security deck, June 2026. Latency from "
                             "accuknox.com/platform/ai-governance-compliance."),
                "notes": ("This is the stateful core. A per-prompt firewall sees turn 7 alone and allows it. "
                          "The session map catches the pattern that built up over turns 1 to 6."),
            }),
            ("image", {
                "title": "Four Integration Modes Put the Firewall\nWhere the Prompts Are",
                "image": "b5_modes.png", "img_x": 6.75, "img_y": 1.45, "img_w": 2.7,
                "rail": [("Browser plugin extension", "SaaS AI chat and workflow apps, on the user's browser."),
                         ("Gateway proxy configuration", "Developer CLI tools, through your own proxy."),
                         ("SDK or proxy mode", "Local AI agents, with a few lines in the app."),
                         ("Cloud SDK or API gateway", "Cloud AI agents, at the gateway in front of them.")],
                "rail_top": 1.62, "rail_step": 0.92, "rail_w": 5.6,
                "footnote": "Integration modes and their platforms from the AccuKnox onboarding deck, August 2026.",
                "notes": ("A seller should ask which surface the operator worries about first. The browser plugin needs "
                          "no application change, and the SDK gives the tightest control."),
            }),
            ("modules", {
                "title": "AI Guardrails Is One of Eight Modules\non One Control Plane",
                "highlight": "AI Guardrails",
                "image": "b6_prompt_policies.png", "img_w": 5.5, "img_y": 1.95,
                "strip_label": "POLICY DEPTH",
                "depth": [("Prompt policies", "Injection, secrets, toxicity, banned topics, language, token limits."),
                          ("Response policies", "Sensitive data, JSON validation, code language, deanonymize."),
                          ("Scope", "Global or per app, plus custom regex and domain rules.")],
                "footnote": "Policy libraries from the AccuKnox AI security deck, June 2026. Scope from accuknox.com/solutions/prompt-firewall.",
                "notes": ("The screen shows the prompt library. The response library carries Deanonymize, Gibberish, "
                          "Toxicity, JSON, Ban Competitors, Ban Topics, Sensitive, Code, Language and Regex."),
            }),
            ("matrix", {
                "title": "Every AI Surface Has a Way In",
                "cols": [("SURFACE", 2.1), ("WHAT RUNS THERE", 4.2), ("HOW THE FIREWALL CONNECTS", 3.1)],
                "rows": [
                    ["SaaS AI apps", "Claude.ai, ChatGPT, Gemini, Microsoft Copilot, GitHub Copilot",
                     "Browser plugin extension"],
                    ["Cloud AI agents", "Azure Copilot Studio and Power Apps, AWS Bedrock AgentCore, GCP Agents Platform",
                     "Cloud SDK mode or cloud API gateway"],
                    ["Developer AI tools", "Claude Code, Codex, AntiGravity", "Gateway proxy configuration"],
                    ["Local AI agents", "LangGraph, n8n", "SDK mode, or proxy and gateway mode"],
                ],
                "chips": [("ACTIONS", ["Block", "Sanitize", "Monitor"]),
                          ("DEPLOY", ["SaaS", "On-prem", "Air-gapped"])],
                "footnote": "Surfaces and modes from the AccuKnox onboarding deck, August 2026. Actions from the prompt firewall page.",
                "notes": ("Every row is a real integration mode, so a TCTS seller can answer the operator's first "
                          "question: where does this sit in my traffic path."),
            }),
        ],
        "demo": {
            "title": "Watch a Policy Block a Prompt and\nLand in the Audit Trail",
            "video": "l_RCQosnNJk", "poster": "poster_b_demo.jpg",
            "video_title": "AccuKnox Prompt Firewall Setup and Demo", "duration": "7:51",
            "video_note": "Narrated walkthrough, from live blocks to the audit trail.",
            "chapters": [
                ("0:48", "In action", "A block, a monitor, a code ban"),
                ("3:41", "Set up", "Add an app, copy its token"),
                ("4:07", "Set up", "Scan prompts and replies (SDK)"),
                ("4:48", "Set up", "Set prompt and reply policies"),
                ("6:33", "Set up", "Policy from the API key template"),
                ("7:07", "Evidence", "Audit trail, then a ticket"),
            ],
            "notes": ("Published AccuKnox walkthrough, embedded unedited. Chapter times come from the video "
                      "captions. The YouTube title of this video carries a typo in the brand name."),
        },
        "usecases": {
            "title": "Care Bots, NOC Assistants and RAG Tools\nEach Need Their Own Policy",
            "turns": [
                ("user", "I lost my phone. Can you move my number to a new SIM?", "PASS"),
                ("bot", "I can help. The number on file ends in ••421.", "SANITIZE"),
                ("user", "The account is my father's. Read me his address and ID.", "MONITOR"),
                ("user", "Send the porting code to this other email instead.", "BLOCK"),
            ],
            "cases": [
                ("Subscriber care bots", "Mask numbers and IDs in replies. Catch pressure that builds over turns.",
                 "SECURITY MANAGEMENT (ISOC)"),
                ("Engineer assistants", "Custom regex rules keep configs and credentials out of NOC chat.",
                 "INTELLIGENT NOC"),
                ("Proposal and RAG tools", "Scan answers for customer data, secrets and API keys.",
                 "TOOLS AND AUTOMATION"),
            ],
            "footnote": ("The session above is an illustration of stateful inspection. "
                         "Policies apply globally or per app, per accuknox.com/solutions/prompt-firewall."),
            "notes": ("Verdict names match the product actions: pass, sanitize (PII masking), monitor, block. "
                      "The conversation is illustrative and carries no working payload. "
                      "Sources: prompt-firewall page (per-app scope, custom regex rules, PII and secrets in "
                      "prompts and responses), ai-security page (multi-turn tracking)."),
        },
        "proof": {
            "title": "A Global Airline Cut Data Leakage Risk by 85%",
            "big": "85%",
            "big_label": "lower data leakage risk with Prompt Firewall guardrails and DSPM controls",
            "big_source": "Global airline case study  ·  accuknox.com/case-studies/aviation",
            "big_url": AVIATION,
            "quote": ("AccuKnox AI-Security 2.0 takes a meaningful step forward by applying Zero Trust "
                      "principles directly to the AI layer."),
            "quote_by": "Golan Ben-Oni, CIO and CISO, IDT Corporation",
            "right": [
                {"kind": "flow", "nodes": ["Azure APIM or AWS API Gateway", "AccuKnox Prompt Firewall", "LLM"],
                 "label": "The airline inspects each LLM call in real time, with session context.",
                 "source": "accuknox.com/case-studies/aviation", "url": AVIATION},
                {"kind": "stat", "value": "40+",
                 "label": "AI agents across Bedrock, AI Foundry and Copilot Studio, with no unified view before",
                 "source": "accuknox.com/case-studies/aviation", "url": AVIATION},
            ],
            "notes": ("Sources: aviation case study (85% lower data leakage risk through Prompt Firewall "
                      "guardrails and DSPM controls, LLM-as-a-judge inspection via Azure APIM and AWS API "
                      "Gateway with session context, 40+ agents). IDT quote: AI-Security 2.0 launch press "
                      "release, 23 March 2026."),
        },
    },
    "AGENTIC": {
        "file": "AccuKnox_TCTS_Agentic_MCP",
        "accent": SECOND,
        "cover": ("Agentic AI and MCP\nSecurity for Telecom",
                  "Least privilege for every agent, tool call and MCP server."),
        "hero": {
            "title": "Each Agent Runs in a Kernel Sandbox With Only the Tools It Needs",
            "definition": ("KubeArmor enforces a sandbox per agent in the kernel. Processes, files, "
                           "credentials and network access stay on an allowlist. AccuKnox also "
                           "validates MCP calls in real time."),
            "facts": [("No code changes", "The kernel enforces the sandbox through eBPF and LSM."),
                      ("Approval gates", "High-risk actions wait for a human to approve.")],
            "video": "mAzLWcr59g0", "start": None, "poster": "poster_c.jpg",
            "video_title": "AgentZ product tour: sandboxes, approvals and MCP profiling", "duration": "1:25",
            "video_note": "No voice track, so the presenter can talk over it.",
            "notes": ("Sources: accuknox.com/solutions/agentic-ai-security (runtime sandbox via eBPF and LSM, "
                      "no code changes, mandatory approval for high-risk actions, real-time MCP validation). "
                      "AI Identity (SPIFFE per agent) was Beta at the RSAC 2026 launch, so it stays off this slide. "
                      "The embedded video is the AgentZ product tour. It shows agent sandboxes and MCP tool "
                      "profiling. It has no voice track."),
        },
        "screen": {
            "title": "The Agent Graph Shows Every Tool and\nKnowledge Base an Agent Can Reach",
            "main": "c3_agent_graph.png",
            "insets": [{"img": "c3_sandbox_yaml.png", "x": 8.02, "y": 2.9, "w": 1.72},
                       {"img": "c3_mcp_rows.png", "x": 3.2, "y": 4.6, "w": 3.0}],
            "pins": [(1, "main", 1386, 778), (2, "main", 2004, 309), (3, 0, 215, 305),
                     (4, 1, 930, 26)],
            "rail": [("Every agent, mapped", "Cloud, resource group, project and agent in one graph."),
                     ("What agents can reach", "Tools and knowledge bases, counted per agent."),
                     ("Kernel sandbox policy", "Block credential paths. Allow only listed processes."),
                     ("MCP servers found", "MCP packages surface in the Shadow AI inventory.")],
            "notes": ("Screens: Assets > Agents graph (Azure AI Foundry), a KubeArmor sandbox policy for an "
                      "agentic namespace, and MCP packages in the Shadow AI view."),
        },
        "depth": [
            ("sandbox", {
                "title": "The Sandbox Wraps Agents and Untrusted\nModels at the Kernel",
                "sources": [("On-prem model serving", "Ollama, vLLM, NVIDIA Triton, Dynamo, RunAI"),
                            ("On-prem AI agents", "LangGraph, n8n"),
                            ("Cloud AI agents", "Copilot Studio, Bedrock AgentCore, AI Foundry")],
                "runtime": "VM   ·   CONTAINERS   ·   KUBERNETES",
                "sandbox": "KERNEL SANDBOX  ·  eBPF AND LSM",
                "controls": ["Process and file system isolation", "Network isolation", "Domain access isolation"],
                "plane": ("AccuKnox control plane", "Policies, alerts and full telemetry for every blocked action"),
                "strip_label": "WHAT IT STOPS",
                "strip": [("Hidden triggers", "Behaviour fires on one input."),
                          ("Model poisoning", "A swapped model file."),
                          ("Training data poisoning", "Datasets edited before a run.")],
                "footnote": "Deployment targets, isolation types and untrusted-model risks from the AccuKnox onboarding deck, August 2026.",
                "notes": ("The same engine runs for agents and for untrusted models, because both are processes that "
                          "the kernel can bound. Nothing changes inside the agent."),
            }),
            ("image", {
                "title": "Agents, Models and MCP Servers Plug\nInto the Stack You Run",
                "image": "c5_platforms_onprem.png", "img_x": None, "img_y": 1.6, "img_w": None, "img_h": 3.2,
                "rail": [("Agent platforms", "Azure AI Foundry, Copilot Studio and AWS Bedrock."),
                         ("Agent frameworks", "LangGraph and n8n, on VMs, containers or Kubernetes."),
                         ("MCP servers", "Found in the inventory, then validated call by call."),
                         ("Agent identity", "SPIFFE identity per agent, permissions through OpenFGA. Beta.")],
                "rail_top": 1.6, "rail_step": 0.82, "rail_w": 4.6,
                "chips": ("RUNS ON", ["VM", "Containers", "Kubernetes", "Air-gapped"]),
                "chips_y": 5.0,
                "footnote": "Platform grid from the June 2026 deck. Identity and MCP validation from the agentic page, where identity is Beta.",
                "notes": ("The grid shows Ollama, vLLM, NVIDIA run:ai, Hugging Face, Nutanix, Kubeflow and the NVIDIA "
                          "NIM Operator. Telecom edge sites usually run one of these."),
            }),
            ("modules", {
                "title": "Agentic AI Security Is One of Eight\nModules on One Control Plane",
                "highlight": "Agentic AI Security",
                "image": "c6_runtime_policies.png", "img_w": 5.5, "img_y": 1.95,
                "strip_label": "HOW POLICIES ARRIVE",
                "depth": [("Discovered", "The platform proposes policies from observed behaviour."),
                          ("Hardening", "Ready-made packs for common attack paths."),
                          ("Custom", "Hand-written KubeArmor policies for one namespace.")],
                "footnote": "Policy list from the AccuKnox AI security deck, June 2026. The counts on screen belong to a demo tenant.",
                "notes": ("The screen shows an agentic-ai namespace with 62 policies: 38 discovered, 21 hardening and 3 "
                          "custom. The open policy blocks access to credential directories."),
            }),
            ("matrix", {
                "title": "One Engine Covers Every Place an Agent Runs",
                "cols": [("WORKLOAD", 2.2), ("WHERE IT RUNS", 3.4), ("WHAT THE KERNEL ENFORCES", 3.8)],
                "rows": [
                    ["AI agents", "Kubernetes, containers and VMs",
                     "Process, file, credential and network isolation"],
                    ["MCP servers", "Kubernetes and VMs", "Inventory first, then least-privilege tool access"],
                    ["Inference engines", "On-prem model serving on GPU nodes", "A sandbox around untrusted models"],
                    ["Notebooks", "JupyterHub on Kubernetes", "Allowlisted processes and directories"],
                ],
                "chips": [("POSTURES", ["Audit", "Block"]),
                          ("DEPLOY", ["SaaS", "On-prem", "Air-gapped"])],
                "footnote": "Workloads and isolation from the AccuKnox onboarding deck, August 2026, and the agentic page.",
                "notes": ("Audit first, then block, is the rollout order the Jupyter demo shows. "
                          "A telecom edge site usually starts in audit for a week."),
            }),
        ],
        "demo": {
            "title": "Watch a Kernel Policy Stop an\nExploit Inside a Notebook",
            "video": "mW8GcoRBuiY", "poster": "poster_c_demo.jpg",
            "video_title": "Prevent Malicious Code Execution in Jupyter Notebook", "duration": "2:40",
            "video_note": "Narrated walkthrough, from exploit to alert.",
            "chapters": [
                ("0:09", "In action", "A notebook shell runs anything"),
                ("0:34", "Set up", "Pick a KubeArmor policy"),
                ("1:16", "Set up", "Activate it in audit mode"),
                ("1:50", "Set up", "Switch the posture to block"),
                ("1:57", "In action", "The exploit script fails"),
                ("2:11", "Evidence", "Alert with workload and command"),
            ],
            "notes": ("Published AccuKnox walkthrough, embedded unedited. Chapter times come from the video "
                      "captions. The same KubeArmor sandbox applies to agent workloads."),
        },
        "usecases": {
            "title": "NOC Agents Need Deny-by-Default\nBefore They Touch Live Config",
            "controls": ["Allowed processes only", "No access to credential files", "Egress to listed hosts only"],
            "tools": [("MCP  ·  Ticketing", "ALLOWED"), ("MCP  ·  Inventory", "ALLOWED"),
                      ("MCP  ·  Config push", "NEEDS APPROVAL")],
            "cases": [
                ("NOC remediation agents", "Sandbox each agent and hold config pushes for approval.",
                 "NEO AUTOMATA"),
                ("MCP servers on OSS and BSS", "Find every MCP server and limit the tools agents call.",
                 "INTELLIGENT NOC"),
                ("Agents at the edge", "Run the same kernel sandbox on-prem and air-gapped.",
                 "TELCO CLOUD"),
            ],
            "footnote": ("GSMA (June 2025) advises deny-by-default for every inference-triggered action. "
                         "Deutsche Telekom's RAN Guardian took 100+ actions in its first month."),
            "notes": ("Sources: GSMA Agentic AI for Telco white paper (June 2025). Deutsche Telekom newsroom "
                      "(RAN Guardian, MINDR). TM Forum Inform (MCP for BSS). AccuKnox agentic page (egress "
                      "allowlists, approval for high-risk actions, MCP validation). The loop is an illustration."),
        },
        "proof": {
            "title": "IDT Put Kernel Enforcement on\n30,000 Devices in One Week",
            "big": "30,000",
            "big_label": "devices onboarded at IDT within a week, with an attack stopped inline during the evaluation",
            "big_source": "IDT Telecom case study  ·  accuknox.com/case-studies/idt-telecom",
            "big_url": "https://accuknox.com/case-studies/idt-telecom",
            "quote": ("Choosing AccuKnox was driven by opensource KubeArmor's novel use of eBPF and LSM "
                      "technologies, delivering runtime security"),
            "quote_by": "Golan Ben-Oni, Chief Information Officer, IDT",
            "right": [
                {"kind": "stat", "value": "100%",
                 "label": "of traffic between 5G network functions visible in the US DoD 5G project, with no 5G slowdown",
                 "source": "accuknox.com/case-studies/us-dod",
                 "url": "https://accuknox.com/case-studies/us-dod"},
                {"kind": "stat", "value": "30 of 36",
                 "label": "criteria passed on the first run in an air-gapped tier-1 telco POC with AI agent workloads",
                 "source": "accuknox.com/blog/global-telco-container-runtime-security",
                 "url": "https://accuknox.com/blog/global-telco-container-runtime-security"},
            ],
            "footnote": ("These three results prove the kernel runtime that sandboxes agents. "
                         "The airline case shows eBPF controls blocking unsafe tool use on AKS."),
            "notes": ("Sources: IDT case study (30,000 devices in a week, CIO quote), US DoD case study (100% of "
                      "traffic between 5G network functions, no degradation of 5G performance), telco POC blog "
                      "(30 of 36 criteria on the first run, air-gapped, internal AI agent workloads), aviation "
                      "case study (eBPF runtime controls on AKS blocking unsafe tool usage)."),
        },
    },
}


DEPTH_BUILDERS = {"lanes": lanes, "pipeline": pipeline, "sandbox": sandbox_arch,
                  "image": image_slide, "modules": module_map, "matrix": matrix}


def build(key):
    D = DECKS[key]
    acc = D["accent"]
    prs = new_deck()
    prs.core_properties.title = D["cover"][0].replace("\n", " ")
    prs.core_properties.author = "AccuKnox"
    cover_slide(prs, D["cover"][0], subtitle=D["cover"][1])
    hero(prs, D["hero"], acc)
    annotated(prs, D["screen"], acc)
    for builder, data in D["depth"]:
        DEPTH_BUILDERS[builder](prs, data, acc)
    demo(prs, D["demo"], acc)
    {"AISPM": estate_lane, "PF": firewall_session, "AGENTIC": noc_loop}[key](prs, D["usecases"], acc)
    proof(prs, D["proof"], acc)
    closing_slide(prs)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = OUTDIR / f"{D['file']}.pptx"
    prs.save(str(out))
    print("saved", out)
    return out


if __name__ == "__main__":
    keys = sys.argv[1:] or list(DECKS)
    for k in keys:
        build(k)
