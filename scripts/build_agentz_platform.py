# -*- coding: utf-8 -*-
"""
AgentZ, the Zero Trust Agentic AI Platform. AccuKnox branded, consolidated deck.

Rebuilds "AgentZ _ Agentic AI Security _ AUGUST 2026.pptx" (39 slides) as 25 slides
on the AccuKnox master template. Both decks run at 10 x 5.625 in, so every geometry
here is a direct redraw, not a rescale.

What changed against the source
  - Source 2, 3 and 4 become one gap-and-answer ledger (slide 2).
  - Source 12 and 13 become one slide: the four moves plus the security DNA (slide 10).
  - Source 18 and 19 become one paired slide: blast radius and runtime audit (slide 15).
  - Source 15 and 24 become one slide: the object model plus a real environment scope.
  - Source 10 and 30 become one slide: six functions plus five concrete agents.
  - Source 25 and 26 become one slide: the same workflow pushed and pulled.
  - Source 20 and 29 become one console proof slide.
  - The seven product tour video slides become two 4-up grids. Every tile keeps its
    Google Drive hyperlink, so a click still opens the recording.
  - The cover and the closing slide come from template layouts 0 and 1.
  - Em dashes, semicolons and sentences over 20 words are rewritten.

Build:   py -3.11 scripts/build_agentz_platform.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_AgentZ_Platform.pptx -Out output/render/agentz
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
TPL  = os.path.join(HERE, "..", "PPT Template.pptx")
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_AgentZ_Platform.pptx")
if len(sys.argv) > 1:                # build somewhere else when the deck is open
    OUT = sys.argv[1]
IMG  = os.path.join(HERE, "..", "output", "assets", "agentz")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(TPL, OUT)
prs = Presentation(OUT)
L_STD = prs.slide_layouts[4]
xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try: prs.part.drop_rel(sid.get(qn('r:id')))
    except Exception: pass
    xml_slides.remove(sid)

def A(name): return os.path.join(IMG, name)


# ======================================================= portable icon glyphs
# Segoe MDL2 Assets renders every icon in this deck, and it ships only with
# Windows. Google Slides has no copy, so an imported deck draws a tofu box
# wherever a live glyph sits. Rasterise each glyph to a transparent PNG once and
# place a picture instead. The deck then carries its own icons and imports
# anywhere. Cached under output/assets/glyphs, so a rebuild costs nothing.
GLYPHS   = os.path.join(HERE, "..", "output", "assets", "glyphs")
MDL2_TTF = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "segmdl2.ttf")
os.makedirs(GLYPHS, exist_ok=True)
_GCACHE = {}


def _rgb(c):
    h = str(c)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def glyph_png(glyph, color, px=320):
    """Return (path, aspect) for one MDL2 glyph drawn in `color` on transparency."""
    cp = ord(glyph)
    key = (cp, str(color))
    if key in _GCACHE:
        return _GCACHE[key]
    path = os.path.join(GLYPHS, "mdl2-%04X-%s.png" % (cp, str(color)))
    if not os.path.exists(path):
        from PIL import Image, ImageDraw, ImageFont
        f = ImageFont.truetype(MDL2_TTF, int(px * 0.78))
        im = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.text((px * 0.11, px * 0.11), glyph, font=f, fill=_rgb(color) + (255,))
        im = im.crop(im.getbbox())
        im.save(path)
    from PIL import Image as _I
    w, h = _I.open(path).size
    _GCACHE[key] = (path, w / float(h))
    return _GCACHE[key]


def glyph_pic(s, cx, cy, height, glyph, color, max_w=None):
    """Centre a glyph picture on (cx, cy) at the given height, in inches."""
    path, ar = glyph_png(glyph, color)
    w = height * ar
    if max_w and w > max_w:           # wide glyphs, the eye and the doc, must not
        height *= max_w / w           # touch the chip edge
        w = max_w
    return s.shapes.add_picture(path, Inches(cx - w / 2), Inches(cy - height / 2),
                                Inches(w), Inches(height))


def icon(s, x, y, size, glyph, color=WHITE, bg=PRIMARY, radius=0.26, fsz=None):
    """Same call shape as _akdeck.icon, but the glyph is a picture, not text."""
    sp = box(s, x, y, size, size, fill=bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
             radius=radius, wrap=False, ml=0, mr=0, mt=0, mb=0)
    glyph_pic(s, x + size / 2, y + size / 2, (fsz or size * 42) / 72.0 * 1.06, glyph, color,
              max_w=size * 0.66)
    return sp


import _akdeck                      # noqa: E402  patch the helpers that draw icons too
_akdeck.icon = icon
MONO = _akdeck.MONO = "Courier New"      # Consolas does not exist outside Windows


# =================================================================== scaffold
def std(title, kicker, lede=None, source=None):
    s = prs.slides.add_slide(L_STD); set_title(s, title); blank_footer(s)
    if kicker:
        eyebrow(s, kicker, y=0.84, w=8.6)
    if lede:
        box(s, CX, 1.08, CW, 0.34, text=lede, size=10.2, color=MUTE,
            anchor=MSO_ANCHOR.TOP)
    if source:
        footer_note(s, source, y=5.26, size=7.4)
    return s


def label(s, x, y, text, w=4.4, color=GREY_TX, size=7.8, align=PP_ALIGN.LEFT):
    return box(s, x, y, w, 0.22, text=text.upper(), size=size, color=color,
               bold=True, align=align, anchor=MSO_ANCHOR.MIDDLE)


def band(s, y, text, h=0.44, fill=NAVY, color=WHITE, size=10.4, x=CX, w=CW, bold=True):
    return box(s, x, y, w, h, text=text, size=size, color=color, bold=bold,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=fill,
               shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)


def soft(s, x, y, w, h, text, size=9.4, color=NAVY, fill=GREY_BG, bold=False,
         align=PP_ALIGN.CENTER):
    return box(s, x, y, w, h, text=text, size=size, color=color, bold=bold,
               align=align, anchor=MSO_ANCHOR.MIDDLE, fill=fill,
               shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)


def panel(s, x, y, w, h, fill=WHITE, line=GREY_BD, radius=0.05, lw=1.0):
    return box(s, x, y, w, h, fill=fill, line=line, line_w=lw,
               shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)


def accent_card(s, x, y, w, h, head, body, accent=PRIMARY, ic=None,
                hsize=11.0, bsize=8.6, fill=WHITE, hcolor=NAVY, bcolor=MUTE):
    """White card with a coloured top rule, an optional icon chip and two texts."""
    panel(s, x, y, w, h, fill=fill)
    box(s, x, y, w, 0.075, fill=accent, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    ty = y + 0.16
    if ic:
        icon(s, x + 0.16, ty, 0.40, G(ic), bg=accent, fsz=15)
        box(s, x + 0.62, ty - 0.02, w - 0.76, 0.44, text=head, size=hsize, color=hcolor,
            bold=True, anchor=MSO_ANCHOR.MIDDLE)
        ty += 0.50
    else:
        box(s, x + 0.16, ty, w - 0.32, 0.40, text=head, size=hsize, color=hcolor,
            bold=True, anchor=MSO_ANCHOR.TOP)
        ty += 0.42
    box(s, x + 0.17, ty, w - 0.34, y + h - ty - 0.10, text=body, size=bsize,
        color=bcolor, anchor=MSO_ANCHOR.TOP)


def node(s, x, y, w, h, text, fill=WHITE, color=NAVY, size=8.6, sub=None,
         line=GREY_BD, bold=True, ssize=7.4, scolor=MUTE, lw=1.0, radius=0.10):
    """A boxed diagram node, with an optional second line."""
    panel(s, x, y, w, h, fill=fill, line=line, radius=radius, lw=lw)
    if sub:
        box(s, x + 0.04, y, w - 0.08, h * 0.50, text=text, size=size, color=color,
            bold=bold, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM, mt=0, mb=0)
        box(s, x + 0.04, y + h * 0.50, w - 0.08, h * 0.50, text=sub, size=ssize,
            color=scolor, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, mt=0.01, mb=0)
    else:
        box(s, x + 0.04, y, w - 0.08, h, text=text, size=size, color=color, bold=bold,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def head_node(s, x, y, w, h, text, fill=NAVY, color=WHITE, size=8.6, **kw):
    return node(s, x, y, w, h, text, fill=fill, color=color, size=size, line=None, **kw)


def num_chip(s, x, y, size, text, bg=PRIMARY, color=WHITE, fsz=None):
    """A rounded chip holding a digit. icon() cannot do this: Segoe MDL2 has no digits."""
    sp = box(s, x, y, size, size, fill=bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.24,
             anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0, mr=0, mt=0, mb=0)
    p = sp.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.name = FONT; r.font.size = Pt(fsz or size * 40); r.font.bold = True
    r.font.color.rgb = color
    return sp


def tri(s, cx, cy, size=0.11, color=GREY_BD, rot=90):
    t = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE,
                           Inches(cx - size / 2), Inches(cy - size / 2),
                           Inches(size), Inches(size))
    t.rotation = rot
    t.fill.solid(); t.fill.fore_color.rgb = color
    t.line.fill.background(); t.shadow.inherit = False
    return t


def cx_h(s, x, y, w, color=GREY_BD, tag=None, tcolor=MUTE, tsize=7.0, lw=0.020):
    """Horizontal connector with a right arrowhead. y is the centre line."""
    box(s, x, y - lw / 2, w - 0.07, lw, fill=color)
    tri(s, x + w - 0.05, y, color=color, rot=90)
    if tag:
        box(s, x - 0.10, y - 0.28, w + 0.20, 0.22, text=tag, size=tsize, color=tcolor,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0, mr=0)


def cx_v(s, x, y, h, color=GREY_BD, tag=None, tcolor=MUTE, tsize=7.0, lw=0.020,
         tag_w=1.4, tag_dx=0.08):
    """Vertical connector with a down arrowhead. x is the centre line."""
    box(s, x - lw / 2, y, lw, h - 0.07, fill=color)
    tri(s, x, y + h - 0.05, color=color, rot=180)
    if tag:
        box(s, x + tag_dx, y + h / 2 - 0.13, tag_w, 0.24, text=tag, size=tsize,
            color=tcolor, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0.02, mr=0)


def rel_row(s, x, y, w, left, rel, right, h=0.40, lw_=1.60):
    """[left] --rel--> [right] on one line, inside width w."""
    rw = w - lw_ - 0.72
    node(s, x, y, lw_, h, left, fill=LAV, color=NAVY, size=8.4)
    cx_h(s, x + lw_ + 0.06, y + h / 2, 0.60, color=SECOND, tag=rel, tcolor=PURPLE)
    node(s, x + lw_ + 0.72, y, rw, h, right, fill=WHITE, color=NAVY, size=8.4)


def kv_row(s, x, y, w, k, v, h=0.32, kw_=0.98, ksize=7.8, vsize=8.0, fill=GREY_BG):
    box(s, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    box(s, x + 0.10, y, kw_, h, text=k, size=ksize, color=MUTE, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.10 + kw_, y, w - kw_ - 0.20, h, text=v, size=vsize, color=NAVY,
        anchor=MSO_ANCHOR.MIDDLE, font=MONO)


def chip_row(s, x, y, w, items, h=0.30, gap=0.08, fill=LAV, color=PURPLE, size=7.6):
    n = len(items)
    cw = (w - gap * (n - 1)) / n
    for i, it in enumerate(items):
        soft(s, x + i * (cw + gap), y, cw, h, it, size=size, color=color, fill=fill,
             bold=True)


# =================================================================== 1 cover
cover_slide(prs, "Zero Trust Agentic AI Platform",
            subtitle="AgentZ. Build, run and govern agents.", tsize=25, ssize=11.5)


# ================================================= 2 the gap and the answer
s = std("AI agents arrive faster than the controls", "market context",
        "Agents are autonomous, privileged and ungoverned. They act on their own, "
        "they need real credentials, and no standard sandbox exists.")
label(s, CX + 0.02, 1.56, "what builders want", w=4.4)
panel(s, CX, 1.80, 4.42, 0.56)
box(s, CX + 0.14, 1.80, 4.14, 0.56, text="Ship agents fast  ·  Use any model or framework  ·  "
    "Connect real tools and data  ·  Automate on a schedule", size=8.4, color=NAVY,
    anchor=MSO_ANCHOR.MIDDLE)
label(s, 5.20, 1.56, "what security fears", w=4.4)
panel(s, 5.18, 1.80, 4.42, 0.56)
box(s, 5.32, 1.80, 4.14, 0.56, text="Leaked API keys and secrets  ·  Agents with too much access  ·  "
    "No visibility into actions  ·  No audit", size=8.4, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)

soft(s, CX, 2.52, 4.42, 0.26, "THE GAP IN EVERY UNGUARDED DEPLOYMENT", size=7.6,
     color=RED, fill=RED_LT, bold=True)
soft(s, 5.18, 2.52, 4.42, 0.26, "WHAT AGENTZ DOES INSTEAD", size=7.6,
     color=PRIMARY, fill=LAV, bold=True)
LEDGER = [
    ("Credentials in the clear", "Raw keys land in prompts, logs and memory.",
     "Credential-less by design", "A proxy injects vault tokens. Agents never see a key."),
    ("Over-broad access", "Full cloud roles and open egress, far past the task.",
     "Scoped environments", "One environment names packages, domains, tools and skills."),
    ("No runtime visibility", "Nobody sees what the agent reads, writes or sends.",
     "Every action enforced", "File, process, network and domain activity is restricted."),
    ("No compliance story", "No tenancy isolation, no baseline, no audit trail.",
     "Audit and reuse by default", "Signed traces, reusable workflows, no provider lock-in."),
]
ly = 2.86
for g_h, g_b, a_h, a_b in LEDGER:
    for x, w, hd, bd, ac, fl in ((CX, 4.42, g_h, g_b, RED, RED_LT),
                                 (5.18, 4.42, a_h, a_b, PRIMARY, LAV)):
        box(s, x, ly, w, 0.46, fill=fl, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.10)
        box(s, x, ly + 0.05, 0.055, 0.36, fill=ac)
        box(s, x + 0.16, ly + 0.02, w - 0.30, 0.22, text=hd, size=9.2, color=NAVY,
            bold=True, anchor=MSO_ANCHOR.MIDDLE)
        box(s, x + 0.16, ly + 0.23, w - 0.30, 0.21, text=bd, size=7.6, color=MUTE,
            anchor=MSO_ANCHOR.MIDDLE)
    tri(s, 4.89, ly + 0.23, size=0.13, color=SECOND, rot=90)
    ly += 0.52
band(s, 4.98, "AgentZ closes the gap. Builders move fast and security stays in control.")


# ============================================== 3 why pilots stall (source 5)
s = std("Why agent pilots stall before production", "the pattern",
        "Four failure modes end most agent pilots. AgentZ answers each one by default.")
STALL = [
    ("bug", "Locked to one model",
     "The vendor picks the model. No bring-your-own key, no bring-your-own "
     "subscription, no swap when something better ships.",
     "Model agnostic. Your key or your subscription."),
    ("cloud", "SaaS or nothing",
     "No on-prem. No air gap. Regulated and sovereign workloads never clear review.",
     "On-prem, air-gapped or SaaS."),
    ("warn", "Security bolted on later",
     "Standing credentials, wide scopes, open egress. The demo works. The security "
     "review kills it.",
     "Zero Trust and default deny out of the box."),
    ("eye", "Blind at runtime",
     "No traces, no telemetry, no record of what the agent actually touched or sent.",
     "A signed trace for every span and tool call."),
]
cw = (CW - 0.36) / 4
for i, (g, h_, b_, ans) in enumerate(STALL):
    x = CX + i * (cw + 0.12)
    accent_card(s, x, 1.52, cw, 1.92, h_, b_, accent=RED, ic=g, hsize=10.6, bsize=8.4)
    label(s, x, 3.58, "agentz answer", w=cw, color=PRIMARY, size=7.2)
    soft(s, x, 3.82, cw, 0.86, ans, size=8.8, color=NAVY, fill=LAV, bold=True)
band(s, 4.84, "The demo lands. The rollout does not. AgentZ closes the gap between the two.", h=0.48)


# ================================== 4 why AgentZ, not the alternatives (src 6)
s = std("Why AgentZ, not the alternatives", "positioning",
        "Four questions decide every agent platform review. Only one column answers all four.")
COLS = [("Hosted assistants", "Claude, ChatGPT"), ("Self-hosted runners", "Hermes and friends"),
        ("Hardened OSS sandboxes", "OpenClaw and friends"), ("AgentZ", "AccuKnox")]
ROWS = [("Model choice", ["Locked to the vendor", "Bring your own, you wire it",
                          "Bring your own, you wire it", "Model agnostic. Your key or your subscription."]),
        ("Deployment", ["SaaS only", "You provision and run the box",
                        "You provision and run the box", "On-prem, air-gapped or SaaS"]),
        ("Security posture", ["Vendor defined, opaque", "Bolt on your own services",
                              "Secure by default, rough UX", "Zero Trust, default deny, out of the box"]),
        ("Time to first agent", ["Minutes, then a dead end", "VM, install, providers, security, MCP by hand",
                                 "Heavy setup, then fight the sandbox", "Three steps in the UI"])]
LX, LW, VW, GP = CX, 1.70, 1.83, 0.06
for i, (t, sub) in enumerate(COLS):
    x = LX + LW + GP + i * (VW + GP)
    last = (i == 3)
    node(s, x, 1.42, VW, 0.60, t, sub=sub, fill=PRIMARY if last else GREY_BG,
         color=WHITE if last else NAVY, scolor=LAV if last else GREY_TX,
         line=None if last else GREY_BD, size=8.6, ssize=6.6)
ry = 2.08
for name, vals in ROWS:
    soft(s, LX, ry, LW, 0.66, name, size=8.8, color=NAVY, fill=LAV, bold=True)
    for i, v in enumerate(vals):
        x = LX + LW + GP + i * (VW + GP)
        last = (i == 3)
        node(s, x, ry, VW, 0.66, v, fill=LAV if last else WHITE,
             color=NAVY if last else MUTE, size=8.2, bold=last,
             line=PRIMARY if last else GREY_BD, lw=1.25 if last else 1.0)
    ry += 0.72
band(s, 5.04, "Builders keep the speed. Security keeps the control plane.", h=0.38, size=9.8)


# ================================================= 5 one control plane (src 7)
s = std("One control plane", "the platform",
        "Six objects cover the whole life of an agent, from a packaged skill to a signed trace.")
PLANE = [("star", "Skills", "Package a capability once. Version it, test it, share it across every agent."),
         ("sitemap", "Workflows", "Chain skills. Trigger on a schedule, an event or a request. Watch the graph run live."),
         ("books", "Context", "Shared memory, files and knowledge at the organization level, not just per user."),
         ("people", "Teams", "Roles, ownership and scope, so every function ships agents, not just the platform team."),
         ("shield", "Guardrails", "Scoped secrets, allow-listed egress, approval on anything irreversible."),
         ("doc", "Audit", "Every span, tool call and token in a signed, replayable record.")]
cw = (CW - 0.24) / 3
for i, (g, h_, b_) in enumerate(PLANE):
    x = CX + (i % 3) * (cw + 0.12)
    y = 1.50 + (i // 3) * 1.44
    accent_card(s, x, y, cw, 1.34, h_, b_, accent=PRIMARY if i < 3 else PURPLE,
                ic=g, hsize=11.5, bsize=8.5)
for x, ttl, sub in ((CX, "YOUR TOOLS AND DATA", "Databases  ·  SaaS APIs  ·  MCP tools  ·  Files"),
                    (5.18, "ANY MODEL, ANY PROVIDER", "OpenAI  ·  Anthropic  ·  Gemini  ·  Open source  ·  Your own")):
    panel(s, x, 4.42, 4.42, 0.72, fill=NAVY, line=None)
    box(s, x + 0.16, 4.50, 4.10, 0.26, text=ttl, size=8.2, color=SECOND, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.16, 4.74, 4.10, 0.30, text=sub, size=8.8, color=WHITE,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ======================================== 6 secure and governed by default (8)
s = std("Secure by default, governed by default", "zero trust",
        "Default deny. An agent reaches no domain until you allow it and holds no secret until you grant it.")
panel(s, CX, 1.46, CW, 0.52, fill=NAVY_DK, line=None)
box(s, CX + 0.20, 1.46, CW - 0.40, 0.52, text="Anything irreversible waits on a person. "
    "Nothing about that is optional or configurable away.", size=9.8, color=WHITE,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
SEC = [("01", "key", "Credentials, handled",
        "Secrets stay in the vault. Agents get scoped access at the moment they need it and never see the key."),
       ("02", "lock", "Just-enough access",
        "Every skill runs on the narrowest permissions that finish the job. No standing cloud roles."),
       ("03", "eye", "Runtime you can see",
        "Every egress logged by domain, port and protocol, allowed or blocked at the kernel."),
       ("04", "doc", "Audit, out of the box",
        "A signed trace for every run, so SOC and compliance reviews stop being a project.")]
cw = (CW - 0.36) / 4
for i, (num, g, h_, b_) in enumerate(SEC):
    x = CX + i * (cw + 0.12)
    panel(s, x, 2.14, cw, 1.86)
    box(s, x, 2.14, cw, 0.075, fill=PRIMARY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    box(s, x + 0.16, 2.22, 0.60, 0.34, text=num, size=17, color=SECOND, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    icon(s, x + cw - 0.56, 2.24, 0.38, G(g), bg=LAV, color=PRIMARY, fsz=14)
    box(s, x + 0.16, 2.60, cw - 0.32, 0.44, text=h_, size=11.0, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.TOP)
    box(s, x + 0.17, 2.98, cw - 0.34, 0.94, text=b_, size=8.4, color=MUTE,
        anchor=MSO_ANCHOR.TOP)
panel(s, CX, 4.12, CW, 0.94, fill=LAV, line=None)
box(s, CX + 0.20, 4.20, CW - 0.40, 0.24, text="GOVERNED FOR THE WHOLE ORGANIZATION",
    size=8.2, color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
box(s, CX + 0.20, 4.44, CW - 0.40, 0.56, text="Admins set roles and provision credentials, "
    "environments and workflows on behalf of the team. People request the exact access they "
    "need. Fine-grained RBAC gates every agent action.", size=9.0, color=NAVY,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)


# ================================================ 7 three steps (source 9)
s = std("Three steps to your first agent", "onboarding",
        "Sign up, scope a sandbox, run the workflow. No provisioning project in front of it.")
STEPS = [("1", "person", "Bring your LLM provider",
          "Sign up and connect a provider. Your API key or your existing subscription. Swap it whenever you want."),
         ("2", "shield", "Create a sandbox and an agent",
          "Pick the packages, scope the network egress, attach the secrets and MCP tools the job needs."),
         ("3", "rocket", "Run workflows securely",
          "Chat, API, CLI or a schedule. Watch the execution graph live and read the trace afterwards.")]
cw, gp = 2.86, 0.31
for i, (num, g, h_, b_) in enumerate(STEPS):
    x = CX + i * (cw + gp)
    panel(s, x, 1.52, cw, 2.06, fill=WHITE)
    box(s, x, 1.52, cw, 0.075, fill=PRIMARY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    num_chip(s, x + 0.20, 1.70, 0.52, num, bg=PRIMARY, fsz=20)
    icon(s, x + cw - 0.66, 1.72, 0.46, G(g), bg=LAV, color=PRIMARY, fsz=17)
    box(s, x + 0.20, 2.34, cw - 0.40, 0.46, text=h_, size=12.0, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.TOP)
    box(s, x + 0.21, 2.82, cw - 0.42, 0.70, text=b_, size=9.0, color=MUTE,
        anchor=MSO_ANCHOR.TOP)
    if i < 2:
        tri(s, x + cw + gp / 2, 2.55, size=0.17, color=SECOND, rot=90)
panel(s, CX, 3.74, CW, 0.94, fill=GREY_BG, line=None)
box(s, CX + 0.20, 3.82, CW - 0.40, 0.24, text="EVERYWHERE ELSE", size=8.4, color=RED,
    bold=True, anchor=MSO_ANCHOR.MIDDLE)
box(s, CX + 0.20, 4.06, CW - 0.40, 0.58, text="Provision a machine. Install the runner. "
    "Wire up the providers. Add the services that make it secure. Then hand-configure every "
    "MCP server, one client ID and callback URL at a time.", size=9.6, color=INK,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
band(s, 4.84, "Minutes to a working agent, not a quarter to a platform.", h=0.48, size=10.4)


# ============================================== 8 who this is built for (11)
s = std("Who this is built for", "audience",
        "A general purpose platform. These five groups feel the pain first.")
WHO1 = [("shield", "Security and platform leads",
         "They want agents in production. They cannot sign off on standing credentials, "
         "open egress or an unauditable runtime."),
        ("gears", "DevOps and SRE teams",
         "Buried in provisioning, access reviews and routine remediation. Every one of "
         "those is a workflow."),
        ("chip", "Internal AI platform teams",
         "Asked to give every function agents without becoming the bottleneck for every request.")]
WHO2 = [("briefcase", "Automation agencies and MSPs",
         "Build once, run it per client. Tenant isolation and a signed trace are the whole business case."),
        ("cert", "Regulated and sovereign enterprises",
         "Banking, healthcare, defence, public sector. On-prem or air-gapped, or it does not happen.")]
cw = (CW - 0.24) / 3
for i, (g, h_, b_) in enumerate(WHO1):
    accent_card(s, CX + i * (cw + 0.12), 1.50, cw, 1.52, h_, b_, accent=PRIMARY, ic=g,
                hsize=11.0, bsize=8.8)
for i, (g, h_, b_) in enumerate(WHO2):
    accent_card(s, CX + i * (4.52 + 0.16), 3.14, 4.52, 1.36, h_, b_, accent=PURPLE, ic=g,
                hsize=11.0, bsize=8.8)
band(s, 4.62, "Every one of them stalls at the same place. Security review.", h=0.42, size=10.2)


# ==================================== 9 what teams automate (source 10 + 30)
s = std("What teams automate with AgentZ", "use cases",
        "Six functions, one runtime. Five agents worth building in the first month.")
FUNC = [("gears", "IT and DevOps", "Triage alerts, run remediations, automate routine ops."),
        ("shield", "Security operations", "Enrich incidents and run guarded response workflows."),
        ("chart", "Data and reporting", "Pull, summarize and distribute recurring reports."),
        ("mail", "Customer ops", "Resolve tickets and update records with scoped access."),
        ("briefcase", "Back office", "Automate finance, HR and procurement under tight controls."),
        ("bulb", "Custom workflows", "Compose your own from marketplace building blocks.")]
cw = (CW - 0.30) / 3
for i, (g, h_, b_) in enumerate(FUNC):
    x = CX + (i % 3) * (cw + 0.15)
    y = 1.46 + (i // 3) * 0.66
    panel(s, x, y, cw, 0.58)
    icon(s, x + 0.10, y + 0.09, 0.40, G(g), bg=LAV, color=PRIMARY, fsz=15)
    box(s, x + 0.56, y + 0.03, cw - 0.66, 0.26, text=h_, size=9.6, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.56, y + 0.28, cw - 0.66, 0.26, text=b_, size=7.6, color=MUTE,
        anchor=MSO_ANCHOR.MIDDLE)
label(s, CX, 2.86, "five agents worth building first", w=6.0, color=PRIMARY)
AG = [("Access that expires actually expires", "SECURITY AND IT",
       "The agent watches your provisioning board. When a ticket ETA passes, it posts the owner "
       "and the assignee to the team channel. The resource gets torn down."),
      ("Monday morning docs digest", "ENABLEMENT AND SALES",
       "The agent reads the commits from last week on the docs repo. It works out which pages "
       "changed and what changed. Then it sends a linked digest to sales."),
      ("GitHub issue to Jira to Slack", "ENGINEERING",
       "New issues get triaged and mirrored into the right Jira project. The owning squad is "
       "pinged with the context already attached."),
      ("Guarded incident response", "SECURITY OPERATIONS",
       "The agent enriches the alert across your real tools and proposes the containment step. "
       "It waits for a human before anything irreversible."),
      ("Reports that file themselves", "DATA AND BACK OFFICE",
       "On a schedule, the agent pulls from databases, dashboards and SaaS APIs. It writes the "
       "summary and drops it where the team already looks.")]
ay = 3.12
for h_, team, b_ in AG:
    panel(s, CX, ay, CW, 0.42, fill=GREY_BG, line=None, radius=0.10)
    box(s, CX, ay + 0.05, 0.055, 0.32, fill=PRIMARY)
    box(s, CX + 0.14, ay + 0.02, 2.66, 0.22, text=h_, size=9.0, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, CX + 0.14, ay + 0.22, 2.66, 0.18, text=team, size=6.6, color=PRIMARY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, CX + 2.92, ay, CW - 3.06, 0.42, text=b_, size=7.8, color=MUTE,
        anchor=MSO_ANCHOR.MIDDLE)
    ay += 0.46


# =================================== 10 four moves + security DNA (12 + 13)
s = std("Four moves, built on security DNA", "how it works",
        "From an empty environment to a scheduled, audited agent fleet.")
MOVES = [("1", "Define environment", "Set the packages, allowed domains, MCP tools and skills an agent may use."),
         ("2", "Bind secrets", "Map credentials to a secrets manager. Agents reference keys and never hold them."),
         ("3", "Deploy hardened", "Run on CIS and STIG hardened compute, with enforcement on every action."),
         ("4", "Schedule and scale", "Trigger workflows on a schedule. Reuse them and publish to the marketplace.")]
cw = (CW - 0.60) / 4
for i, (num, h_, b_) in enumerate(MOVES):
    x = CX + i * (cw + 0.20)
    panel(s, x, 1.46, cw, 1.30, fill=NAVY, line=None)
    box(s, x + 0.16, 1.54, 0.40, 0.30, text=num, size=15, color=SECOND, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.16, 1.84, cw - 0.32, 0.28, text=h_, size=10.4, color=WHITE, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.17, 2.12, cw - 0.34, 0.58, text=b_, size=8.2, color=NAVY_TXT,
        anchor=MSO_ANCHOR.TOP)
    if i < 3:
        tri(s, x + cw + 0.10, 2.11, size=0.15, color=SECOND, rot=90)
label(s, CX, 2.90, "why accuknox", w=6.0, color=PRIMARY)
DNA = [("cnapp", "Zero Trust CNAPP heritage",
        "AccuKnox secures cloud, containers, APIs and AI today. Agent security extends that work."),
       ("chip", "KubeArmor eBPF enforcement",
        "Open source inline enforcement at the kernel gives per-action control, already battle tested."),
       ("bolt", "AI Security 2.0",
        "Identity-first Zero Trust products for AI models, agents and MCP already ship today."),
       ("swap", "Model agnostic",
        "AgentZ is not tied to one LLM provider. Closed platforms secure only themselves.")]
cw = (CW - 0.36) / 4
for i, (g, h_, b_) in enumerate(DNA):
    accent_card(s, CX + i * (cw + 0.12), 3.14, cw, 1.34,
                h_, b_, accent=PURPLE, ic=('shield' if g == 'cnapp' else g),
                hsize=10.2, bsize=8.2)
band(s, 4.62, "The same four moves cover one pilot agent and a fleet of fifty.", h=0.42, size=10.2)


# ============================================ 11 platform map (source 14)
s = std("Where AgentZ sits in the AccuKnox AI platform", "platform map",
        "AgentZ is the runtime layer under the AI operator column.",
        source="Source: accuknox.com agentic AI security platform")
image_fit(s, A("Agentic-AI-Security-Platform.png"), 1.16, 1.46, 7.68, 3.66, frame=GREY_BD)


# ============================== 12 the environment object model (15 + 24)
s = std("The environment is the policy object", "object model",
        "Every agent binds to exactly one environment. The environment decides what it can reach.")
label(s, CX, 1.44, "how the objects relate", w=4.4)
REL = [("Users", "1:N", "AI agents"),
       ("AI agents", "M:N", "Sandbox environment"),
       ("AI agents", "1:N", "Workflows"),
       ("Sandbox", "1:1", "Credentials proxy")]
ry = 1.70
for a, r, b_ in REL:
    rel_row(s, CX, ry, 4.42, a, r, b_, h=0.40)
    ry += 0.46
label(s, CX, 3.60, "allow lists the sandbox holds", w=4.4)
code_block(s, CX, 3.84, 4.42, 1.14, [
    ("credentials", True), "ANTHROPIC_KEY  =>  *.anthropic.com",
    "GOOGLE_TOKEN  =>  *.google.com",
    ("domains", True), "*.acmeapi.com   *.accuknox.com",
    ("mcp  =>  packages", True),
    "AccuKnox, Atlassian  |  libcurl, nmap, libregex",
], size=7.4)

label(s, 5.18, 1.44, "sample scope, one soc agent", w=4.4)
SCOPE = [("Packages", "python3.12, curl, jq"), ("Domains", "6 allow-listed hosts"),
         ("Skills", "triage, enrich, report"), ("Identity", "one SPIFFE ID")]
ry = 1.70
for k, v in SCOPE:
    kv_row(s, 5.18, ry, 4.42, k, v, h=0.34, kw_=0.92)
    ry += 0.40
label(s, 5.18, 3.32, "allowed tools", w=4.4)
chip_row(s, 5.18, 3.54, 4.42, ["Gmail", "Slack", "AccuKnox MCP"], h=0.30)
chip_row(s, 5.18, 3.90, 4.42, ["MISP MCP", "AlienVault MCP"], h=0.30)
label(s, 5.18, 4.26, "llm providers", w=4.4)
chip_row(s, 5.18, 4.48, 4.42, ["OpenAI", "OpenRouter", "Anthropic"], h=0.30,
         fill=GREY_BG, color=NAVY)
box(s, 5.18, 4.82, 4.42, 0.24, text="AccuKnox CNAPP is reached through the AccuKnox MCP server.",
    size=7.4, color=GREY_TX, italic=True, anchor=MSO_ANCHOR.MIDDLE)
band(s, 5.10, "Anything outside these lists is denied at the kernel and written to the audit log.",
     h=0.40, size=9.8)


# ============================================ 13 systems architecture (16)
s = std("Systems architecture", "deployment view",
        "One Kubernetes cluster holds the runtime, the credentials proxy and the vault.")
# clients
CLIENTS = [("User browser", None, 1.62), ("Integrations", "Slack, Telegram, Discord", 2.44),
           ("OpenCode client", None, 3.26)]
for t, sub, y in CLIENTS:
    node(s, CX, y, 1.34, 0.60, t, sub=sub, fill=GREY_BG, size=8.2, ssize=6.8)
# cluster
panel(s, 2.02, 1.46, 5.62, 3.40, fill=WHITE, line=SECOND, lw=1.25)
box(s, 2.14, 1.52, 1.90, 0.24, text="KUBERNETES CLUSTER", size=7.8, color=PURPLE, bold=True,
    anchor=MSO_ANCHOR.MIDDLE)
node(s, 2.18, 1.86, 1.50, 0.54, "Web management", fill=LAV, size=8.2)
node(s, 2.18, 2.62, 1.50, 0.64, "Agents runtime", sub="OpenCode server", fill=LAV, size=8.2, ssize=6.8)
node(s, 2.18, 3.44, 1.50, 0.64, "K8s CronJob", sub="Agent workflow", fill=LAV, size=8.2, ssize=6.8)
node(s, 3.92, 1.82, 1.54, 0.64, "Secrets manager", sub="OpenBao or AccuKnox", fill=GREY_BG,
     size=8.2, ssize=6.8)
node(s, 3.92, 2.66, 1.54, 0.56, "Credentials proxy", fill=PRIMARY, color=WHITE, line=None, size=8.2)
node(s, 5.70, 2.66, 1.54, 0.56, "Agent gateway", fill=PRIMARY, color=WHITE, line=None, size=8.2)
for y in (2.13, 2.94, 3.76):
    cx_h(s, 1.78, y, 0.36, color=SECOND)
cx_h(s, 3.72, 2.94, 0.18, color=SECOND)
cx_h(s, 5.50, 2.94, 0.18, color=SECOND)
cx_v(s, 4.69, 2.48, 0.16, color=GREY_BD)
box(s, 2.92, 2.40, 0.02, 0.22, fill=GREY_BD)
box(s, 2.92, 3.26, 0.02, 0.18, fill=GREY_BD)
for i, (t, tag) in enumerate((("API security", "AccuKnox"), ("Network", "Cilium"),
                              ("Sandboxing", "KubeArmor"))):
    node(s, 2.18 + i * 1.76, 4.22, 1.66, 0.48, t, sub=tag, fill=NAVY, color=WHITE,
         line=None, size=7.8, ssize=6.6, scolor=SECOND)
# external, reached through one egress spine out of the gateway
box(s, 7.43, 2.12, 0.02, 1.64, fill=SECOND)
cx_h(s, 7.26, 2.94, 0.19, color=SECOND)
for t, y in (("LLM providers", 1.86), ("MCP providers", 2.68), ("Internet", 3.50)):
    node(s, 8.00, y, 1.60, 0.52, t, fill=GREY_BG, size=8.2)
    cx_h(s, 7.44, y + 0.26, 0.58, color=SECOND)
band(s, 4.94, "Security controls sit inside the cluster, so no agent traffic leaves without a policy decision.",
     h=0.42, size=9.8)


# ========================================= 14 secure credentials handling (17)
s = std("Secure credentials handling", "credential broker",
        "Never expose a real credential to an agent. The proxy holds the mapping.")
node(s, 0.86, 1.50, 1.70, 0.52, "Agent workflow", fill=LAV, size=9.0)
node(s, 4.14, 1.50, 1.70, 0.52, "Credentials proxy", fill=PRIMARY, color=WHITE, line=None, size=9.0)
node(s, 7.42, 1.50, 1.70, 0.52, "GitHub MCP server", fill=GREY_BG, size=9.0)
cx_h(s, 2.62, 1.76, 1.44, color=SECOND, tag="placeholder key")
cx_h(s, 5.90, 1.76, 1.44, color=SECOND, tag="real key")
node(s, 4.14, 2.30, 1.70, 0.44, "Secrets manager", fill=NAVY, color=WHITE, line=None, size=8.4)
cx_v(s, 4.99, 2.04, 0.26, color=GREY_BD)
for x, ttl, lines in (
    (CX, "PLACEHOLDER KEYS THE AGENT SEES",
     ["ANTHROPIC_KEY  => CLAWARMOR_ANTHROPIC_KEY",
      "GITHUB_MCP_KEY => CLAWARMOR_GITHUB_MCP_KEY"]),
    (5.18, "VAULT MAPPING THE PROXY HOLDS",
     ["CLAWARMOR_ANTHROPIC_KEY  => /agent/anthropic_key  [*.anthropic.com]",
      "CLAWARMOR_GITHUB_MCP_KEY => /agent/github_key     [*.github.com]"])):
    code_block(s, x, 2.86, 4.42, 0.70, lines, size=6.8, title=ttl)
code_block(s, CX, 3.66, 4.42, 0.94, [
    "GET /api/v1/resource HTTP/1.1",
    "Host: mcp.github.com",
    ("Authorization: Bearer CLAWARMOR_GITHUB_MCP_KEY", True),
], size=7.4, title="STEP 1   REQUEST LEAVES THE AGENT")
code_block(s, 5.18, 3.66, 4.42, 0.94, [
    "GET /api/v1/resource HTTP/1.1",
    "Host: mcp.github.com",
    ("Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9", True),
], size=7.4, title="STEP 4   PROXY SWAPS IN THE REAL KEY")
for i, (num, t) in enumerate((("STEP 2", "Check domain access for the placeholder key in the request."),
                              ("STEP 3", "Map the placeholder to the real key held in the vault."))):
    x = CX + i * (4.42 + 0.34)
    soft(s, x, 4.72, 4.42, 0.42, "", fill=LAV)
    box(s, x + 0.14, 4.72, 0.60, 0.42, text=num, size=8.0, color=PRIMARY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.72, 4.72, 3.56, 0.42, text=t, size=8.4, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
band(s, 5.22, "The agent never holds a secret, so a leaked prompt or log leaks nothing.",
     h=0.32, size=9.4)


# ================================ 15 blast radius and runtime audit (18 + 19)
s = std("Blast radius, and the proof it held", "policy and enforcement",
        "The environment decides what an agent may reach. KubeArmor watches the same four planes.")
soft(s, CX, 1.44, 4.42, 0.28, "THE ENVIRONMENT SETS THE BLAST RADIUS", size=7.8,
     color=PRIMARY, fill=LAV, bold=True)
soft(s, 5.18, 1.44, 4.42, 0.28, "EVERY ACTION IS AUDITED AT RUNTIME", size=7.8,
     color=PURPLE, fill=GREY_BG, bold=True)
PAIRS = [(("books", "Packages", "Runtime libraries and dependencies available for agentic execution."),
          ("wrench", "Tool calls", "Every tool access and response is audited, with its parameters.")),
         (("globe", "External domains", "Allow-listed egress. The only destinations the agent may reach."),
          ("terminal", "System calls", "Every file, process and sensitive data access is audited.")),
         (("link", "MCP tools", "The specific Model Context Protocol tools the agent may call."),
          ("net", "Networks", "Egress is limited to allow-listed endpoints and ports.")),
         (("star", "Skills", "The curated skills and capabilities the agent can invoke at runtime."),
          ("route", "Domains", "DNS and domain access is matched against the environment list."))]
py = 1.82
for left, right in PAIRS:
    for (g, h_, b_), x, ac in ((left, CX, PRIMARY), (right, 5.18, PURPLE)):
        panel(s, x, py, 4.42, 0.72)
        icon(s, x + 0.14, py + 0.16, 0.40, G(g), bg=ac, fsz=15)
        box(s, x + 0.62, py + 0.06, 3.66, 0.26, text=h_, size=10.0, color=NAVY, bold=True,
            anchor=MSO_ANCHOR.MIDDLE)
        box(s, x + 0.62, py + 0.32, 3.66, 0.34, text=b_, size=8.0, color=MUTE,
            anchor=MSO_ANCHOR.TOP)
    py += 0.78
band(s, 5.00, "Change the environment and you change the blast radius. Audit is the default state.",
     h=0.42, size=10.0)


# ============================================== 16 unattended runs (src 21)
s = std("Scheduled and event driven workflows", "unattended runs",
        "Agent workflows run without a human present, on exactly the same policy.")
panel(s, CX, 1.50, CW, 0.56, fill=LAV, line=None)
box(s, CX + 0.20, 1.50, CW - 0.40, 0.56, text="Each invocation inherits the same environment "
    "scope, the same proxy broker and the same enforcement.", size=9.8, color=NAVY,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
RUN = [("clock", "Trigger", "A cron schedule, a webhook or an event fires the workflow.",
        ["cron", "webhook", "event"]),
       ("shield", "Scoped run", "The agent executes inside its hardened environment.",
        ["packages", "domains", "tools"]),
       ("doc", "Audit and result", "Actions are logged, outputs delivered, secrets never exposed.",
        ["trace", "output", "alert"])]
cw, gp = 2.88, 0.28
for i, (g, h_, b_, chips) in enumerate(RUN):
    x = CX + i * (cw + gp)
    panel(s, x, 2.24, cw, 1.90)
    box(s, x, 2.24, cw, 0.075, fill=PRIMARY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    icon(s, x + 0.20, 2.42, 0.46, G(g), bg=PRIMARY, fsz=17)
    box(s, x + 0.76, 2.40, cw - 0.94, 0.50, text=h_, size=12.0, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.21, 3.00, cw - 0.42, 0.62, text=b_, size=9.2, color=MUTE,
        anchor=MSO_ANCHOR.TOP)
    chip_row(s, x + 0.20, 3.70, cw - 0.40, chips, h=0.28)
    if i < 2:
        tri(s, x + cw + gp / 2, 3.19, size=0.17, color=SECOND, rot=90)
panel(s, CX, 4.36, CW, 0.76, fill=NAVY, line=None)
box(s, CX + 0.20, 4.36, CW - 0.40, 0.76, text="Concurrency, retries and resource quotas are "
    "governed centrally. Agents scale without widening the trust boundary.", size=10.2,
    color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# =============================== 17 finding enrichment, push and pull (25+26)
s = std("Finding enrichment, pushed and pulled", "event driven and scheduled",
        "Read the finding, ask threat intel for context, write the enriched result back through MCP.")
for x, ttl, sub, col in ((CX, "PUSH  ·  WEBHOOK", "A new CSPM finding enriches itself before an analyst opens it.", PRIMARY),
                         (5.18, "PULL  ·  CRON EVERY 15 MINUTES", "Use the schedule when the source system cannot send a webhook.", PURPLE)):
    soft(s, x, 1.44, 4.42, 0.28, ttl, size=7.8, color=col, fill=LAV if col == PRIMARY else GREY_BG,
         bold=True)
    box(s, x, 1.74, 4.42, 0.24, text=sub, size=8.0, color=MUTE, align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE)
CHAIN_L = [("AWS cloud accounts", "CSPM scan"), ("AccuKnox CNAPP", "Scanner, findings, rule engine"),
           ("AgentZ workflow", "Webhook fires the run"), ("AccuKnox MCP", "Tool: update_finding")]
CHAIN_R = [("AWS cloud accounts", "CSPM scan"), ("AccuKnox CNAPP", "Scanner, findings, finding store"),
           ("AgentZ workflow", "Cron every 15 minutes"), ("AccuKnox MCP", "get_finding, update_finding")]
for x, chain, col in ((CX, CHAIN_L, PRIMARY), (5.18, CHAIN_R, PURPLE)):
    NX, NW = x + 0.52, 3.36
    cy = 2.08
    ytop = cy
    for i, (t, sub) in enumerate(chain):
        last = (i == 3)
        node(s, NX, cy, NW, 0.52, t, sub=sub,
             fill=col if last else WHITE, color=WHITE if last else NAVY,
             scolor=LAV if last else MUTE, line=None if last else GREY_BD, size=9.0, ssize=7.2)
        if not last:
            cx_v(s, NX + NW / 2, cy + 0.54, 0.22, color=SECOND)
        cy += 0.74
    # the enriched result is written back into the finding store
    ybot = cy - 0.74 + 0.26          # centre of the MCP node
    yret = ytop + 0.74 + 0.26        # centre of the CNAPP node
    box(s, x + 0.20, yret, 0.02, ybot - yret, fill=GREY_BD)
    box(s, x + 0.20, ybot - 0.01, NX - x - 0.20, 0.02, fill=GREY_BD)
    box(s, x + 0.22, yret - 0.01, NX - x - 0.22 - 0.06, 0.02, fill=GREY_BD)
    tri(s, NX - 0.04, yret, size=0.10, color=GREY_BD, rot=90)
    box(s, x - 0.04, (yret + ybot) / 2 - 0.24, 0.52, 0.48, text="write\nback", size=6.8,
        color=GREY_TX, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
band(s, 4.92, "Every tool call lands in the audit trail, whether a webhook or a cron started the run.",
     h=0.42, size=10.0)


# ======================================== 18 automated alert investigation (27)
s = std("Automated alert investigation", "ai soc",
        "A KubeArmor policy violation becomes a written investigation report.")
# one left-to-right chain: where the alert starts, who runs it, what it reads, where it lands
node(s, CX, 1.66, 1.44, 0.76, "Kubernetes cluster", sub="KubeArmor", fill=GREY_BG,
     size=8.6, ssize=7.2)
panel(s, 2.20, 1.52, 2.22, 1.04, fill=WHITE, line=SECOND, lw=1.25)
box(s, 2.30, 1.57, 2.02, 0.22, text="ACCUKNOX CNAPP", size=7.4, color=PURPLE, bold=True,
    anchor=MSO_ANCHOR.MIDDLE)
node(s, 2.30, 1.84, 0.94, 0.62, "CWPP", fill=LAV, size=8.4)
node(s, 3.36, 1.84, 0.94, 0.62, "Triggers", fill=LAV, size=8.4)
cx_h(s, 1.88, 2.04, 0.30, color=SECOND, tag="alert")
node(s, 4.72, 1.66, 1.84, 0.76, "AgentZ workflow", sub="Alert investigation",
     fill=PRIMARY, color=WHITE, line=None, size=9.4, ssize=7.2, scolor=LAV)
cx_h(s, 4.48, 2.04, 0.22, color=SECOND)
node(s, 6.86, 1.66, 1.32, 0.76, "Threat intel", sub="MISP, AlienVault", fill=GREY_BG,
     size=8.8, ssize=7.0)
cx_h(s, 6.60, 2.04, 0.24, color=SECOND)
node(s, 8.48, 1.66, 1.12, 0.76, "Gmail, Slack", sub="Report out", fill=NAVY, color=WHITE,
     line=None, size=8.8, ssize=7.0, scolor=SECOND)
cx_h(s, 8.22, 2.04, 0.24, color=SECOND)
STEPS3 = [("1", "The webhook fires the workflow",
           "A KubeArmor policy violation hits the trigger and starts the run."),
          ("2", "The agent investigates",
           "Pull the alert, check the process tree, score the threat, enrich across threat intel."),
          ("3", "The report goes out",
           "A written investigation lands in Gmail and Slack, with the evidence attached.")]
cw3 = (CW - 0.28) / 3
for i, (num, h_, b_) in enumerate(STEPS3):
    x = CX + i * (cw3 + 0.14)
    panel(s, x, 2.76, cw3, 1.30)
    box(s, x, 2.76, cw3, 0.075, fill=PRIMARY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    num_chip(s, x + 0.16, 2.92, 0.40, num, bg=LAV, color=PRIMARY, fsz=15)
    box(s, x + 0.62, 2.90, cw3 - 0.78, 0.44, text=h_, size=10.4, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.17, 3.40, cw3 - 0.34, 0.58, text=b_, size=8.4, color=MUTE,
        anchor=MSO_ANCHOR.TOP)
band(s, 4.20, "The analyst reads a finished report instead of a raw alert.", h=0.46)
footer_note(s, "Every tool call in the run is written to the signed trace.", y=4.78, size=8.2)


# ===================================== 19 AccuKnox agentic AI integration (23)
s = std("AccuKnox agentic AI integration", "enterprise fit",
        "Twelve purpose-built agents, one MCP server, one control plane.")
panel(s, CX, 1.44, 3.34, 2.86, fill=WHITE, line=SECOND, lw=1.25)
box(s, CX + 0.16, 1.50, 3.02, 0.24, text="ACCUKNOX AGENTZ", size=7.8, color=PURPLE, bold=True,
    anchor=MSO_ANCHOR.MIDDLE)
AGENTS = ["SRE Agent", "AI SOC Agent", "ASPM Agent", "Custom Reporting", "Toxic Combinations",
          "CloudSecOps Agent", "Security Advisory", "Virtual Patch Agent", "Cloud CTEM Agent",
          "Policy Recommendation", "FedRAMP Compliance", "Blast Radius"]
for i, a in enumerate(AGENTS):
    x = CX + 0.16 + (i % 2) * 1.54
    y = 1.78 + (i // 2) * 0.40
    soft(s, x, y, 1.46, 0.34, a, size=7.4, color=NAVY, fill=LAV, bold=True)
node(s, 4.14, 2.16, 1.42, 0.66, "AccuKnox MCP", sub="Assets, findings, email", fill=PRIMARY,
     color=WHITE, line=None, size=8.8, ssize=7.0, scolor=LAV)
cx_h(s, 3.80, 2.49, 0.28, color=SECOND, tag="skills")
cx_h(s, 5.62, 2.49, 0.24, color=SECOND)
panel(s, 5.90, 1.44, 3.70, 1.42, fill=NAVY, line=None)
box(s, 5.98, 1.50, 3.54, 0.44, text="AccuKnox enterprise CNAPP control plane", size=10.2,
    color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
soft(s, 6.06, 1.98, 1.68, 0.36, "US production", size=8.0, color=NAVY, fill=SECOND, bold=True)
soft(s, 7.80, 1.98, 1.68, 0.36, "India production", size=8.0, color=NAVY, fill=SECOND, bold=True)
box(s, 5.98, 2.40, 3.54, 0.34, text="Two production environments, one policy model", size=7.8,
    color=NAVY_TXT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
node(s, 5.90, 2.98, 1.78, 0.52, "AccuKnox SIEM", fill=GREY_BG, size=8.6)
node(s, 7.82, 2.98, 1.78, 0.52, "Webhooks: IoCs", fill=GREY_BG, size=8.6)
label(s, CX, 4.42, "shared services", w=3.0, color=PRIMARY)
for i, t in enumerate(["Workflows in Git repos", "Secrets manager", "Triggers and schedules",
                       "Slack and email"]):
    soft(s, CX + i * 2.33, 4.68, 2.21, 0.50, t, size=8.6, color=NAVY, fill=GREY_BG, bold=True)


# ============================================== 20 token optimization (22)
s = std("Token optimization for deterministic steps", "cost control",
        "Deterministic work moves out of the model and into plain code.",
        source="Costs are for one workflow run, measured on the same trace.")
for ttl, img, y in (("BEFORE OPTIMIZATION", "trace-before.png", 1.42),
                    ("AFTER OPTIMIZATION", "trace-after.png", 2.32)):
    label(s, CX, y, ttl, w=4.0, color=GREY_TX)
    image_fit(s, A(img), CX, y + 0.22, CW, 0.62, frame=GREY_BD)
TAB = [["", "Input tokens", "Input cost", "Output tokens", "Output cost"],
       ["Before optimization", "90.2K", "20 cents", "10K", "25 cents"],
       ["After optimization", "8K", "4 cents", "1K", "2.5 cents"]]
table(s, CX, 3.26, CW, 0.90, TAB, colw=[2.40, 1.70, 1.70, 1.70, 1.70], hsize=8.6, bsize=9.0,
      aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER])
for i, (num, lab) in enumerate((("11x", "Fewer input tokens"), ("10x", "Fewer output tokens"),
                                ("83%", "Lower run cost"))):
    stat(s, CX + i * 3.14, 4.26, 2.92, num, lab, color=PRIMARY, nsize=24, lsize=9.4, h=0.90)


# ================================= 21 differentiation matrix (source 31)
s = std("Differentiation", "comparison",
        "Where AgentZ holds ground that agent frameworks do not.")
MCOLS = ["AccuKnox AgentZ", "Nous Hermes", "Kindo.AI", "OpenAI ONA"]
MROWS = [("Cloud or SaaS offering", [1, 1, 1, 1]),
         ("On-premise deployment", [1, 1, 0, 0]),
         ("Deterministic code cuts token cost", [1, 1, 0, 0]),
         ("Workflows triggered by webhooks", [1, 0, 0, 0]),
         ("Security hardening out of the box", [1, 0, 1, 1]),
         ("Agents never see credentials", [1, 0, 0, 0]),
         ("Every tool and network call visible", [1, 0, 0, 0]),
         ("Built-in memory", [1, 1, 1, 1]),
         ("Workflow marketplace", [1, 0, 0, 0]),
         ("Cost management", [1, 0, 1, 0])]
CAPW, VW2, GP2, RH = 3.46, 1.40, 0.06, 0.325
AGX = CX + CAPW + GP2
# one continuous highlight behind the AgentZ column, so the eye reads it as a block
box(s, AGX, 1.42, VW2, 0.34 + len(MROWS) * RH + 0.04, fill=LAV,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.03)
soft(s, CX, 1.42, CAPW, 0.34, "CAPABILITY", size=7.8, color=GREY_TX, fill=GREY_BG, bold=True,
     align=PP_ALIGN.LEFT)
for i, c in enumerate(MCOLS):
    x = AGX + i * (VW2 + GP2)
    first = (i == 0)
    soft(s, x, 1.42, VW2, 0.34, c, size=7.8, color=WHITE if first else NAVY,
         fill=PRIMARY if first else GREY_BG, bold=True)
my = 1.80
for ri, (name, vals) in enumerate(MROWS):
    if ri % 2 == 0:
        box(s, CX, my, CAPW, RH - 0.02, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
            radius=0.14)
        box(s, AGX + VW2 + GP2, my, 3 * VW2 + 2 * GP2, RH - 0.02, fill=GREY_BG,
            shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.14)
    box(s, CX + 0.14, my, CAPW - 0.14, RH - 0.02, text=name, size=8.6, color=NAVY,
        anchor=MSO_ANCHOR.MIDDLE)
    for i, v in enumerate(vals):
        x = AGX + i * (VW2 + GP2)
        gl = G('check') if v else G('cancel')
        cl = (GREEN_DK if i == 0 else GREEN) if v else GREY_TX
        glyph_pic(s, x + VW2 / 2, my + (RH - 0.02) / 2, 0.155, gl, cl)
    my += RH
box(s, CX, my + 0.06, 4.20, 0.26, text="Ten rows. One column says yes to all ten.", size=9.2,
    color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
box(s, 4.70, my + 0.06, 4.90, 0.26, text="Competitor rows reflect the publicly documented "
    "feature set at the time of writing.", size=7.4, color=GREY_TX, italic=True,
    align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


# ==================================== 22 console proof (source 20 + 29)
s = std("Proof in the console", "product view",
        "Zero Trust policy per agent workload, a live agent inventory and a governance record.",
        source="Source: AccuKnox AI Security console")
SHOTS = [("Runtime agent sandboxing", "Ai-sec-Runtime-Agent-Sandboxing.png",
          "A KubeArmor policy scoped to one agent workload."),
         ("Managed agent inventory", "Ai-sec-Managed-Agents-View.png",
          "Every discovered agent, its region, version and findings."),
         ("Governance and violations", "agentic-ai-dashboard.png",
          "Policy failures by severity, application and owner.")]
sw = (CW - 0.28) / 3
for i, (ttl, img, cap) in enumerate(SHOTS):
    x = CX + i * (sw + 0.14)
    label(s, x, 1.48, ttl, w=sw, color=PRIMARY)
    image_fit(s, A(img), x, 1.74, sw, 1.90, frame=GREY_BD)
    box(s, x, 3.70, sw, 0.34, text=cap, size=7.8, color=MUTE, align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.TOP)
panel(s, CX, 4.22, CW, 0.74, fill=LAV, line=None)
box(s, CX + 0.20, 4.28, CW - 0.40, 0.24, text="WHAT THE AUDITOR ASKS FOR", size=8.2,
    color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
box(s, CX + 0.20, 4.52, CW - 0.40, 0.40, text="Which agents exist, what each one may reach, "
    "and what it actually did. All three answers already sit in the console.", size=9.6,
    color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)


# ================================================ 23 and 24 product tour grids
TOUR = [("01", "Create", "Spin up an agent",
         "Agent config sets the sandbox, immutable skills, persistent memory and the model. "
         "The provider list opens: Claude, Gemini, GPT, Qwen, Kimi, DeepSeek.",
         "tour-1-create.png", "http://drive.google.com/file/d/1wJwAwWu7RMkaMgOHz4xZKBOCjljjztEJ/view"),
        ("02", "Confine", "Grant the narrowest permissions",
         "The sandbox wizard end to end: identity, packages, MCP, skills and allowed hosts, "
         "landing on per-tool on and off switches.",
         "tour-2-confine.png", "http://drive.google.com/file/d/1CZXEuzY7NOIfWuCsk41UmV0VolZbLvRB/view"),
        ("03", "Connect", "Wire in the stack you already run",
         "Connect an MCP server, pick the provider, watch the connection flip to Ready in the "
         "MCP list. Twelve seconds to a live connection.",
         "tour-3-connect.png", "http://drive.google.com/file/d/1_gp8_d8r3B79lFWLDYcOORWdnrPL0yK1/view"),
        ("04", "Run", "Work in chat, against real files",
         "The Run Graph page, then the chat with the file explorer open and the run history in "
         "the sidebar. Artifacts land on disk.",
         "tour-4-run.png", "http://drive.google.com/file/d/19nB0yW2Z5JHFQBqadMYCqeQtmEc7G8VJ/view"),
        ("05", "Schedule", "Put the agent on a clock",
         "The trigger list with live cron expressions, then edit schedule with the cron field, "
         "timeout and history limits. No redeploy.",
         "tour-5-schedule.png", "http://drive.google.com/file/d/151_RXIma3bZ1CFs-OYOOkNANzsXQV-7x/view"),
        ("06", "Watch", "See every step as it runs",
         "Graph nodes moving through Running and Succeeded, with the instructions and done "
         "criteria open on a step.",
         "agentz-workflow-graph.png", "http://drive.google.com/file/d/1H3IBkvpJQnN-ipW9nnoxTTXFMvZdSXgJ/view"),
        ("07", "Prove", "Read the record afterwards",
         "A span tree with per-call durations and token counts, the network, process and file "
         "event tabs, and an inspected error.",
         "tour-7-prove.png", "http://drive.google.com/file/d/1kBtbgj9fhUe5JJfkUpjhAx93GBCkeEC-/view")]


def tour_tile(s, x, y, w, h, num, step, head, body, img, url):
    panel(s, x, y, w, h)
    box(s, x, y, w, 0.07, fill=PRIMARY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    iw = 2.30
    panel(s, x + 0.12, y + 0.16, iw, 1.24, fill=NAVY_DK, line=None, radius=0.06)
    pic = image_fit(s, A(img), x + 0.14, y + 0.18, iw - 0.04, 1.20, frame=None)
    pic.click_action.hyperlink.address = url
    pcx, pcy = x + 0.12 + iw / 2, y + 0.16 + 0.62
    play = box(s, pcx - 0.19, pcy - 0.19, 0.38, 0.38, fill=WHITE, shape=MSO_SHAPE.OVAL,
               wrap=False, ml=0, mr=0, mt=0, mb=0, anchor=MSO_ANCHOR.MIDDLE)
    play.click_action.hyperlink.address = url
    ptri = tri(s, pcx + 0.015, pcy, size=0.15, color=PRIMARY, rot=90)
    ptri.click_action.hyperlink.address = url
    tx = x + iw + 0.24
    tw = w - iw - 0.38
    box(s, tx, y + 0.16, tw, 0.22, text="STEP %s  ·  %s" % (num, step.upper()), size=7.2,
        color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, tx, y + 0.38, tw, 0.46, text=head, size=10.4, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.TOP)
    box(s, tx, y + 0.88, tw, h - 1.02, text=body, size=7.8, color=MUTE, anchor=MSO_ANCHOR.TOP)


s = std("Product tour, create to run", "recorded walkthrough",
        "Four clips, four minutes. Click any tile to open the recording.")
TW, TH = 4.44, 1.82
for i, t in enumerate(TOUR[:4]):
    tour_tile(s, CX + (i % 2) * (TW + 0.32), 1.46 + (i // 2) * (TH + 0.14), TW, TH, *t)
band(s, 5.24, "Create, confine, connect, run. The order never changes.", h=0.30, size=9.2)

s = std("Product tour, schedule to proof", "recorded walkthrough",
        "Three clips that cover unattended runs and the audit record.")
for i, t in enumerate(TOUR[4:]):
    tour_tile(s, CX + (i % 2) * (TW + 0.32), 1.46 + (i // 2) * (TH + 0.14), TW, TH, *t)
x4, y4 = CX + (TW + 0.32), 1.46 + (TH + 0.14)
panel(s, x4, y4, TW, TH, fill=NAVY, line=None)
box(s, x4, y4, TW, 0.07, fill=SECOND, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
box(s, x4 + 0.20, y4 + 0.18, TW - 0.40, 0.26, text="WHAT THE TOUR PROVES", size=8.0,
    color=SECOND, bold=True, anchor=MSO_ANCHOR.MIDDLE)
bullets(s, x4 + 0.22, y4 + 0.50, TW - 0.44, 1.20, [
    "Least privilege you can point at, per tool call.",
    "Unattended runs edited in place, with no redeploy.",
    "A signed span tree, not a claim about one.",
], size=8.8, color=WHITE, mcolor=SECOND, gap=5, marker="•")
band(s, 5.24, "Everything else is a claim. This is the evidence.", h=0.30, size=9.2)


# =================================================================== 25 closing
closing = closing_slide(prs, headline="Powered by Agentic AI.\nProtected by Zero Trust.",
                        contact="accuknox.com/demo", tsize=19, csize=13)
for ph in closing.placeholders:
    if ph.placeholder_format.idx == 0:
        left, width = ph.left, ph.width
        ph.left, ph.width = left, width
        ph.top, ph.height = Inches(1.82), Inches(0.94)
    elif ph.placeholder_format.idx == 1:
        left, width = ph.left, ph.width
        ph.left, ph.width = left, width
        ph.top, ph.height = Inches(2.80), Inches(0.44)

prs.save(OUT)
print("wrote %s  (%d slides)" % (os.path.abspath(OUT), len(prs.slides._sldIdLst)))
