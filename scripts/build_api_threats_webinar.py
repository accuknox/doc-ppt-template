# -*- coding: utf-8 -*-
"""
Stop API Threats in Nginx & Kubernetes with AccuKnox.

Rebuilds the source webinar deck ("_Stop API Threats Webinar.pptx", a Google Slides
export) on the AccuKnox master template. Every data point from the source deck is
kept. Added on top: industry statistics with citations, the OWASP API Security
Top 10 (2023), published breach examples, MITRE ATT&CK for Containers mapping,
KubeArmor project facts, product screenshots, and a sources slide.

The "CLASSIFICATION: CONFIDENTIAL" footers from the source deck are dropped.

Build:   py -3.11 scripts/build_api_threats_webinar.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_Stop_API_Threats_Webinar.pptx -Out output/render/api-threats
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
AST  = os.path.join(HERE, "..", "output", "assets")
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_Stop_API_Threats_Webinar.pptx")

def A(name):  return os.path.join(AST, name)
def W(name):  return os.path.join(AST, "apiwebinar", name)
def P(name):  return os.path.join(AST, "apisec", name)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_COVER, L_DIV, L_STD = prs.slide_layouts[0], prs.slide_layouts[2], prs.slide_layouts[4]
xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try: prs.part.drop_rel(sid.get(qn('r:id')))
    except Exception: pass
    xml_slides.remove(sid)


def content(title, kicker=None):
    s = prs.slides.add_slide(L_STD); set_title(s, title); blank_footer(s)
    if kicker: eyebrow(s, kicker)
    return s


def divider(part, title, sub):
    s = prs.slides.add_slide(L_DIV); blank_footer(s)
    box(s, 0.86, 1.62, 8.3, 0.32, text=part.upper(), size=13, color=SECOND, bold=True)
    box(s, 0.82, 1.98, 8.4, 1.1, text=title, size=30, color=WHITE, bold=True,
        anchor=MSO_ANCHOR.TOP)
    box(s, 0.86, 3.12, 0.12, 0.62, fill=PRIMARY)
    box(s, 1.10, 3.10, 7.9, 0.66, text=sub, size=12.5, color=NAVY_TXT,
        anchor=MSO_ANCHOR.MIDDLE)
    return s


# =================================================================== 1. COVER
s = prs.slides.add_slide(L_DIV); blank_footer(s)
box(s, 0.70, 1.02, 8.6, 0.32, text="ZERO TRUST CNAPP SECURITY PLATFORM",
    size=12, color=SECOND, bold=True)
box(s, 0.66, 1.38, 8.7, 0.42, text="API Security beyond the WAF", size=15,
    color=NAVY_TXT, bold=False)
box(s, 0.70, 1.86, 3.2, 0.035, fill=PRIMARY)
box(s, 0.66, 2.00, 8.7, 1.5, text="Stop API Threats in Nginx\nand Kubernetes",
    size=38, color=WHITE, bold=True, anchor=MSO_ANCHOR.TOP)
box(s, 0.70, 3.46, 8.4, 0.66,
    text="Why the perimeter is only half the story, and how KubeArmor enforces network "
         "policy per workload at L3/L4 inside the cluster.",
    size=13, color=NAVY_TXT)
box(s, 0.70, 4.34, 0.12, 0.58, fill=PRIMARY)
box(s, 0.94, 4.32, 8.2, 0.62,
    text="AccuKnox Webinar  ·  2026\nRun-time API defense for Nginx, Kubernetes, Istio and AWS API Gateway",
    size=10.5, color=NAVY_TXT, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 2. AGENDA
s = content("What we'll cover today", "Agenda")
ag = [
 ("01", "Why API Security Needs More Than a WAF", PRIMARY,
  ["What a WAF misses, lateral API calls and service mesh traffic",
   "API risk across Nginx, Kubernetes, Istio and AWS API Gateway",
   "Abuse patterns: credential stuffing, shadow APIs, unauthorized access"]),
 ("02", "KubeArmor Network Enforcement at L3/L4", PURPLE,
  ["Per-workload network policies for ingress and egress",
   "DNS-based egress rules and domain allowlisting",
   "Violation alerts and PTS rules for shell vs. programmatic paths"]),
 ("03", "AccuKnox API Security in Practice", GREEN_DK,
  ["Integration matrix across gateways, proxies and service meshes",
   "Reference architecture: discovery, analytics, policy, alerting",
   "What it looks like in the console, and how to start"]),
]
cw3 = (CW - 0.6) / 3
cw2 = (CW - 0.3) / 2
rx  = CX + cw2 + 0.3
for i, (num, hd, ac, subs) in enumerate(ag):
    x = CX + i * (cw3 + 0.3)
    box(s, x, 1.24, cw3, 3.10, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, 1.24, cw3, 0.09, fill=ac, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    box(s, x + 0.18, 1.42, 0.9, 0.5, text=num, size=27, color=ac, bold=True)
    box(s, x + 0.18, 1.96, cw3 - 0.36, 0.86, text=hd, size=13, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.TOP)
    bullets(s, x + 0.18, 2.80, cw3 - 0.34, 1.5, subs, size=9.6, color=MUTE,
            mcolor=ac, gap=7)
box(s, CX, 4.52, CW, 0.5, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.14,
    text="Takeaway: a WAF and a run-time enforcer answer different questions. You need both, "
         "and you need them on the same policy model.",
    size=10.5, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== 3. THE NUMBERS
s = content("The API attack surface, by the numbers", "Why this session exists")
nums = [
 ("108 bn", "API attacks logged, Jan 2023 to Jun 2024", RED, "Akamai SOTI, 2024"),
 ("57%", "of dynamic internet traffic is API traffic", PRIMARY, "Cloudflare, 2024"),
 ("60-80%", "of API calls go east-west", NAVY, "AccuKnox telemetry, 2026"),
 ("99%", "of attack attempts are authenticated", PURPLE, "Salt Security, 2026"),
 ("+30.7%", "more live endpoints than inventoried", GREEN_DK, "Cloudflare, 2024"),
 ("59%", "of API flaws need no authentication", RED, "Wallarm, 2026"),
]
nw = (CW - 5 * 0.16) / 6
for i, (n, l, c, src) in enumerate(nums):
    stat(s, CX + i * (nw + 0.16), 1.20, nw, n, l, color=c, nsize=19, lsize=7.8, h=1.60,
         source=src, ssize=6.8)
box(s, CX, 3.00, CW, 0.72, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, CX + 0.18, 3.06, CW - 0.4, 0.26, text="THE ARCHITECTURAL FACT UNDERNEATH ALL OF IT",
    size=8.6, color=SECOND, bold=True)
box(s, CX + 0.18, 3.30, CW - 0.4, 0.38,
    text="“By default, if no policies exist in a namespace, then all ingress and egress traffic "
         "is allowed to and from pods in that namespace.”  ·  Kubernetes documentation",
    size=10.6, color=WHITE, italic=True)
two = [("Authenticated attackers are the norm, not the exception", PURPLE,
        "Salt Labs found 99% of attack attempts arrive with valid credentials, and 78% use an "
         "OWASP API Top 10 technique. Signature matching at the edge has nothing to match on."),
       ("The endpoints you do not know about are the exposed ones", GREEN_DK,
        "Cloudflare's discovery found a median 30.7% more endpoints than customers listed, and "
         "only 24% of organisations run a fully automated API inventory.")]
for i, (hd, ac, bd) in enumerate(two):
    x = CX + i * (cw2 + 0.3)
    box(s, x, 3.86, cw2, 1.00, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, 3.86, 0.08, 1.00, fill=ac)
    box(s, x + 0.18, 3.88, cw2 - 0.36, 0.28, text=hd, size=10.4, color=ac, bold=True)
    box(s, x + 0.18, 4.16, cw2 - 0.36, 0.66, text=bd, size=8.8, color=MUTE,
        anchor=MSO_ANCHOR.TOP)
footer_note(s, "Full source list on the last slide. AccuKnox's east-west share is its own telemetry, "
               "not a third-party report.", y=4.94)

# =================================================================== 4. DIVIDER 1
divider("Part 01", "Why API Security Needs\nMore Than a WAF",
        "Security across the entire API attack surface, not only at the perimeter.")

# =================================================================== 4. WHAT A WAF SEES
s = content("What a WAF actually sees", "The perimeter problem")
box(s, CX, 1.20, CW, 0.34,
    text="A Web Application Firewall inspects traffic crossing the edge. It has no visibility "
         "once a request is already inside the cluster.",
    size=11.5, color=INK)
# left: what a WAF covers
box(s, CX, 1.66, cw2, 3.22, fill=WHITE, line=GREY_BD, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, CX, 1.66, cw2, 0.09, fill=GREEN, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
icon(s, CX + 0.18, 1.86, 0.42, G('check'), bg=GREEN_DK)
box(s, CX + 0.70, 1.84, cw2 - 0.9, 0.46, text="What a WAF covers", size=13.5,
    color=GREEN_DK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
for i, t in enumerate(["North-south traffic entering at the edge",
                       "Known signature-based attacks (SQLi, XSS)",
                       "Rate limiting on public-facing endpoints",
                       "Basic bot and scanner fingerprinting"]):
    y = 2.46 + i * 0.56
    box(s, CX + 0.20, y, cw2 - 0.4, 0.46, fill=GREEN_LT,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.09)
    box(s, CX + 0.32, y, cw2 - 0.6, 0.46, text=t, size=10.2, color=INK,
        anchor=MSO_ANCHOR.MIDDLE)
# right: what it misses
box(s, rx, 1.66, cw2, 3.22, fill=WHITE, line=GREY_BD, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, rx, 1.66, cw2, 0.09, fill=RED, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
icon(s, rx + 0.18, 1.86, 0.42, G('warn'), bg=RED)
box(s, rx + 0.70, 1.84, cw2 - 0.9, 0.46, text="What it misses", size=13.5,
    color=RED, bold=True, anchor=MSO_ANCHOR.MIDDLE)
for i, t in enumerate(["Lateral, service-to-service (east-west) API calls",
                       "Traffic already inside the mesh, pod-to-pod",
                       "Internal abuse by compromised or over-privileged workloads",
                       "Business-logic and authorization abuse on valid requests"]):
    y = 2.46 + i * 0.56
    box(s, rx + 0.20, y, cw2 - 0.4, 0.46, fill=RED_LT,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.09)
    box(s, rx + 0.32, y, cw2 - 0.6, 0.46, text=t, size=10.2, color=INK,
        anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== OWASP API TOP 10
s = content("OWASP API Security Top 10, and what a WAF can reach", "The risk model")
box(s, CX, 1.16, CW, 0.30,
    text="Five of the ten risks depend on identity, object ownership or business meaning. A WAF "
         "has none of that context, so it cannot see them at all.", size=11, color=INK)
owasp = [
 ("API1:2023", "Broken Object Level Authorization", False),
 ("API2:2023", "Broken Authentication", True),
 ("API3:2023", "Broken Object Property Level Authorization", False),
 ("API4:2023", "Unrestricted Resource Consumption", False),
 ("API5:2023", "Broken Function Level Authorization", False),
 ("API6:2023", "Unrestricted Access to Sensitive Business Flows", True),
 ("API7:2023", "Server Side Request Forgery", True),
 ("API8:2023", "Security Misconfiguration", True),
 ("API9:2023", "Improper Inventory Management", False),
 ("API10:2023", "Unsafe Consumption of APIs", True),
]
ow = 4.42
for i, (rid, name, partial) in enumerate(owasp):
    col, row = i // 5, i % 5
    x = CX + col * (ow + 0.36)
    y = 1.58 + row * 0.44
    fl = GREY_BG if partial else RED_LT
    ln = GREY_BD if partial else RED
    box(s, x, y, ow, 0.38, fill=fl, line=ln, line_w=0.75,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    box(s, x + 0.10, y, 0.80, 0.38, text=rid.split(':')[0], size=8.6,
        color=(MUTE if partial else RED), bold=True, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    box(s, x + 0.92, y, ow - 1.30, 0.38, text=name, size=9.0, color=INK,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + ow - 0.44, y, 0.40, 0.38, text=("part" if partial else "blind"), size=7.4,
        color=(MUTE if partial else RED), bold=True, align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE, wrap=False)
# legend
box(s, CX, 3.86, 1.90, 0.28, fill=RED_LT, line=RED, line_w=0.75,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
box(s, CX, 3.86, 1.90, 0.28, text="blind  =  WAF cannot see it", size=8.4, color=RED,
    bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, 2.42, 3.86, 2.30, 0.28, fill=GREY_BG, line=GREY_BD, line_w=0.75,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
box(s, 2.42, 3.86, 2.30, 0.28, text="part  =  partial signature coverage", size=8.4,
    color=MUTE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, CX, 4.28, CW, 0.74, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, CX + 0.18, 4.32, CW - 0.4, 0.24, text="WHY BOLA IS THE CANONICAL CASE", size=8.4,
    color=SECOND, bold=True)
box(s, CX + 0.18, 4.56, CW - 0.4, 0.42,
    text="A valid user changes an object ID and reads someone else's record. The request is "
         "well-formed, authenticated and rate-limit compliant. Nothing in it looks like an attack.",
    size=10.2, color=WHITE)
footer_note(s, "OWASP API Security Top 10, 2023 edition. Wallarm's 2026 dataset puts BOLA at 39% of "
               "API vulnerabilities, the single largest class.", y=5.12)

# =================================================================== 5. N-S vs E-W
s = content("Lateral API calls and service mesh traffic", "North-south vs east-west")
box(s, CX, 1.18, CW, 0.30,
    text="Most east-west traffic inside a service mesh never touches the WAF at all.",
    size=11.5, color=INK)
# north-south band
box(s, CX, 1.58, CW, 1.16, fill=GREY_BG, line=GREY_BD, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, CX + 0.14, 1.64, 3.4, 0.24, text="NORTH-SOUTH (WAF-VISIBLE)", size=8.6,
    color=GREEN_DK, bold=True)
nsx = [("globe", "Internet\nClient", MUTE), ("firewall", "WAF", GREEN_DK),
       ("swap", "API Gateway", PRIMARY)]
bw = 1.66
for i, (g, lbl, c) in enumerate(nsx):
    x = CX + 0.20 + i * (bw + 0.52)
    box(s, x, 1.94, bw, 0.68, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    icon(s, x + 0.12, 2.05, 0.44, G(g), bg=c)
    box(s, x + 0.62, 1.94, bw - 0.7, 0.68, text=lbl, size=10, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    if i < 2:
        arrow(s, x + bw + 0.10, 2.14, 0.32, 0.32, color=GREEN_DK, size=15)
arrow(s, CX + 0.20 + 2 * (bw + 0.52) + bw + 0.10, 2.14, 0.32, 0.32, color=PRIMARY, size=15)
box(s, 7.06, 1.94, 2.5, 0.68, fill=WHITE, line=GREY_BD, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08,
    text="Only this hop is\ninspected by the WAF", size=9.2, color=MUTE,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
# east-west band
box(s, CX, 2.88, CW, 2.02, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
box(s, CX + 0.14, 2.96, 5.0, 0.24, text="KUBERNETES CLUSTER  ·  ISTIO SERVICE MESH",
    size=8.6, color=NAVY_TXT, bold=True)
box(s, CX + 0.14, 4.60, 5.4, 0.24, text="EAST-WEST (INVISIBLE TO THE WAF)", size=9,
    color=RGBColor(0xFF, 0x8A, 0x9A), bold=True)
svcs = [("swap", "Orders API"), ("key", "Payments API"), ("db", "Inventory API"),
        ("finger", "Auth Service")]
sw = 2.02
for i, (g, lbl) in enumerate(svcs):
    x = CX + 0.20 + i * (sw + 0.18)
    box(s, x, 3.30, sw, 1.16, fill=NAVY_DK, line=SECOND, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    icon(s, x + (sw - 0.46) / 2, 3.42, 0.46, G(g), bg=SECOND)
    box(s, x, 3.94, sw, 0.44, text=lbl, size=10.5, color=WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < 3:
        box(s, x + sw + 0.005, 3.80, 0.17, 0.20, text="⇄", size=12,
            color=RGBColor(0xFF, 0x8A, 0x9A), bold=True, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0, mr=0, mt=0, mb=0)

# =================================================================== 6. INTERNAL ABUSE
s = content("Internal abuse: when trusted becomes the threat", "The trusted-zone risk")
box(s, CX, 1.20, CW, 0.30,
    text="Once a workload is inside the cluster, most stacks implicitly trust it. Attackers know this.",
    size=11.5, color=INK)
ab = [
 ("bug", "Compromised Pod", RED,
  "A single vulnerable container becomes a foothold for calling internal APIs directly, "
  "bypassing edge controls entirely."),
 ("key", "Over-Permissioned Service Accounts", NAVY,
  "Service identities with broad network and API access let one breached workload reach "
  "far more than it needs."),
 ("person", "Insider / Credential Misuse", PURPLE,
  "Valid credentials used from an unexpected workload or namespace rarely trigger any "
  "perimeter alert."),
 ("route", "Post-Breach Lateral Movement", PRIMARY,
  "Attackers pivot pod-to-pod and service-to-service, mapping and exfiltrating data the "
  "WAF never inspects."),
]
ch = 1.62
for i, (g, hd, ac, bd) in enumerate(ab):
    card(s, CX + (i % 2) * (cw2 + 0.3), 1.62 + (i // 2) * (ch + 0.2), cw2, ch, hd, bd,
         accent=ac, hsize=12.5, bsize=10.2, ic=g)

# =================================================================== 7. STACK RISK
s = content("API risk across the cloud-native stack", "Cloud-native attack surface")
box(s, CX, 1.18, CW, 0.30,
    text="Each layer of the stack introduces its own API exposure and its own blind spots.",
    size=11.5, color=INK)
layers = [
 ("swap", "Nginx / Ingress", PRIMARY,
  "Routes external traffic into the cluster.",
  "A misconfigured ingress rule exposes an internal admin API (/internal/admin/*) to the "
  "public internet because a path-matching rule was too broad."),
 ("gears", "Kubernetes", PURPLE,
  "Pod networking is flat by default.",
  "Any pod can reach any other pod's IP unless a NetworkPolicy explicitly restricts it, "
  "so one foothold sees the whole namespace."),
 ("net", "Istio Service Mesh", SECOND,
  "mTLS protects transport, not authorization.",
  "Service A and Service B authenticate fine via mTLS, but with no AuthorizationPolicy "
  "nothing restricts which service may call which endpoint."),
 ("cloud", "AWS API Gateway", GREEN_DK,
  "Throttling, API keys and usage plans at the edge.",
  "A resource policy or Lambda integration left too permissive lets an internal-only "
  "endpoint be invoked by any authenticated AWS caller."),
]
lw = (CW - 0.6) / 4
for i, (g, hd, ac, lead, risk) in enumerate(layers):
    x = CX + i * (lw + 0.2)
    box(s, x, 1.58, lw, 3.44, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, 1.58, lw, 0.09, fill=ac, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    icon(s, x + 0.16, 1.76, 0.42, G(g), bg=ac)
    box(s, x + 0.16, 2.26, lw - 0.32, 0.44, text=hd, size=12, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.TOP)
    box(s, x + 0.16, 2.70, lw - 0.32, 0.50, text=lead, size=9.6, color=MUTE)
    box(s, x + 0.14, 3.24, lw - 0.28, 1.70, fill=RED_LT,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, x + 0.24, 3.30, lw - 0.48, 0.22, text="RISK EXAMPLE", size=7.6, color=RED, bold=True)
    box(s, x + 0.24, 3.52, lw - 0.48, 1.36, text=risk, size=8.8, color=INK,
        anchor=MSO_ANCHOR.TOP)

# =================================================================== 8. ABUSE PATTERNS
s = content("Common API abuse patterns", "Abuse patterns")
box(s, CX, 1.18, CW, 0.30,
    text="These patterns routinely slip past a WAF because the individual requests look legitimate.",
    size=11.5, color=INK)
pat = [
 ("Volumetric", "bolt", "Credential Stuffing", RED,
  "Automated login attempts using breached credential pairs, distributed across IPs and "
  "sessions to stay under rate-limit thresholds."),
 ("Visibility Gap", "eye", "Shadow APIs", PURPLE,
  "Undocumented or forgotten endpoints running in production with no inventory, ownership "
  "or monitoring. For example /v1/debug/users."),
 ("Logic Flaw", "lock", "Unauthorized Access", NAVY,
  "Broken object-level authorization lets an authenticated caller reach data or actions "
  "outside its intended scope."),
]
for i, (tag, g, hd, ac, bd) in enumerate(pat):
    x = CX + i * (cw3 + 0.3)
    box(s, x, 1.62, cw3, 2.40, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, 1.62, cw3, 0.09, fill=ac, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    pill(s, x + 0.16, 1.80, 1.26, 0.26, tag, fill=LAV, tcolor=ac, size=8)
    icon(s, x + 0.16, 2.18, 0.44, G(g), bg=ac)
    box(s, x + 0.70, 2.16, cw3 - 0.9, 0.48, text=hd, size=13, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.18, 2.74, cw3 - 0.36, 1.18, text=bd, size=10, color=MUTE)

# =================================================================== INCIDENTS
s = content("This is not theoretical", "Published incidents")
box(s, CX, 1.16, CW, 0.30,
    text="Two shapes of failure. One abuses a public endpoint at scale. The other gets a foothold, "
         "then walks the cluster.", size=11, color=INK)
box(s, CX, 1.54, cw2, 0.34, text="PERIMETER API ABUSE  ·  NORTH-SOUTH", size=9,
    color=GREEN_DK, bold=True)
ns_inc = [("T-Mobile", "2023", "37 million accounts exposed through a single abused API. No other "
           "system was breached.", "SEC filing"),
          ("Dell", "2024", "49 million customer records scraped from a partner-portal API after "
           "registering as a fake company.", "BleepingComputer"),
          ("Optus", "2022", "About 9.5 million Australians affected. The regulator is pursuing "
           "penalties per individual.", "OAIC"),
          ("Duolingo", "2023", "2.6 million user records scraped from one exposed endpoint that "
           "stayed open after disclosure.", "CPO Magazine")]
for i, (org, yr, bd, src) in enumerate(ns_inc):
    y = 1.92 + i * 0.76
    box(s, CX, y, cw2, 0.70, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, CX, y, 0.08, 0.70, fill=GREEN_DK)
    box(s, CX + 0.18, y + 0.02, 2.0, 0.26, text=f"{org}  ·  {yr}", size=10.4,
        color=GREEN_DK, bold=True)
    box(s, cw2 - 1.30, y + 0.02, 1.36, 0.26, text=src, size=7.6, color=GREY_BD,
        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    box(s, CX + 0.18, y + 0.26, cw2 - 0.36, 0.42, text=bd, size=8.8, color=MUTE,
        anchor=MSO_ANCHOR.TOP)
box(s, rx, 1.54, cw2, 0.34, text="IN-CLUSTER LATERAL MOVEMENT  ·  EAST-WEST", size=9,
    color=RED, bold=True)
ew_inc = [("Hildegard / TeamTNT", "2021", "Entry through an anonymous-access kubelet, then "
           "container-to-container movement and token harvesting.", "Unit 42"),
          ("Siloscape", "2021", "Container escape into the cluster, then a backdoor for running "
           "attacker containers.", "Unit 42"),
          ("SCARLETEEL", "2023", "Foothold in a container, plaintext credentials, then lateral "
           "movement via direct cloud API calls.", "Sysdig"),
          ("Tesla", "2018", "An open, unauthenticated Kubernetes console mining cryptocurrency. "
           "The exposed API was the whole attack.", "RedLock / WIRED")]
for i, (org, yr, bd, src) in enumerate(ew_inc):
    y = 1.92 + i * 0.76
    box(s, rx, y, cw2, 0.70, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, rx, y, 0.08, 0.70, fill=RED)
    box(s, rx + 0.18, y + 0.02, 2.4, 0.26, text=f"{org}  ·  {yr}", size=10.4,
        color=RED, bold=True)
    box(s, rx + cw2 - 1.42, y + 0.02, 1.36, 0.26, text=src, size=7.6, color=GREY_BD,
        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    box(s, rx + 0.18, y + 0.26, cw2 - 0.36, 0.42, text=bd, size=8.8, color=MUTE,
        anchor=MSO_ANCHOR.TOP)
footer_note(s, "In every east-west case the first foothold was small. What made it a breach was "
               "everything the workload could reach next.", y=5.02)

# =================================================================== MITRE
s = content("What the lateral path looks like in MITRE ATT&CK", "Mapping the movement")
box(s, CX, 1.18, CW, 0.32,
    text="MITRE's Containers matrix has no Lateral Movement column. Real container-to-container "
         "movement shows up as this chain of techniques instead.", size=11, color=INK)
rows = [("ID", "Technique", "What it looks like in your cluster", "Does a network allow-list help?"),
        ("T1610", "Deploy Container", "Attacker schedules a pod to run code inside the cluster network", "Yes, the new pod has no declared peers"),
        ("T1611", "Escape to Host", "Container-to-node break-out, the usual step before moving sideways", "Partly, host policy still applies"),
        ("T1613", "Container and Resource Discovery", "Enumerating pods and services over the cluster API", "Yes, API-server egress is deniable"),
        ("T1609", "Container Administration Command", "Abusing kubelet or the docker daemon API to execute commands", "Yes, plus PTS flags the shell path"),
        ("T1552.007", "Unsecured Credentials: Container API", "Harvesting credentials through the container or cluster API", "Partly, blocks the exfil hop"),
        ("T1550.001", "Application Access Token", "Reusing a stolen service-account token to call internal APIs", "Yes, the caller is not a declared peer")]
table(s, CX, 1.58, CW, 2.92, rows, colw=[0.98, 2.30, 3.42, 2.50], hsize=9.0, bsize=8.4)
box(s, CX, 4.62, CW, 0.46, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12,
    text="A per-workload allow-list does not stop the initial foothold. It stops the four steps "
         "that turn a foothold into an incident.",
    size=10.4, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
footer_note(s, "Technique IDs and names from MITRE ATT&CK Enterprise, current version.", y=5.14)

# =================================================================== 9. WAF vs KUBEARMOR
s = content("A WAF alone isn't enough", "The case for layered defense")
box(s, CX, 1.20, CW, 0.30,
    text="Perimeter filtering and run-time enforcement solve different problems. You need both.",
    size=11.5, color=INK)
rows = [
 ("", "WAF (Perimeter)", "KubeArmor (Run-time L3/L4)"),
 ("Scope", "Edge / perimeter, north-south traffic",
  "Per-workload, ingress and egress at L3/L4"),
 ("Blind spot", "East-west / lateral API calls inside the mesh",
  "None inside the cluster boundary it governs"),
 ("Detection basis", "Signatures, rate limits, known attack patterns",
  "Declared policy: allowed peers, ports, domains"),
 ("Enforcement point", "Before the request reaches the cluster",
  "At the workload, using kernel-level primitives"),
 ("Best for", "Stopping known external attack patterns early",
  "Containing abuse and lateral movement in real time"),
]
table(s, CX, 1.62, CW, 3.10, rows, colw=[1.90, 3.65, 3.65], hsize=11, bsize=10.2)
footer_note(s, "Same policy language, two enforcement points. The rest of this session is about the second one.")

# =================================================================== DIVIDER 2
divider("Part 02", "KubeArmor Network\nEnforcement at L3/L4",
        "Declare what each workload may talk to, then enforce it in the kernel.")

# =================================================================== KUBEARMOR INTRO
s = content("What KubeArmor enforces, and where", "The run-time engine")
box(s, CX, 1.18, 4.35, 0.64,
    text="KubeArmor is the CNCF run-time engine under AccuKnox CWPP. It watches each workload "
         "with eBPF, then enforces a least-permissive policy in the kernel.",
    size=10.8, color=INK)
ka = [("eye", "Observe", "eBPF traces process, file, network and API behaviour per workload.", PRIMARY),
      ("wrench", "Auto-discover", "The Policy Discovery Engine drafts policy from observed behaviour.", PURPLE),
      ("shield", "Enforce", "AppArmor, BPF-LSM or SELinux block off-policy actions inline.", RED),
      ("pulse", "Alert", "Every denial becomes a structured event for your SIEM.", GREEN_DK)]
for i, (g, hd, sub, ac) in enumerate(ka):
    list_row(s, CX, 2.00 + i * 0.74, 4.35, G(g), hd, sub, accent=ac, h=0.70, ssize=9.2)
image_fit(s, P("kubearmor-observe-enforce-arch.png"), RCOLX, 1.10, 4.62, 3.34,
          frame=GREY_BD,
          caption="Observe with eBPF, deploy least-permissive policy, enforce at the kernel.")
kf = [("CNCF Sandbox", "since 16 Nov 2021"), ("2,577", "GitHub stars"),
      ("BPF-LSM", "first K8s engine "), ("3 LSMs", "AppArmor, BPF, SELinux")]
kw = (4.62 - 3 * 0.12) / 4
for i, (n, l) in enumerate(kf):
    x = RCOLX + i * (kw + 0.12)
    box(s, x, 4.80, kw, 0.50, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.10)
    box(s, x, 4.82, kw, 0.24, text=n, size=9.6, color=NAVY, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    box(s, x, 5.04, kw, 0.22, text=l, size=6.8, color=MUTE, align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE, wrap=False)
box(s, CX, 4.94, 4.35, 0.44, fill=GREEN_LT, line=GREEN, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12,
    text="Runs alongside your CNI NetworkPolicy, not instead of it.", size=9.4,
    color=GREEN_DK, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== PER-WORKLOAD POLICY
s = content("Per-workload network policies", "Ingress and egress control")
box(s, CX, 1.18, CW, 0.30,
    text="Each workload gets its own explicit allow-list, covering both what may reach it and "
         "what it may reach.", size=11.5, color=INK)
# centre workload chip
box(s, 3.86, 1.58, 2.28, 0.72, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.10)
icon(s, 3.98, 1.71, 0.46, G('gears'), bg=PRIMARY)
box(s, 4.52, 1.58, 1.54, 0.40, text="Workload Pod", size=10.5, color=WHITE, bold=True,
    anchor=MSO_ANCHOR.BOTTOM, mb=0)
box(s, 4.52, 1.96, 1.54, 0.30, text="KubeArmor policy attached", size=7.8, color=NAVY_TXT,
    anchor=MSO_ANCHOR.TOP, mt=0)
# ingress panel
def _rules(x, y, w, title, tcolor, items, deny):
    box(s, x, y, w, 2.62, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, y, w, 0.09, fill=tcolor, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    box(s, x + 0.16, y + 0.14, w - 0.32, 0.28, text=title, size=9.6, color=tcolor, bold=True)
    for i, it in enumerate(items):
        yy = y + 0.48 + i * 0.48
        box(s, x + 0.16, yy, w - 0.32, 0.40, fill=GREY_BG,
            shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.10)
        box(s, x + 0.28, yy, w - 0.5, 0.40, text=it, size=9.6, color=INK,
            anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.16, y + 2.06, w - 0.32, 0.42, fill=RED_LT, line=RED, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.10)
    box(s, x + 0.16, y + 2.06, w - 0.32, 0.42, text=deny, size=9.4, color=RED, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

_rules(CX, 2.42, 4.42, "INGRESS  ·  ALLOWED CALLERS", GREEN_DK,
       ["Frontend Gateway  →  :8080/tcp",
        "Auth Service  →  :8443/tcp",
        "Internal Health Checker  →  :9090/tcp"],
       "All other inbound traffic: DENIED")
_rules(5.18, 2.42, 4.42, "EGRESS  ·  ALLOWED TARGETS", PRIMARY,
       ["Payments API  →  :443/tcp",
        "Internal DB Service  →  :5432/tcp",
        "api.stripe.com  →  :443/tcp (DNS)"],
       "All other outbound traffic: DENIED")

# =================================================================== POLICY YAML
s = content("What the policy looks like", "Copy-ready")
box(s, CX, 1.18, CW, 0.30,
    text="One KubeArmorPolicy object per workload. Declarative, version-controlled, and enforced "
         "in the kernel rather than by a sidecar.", size=11.5, color=INK)
code_block(s, CX, 1.58, 4.90, 3.48, [
    ("apiVersion: security.kubearmor.com/v1", True),
    ("kind: KubeArmorPolicy", True),
    "metadata:",
    "  name: egress-allow-payments-api",
    "  namespace: production",
    "spec:",
    "  selector:",
    "    matchLabels:",
    "      app: orders-api",
    "  network:",
    "    matchProtocols:",
    "      - protocol: tcp",
    "        fromSource:",
    "          - path: /usr/local/bin/orders-api   # PTS rule",
    "  action: Allow",
    "",
    "# anything not declared above is denied,",
    "# and every denial raises a structured alert",
], size=8.8, title="kubearmor-policy.yaml")
notes = [
 ("shield", "Kernel enforcement", "No sidecar to bypass. AppArmor or BPF-LSM applies the rule.", RED),
 ("wrench", "Auto-drafted", "AccuKnox proposes this YAML from observed behaviour, so you review rather than write.", PURPLE),
 ("swap", "fromSource is the PTS hook", "The same destination can be allowed for the binary and denied for a shell.", PRIMARY),
 ("check", "GitOps friendly", "Ship policy through the same pipeline as your manifests.", GREEN_DK),
]
for i, (g, hd, sub, ac) in enumerate(notes):
    list_row(s, 5.52, 1.62 + i * 0.82, 4.08, G(g), hd, sub, accent=ac, h=0.78, ssize=9.3)

# =================================================================== DNS EGRESS
s = content("DNS-based egress rules", "Domain-aware egress")
box(s, CX, 1.18, CW, 0.30,
    text="Outbound traffic is restricted to a declared domain allowlist, resolved and enforced at "
         "the DNS layer rather than by IP alone.", size=11.5, color=INK)
flow = [("gears", "Workload", "opens an outbound connection", PRIMARY),
        ("search", "DNS Resolution", "KubeArmor intercepts and checks", PURPLE),
        ("list", "Declared Allowlist", "matched against policy", NAVY)]
fw = 2.86
for i, (g, hd, sub, ac) in enumerate(flow):
    x = CX + i * (fw + 0.31)
    box(s, x, 1.58, fw, 0.92, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    icon(s, x + 0.16, 1.78, 0.50, G(g), bg=ac)
    box(s, x + 0.76, 1.68, fw - 0.9, 0.40, text=hd, size=11.5, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.BOTTOM, mb=0)
    box(s, x + 0.76, 2.06, fw - 0.9, 0.34, text=sub, size=9.2, color=MUTE,
        anchor=MSO_ANCHOR.TOP, mt=0)
    if i < 2:
        arrow(s, x + fw + 0.02, 1.92, 0.28, 0.28, color=PRIMARY, size=15)
# allow branch
box(s, CX, 2.72, 4.42, 2.16, fill=GREEN_LT, line=GREEN, line_w=1.25,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
icon(s, CX + 0.18, 2.86, 0.40, G('check'), bg=GREEN_DK)
box(s, CX + 0.68, 2.84, 3.5, 0.42, text="ALLOW  →  connection proceeds", size=11,
    color=GREEN_DK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
for i, d in enumerate(["api.stripe.com", "*.internal.svc.cluster.local", "pypi.org"]):
    yy = 3.36 + i * 0.46
    box(s, CX + 0.20, yy, 4.02, 0.38, fill=WHITE, line=GREEN, line_w=0.75,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    box(s, CX + 0.34, yy, 3.8, 0.38, text=d, size=9.6, color=INK,
        anchor=MSO_ANCHOR.MIDDLE, font=MONO)
# deny branch
box(s, 5.18, 2.72, 4.42, 2.16, fill=RED_LT, line=RED, line_w=1.25,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
icon(s, 5.36, 2.86, 0.40, G('cancel'), bg=RED)
box(s, 5.86, 2.84, 3.5, 0.42, text="DENY  →  connection blocked", size=11,
    color=RED, bold=True, anchor=MSO_ANCHOR.MIDDLE)
box(s, 5.38, 3.36, 4.02, 0.38, fill=WHITE, line=RED, line_w=0.75,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
box(s, 5.52, 3.36, 3.8, 0.38, text="evil-exfil.net", size=9.6, color=RED,
    anchor=MSO_ANCHOR.MIDDLE, font=MONO)
box(s, 5.38, 3.84, 4.02, 0.94,
    text="An undeclared domain never resolves into an allowed connection, so a compromised "
         "workload cannot dial out to attacker infrastructure even with valid credentials in hand.",
    size=9.6, color=INK, anchor=MSO_ANCHOR.TOP)

# =================================================================== ALERTS
s = content("Violations surface as alerts", "Observability")
box(s, CX, 1.18, CW, 0.30,
    text="Every denied connection is logged as a structured alert and feeds straight into your "
         "existing monitoring stack.", size=11.5, color=INK)
steps = [("warn", "Policy Violation", "Egress or ingress attempt outside declared policy", RED),
         ("shield", "KubeArmor Enforcement", "Connection blocked at the kernel layer", NAVY),
         ("pulse", "Alert Generated", "Structured event with workload, policy and rule detail", PURPLE),
         ("chart", "SIEM / Dashboard", "Forwarded to your logging and alerting pipeline", GREEN_DK)]
stw = (CW - 3 * 0.28) / 4
for i, (g, hd, sub, ac) in enumerate(steps):
    x = CX + i * (stw + 0.28)
    box(s, x, 1.58, stw, 1.46, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, x, 1.58, stw, 0.09, fill=ac, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    icon(s, x + (stw - 0.44) / 2, 1.76, 0.44, G(g), bg=ac)
    box(s, x + 0.10, 2.22, stw - 0.20, 0.40, text=hd, size=10.5, color=NAVY, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
    box(s, x + 0.10, 2.62, stw - 0.20, 0.40, text=sub, size=8.2, color=MUTE,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
    if i < 3:
        arrow(s, x + stw + 0.01, 2.18, 0.26, 0.26, color=PRIMARY, size=13)
# sample alert
box(s, CX, 3.18, 4.34, 1.80, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, CX + 0.16, 3.24, 4.0, 0.26, text="SAMPLE ALERT", size=8.4, color=SECOND, bold=True)
al = [("POLICY", "egress-allow-payments-api"), ("WORKLOAD", "orders-api-7c9f5b-x2kq9"),
      ("NAMESPACE", "production"), ("ACTION", "Block"),
      ("DESTINATION", "203.0.113.44:443 (unresolved domain)"),
      ("RULE TYPE", "Network (L3/L4), Egress")]
for i, (k, v) in enumerate(al):
    yy = 3.54 + i * 0.24
    box(s, CX + 0.16, yy, 1.10, 0.24, text=k, size=7.4, color=NAVY_TXT, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    box(s, CX + 1.28, yy, 2.92, 0.24, text=v, size=8.2, color=WHITE,
        anchor=MSO_ANCHOR.MIDDLE, font=MONO)
image_fit(s, P("runtime-alert-events.png"), 5.10, 3.18, 4.50, 1.60, frame=GREY_BD,
          caption="Live KubeArmor alert stream in the AccuKnox console, filterable by cluster and severity.")

# =================================================================== PTS
s = content("PTS rules: shell vs. programmatic paths", "Process tracking")
box(s, CX, 1.18, CW, 0.34,
    text="Process Tree Source (PTS) rules let policy distinguish how a connection was initiated, "
         "not just where it goes. Same destination, different verdict.", size=11.5, color=INK)
# shell path
box(s, CX, 1.66, cw2, 3.22, fill=WHITE, line=RED, line_w=1.25,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, CX, 1.66, cw2, 0.09, fill=RED, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
icon(s, CX + 0.18, 1.86, 0.44, G('terminal'), bg=RED)
box(s, CX + 0.72, 1.84, cw2 - 0.9, 0.48, text="Shell-Initiated Path", size=13.5,
    color=RED, bold=True, anchor=MSO_ANCHOR.MIDDLE)
box(s, CX + 0.20, 2.42, cw2 - 0.40, 0.52,
    text="A connection opened from an interactive shell or a shell-spawned process inside the container.",
    size=10, color=MUTE)
code_block(s, CX + 0.20, 3.00, cw2 - 0.40, 0.52,
           [("bash  →  curl  →  api.internal.svc", True)], size=9.6, fill=NAVY_DK)
box(s, CX + 0.20, 3.62, cw2 - 0.40, 0.60,
    text="Usually means manual, debugging or anomalous activity. A common post-exploitation pattern.",
    size=10, color=MUTE)
box(s, CX + 0.20, 4.28, cw2 - 0.40, 0.44, fill=RED_LT, line=RED, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12,
    text="PTS RULE:  flag or deny by default", size=10, color=RED, bold=True,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
# programmatic path
box(s, rx, 1.66, cw2, 3.22, fill=WHITE, line=GREEN, line_w=1.25,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, rx, 1.66, cw2, 0.09, fill=GREEN, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
icon(s, rx + 0.18, 1.86, 0.44, G('code'), bg=GREEN_DK)
box(s, rx + 0.72, 1.84, cw2 - 0.9, 0.48, text="Programmatic Path", size=13.5,
    color=GREEN_DK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
box(s, rx + 0.20, 2.42, cw2 - 0.40, 0.52,
    text="A connection opened directly by the compiled application binary or its declared runtime.",
    size=10, color=MUTE)
code_block(s, rx + 0.20, 3.00, cw2 - 0.40, 0.52,
           [("orders-api (binary)  →  payments-api", True)], size=9.6, fill=NAVY_DK)
box(s, rx + 0.20, 3.62, cw2 - 0.40, 0.60,
    text="Matches the application's expected, declared communication pattern.",
    size=10, color=MUTE)
box(s, rx + 0.20, 4.28, cw2 - 0.40, 0.44, fill=GREEN_LT, line=GREEN, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12,
    text="PTS RULE:  allow per declared policy", size=10, color=GREEN_DK, bold=True,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== AUTO-DISCOVERY
s = content("You don't write these policies by hand", "Policy discovery")
box(s, CX, 1.18, 4.30, 0.80,
    text="The Policy Discovery Engine reads network and system logs, learns what each workload "
         "really talks to, then drafts Cilium, Kubernetes NetworkPolicy and KubeArmor objects "
         "for you to approve.",
    size=10.8, color=INK)
image_fit(s, P("policy-discovery-engine-arch.png"), CX, 2.06, 4.30, 1.78, frame=GREY_BD)
box(s, CX, 3.92, 4.30, 1.08, fill=GREEN_LT, line=GREEN, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
icon(s, CX + 0.16, 4.04, 0.40, G('bulb'), bg=GREEN_DK)
box(s, CX + 0.66, 3.98, 3.5, 0.30, text="Why this matters operationally", size=11,
    color=GREEN_DK, bold=True, anchor=MSO_ANCHOR.BOTTOM)
box(s, CX + 0.66, 4.28, 3.5, 0.70,
    text="Least-privilege networking fails in practice because nobody can enumerate every "
         "legitimate call. Discovery makes the allow-list an approval job, not a writing job.",
    size=8.8, color=INK, anchor=MSO_ANCHOR.TOP)
image_fit(s, P("network-policy-discovered-list.png"), RCOLX, 1.14, 4.62, 2.18, frame=GREY_BD,
          caption="Auto-discovered ingress and egress policies, waiting on approval.")
image_fit(s, P("runtime-policy-approved-active.png"), RCOLX, 3.68, 4.62, 1.18, frame=GREY_BD,
          caption="One click flips a discovered policy to Active enforcement.")

# =================================================================== DIVIDER 3
divider("Part 03", "AccuKnox API Security\nin Practice",
        "Discovery, risk analytics, policy and alerting on one control plane.")

# =================================================================== INTEGRATION MATRIX
s = content("API security integration matrix", "Where AccuKnox plugs in")
box(s, CX, 1.18, CW, 0.32,
    text="AccuKnox integrates with the gateways, proxies and service meshes already in your path, "
         "so live API traffic is observed without a new inline hop.", size=11.5, color=INK)
image_fit(s, W("api-integration-logos.png"), CX, 1.58, 3.30, 1.92, frame=GREY_BD,
          caption="Supported gateways, proxies and meshes.")
box(s, CX, 3.86, 3.30, 0.80, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06,
    text="Observation rides on infrastructure you already run, so there is no extra proxy in the "
         "request path and no latency budget to argue about.",
    size=9.4, color=NAVY, anchor=MSO_ANCHOR.MIDDLE, ml=0.16, mr=0.16)
rows = [("Plane", "What AccuKnox observes"),
        ("Data plane", "North-south API calls plus inter-microservice east-west calls"),
        ("Control plane", "Kubernetes API server and AWS CloudTrail"),
        ("Kubernetes", "On-prem and managed clusters, API server visibility"),
        ("Non-Kubernetes", "Ingress controllers such as Nginx and Kong"),
        ("AWS", "CloudTrail, CloudWatch and App Mesh"),
        ("Azure", "API Management, static functions and web apps"),
        ("Google", "Anthos")]
table(s, 3.96, 1.58, 5.64, 3.06, rows, colw=[1.44, 4.20], hsize=9.8, bsize=9.0)
footer_note(s, "Reference: help.accuknox.com/integrations/api-overview")

# =================================================================== REFERENCE ARCH
s = content("Reference architecture", "How the pieces fit")
stages = [("globe", "Client"), ("swap", "NGINX / Istio\nGateway"), ("eye", "API Observation\nLayer"),
          ("bolt", "Runtime\nDetection Engine"), ("search", "API\nDiscovery"),
          ("pie", "Risk\nAnalytics"), ("gears", "Policy\nEngine"), ("chart", "Dashboard\n& Alerts")]
gw = 1.02; gap = 0.14
tot = len(stages) * gw + (len(stages) - 1) * gap
sx = (10.0 - tot) / 2
for i, (g, lbl) in enumerate(stages):
    x = sx + i * (gw + gap)
    ac = PRIMARY if i < 3 else (PURPLE if i < 6 else GREEN_DK)
    box(s, x, 1.32, gw, 1.34, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.09)
    box(s, x, 1.32, gw, 0.08, fill=ac, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    icon(s, x + (gw - 0.42) / 2, 1.50, 0.42, G(g), bg=ac)
    box(s, x + 0.04, 2.00, gw - 0.08, 0.60, text=lbl, size=8.4, color=NAVY, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
    if i < len(stages) - 1:
        arrow(s, x + gw - 0.005, 1.86, 0.15, 0.22, color=PRIMARY, size=11)
box(s, CX, 2.74, CW, 0.30,
    text="Each component contributes to continuous API visibility, run-time protection, policy "
         "enforcement and centralised monitoring.", size=10.5, color=MUTE, italic=True)
image_fit(s, P("api-security-architecture.png"), CX, 3.08, 5.30, 1.94, frame=GREY_BD)
grp = [("OBSERVE", "Client through the observation layer. Traffic is read from the gateway, mesh "
        "or proxy already in your path, so there is no new inline hop.", PRIMARY),
       ("ANALYSE", "Discovery and risk analytics turn raw calls into an endpoint inventory with "
        "sensitive-data tags and severity.", PURPLE),
       ("ACT", "The policy engine pushes KubeArmor and network policy back to the workload, and "
        "every denial lands in your SIEM.", GREEN_DK)]
for i, (hd, bd, ac) in enumerate(grp):
    y = 3.08 + i * 0.66
    box(s, 5.90, y, 3.70, 0.60, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, 5.90, y, 0.08, 0.60, fill=ac)
    box(s, 6.06, y + 0.02, 3.44, 0.22, text=hd, size=8.6, color=ac, bold=True)
    box(s, 6.06, y + 0.22, 3.44, 0.36, text=bd, size=8.2, color=MUTE, anchor=MSO_ANCHOR.TOP)

# =================================================================== CONSOLE: DISCOVERY
s = content("API discovery and sensitive-data mapping", "In the console  ·  1 of 2")
box(s, CX, 1.18, 4.30, 0.60,
    text="AccuKnox inventories every live endpoint it observes, marks the ones that carry "
         "sensitive parameters, and flags endpoints with no authentication at all.",
    size=11, color=INK)
disc = [("search", "Full endpoint inventory", "Method, path, auth state and last-seen, per cluster.", PRIMARY),
        ("eye", "Internal vs external split", "Know which endpoints are reachable from outside.", PURPLE),
        ("lock", "Sensitive parameter tagging", "Usernames, emails, tokens, JWTs and access keys.", RED),
        ("warn", "Unauthenticated endpoints", "Surfaced as their own filter, not buried in a report.", GREEN_DK)]
for i, (g, hd, sub, ac) in enumerate(disc):
    list_row(s, CX, 1.90 + i * 0.76, 4.30, G(g), hd, sub, accent=ac, h=0.72, ssize=9.3)
image_fit(s, P("api-discovery-dashboard.png"), RCOLX, 1.16, 4.62, 3.52, frame=GREY_BD,
          caption="API Security dashboard: discovered endpoints, sensitive datatypes and severity split.")

# =================================================================== CONSOLE: SHADOW
s = content("Shadow and orphan APIs, found and ranked", "In the console  ·  2 of 2")
box(s, CX, 1.18, CW, 0.32,
    text="Endpoints that exist in traffic but not in any spec are the ones nobody is watching. "
         "AccuKnox raises them as findings with severity, not as a list to triage later.",
    size=11.5, color=INK)
image_fit(s, P("api-shadow-orphan-findings.png"), CX, 1.62, 5.42, 1.78, frame=GREY_BD,
          caption="API security findings grouped by Shadow API (76) and Orphan API (4).")
defs = [("Shadow API", "Live in production, absent from the spec and the inventory. No owner, no monitoring.", PURPLE),
        ("Orphan API", "Still serving traffic after the consumer was retired. Nobody notices when it breaks or leaks.", NAVY),
        ("Zombie API", "A deprecated version left routable, usually on an older, unpatched code path.", RED)]
for i, (hd, bd, ac) in enumerate(defs):
    y = 1.60 + i * 0.78
    box(s, 6.10, y, 3.50, 0.70, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, 6.10, y, 0.08, 0.70, fill=ac)
    box(s, 6.28, y + 0.02, 3.24, 0.26, text=hd, size=10.5, color=ac, bold=True)
    box(s, 6.28, y + 0.26, 3.24, 0.42, text=bd, size=8.6, color=MUTE, anchor=MSO_ANCHOR.TOP)
tiles = [("76", "shadow APIs", PURPLE), ("4", "orphan APIs", NAVY),
         ("200", "endpoints discovered", PRIMARY), ("185", "sensitive-data findings", RED)]
tw2 = (5.42 - 3 * 0.16) / 4
for i, (n, l, c) in enumerate(tiles):
    x = CX + i * (tw2 + 0.16)
    box(s, x, 3.86, tw2, 0.84, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.10)
    box(s, x, 3.90, tw2, 0.36, text=n, size=20, color=c, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    box(s, x + 0.06, 4.26, tw2 - 0.12, 0.38, text=l, size=8.2, color=MUTE,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
box(s, CX, 4.76, 5.42, 0.26,
    text="Counts from the sample environment shown in the console screenshots.",
    size=8.5, color=MUTE, italic=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, 6.10, 3.94, 3.50, 1.08, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
box(s, 6.26, 4.02, 3.20, 0.28, text="Discovery feeds enforcement", size=11, color=WHITE, bold=True)
box(s, 6.26, 4.30, 3.20, 0.66,
    text="The same observed traffic that finds a shadow API also drafts the KubeArmor policy that "
         "fences it in. One data source, two outcomes.", size=8.8, color=NAVY_TXT,
    anchor=MSO_ANCHOR.TOP)

# =================================================================== LAYERED MODEL
s = content("Put the two layers together", "The target state")
box(s, CX, 1.18, CW, 0.32,
    text="Keep the WAF for what it is good at. Add per-workload enforcement for everything that "
         "never crosses the edge.", size=11.5, color=INK)
lay = [
 ("EDGE", "firewall", "WAF and API Gateway", GREEN_DK,
  ["Signature and rate-limit filtering", "Bot and scanner fingerprinting",
   "TLS termination and schema checks"]),
 ("IN-CLUSTER", "shield", "KubeArmor L3/L4 policy", PRIMARY,
  ["Per-workload ingress and egress allow-lists", "DNS-based domain allowlisting",
   "PTS rules on shell vs. binary paths"]),
 ("CONTROL PLANE", "chart", "AccuKnox API Security", PURPLE,
  ["Endpoint discovery and sensitive-data tagging", "Shadow, orphan and zombie API findings",
   "Policy discovery, approval and SIEM alerting"]),
]
for i, (tag, g, hd, ac, items) in enumerate(lay):
    x = CX + i * (cw3 + 0.3)
    box(s, x, 1.60, cw3, 2.66, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, 1.60, cw3, 0.09, fill=ac, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    pill(s, x + 0.16, 1.78, 1.44, 0.26, tag, fill=LAV, tcolor=ac, size=8)
    icon(s, x + 0.16, 2.16, 0.44, G(g), bg=ac)
    box(s, x + 0.70, 2.14, cw3 - 0.9, 0.48, text=hd, size=12, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    bullets(s, x + 0.18, 2.74, cw3 - 0.36, 1.44, items, size=9.4, color=MUTE,
            mcolor=ac, gap=6)
box(s, CX, 4.42, CW, 0.60, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.10)
icon(s, CX + 0.16, 4.50, 0.42, G('check'), bg=PRIMARY)
box(s, CX + 0.70, 4.42, CW - 0.9, 0.60,
    text="The test of the design: a compromised pod with valid credentials still cannot reach a "
         "service it was never declared to call, and the attempt shows up as an alert within seconds.",
    size=10.4, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== CTA
s = prs.slides.add_slide(L_DIV); blank_footer(s)
box(s, 0.70, 1.20, 8.6, 0.32, text="NEXT STEPS", size=13, color=SECOND, bold=True)
box(s, 0.66, 1.54, 8.7, 1.0, text="See it on your own cluster",
    size=32, color=WHITE, bold=True, anchor=MSO_ANCHOR.TOP)
box(s, 0.70, 2.52, 8.5, 0.62,
    text="Point AccuKnox at one namespace. You get the live endpoint inventory, the shadow-API "
         "findings, and a drafted KubeArmor policy set without writing a single rule yourself.",
    size=12.5, color=NAVY_TXT)
steps = [("search", "1.  Onboard a cluster", "Agentless connector on one namespace. Nothing inline, nothing to break."),
         ("eye", "2.  Watch for a week", "Endpoint inventory, sensitive-data tags and discovered policies build up."),
         ("shield", "3.  Enforce", "Approve the drafted policies, then flip them from audit to block.")]
sw = (8.6 - 0.4) / 3
for i, (g, hd, bd) in enumerate(steps):
    x = 0.70 + i * (sw + 0.2)
    icon(s, x, 3.34, 0.46, G(g), bg=PRIMARY, color=WHITE)
    box(s, x + 0.58, 3.32, sw - 0.58, 0.34, text=hd, size=12, color=WHITE, bold=True)
    box(s, x + 0.58, 3.64, sw - 0.58, 0.80, text=bd, size=9.5, color=NAVY_TXT,
        anchor=MSO_ANCHOR.TOP)
box(s, 0.70, 4.62, 0.12, 0.52, fill=PRIMARY)
box(s, 0.94, 4.60, 8.3, 0.56,
    text="Questions welcome now.  ·  help.accuknox.com  ·  support@accuknox.com  ·  accuknox.com",
    size=11, color=SECOND, bold=True, anchor=MSO_ANCHOR.MIDDLE)

# =================================================================== SOURCES
s = content("Sources", "Every number on the preceding slides")
src_l = [
 ("Akamai State of the Internet, 2024", "108 bn API attacks, Jan 2023 to Jun 2024. akamai.com/lp/soti/securing-apps-report-2024"),
 ("Cloudflare API Security Report, 2024", "APIs at 57% of dynamic traffic. A median 30.7% more endpoints found than inventoried."),
 ("Salt Security State of API Security, 2026", "99% of attempts authenticated; 78% use an OWASP API Top 10 method; 32% had an incident; 24% have automated inventory."),
 ("Wallarm API ThreatStats, 2026", "59% of API vulnerabilities need no authentication; BOLA is 39% of the dataset; 97% exploitable in one request."),
 ("OWASP API Security Project, 2023 edition", "The Top 10 IDs and names, quoted verbatim. owasp.org/API-Security/editions/2023"),
]
src_r = [
 ("MITRE ATT&CK Enterprise, current", "Technique IDs T1610, T1611, T1613, T1609, T1552.007, T1550.001."),
 ("Kubernetes documentation, current", "Default-allow ingress and egress in a namespace with no NetworkPolicy."),
 ("KubeArmor project and CNCF", "CNCF Sandbox since 16 Nov 2021; AppArmor, BPF-LSM and SELinux enforcement; 2,577 GitHub stars as of 13 Aug 2026."),
 ("Incident reporting, 2018 to 2024", "Unit 42 (Hildegard, Siloscape), Sysdig (SCARLETEEL), WIRED (Tesla), TechCrunch (T-Mobile), BleepingComputer (Dell), OAIC (Optus)."),
 ("AccuKnox", "60-80% east-west share is AccuKnox's own telemetry. accuknox.com/blog/api-security  ·  help.accuknox.com"),
]
for col, items in enumerate((src_l, src_r)):
    x = CX + col * (cw2 + 0.3)
    for i, (hd, bd) in enumerate(items):
        y = 1.20 + i * 0.76
        box(s, x, y, cw2, 0.70, fill=WHITE, line=GREY_BD, line_w=1.0,
            shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
        box(s, x, y, 0.08, 0.70, fill=PRIMARY if col == 0 else PURPLE)
        box(s, x + 0.18, y + 0.02, cw2 - 0.36, 0.24, text=hd, size=9.6,
            color=NAVY, bold=True)
        box(s, x + 0.18, y + 0.26, cw2 - 0.36, 0.42, text=bd, size=8.2, color=MUTE,
            anchor=MSO_ANCHOR.TOP)
footer_note(s, "Vendor research is cited to the publishing vendor. Where a figure is AccuKnox's own "
               "telemetry rather than third-party research, the slide says so.", y=5.04)

prs.save(OUT)
print("Saved:", OUT, "slides:", len(prs.slides._sldIdLst))
