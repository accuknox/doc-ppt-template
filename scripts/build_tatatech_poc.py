# -*- coding: utf-8 -*-
"""
Tata Technologies POC deck, CSPM and CWPP, two-week scoped plan.

Built on the AccuKnox master template (10 x 5.625 in). Co-branded on the cover
with the Tata Technologies wordmark on a white pill, the pattern already used by
build_rakuten_status_report.py.

Every technical fact comes from an opened AccuKnox help doc, listed here so a
reviewer can check it:

  docs/how-to/cspm-prereq-aws.md          IAM user, ReadOnlyAccess, SecurityAudit,
                                          Bedrock and SageMaker inline policy
  docs/how-to/cspm-prereq-azure.md        App registration, Reader,
                                          Log Analytics Reader, Directory.Read.All
  docs/how-to/terraform-aws-onboarding.md    what terraform apply creates on AWS
  docs/how-to/terraform-azure-onboarding.md  what terraform apply creates on Azure
  docs/getting-started/cwpp-prereq.md     agent list, resource usage, ports
  docs/how-to/vm-onboard-deboard-systemd.md  knoxctl onboard and deboard, ports
  docs/how-to/vm-security/agent-based/linux.md  omni scanner, S3 URL, CPU and
                                          memory caps, malware scan default,
                                          omni-uninstall.sh
  docs/how-to/cluster-onboarding.md       helm chart, KSPM job toggles
  docs/how-to/cluster-offboarding.md      helm uninstall commands
  docs/how-to/cloud-offboarding.md        cloud account deletion
  docs/support-matrix/compliance-matrix.md   CIS, ISO 27001, SOC 2 Type II
  docs/integrations/webhook-integration.md   webhook alert delivery and payload

Excluded on purpose, per the client scope call: CDR, JIRA, two-way ticket sync,
HIPAA, GuardDuty, VPC.

Build:   py -3.11 scripts/build_tatatech_poc.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_TataTech_CSPM_CWPP_POC.pptx -Out output/render/tatatech
"""
import os, shutil, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image as PILImage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import *                      # noqa: F401,F403  palette + primitives
from _akdeck import _ph, _move_ph, _fill_ph

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "PPT Template.pptx")
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_TataTech_CSPM_CWPP_POC.pptx")
TTL  = os.path.join(HERE, "..", "assets", "partner-logos", "tata-technologies.png")
IMG  = os.path.join(HERE, "..", "assets", "deck-images", "tatatech")
def img(n): return os.path.join(IMG, n)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_COVER, L_CLOSE, L_STD = prs.slide_layouts[0], prs.slide_layouts[1], prs.slide_layouts[4]

xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try:
        prs.part.drop_rel(sid.get(qn("r:id")))
    except Exception:
        pass
    xml_slides.remove(sid)

DOCS = "https://help.accuknox.com/"


# =================================================================== helpers
def std(title, kicker, lede=None, lede_h=0.30):
    """A content slide on the navy-band layout."""
    s = prs.slides.add_slide(L_STD)
    set_title(s, title)
    blank_footer(s)
    eyebrow(s, kicker, y=0.84, w=6.4)
    if lede:
        box(s, CX, 1.12, CW, lede_h, text=lede, size=9.8, color=MUTE,
            anchor=MSO_ANCHOR.MIDDLE)
    return s


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
        fill.append(clr)
        ln.append(fill)
        tcPr.insert(idx, ln)
        idx += 1


def table_grid(t, color=GREY_BD):
    for ri in range(1, len(t.rows)):
        for ci in range(len(t.columns)):
            cell_border(t.cell(ri, ci), "LRTB", color=color)


def set_rows(t, head_h, row_h, pad=0.03):
    """PowerPoint treats a row height as a minimum, so this holds only while a
    cell stays on one line. Trimming the vertical padding buys back the space a
    long table needs on a 5.625 in canvas."""
    for ri, row in enumerate(t.rows):
        row.height = Inches(head_h if ri == 0 else row_h)
        for c in row.cells:
            c.margin_top = Inches(pad)
            c.margin_bottom = Inches(pad)


def center_cols(t, cols):
    for ci in cols:
        for ri in range(1, len(t.rows)):
            for p in t.cell(ri, ci).text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER


def grid(s, x, y, w, h, rows, colw, head_h=0.30, row_h=0.30, bsize=8.0,
         hsize=8.4, pad=0.03, firstcol_fill=LAV, center=()):
    t = table(s, x, y, w, h, rows, colw=colw, hsize=hsize, bsize=bsize,
              firstcol_fill=firstcol_fill)
    set_rows(t, head_h, row_h, pad)
    table_grid(t)
    if center:
        center_cols(t, list(center))
    return t


def link(s, x, y, w, h, label, url, size=8.2, color=PRIMARY, bold=False):
    """A clickable help-doc link. python-pptx sets the address on the run."""
    sp = box(s, x, y, w, h, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0, mt=0, mb=0,
             wrap=False)
    p = sp.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = label
    r.font.name = FONT
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.hyperlink.address = url
    return sp


def link_strip(s, y, items, size=8.2, h=0.24, gap=0.30, x=CX, marker="↗  "):
    """A left-aligned row of clickable doc links."""
    cx = x
    for label, url in items:
        text = marker + label
        w = max(0.85, 0.0072 * size * len(text))
        link(s, cx, y, w, h, text, url, size=size)
        cx += w + gap
    return cx


def logo_pill(s, x, y, w, h, path, pad=0.10, radius=0.5, fill=WHITE):
    """A white rounded pill with a partner mark centred inside it, sized so the
    mark keeps its clear space on all four sides."""
    box(s, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)
    im = PILImage.open(path)
    ar = im.size[0] / im.size[1]
    ih = h - 2 * pad
    iw = ih * ar
    if iw > w - 2 * pad:
        iw = w - 2 * pad
        ih = iw / ar
    pic = s.shapes.add_picture(path, Inches(x + (w - iw) / 2), Inches(y + (h - ih) / 2),
                               Inches(iw), Inches(ih))
    pic.shadow.inherit = False
    return pic


def cobrand_cover(title, subtitle, partner):
    """The AccuKnox front cover on layout 0, co-branded.

    The layout already carries the AccuKnox lockup, the badge groups and the
    product collage. The only addition is the partner mark, on a white pill
    under the title, where the layout leaves clear space."""
    s = prs.slides.add_slide(L_COVER)
    blank_footer(s)
    ph = _ph(s, 0)
    tx, tw = _move_ph(ph, 1.80, 1.04)
    _fill_ph(ph, title, 25, WHITE, True, spacing=1.0)
    sub = _ph(s, 1)
    _move_ph(sub, 2.92, 0.34)
    _fill_ph(sub, subtitle, 10.5, NAVY_TXT, False)
    pw, phh = 2.00, 0.54
    logo_pill(s, tx + (tw - pw) / 2, 3.30, pw, phh, partner, pad=0.11)
    return s


def chips(s, x, y, w, labels, per_row=5, h=0.28, gap=0.10, rgap=0.08,
          fill=GREY_BG, tcolor=NAVY, size=8.2):
    """A wrapped row of soft chips, used for asset names."""
    cw = (w - gap * (per_row - 1)) / per_row
    for i, lab in enumerate(labels):
        r, c = divmod(i, per_row)
        cx = x + c * (cw + gap)
        cy = y + r * (h + rgap)
        box(s, cx, cy, cw, h, text=lab, size=size, color=tcolor, bold=True,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=fill,
            shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.28, wrap=False,
            ml=0.02, mr=0.02)


def panel(s, x, y, w, h, heading, fill=WHITE, hfill=NAVY, hh=0.34, hsize=10.0):
    """A bordered panel with a coloured caption bar across the top."""
    box(s, x, y, w, h, fill=fill, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, y, w, hh, fill=hfill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.14)
    box(s, x, y + hh - 0.12, w, 0.12, fill=hfill)
    box(s, x + 0.14, y, w - 0.28, hh, text=heading, size=hsize, color=WHITE,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    return y + hh


def callout(s, x, y, w, h, text, accent=PRIMARY, size=9.0, tint=LAV, tcolor=NAVY):
    box(s, x, y, w, h, fill=tint, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    box(s, x, y, 0.07, h, fill=accent)
    box(s, x + 0.20, y, w - 0.34, h, text=text, size=size, color=tcolor,
        anchor=MSO_ANCHOR.MIDDLE)


def flow_node(s, x, y, w, h, tag, head, detail, accent=PRIMARY):
    """One stage in the timeline flowchart. Day chip, title, one detail line."""
    box(s, x, y, w, h, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    box(s, x + 0.10, y + 0.09, w - 0.20, 0.22, text=tag, size=6.8, color=WHITE,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=accent,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5, wrap=False, ml=0, mr=0)
    box(s, x + 0.07, y + 0.35, w - 0.14, 0.34, text=head, size=8.8, color=NAVY,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.07, y + 0.69, w - 0.14, h - 0.76, text=detail, size=7.2,
        color=MUTE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)


def flow_lane(s, y, label, accent, nodes, h=1.22, gap=0.22, lw=3.90):
    """A labelled row of flow nodes joined by arrows."""
    pill(s, CX, y, lw, 0.26, label, fill=accent, size=8.2)
    n = len(nodes)
    nw = (CW - gap * (n - 1)) / n
    ny = y + 0.32
    for i, (tag, head, detail) in enumerate(nodes):
        nx = CX + i * (nw + gap)
        flow_node(s, nx, ny, nw, h, tag, head, detail, accent=accent)
        if i < n - 1:
            arrow(s, nx + nw + 0.01, ny + h / 2 - 0.11, 0.20, 0.22, color=accent,
                  size=12)
    return ny + h


def step_row(s, x, y, w, tag, head, sub, accent=PRIMARY, h=0.60, tagw=0.94):
    box(s, x, y + 0.03, tagw, 0.26, text=tag, size=7.6, color=WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=accent,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5, wrap=False, ml=0, mr=0)
    box(s, x + tagw + 0.12, y - 0.02, w - tagw - 0.12, 0.28, text=head, size=9.6,
        color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, mb=0)
    box(s, x + tagw + 0.12, y + 0.24, w - tagw - 0.12, h - 0.24, text=sub,
        size=8.2, color=MUTE, anchor=MSO_ANCHOR.TOP, mt=0)


# ================================================================= 1. cover
cobrand_cover("CSPM and CWPP\nProof of Concept",
              "A two week scoped plan for Tata Technologies, AWS and Azure",
              TTL)


# ========================================================= 2. scope at a glance
s = std("What We Will Prove in Two Weeks", "POC scope",
        "Two clouds, four capabilities, three compliance frameworks. "
        "Nothing outside this list is part of the POC.")

CARDS = [
    ("CSPM", "cloud",
     "Read-only posture scan of every AWS account and Azure subscription. "
     "Misconfigurations, identity hardening and AI asset discovery."),
    ("CWPP", "shield",
     "Agent-based scanner on cloud VMs. Vulnerability scanning, malware "
     "scanning and a full package inventory per host."),
    ("Runtime Security", "pulse",
     "KubeArmor applies process, file and network policy inside the workload, "
     "using eBPF and Linux Security Modules."),
    ("KSPM", "gears",
     "CIS benchmark, identity and entitlement, and misconfiguration jobs "
     "running on the agreed EKS and AKS clusters."),
]
cw = (CW - 3 * 0.16) / 4
for i, (h_, ic_, body) in enumerate(CARDS):
    card(s, CX + i * (cw + 0.16), 1.50, cw, 1.74, h_, body,
         accent=(PRIMARY, SECOND, PURPLE, PRIMARY)[i], ic=ic_,
         hsize=9.8, bsize=8.2)

box(s, CX, 3.36, 4.0, 0.24, text="ASSETS IN SCOPE", size=8.4, color=NAVY,
    bold=True, anchor=MSO_ANCHOR.MIDDLE)
chips(s, CX, 3.62, CW,
      ["VM", "EKS", "ECS", "ECR", "RDS",
       "Block Storage", "Object Storage", "Bedrock", "AI Foundry", "AI and ML assets"],
      per_row=5)

box(s, CX, 4.46, 4.0, 0.24, text="COMPLIANCE FRAMEWORKS", size=8.4, color=NAVY,
    bold=True, anchor=MSO_ANCHOR.MIDDLE)
for i, lab in enumerate(["CIS Benchmarks", "ISO 27001", "SOC 2 Type II"]):
    pill(s, CX + i * 1.60, 4.72, 1.48, 0.30, lab, fill=PRIMARY, size=8.6)
link_strip(s, 4.76, [("All supported frameworks",
            DOCS + "support-matrix/compliance-matrix/")],
           size=8.4, h=0.26, x=CX + 5.06)

footer_note(s, "Clouds in scope, AWS and Azure. Agent-based scanning is the "
               "default for cloud VMs in this POC.", y=5.16, size=8.0)


# =========================================== 3. the two week timeline flowchart
s = std("The Two Week POC Timeline", "How the fourteen days run",
        "Week one onboards and discovers. Week two ranks the findings and "
        "delivers a pass or fail report.")

flow_lane(s, 1.40, "WEEK 1    ONBOARDING AND DISCOVERY", PRIMARY, [
    ("DAY 1-2", "Access and firewall",
     "Terraform runs on AWS and Azure. Outbound rules confirmed."),
    ("DAY 3", "Asset discovery",
     "Every account, every region. AI assets included."),
    ("DAY 4", "VM agent rollout",
     "Scanner on the agreed VMs. First vulnerability scan."),
    ("DAY 5", "Cluster onboarding",
     "Helm chart on EKS and AKS. CIS job scheduled."),
    ("DAY 5", "Baseline review",
     "Joint walkthrough of the inventory and first findings."),
])

flow_lane(s, 3.06, "WEEK 2    FINDINGS AND REPORT", PURPLE, [
    ("DAY 6-7", "Full scan results",
     "Misconfigurations, vulnerabilities and compliance scores."),
    ("DAY 8", "Risk ranking",
     "Critical findings triaged and prioritized with you."),
    ("DAY 9", "Runtime demonstration",
     "A policy blocks a violation on the test workload."),
    ("DAY 10-11", "Identity and toxic paths",
     "Accounts without MFA, wide roles, chained risk."),
    ("DAY 12-14", "Report and readout",
     "Pass or fail CSPM report, then a live session."),
])

for i, (g, txt, accent) in enumerate([
    ("check", "Day 5    Asset inventory agreed", PRIMARY),
    ("flag", "Day 8    Critical findings prioritized", SECOND),
    ("doc", "Day 14    Pass or fail CSPM report", PURPLE),
]):
    bx = CX + i * 3.12
    box(s, bx, 4.76, 2.96, 0.34, fill=GREY_BG,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.26)
    icon(s, bx + 0.09, 4.81, 0.24, G(g), bg=accent, fsz=9)
    box(s, bx + 0.40, 4.76, 2.50, 0.34, text=txt, size=8.2, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)

footer_note(s, "The clock starts the day read-only access is confirmed on both "
               "clouds. Three gates, three dates.", y=5.20, size=8.0)


# ========================================================= 4. success criteria
s = std("POC Success Criteria", "What pass looks like",
        "Ten criteria decide the POC. Each one is checked on a named day, "
        "against evidence you can see in the platform.")

ROWS = [
    ["Area", "What pass looks like", "Checked"],
    ["Asset discovery",
     "Every AWS account and Azure subscription inventoried, across all regions",
     "Day 3"],
    ["AI asset coverage",
     "Bedrock, AI Foundry and other AI assets listed in the inventory", "Day 3"],
    ["VM vulnerability",
     "A package inventory and a CVE list returned for every nominated VM", "Day 6"],
    ["Malware scanning",
     "A malware scan result returned for every nominated VM", "Day 6"],
    ["Compliance",
     "CIS, ISO 27001 and SOC 2 Type II scored per control group, on both clouds",
     "Day 7"],
    ["KSPM",
     "CIS Kubernetes benchmark scored for each onboarded cluster", "Day 7"],
    ["Prioritization",
     "Critical findings risk ranked, triaged and prioritized with your team",
     "Day 8"],
    ["Runtime security",
     "A policy violation blocked on the agreed test workload", "Day 9"],
    ["Identity hardening",
     "Accounts without MFA and over-permissive roles listed", "Day 10"],
    ["Alerting and report",
     "An alert reaches your webhook, and the pass or fail report is delivered",
     "Day 14"],
]
t = grid(s, CX, 1.44, CW, 3.38, ROWS, colw=[1.66, 6.24, 1.30],
         head_h=0.28, row_h=0.31, bsize=7.8, hsize=8.4, pad=0.02, center=(2,))
for ri in range(1, len(ROWS)):
    c = t.cell(ri, 2)
    c.fill.solid(); c.fill.fore_color.rgb = LAV
    for pp in c.text_frame.paragraphs:
        for r in pp.runs:
            r.font.bold = True
            r.font.color.rgb = PURPLE

callout(s, CX, 4.92, CW, 0.40,
        "We mark every criterion pass or fail together during the day 14 "
        "readout. Nothing is scored behind closed doors.",
        accent=GREEN, tint=GREEN_LT, tcolor=GREEN_DK, size=8.8)


# ======================================================== 5. Q1 architecture
s = std("Question 1  Architecture and Data Flow", "End to end connectivity",
        "Three flows connect the TTL cloud to AccuKnox. Every one of them runs "
        "over TLS, and every agent connection is outbound.")

# left, the TTL cloud
ty = panel(s, CX, 1.52, 2.66, 2.94, "TTL CLOUD", hfill=NAVY, hsize=9.6)
box(s, CX + 0.14, ty + 0.12, 2.38, 0.26, text="AWS accounts", size=9.0,
    color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
chips(s, CX + 0.14, ty + 0.40, 2.38, ["EC2", "EKS", "ECS", "ECR", "RDS", "S3"],
      per_row=3, h=0.24, size=7.4)
box(s, CX + 0.14, ty + 1.10, 2.38, 0.26, text="Azure subscriptions", size=9.0,
    color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
chips(s, CX + 0.14, ty + 1.38, 2.38, ["VMs", "AKS", "Blob", "Disks", "SQL", "AI Foundry"],
      per_row=3, h=0.24, size=7.4)
box(s, CX + 0.14, ty + 2.06, 2.38, 0.44, size=7.8, color=MUTE,
    anchor=MSO_ANCHOR.TOP,
    text="One read-only identity per cloud. CSPM installs nothing in your network.")

# right, AccuKnox SaaS
ty2 = panel(s, 6.94, 1.52, 2.66, 2.94, "ACCUKNOX SAAS", hfill=PRIMARY, hsize=9.6)
for j, (lab, sub) in enumerate([
        ("CSPM", "Posture and compliance"),
        ("CWPP", "Vulnerability and malware"),
        ("KSPM", "Cluster posture"),
        ("Reporting", "Risk ranking and reports")]):
    yy = ty2 + 0.14 + j * 0.62
    box(s, 7.08, yy, 2.38, 0.28, text=lab, size=9.2, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
        radius=0.22)
    box(s, 7.08, yy + 0.28, 2.38, 0.24, text=sub, size=7.6, color=MUTE,
        anchor=MSO_ANCHOR.MIDDLE)

# middle, the three flows
FLOWS = [
    ("1", "CSPM read-only scan", "←",
     "AccuKnox calls the AWS and Azure management APIs. HTTPS 443.", PRIMARY),
    ("2", "Agent telemetry", "→",
     "Your VMs and clusters connect out to AccuKnox. TCP 443, 3000, 8081, 9090.", SECOND),
    ("3", "Alerts, one way", "←",
     "AccuKnox posts alerts to your ticketing tool webhook. HTTPS 443.", PURPLE),
]
for j, (num, head, glyph, sub, accent) in enumerate(FLOWS):
    fy = 1.58 + j * 0.98
    box(s, 3.22, fy, 3.60, 0.86, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    box(s, 3.30, fy + 0.06, 0.26, 0.26, text=num, size=8.0, color=WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=accent,
        shape=MSO_SHAPE.OVAL, wrap=False, ml=0, mr=0)
    box(s, 3.62, fy + 0.04, 2.60, 0.30, text=head, size=9.4, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 6.24, fy + 0.04, 0.50, 0.30, text=glyph, size=15, color=accent,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False,
        ml=0, mr=0)
    box(s, 3.34, fy + 0.36, 3.36, 0.44, text=sub, size=8.0, color=MUTE,
        anchor=MSO_ANCHOR.TOP)

callout(s, CX, 4.62, CW, 0.44,
        "No inbound connection into the TTL network is required. AccuKnox never "
        "opens a session towards your VMs, and your agents dial out only.",
        accent=GREEN, tint=GREEN_LT, tcolor=GREEN_DK, size=9.0)


# ================================== 6. how AccuKnox connects to the workloads
s = std("How AccuKnox Connects to Your Workloads", "Deployment architecture",
        "The agents inside your clusters and VMs dial out to the AccuKnox "
        "control plane. The control plane never dials in.")

image_fit(s, img("ctrlplane.png"), CX, 1.46, 6.30, 2.98, frame=GREY_BD)

for j, (head, body, accent) in enumerate([
    ("Telemetry goes out",
     "Clusters and VMs post alerts and telemetry to AccuKnox over an outbound "
     "TLS session they open themselves.", PRIMARY),
    ("Policies come back",
     "The control plane returns runtime policies on that same session. No "
     "inbound firewall rule is needed.", SECOND),
    ("In POC scope",
     "The two blocks on the left, Kubernetes clusters and cloud VMs. Registry "
     "and pipeline scanning stay out.", PURPLE),
]):
    yy = 1.46 + j * 1.02
    box(s, 6.86, yy, 2.74, 0.98, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    box(s, 6.86, yy, 0.07, 0.98, fill=accent)
    box(s, 7.04, yy + 0.06, 2.48, 0.26, text=head, size=9.6, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 7.04, yy + 0.32, 2.48, 0.60, text=body, size=8.0, color=MUTE,
        anchor=MSO_ANCHOR.TOP)

footer_note(s, "AccuKnox control plane deployment. Source, the AccuKnox "
               "enterprise architecture page.", y=4.56, size=8.0)
link_strip(s, 4.86, [
    ("AccuKnox enterprise architecture", DOCS + "getting-started/accuknox-arch/"),
    ("CWPP prerequisites", DOCS + "getting-started/cwpp-prereq/"),
], size=8.4, gap=0.26)


# =================================================== 7. Q1 ports and endpoints
s = std("Question 1  Ports, Protocols and Endpoints", "What to whitelist",
        "Open these outbound rules before day one. Nothing on this list needs an "
        "inbound rule from the internet.")

ROWS = [
    ["Flow", "Direction", "Port", "Endpoint", "Purpose"],
    ["CSPM cloud scan", "AccuKnox to cloud API", "443",
     "AWS and Azure management API endpoints", "Read-only asset and configuration discovery"],
    ["VM scanner download", "VM outbound", "443",
     "accuknox-omni.s3.us-east-1.amazonaws.com", "Download the scanner installer and binary"],
    ["VM scan results", "VM outbound", "443",
     "cspm.accuknox.com", "Post vulnerability and malware findings"],
    ["Runtime telemetry", "VM and cluster outbound", "3000",
     "knox-gw.<env>.accuknox.com", "KubeArmor feeds and cluster metadata"],
    ["Policy service", "VM and cluster outbound", "443",
     "pps.<env>.accuknox.com", "Policy provisioning to the agents"],
    ["Workload identity", "VM and cluster outbound", "8081, 9090",
     "spire.<env>.accuknox.com", "SPIRE attestation and health check"],
    ["Alerts", "AccuKnox to TTL", "443",
     "Your ticketing tool webhook URL", "One-way alert delivery"],
]
grid(s, CX, 1.56, CW, 3.06, ROWS, colw=[1.62, 1.74, 0.72, 2.62, 2.50],
     head_h=0.30, row_h=0.36, bsize=7.8, hsize=8.2, pad=0.03, center=(1, 2))

callout(s, CX, 4.52, CW, 0.40,
        "The <env> value is the AccuKnox tenant environment. We confirm the exact "
        "host names with you on day one, before any rule is raised.",
        accent=PRIMARY, size=8.6)

link_strip(s, 5.08, [
    ("CWPP network requirements", DOCS + "getting-started/cwpp-prereq/"),
    ("VM onboarding ports", DOCS + "how-to/vm-onboard-deboard-systemd/"),
], size=8.4)


# ================================================== 6. Q2 CSPM, what is created
s = std("Question 2  What CSPM Creates in Your Cloud", "CSPM footprint",
        "CSPM reads across a cross-account link. It creates one read-only "
        "identity per cloud and nothing else.")

image_fit(s, img("aws-arch.png"), CX, 1.42, 4.50, 0.62, frame=GREY_BD)
image_fit(s, img("azure-arch.png"), 5.10, 1.42, 4.50, 0.62, frame=GREY_BD)

ROWS = [
    ["Cloud", "What is created", "Purpose"],
    ["AWS", "IAM user with the ReadOnlyAccess and SecurityAudit policies",
     "Reads asset inventory, configuration and security settings in every region"],
    ["AWS", "Inline policy for Bedrock, SageMaker and Bedrock AgentCore",
     "Discovers and assesses AI and ML assets"],
    ["AWS", "Access key and secret key",
     "Authenticates the scheduled AccuKnox scan"],
    ["Azure", "Entra ID app registration and service principal",
     "Gives AccuKnox a read-only identity in your tenant"],
    ["Azure", "Reader and Log Analytics Reader role assignments",
     "Reads resource configuration and activity log data"],
    ["Azure", "Directory.Read.All Microsoft Graph permission",
     "Reads identity objects for the identity hardening checks"],
]
grid(s, CX, 2.14, CW, 2.32, ROWS, colw=[0.86, 3.62, 4.72],
     head_h=0.28, row_h=0.34, bsize=8.0, hsize=8.4, pad=0.03, center=(0,))

callout(s, CX, 4.56, CW, 0.42,
        "CSPM creates no compute, storage or network resource. Terraform "
        "provisions the read-only identity, and terraform destroy removes it.",
        accent=GREEN, tint=GREEN_LT, tcolor=GREEN_DK, size=9.0)

link_strip(s, 5.10, [
    ("AWS prerequisites", DOCS + "how-to/cspm-prereq-aws/"),
    ("Azure prerequisites", DOCS + "how-to/cspm-prereq-azure/"),
    ("AWS Terraform onboarding", DOCS + "how-to/terraform-aws-onboarding/"),
    ("Azure Terraform onboarding", DOCS + "how-to/terraform-azure-onboarding/"),
], size=8.2, gap=0.22)


# =========================================== 7. Q2 CWPP and KSPM, what deploys
s = std("Question 2  What CWPP and KSPM Deploy", "CWPP and KSPM footprint",
        "The scanner is a systemd service on the VM. The cluster agents install "
        "from one Helm chart.")

ROWS = [
    ["Component", "Where it runs", "Purpose"],
    ["Omni VM scanner, a systemd service with a daily timer",
     "Each in-scope EC2 and Azure VM",
     "Vulnerability scan, malware scan and package inventory"],
    ["KubeArmor, a DaemonSet",
     "Each in-scope EKS and AKS cluster",
     "Runtime enforcement through eBPF and Linux Security Modules"],
    ["Shared Informer Agent, a Deployment",
     "Cluster and VM control plane",
     "Collects pod, node, container and namespace metadata"],
    ["Feeder Service, a Deployment",
     "Cluster and VM control plane",
     "Forwards KubeArmor telemetry to AccuKnox"],
    ["Policy Enforcement Agent, a Deployment",
     "Cluster and VM control plane",
     "Applies labels and runtime policies to the workloads"],
    ["CIS benchmark, KIEM and risk assessment jobs",
     "Cluster, on a schedule you set",
     "The KSPM posture checks, each one a short-lived job"],
]
grid(s, CX, 1.50, CW, 2.62, ROWS, colw=[3.30, 2.42, 3.48],
     head_h=0.28, row_h=0.38, bsize=8.0, hsize=8.4, pad=0.03,
     firstcol_fill=None)

for i, (num, lab, src) in enumerate([
        ("200m", "KubeArmor CPU request", "per node"),
        ("10%", "VM scanner CPU ceiling", "systemd default"),
        ("2 GB", "VM scanner memory ceiling", "systemd default")]):
    stat(s, CX + i * 3.12, 4.20, 2.96, num, lab, source=src, nsize=19, lsize=8.6,
         h=0.82, ssize=7.0)

link_strip(s, 5.18, [
    ("Agent-based VM scanning", DOCS + "how-to/vm-security/agent-based/linux/"),
    ("CWPP prerequisites", DOCS + "getting-started/cwpp-prereq/"),
    ("Cluster onboarding", DOCS + "how-to/cluster-onboarding/"),
], size=8.2, gap=0.24)


# ============================================================= 8. CSPM prereqs
s = std("Prerequisites for CSPM", "Before day one",
        "CSPM needs one read-only identity per cloud. It needs no agent and no "
        "firewall change on your side.")

pw = (CW - 0.20) / 2
for i, (head, accent, items, links) in enumerate([
    ("AWS", PRIMARY, [
        "An AWS account with permission to create an IAM user.",
        "Terraform and the AWS CLI on the machine that runs the script.",
        "The ReadOnlyAccess and SecurityAudit managed policies attached.",
        "An inline policy for Bedrock and SageMaker, needed only for AI assets.",
        "The access key and secret key handed to AccuKnox at onboarding.",
    ], [("AWS prerequisites", DOCS + "how-to/cspm-prereq-aws/"),
        ("AWS Terraform", DOCS + "how-to/terraform-aws-onboarding/")]),
    ("Azure", SECOND, [
        "Permission to register an Entra ID application in the tenant.",
        "Terraform and the Azure CLI, authenticated against the subscription.",
        "The Reader and Log Analytics Reader roles on each subscription.",
        "Admin consent for the Directory.Read.All Graph permission.",
        "The application ID, directory ID and client secret at onboarding.",
    ], [("Azure prerequisites", DOCS + "how-to/cspm-prereq-azure/"),
        ("Azure Terraform", DOCS + "how-to/terraform-azure-onboarding/")]),
]):
    px = CX + i * (pw + 0.20)
    ty = panel(s, px, 1.48, pw, 2.92, head, hfill=accent, hsize=10.5)
    bullets(s, px + 0.18, ty + 0.14, pw - 0.36, 2.10, items, size=9.0,
            color=INK, mcolor=accent, gap=10)
    link_strip(s, 4.02, links, size=8.2, gap=0.24, x=px + 0.18)

callout(s, CX, 4.56, CW, 0.46,
        "No port needs to be opened for CSPM. AccuKnox calls the AWS and Azure "
        "management APIs from outside, so nothing is installed in your network.",
        accent=GREEN, tint=GREEN_LT, tcolor=GREEN_DK, size=9.0)


# ==================================================== 9. CWPP and KSPM prereqs
s = std("Prerequisites for CWPP and KSPM", "Before day one",
        "The VM scanner needs root and outbound 443. The cluster agents need "
        "Helm and the same outbound rules.")

for i, (head, accent, items, links) in enumerate([
    ("Cloud VMs, agent-based scanning", PRIMARY, [
        "Root or sudo access on each VM in scope.",
        "Outbound 443 to the AccuKnox scanner bucket and to cspm.accuknox.com.",
        "curl installed on the VM.",
        "An AccuKnox tenant ID and an artifact API token, created in Settings.",
        "A label per VM group, so findings map to the right owner.",
    ], [("Agent-based VM scanning", DOCS + "how-to/vm-security/agent-based/linux/"),
        ("Supported VM platforms", DOCS + "support-matrix/vms/")]),
    ("EKS and AKS clusters", PURPLE, [
        "kubectl and Helm on the machine that runs the install command.",
        "Outbound 443, 3000, 8081 and 9090 from the cluster nodes.",
        "A kernel with BTF support, checked by the script in the docs.",
        "A namespace the chart can create, named agents by default.",
        "A join token, generated on the onboarding screen.",
    ], [("Cluster onboarding", DOCS + "how-to/cluster-onboarding/"),
        ("CWPP prerequisites", DOCS + "getting-started/cwpp-prereq/")]),
]):
    px = CX + i * (pw + 0.20)
    ty = panel(s, px, 1.48, pw, 2.92, head, hfill=accent, hsize=10.0)
    bullets(s, px + 0.18, ty + 0.14, pw - 0.36, 2.10, items, size=9.0,
            color=INK, mcolor=accent, gap=10)
    link_strip(s, 4.02, links, size=8.2, gap=0.24, x=px + 0.18)

callout(s, CX, 4.56, CW, 0.46,
        "Malware scanning is off by default because it uses more CPU. We switch "
        "it on for the POC, on the VMs you nominate.",
        accent=PRIMARY, size=9.0)


# ============================================================== 10. Q3 cost
s = std("Question 3  Azure Cost for the POC and Production", "Cost model",
        "AccuKnox creates no Azure resource. The only Azure charge that changes "
        "is outbound data.")

for i, (num, lab, src) in enumerate([
        ("0", "New Azure resources created", "CSPM and CWPP"),
        ("10%", "CPU ceiling per scanned VM", "raise it if you want faster scans"),
        ("2 GB", "Memory ceiling per scanned VM", "systemd default")]):
    stat(s, CX + i * 3.12, 1.48, 2.96, num, lab, source=src, nsize=21, lsize=8.8,
         h=0.92, ssize=7.0)

ROWS = [
    ["Cost driver", "During the two week POC", "In production"],
    ["CSPM API reads",
     "No Azure charge. Read-only calls to the management APIs.",
     "No Azure charge. Scan frequency does not change this."],
    ["CWPP VM scanner",
     "Runs inside the existing VM, capped at 10% CPU and 2 GB memory.",
     "Same ceilings. Cost scales with the number of VMs you keep scanning."],
    ["KSPM cluster jobs",
     "Short-lived jobs on nodes you already pay for.",
     "Same jobs on the schedule you set, typically once a day."],
    ["Outbound data to AccuKnox",
     "Findings and alert metadata only. No workload data leaves Azure.",
     "Grows with asset count. We measure the real figure during the POC."],
    ["AccuKnox platform",
     "No charge for the POC period.",
     "Priced per asset. Quoted separately once the POC scope is confirmed."],
]
grid(s, CX, 2.54, CW, 1.96, ROWS, colw=[1.86, 3.62, 3.72],
     head_h=0.28, row_h=0.32, bsize=8.0, hsize=8.4, pad=0.03)

callout(s, CX, 4.66, CW, 0.44,
        "The POC adds no new line item to the Azure bill. We report the measured "
        "egress at the end of week two, so the production figure rests on your data.",
        accent=GREEN, tint=GREEN_LT, tcolor=GREEN_DK, size=9.0)


# ============================================================== 11. Q4 risk
s = std("Question 4  Risk and Business Impact", "Risk assessment",
        "Five risks are worth naming. Each one has a control that is already in "
        "the product, not a promise.")

ROWS = [
    ["Risk", "Business impact", "Mitigation"],
    ["The scanner competes for CPU on a production VM",
     "Slower application response during a scan window",
     "The systemd unit caps the scanner at 10% CPU and 2 GB memory. Scans run on a daily timer you set."],
    ["A runtime policy blocks a legitimate process",
     "An application function stops working",
     "Policies run in audit mode first. Blocking is switched on only for the test workload you agree."],
    ["Cloud credentials are misused",
     "Unauthorised read of configuration data",
     "The identity holds read-only policies. It carries no write or delete permission on either cloud."],
    ["An older VM kernel lacks BTF support",
     "The agent fails to install on part of the fleet",
     "A one-line check runs before rollout. The docs carry a supported path for kernels without BTF."],
    ["Data leaves the TTL boundary",
     "Exposure of sensitive material to a third party",
     "Only findings and alert metadata are sent. Source code, customer data and workload payloads stay put."],
]
grid(s, CX, 1.54, CW, 3.20, ROWS, colw=[2.52, 2.66, 4.02],
     head_h=0.28, row_h=0.52, bsize=7.8, hsize=8.4, pad=0.04)

callout(s, CX, 4.62, CW, 0.40,
        "Third party risk management sits with the TTL procurement team. We "
        "supply the data processing addendum and the supplier record on request.",
        accent=PRIMARY, size=8.6)


# ============================================================ 12. Q5 rollback
s = std("Question 5  Rollback and Cleanup", "If we stop, nothing is left behind",
        "Three commands remove everything AccuKnox installed. The whole rollback "
        "takes under an hour.")

COLS = [
    ("1  CSPM", PRIMARY, [
        "terraform destroy",
        "# AWS    IAM user, policies, keys",
        "# Azure  app registration, roles",
    ], "Delete the cloud account under Settings, Cloud Accounts. Then run "
       "terraform destroy to remove the identity on both clouds."),
    ("2  Cloud VMs", SECOND, [
        "/usr/local/bin/omni-uninstall.sh",
        "knoxctl deboard vm node",
        "sudo rm -rf ~/.accuknox-config",
    ], "Removes the scanner, the systemd service and timer, the agent containers "
       "and the local config directory."),
    ("3  Clusters", PURPLE, [
        "helm uninstall agents -n agents",
        "kubectl delete ns agents",
        "helm uninstall cis-k8s-job kiem-job",
    ], "Removes every agent, every KSPM job and the namespace. Then delete the "
       "cluster under Settings, Manage Cluster."),
]
cwid = (CW - 2 * 0.18) / 3
for i, (head, accent, cmds, note) in enumerate(COLS):
    px = CX + i * (cwid + 0.18)
    ty = panel(s, px, 1.52, cwid, 2.44, head, hfill=accent, hsize=10.5)
    code_block(s, px + 0.16, ty + 0.14, cwid - 0.32, 0.24 + 0.24 * len(cmds),
               cmds, size=7.6)
    box(s, px + 0.16, ty + 0.48 + 0.24 * len(cmds), cwid - 0.32, 0.90,
        text=note, size=8.2, color=MUTE, anchor=MSO_ANCHOR.TOP)

callout(s, CX, 4.16, CW, 0.44,
        "Deboard the cluster from the AccuKnox console first, then run the "
        "uninstall commands. That order leaves no orphaned record on either side.",
        accent=GREEN, tint=GREEN_LT, tcolor=GREEN_DK, size=9.0)

link_strip(s, 4.76, [
    ("Cloud account offboarding", DOCS + "how-to/cloud-offboarding/"),
    ("Cluster offboarding", DOCS + "how-to/cluster-offboarding/"),
    ("VM deboarding", DOCS + "how-to/vm-onboard-deboard-systemd/"),
], size=8.2, gap=0.24)


# ======================================================= 13. compliance report
s = std("Compliance and the Report You Get", "Deliverable",
        "Three frameworks run during the POC. The output is one pass or fail "
        "report per cloud, not a dashboard tour.")

LW = 4.50
ty = panel(s, CX, 1.46, LW, 1.74, "FRAMEWORKS RUN DURING THE POC",
           hfill=NAVY, hsize=9.4)
for j, (g, head, sub_) in enumerate([
    ("cert", "CIS Benchmarks",
     "AWS CIS to v4.0.1, Azure CIS to v3.0, plus the Kubernetes job."),
    ("doc", "ISO 27001",
     "Each cloud rule maps to the controls it supports."),
    ("check", "SOC 2 Type II",
     "Runs on both clouds with the same pass and fail split."),
]):
    list_row(s, CX + 0.18, ty + 0.16 + j * 0.44, LW - 0.36, G(g), head, sub_,
             accent=(PRIMARY, SECOND, PURPLE)[j], h=0.42, hsize=9.8, ssize=7.8,
             isz=0.30)

ty2 = panel(s, CX, 3.26, LW, 1.62, "WHAT THE REPORT CONTAINS", hfill=PRIMARY,
            hsize=9.4)
bullets(s, CX + 0.18, ty2 + 0.12, LW - 0.36, 1.10, [
    "Asset inventory across both clouds and every region.",
    "Pass or fail result per control, per cloud account.",
    "Critical findings, risk ranked, triaged and prioritized.",
    "Vulnerability, malware and identity hardening results.",
], size=8.6, color=INK, mcolor=PRIMARY, gap=5)

image_fit(s, img("report-1.png"), 5.12, 1.46, 2.20, 2.62, frame=GREY_BD)
image_fit(s, img("report-2.png"), 7.42, 1.46, 2.20, 2.62, frame=GREY_BD)
box(s, 5.12, 4.14, 4.50, 0.24, text="Sample pages from the CSPM report",
    size=8.0, color=MUTE, italic=True, align=PP_ALIGN.CENTER,
    anchor=MSO_ANCHOR.MIDDLE)
link_strip(s, 4.46, [("Full sample report, CSPM_Report.pdf",
                      DOCS + "resources/assets/CSPM_Report.pdf")],
           size=8.0, x=5.12)

link_strip(s, 5.02, [
    ("Compliance matrix", DOCS + "support-matrix/compliance-matrix/"),
    ("CSPM playbook", DOCS + "how-to/playbook-cspm/"),
    ("CWPP playbook", DOCS + "how-to/playbook-cwpp/"),
    ("KSPM playbook", DOCS + "how-to/playbook-kspm/"),
], size=8.2, gap=0.24)


# ============================================================== 14. alerting
s = std("Alerts Into Your Ticketing Tool", "Integration",
        "AccuKnox posts each alert to a webhook URL you own. Delivery runs one "
        "way, from AccuKnox to your tool.")

FLOW = [("Finding or alert", "AccuKnox detects a policy violation or a new critical finding.", PRIMARY),
        ("Trigger", "A filter you define decides which alerts leave the platform.", SECOND),
        ("Webhook POST", "AccuKnox sends JSON to your URL, with your auth header.", PURPLE),
        ("Your ticketing tool", "Your tool creates the ticket and owns it from there.", NAVY)]
bw = (CW - 3 * 0.44) / 4
for i, (head, sub, accent) in enumerate(FLOW):
    bx = CX + i * (bw + 0.44)
    box(s, bx, 1.52, bw, 1.14, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    box(s, bx, 1.52, bw, 0.08, fill=accent, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
        radius=0.5)
    box(s, bx + 0.12, 1.66, bw - 0.24, 0.30, text=head, size=9.6, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, bx + 0.12, 1.96, bw - 0.24, 0.62, text=sub, size=8.0, color=MUTE,
        anchor=MSO_ANCHOR.TOP)
    if i < 3:
        arrow(s, bx + bw + 0.09, 2.00, 0.26, 0.26)

code_block(s, CX, 2.86, 4.52, 1.62, [
    ("{", False),
    ('  "Action": "Block",', True),
    ('  "Message": "Detected and prevented compromise to File integrity",', False),
    ('  "PolicyName": "harden-file-integrity-monitoring",', False),
    ('  "ProcessName": "/bin/touch",', False),
    ('  "Tags": "MITRE_T1036,MITRE_T1565"', False),
    ("}", False),
], size=7.4, title="SAMPLE WEBHOOK PAYLOAD")

ty = panel(s, 5.08, 2.86, 4.52, 1.62, "WHAT WE COMMIT TO", hfill=NAVY, hsize=9.6)
bullets(s, 5.24, ty + 0.12, 4.20, 1.10, [
    "One-way delivery from AccuKnox to your webhook URL.",
    "You choose the method, the success codes and the auth header.",
    "Alerts also reach Microsoft Teams through the same webhook channel.",
], size=8.8, color=INK, mcolor=PRIMARY, gap=6)

callout(s, CX, 4.60, CW, 0.40,
        "Two-way sync between your ticketing tool and AccuKnox is not part of "
        "this POC. We will confirm feasibility separately.",
        accent=PRIMARY, size=9.0)

link_strip(s, 5.14, [
    ("Webhook integration guide", DOCS + "integrations/webhook-integration/"),
], size=8.4)


# ============================================================= 15. references
s = std("Documentation", "Everything in this deck, with a source",
        "Each link opens the AccuKnox help doc that the matching slide was "
        "written from.")

REFS = [
    ("Onboarding and prerequisites", PRIMARY, [
        ("CSPM prerequisites for AWS", DOCS + "how-to/cspm-prereq-aws/"),
        ("CSPM prerequisites for Azure", DOCS + "how-to/cspm-prereq-azure/"),
        ("AWS Terraform onboarding", DOCS + "how-to/terraform-aws-onboarding/"),
        ("Azure Terraform onboarding", DOCS + "how-to/terraform-azure-onboarding/"),
        ("AWS account onboarding", DOCS + "how-to/aws-onboarding/"),
        ("Azure account onboarding", DOCS + "how-to/azure-onboarding/"),
        ("AI and ML onboarding for AWS", DOCS + "how-to/aiml-aws-onboard/"),
        ("AI and ML onboarding for Azure", DOCS + "how-to/aiml-azure-onboard/"),
    ]),
    ("Workloads, clusters and cleanup", PURPLE, [
        ("CWPP prerequisites and ports", DOCS + "getting-started/cwpp-prereq/"),
        ("Agent-based VM scanning", DOCS + "how-to/vm-security/agent-based/linux/"),
        ("VM onboarding and deboarding", DOCS + "how-to/vm-onboard-deboard-systemd/"),
        ("Cluster onboarding", DOCS + "how-to/cluster-onboarding/"),
        ("Supported VM platforms", DOCS + "support-matrix/vms/"),
        ("Compliance matrix", DOCS + "support-matrix/compliance-matrix/"),
        ("Webhook integration", DOCS + "integrations/webhook-integration/"),
        ("Cloud and cluster offboarding", DOCS + "how-to/cluster-offboarding/"),
    ]),
]
for i, (head, accent, items) in enumerate(REFS):
    px = CX + i * (pw + 0.20)
    ty = panel(s, px, 1.52, pw, 3.16, head, hfill=accent, hsize=10.0)
    for j, (label, url) in enumerate(items):
        yy = ty + 0.14 + j * 0.34
        box(s, px + 0.18, yy, 0.20, 0.26, text="↗", size=9, color=accent,
            bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
            wrap=False, ml=0, mr=0)
        link(s, px + 0.42, yy, pw - 0.60, 0.26, label, url, size=8.8, color=NAVY)

footer_note(s, "Full documentation, help.accuknox.com. Questions during the POC "
               "go to support@accuknox.com.", y=4.90, size=8.4)


# ============================================================== 16. closing
closing_slide(prs)


prs.save(OUT)
print("wrote", os.path.abspath(OUT), "slides:", len(prs.slides._sldIdLst))
