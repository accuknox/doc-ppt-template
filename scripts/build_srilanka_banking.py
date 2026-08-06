# -*- coding: utf-8 -*-
"""
AccuKnox x VSOne - Zero Trust Security for Sri Lanka's Banks.
18-slide branded pitch deck built from the master PPT Template.pptx, using real
AccuKnox product screenshots / architecture diagrams (extracted from the CISO and
AI-Security macro decks into output/assets) and Segoe MDL2 line icons.

Render:  powershell -File scripts/render.ps1 -Pptx <OUT> -Out <dir>
"""
import os, shutil
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image as PILImage

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "PPT Template.pptx")
AST  = os.path.join(HERE, "..", "output", "assets")
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_SriLanka_Banking_Security.pptx")
def A(name): return os.path.join(AST, name)

# ---- palette ------------------------------------------------------
NAVY     = RGBColor(0x11, 0x20, 0x6D)
NAVY_DK  = RGBColor(0x0A, 0x14, 0x4A)
BLACK    = RGBColor(0x00, 0x00, 0x00)
PRIMARY  = RGBColor(0x00, 0x46, 0xFF)
SECOND   = RGBColor(0x64, 0x64, 0xFF)
PURPLE   = RGBColor(0x4D, 0x4D, 0xD9)
RED      = RGBColor(0xC8, 0x00, 0x19)
GREEN    = RGBColor(0x16, 0xA5, 0x5C)
GREEN_DK = RGBColor(0x0B, 0x7A, 0x42)
GREEN_LT = RGBColor(0xE7, 0xF6, 0xEE)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
INK      = RGBColor(0x1B, 0x22, 0x3B)
MUTE     = RGBColor(0x5A, 0x63, 0x7D)
GREY_BD  = RGBColor(0xC4, 0xCC, 0xDE)
LAV      = RGBColor(0xEC, 0xEC, 0xFB)
NAVY_TXT = RGBColor(0xB8, 0xC4, 0xE8)
FONT     = "Space Grotesk"
ICF      = "Segoe MDL2 Assets"

IC = {
 'lock':0xE72E,'shield':0xE83D,'cloud':0xE753,'globe':0xE774,'pulse':0xE9D9,
 'doc':0xE8A5,'person':0xE7EE,'gear':0xE713,'gears':0xE9F5,'key':0xE8D7,
 'finger':0xE928,'bolt':0xE945,'warn':0xE7BA,'copy':0xE8C8,'check':0xE930,
 'flag':0xE7C1,'pie':0xEB05,'bulb':0xEB50,'server':0xE968,'devices':0xE977,
 'chip':0xE964,'swap':0xE8AB,'search':0xE721,'wrench':0xE90F,'clock':0xE81C,
 'star':0xE734,'books':0xE8F1,'wifi':0xEC3F,'cert':0xEB95,'eye':0xE890,
 'briefcase':0xE821,'list':0xE71D,'rocket':0xE7A7,
}
def G(name): return chr(IC[name])

# ---- geometry -----------------------------------------------------
CX, CW = 0.40, 9.20
RCOLX  = 4.98            # right-column start for split slides

# ===================================================================
def _set_title(slide, text, color=None):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0:
            ph.text_frame.paragraphs[0].text = text
            for r in ph.text_frame.paragraphs[0].runs:
                r.font.name = FONT
                if color is not None: r.font.color.rgb = color
            return ph

def _blank_footer(slide):
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx in (10, 11):
            ph.text_frame.paragraphs[0].text = ""

def box(slide, x, y, w, h, text="", size=12, color=INK, bold=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, fill=None, line=None,
        line_w=0.75, shape=MSO_SHAPE.RECTANGLE, radius=None, italic=False,
        wrap=True, ml=0.08, mr=0.08, mt=0.04, mb=0.04, font=FONT):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None: sp.fill.background()
    else: sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    if radius is not None:
        try: sp.adjustments[0] = radius
        except Exception: pass
    tf = sp.text_frame; tf.word_wrap = wrap
    tf.margin_left=Inches(ml); tf.margin_right=Inches(mr)
    tf.margin_top=Inches(mt); tf.margin_bottom=Inches(mb)
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align
    if text:
        r = p.add_run(); r.text = text
        r.font.name=font; r.font.size=Pt(size); r.font.bold=bold; r.font.italic=italic
        r.font.color.rgb = color
    return sp

def para(shape, text, size=12, color=INK, bold=False, align=PP_ALIGN.LEFT,
         italic=False, space_before=0, space_after=4, first=False):
    tf = shape.text_frame
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align; p.space_before = Pt(space_before); p.space_after = Pt(space_after)
    r = p.add_run(); r.text = text
    r.font.name=FONT; r.font.size=Pt(size); r.font.bold=bold; r.font.italic=italic
    r.font.color.rgb = color
    return p

def icon(slide, x, y, size, glyph, color=WHITE, bg=PRIMARY, radius=0.26, fsz=None):
    sp = box(slide, x, y, size, size, fill=bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
             radius=radius, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0, mr=0, mt=0, mb=0)
    p = sp.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = glyph
    r.font.name = ICF; r.font.size = Pt(fsz or size*42); r.font.color.rgb = color
    return sp

def image_fit(slide, path, x, y, w, h, caption=None, frame=GREY_BD, panel=None, capcolor=None):
    im = PILImage.open(path); ar = im.size[0]/im.size[1]
    if w/h > ar: dh=h; dw=h*ar
    else: dw=w; dh=w/ar
    dx=x+(w-dw)/2; dy=y+(h-dh)/2
    if panel is not None:
        box(slide, x, y, w, h, fill=panel, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
    pic = slide.shapes.add_picture(path, Inches(dx), Inches(dy), Inches(dw), Inches(dh))
    if frame is not None: pic.line.color.rgb=frame; pic.line.width=Pt(1.0)
    pic.shadow.inherit = False
    if caption:
        box(slide, x, y+h+0.02, w, 0.26, text=caption, size=8.5, color=capcolor or MUTE,
            italic=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return pic

def card(slide, x, y, w, h, heading, body, accent=PRIMARY, hsize=12.5, bsize=10.2,
         ic=None):
    box(slide, x, y, w, h, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(slide, x, y, w, 0.09, fill=accent, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    if ic:
        icon(slide, x+0.16, y+0.2, 0.42, G(ic), bg=accent)
        box(slide, x+0.66, y+0.16, w-0.8, 0.52, text=heading, size=hsize, color=NAVY,
            bold=True, anchor=MSO_ANCHOR.MIDDLE)
        box(slide, x+0.18, y+0.76, w-0.36, h-0.86, text=body, size=bsize, color=MUTE,
            anchor=MSO_ANCHOR.TOP)
    else:
        box(slide, x+0.16, y+0.18, w-0.32, 0.4, text=heading, size=hsize, color=NAVY, bold=True)
        box(slide, x+0.16, y+0.6, w-0.32, h-0.72, text=body, size=bsize, color=MUTE)

def stat(slide, x, y, w, number, label, color=PRIMARY, nsize=25, lsize=9.5, h=1.15):
    b = box(slide, x, y, w, h, fill=WHITE, line=GREY_BD, line_w=1.0,
            shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.09, anchor=MSO_ANCHOR.MIDDLE)
    para(b, number, size=nsize, color=color, bold=True, align=PP_ALIGN.CENTER, first=True, space_after=1)
    para(b, label, size=lsize, color=MUTE, align=PP_ALIGN.CENTER, space_after=0)
    return b

def pill(slide, x, y, w, h, text, fill=PRIMARY, tcolor=WHITE, size=10):
    return box(slide, x, y, w, h, text=text, size=size, color=tcolor, bold=True,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=fill,
               shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5, wrap=False)

def eyebrow(slide, text, x=CX, y=0.88, color=PRIMARY):
    return box(slide, x, y, 7.0, 0.26, text=text.upper(), size=10.5, color=color,
               bold=True, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

def footer_note(slide, text, color=MUTE):
    return box(slide, CX, 5.18, CW, 0.28, text=text, size=8.5, color=color,
               italic=True, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

def list_row(slide, x, y, w, glyph, head, sub, accent=PRIMARY, h=0.66, hsize=11.5, ssize=9.3):
    icon(slide, x, y+0.02, 0.4, glyph, bg=accent)
    box(slide, x+0.54, y-0.04, w-0.54, 0.3, text=head, size=hsize, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.BOTTOM, mb=0)
    box(slide, x+0.54, y+0.26, w-0.54, h-0.24, text=sub, size=ssize, color=MUTE,
        anchor=MSO_ANCHOR.TOP, mt=0)

def bullets(slide, x, y, w, h, items, size=11, color=INK, marker="▸", mcolor=None, gap=5):
    mcolor = mcolor or PRIMARY
    sp = box(slide, x, y, w, h, wrap=True, anchor=MSO_ANCHOR.TOP, ml=0.02, mr=0.04, mt=0.02)
    tf = sp.text_frame
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        rm=p.add_run(); rm.text=marker+"  "; rm.font.name=FONT; rm.font.size=Pt(size)
        rm.font.bold=True; rm.font.color.rgb=mcolor
        if isinstance(it, tuple):
            r1=p.add_run(); r1.text=it[0]; r1.font.name=FONT; r1.font.size=Pt(size); r1.font.bold=True; r1.font.color.rgb=color
            r2=p.add_run(); r2.text=it[1]; r2.font.name=FONT; r2.font.size=Pt(size); r2.font.color.rgb=color
        else:
            r=p.add_run(); r.text=it; r.font.name=FONT; r.font.size=Pt(size); r.font.color.rgb=color
    return sp

# ===================================================================
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
    s = prs.slides.add_slide(L_STD); _set_title(s, title); _blank_footer(s)
    if kicker: eyebrow(s, kicker)
    return s

# ------------------------------------------------------------------ 1. COVER
s = prs.slides.add_slide(L_DIV); _blank_footer(s)
box(s, 0.7, 1.30, 8.6, 0.34, text="ACCUKNOX  ×  VSONE", size=13, color=SECOND, bold=True)
box(s, 0.66, 1.66, 8.7, 1.7, text="Zero Trust Security for\nSri Lanka's Banks",
    size=37, color=WHITE, bold=True, anchor=MSO_ANCHOR.TOP)
box(s, 0.7, 3.34, 8.4, 0.7,
    text="One platform to secure code, cloud, workloads, APIs and AI, and to stay audit-ready for CBSL, PDPA and PCI DSS.",
    size=13.5, color=NAVY_TXT)
box(s, 0.7, 4.28, 0.14, 0.62, fill=PRIMARY)
box(s, 0.96, 4.28, 8.2, 0.62,
    text="Delivered in Sri Lanka by VSONE, AccuKnox's in-country partner for banking, "
         "telecom and enterprise.\nBanking Security Briefing  ·  2026",
    size=10.5, color=NAVY_TXT, anchor=MSO_ANCHOR.MIDDLE)

# ------------------------------------------------------------------ 2. PRESSURE
s = content("Four forces are squeezing Sri Lanka's banks at once", "The moment")
q = [
 ("globe","Digital banking has exploded", PRIMARY,
  "LankaPay, CEFTS and mobile wallets put the sector online. Every new channel, app and API is a new way in."),
 ("cert","The regulator has raised the bar", NAVY,
  "CBSL Direction No. 16 of 2021 and the PDPA put technology risk on the board, with a senior CISO and a 24x7 SOC."),
 ("warn","Attackers moved to run-time", RED,
  "The 2025 Cargills Bank ransomware breach hit a live environment. Advanced attacks execute in production."),
 ("person","Budgets and talent are thin", GREEN_DK,
  "After the 2022 crisis, teams do more with less, fewer people, tighter forex, a stack of disconnected tools."),
]
cw=(CW-0.3)/2; ch=1.66
for i,(g,hd,ac,bd) in enumerate(q):
    card(s, CX+(i%2)*(cw+0.3), 1.30+(i//2)*(ch+0.22), cw, ch, hd, bd, accent=ac,
         hsize=13, bsize=10.8, ic=g)
footer_note(s, "Sourced to CBSL, Sri Lanka's PDPA No. 9 of 2022, and regional banking-sector threat reporting.")

# ------------------------------------------------------------------ 3. THREAT LANDSCAPE
s = content("The threat landscape is now a run-time problem", "Why it matters")
stats = [("4,347","cyber incidents logged by SLCERT in\n2024, up from 596 in 2019", RED),
         ("1.9 TB","of bank data exfiltrated in the 2025\nCargills Bank ransomware breach", NAVY),
         ("87%","of hybrid environments carry blind\nspots public-cloud tools never reach", PRIMARY)]
sw=(CW-0.6)/3
for i,(n,l,c) in enumerate(stats):
    stat(s, CX+i*(sw+0.3), 1.22, sw, n, l, color=c, nsize=24, h=1.12)
box(s, CX, 2.62, 4.3, 0.32, text="What hides in the blind spots", size=12.5, color=NAVY, bold=True)
bullets(s, CX, 3.0, 4.4, 1.9, [
 ("Unpatched on-prem servers ","running core banking, outside cloud tools."),
 ("Containers with no run-time rules ","and shadow workloads."),
 ("Over-permissioned identities ","and secrets sprawled everywhere."),
 ("Shadow AI ","moving customer data before any guardrail fires."),
], size=10.5, gap=8)
image_fit(s, A("attack-path.png"), RCOLX, 2.66, 4.62, 2.2, panel=BLACK, frame=NAVY,
          caption="AccuKnox security graph: real attack paths surfaced across cloud, K8s and VMs.")

# ------------------------------------------------------------------ 4. REGULATORY SQUEEZE
s = content("The compliance mandates a Sri Lankan bank must answer to", "The regulatory squeeze")
regs = [
 ("cert","CBSL Direction No. 16 of 2021", NAVY,
  "Technology Risk & Resilience: board and BIRMC accountability, a senior CISO, a 24x7 SOC, quarterly VAs, annual pen tests, RTO under 4 hours."),
 ("shield","CBSL Baseline Security Standard", PRIMARY,
  "The Central Bank's ISO 27000-based control baseline for information-security management across licensed banks."),
 ("lock","PDPA No. 9 of 2022", PURPLE,
  "Data Protection Officers, breach notification to the DPA, and penalties up to LKR 10 million for a first violation."),
 ("warn","Incident reporting", RED,
  "CBSL's May 2025 IT & cybersecurity incident circular, plus FinCSIRT and SLCERT coordinated disclosure."),
 ("key","PCI DSS 4.0 & SWIFT CSP", GREEN_DK,
  "Continuous card-data control validation and annual attestation for cross-border payment infrastructure."),
 ("eye","AML / CFT (FIU)", SECOND,
  "Customer due diligence, suspicious-transaction reporting and six-year record retention under the FTRA."),
]
cw3=(CW-0.6)/3; ch3=1.66
for i,(g,hd,ac,bd) in enumerate(regs):
    card(s, CX+(i%3)*(cw3+0.3), 1.28+(i//3)*(ch3+0.2), cw3, ch3, hd, bd, accent=ac,
         hsize=11.5, bsize=9.5, ic=g)
footer_note(s, "Six overlapping regimes, each demanding continuous evidence. AccuKnox maps one control set to all of them.")

# ------------------------------------------------------------------ 5. CISO PAIN
s = content("What that leaves the CISO carrying", "The CISO's reality")
pains = [
 ("gears","Tool sprawl","Separate products for cloud, containers, code, APIs and identity, none of them talking."),
 ("warn","Alert fatigue","Thousands of findings, no context on which are actually exploitable in production."),
 ("copy","Stacked mandates","Direction 16, the Baseline Standard, PDPA and AML rules each demand fresh manual evidence."),
 ("person","Talent drain","Too few certified engineers, and the crisis pushed skilled staff to jobs overseas."),
 ("swap","On-prem + cloud split","Core banking on-prem and air-gapped, new services in cloud, two different playbooks."),
 ("bolt","Zero-day exposure","Build-time scanning misses run-time attacks; the team finds out after the breach."),
]
for i,(g,hd,bd) in enumerate(pains):
    card(s, CX+(i%3)*(cw3+0.3), 1.28+(i//3)*(ch3+0.2), cw3, ch3, hd, bd, accent=RED,
         hsize=12.5, bsize=9.8, ic=g)
footer_note(s, "The result: high cost, thin coverage, and a compliance posture that is hard to prove on demand.")

# ------------------------------------------------------------------ 6. DIVIDER
s = prs.slides.add_slide(L_DIV); _set_title(s, "Meet AccuKnox", color=WHITE); _blank_footer(s)
box(s, 2.04, 3.05, 5.93, 0.9,
    text="AI-powered Zero Trust CNAPP  ·  Secure Code to Cognition  ·  brought to Sri Lanka by VSONE",
    size=13.5, color=NAVY_TXT, align=PP_ALIGN.CENTER)

# ------------------------------------------------------------------ 7. OVERVIEW
s = content("One Zero Trust platform, from code to cloud to AI", "What AccuKnox is")
box(s, CX, 1.2, CW, 0.6,
    text="Founded in 2020 with Stanford Research Institute. AccuKnox secures public, private, "
         "hybrid and air-gapped clouds, plus VMs, Kubernetes, APIs, edge and AI/LLM assets, on one control plane.",
    size=11, color=INK)
feat = [("bolt","Agentless onboarding","Connect and see risk in minutes, no heavy agents.", PRIMARY),
        ("shield","Run-time, inline defense","eBPF and KubeArmor stop zero-days in production.", RED),
        ("cloud","Deploy anywhere","SaaS, your cloud, on-prem or fully air-gapped.", PURPLE),
        ("cert","GRC included","35+ compliance frameworks and audit trails built in.", GREEN_DK)]
for i,(g,hd,sub,ac) in enumerate(feat):
    list_row(s, CX, 1.98+i*0.72, 4.4, G(g), hd, sub, accent=ac)
image_fit(s, A("policies.png"), RCOLX, 1.96, 4.62, 2.36, frame=GREY_BD,
          caption="AccuKnox console: unified policies across cloud, workloads and clusters.")
box(s, CX, 4.74, CW, 0.42, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.16,
    text="In Sri Lanka, delivered and supported locally by VSONE, with AccuKnox pre-sales engineering behind every deployment.",
    size=10, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ------------------------------------------------------------------ 8. CONSOLIDATION
s = content("One platform replaces a shelf of point tools", "Consolidate and save")
box(s, CX, 1.2, 4.4, 0.8,
    text="AccuKnox brings 12+ security domains under one console, cutting licences, integration "
         "work and the people-cost of running disconnected tools.", size=11, color=INK)
kpis=[("12+","security domains",PRIMARY),(">50%","cost saving",GREEN_DK),
      ("3→1","vendors",NAVY),("Minutes","to first risk",PURPLE)]
kw=(4.4-0.2)/2
for i,(n,l,c) in enumerate(kpis):
    stat(s, CX+(i%2)*(kw+0.2), 2.06+(i//2)*(1.12+0.16), kw, n, l, color=c, nsize=22, h=1.12)
box(s, CX, 4.5, 4.4, 0.5, text="Replaces Wiz, Prisma, Orca, Aqua, Snyk, Qualys, SentinelOne and more.",
    size=9.5, color=MUTE, italic=True)
image_fit(s, A("replaces-wheel.png"), RCOLX, 1.12, 4.62, 3.86, panel=BLACK, frame=NAVY,
          caption="12 security domains, one Gen-AI powered CNAPP.")

# ------------------------------------------------------------------ 9. ARCHITECTURE
s = content("How it works: one control plane over everything", "Platform architecture")
box(s, CX, 1.16, 3.35, 0.6, text="Secure the full lifecycle, cloud to on-prem to edge:",
    size=11.5, color=INK, bold=True)
arch=[("swap","Agentless collectors","On clusters, VMs and registries stream telemetry to AccuKnox.", PRIMARY),
      ("gear","One control plane","SaaS or on-prem correlates risk and pushes policy back inline.", PURPLE),
      ("pulse","Feeds your stack","SIEM (Splunk), email, Slack alerts, plus CI/CD registry scanning.", GREEN_DK)]
for i,(g,hd,sub,ac) in enumerate(arch):
    list_row(s, CX, 1.86+i*0.98, 3.4, G(g), hd, sub, accent=ac, h=0.9, ssize=9.5)
image_fit(s, A("onprem-arch.png"), 3.95, 1.02, 5.65, 4.0, frame=GREY_BD)

# ------------------------------------------------------------------ 10. RUNTIME
s = content("The difference: stop zero-days at run-time, inline", "Unique differentiator")
box(s, CX, 1.18, CW, 0.44,
    text="Most tools tell you about an attack after it runs. AccuKnox watches behaviour in production "
         "and enforces inline, so a zero-day is blocked as it happens.", size=11, color=INK)
steps=[("eye","1.  Observe","Learn each workload's normal process, file, network and API behaviour."),
       ("shield","2.  Enforce","Block anything off-baseline inline, at the kernel, during the attack."),
       ("wrench","3.  Auto-policy","Generate hardening policy automatically from observed behaviour.")]
for i,(g,hd,sub) in enumerate(steps):
    list_row(s, CX, 1.78+i*0.72, 4.4, G(g), hd, sub, accent=NAVY, h=0.66)
image_fit(s, A("runtime-events.png"), RCOLX, 1.8, 4.62, 1.95, frame=GREY_BD,
          caption="Run-time events and enforcement, live across the estate.")
box(s, CX, 4.16, CW, 0.86, fill=GREEN_LT, line=GREEN, line_w=1.25,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
icon(s, CX+0.16, 4.28, 0.4, G('check'), bg=GREEN_DK)
box(s, CX+0.68, 4.22, CW-0.9, 0.3, text="Why a bank should care", size=12, color=GREEN_DK, bold=True, anchor=MSO_ANCHOR.BOTTOM)
box(s, CX+0.68, 4.52, CW-0.9, 0.44,
    text="Ransomware is contained before it touches core banking. Proven on US DoD 5G and Zero Trust satellite security programs.",
    size=10, color=INK, anchor=MSO_ANCHOR.TOP)

# ------------------------------------------------------------------ 11. COMPLIANCE MAPPING
s = content("Compliance and GRC, mapped to your mandates", "Audit-ready by design")
box(s, CX, 1.18, CW, 0.42,
    text="One set of controls becomes continuous, audit-ready evidence for every framework a Sri Lankan "
         "bank reports against, GRC included with the platform.", size=11, color=INK)
rows=[("Mandate","How AccuKnox helps"),
 ("CBSL Direction 16 of 2021","Continuous posture, quarterly VA & pen-test evidence"),
 ("Baseline Standard / ISO 27001","Pre-built templates, auto-mapped findings, reports"),
 ("PDPA No. 9 of 2022","Data discovery (DSPM), residency-aware deployment"),
 ("PCI DSS 4.0 & SWIFT CSP","Config, workload and access controls validated"),
 ("Incident reporting (FinCSIRT)","Real-time detection, forensics and audit trail")]
tx,ty,tw = CX, 1.74, 5.0
gt = s.shapes.add_table(len(rows),2,Inches(tx),Inches(ty),Inches(tw),Inches(2.95)).table
gt.first_row=False; gt.horz_banding=False
gt.columns[0].width=Inches(2.28); gt.columns[1].width=Inches(tw-2.28)
for ri,row in enumerate(rows):
    for ci,val in enumerate(row):
        c=gt.cell(ri,ci)
        c.margin_left=Inches(0.08); c.margin_right=Inches(0.05)
        c.margin_top=Inches(0.02); c.margin_bottom=Inches(0.02); c.vertical_anchor=MSO_ANCHOR.MIDDLE
        if ri==0: c.fill.solid(); c.fill.fore_color.rgb=NAVY
        elif ci==0: c.fill.solid(); c.fill.fore_color.rgb=LAV
        else: c.fill.solid(); c.fill.fore_color.rgb=WHITE
        p=c.text_frame.paragraphs[0]; r=p.add_run(); r.text=val; r.font.name=FONT
        r.font.size=Pt(9.5 if ri==0 else 8.6); r.font.bold=(ri==0 or ci==0)
        r.font.color.rgb=WHITE if ri==0 else NAVY
image_fit(s, A("compliance-dashboard.png"), 5.62, 1.74, 3.98, 2.6, frame=GREY_BD,
          caption="Live compliance scores: ISO 27001, ISO 42001, EU AI Act, MITRE ATLAS and more.")
footer_note(s, "One control set, evidence for every regime, so audit prep stops being a manual fire drill.")

# ------------------------------------------------------------------ 12. CLOUD & WORKLOAD
s = content("Cloud and workload security", "Platform coverage  ·  1 of 3")
mods=[("cloud","CSPM","Cloud posture: misconfig, attack-path & security graph."),
      ("server","CWPP","Workload protection: eBPF run-time for VMs & containers."),
      ("gears","KSPM","Kubernetes posture: CIS benchmarks, cluster hardening."),
      ("finger","CIEM","Cloud identities: permissions graph, over-provision detection."),
      ("warn","CDR","Cloud detection & response across cloud, VMs and K8s."),
      ("pie","SIEM","Events: high-volume ingestion, code-to-cloud correlation.")]
for i,(g,hd,sub) in enumerate(mods):
    list_row(s, CX, 1.28+i*0.63, 4.5, G(g), hd, sub, accent=PRIMARY, h=0.58, ssize=9.2)
image_fit(s, A("iac-findings.png"), RCOLX, 1.24, 4.62, 1.72, frame=GREY_BD, caption="IaC & misconfiguration findings")
image_fit(s, A("api-endpoints.png"), RCOLX, 3.36, 4.62, 1.72, frame=GREY_BD, caption="Cloud asset & API inventory")

# ------------------------------------------------------------------ 13. APP / API / DATA
s = content("Application, API and data security", "Platform coverage  ·  2 of 3")
mods=[("doc","ASPM","App posture: SAST, SCA, AI-assisted triage & prioritisation."),
      ("search","DAST","Dynamic testing of web UI and APIs at run-time."),
      ("swap","API Security","Discover shadow, orphan & zombie APIs; run-time control."),
      ("books","SBOM","Live SBOM, dependency drift, licence & vuln mapping."),
      ("key","Secrets","Shift-left scanning, Vault hardening, no hardcoded creds."),
      ("eye","DSPM","Discover & classify sensitive data; flag risky access.")]
for i,(g,hd,sub) in enumerate(mods):
    list_row(s, CX, 1.28+i*0.63, 4.5, G(g), hd, sub, accent=PURPLE, h=0.58, ssize=9.2)
image_fit(s, A("secret-scan.png"), RCOLX, 1.24, 4.62, 1.72, frame=GREY_BD, caption="Secret-scan findings & remediation")
image_fit(s, A("vuln-bubbles.png"), RCOLX, 3.36, 4.62, 1.72, frame=GREY_BD, caption="Vulnerability prioritisation by severity")

# ------------------------------------------------------------------ 14. AI SECURITY
s = content("AI security for the next wave of banking", "Platform coverage  ·  3 of 3")
box(s, CX, 1.18, 4.35, 0.8,
    text="As banks roll out chatbots, copilots and agentic workflows, AccuKnox governs and defends AI "
         "the same way it does cloud and code.", size=11, color=INK)
ai=[("chip","AI-SPM","Discover LLMs, ML & agentic apps; score their risk.", PRIMARY),
    ("shield","Prompt Firewall","Inline guardrails vs. prompt injection & data leaks.", RED),
    ("warn","AI Red Teaming","Automated adversarial testing vs. OWASP LLM Top 10.", PURPLE),
    ("eye","AI-DR & DSPM","Detect AI threats, stop data leaking to public AI.", GREEN_DK)]
for i,(g,hd,sub,ac) in enumerate(ai):
    list_row(s, CX, 2.0+i*0.62, 4.35, G(g), hd, sub, accent=ac, h=0.58, ssize=9.2)
image_fit(s, A("ai-modules.png"), 4.95, 1.16, 4.65, 3.05, panel=BLACK, frame=NAVY)
box(s, CX, 4.62, CW, 0.44, fill=GREEN_LT, line=GREEN, line_w=1.0,
    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.14,
    text="Recognised as Agentic AI Security Startup of the Year, 2025.",
    size=10.5, color=GREEN_DK, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ------------------------------------------------------------------ 15. DEPLOYMENT
s = content("Deployment models built for a regulated bank", "Data residency & control")
box(s, CX, 1.18, CW, 0.46,
    text="Sensitive banking data can stay inside your walls. AccuKnox runs the same platform wherever "
         "your data-residency and PDPA obligations require it to live.", size=11, color=INK)
dep=[("cloud","AccuKnox SaaS","Fastest to value, fully managed, for lower-sensitivity workloads.", PRIMARY),
     ("globe","Your cloud / private","Runs inside your AWS, Azure, GCP or Oracle tenant, your keys.", SECOND),
     ("server","On-prem","Deploy on your own VMs and bare metal for core banking.", PURPLE),
     ("shield","Fully air-gapped","No public-internet dependency, for the most sensitive systems.", NAVY)]
sw=(CW-0.9)/4
for i,(g,hd,bd,c) in enumerate(dep):
    x=CX+i*(sw+0.3)
    box(s, x, 1.86, sw, 0.62, fill=c, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    icon(s, x+0.14, 1.97, 0.4, G(g), bg=WHITE, color=c)
    box(s, x+0.6, 1.86, sw-0.66, 0.62, text=hd, size=11, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x, 2.56, sw, 1.16, text=bd, size=9.8, color=MUTE, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, anchor=MSO_ANCHOR.TOP, ml=0.1, mr=0.1, mt=0.08)
box(s, CX, 3.98, CW, 0.92, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
box(s, CX+0.18, 4.08, CW-0.4, 0.34, text="Same product, same policies, everywhere", size=12.5, color=WHITE, bold=True)
box(s, CX+0.2, 4.44, CW-0.45, 0.42,
    text="Secure cloud-native services and legacy on-prem core banking from one console, without shipping "
         "sensitive data outside the country or your control.", size=10.5, color=NAVY_TXT)

# ------------------------------------------------------------------ 16. WHY ACCUKNOX
s = content("Why AccuKnox over point vendors", "The differentiators")
diff=[("bolt","EFFORTLESS","Agentless onboarding, protect in minutes."),
      ("shield","EXTENSIVE","Broadest AppSec, CloudSec, API & AI security in one."),
      ("cloud","EFFICIENT","Runs on every cloud, on-prem and air-gapped."),
      ("check","EFFECTIVE","Run-time, inline mitigation of zero-day attacks."),
      ("bulb","INNOVATIVE","SRI R&D partnership, 10+ Zero Trust patents."),
      ("person","PARTNER-FIRST","150+ partners; in Sri Lanka, VSONE.")]
for i,(g,hd,bd) in enumerate(diff):
    card(s, CX+(i%3)*(cw3+0.3), 1.28+(i//3)*(0.98+0.16), cw3, 0.98, hd, bd, accent=PRIMARY,
         hsize=11.5, bsize=9.4, ic=g)
box(s, CX, 3.5, CW, 0.32, text="Run-time, inline security across the CNAPP stack", size=12, color=NAVY, bold=True)
comp=[("AccuKnox",True),("Wiz",False),("Palo Alto",False),("CrowdStrike",False),("Sysdig",False),("Upwind",False)]
bw=(CW-0.1*5)/6
for i,(name,yes) in enumerate(comp):
    x=CX+i*(bw+0.1)
    box(s, x, 3.86, bw, 0.62, fill=(GREEN_LT if yes else WHITE), line=(GREEN if yes else GREY_BD),
        line_w=1.25 if yes else 1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    box(s, x, 3.9, bw, 0.28, text=name, size=9.5, color=(GREEN_DK if yes else NAVY), bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    box(s, x, 4.16, bw, 0.24, text=("✓ Yes" if yes else "Limited / No"), size=8.5,
        color=(GREEN_DK if yes else MUTE), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
footer_note(s, "AccuKnox is the only vendor in the set with full private-cloud and air-gapped run-time, inline security.")

# ------------------------------------------------------------------ 17. PROOF
s = content("Proof the market already trusts", "Traction & recognition")
sw=(CW-0.9)/4
for i,(n,l,c) in enumerate([("$1.5M","US DoD 5G security\nR&D contract",NAVY),
                            ("$500K","Zero Trust satellite\nsecurity contract",PRIMARY),
                            ("$4.6M","funding for the\nZero Trust platform",PURPLE),
                            ("150+","partners, 10+\nZero Trust patents",GREEN_DK)]):
    stat(s, CX+i*(sw+0.3), 1.24, sw, n, l, color=c, nsize=21, h=1.1)
# quote (left)
box(s, CX, 2.52, 5.3, 1.55, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, CX+0.18, 2.62, 5.0, 1.05,
    text="“We evaluated best-in-class vendors and selected AccuKnox for its breadth, ease of deployment, "
         "and real-time security against zero-day attacks.”", size=10.8, color=INK, italic=True, anchor=MSO_ANCHOR.MIDDLE)
box(s, CX+0.18, 3.72, 5.0, 0.28, text="David Billeter, Cybersecurity Leader, Sonesta International Hotels",
    size=9, color=PRIMARY, bold=True)
# proof images (right)
image_fit(s, A("omdia-report.png"), 5.9, 2.52, 1.78, 1.55, frame=GREY_BD, caption="Omdia CNAPP report")
image_fit(s, A("patent.png"), 7.82, 2.52, 1.78, 1.55, frame=GREY_BD, caption="10+ US patents granted")
bullets(s, CX, 4.24, CW, 0.8, [
 ("Aligned to Gartner's CNAPP Market Guide ","and OWASP Cloud-Native Top 10."),
 ("Trusted by regulated enterprises ","including IDT Telecom and SupportLogic (45% less engineering overhead)."),
], size=10, gap=4)

# ------------------------------------------------------------------ 18. CTA
s = prs.slides.add_slide(L_DIV); _blank_footer(s)
box(s, 0.7, 1.36, 8.6, 0.34, text="ACCUKNOX  ×  VSONE", size=13, color=SECOND, bold=True)
box(s, 0.66, 1.72, 8.7, 1.0, text="Let's secure your bank,\nfrom first commit to live production.",
    size=27, color=WHITE, bold=True, anchor=MSO_ANCHOR.TOP)
box(s, 0.7, 2.9, 8.5, 0.7,
    text="Start with a scoped proof of value on your own environment. See AccuKnox find real risk in your "
         "cloud, workloads and code within days, not months.", size=12.5, color=NAVY_TXT)
steps=[("search","Discovery call","Map your estate, mandates and priorities with VSONE and AccuKnox."),
       ("bolt","Proof of value","Agentless onboarding, first findings in your environment fast."),
       ("cloud","Roll out","Phase across cloud, on-prem and air-gapped with local support.")]
sw=(8.6-0.4)/3
for i,(g,hd,bd) in enumerate(steps):
    x=0.7+i*(sw+0.2)
    icon(s, x, 3.72, 0.46, G(g), bg=PRIMARY, color=WHITE)
    box(s, x+0.58, 3.7, sw-0.58, 0.34, text=hd, size=12, color=WHITE, bold=True)
    box(s, x+0.58, 4.02, sw-0.58, 0.72, text=bd, size=9.5, color=NAVY_TXT, anchor=MSO_ANCHOR.TOP)
box(s, 0.7, 4.94, 8.6, 0.34,
    text="VSONE (Colombo)  ·  AccuKnox pre-sales engineering  ·  support@accuknox.com  ·  accuknox.com",
    size=10, color=SECOND, bold=True, anchor=MSO_ANCHOR.MIDDLE)

# ===================================================================
prs.save(OUT)
print("Saved:", OUT, "slides:", len(prs.slides._sldIdLst))
