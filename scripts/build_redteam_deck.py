# -*- coding: utf-8 -*-
"""
AI Red Teaming Stack Ranking deck, 8 vendors, visual edition.

AccuKnox vs Cisco AI Defense, F5 AI Red Team, Zscaler (SPLX), Mindgard, Lakera,
HiddenLayer, Palo Alto Networks. Scope is red teaming only.

Score = 8 capability criteria (Yes 2, Partial 1, Not stated 0, max 16)
      + 13 attack techniques (Yes 1, Partial 0.5, Not stated 0, max 13).
Every rank, total and count on every slide is computed from the tables below.

Evidence:
  D:\\Atharva\\AccuKnox\\redteam-briefs\\source\\<vendor>.md       one brief per vendor
  D:\\Atharva\\AccuKnox\\redteam-briefs\\source\\technique-coverage.md
  D:\\Atharva\\AccuKnox\\redteam-briefs\\source\\cisco.md, f5.md
  D:\\Atharva\\AccuKnox\\redteam-briefs\\source\\demo-recording-observations.md
  AccuKnox: help.accuknox.com red-teaming, 3.6 release notes, aiml-saas-vs-onprem,
            knox-rt module reference (v0.1), product team figures (15 Sep 2026)

Visual rules: white ground, solid fills only, no light tint boxes.
Tick = solid green, dash = solid #6464FF, cross = solid red, white glyphs.

Build:   py -3.11 scripts/build_redteam_deck.py
Render:  powershell -File scripts/render.ps1 -Pptx <abs pptx> -Out <abs dir>
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

SRC = os.path.join(HERE, "..", "PPT Template.pptx")
OUT = os.path.join(HERE, "..", "output", "AccuKnox_AI_Red_Teaming_Stack_Ranking.pptx")
ASSETS = os.path.join(HERE, "..", "output", "assets", "redteam")
DOCS = r"D:\Atharva\AccuKnox\HelpDocs\docs"
os.makedirs(ASSETS, exist_ok=True)

SYM_FONT = "Arial"
LINE = RGBColor(0xD5, 0xDA, 0xE6)

# =================================================================== data
# key, short name, product
VENDORS = [
    ("ak", "AccuKnox", "AI Red Teaming"),
    ("cs", "Cisco", "AI Defense Validation"),
    ("f5", "F5", "AI Red Team"),
    ("zs", "Zscaler", "SPLX Probe"),
    ("mg", "Mindgard", "Automated AI Red Teaming"),
    ("lk", "Lakera", "AI Red Teaming"),
    ("hl", "HiddenLayer", "AI Attack Simulation"),
    ("pa", "Palo Alto", "Prisma AIRS AI Red Teaming"),
]
KEYS = [v[0] for v in VENDORS]


def row(s):
    """'y p n ...' in VENDORS order -> dict."""
    parts = s.split()
    assert len(parts) == len(KEYS), s
    return dict(zip(KEYS, parts))


#                                     ak cs f5 zs mg lk hl pa
CAPS = [
    ("Published attack library",      row("y  y  y  p  p  p  p  y")),
    ("Context-aware attacks",         row("y  y  y  y  y  p  p  y")),
    ("Agents, RAG and MCP",           row("y  y  p  p  y  y  p  p")),
    ("Multimodal and ML models",      row("p  n  n  y  y  y  p  p")),
    ("Compliance mapping",            row("y  p  n  y  y  p  n  p")),
    ("Self-hosted and air-gapped",    row("y  p  p  p  p  n  n  n")),
    ("Continuous testing",            row("y  p  y  y  y  n  y  n")),
    ("Actionable findings",           row("y  y  y  y  y  y  y  p")),
]
TECH = [
    ("Crescendo",                     row("y  p  y  p  y  n  y  n")),
    ("Multi-turn",                    row("y  y  y  y  y  y  p  y")),
    ("Tree of Attacks (TAP)",         row("y  p  n  y  n  n  n  p")),
    ("Attacker LLM (PAIR)",           row("y  y  p  y  p  p  n  y")),
    ("Many-shot",                     row("y  n  p  n  n  n  p  n")),
    ("Encoding and obfuscation",      row("y  p  y  y  y  n  y  n")),
    ("Multilingual",                  row("y  p  n  p  n  y  p  y")),
    ("Role-play and persona",         row("y  y  y  n  y  n  y  n")),
    ("Indirect injection via RAG",    row("y  y  p  y  p  y  p  y")),
    ("Agent, tool and MCP abuse",     row("y  y  p  y  p  y  y  y")),
    ("System prompt extraction",      row("y  y  y  y  y  y  y  y")),
    ("PII and data exfiltration",     row("y  y  y  y  y  y  y  y")),
    ("Image and audio attacks",       row("n  n  n  y  y  p  n  n")),
]
#                                     ak cs f5 zs mg lk hl pa
DEPLOY = [
    ("SaaS",                          row("y  y  y  y  y  y  n  y")),
    ("Private cloud",                 row("y  y  y  n  y  n  n  n")),
    ("On-premises",                   row("y  p  y  p  p  n  n  n")),
    ("Air-gapped",                    row("y  n  n  n  n  n  n  n")),
]
LIBRARY = {
    "ak": ("30,000+", "probes"),
    "cs": ("200+", "attack techniques"),
    "f5": ("10,000+", "prompts per pack"),
    "zs": ("25+", "probes listed"),
    "mg": ("150+", "disclosed flaws"),
    "lk": ("85M+", "Gandalf prompts"),
    "hl": ("~40", "techniques charted"),
    "pa": ("500+", "attack vectors"),
}
H2H = [
    ("cs", "200+ techniques, adaptive multi-turn", "Air-gapped, 30,000+ probes"),
    ("f5", "10,000+ new prompts every month", "Air-gapped, agents and MCP as targets"),
    ("zs", "8 frameworks, TAP attacks", "Air-gapped, one clear probe count"),
    ("mg", "Research team, multimodal attacks", "30,000+ probes, air-gapped"),
    ("lk", "85M+ Gandalf prompt corpus", "Self-hosted red teaming"),
    ("hl", "Human-led red team services", "Compliance mapping in the product"),
    ("pa", "Unit 42 library refresh", "On-premises and air-gapped"),
]
DOMAINS = ["Prompt & Instruction Integrity", "Data Protection & Privacy", "Access Control",
           "Downstream System Injection", "RAG & Knowledge Base", "Agentic & Tool Use",
           "Jailbreak & Guardrail Evasion", "Harmful Content", "Criminal Facilitation",
           "Malicious Code & Supply Chain", "Accuracy & Reliability", "Brand, Legal & Commercial",
           "Fairness & Bias", "Regulated Sectors", "Transparency & Robustness"]
GALLERY = [
    ("getting-started/images/release-notes/v3.6/redteam-assets-page.png", "Models and Scan Risk"),
    ("getting-started/images/release-notes/v3.6/redteam-model-purpose.png", "Intelligent Scan by Model Purpose"),
    ("getting-started/images/release-notes/v3.6/redteam-scan-configurations.png", "Scan Configurations Across Models"),
    ("how-to/image-22.png", "Ask AI Remediation With OWASP Tags"),
]
SOURCES = [
    ("AccuKnox", ["help.accuknox.com/use-cases/red-teaming", "help.accuknox.com/getting-started/3.6-release",
                  "help.accuknox.com/how-to/aiml-saas-vs-onprem", "AccuKnox product team, Sep 2026"]),
    ("Cisco", ["securitydocs.cisco.com/docs/ai-def (Validation)", "blogs.cisco.com/ai/security-framework",
               "Cisco AI Defense data sheet"]),
    ("F5", ["f5.com/products/ai-red-team", "docs.aisecurity.f5.com/red-team", "f5.com/labs/casi"]),
    ("Zscaler", ["zscaler.com continuous-automated-red-teaming", "splx.ai/platform/probe", "splx.ai/pricing"]),
    ("Mindgard", ["mindgard.ai/automated-ai-red-teaming", "mindgard.ai/ai-attack-library"]),
    ("Lakera", ["lakera.ai/ai-red-teaming", "docs.lakera.ai/red", "docs.lakera.ai/docs/selfhosting"]),
    ("HiddenLayer", ["hiddenlayer.com/platform/ai-attack-simulation", "hiddenlayer.com/services"]),
    ("Palo Alto", ["paloaltonetworks.com/ai-security/ai-red-teaming", "Prisma AIRS AI Red Teaming docs"]),
]

CAP_PTS = {"y": 2, "p": 1, "n": 0}
TECH_PTS = {"y": 1, "p": 0.5, "n": 0}
CAP_MAX, TECH_MAX = 2 * len(CAPS), len(TECH)
TOTAL_MAX = CAP_MAX + TECH_MAX
NAME = {k: n for k, n, _p in VENDORS}


def cap_score(k):
    return sum(CAP_PTS[r[k]] for _l, r in CAPS)


def tech_score(k):
    return sum(TECH_PTS[r[k]] for _l, r in TECH)


def total(k):
    return cap_score(k) + tech_score(k)


def fmt(x):
    return ("%g" % x)


RANKED = sorted(KEYS, key=lambda k: (-total(k), NAME[k]))


def rank_of(k):
    return 1 + sum(1 for j in KEYS if total(j) > total(k))


# =================================================================== deck setup
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_STD = prs.slide_layouts[4]
for sid in list(prs.slides._sldIdLst):
    try:
        prs.part.drop_rel(sid.get(qn("r:id")))
    except Exception:
        pass
    prs.slides._sldIdLst.remove(sid)

Y0 = 0.92
SYM = {"y": (GREEN, "\u2713"), "p": (SECOND, "\u2212"), "n": (RED, "\u2715"), "s": (NAVY, "+")}


def std(title):
    s = prs.slides.add_slide(L_STD)
    set_title(s, title)
    blank_footer(s)
    return s


def sym(slide, cx, cy, state, size=0.30):
    fill, glyph = SYM[state]
    b = box(slide, cx - size / 2, cy - size / 2, size, size, fill=fill,
            shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.18, anchor=MSO_ANCHOR.MIDDLE,
            align=PP_ALIGN.CENTER, ml=0, mr=0, mt=0, mb=0, wrap=False)
    r = b.text_frame.paragraphs[0].add_run()
    r.text = glyph
    r.font.name = SYM_FONT
    r.font.bold = True
    r.font.size = Pt(size * 46)
    r.font.color.rgb = WHITE
    return b


def hline(slide, x, y, w, color=LINE, h=0.012):
    box(slide, x, y, w, h, fill=color)


def legend(slide, x, y, items=(("y", "Yes"), ("p", "Partial"), ("n", "Not stated"))):
    for st, lab in items:
        sym(slide, x + 0.11, y + 0.11, st, 0.22)
        box(slide, x + 0.28, y - 0.02, 1.1, 0.26, text=lab, size=10, color=INK, anchor=MSO_ANCHOR.MIDDLE)
        x += 1.25


def grid_slide(title, rows, pts_fn, max_pts, label_w=2.1, body_top=0.88, bottom=5.12, box_sz=0.30,
               label_size=10.5, pts_label="Score"):
    s = std(title)
    order = RANKED
    colw = (CW - label_w) / len(order)
    head_h = 0.44
    n = len(rows)
    rh = (bottom - body_top - head_h - 0.42) / n
    x0 = CX + label_w
    # AccuKnox column band, solid primary outline
    ak_i = order.index("ak")
    box(s, x0 + ak_i * colw, body_top, colw, head_h + n * rh + 0.42, line=PRIMARY, line_w=2.5)
    for i, k in enumerate(order):
        fill = PRIMARY if k == "ak" else NAVY
        box(s, x0 + i * colw + 0.02, body_top, colw - 0.04, head_h, text=NAME[k], size=(9 if len(NAME[k]) > 9 else 10) if k != "ak" else 10.5,
            bold=True, color=WHITE, fill=fill, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0.02, mr=0.02)
    for r, (label, states) in enumerate(rows):
        y = body_top + head_h + r * rh
        box(s, CX, y, label_w - 0.05, rh, text=label, size=label_size, bold=True, color=NAVY,
            anchor=MSO_ANCHOR.MIDDLE, ml=0.02)
        for i, k in enumerate(order):
            sym(s, x0 + i * colw + colw / 2, y + rh / 2, states[k], min(box_sz, rh - 0.06))
        hline(s, CX, y + rh - 0.006, CW)
    ty = body_top + head_h + n * rh
    box(s, CX, ty + 0.02, label_w - 0.05, 0.38, text=pts_label, size=12, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE, ml=0.02)
    for i, k in enumerate(order):
        val = pts_fn(k)
        box(s, x0 + i * colw + 0.02, ty + 0.04, colw - 0.04, 0.34, text=fmt(val), size=13, bold=True,
            color=WHITE, fill=PRIMARY if k == "ak" else NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
            shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.15)
    legend(s, CX, 5.26)
    box(s, CX + 4.0, 5.2, CW - 4.0, 0.3, text="Out of %s" % fmt(max_pts), size=10, color=MUTE,
        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    return s


# =================================================================== 1. cover
cover_slide(prs, "AI Red Teaming Stack Ranking")

# =================================================================== 2. ranking
s = std("AI Red Teaming Stack Ranking")
rows_top, rows_bot = Y0, 4.62
rh = (rows_bot - rows_top) / len(RANKED)
bar_x, bar_w = CX + 2.75, 5.55
for i, k in enumerate(RANKED):
    y = rows_top + i * rh
    is_ak = k == "ak"
    if is_ak:
        box(s, CX, y + 0.02, CW, rh - 0.04, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    txt = WHITE if is_ak else INK
    box(s, CX + 0.08, y + (rh - 0.36) / 2, 0.36, 0.36, text=str(rank_of(k)), size=12, bold=True, color=WHITE,
        fill=PRIMARY if is_ak else NAVY, shape=MSO_SHAPE.OVAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
        ml=0, mr=0)
    box(s, CX + 0.55, y, 2.15, rh, text=NAME[k], size=14 if is_ak else 12.5, bold=True, color=txt,
        anchor=MSO_ANCHOR.MIDDLE)
    cw_ = bar_w * cap_score(k) / TOTAL_MAX
    tw_ = bar_w * tech_score(k) / TOTAL_MAX
    by, bh = y + rh * 0.24, rh * 0.52
    box(s, bar_x, by, bar_w, bh, fill=WHITE if is_ak else GREY_BG)
    box(s, bar_x, by, cw_, bh, fill=PRIMARY if is_ak else NAVY)
    box(s, bar_x + cw_, by, tw_, bh, fill=GREEN if is_ak else SECOND)
    box(s, bar_x + bar_w + 0.05, y, CW - (bar_x - CX) - bar_w - 0.05, rh, text=fmt(total(k)), size=14, bold=True,
        color=txt, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT, mr=0.1)
# legend
lx = bar_x
for fill, lab in ((NAVY, "Capabilities, max %d" % CAP_MAX), (SECOND, "Attack techniques, max %d" % TECH_MAX)):
    box(s, lx, 4.72, 0.22, 0.18, fill=fill)
    box(s, lx + 0.28, 4.66, 2.4, 0.3, text=lab, size=10, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    lx += 2.55
st_ = box(s, CX, 5.02, CW, 0.42, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.15,
          anchor=MSO_ANCHOR.MIDDLE, ml=0.18)
runs(st_.text_frame.paragraphs[0], "Red teaming only.  ", size=10.5, bold=True, color=WHITE)
runs(st_.text_frame.paragraphs[0], "AccuKnox also ships AI-SPM, AI-DR, Prompt Firewall, Model Security, "
     "Agentic AI Security and CTEM.", size=10.5, color=WHITE)

# =================================================================== 3. capability matrix
grid_slide("Capability Matrix", CAPS, cap_score, CAP_MAX, box_sz=0.32, label_size=10.5)

# =================================================================== 4. attack techniques
grid_slide("Attack Technique Coverage", TECH, tech_score, TECH_MAX, box_sz=0.22, label_size=9.5,
           pts_label="Techniques")

# =================================================================== 5. deployment
s = std("Deployment Options")
cols = [c for c, _r in DEPLOY]
label_w = 2.0
colw = (CW - label_w) / len(cols)
head_h = 0.44
rh = (5.34 - Y0 - head_h) / len(RANKED)
x0 = CX + label_w
for i, c in enumerate(cols):
    box(s, x0 + i * colw + 0.03, Y0, colw - 0.06, head_h, text=c, size=12, bold=True, color=WHITE,
        fill=RED if c == "Air-gapped" else NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
for r, k in enumerate(RANKED):
    y = Y0 + head_h + r * rh
    if k == "ak":
        box(s, CX, y + 0.03, CW, rh - 0.06, line=PRIMARY, line_w=2.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    box(s, CX + 0.1, y, label_w - 0.1, rh, text=NAME[k], size=12.5, bold=True,
        color=PRIMARY if k == "ak" else NAVY, anchor=MSO_ANCHOR.MIDDLE)
    for i, (c, states) in enumerate(DEPLOY):
        sym(s, x0 + i * colw + colw / 2, y + rh / 2, states[k], 0.32)
    if k != RANKED[-1]:
        hline(s, CX, y + rh - 0.006, CW)

# =================================================================== 6. attack library
s = std("Published Attack Library")
tw, th, g = (CW - 3 * 0.16) / 4, 1.72, 0.18
for i, k in enumerate(RANKED):
    x = CX + (i % 4) * (tw + 0.16)
    y = Y0 + (i // 4) * (th + g)
    is_ak = k == "ak"
    box(s, x, y, tw, th, fill=PRIMARY if is_ak else WHITE, line=None if is_ak else NAVY, line_w=1.5,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    num, unit = LIBRARY[k]
    c1, c2 = (WHITE, WHITE) if is_ak else (NAVY, INK)
    box(s, x + 0.15, y + 0.14, tw - 0.3, 0.32, text=NAME[k], size=12, bold=True, color=c1)
    box(s, x + 0.15, y + 0.5, tw - 0.3, 0.7, text=num, size=30, bold=True, color=c1, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.15, y + 1.2, tw - 0.3, 0.36, text=unit, size=11.5, color=c2)
nt = box(s, CX, Y0 + 2 * th + g + 0.12, CW, 0.36, fill=RED, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2,
         anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
runs(nt.text_frame.paragraphs[0], "Units differ.  ", size=11, bold=True, color=WHITE)
runs(nt.text_frame.paragraphs[0], "Ask each vendor for attacks per standard scan.", size=11, color=WHITE)

# =================================================================== 7. AccuKnox red teaming
s = std("AccuKnox AI Red Teaming")
cards = [("30,000+", "Static Red Teaming", PRIMARY, ["20+ categories", "Standard policy packs", "OWASP LLM Top 10"]),
         ("Custom", "Intelligent Red Teaming", NAVY, ["Your industry context", "JSON, document or direct input", "Purpose-built probes"]),
         ("Air-Gapped", "Deployment Flexibility", GREEN_DK, ["SaaS", "Private cloud", "On-premises"])]
cw3, gap = (CW - 2 * 0.18) / 3, 0.18
for i, (big, head, col, items) in enumerate(cards):
    x = CX + i * (cw3 + gap)
    box(s, x, Y0, cw3, 3.0, fill=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x + 0.22, Y0 + 0.18, cw3 - 0.4, 0.62, text=big, size=28, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.22, Y0 + 0.80, cw3 - 0.4, 0.36, text=head, size=13, bold=True, color=WHITE)
    hline(s, x + 0.22, Y0 + 1.22, cw3 - 0.44, color=WHITE, h=0.015)
    for j, it in enumerate(items):
        yy = Y0 + 1.40 + j * 0.5
        b = box(s, x + 0.22, yy + 0.06, 0.28, 0.28, fill=WHITE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.18,
                anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, ml=0, mr=0, mt=0, mb=0, wrap=False)
        rr = b.text_frame.paragraphs[0].add_run(); rr.text = "\u2713"; rr.font.name = SYM_FONT
        rr.font.bold = True; rr.font.size = Pt(13); rr.font.color.rgb = col
        box(s, x + 0.6, yy, cw3 - 0.75, 0.4, text=it, size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
steps = ["Pick Static or Intelligent", "Add purpose or context", "Review generated probes", "Schedule and rescan"]
sw = (CW - 3 * 0.18) / 4
for i, t_ in enumerate(steps):
    x = CX + i * (sw + 0.18)
    box(s, x, 4.12, sw, 1.18, fill=WHITE, line=NAVY, line_w=1.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    box(s, x + 0.16, 4.28, 0.42, 0.42, text=str(i + 1), size=14, bold=True, color=WHITE, fill=PRIMARY,
        shape=MSO_SHAPE.OVAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
    box(s, x + 0.14, 4.76, sw - 0.26, 0.46, text=t_, size=12, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 8. domain categories
s = std("15 Domain-Specific Red Teaming Categories")
cols_n = 3
tw = (CW - 2 * 0.14) / cols_n
th = (5.40 - Y0 - 4 * 0.12) / 5
for i, c in enumerate(DOMAINS):
    x = CX + (i % cols_n) * (tw + 0.14)
    y = Y0 + (i // cols_n) * (th + 0.12)
    box(s, x, y, tw, th, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    box(s, x + 0.14, y + (th - 0.42) / 2, 0.42, 0.42, text=str(i + 1), size=12, bold=True, color=WHITE,
        fill=PRIMARY, shape=MSO_SHAPE.OVAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
    box(s, x + 0.66, y, tw - 0.76, th, text=c, size=12.5, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 9. gallery
s = std("AccuKnox Red Teaming Gallery")
gw, gh, gg = (CW - 0.2) / 2, 2.12, 0.2
for i, (rel, cap) in enumerate(GALLERY):
    im = Image.open(os.path.join(DOCS, rel)).convert("RGB")
    ratio = gw / (gh - 0.38)
    crop_h = min(im.height, int(im.width / ratio))
    im = im.crop((0, 0, im.width, crop_h))
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.Resampling.LANCZOS)
    path = os.path.join(ASSETS, "gallery-%d.png" % (i + 1))
    im.save(path)
    x = CX + (i % 2) * (gw + gg)
    y = 0.88 + (i // 2) * (gh + 0.14)
    box(s, x, y, gw, gh, fill=WHITE, line=NAVY, line_w=1.5)
    pic = s.shapes.add_picture(path, Inches(x + 0.02), Inches(y + 0.02), Inches(gw - 0.04), Inches(gh - 0.40))
    pic.shadow.inherit = False
    box(s, x, y + gh - 0.38, gw, 0.38, fill=NAVY)
    box(s, x + 0.1, y + gh - 0.33, 0.28, 0.28, text=str(i + 1), size=10.5, bold=True, color=WHITE,
        fill=PRIMARY, shape=MSO_SHAPE.OVAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
    box(s, x + 0.46, y + gh - 0.38, gw - 0.5, 0.38, text=cap, size=12, bold=True, color=WHITE,
        anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 10. head to head
s = std("Head to Head")
head_h = 0.42
rh = (5.40 - Y0 - head_h) / len(H2H)
c0, c1 = 1.5, (CW - 1.5) / 2
box(s, CX + c0, Y0, c1 - 0.06, head_h, text="They Lead", size=12.5, bold=True, color=WHITE, fill=NAVY,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, CX + c0 + c1, Y0, c1, head_h, text="AccuKnox Leads", size=12.5, bold=True, color=WHITE, fill=PRIMARY,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
for r, (k, them, ak) in enumerate(H2H):
    y = Y0 + head_h + r * rh
    box(s, CX, y, c0 - 0.05, rh, text=NAME[k], size=13, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    sym(s, CX + c0 + 0.24, y + rh / 2, "s", 0.30)
    box(s, CX + c0 + 0.48, y, c1 - 0.6, rh, text=them, size=12, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    sym(s, CX + c0 + c1 + 0.24, y + rh / 2, "y", 0.30)
    box(s, CX + c0 + c1 + 0.48, y, c1 - 0.55, rh, text=ak, size=12, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    hline(s, CX, y + rh - 0.006, CW)

# =================================================================== 11. modules
s = std("More AccuKnox AI Security Modules")
mods = [("AI-SPM", "AI asset discovery"), ("AI-DR", "Detection and response"), ("Prompt Firewall", "Runtime guardrails"),
        ("Model Security", "Model and dataset scans"), ("Agentic AI Security", "Agent and MCP sandboxing"),
        ("AI Pen Testing and CTEM", "Threat exposure"), ("Shadow AI Defense", "Unsanctioned AI discovery"),
        ("AI Model Cards", "Per-model governance")]
mw = (CW - 3 * 0.16) / 4
mh = (5.40 - Y0 - 0.18) / 2
for i, (h, sub) in enumerate(mods):
    x = CX + (i % 4) * (mw + 0.16)
    y = Y0 + (i // 4) * (mh + 0.18)
    box(s, x, y, mw, mh, fill=NAVY if i % 2 == 0 else PRIMARY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, x + 0.2, y + 0.25, mw - 0.35, 1.1, text=h, size=17, bold=True, color=WHITE)
    hline(s, x + 0.2, y + mh - 0.75, mw - 0.4, color=WHITE, h=0.015)
    box(s, x + 0.2, y + mh - 0.66, mw - 0.35, 0.5, text=sub, size=12, color=WHITE)

# =================================================================== 12. sources
s = std("Sources")
sw2 = CW / 4
for i, (v, lines) in enumerate(SOURCES):
    x = CX + (i % 4) * sw2
    y = Y0 + (i // 4) * 2.2
    b = box(s, x, y, sw2 - 0.12, 2.1, ml=0)
    para(b, v, size=12, bold=True, color=NAVY, first=True, space_after=3)
    for ln in lines:
        para(b, ln, size=9, color=INK, space_after=2)

# =================================================================== 13. closing
closing_slide(prs)

prs.save(OUT)
print("wrote", os.path.abspath(OUT), "slides:", len(prs.slides))
for k in RANKED:
    print(rank_of(k), NAME[k], fmt(cap_score(k)), fmt(tech_score(k)), fmt(total(k)))
