# -*- coding: utf-8 -*-
"""
AccuKnox AgentZ, Security Hardened Sovereign Autonomous AI Agents.

Rebuilds the source draft ("AccuKnox AgentZ Harness.pptx", a Google Slides export)
on the AccuKnox master template at 10 x 5.625 in.

Changes on top of the source:
  - AccuKnox master layouts, palette, logo and Space Grotesk throughout.
  - The nine flat card images from the source are rebuilt as native shapes, so
    every word stays editable and the type matches the brand.
  - The four hand-drawn architecture diagrams are redrawn on the brand grid.
  - Three part dividers, so the pitch, the architecture and the use cases read
    as one deck.
  - Real product imagery pulled from accuknox.com fills the platform,
    sandboxing and governance slides.
  - Em dashes, semicolons and sentences over 20 words are rewritten.

Build:   py -3.11 scripts/build_agentz_harness.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_AgentZ_Harness.pptx -Out output/render/agentz
"""
import os, shutil, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import *          # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "PPT Template.pptx")
IMG  = os.path.join(HERE, "..", "output", "assets", "agentz")
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_AgentZ_Harness.pptx")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_DIV, L_STD = prs.slide_layouts[2], prs.slide_layouts[4]
xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try: prs.part.drop_rel(sid.get(qn('r:id')))
    except Exception: pass
    xml_slides.remove(sid)

def P(name): return os.path.join(IMG, name)


# =================================================================== helpers
def std(title, kicker=None, lede=None, source=None):
    s = prs.slides.add_slide(L_STD); set_title(s, title); blank_footer(s)
    if kicker:
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
    box(s, x, y, w, h, fill=fill, line=line, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
    if head:
        box(s, x + 0.20, y + 0.09, w - 0.40, 0.24, text=head.upper(), size=8.0,
            color=GREY_TX, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        return y + 0.38
    return y + 0.14


def cards(s, y, h, items, x=CX, w=CW, gap=0.16, hsize=12.5, bsize=9.4,
          dark=False, isz=0.42):
    """items: (glyph, heading, body, accent)."""
    n = len(items)
    cw = (w - gap * (n - 1)) / n
    for i, (g, head, body, acc) in enumerate(items):
        cx = x + i * (cw + gap)
        fill = NAVY if dark else WHITE
        box(s, cx, y, cw, h, fill=fill, line=None if dark else GREY_BD, line_w=1.0,
            shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
        box(s, cx, y, cw, 0.075, fill=acc, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
        icon(s, cx + 0.20, y + 0.24, isz, G(g), bg=acc)
        box(s, cx + 0.20, y + 0.24 + isz + 0.12, cw - 0.40, 0.30, text=head,
            size=hsize, color=WHITE if dark else NAVY, bold=True, ml=0)
        box(s, cx + 0.20, y + 0.24 + isz + 0.46, cw - 0.40, h - isz - 0.80,
            text=body, size=bsize, color=NAVY_TXT if dark else MUTE, ml=0)


def node(s, x, y, w, h, text, fill=WHITE, tcolor=NAVY, line=GREY_BD, size=8.4,
         bold=True, sub=None, ssize=6.8, radius=0.10):
    box(s, x, y, w, h, fill=fill, line=line, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)
    if sub:
        box(s, x + 0.04, y + 0.05, w - 0.08, h * 0.52, text=text, size=size,
            color=tcolor, bold=bold, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.BOTTOM, ml=0, mr=0, mb=0)
        box(s, x + 0.04, y + h * 0.52, w - 0.08, h * 0.46, text=sub, size=ssize,
            color=GREY_TX if fill == WHITE else NAVY_TXT, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.TOP, ml=0, mr=0, mt=0.02)
    else:
        box(s, x + 0.04, y, w - 0.08, h, text=text, size=size, color=tcolor,
            bold=bold, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
            ml=0, mr=0)


def hline(s, x, y, w, color=GREY_BD, t=0.014):
    box(s, x, y, w, t, fill=color)


def vline(s, x, y, h, color=GREY_BD, t=0.014):
    box(s, x, y, t, h, fill=color)


def harrow(s, x, y, w, color=PRIMARY, label=None, lsize=6.6, t=0.014):
    hline(s, x, y, w, color=color, t=t)
    box(s, x + w - 0.10, y - 0.09, 0.20, 0.20, text="▸", size=10, color=color,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False,
        ml=0, mr=0, mt=0, mb=0)
    if label:
        box(s, x, y - 0.26, w, 0.22, text=label, size=lsize, color=MUTE,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0, mr=0)


def tag(s, x, y, w, h, text, fill=GREY_BG, tcolor=NAVY, size=7.0, bold=False):
    return box(s, x, y, w, h, text=text, size=size, color=tcolor, bold=bold,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=fill,
               shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.20, ml=0.03, mr=0.03)


def step(s, x, y, w, h, num, head, body, accent=PRIMARY):
    box(s, x, y, w, h, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, y, w, 0.075, fill=accent, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    box(s, x + 0.20, y + 0.18, 0.44, 0.44, text=num, size=20, color=accent,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0, wrap=False)
    box(s, x + 0.20, y + 0.68, w - 0.40, 0.30, text=head, size=12, color=NAVY,
        bold=True, ml=0)
    box(s, x + 0.20, y + 1.00, w - 0.40, h - 1.10, text=body, size=9.4,
        color=MUTE, ml=0)


# =================================================================== 1. COVER
cover_slide(prs, "AgentZ: Security Hardened Sovereign\nAutonomous AI Agents",
            scope=[("0", "Secrets seen by agents"),
                   ("100%", "Actions audited"),
                   ("11x", "Lower token cost")])

# =================================================================== 2. DIVIDER
divider("Part 1", "The agent security gap",
        "Every enterprise will run AI agents. We make it safe to.")

# =================================================================== 3
s = std("AI agents arrive faster than the controls",
        "Market context",
        "Agents moved from chat to action in one product cycle.",
        source="Confidential. Limited distribution under NDA.")
cards(s, 1.52, 2.34, [
    ("chip", "Autonomous",
     "Agents act on their own. They call tools, move data, and run unattended.", PRIMARY),
    ("key", "Privileged",
     "Every useful agent needs API keys, cloud roles, and broad system access.", SECOND),
    ("warn", "Ungoverned",
     "Security teams have no standard way to sandbox, scope, or audit an agent.", RED),
], dark=True)
box(s, CX, 4.14, CW, 0.72,
    text="The market races to deploy agents. The winners are the teams that "
         "deploy them safely.",
    size=12.5, color=PRIMARY, bold=True, align=PP_ALIGN.CENTER, fill=GREY_BG,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 4
s = std("Teams want agents. Security cannot sign off.", "The standoff")
cy = panel(s, CX, 1.46, 4.52, 2.62, "What builders want")
icon(s, CX + 0.22, cy - 0.02, 0.44, G('bolt'), bg=PRIMARY)
bullets(s, CX + 0.24, cy + 0.62, 4.04, 1.50, [
    "Ship agents fast", "Use any model or framework",
    "Connect real tools and data", "Automate on a schedule"], size=11, color=NAVY)
cy = panel(s, 5.08, 1.46, 4.52, 2.62, "What security fears")
icon(s, 5.30, cy - 0.02, 0.44, G('block'), bg=RED)
bullets(s, 5.32, cy + 0.62, 4.04, 1.50, [
    "Leaked API keys and secrets", "Agents with too much access",
    "No visibility into actions", "No audit or compliance"],
    size=11, color=NAVY, mcolor=RED)
box(s, CX, 4.30, CW, 0.72,
    text="AgentZ closes the gap. Builders move fast and security stays in control.",
    size=12.5, color=PRIMARY, bold=True, align=PP_ALIGN.CENTER, fill=GREY_BG,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 5
s = std("An autonomous agent is a new attack surface", "The risk",
        "Four gaps show up in every unguarded agent deployment.")
FOUR = [("key", "Credentials in the clear",
         "Agents get raw API keys and tokens. The keys land in prompts, logs, "
         "and memory.", RED),
        ("warn", "Over-broad access",
         "Agents get far more reach than a task needs: full cloud roles and "
         "open egress.", SECOND),
        ("eye", "No runtime visibility",
         "Once the agent runs, nobody sees what it reads, writes, or sends.", PURPLE),
        ("flag", "No compliance story",
         "No tenancy isolation, no hardening baseline, no audit trail. "
         "Regulated buyers refuse it.", PRIMARY)]
for i, (g, head, body, acc) in enumerate(FOUR):
    x = CX + (i % 2) * 4.68
    y = 1.50 + (i // 2) * 1.60
    box(s, x, y, 4.52, 1.44, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, y, 0.075, 1.44, fill=acc)
    icon(s, x + 0.22, y + 0.24, 0.46, G(g), bg=acc)
    box(s, x + 0.84, y + 0.20, 3.50, 0.32, text=head, size=12.5, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.84, y + 0.56, 3.50, 0.78, text=body, size=9.6, color=MUTE, ml=0)

# =================================================================== 6. DIVIDER
divider("Part 2", "AgentZ, the secure agent runtime",
        "A hardened place to run agents, with the guardrails already wired in.")

# =================================================================== 7
s = std("Solution: a secure agents runtime", "The platform",
        "Four properties separate AgentZ from a bare agent framework.")
FOUR = [("lock", "Credential-less by design",
         "Agents never see secrets. A proxy injects tokens into outbound "
         "requests from the vault.", PRIMARY),
        ("shield", "Every action enforced",
         "File, process, network, and domain activity is watched and "
         "restricted at runtime.", GREEN),
        ("chip", "Scoped environments",
         "Each agent runs in a hardened environment that names its packages, "
         "domains, tools, and skills.", SECOND),
        ("star", "Marketplace ready",
         "Agents and workflows are reusable, scheduled, and shareable, with "
         "no provider lock-in.", PURPLE)]
for i, (g, head, body, acc) in enumerate(FOUR):
    x = CX + (i % 2) * 4.68
    y = 1.50 + (i // 2) * 1.60
    box(s, x, y, 4.52, 1.44, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, y, 0.075, 1.44, fill=acc)
    icon(s, x + 0.22, y + 0.24, 0.46, G(g), bg=acc)
    box(s, x + 0.84, y + 0.20, 3.50, 0.32, text=head, size=12.5, color=WHITE,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.84, y + 0.56, 3.50, 0.78, text=body, size=9.6, color=NAVY_TXT, ml=0)

# =================================================================== 8
s = std("How it works", "Four moves",
        "From an empty environment to a scheduled, audited agent fleet.")
W = (CW - 3 * 0.16) / 4
for i, (num, head, body) in enumerate([
        ("1", "Define environment",
         "Set the packages, allowed domains, MCP tools, and skills an agent may use."),
        ("2", "Bind secrets",
         "Map credentials to a secrets manager. Agents reference keys and never hold them."),
        ("3", "Deploy hardened",
         "Run on CIS and STIG hardened compute, with enforcement on every action."),
        ("4", "Schedule and scale",
         "Trigger workflows on a schedule. Reuse them and publish to the marketplace.")]):
    step(s, CX + i * (W + 0.16), 1.52, W, 2.90, num, head, body,
         accent=[PRIMARY, SECOND, GREEN, PURPLE][i])
box(s, CX, 4.60, CW, 0.34,
    text="The same four moves cover one pilot agent and a fleet of fifty.",
    size=11, color=PRIMARY, bold=True, italic=True, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 9
s = std("Built on security DNA competitors cannot bolt on", "Why AccuKnox")
FOUR = [("shield", "Zero Trust CNAPP heritage",
         "AccuKnox secures cloud, containers, APIs, and AI today. Agent "
         "security extends that work.", PRIMARY),
        ("bolt", "KubeArmor eBPF enforcement",
         "Open source inline enforcement at the kernel gives per-action "
         "control, already battle tested.", GREEN),
        ("chip", "ClawArmor and AI Security 2.0",
         "Identity-first Zero Trust products for AI models, agents, and MCP "
         "already ship today.", SECOND),
        ("globe", "Model agnostic",
         "AgentZ is not tied to one LLM provider. Closed platforms secure only "
         "themselves.", PURPLE)]
for i, (g, head, body, acc) in enumerate(FOUR):
    x = CX + (i % 2) * 4.68
    y = 1.30 + (i // 2) * 1.72
    box(s, x, y, 4.52, 1.54, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, y, 0.075, 1.54, fill=acc)
    icon(s, x + 0.22, y + 0.28, 0.46, G(g), bg=acc)
    box(s, x + 0.84, y + 0.22, 3.50, 0.34, text=head, size=12.5, color=WHITE,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.84, y + 0.60, 3.50, 0.84, text=body, size=9.6, color=NAVY_TXT, ml=0)

# =================================================================== 10
s = std("Where AgentZ sits in the AccuKnox AI platform", "Platform map",
        "AgentZ is the runtime layer under the AI operator column.",
        source="Source: accuknox.com agentic AI security platform")
image_fit(s, P("Agentic-AI-Security-Platform.png"), CX, 1.42, CW, 3.62, frame=None)

# =================================================================== 11
s = std("Architecture principles", "Relationships",
        "Users, agents, sandboxes and allow lists, and how many of each.")
node(s, 0.44, 2.30, 0.98, 0.62, "Users", fill=NAVY, tcolor=WHITE, size=9)
harrow(s, 1.46, 2.60, 0.60, label="1:N")
node(s, 2.10, 2.30, 1.20, 0.62, "AI agents", fill=PRIMARY, tcolor=WHITE, size=9)
harrow(s, 3.34, 2.60, 0.62, label="M:N")
node(s, 4.00, 2.30, 1.20, 0.62, "Sandbox", fill=NAVY, tcolor=WHITE, size=9)
vline(s, 2.66, 2.94, 0.42, color=GREY_BD)
box(s, 2.70, 2.98, 0.40, 0.22, text="1:N", size=6.6, color=MUTE, ml=0, mr=0)
for i in range(3):
    node(s, 2.02 + i * 0.06, 3.34 + i * 0.06, 1.20, 0.42, "Workflows",
         fill=GREY_BG, tcolor=NAVY, size=8, line=GREY_BD)
vline(s, 2.70, 1.62, 0.70, color=GREY_BD)
hline(s, 2.70, 1.62, 0.68, color=GREY_BD)
box(s, 2.76, 1.34, 0.44, 0.22, text="1:1", size=6.6, color=MUTE, ml=0, mr=0)
node(s, 3.36, 1.34, 1.42, 0.56, "Credentials proxy", fill=SECOND, tcolor=WHITE, size=8.4)
LISTS = [("Credentials list", 1.06,
          "ANTHROPIC_KEY  =>  *.anthropic.com\nGOOGLE_TOKEN  =>  *.google.com\n"
          "API_ACCESS_KEY  =>  *.acmeapi.com", PRIMARY),
         ("Domain list", 2.02,
          "*.anthropic.com     *.google.com\n*.acmeapi.com     *.accuknox.com", GREEN),
         ("MCP list", 2.98,
          "AccuKnox MCP  =>  mcp.accuknox.com\nAtlassian  =>  mcp.atlassian.com", SECOND),
         ("Package list", 3.94,
          "libcurl     libapr     libregex     nmap", PURPLE)]
for name, y, detail, acc in LISTS:
    node(s, 5.44, y, 1.34, 0.48, name, fill=WHITE, tcolor=acc, size=8, line=acc)
    harrow(s, 6.82, y + 0.24, 0.36, color=acc)
    box(s, 7.24, y - 0.02, 2.36, 0.54, text=detail, size=6.6, color=NAVY,
        fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08,
        anchor=MSO_ANCHOR.MIDDLE, font=MONO)
    hline(s, 5.24, y + 0.24, 0.20, color=GREY_BD)
vline(s, 5.24, 1.30, 2.88, color=GREY_BD)
hline(s, 5.20, 2.60, 0.08, color=GREY_BD)

# =================================================================== 12
s = std("Systems architecture", "Deployment view",
        "One Kubernetes cluster holds the runtime, the proxy and the vault.")
box(s, 2.10, 1.34, 5.44, 3.10, fill=None, line=PRIMARY, line_w=1.25,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.03)
box(s, 2.22, 1.38, 1.70, 0.24, text="KUBERNETES CLUSTER", size=7.2, color=PRIMARY,
    bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
node(s, 0.44, 1.42, 1.30, 0.52, "User browser", fill=GREY_BG, size=8)
node(s, 0.44, 2.28, 1.30, 0.62, "Integrations", sub="Slack, Telegram, Discord",
     fill=GREY_BG, size=8)
node(s, 0.44, 3.24, 1.30, 0.52, "OpenCode client", fill=GREY_BG, size=8)
for y in (1.68, 2.59, 3.50):
    harrow(s, 1.78, y, 0.28)
node(s, 2.26, 1.70, 1.44, 0.52, "Web management", fill=NAVY, tcolor=WHITE, size=8)
node(s, 2.26, 2.44, 1.44, 0.62, "Agents runtime", sub="OpenCode server",
     fill=PRIMARY, tcolor=WHITE, size=8.4)
node(s, 2.26, 3.28, 1.44, 0.56, "K8s CronJob", sub="Agent workflow",
     fill=GREY_BG, size=8)
node(s, 4.00, 2.44, 1.42, 0.62, "Credentials proxy", fill=SECOND, tcolor=WHITE, size=8.4)
node(s, 4.00, 1.62, 1.42, 0.62, "Secrets manager", sub="OpenBao or AccuKnox",
     fill=WHITE, size=8, line=SECOND)
node(s, 5.72, 2.44, 1.42, 0.62, "Agent gateway", fill=NAVY, tcolor=WHITE, size=8.4)
harrow(s, 3.74, 2.74, 0.22)
harrow(s, 5.46, 2.74, 0.22)
vline(s, 4.70, 2.26, 0.18, color=GREY_BD)
vline(s, 2.98, 2.24, 0.20, color=GREY_BD)
vline(s, 2.98, 3.08, 0.20, color=GREY_BD)
node(s, 7.90, 1.62, 1.70, 0.52, "LLM providers", fill=GREY_BG, size=8)
node(s, 7.90, 2.48, 1.70, 0.52, "MCP providers", fill=GREY_BG, size=8)
node(s, 7.90, 3.34, 1.70, 0.52, "Internet", fill=GREY_BG, size=8)
for y in (1.88, 2.74, 3.60):
    harrow(s, 7.20, y, 0.62)
SEC = [("API security", "AccuKnox", PRIMARY), ("Network", "Cilium", GREEN),
       ("Sandboxing", "KubeArmor", RED)]
for i, (n, sub, acc) in enumerate(SEC):
    node(s, 2.26 + i * 1.78, 3.98, 1.62, 0.42, n + "  |  " + sub, fill=WHITE,
         tcolor=acc, size=7.4, line=acc)
box(s, CX, 4.60, CW, 0.30,
    text="Security controls sit inside the cluster, so no agent traffic leaves "
         "without a policy decision.",
    size=9.4, color=MUTE, italic=True, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 13
s = std("Secure credentials handling", "Credential broker",
        "Never expose a real credential to an agent.")
box(s, CX, 1.44, 4.44, 0.62, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, 0.54, 1.48, 4.20, 0.24, text="PLACEHOLDER KEYS THE AGENT SEES", size=7,
    color=GREY_TX, bold=True, ml=0)
box(s, 0.54, 1.70, 4.20, 0.32,
    text="ANTHROPIC_KEY => CLAWARMOR_ANTHROPIC_KEY\n"
         "GITHUB_MCP_KEY => CLAWARMOR_GITHUB_MCP_KEY",
    size=6.8, color=NAVY, font=MONO, ml=0)
box(s, 5.16, 1.44, 4.44, 0.62, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, 5.30, 1.48, 4.20, 0.24, text="VAULT MAPPING THE PROXY HOLDS", size=7,
    color=PURPLE, bold=True, ml=0)
box(s, 5.30, 1.70, 4.20, 0.32,
    text="CLAWARMOR_ANTHROPIC_KEY => /agent/anthropic_key  [*.anthropic.com]\n"
         "CLAWARMOR_GITHUB_MCP_KEY => /agent/github_key  [*.github.com]",
    size=6.4, color=NAVY, font=MONO, ml=0)
node(s, 0.86, 2.44, 1.42, 0.60, "Agent workflow", fill=PRIMARY, tcolor=WHITE, size=8.4)
node(s, 3.30, 2.44, 1.42, 0.60, "Credentials proxy", fill=SECOND, tcolor=WHITE, size=8.4)
node(s, 3.30, 3.94, 1.42, 0.56, "Secrets manager", fill=WHITE, size=8.4, line=SECOND)
node(s, 6.06, 2.44, 1.42, 0.60, "GitHub MCP server", fill=NAVY, tcolor=WHITE, size=8.4)
harrow(s, 2.32, 2.74, 0.94)
harrow(s, 4.76, 2.74, 1.26)
vline(s, 4.01, 3.06, 0.86, color=GREY_BD)
box(s, 0.44, 3.24, 2.62, 0.94, fill=NAVY_DK, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, 0.56, 3.28, 2.40, 0.22, text="STEP 1  REQUEST LEAVES THE AGENT", size=6.6,
    color=SECOND, bold=True, ml=0)
box(s, 0.56, 3.48, 2.40, 0.66,
    text="GET /api/v1/resource HTTP/1.1\nHost: mcp.github.com\n"
         "Authorization: Bearer CLAWARMOR_GITHUB_MCP_KEY",
    size=6.0, color=NAVY_TXT, font=MONO, ml=0)
box(s, 5.02, 3.24, 4.58, 0.44, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, 5.14, 3.26, 4.34, 0.40,
    text="STEP 2   Check domain access for the placeholder key in the request.",
    size=8, color=NAVY, anchor=MSO_ANCHOR.MIDDLE, ml=0)
box(s, 5.02, 3.76, 4.58, 0.44, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, 5.14, 3.78, 4.34, 0.40,
    text="STEP 3   Map the placeholder to the real key held in the vault.",
    size=8, color=NAVY, anchor=MSO_ANCHOR.MIDDLE, ml=0)
box(s, 5.02, 4.28, 4.58, 0.86, fill=NAVY_DK, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, 5.14, 4.32, 4.34, 0.22, text="STEP 4  PROXY SWAPS IN THE REAL KEY", size=6.6,
    color=SECOND, bold=True, ml=0)
box(s, 5.14, 4.52, 4.34, 0.58,
    text="GET /api/v1/resource HTTP/1.1\nHost: mcp.github.com\n"
         "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9",
    size=6.0, color=NAVY_TXT, font=MONO, ml=0)

# =================================================================== 14
s = std("The environment sets an agent's blast radius", "Policy object",
        "Every agent binds to exactly one environment. The environment decides "
        "what it can reach.")
cards(s, 1.54, 2.34, [
    ("code", "Packages",
     "Runtime libraries and dependencies available for agentic execution.", PRIMARY),
    ("globe", "External domains",
     "Allow-listed egress. These are the only destinations the agent may reach.", GREEN),
    ("link", "MCP tools",
     "The specific Model Context Protocol tools the agent may call.", SECOND),
    ("list", "Skills",
     "The curated skills and capabilities the agent can invoke at runtime.", PURPLE),
])
box(s, CX, 4.16, CW, 0.72,
    text="Change the environment and you change the blast radius. No code edit "
         "is needed.",
    size=12.5, color=PRIMARY, bold=True, align=PP_ALIGN.CENTER, fill=GREY_BG,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 15
s = std("Every action is audited at runtime", "Runtime enforcement",
        "KubeArmor watches four planes and blocks anything outside the policy.")
cards(s, 1.54, 2.34, [
    ("wrench", "Tool calls",
     "Every tool access and response is audited, with the parameters it "
     "carries.", PRIMARY),
    ("terminal", "System calls",
     "Every file, process, and sensitive data access is audited.", GREEN),
    ("net", "Networks",
     "Egress is limited to allow-listed endpoints and ports.", SECOND),
    ("globe", "Domains",
     "DNS and domain access is matched against the environment list.", PURPLE),
])
box(s, CX, 4.16, CW, 0.72,
    text="Audit is the default state. You do not switch it on later.",
    size=12.5, color=PRIMARY, bold=True, align=PP_ALIGN.CENTER, fill=GREY_BG,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 16
s = std("Sandboxing and inventory in the product", "Product view",
        "Zero trust policy per agent workload, plus a live agent inventory.",
        source="Source: AccuKnox AI Security console")
box(s, CX, 1.44, 4.52, 0.28, text="RUNTIME AGENT SANDBOXING", size=8,
    color=GREY_TX, bold=True, ml=0)
image_fit(s, P("Ai-sec-Runtime-Agent-Sandboxing.png"), CX, 1.74, 4.52, 3.10)
box(s, 5.08, 1.44, 4.52, 0.28, text="MANAGED AGENT INVENTORY", size=8,
    color=GREY_TX, bold=True, ml=0)
image_fit(s, P("Ai-sec-Managed-Agents-View.png"), 5.08, 1.74, 4.52, 3.10)

# =================================================================== 17
s = std("Scheduled and event driven workflows", "Unattended runs",
        "Agent workflows run without a human present, on the same policy.")
box(s, CX, 1.46, CW, 0.52,
    text="Each invocation inherits the same environment scope, the same proxy "
         "broker, and the same enforcement.",
    size=10.6, color=NAVY, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
    radius=0.05, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
CH = [("clock", "Trigger", "A cron schedule, a webhook, or an event fires the workflow.", PRIMARY),
      ("chip", "Scoped run", "The agent executes inside its hardened environment.", SECOND),
      ("books", "Audit and result", "Actions are logged, outputs delivered, secrets never exposed.", GREEN)]
cw = (CW - 2 * 0.52) / 3
for i, (g, head, body, acc) in enumerate(CH):
    x = CX + i * (cw + 0.52)
    box(s, x, 2.20, cw, 1.60, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    icon(s, x + 0.22, 2.42, 0.46, G(g), bg=acc)
    box(s, x + 0.84, 2.40, cw - 1.04, 0.32, text=head, size=12.5, color=WHITE,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.24, 3.00, cw - 0.48, 0.68, text=body, size=9.6, color=NAVY_TXT, ml=0)
    if i < 2:
        arrow(s, x + cw + 0.13, 2.86, 0.26, 0.26, color=PRIMARY, size=15)
box(s, CX, 4.02, CW, 0.52,
    text="Concurrency, retries, and resource quotas are governed centrally. "
         "Agents scale without widening the trust boundary.",
    size=10.6, color=NAVY, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
    radius=0.05, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

# =================================================================== 18
s = std("Token optimization for deterministic steps", "Cost control",
        "Deterministic work moves out of the model and into plain code.")
box(s, CX, 1.40, CW, 0.24, text="BEFORE OPTIMIZATION", size=8, color=RED,
    bold=True, ml=0)
image_fit(s, P("trace-before.png"), CX, 1.62, CW, 0.62, frame=GREY_BD)
box(s, CX, 2.30, CW, 0.24, text="AFTER OPTIMIZATION", size=8, color=GREEN_DK,
    bold=True, ml=0)
image_fit(s, P("trace-after.png"), CX, 2.52, CW, 0.62, frame=GREY_BD)
table(s, CX, 3.28, CW, 1.06, [
    ["", "Input tokens", "Input cost", "Output tokens", "Output cost"],
    ["Before optimization", "90.2K", "20 cents", "10K", "25 cents"],
    ["After optimization", "8K", "4 cents", "1K", "2.5 cents"]],
    colw=[2.60, 1.65, 1.65, 1.65, 1.65], hsize=8.6, bsize=9.4)
for i, (num, lab, acc) in enumerate([("11x", "Fewer input tokens", GREEN),
                                     ("10x", "Fewer output tokens", GREEN),
                                     ("83%", "Lower run cost", PRIMARY)]):
    stat(s, CX + i * 3.12, 4.46, 2.96, num, lab, color=acc, nsize=19, h=0.74,
         lsize=8.6)
footer_note(s, "Costs are for one workflow run, measured on the same trace.",
            y=5.26, size=7.6)

# =================================================================== 19. DIVIDER
divider("Part 3", "AgentZ inside the enterprise",
        "How AgentZ plugs into AccuKnox CNAPP, MCP and the security workflow.")

# =================================================================== 20
s = std("AccuKnox agentic AI integration", "Enterprise fit",
        "Twelve purpose-built agents, one MCP server, one control plane.")
box(s, CX, 1.44, 3.30, 2.76, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
box(s, CX + 0.16, 1.52, 3.00, 0.28, text="ACCUKNOX AGENTZ", size=9, color=SECOND,
    bold=True, ml=0)
AGENTS = ["SRE Agent", "AI SOC Agent", "ASPM Agent", "Custom Reporting",
          "Toxic Combinations", "CloudSecOps Agent", "Security Advisory",
          "Virtual Patch Agent", "Cloud CTEM Agent", "Policy Recommendation",
          "FedRAMP Compliance", "Blast Radius"]
for i, a in enumerate(AGENTS):
    x = CX + 0.16 + (i % 2) * 1.54
    y = 1.80 + (i // 2) * 0.38
    tag(s, x, y, 1.44, 0.32, a, fill=NAVY_DK, tcolor=WHITE, size=7.2)
node(s, 4.14, 2.10, 1.34, 0.66, "AccuKnox MCP", sub="Assets, findings, email",
     fill=SECOND, tcolor=WHITE, size=8.4)
harrow(s, 3.74, 2.42, 0.34, label="skills")
harrow(s, 5.52, 2.42, 0.34)
node(s, 5.90, 1.44, 3.70, 0.86, "AccuKnox enterprise CNAPP control plane",
     sub="US production environment", fill=PRIMARY, tcolor=WHITE, size=9)
node(s, 5.90, 2.38, 3.70, 0.44, "India production environment", fill=GREY_BG, size=8)
node(s, 5.90, 2.94, 1.74, 0.52, "AccuKnox SIEM", fill=NAVY, tcolor=WHITE, size=8)
node(s, 7.86, 2.94, 1.74, 0.52, "Webhooks: IoCs", fill=WHITE, size=8, line=PRIMARY)
box(s, CX, 4.42, CW, 0.26, text="SHARED SERVICES", size=8, color=GREY_TX,
    bold=True, ml=0)
node(s, 0.44, 4.70, 2.20, 0.52, "Workflows in Git repos", fill=WHITE, size=8, line=GREY_BD)
node(s, 2.90, 4.70, 2.20, 0.52, "Secrets manager", fill=WHITE, size=8, line=SECOND)
node(s, 5.36, 4.70, 2.20, 0.52, "Triggers and schedules", fill=WHITE, size=8, line=GREEN)
node(s, 7.82, 4.70, 1.78, 0.52, "Slack and email", fill=WHITE, size=8, line=PURPLE)

# =================================================================== 21
s = std("Sample environment", "One agent, one scope",
        "What a single AgentZ environment allows, tool by tool.")
node(s, 0.60, 1.62, 2.40, 0.90, "AccuKnox AgentZ", sub="One hardened environment",
     fill=PRIMARY, tcolor=WHITE, size=11)
harrow(s, 3.06, 2.07, 0.62)
box(s, 0.60, 2.72, 2.40, 0.26, text="ENVIRONMENT SCOPE", size=7.6, color=GREY_TX,
    bold=True, ml=0)
for i, (k, v) in enumerate([("Packages", "python3.12, curl, jq"),
                            ("Domains", "6 allow-listed hosts"),
                            ("Skills", "triage, enrich, report"),
                            ("Identity", "one SPIFFE ID")]):
    y = 3.00 + i * 0.44
    box(s, 0.60, y, 2.40, 0.40, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
        radius=0.10)
    box(s, 0.70, y, 0.86, 0.40, text=k, size=7.6, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, 1.56, y, 1.36, 0.40, text=v, size=7.2, color=MUTE,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
box(s, 3.82, 1.42, 2.60, 3.42, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
box(s, 3.94, 1.50, 2.36, 0.26, text="ALLOWED TOOLS", size=8, color=GREY_TX,
    bold=True, ml=0)
for i, t_ in enumerate(["Gmail", "Slack", "AccuKnox MCP", "MISP MCP",
                        "AlienVault MCP"]):
    node(s, 3.98, 1.84 + i * 0.58, 2.28, 0.46, t_, fill=WHITE, size=8.6, line=GREY_BD)
box(s, 6.86, 1.42, 2.74, 1.60, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
box(s, 6.98, 1.50, 2.50, 0.26, text="LLM PROVIDERS", size=8, color=GREY_TX,
    bold=True, ml=0)
for i, t_ in enumerate(["OpenAI", "OpenRouter", "Anthropic"]):
    node(s, 7.02, 1.82 + i * 0.38, 2.42, 0.32, t_, fill=WHITE, size=8, line=GREY_BD)
node(s, 6.86, 3.24, 2.74, 0.60, "AccuKnox CNAPP", sub="Reached through AccuKnox MCP",
     fill=NAVY, tcolor=WHITE, size=9)
harrow(s, 6.50, 2.20, 0.30)
harrow(s, 6.50, 3.54, 0.30)
box(s, CX, 4.98, CW, 0.32,
    text="Anything outside this list is denied at the kernel and written to the "
         "audit log.",
    size=10, color=MUTE, italic=True, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 22
s = std("Use case: finding enrichment on a webhook", "Event driven",
        "A new CSPM finding enriches itself before an analyst opens it.")
box(s, 2.36, 1.42, 2.90, 1.94, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
box(s, 2.48, 1.50, 2.66, 0.26, text="ACCUKNOX CNAPP", size=8, color=SECOND,
    bold=True, ml=0)
node(s, 2.52, 1.82, 1.24, 0.42, "Scanner", fill=NAVY_DK, tcolor=WHITE, size=8)
node(s, 3.90, 1.82, 1.24, 0.42, "Findings", fill=NAVY_DK, tcolor=WHITE, size=8)
node(s, 2.52, 2.52, 2.62, 0.42, "Rule engine", fill=NAVY_DK, tcolor=WHITE, size=8)
node(s, 0.44, 1.82, 1.30, 0.62, "AWS", sub="Cloud accounts", fill=GREY_BG, size=8.6)
harrow(s, 1.80, 2.10, 0.50, label="CSPM scan")
node(s, 6.10, 1.42, 3.50, 1.10, "AccuKnox MCP", sub="Tool: update_finding",
     fill=SECOND, tcolor=WHITE, size=10)
node(s, 6.10, 3.34, 3.50, 1.10, "AccuKnox AgentZ",
     sub="Finding enrichment workflow", fill=PRIMARY, tcolor=WHITE, size=10)
vline(s, 3.81, 3.36, 0.52, color=PRIMARY)
harrow(s, 3.81, 3.88, 2.29, label="1. Webhook fires the workflow")
vline(s, 7.85, 2.52, 0.82, color=GREY_BD)
box(s, 7.95, 2.66, 1.70, 0.54, text="2. Tool call writes\nthe enrichment back",
    size=7.6, color=MUTE, ml=0)
box(s, 0.44, 4.42, 5.30, 0.86, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
    radius=0.05)
box(s, 0.60, 4.46, 5.00, 0.24, text="WHAT THE WORKFLOW DOES", size=7.6,
    color=GREY_TX, bold=True, ml=0)
box(s, 0.60, 4.68, 5.00, 0.56,
    text="Read the finding, ask threat intel for context, and write the "
         "enriched result back through MCP.",
    size=9, color=NAVY, ml=0)
box(s, 6.10, 4.60, 3.50, 0.60,
    text="Every tool call lands in the audit trail.",
    size=9.4, color=MUTE, italic=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)

# =================================================================== 23
s = std("Use case: finding enrichment on a schedule", "Scheduled run",
        "The same workflow, pulled on a cron instead of pushed by a webhook.")
box(s, 2.36, 1.42, 2.90, 1.94, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
box(s, 2.48, 1.50, 2.66, 0.26, text="ACCUKNOX CNAPP", size=8, color=SECOND,
    bold=True, ml=0)
node(s, 2.52, 1.82, 1.24, 0.42, "Scanner", fill=NAVY_DK, tcolor=WHITE, size=8)
node(s, 3.90, 1.82, 1.24, 0.42, "Findings", fill=NAVY_DK, tcolor=WHITE, size=8)
node(s, 2.52, 2.52, 2.62, 0.42, "Finding store", fill=NAVY_DK, tcolor=WHITE, size=8)
node(s, 0.44, 1.82, 1.30, 0.62, "AWS", sub="Cloud accounts", fill=GREY_BG, size=8.6)
harrow(s, 1.80, 2.10, 0.50, label="CSPM scan")
box(s, 6.10, 1.42, 3.50, 1.44, fill=SECOND, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, 6.22, 1.50, 3.26, 0.28, text="ACCUKNOX MCP", size=9, color=WHITE, bold=True, ml=0)
node(s, 6.24, 1.84, 3.22, 0.42, "Tool: get_finding", fill=WHITE, tcolor=SECOND, size=8.4)
node(s, 6.24, 2.34, 3.22, 0.42, "Tool: update_finding", fill=WHITE, tcolor=SECOND, size=8.4)
node(s, 6.10, 3.62, 3.50, 1.10, "AccuKnox AgentZ",
     sub="Cron: every 15 minutes", fill=PRIMARY, tcolor=WHITE, size=10)
vline(s, 7.20, 2.92, 0.70, color=GREY_BD)
vline(s, 8.50, 2.92, 0.70, color=GREY_BD)
box(s, 5.30, 3.02, 1.86, 0.28, text="Get findings", size=7.6, color=MUTE,
    align=PP_ALIGN.RIGHT, ml=0)
box(s, 8.58, 3.02, 1.02, 0.28, text="Write back", size=7.6, color=MUTE, ml=0)
box(s, CX, 4.94, CW, 0.32,
    text="Use the schedule when the source system cannot send a webhook.",
    size=10, color=MUTE, italic=True, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 24
s = std("Use case: automated alert investigation", "AI SOC",
        "A KubeArmor policy violation becomes a written investigation report.")
node(s, 0.44, 1.60, 1.44, 0.90, "Kubernetes cluster", sub="KubeArmor",
     fill=GREY_BG, size=8.4)
box(s, 2.30, 1.44, 2.60, 1.30, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
box(s, 2.42, 1.52, 2.36, 0.26, text="ACCUKNOX CNAPP", size=8, color=SECOND,
    bold=True, ml=0)
node(s, 2.44, 1.84, 1.16, 0.42, "CWPP", fill=NAVY_DK, tcolor=WHITE, size=8)
node(s, 3.66, 1.84, 1.10, 0.42, "Triggers", fill=NAVY_DK, tcolor=WHITE, size=8)
harrow(s, 1.94, 2.04, 0.30, label="Alert")
node(s, 3.20, 3.36, 3.30, 1.10, "AccuKnox AgentZ",
     sub="KubeArmor alert investigation workflow", fill=PRIMARY, tcolor=WHITE, size=10)
vline(s, 4.20, 2.74, 0.62, color=PRIMARY)
box(s, 4.32, 2.86, 2.10, 0.34, text="1. Webhook triggers the workflow", size=7.6,
    color=MUTE, anchor=MSO_ANCHOR.MIDDLE, ml=0)
node(s, 7.10, 1.60, 1.20, 0.50, "Gmail", fill=WHITE, size=8.4, line=GREY_BD)
node(s, 8.40, 1.60, 1.20, 0.50, "Slack", fill=WHITE, size=8.4, line=GREY_BD)
node(s, 7.10, 3.36, 2.50, 1.10, "Threat intel", sub="MISP and AlienVault",
     fill=NAVY, tcolor=WHITE, size=9)
harrow(s, 6.56, 3.90, 0.48)
vline(s, 7.70, 2.12, 1.22, color=GREY_BD)
vline(s, 9.00, 2.12, 1.22, color=GREY_BD)
box(s, 6.62, 2.66, 2.98, 0.34, text="2. Send the investigation report", size=7.6,
    color=MUTE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0)
box(s, 0.44, 3.36, 2.34, 1.10, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
    radius=0.05)
box(s, 0.58, 3.42, 2.06, 0.24, text="THE AGENT DOES", size=7.6, color=GREY_TX,
    bold=True, ml=0)
box(s, 0.58, 3.64, 2.06, 0.76,
    text="Pull the alert, check the process tree, and score the threat.",
    size=8.6, color=NAVY, ml=0)
box(s, CX, 4.66, CW, 0.34,
    text="The analyst reads a finished report instead of a raw alert.",
    size=10, color=MUTE, italic=True, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 25
s = std("AgentZ workflow builder", "Product view",
        "The alert investigation workflow as it runs in the console.",
        source="Source: AccuKnox AgentZ console")
image_fit(s, P("agentz-workflow-graph.png"), CX, 1.42, CW, 3.62)

# =================================================================== 26
s = std("Governance the auditor can read", "Product view",
        "Policy violations, severity and owner attribution per application.",
        source="Source: AccuKnox AI Security console")
image_fit(s, P("agentic-ai-dashboard.png"), 1.60, 1.42, 6.80, 3.62)

# =================================================================== 27
s = std("What teams automate with AgentZ", "Use cases")
USE = [("gear", "IT and DevOps",
        "Triage alerts, run remediations, and automate routine ops on a schedule.", PRIMARY),
       ("shield", "Security operations",
        "Enrich incidents and run guarded response workflows over real tools.", GREEN),
       ("chart", "Data and reporting",
        "Pull, summarize, and distribute recurring reports across systems.", SECOND),
       ("people", "Customer ops",
        "Resolve tickets and update records with auditable, scoped access.", PURPLE),
       ("briefcase", "Back office",
        "Automate finance, HR, and procurement tasks under tight controls.", NAVY),
       ("bulb", "Custom workflows",
        "Compose your own agents from marketplace building blocks.", PRIMARY)]
for i, (g, head, body, acc) in enumerate(USE):
    x = CX + (i % 3) * 3.12
    y = 1.20 + (i // 3) * 1.92
    box(s, x, y, 2.96, 1.72, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, y, 2.96, 0.075, fill=acc, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    icon(s, x + 0.18, y + 0.24, 0.42, G(g), bg=acc)
    box(s, x + 0.68, y + 0.22, 2.10, 0.44, text=head, size=11.5, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.18, y + 0.78, 2.60, 0.84, text=body, size=9.4, color=MUTE, ml=0)

# =================================================================== 28
s = std("Differentiation", "Comparison",
        "Where AgentZ holds ground that agent frameworks do not.")
ROWS = [("Cloud or SaaS offering", 1, 1, 1, 1),
        ("On-premise deployment", 1, 1, 0, 0),
        ("Deterministic code cuts token cost", 1, 1, 0, 0),
        ("Workflows triggered by webhooks", 1, 0, 0, 0),
        ("Security hardening out of the box", 1, 0, 1, 1),
        ("Agents never see credentials", 1, 0, 0, 0),
        ("Every tool and network call visible", 1, 0, 0, 0),
        ("Built-in memory", 1, 1, 1, 1),
        ("Workflow marketplace", 1, 0, 0, 0),
        ("Cost management", 1, 0, 1, 0)]
COLS = ["AccuKnox AgentZ", "Nous Hermes", "Kindo.AI", "OpenAI ONA"]
gx, gy, gw = CX, 1.38, CW
fw = 3.56
cwd = (gw - fw) / 4
box(s, gx, gy, gw, 0.36, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
box(s, gx + 0.12, gy, fw - 0.12, 0.36, text="CAPABILITY", size=8, color=WHITE,
    bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
for i, c in enumerate(COLS):
    box(s, gx + fw + i * cwd, gy, cwd, 0.36, text=c, size=8,
        color=SECOND if i == 0 else WHITE, bold=True, align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
for r, row in enumerate(ROWS):
    y = gy + 0.40 + r * 0.33
    if r % 2 == 0:
        box(s, gx, y, gw, 0.32, fill=GREY_BG)
    box(s, gx + 0.12, y, fw - 0.12, 0.32, text=row[0], size=8.4, color=NAVY,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
    for i in range(4):
        yes = row[i + 1] == 1
        cx = gx + fw + i * cwd
        if i == 0:
            box(s, cx, y, cwd, 0.32, fill=GREEN_LT)
        box(s, cx, y, cwd, 0.32, text="Yes" if yes else "No", size=8.4,
            color=GREEN_DK if yes else GREY_TX, bold=yes, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)
footer_note(s, "Competitor rows reflect the publicly documented feature set at "
               "the time of writing.", y=5.16, size=7.6)

# =================================================================== 29. CLOSING
closing_slide(prs)

prs.save(OUT)
print("saved:", os.path.abspath(OUT), "slides:", len(prs.slides._sldIdLst))
