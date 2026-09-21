# -*- coding: utf-8 -*-
"""
AI Red Teaming Stack Ranking, AccuKnox branded, editable PowerPoint.

Data (criteria, cell states, scores, head to head, sources, gallery) is imported
from build_redteam_stack_ranking.py, so the PDF and the deck can never disagree.
Every visual is a native shape, table or text box.

Build:   py -3.11 scripts/build_redteam_stack_ranking_pptx.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_AI_Red_Teaming_Stack_Ranking.pptx -Out output/render/redteam
"""
import os
import shutil
import sys

from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _akdeck import *  # noqa: F401,F403
import build_redteam_stack_ranking as D

SRC = os.path.join(HERE, "..", "PPT Template.pptx")
OUT = os.path.join(HERE, "..", "output", "AccuKnox_AI_Red_Teaming_Stack_Ranking.pptx")
ASSETS = os.path.join(HERE, "..", "output", "assets", "redteam")
os.makedirs(ASSETS, exist_ok=True)

shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_STD = prs.slide_layouts[4]
for sid in list(prs.slides._sldIdLst):
    try:
        prs.part.drop_rel(sid.get(qn("r:id")))
    except Exception:
        pass
    prs.slides._sldIdLst.remove(sid)

MARK = {"y": GREEN, "p": SECOND, "n": RED}
TINT = RGBColor(0xF4, 0xF7, 0xFF)
Y0 = 0.92          # first content line under the title band
YMAX = 5.30        # last content line


def std(title):
    s = prs.slides.add_slide(L_STD)
    set_title(s, title)
    blank_footer(s)
    return s


def cell_text(cell, parts, size, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """parts: list of paragraphs, each a list of (text, color, bold)."""
    cell.vertical_anchor = anchor
    tf = cell.text_frame
    tf.word_wrap = True
    for i, runs_ in enumerate(parts):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if i:
            p.space_before = Pt(2)
        for text, color, bold in runs_:
            r = p.add_run()
            r.text = text
            r.font.name = FONT
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color


def grid(slide, x, y, colw, rows_h, data, fills):
    """data[r][c] = list of paragraphs, fills[r][c] = RGBColor."""
    t = slide.shapes.add_table(len(rows_h), len(colw), Inches(x), Inches(y),
                               Inches(sum(colw)), Inches(sum(rows_h))).table
    t.first_row = False
    t.horz_banding = False
    for i, w in enumerate(colw):
        t.columns[i].width = Inches(w)
    for r, h in enumerate(rows_h):
        t.rows[r].height = Inches(h)
    return t


def chip_w(text, size):
    return len(text) * size / 72.0 * 0.50 + 0.24


# ================================================================ 1. cover
cover_slide(prs, "AI Red Teaming Stack Ranking")

# ================================================================ 2. ranking
s = std("AI Red Teaming Stack Ranking")
sc = D.scores()
# winner card
box(s, CX, Y0, 3.55, 3.72, fill=PRIMARY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, CX + 0.25, Y0 + 0.18, 3.0, 0.28, text="RANK 1", size=11, color=NAVY_TXT, bold=True)
box(s, CX + 0.25, Y0 + 0.44, 3.1, 0.56, text="AccuKnox", size=30, color=WHITE, bold=True)
b = box(s, CX + 0.25, Y0 + 1.00, 3.1, 0.86, anchor=MSO_ANCHOR.TOP)
p = b.text_frame.paragraphs[0]
runs(p, str(sc["ak"]), size=54, bold=True, color=WHITE)
runs(p, " / %d" % D.MAX, size=20, bold=True, color=NAVY_TXT)
for i, (bold_txt, rest_txt) in enumerate([("30,000+", " probes, 20+ categories"),
                                          ("Intelligent", " context probes"),
                                          ("Air-gapped", " deployment"),
                                          ("7", " compliance frameworks")]):
    yy = Y0 + 2.02 + i * 0.41
    box(s, CX + 0.25, yy, 3.05, 0.01, fill=RGBColor(0x4D, 0x7D, 0xFF))
    t = box(s, CX + 0.25, yy + 0.04, 3.1, 0.36, anchor=MSO_ANCHOR.MIDDLE)
    runs(t.text_frame.paragraphs[0], bold_txt, size=12.5, bold=True, color=WHITE)
    runs(t.text_frame.paragraphs[0], rest_txt, size=12.5, color=WHITE)
# the rest
rx, rw = 4.25, 5.35
others = [r for r in D.ranked() if r[2][0] != "ak"]
rh = 3.72 / len(others)
for i, (rank, tie, (k, name, _prod), score) in enumerate(others):
    yy = Y0 + i * rh
    box(s, rx, yy, 0.45, rh, text=str(rank), size=22, bold=True, color=GREY_TX,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, rx + 0.5, yy + 0.08, 2.9, 0.34, text=name, size=15, bold=True, color=INK)
    box(s, rx + 0.5, yy + 0.40, 2.95, 0.3, text=D.VERDICT[k], size=10, color=MUTE)
    t = box(s, rx + 3.55, yy + 0.08, 1.8, 0.36, align=PP_ALIGN.RIGHT)
    runs(t.text_frame.paragraphs[0], str(score), size=17, bold=True, color=NAVY)
    runs(t.text_frame.paragraphs[0], " / %d" % D.MAX, size=10, bold=True, color=MUTE)
    box(s, rx + 3.65, yy + 0.50, 1.7, 0.09, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    box(s, rx + 3.65, yy + 0.50, 1.7 * score / D.MAX, 0.09, fill=SECOND,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    if i < len(others) - 1:
        box(s, rx, yy + rh - 0.005, rw, 0.01, fill=GREY_BD)
# scope strip
strip = box(s, CX, 4.76, CW, 0.50, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12,
            anchor=MSO_ANCHOR.MIDDLE, ml=0.2)
runs(strip.text_frame.paragraphs[0], "Red teaming only.  ", size=11, bold=True, color=NAVY)
runs(strip.text_frame.paragraphs[0],
     "AccuKnox also ships AI-SPM, AI-DR, Prompt Firewall, Model and Dataset Security, "
     "Agentic AI Security and CTEM.", size=11, color=NAVY)

# ================================================================ 3. matrix
s = std("Capability Matrix")
colw = [1.24] + [1.326] * 6
head_h, body_h, tot_h = 0.36, 0.43, 0.34
rows_h = [head_h] + [body_h] * len(D.CRITERIA) + [tot_h]
t = grid(s, CX, 0.86, colw, rows_h, None, None)
ak_col = 1
for c, (k, n, _p) in enumerate([("", "Criterion", "")] + D.VENDORS):
    cell = t.cell(0, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = PRIMARY if k == "ak" else NAVY
    cell_text(cell, [[(n, WHITE, True)]], 9.5 if k != "ak" else 10.5, anchor=MSO_ANCHOR.MIDDLE)
for r, (name, _hint, cells) in enumerate(D.CRITERIA, start=1):
    cell = t.cell(r, 0)
    cell.fill.solid(); cell.fill.fore_color.rgb = WHITE
    cell_text(cell, [[(name, NAVY, True)]], 8.4)
    for c, (k, _n, _p) in enumerate(D.VENDORS, start=1):
        state, txt = cells[k]
        cell = t.cell(r, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = LAV if k == "ak" else WHITE
        cell_text(cell, [[("● ", MARK[state], True),
                          (txt, NAVY if k == "ak" else INK, k == "ak")]], 7.4)
r = len(D.CRITERIA) + 1
cell = t.cell(r, 0); cell.fill.solid(); cell.fill.fore_color.rgb = GREY_BG
cell_text(cell, [[("Score", NAVY, True)]], 11, anchor=MSO_ANCHOR.MIDDLE)
for c, (k, _n, _p) in enumerate(D.VENDORS, start=1):
    cell = t.cell(r, c); cell.fill.solid()
    cell.fill.fore_color.rgb = PRIMARY if k == "ak" else GREY_BG
    cell_text(cell, [[("%d / %d" % (sc[k], D.MAX), WHITE if k == "ak" else NAVY, True)]], 11,
              anchor=MSO_ANCHOR.MIDDLE)
for rr in range(len(rows_h)):
    for cc in range(len(colw)):
        cl = t.cell(rr, cc)
        cl.margin_left = Inches(0.05); cl.margin_right = Inches(0.04)
        cl.margin_top = Inches(0.03); cl.margin_bottom = Inches(0.02)
# legend
lx = CX
for st in "ypn":
    lb = box(s, lx, 5.30, 1.2, 0.22, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    runs(lb.text_frame.paragraphs[0], "● ", size=10, bold=True, color=MARK[st])
    runs(lb.text_frame.paragraphs[0], "%s = %d" % (D.LABEL[st], D.PTS[st]), size=9, color=MUTE)
    lx += 1.25

# ================================================================ 4. AccuKnox red teaming
s = std("AccuKnox AI Red Teaming")
cards = [("30,000+", "Static Red Teaming", PRIMARY,
          ["30,000+ probes, 20+ categories", "Standard policy packs", "OWASP Top 10 for LLMs"]),
         ("Custom", "Intelligent Red Teaming", SECOND,
          ["Probes from your industry context", "JSON, document or direct input", "Presets for support, coding, legal"]),
         ("3 Options", "Deployment Flexibility", NAVY,
          ["SaaS", "Private cloud", "On-premises, air-gapped"])]
cw3, gap = 2.96, 0.16
for i, (big, head, col, items) in enumerate(cards):
    x = CX + i * (cw3 + gap)
    box(s, x, Y0, cw3, 2.92, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, Y0, cw3, 1.12, fill=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    box(s, x, Y0 + 0.9, cw3, 0.22, fill=col)
    box(s, x + 0.2, Y0 + 0.1, cw3 - 0.3, 0.6, text=big, size=28, bold=True, color=WHITE,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.2, Y0 + 0.68, cw3 - 0.3, 0.36, text=head, size=13, bold=True, color=WHITE,
        anchor=MSO_ANCHOR.MIDDLE)
    for j, it in enumerate(items):
        yy = Y0 + 1.30 + j * 0.52
        box(s, x + 0.22, yy + 0.13, 0.12, 0.12, fill=col, shape=MSO_SHAPE.OVAL)
        box(s, x + 0.42, yy, cw3 - 0.55, 0.40, text=it, size=12, color=INK, anchor=MSO_ANCHOR.MIDDLE)
steps = ["Pick Static or Intelligent Scan", "Add model purpose or context",
         "Review generated probes", "Schedule and rescan"]
sw = (CW - 3 * 0.16) / 4
for i, st in enumerate(steps):
    x = CX + i * (sw + 0.16)
    box(s, x, 4.08, sw, 1.14, fill=TINT, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    box(s, x, 4.08, sw, 0.07, fill=NAVY)
    box(s, x + 0.16, 4.26, 0.36, 0.36, text=str(i + 1), size=12, bold=True, color=WHITE,
        fill=NAVY, shape=MSO_SHAPE.OVAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
    box(s, x + 0.12, 4.66, sw - 0.24, 0.5, text=st, size=12, bold=True, color=NAVY)

# ================================================================ 5. gallery
s = std("AccuKnox Red Teaming Gallery")
gw, gh, gg = (CW - 0.2) / 2, 2.02, 0.2
for i, (rel, cap) in enumerate(D.GALLERY):
    src = os.path.join(D.DOCS, rel)
    im = Image.open(src).convert("RGB")
    ratio = gw / (gh - 0.34)
    if "prompt-categories" in rel:
        crop_h = int(im.width / ratio)
        im = im.crop((0, max(0, im.height - crop_h), im.width, im.height))
    else:
        crop_h = min(im.height, int(im.width / ratio))
        im = im.crop((0, 0, im.width, crop_h))
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.Resampling.LANCZOS)
    path = os.path.join(ASSETS, "gallery-%d.png" % (i + 1))
    im.save(path)
    x = CX + (i % 2) * (gw + gg)
    y = 0.90 + (i // 2) * (gh + 0.18)
    box(s, x, y, gw, gh, fill=WHITE, line=GREY_BD, line_w=1.0)
    pic = s.shapes.add_picture(path, Inches(x + 0.01), Inches(y + 0.01), Inches(gw - 0.02), Inches(gh - 0.36))
    pic.shadow.inherit = False
    box(s, x, y + gh - 0.34, gw, 0.34, fill=NAVY)
    box(s, x + 0.1, y + gh - 0.30, 0.26, 0.26, text=str(i + 1), size=10, bold=True, color=WHITE,
        fill=PRIMARY, shape=MSO_SHAPE.OVAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
    box(s, x + 0.44, y + gh - 0.34, gw - 0.5, 0.34, text=cap, size=11.5, bold=True, color=WHITE,
        anchor=MSO_ANCHOR.MIDDLE)

# ================================================================ 6. coverage
s = std("Domain-Specific Red Teaming Coverage")
cats = ["Prompt & Instruction Integrity", "Data Protection & Privacy", "Access Control",
        "Downstream System Injection", "RAG & Knowledge Base", "Agentic & Tool Use",
        "Jailbreak & Guardrail Evasion", "Harmful Content", "Criminal Facilitation",
        "Malicious Code & Supply Chain", "Accuracy & Reliability", "Brand, Legal & Commercial",
        "Fairness & Bias", "Regulated Sectors", "Transparency & Robustness"]
strat = ["Encoding", "Crescendo Multi-Turn", "Multilingual", "Many-Shot", "Role-Play"]
fws = ["OWASP LLM Top 10", "OWASP API Top 10", "MITRE ATLAS", "NIST AI RMF", "EU AI Act",
       "ISO/IEC 42001", "AVID"]


def chips(slide, x, y, w, items, fill, tcolor, size=9, line=None):
    cx, cy, hh = x, y, 0.26
    for it in items:
        cwid = chip_w(it, size)
        if cx + cwid > x + w:
            cx, cy = x, cy + hh + 0.06
        box(slide, cx, cy, cwid, hh, text=it, size=size, bold=True, color=tcolor, fill=fill,
            line=line, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.25,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0.04, mr=0.04)
        cx += cwid + 0.06
    return cy + hh


# banner
ban = box(s, CX, Y0, CW, 0.50, fill=PRIMARY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.14,
          anchor=MSO_ANCHOR.MIDDLE, ml=0.22)
runs(ban.text_frame.paragraphs[0], "15 domain-specific categories.  ", size=13, bold=True, color=WHITE)
runs(ban.text_frame.paragraphs[0], "AccuKnox red teams every one, with static and intelligent probes.",
     size=12, color=WHITE)

# left panel, category tiles
py0 = Y0 + 0.64
ph = 5.44 - py0
lw = 5.55
box(s, CX, py0, lw, ph, fill=TINT, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.03)
tw, gx, gy = (lw - 0.4 - 0.2) / 3, 0.1, 0.1
th = (ph - 0.4 - 4 * gy) / 5
for i, c in enumerate(cats):
    x = CX + 0.2 + (i % 3) * (tw + gx)
    y = py0 + 0.2 + (i // 3) * (th + gy)
    box(s, x, y, tw, th, fill=WHITE, line=GREY_BD, line_w=0.75, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    box(s, x, y, 0.06, th, fill=PRIMARY)
    box(s, x + 0.1, y + (th - 0.34) / 2, 0.34, 0.34, text=str(i + 1), size=9.5, bold=True, color=WHITE, fill=NAVY,
        shape=MSO_SHAPE.OVAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
    box(s, x + 0.48, y, tw - 0.52, th, text=c, size=10, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)

# right panel
rx2 = CX + lw + 0.2
rw2 = CW - lw - 0.2
box(s, rx2, py0, rw2, ph, fill=TINT, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
ix, iw = rx2 + 0.18, rw2 - 0.36
box(s, ix, py0 + 0.08, iw, 0.3, text="Compliance Frameworks", size=12, bold=True, color=NAVY)
end = chips(s, ix, py0 + 0.42, iw, fws, PRIMARY, WHITE)
box(s, ix, end + 0.08, iw, 0.3, text="Attack Strategies", size=12, bold=True, color=NAVY)
end = chips(s, ix, end + 0.42, iw, strat, WHITE, INK, line=GREY_BD)
gy0 = end + 0.14
gh = 5.44 - 0.12 - gy0
box(s, ix, gy0, iw, gh, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
box(s, ix, gy0, 0.06, gh, fill=MUTE)
box(s, ix + 0.16, gy0 + 0.06, iw - 0.3, 0.3, text="Gaps to Know", size=11.5, bold=True, color=MUTE)
bullets(s, ix + 0.16, gy0 + 0.36, iw - 0.3, gh - 0.4,
        ["Image and audio attacks not stated", "No human-led service",
         "No published refresh cadence"], size=10, color=INK, mcolor=MUTE, gap=2)

# ================================================================ 7. head to head
s = std("Head to Head")
colw = [1.46, 2.58, 2.58, 2.58]
rows_h = [0.38] + [0.78] * len(D.H2H)
t = grid(s, CX, 0.86, colw, rows_h, None, None)
for c, (lab, fill) in enumerate([("Vendor", NAVY), ("Vendor Strengths", NAVY),
                                 ("AccuKnox Advantage", PRIMARY), ("POC Question", NAVY)]):
    cl = t.cell(0, c); cl.fill.solid(); cl.fill.fore_color.rgb = fill
    cell_text(cl, [[(lab, WHITE, True)]], 11, anchor=MSO_ANCHOR.MIDDLE)
for r, (name, lead, ak, q) in enumerate(D.H2H, start=1):
    vals = [
        ([[(name, NAVY, True)]], WHITE, 12.5),
        ([[("• ", MUTE, True), (x, INK, False)] for x in lead], WHITE, 10.5),
        ([[("• ", PRIMARY, True), (x, NAVY, True)] for x in ak], LAV, 10.5),
        ([[(q, NAVY, False)]], WHITE, 10.5),
    ]
    for c, (parts, fill, size) in enumerate(vals):
        cl = t.cell(r, c); cl.fill.solid(); cl.fill.fore_color.rgb = fill
        cell_text(cl, parts, size, anchor=MSO_ANCHOR.MIDDLE)
        if c == 3:
            for pp in cl.text_frame.paragraphs:
                for rn in pp.runs:
                    rn.font.italic = True
for rr in range(len(rows_h)):
    for cc in range(len(colw)):
        cl = t.cell(rr, cc)
        cl.margin_left = Inches(0.1); cl.margin_right = Inches(0.06)

# ================================================================ 8. modules and sources
s = std("More AccuKnox AI Security Modules")
mods = [("AI-SPM", "AI asset discovery across clouds"), ("AI-DR", "AI threat detection and response"),
        ("Prompt Firewall", "Runtime prompt guardrails"), ("Model and Dataset Security", "Model file and PII scans"),
        ("Agentic AI Security", "Agent and MCP sandboxing"), ("AI Pen Testing and CTEM", "Continuous threat exposure"),
        ("Shadow AI Defense", "Unsanctioned AI discovery"), ("AI Model Cards", "Per-model governance")]
mw = (CW - 3 * 0.14) / 4
for i, (h, sub) in enumerate(mods):
    x = CX + (i % 4) * (mw + 0.14)
    y = Y0 + (i // 4) * 0.98
    box(s, x, y, mw, 0.86, fill=TINT, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, x, y, mw, 0.06, fill=PRIMARY)
    box(s, x + 0.12, y + 0.12, mw - 0.2, 0.34, text=h, size=11.5, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.12, y + 0.46, mw - 0.2, 0.32, text=sub, size=9.5, color=MUTE)
box(s, CX, 2.98, CW, 0.3, text="Sources", size=12.5, bold=True, color=NAVY)
sw3 = CW / 3
for i, (vendor, links) in enumerate(D.SOURCES):
    x = CX + (i % 3) * sw3
    y = 3.30 + (i // 3) * 1.0
    b = box(s, x, y, sw3 - 0.1, 0.95, anchor=MSO_ANCHOR.TOP, ml=0)
    para(b, vendor, size=9.5, bold=True, color=NAVY, first=True, space_after=1)
    for text, url in links:
        para(b, text, size=7.6, color=PRIMARY if url else MUTE, space_after=0)
        if url:
            b.text_frame.paragraphs[-1].runs[0].hyperlink.address = url

# ================================================================ 9. closing
closing_slide(prs)

prs.save(OUT)
print("wrote", os.path.abspath(OUT), "slides:", len(prs.slides))
