# -*- coding: utf-8 -*-
"""
AccuKnox vs Promptfoo — AI Security Stack Ranking.

A 12-slide side-by-side battlecard built on the AccuKnox master template. Every
claim traces to the .xlsx battlecard at
HelpDocs/utils/comparisons-builder/accuknox-vs-promptfoo-ai-security.xlsx,
which in turn cites help.accuknox.com, accuknox.com, and promptfoo.dev
(read 15 August 2026).

Build:   py -3.11 scripts/build_promptfoo_battlecard.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_vs_Promptfoo_Battlecard.pptx -Out output/render/promptfoo
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
SRC = os.path.join(HERE, "..", "PPT Template.pptx")
AST = os.path.join(HERE, "..", "output", "assets", "pfbc")
OUT = os.path.join(HERE, "..", "output", "AccuKnox_vs_Promptfoo_Battlecard.pptx")


def A(name):
    return os.path.join(AST, name)


os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_COVER, L_DIV, L_STD = prs.slide_layouts[0], prs.slide_layouts[2], prs.slide_layouts[4]
xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try:
        prs.part.drop_rel(sid.get(qn("r:id")))
    except Exception:
        pass
    xml_slides.remove(sid)

# ---- 50/50 geometry ------------------------------------------------
LX, RX, COLW = 0.40, 5.18, 4.42
GAP = 0.36
RIVAL = RGBColor(0x6B, 0x72, 0x86)      # neutral grey for the competitor side
RIVAL_BG = RGBColor(0xF3, 0xF4, 0xF7)


def content(title, kicker=None):
    s = prs.slides.add_slide(L_STD)
    set_title(s, title)
    blank_footer(s)
    if kicker:
        eyebrow(s, kicker)
    return s


def shot(s, path, cx, cy, cw, ch, panel=GREY_BG, pad=0.10):
    """Place an image inside a column and wrap it in a panel that actually hugs
    it, instead of a wide grey box with the picture floating in the middle."""
    from PIL import Image as _PIL
    im = _PIL.open(path)
    ar = im.size[0] / im.size[1]
    iw, ih = (ch * ar, ch) if (cw / ch) > ar else (cw, cw / ar)
    iw = min(iw, cw - 2 * pad)
    ih = iw / ar
    if ih > ch - 2 * pad:
        ih = ch - 2 * pad
        iw = ih * ar
    px, py = cx + (cw - iw) / 2, cy + (ch - ih) / 2
    box(s, px - pad, py - pad, iw + 2 * pad, ih + 2 * pad, fill=panel,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    pic = s.shapes.add_picture(path, Inches(px), Inches(py), Inches(iw),
                               Inches(ih))
    pic.line.color.rgb = GREY_BD
    pic.line.width = Pt(1.0)
    pic.shadow.inherit = False
    return py + ih + pad


def split_heads(s, y=1.16, left="ACCUKNOX", right="PROMPTFOO",
                lsub=None, rsub=None, h=0.44):
    """The two column headers that make every comparison slide read the same way.
    Returns the first y a slide may safely put content at."""
    box(s, LX, y, COLW, h, text=left, size=12.5, color=WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=NAVY,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    box(s, RX, y, COLW, h, text=right, size=12.5, color=WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=RIVAL,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    if lsub:
        box(s, LX, y + h + 0.04, COLW, 0.24, text=lsub, size=8.6, color=PRIMARY,
            bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if rsub:
        box(s, RX, y + h + 0.04, COLW, 0.24, text=rsub, size=8.6, color=RIVAL,
            bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return y + h + (0.36 if (lsub or rsub) else 0.16)


def verdict(s, text, color=PRIMARY, fill=None, y=4.86, h=0.42):
    box(s, LX, y, 9.20, h, text=text, size=10.5, color=color, bold=True,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, ml=0.16,
        fill=fill or LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)


def marks(s, x, y, w, items, tick="●", color=PRIMARY, size=10, gap=0.285,
          tcolor=INK):
    """A tight marker list. items = list of str."""
    for i, it in enumerate(items):
        yy = y + i * gap
        box(s, x, yy, 0.20, 0.24, text=tick, size=8.5, color=color, bold=True,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False,
            ml=0, mr=0, mt=0, mb=0)
        box(s, x + 0.22, yy - 0.02, w - 0.22, 0.28, text=it, size=size,
            color=tcolor, anchor=MSO_ANCHOR.MIDDLE, ml=0, mt=0, mb=0)


def source(s, text, y=5.30):
    box(s, LX, y, 9.20, 0.24, text=text, size=7.4, color=GREY_TX, italic=True,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)


# =================================================================== 1. COVER
s = prs.slides.add_slide(L_DIV)
blank_footer(s)
box(s, 0.70, 0.92, 8.6, 0.32, text="COMPETITIVE BATTLECARD  ·  AI SECURITY",
    size=12, color=SECOND, bold=True)
box(s, 0.70, 1.30, 3.2, 0.035, fill=PRIMARY)
box(s, 0.66, 1.46, 8.7, 1.5, text="AccuKnox vs Promptfoo", size=40, color=WHITE,
    bold=True, anchor=MSO_ANCHOR.TOP)
box(s, 0.70, 2.52, 8.7, 0.72,
    text="A platform that secures the AI you are running, against a tool that "
         "tests the AI you already know about.",
    size=14, color=NAVY_TXT, anchor=MSO_ANCHOR.TOP)
for i, (n, l) in enumerate([("85", "sub-features compared"),
                            ("67 / 33", "full support, us vs them"),
                            ("51", "capabilities only we ship"),
                            ("17", "capabilities only they ship")]):
    x = 0.70 + i * 2.18
    box(s, x, 3.34, 2.02, 0.90, fill=NAVY_DK, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
        radius=0.08)
    box(s, x, 3.40, 2.02, 0.44, text=n, size=21, color=WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x, 3.82, 2.02, 0.36, text=l, size=8.4, color=NAVY_TXT,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, 0.70, 4.52, 0.12, 0.58, fill=PRIMARY)
box(s, 0.94, 4.50, 8.3, 0.62,
    text="Sourced from help.accuknox.com, accuknox.com and promptfoo.dev  ·  "
         "Read 15 August 2026\nEvery row in this deck is backed by a URL in the "
         "companion .xlsx battlecard",
    size=9.5, color=NAVY_TXT, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 2. VERDICT
s = content("The one-line verdict", "Where this deal is won")
split_heads(s, y=1.12,
            lsub="AI SECURITY PLATFORM  ·  8 MODULES",
            rsub="AI RED TEAMING TOOL  ·  6 PRODUCTS")
box(s, LX, 1.86, COLW, 1.30, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
    radius=0.06)
box(s, LX + 0.18, 1.96, COLW - 0.36, 1.12,
    text="Finds the AI you did not know you were running, scores its posture, "
         "enforces policy on it at run time, and responds when it drifts. "
         "Testing is one of eight modules.",
    size=11, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
box(s, RX, 1.86, COLW, 1.30, fill=RIVAL_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
    radius=0.06)
box(s, RX + 0.18, 1.96, COLW - 0.36, 1.12,
    text="Attacks an AI application you point it at, and reports what broke. It "
         "is very good at that. It never tells you which AI applications exist "
         "in the first place.",
    size=11, color=INK, anchor=MSO_ANCHOR.MIDDLE)
marks(s, LX + 0.06, 3.30, COLW - 0.12, [
    "Discovery, posture, runtime, response",
    "67 of 85 sub-features fully supported",
    "On-prem and air-gapped, full parity",
    "AI security sits inside a CNAPP platform",
], color=PRIMARY, tcolor=NAVY)
marks(s, RX + 0.06, 3.30, COLW - 0.12, [
    "Testing and evaluation, deep and dynamic",
    "33 of 85 sub-features fully supported",
    "Self-hosted on Docker, SQLite backed",
    "Part of OpenAI, per their own site banner",
], color=RIVAL, tcolor=INK)
verdict(s, "Sell the gap, not a like-for-like win. Concede red teaming, then "
           "ask how they secure the AI nobody has inventoried.")
source(s, "Scorecard from the 85-row battlecard. Promptfoo product set and "
          "ownership: promptfoo.dev")

# =================================================================== 3. SHAPES
s = content("Two different products, sold into the same meeting", "What each one is")
split_heads(s, y=1.12, lsub="EIGHT AI SECURITY MODULES",
            rsub="SIX PRODUCTS, ALL TEST-SIDE")
mods = ["AI-SPM", "AI-DR", "Agentic AI", "Model & Dataset", "Red Teaming",
        "Prompt Firewall", "AI Identity", "AI GRC"]
for i, m in enumerate(mods):
    x = LX + (i % 2) * (COLW / 2 + 0.04)
    y = 1.88 + (i // 2) * 0.46
    soon = i >= 6
    box(s, x, y, COLW / 2 - 0.04, 0.38, text=m + ("  ·  soon" if soon else ""),
        size=9.5, color=MUTE if soon else WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
        fill=GREY_BG if soon else PRIMARY,
        line=GREY_BD if soon else None,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.16)
prods = ["Red Teaming", "Evaluations", "Code Scanning", "Model Security",
         "Guardrails", "MCP Proxy"]
for i, p in enumerate(prods):
    x = RX + (i % 2) * (COLW / 2 + 0.04)
    y = 1.88 + (i // 2) * 0.46
    box(s, x, y, COLW / 2 - 0.04, 0.38, text=p, size=9.5, color=WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=RIVAL,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.16)
box(s, LX, 3.80, COLW, 0.92, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
    radius=0.06)
box(s, LX + 0.16, 3.88, COLW - 0.32, 0.78,
    text="Six of the eight are shipping today. AI Identity Security and AI GRC "
         "are marked coming soon in the help docs, so do not promise them.",
    size=9.8, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
box(s, RX, 3.80, COLW, 0.92, fill=RIVAL_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
    radius=0.06)
box(s, RX + 0.16, 3.88, COLW - 0.32, 0.78,
    text="All six answer the question 'is this AI app safe?'. None answer 'what "
         "AI is running, where, and who deployed it?'.",
    size=9.8, color=INK, anchor=MSO_ANCHOR.MIDDLE)
verdict(s, "The overlap is one module out of eight. Everything else is "
           "greenfield for us.",
        color=NAVY)
source(s, "help.accuknox.com/use-cases/aiml-usecases/  ·  promptfoo.dev "
          "homepage product tabs")

# =================================================================== 4. SHADOW AI
s = content("Shadow AI Discovery: you cannot test what you have not found",
            "Module 1  ·  8 of 8 rows, AccuKnox only")
split_heads(s, y=1.10)
shot(s, A("ak-shadow-categories.png"), LX, 1.68, COLW, 1.42)
marks(s, LX + 0.06, 3.28, COLW - 0.12, [
    "Agentless discovery across AWS, Azure, GCP",
    "VM and in-cluster scanners, package level",
    "Seven asset types, MCP servers included",
    "Browser plugin logs GenAI service usage",
], color=PRIMARY, tcolor=NAVY, size=9.6)
box(s, RX, 1.68, COLW, 1.42, fill=RIVAL_BG, line=GREY_BD, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
box(s, RX + 0.20, 1.80, COLW - 0.40, 0.50, text="No discovery. At all.",
    size=16, color=RIVAL, bold=True, align=PP_ALIGN.CENTER,
    anchor=MSO_ANCHOR.MIDDLE)
box(s, RX + 0.20, 2.28, COLW - 0.40, 0.72,
    text="Promptfoo starts after you hand it a target URL, an endpoint, or a "
         "config file. Somebody has to already know the AI app exists.",
    size=10, color=INK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
marks(s, RX + 0.06, 3.28, COLW - 0.12, [
    "No asset inventory anywhere in 280 site URLs",
    "No cloud account onboarding, no scanners",
    "No unmanaged or on-prem asset view",
    "No browser-side GenAI usage visibility",
], color=RIVAL, tcolor=INK, tick="✕", size=9.6)
verdict(s, "Ask the buyer: how many AI applications are running in your estate "
           "right now? If they hesitate, testing is the wrong first purchase.")
source(s, "help.accuknox.com/use-cases/shadow-ai-discovery/  ·  Promptfoo: no "
          "discovery capability in any product page or doc")

# =================================================================== 5. SPM/DR
s = content("Posture and response: the parts that run without a human",
            "Modules 2 and 8  ·  11 of 11 rows, AccuKnox only")
split_heads(s, y=1.10)
shot(s, A("ak-managed-models.png"), LX, 1.68, COLW, 1.10)
shot(s, A("ak-aidr.png"), LX, 2.86, COLW, 1.00)
marks(s, LX + 0.06, 3.96, COLW - 0.12, [
    "CloudTrail, Azure and GCP logs ingested continuously",
    "Exposed model endpoints made private automatically",
], color=PRIMARY, tcolor=NAVY, size=9.4)
box(s, RX, 1.68, COLW, 2.18, fill=RIVAL_BG, line=GREY_BD, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
box(s, RX + 0.20, 1.82, COLW - 0.40, 0.40,
    text="Nothing runs between test runs", size=13.5, color=RIVAL, bold=True,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
marks(s, RX + 0.20, 2.34, COLW - 0.40, [
    "No cloud log ingestion",
    "No misconfiguration posture on Bedrock or Vertex",
    "No automated remediation of an exposed endpoint",
    "No AIBOM, no security graph",
], color=RIVAL, tcolor=INK, tick="✕", size=9.6, gap=0.30)
marks(s, RX + 0.06, 3.96, COLW - 0.12, [
    "Webhooks on Enterprise, no named ITSM connector",
    "Findings land in a report, not in an incident queue",
], color=RIVAL, tcolor=INK, tick="●", size=9.4)
verdict(s, "A scan tells you what was broken on Tuesday. AI-DR tells you what "
           "changed at 03:00 on Saturday and closes it.")
source(s, "help.accuknox.com/use-cases/aidr/ and /how-to/aiml-overview/  ·  "
          "promptfoo.dev/pricing for the webhook tier")

# =================================================================== 6. MODEL
s = content("Model and dataset security: closer than you think",
            "Module 3  ·  a genuine parity fight")
split_heads(s, y=1.10, lsub="5 FORMATS  ·  PLUS DATASETS AND RUNTIME",
            rsub="5 FORMATS  ·  FILES ONLY")
rows = [
    ("Static model file scanning", "Yes", "Yes"),
    ("Formats covered", "Pickle, HDF5, TF, CKPT, ONNX",
     "PyTorch, TF, Keras, Pickle, JSON/YAML"),
    ("Dataset PII and PHI scanning", "Yes", "No"),
    ("Dataset lineage, poisoning detection", "Yes", "No"),
    ("Runtime protection of model execution", "Yes, eBPF and LSM", "No"),
    ("Foundation model benchmarking", "No", "Yes"),
]
y0 = 1.92
for i, (label, lv, rv) in enumerate(rows):
    y = y0 + i * 0.46
    bg = WHITE if i % 2 else GREY_BG
    box(s, LX, y, 9.20, 0.42, fill=bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
        radius=0.04)
    box(s, LX + 0.14, y, 3.30, 0.42, text=label, size=9.6, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    lc = PRIMARY if lv != "No" else RIVAL
    rc = INK if rv not in ("No",) else RIVAL
    box(s, 3.60, y, 2.90, 0.42, text=lv, size=9.4, color=lc,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 6.56, y, 3.04, 0.42, text=rv, size=9.4, color=rc,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
verdict(s, "Do not claim a win on file scanning. Win on what happens to the "
           "dataset before training and to the model process at run time.",
        color=NAVY)
source(s, "help.accuknox.com/how-to/ml-static-scan/ and /faqs/ai-security/  ·  "
          "promptfoo.dev/model-security/")

# =================================================================== 7. REDTEAM
s = content("Red teaming: they win this one", "Module 4  ·  concede it early and mean it")
split_heads(s, y=1.10, lsub="150+ PROBES  ·  4 CATEGORIES",
            rsub="157 PLUGINS  ·  6 CATEGORIES")
marks(s, LX + 0.06, 1.90, COLW - 0.12, [
    "150+ adversarial probes, OWASP and ATLAS mapped",
    "Runs on a schedule and after every fine-tune",
    "Custom domain probe packs and prompt files",
    "Findings feed the same console as the rest of AI security",
], color=PRIMARY, tcolor=NAVY, size=9.8, gap=0.32)
box(s, LX, 3.22, COLW, 1.50, fill=RED_LT, line=RED, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
box(s, LX + 0.16, 3.28, COLW - 0.32, 0.28, text="WHERE WE ARE THINNER",
    size=9, color=RED, bold=True, anchor=MSO_ANCHOR.MIDDLE)
marks(s, LX + 0.20, 3.60, COLW - 0.40, [
    "No public research datasets (HarmBench, Pliny)",
    "No multimodal or coding-agent red teaming",
    "No shipped industry packs for finance or telecom",
], color=RED, tcolor=INK, tick="✕", size=9.2, gap=0.28)
shot(s, A("pf-riskreport.png"), RX, 1.88, COLW, 1.80, panel=RIVAL_BG)
marks(s, RX + 0.06, 3.80, COLW - 0.12, [
    "157 plugins, dynamic attacks built per target",
    "Free tier, 10k probes a month, one command",
    "Multimodal, coding agents, MCP tool poisoning",
], color=RIVAL, tcolor=INK, size=9.4, gap=0.28)
verdict(s, "Their scan runs tonight and finds 37 issues in 14 minutes. Agree "
           "with the buyer that it is good, then ask what happens on day two.",
        color=NAVY)
source(s, "help.accuknox.com/use-cases/red-teaming/  ·  "
          "promptfoo.dev/docs/red-team/plugins/ and /security/")

# =================================================================== 8. GUARDRAIL
s = content("Guardrails: a product for us, a page for them",
            "Module 5  ·  10 rows, 8 AccuKnox only")
split_heads(s, y=1.10)
shot(s, A("ak-promptfirewall.png"), LX, 1.68, COLW, 1.34)
marks(s, LX + 0.06, 3.20, COLW - 0.12, [
    "14 policy classes: block, sanitize or monitor",
    "PII, PHI and secrets masked in both directions",
    "Stateful across a whole multi-turn conversation",
    "Gateway, SDK, browser and Copilot Studio",
], color=PRIMARY, tcolor=NAVY, size=9.6)
box(s, RX, 1.68, COLW, 1.34, fill=RIVAL_BG, line=GREY_BD, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
box(s, RX + 0.18, 1.78, COLW - 0.36, 0.36,
    text="One marketing page, no product docs", size=12, color=RIVAL, bold=True,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, RX + 0.18, 2.18, COLW - 0.36, 0.74,
    text="The open-source `guardrails` assertion only reads a verdict that AWS "
         "Bedrock or Azure OpenAI already produced. It enforces nothing itself, "
         "and returns a zero score on every other provider.",
    size=9.6, color=INK, anchor=MSO_ANCHOR.TOP)
marks(s, RX + 0.06, 3.20, COLW - 0.12, [
    "No secrets detection in prompts",
    "No ban-topics, ban-competitor or regex policy",
    "No stateful multi-turn tracking at run time",
    "No named AI gateway integrations",
], color=RIVAL, tcolor=INK, tick="✕", size=9.6)
verdict(s, "They can test a guardrail. We are the guardrail. That distinction "
           "is the whole slide.")
source(s, "help.accuknox.com/use-cases/prompt-firewall-overview/  ·  "
          "promptfoo.dev/guardrails/ and the guardrails assert doc")

# =================================================================== 9. AGENTIC
s = content("Agentic AI and MCP: enforcement against inspection",
            "Module 6  ·  we split this one")
split_heads(s, y=1.10, lsub="RUNTIME ENFORCEMENT",
            rsub="PROXY AND TESTING")
marks(s, LX + 0.06, 1.90, COLW - 0.12, [
    "eBPF and LSM sandbox per agent",
    "Process, file, network and credential isolation",
    "MCP tool execution held to least privilege",
    "Memory poisoning stopped before the decision",
], color=PRIMARY, tcolor=NAVY, size=9.8, gap=0.32)
shot(s, A("ak-asset-detail.png"), LX, 3.24, COLW, 1.30, panel=GREY_BG)
shot(s, A("pf-mcpalert.png"), RX, 1.88, COLW, 1.28, panel=RIVAL_BG)
marks(s, RX + 0.06, 3.28, COLW - 0.12, [
    "MCP proxy allowlists approved servers, we do not",
    "Request logging with alerts on data exposure",
    "Strong adversarial tests for tool poisoning",
    "No kernel-level enforcement anywhere",
], color=RIVAL, tcolor=INK, size=9.6, gap=0.30)
verdict(s, "They stop an agent from reaching an unapproved MCP server. We stop "
           "the agent process from reading the file it was told to exfiltrate.",
        color=NAVY)
source(s, "help.accuknox.com/use-cases/modelarmor/ and accuknox.com/solutions/"
          "agentic-ai-security  ·  promptfoo.dev/mcp/")

# =================================================================== 10. AGENTZ
s = content("AgentZ: the category they have no answer to",
            "A separate AccuKnox product, not part of AI-SPM")
box(s, LX, 1.10, 9.20, 0.36,
    text="AgentZ is where you build and run agents. The eight AI security "
         "modules secure agents you already run. Different product, different "
         "buyer, same platform.",
    size=9.6, color=MUTE, italic=True, anchor=MSO_ANCHOR.MIDDLE,
    fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, ml=0.16)
split_heads(s, y=1.58)
shot(s, A("agentz.png"), LX, 2.14, COLW, 1.42)
marks(s, LX + 0.06, 3.68, COLW - 0.12, [
    "Default-deny sandbox from the very first run",
    "Egress allowed or blocked at the kernel, by domain",
    "Agents never hold secrets, credentials injected scoped",
    "Replayable audit trace, RBAC down to the tool call",
], color=PRIMARY, tcolor=NAVY, size=9.4, gap=0.28)
box(s, RX, 2.14, COLW, 1.42, fill=RIVAL_BG, line=GREY_BD, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
box(s, RX + 0.20, 2.34, COLW - 0.40, 0.44, text="Not a harness",
    size=16, color=RIVAL, bold=True, align=PP_ALIGN.CENTER,
    anchor=MSO_ANCHOR.MIDDLE)
box(s, RX + 0.20, 2.80, COLW - 0.40, 0.66,
    text="Promptfoo tests agents that something else builds and runs. There is "
         "nothing to compare on this slide, and that is the point.",
    size=10, color=INK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
marks(s, RX + 0.06, 3.68, COLW - 0.12, [
    "No skills, workflows, scheduling or teams",
    "No credential broker, no runtime injection",
    "No kernel egress policy per agent",
    "No air-gapped agent runtime",
], color=RIVAL, tcolor=INK, tick="✕", size=9.4, gap=0.28)
verdict(s, "Free tier for two users, on-prem and air-gapped on Enterprise, "
           "model agnostic on your own key.")
source(s, "accuknox.com/platform/agentz and github.com/accuknox/agentZ")

# =================================================================== 11. DEPLOY
s = content("Deployment, compliance and the vendor question",
            "Modules 9 and 11  ·  where procurement decides")
split_heads(s, y=1.10)
rows2 = [
    ("SaaS", "Yes", "Yes"),
    ("Self-hosted", "Helm on K8s or 3-node VM, full parity",
     "Docker, Compose, Helm marked experimental"),
    ("Air-gapped", "Yes, documented", "Not documented"),
    ("Horizontal scale, self-hosted", "Yes", "SQLite, single replica only"),
    ("OWASP, NIST AI RMF, EU AI Act", "Yes", "Yes"),
    ("Compliance beyond AI", "CIS, PCI-DSS, SOC 2, HIPAA, ISO 27001", "No"),
    ("Vendor", "Independent", "Part of OpenAI, stated on their site"),
]
y0 = 1.74
for i, (label, lv, rv) in enumerate(rows2):
    y = y0 + i * 0.44
    bg = WHITE if i % 2 else GREY_BG
    box(s, LX, y, 9.20, 0.40, fill=bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
        radius=0.04)
    box(s, LX + 0.14, y, 2.60, 0.40, text=label, size=9.4, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 3.06, y, 3.30, 0.40, text=lv, size=9.2, color=PRIMARY,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 6.42, y, 3.18, 0.40, text=rv, size=9.2,
        color=RIVAL if rv in ("No", "Not documented") else INK,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
verdict(s, "For BFSI, government and PSU buyers, raise the ownership question "
           "factually once, then move on. Do not oversell it.", color=NAVY)
source(s, "help.accuknox.com/how-to/aiml-saas-vs-onprem/  ·  "
          "promptfoo.dev/docs/usage/self-hosting/ and the site-wide banner")

# =================================================================== 12. CLOSE
s = prs.slides.add_slide(L_DIV)
blank_footer(s)
box(s, 0.70, 0.86, 8.6, 0.32, text="HOW TO RUN THE CONVERSATION", size=12,
    color=SECOND, bold=True)
box(s, 0.70, 1.22, 3.2, 0.035, fill=PRIMARY)
box(s, 0.66, 1.38, 8.7, 0.86, text="Four moves, in this order", size=32,
    color=WHITE, bold=True, anchor=MSO_ANCHOR.TOP)
plays = [
    ("01", "Concede red teaming",
     "Say it first. 157 plugins, free tier, dynamic attacks. Arguing costs you the room."),
    ("02", "Ask for the inventory",
     "How many AI apps, agents and MCP servers are running today? The pause is the pitch."),
    ("03", "Run Shadow AI beside their scan",
     "Same cloud account, same week. Show them assets that were never on the list."),
    ("04", "Close on day two",
     "A scan is a Tuesday. Posture, firewall and AI-DR are every day after it."),
]
for i, (n, head, sub) in enumerate(plays):
    y = 2.34 + i * 0.66
    box(s, 0.70, y, 0.52, 0.54, text=n, size=13, color=WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=PRIMARY,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.14)
    box(s, 1.34, y - 0.04, 3.10, 0.32, text=head, size=12, color=WHITE,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 4.44, y - 0.02, 4.86, 0.58, text=sub, size=9.6, color=NAVY_TXT,
        anchor=MSO_ANCHOR.MIDDLE)
box(s, 0.70, 5.06, 8.6, 0.30,
    text="Full 85-row battlecard with every source URL: "
         "accuknox-vs-promptfoo-ai-security.xlsx",
    size=9, color=SECOND, italic=True, anchor=MSO_ANCHOR.MIDDLE)

prs.save(OUT)
print("saved:", os.path.abspath(OUT))
print("slides:", len(prs.slides.__iter__.__self__._sldIdLst))
