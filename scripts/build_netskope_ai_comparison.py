# -*- coding: utf-8 -*-
"""AccuKnox AI Security vs Netskope Skylight AI Security, branded comparison deck.

The rows come from the HelpDocs repo, so the deck, the XLSX and the markdown
draft read one data file:
  D:/AccuKnox/help/references/comparisons-builder/netskope/netskope_data.py

Build:   py -3.11 scripts/build_netskope_ai_comparison.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_vs_Netskope_AI_Security.pptx -Out output/render/netskope
"""
import os
import shutil
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import *  # noqa: F401,F403

HELP = r"D:\AccuKnox\help"
sys.path.insert(0, os.path.join(HELP, "references", "comparisons-builder", "netskope"))
import netskope_data as d  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "PPT Template.pptx")
OUT = os.path.join(HERE, "..", "output", "AccuKnox_vs_Netskope_AI_Security.pptx")
AST = os.path.join(HERE, "..", "output", "assets", "netskope")

SHOTS = {
    "managed": "docs/use-cases/images/shadow-ai/managed-assets-models.png",
    "unmanaged": "docs/use-cases/images/shadow-ai/unmanaged-asset-categories.png",
    "mlscan": "docs/how-to/image-6.png",
    "redteam": "docs/how-to/images/triton-collector/09-finding-detail.png",
    "pf": "docs/how-to/images/prompt-firewall/ai-security-dashboard.png",
    "aidr": "docs/getting-started/image-13.png",
}
os.makedirs(AST, exist_ok=True)
for k, rel in SHOTS.items():
    dst = os.path.join(AST, k + ".png")
    shutil.copy(os.path.join(HELP, rel), dst)
    SHOTS[k] = dst

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_STD = prs.slide_layouts[4]
xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try:
        prs.part.drop_rel(sid.get(qn("r:id")))
    except Exception:
        pass
    xml_slides.remove(sid)

RIVAL = RGBColor(0x6B, 0x72, 0x86)
STATUS_COL = {
    "GA": (GREEN_LT, GREEN_DK),
    "Beta": (LAV, PURPLE),
    "Preview": (LAV, PURPLE),
    "Roadmap": (GREY_BG, MUTE),
    "Not documented": (GREY_BG, MUTE),
}
EDGE_COL = {d.AK: (GREEN_LT, GREEN_DK), d.NS: (GREY_BG, NAVY),
            d.PAR: (LAV, PURPLE), d.NA: (GREY_BG, MUTE)}



def st_colors(s):
    if "Roadmap" in s or s in ("Beta", "Preview"):
        return STATUS_COL["Beta"]
    if s.startswith("GA"):
        return STATUS_COL["GA"]
    return STATUS_COL.get(s, (GREY_BG, MUTE))


def content(title, size=20):
    s = prs.slides.add_slide(L_STD)
    ph = set_title(s, title)
    for p in ph.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(size if len(title) < 52 else 16.5 if len(title) < 64 else 15.5)
            r.font.bold = True
    blank_footer(s)
    return s


def source_line(s, text, y=5.2, size=9):
    box(s, CX, y, CW, 0.3, text=text, size=size, color=MUTE, italic=True,
        anchor=MSO_ANCHOR.MIDDLE)


def add_run(p, text, size, bold=False, color=INK, url=None, italic=False):
    r = p.add_run()
    r.text = text
    r.font.name = FONT
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    if url:
        r.hyperlink.address = url
        r.font.color.rgb = PRIMARY
        r.font.underline = True
        r.font.bold = True
    return r


def link_para(tf, keys, size, first=False, lead=None):
    """A paragraph of [LINK] anchors, one per source key."""
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_before = Pt(3)
    if lead:
        add_run(p, lead, size, color=MUTE)
    for i, k in enumerate(keys):
        if i:
            add_run(p, " ", size)
        add_run(p, "[LINK]", size, url=d.SOURCES[k][2])
    return p


def prep(cell, anchor=MSO_ANCHOR.MIDDLE, fill=WHITE):
    cell.margin_left = Inches(0.09)
    cell.margin_right = Inches(0.07)
    cell.margin_top = Inches(0.05)
    cell.margin_bottom = Inches(0.05)
    cell.vertical_anchor = anchor
    cell.fill.solid()
    cell.fill.fore_color.rgb = fill
    cell.text_frame.word_wrap = True
    return cell.text_frame


def new_table(s, x, y, w, h, nrows, colw):
    t = s.shapes.add_table(nrows, len(colw), Inches(x), Inches(y), Inches(w), Inches(h)).table
    t.first_row = False
    t.horz_banding = False
    for i, cw in enumerate(colw):
        t.columns[i].width = Inches(cw)
    return t


def head_row(t, heads, fills, size=12):
    for ci, h in enumerate(heads):
        tf = prep(t.cell(0, ci), fill=fills[ci])
        add_run(tf.paragraphs[0], h, size, bold=True, color=WHITE)


# ======================================================== 1. COVER
cover_slide(prs, "AccuKnox vs Netskope\nAI Security",
            scope=[(str(len(d.ROWS)), "Capabilities compared"),
                   (str(len(d.CATEGORIES)), "Categories"),
                   (str(len(d.SOURCES)), "Vendor pages cited")])

# ======================================================== 2. METHOD
s = content("16 Capabilities Compared From Each Vendor's Own Docs")
box(s, CX, 0.95, 4.4, 0.34, text="WHAT WE COMPARED", size=12, color=PRIMARY, bold=True)
bullets(s, CX, 1.32, 4.4, 2.4, [(f"{cid}.  ", name) for cid, name in d.CATEGORIES],
        size=14, marker=None, gap=5)
box(s, CX, 3.75, 4.4, 1.3,
    text=(f"We read every source on {d.READ_ON}. Netskope rows cite docs.netskope.com "
          "or netskope.com. AccuKnox rows cite help.accuknox.com and accuknox.com."),
    size=12, color=INK, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06,
    ml=0.16, mr=0.16, anchor=MSO_ANCHOR.MIDDLE)
box(s, 5.1, 0.95, 4.5, 0.34, text="HOW TO READ A CELL", size=12, color=PRIMARY, bold=True)
legend = list(d.LEGEND) + [("⚖️", "Parity. Both vendors ship it."),
                           ("[LINK]", "Opens the vendor page that proves the cell.")]
y = 1.35
for icon_, txt in legend:
    sp = box(s, 5.1, y, 0.75, 0.52, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    add_run(sp.text_frame.paragraphs[0], icon_, 16 if icon_ != "[LINK]" else 11,
            bold=True, color=PRIMARY if icon_ == "[LINK]" else INK)
    sp.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    box(s, 5.9, y, 3.7, 0.52, text=txt, size=12, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.62
box(s, 5.1, y + 0.1, 4.5, 0.55,
    text="AI GRC and AI Identity Security are AccuKnox Beta modules.",
    size=12, color=PURPLE, bold=True, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12,
    anchor=MSO_ANCHOR.MIDDLE, ml=0.16)

# ======================================================== 3. SCORECARD
sc = d.score()
s = content(f"AccuKnox Leads {sc[d.AK]} of 16 Rows and Netskope Leads {sc[d.NS]}")
t = new_table(s, CX, 0.88, 7.3, 4.3, len(d.ROWS) + 1, [0.42, 2.98, 1.6, 1.25, 1.05])
head_row(t, ["ID", "Capability", "AccuKnox", "Netskope", "Edge"], [NAVY, NAVY, NAVY, RIVAL, NAVY], size=10.5)
t.rows[0].height = Inches(0.28)
for ri, x in enumerate(d.ROWS, 1):
    t.rows[ri].height = Inches(0.24)
    tf = prep(t.cell(ri, 0), fill=LAV)
    add_run(tf.paragraphs[0], x["id"], 9.5, bold=True, color=PRIMARY)
    tf = prep(t.cell(ri, 1), fill=LAV)
    add_run(tf.paragraphs[0], x["capability"], 9.5, bold=True, color=NAVY)
    for ci, st in ((2, x["ak_status"]), (3, x["ns_status"])):
        bg, fg = st_colors(st)
        tf = prep(t.cell(ri, ci), fill=bg)
        add_run(tf.paragraphs[0], d.status_label(st).split(",")[0].replace("Not documented", "Not in docs"), 9.5, bold=True, color=fg)
    bg, fg = EDGE_COL[x["edge"]]
    tf = prep(t.cell(ri, 4), fill=bg)
    add_run(tf.paragraphs[0], d.EDGE_LABEL[x["edge"]], 9.5, bold=True, color=fg)
stat(s, 7.85, 0.88, 1.75, str(sc[d.AK]), "rows AccuKnox leads", color=GREEN_DK, h=1.0, nsize=30, lsize=11)
stat(s, 7.85, 1.98, 1.75, str(sc[d.NS]), "rows Netskope leads", color=NAVY, h=1.0, nsize=30, lsize=11)
stat(s, 7.85, 3.08, 1.75, str(sc[d.PAR]), "row at parity", color=PURPLE, h=1.0, nsize=30, lsize=11)
box(s, 7.85, 4.18, 1.75, 1.0, text="Licensing is not scored yet.", size=11, color=MUTE,
    fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08, anchor=MSO_ANCHOR.MIDDLE,
    align=PP_ALIGN.CENTER)

# ======================================================== 4-9. CATEGORY SLIDES
for cid, cname in d.CATEGORIES:
    crow = [x for x in d.ROWS if x["cat"] == cid]
    s = content(d.HEADLINES[cid])
    eyebrow(s, f"{cid}.  {cname}", y=0.84, size=11)
    top = 1.14
    t = new_table(s, CX, top, CW, 5.28 - top, len(crow) + 1, [1.45, 2.9, 2.9, 1.95])
    head_row(t, ["Capability", "AccuKnox", "Netskope", "Edge"], [NAVY, NAVY, RIVAL, NAVY])
    t.rows[0].height = Inches(0.32)
    rh = (5.28 - top - 0.32) / len(crow)
    for ri, x in enumerate(crow, 1):
        t.rows[ri].height = Inches(rh)
        tf = prep(t.cell(ri, 0), fill=LAV)
        add_run(tf.paragraphs[0], x["id"] + "\n" if False else x["id"], 10, bold=True, color=PRIMARY)
        p = tf.add_paragraph()
        add_run(p, x["capability"], 12, bold=True, color=NAVY)
        for ci, st, txt, keys in ((1, x["ak_status"], x["ak_short"], x["ak_src"]),
                                  (2, x["ns_status"], x["ns_short"], x["ns_src"])):
            bg, fg = st_colors(st)
            tf = prep(t.cell(ri, ci))
            add_run(tf.paragraphs[0], d.status_label(st), 11, bold=True, color=fg)
            p = tf.add_paragraph()
            p.space_before = Pt(2)
            add_run(p, txt, 11.5, color=INK)
            link_para(tf, keys, 10)
        bg, fg = EDGE_COL[x["edge"]]
        tf = prep(t.cell(ri, 3), fill=bg)
        add_run(tf.paragraphs[0], d.EDGE_LABEL[x["edge"]], 12, bold=True, color=fg)
        p = tf.add_paragraph()
        p.space_before = Pt(2)
        add_run(p, x["why"], 10, color=INK)

# ======================================================== 10-15. PRODUCT SCREENS
ROW = {x["id"]: x for x in d.ROWS}


def screen(title, key, row_ids, caption, src):
    from PIL import Image as _PIL
    s = content(title)
    im = _PIL.open(SHOTS[key])
    ar = im.size[0] / im.size[1]
    w, hmax = 6.0, 4.1
    h = w / ar
    if h > hmax:
        h = hmax
        w = h * ar
    x0 = CX + (6.0 - w) / 2
    y0 = 0.95 + (4.2 - h) / 2
    box(s, x0 - 0.07, y0 - 0.07, w + 0.14, h + 0.14, fill=GREY_BG,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.03)
    pic = s.shapes.add_picture(SHOTS[key], Inches(x0), Inches(y0), Inches(w), Inches(h))
    pic.line.color.rgb = GREY_BD
    pic.line.width = Pt(1.0)
    px, pw = 6.65, 2.95
    box(s, px, 0.95, pw, 0.3, text="WHAT THE SCREEN SHOWS", size=11, color=PRIMARY, bold=True)
    box(s, px, 1.25, pw, 1.15, text=caption, size=13, color=NAVY, bold=True)
    y = 2.45
    for rid in row_ids:
        x = ROW[rid]
        pill(s, px, y, 0.6, 0.3, rid, fill=PRIMARY, size=10.5)
        box(s, px + 0.68, y - 0.03, pw - 0.68, 0.36, text=x["capability"], size=11.5,
            color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        sp = box(s, px, y + 0.36, pw, 1.0, text=x["ak_short"], size=11, color=INK)
        link_para(sp.text_frame, x["ak_src"], 10)
        y += 1.45 if len(row_ids) > 1 else 0
    source_line(s, src)


screen("AccuKnox Inventories Cloud LLMs With Agentless Roles", "managed", ["A1"],
       "The Managed tab lists Azure LLMs found through read-only cloud roles.",
       "Screen from help.accuknox.com/use-cases/shadow-ai-discovery/. Owner fields are redacted.")
screen("AccuKnox Sorts Shadow AI on Servers Into 7 Package Types", "unmanaged", ["A2", "D2"],
       "The Unmanaged tab groups AI agents, gateways, inference engines, SDKs and MCP.",
       "Screen from help.accuknox.com/use-cases/shadow-ai-discovery/.")
screen("AccuKnox Flags Unsafe Operators Inside Model Files", "mlscan", ["B1"],
       "ML findings name the unsafe TensorFlow and Pickle operators, file by file.",
       "Screen from help.accuknox.com/how-to/ml-static-scan/.")
screen("AccuKnox Red Teams the Running Model by Goal", "redteam", ["B3"],
       "Red team findings grouped by attack goal, with the count of prompts that worked.",
       "Screen from help.accuknox.com/how-to/aiml-triton-collector/.")
screen("AccuKnox Tracks Violations and Latency per App", "pf", ["C1", "C2"],
       "Each protected app shows its policies, queries, violations and p90 latency.",
       "Screen from help.accuknox.com/how-to/prompt-firewall/.")
screen("AccuKnox Alerts When an Azure OpenAI Resource Changes", "aidr", ["E1"],
       "An AI-DR alert from Azure logs, with the raw event beside it.",
       "Screen from help.accuknox.com/getting-started/3.3-release/. IDs and IPs are blurred.")

# ======================================================== 16. NETSKOPE LEADS
s = content("Netskope Leads on Workforce Traffic, DLP and MCP")
box(s, CX, 0.9, CW, 0.45,
    text="These rows favor Netskope. Weigh them when the main risk is employee traffic.",
    size=13, color=INK, anchor=MSO_ANCHOR.MIDDLE)
w = (CW - 0.3) / 2
for i, (head, text, key) in enumerate(d.NETSKOPE_LEADS):
    x0 = CX + (i % 2) * (w + 0.3)
    y0 = 1.45 + (i // 2) * 1.9
    box(s, x0, y0, w, 1.75, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, x0, y0, w, 0.09, fill=RIVAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    box(s, x0 + 0.18, y0 + 0.18, w - 0.36, 0.4, text=d.TICK + "  " + head, size=15,
        color=NAVY, bold=True)
    sp = box(s, x0 + 0.18, y0 + 0.62, w - 0.36, 1.05, text=text, size=13, color=INK)
    link_para(sp.text_frame, [key], 11)

# ======================================================== 17. WHY ACCUKNOX
s = content("Why Customers Choose AccuKnox Over Netskope")
w = (CW - 0.4) / 3
icons = {"Better": "shield", "Faster": "bolt", "Cheaper": "chart"}
for i, (head, text, keys) in enumerate(d.BETTER_FASTER_CHEAPER):
    x0 = CX + i * (w + 0.2)
    box(s, x0, 1.0, w, 3.95, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x0, 1.0, w, 0.09, fill=PRIMARY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    icon(s, x0 + 0.18, 1.25, 0.5, G(icons[head]), bg=PRIMARY)
    box(s, x0 + 0.8, 1.22, w - 0.95, 0.56, text=head, size=18, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    sp = box(s, x0 + 0.18, 1.95, w - 0.36, 2.9, text=text, size=13.5, color=INK)
    link_para(sp.text_frame, keys, 11.5)

# ======================================================== 18. SOURCES
s = content("Every Claim Links to a Page the Vendor Published")
ak_keys = ["ak-arch", "ak-shadow", "ak-matrix", "ak-mlscan", "ak-xbom", "ak-probes",
           "ak-pf", "ak-aiint", "ak-modelarmor", "ak-aidr", "ak-onprem", "ak-web-ai", "ak-web-grc"]
ns_keys = ["ns-aisec", "ns-aicc", "ns-platforms", "ns-client", "ns-guardrails", "ns-profile",
           "ns-gwov", "ns-redteam", "ns-aac", "ns-broker", "ns-mcpgw", "ns-gwlic", "ns-aicclic"]
for x0, keys, head, col in ((CX, ak_keys, "ACCUKNOX", NAVY), (5.06, ns_keys, "NETSKOPE", RIVAL)):
    box(s, x0, 0.92, 4.54, 0.36, text=head, size=12, color=WHITE, bold=True, fill=col,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
        radius=0.2)
    sp = box(s, x0 + 0.05, 1.36, 4.45, 3.85, anchor=MSO_ANCHOR.TOP, ml=0.04)
    tf = sp.text_frame
    for i, k in enumerate(keys):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(4.5)
        add_run(p, d.SOURCES[k][1] + "  ", 13, bold=True, color=NAVY)
        add_run(p, "[LINK]", 12, url=d.SOURCES[k][2])
source_line(s, f"All {len(d.SOURCES)} sources, with the rows each one supports, sit in the Sheet's Sources tab.")

# ======================================================== 19. CLOSING
closing_slide(prs)

prs.save(OUT)
print("saved:", os.path.abspath(OUT))
print("slides:", len(prs.slides))
