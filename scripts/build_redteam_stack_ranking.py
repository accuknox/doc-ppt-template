"""Build the AccuKnox AI Red Teaming Stack Ranking as a branded A4 landscape PDF.

Scope is AI Security > Red Teaming only. Six vendors: AccuKnox, HiddenLayer,
Mindgard, Lakera, Palo Alto Networks and Zscaler.

Every matrix cell carries a state and a short line of evidence. The scores and
the ranking are counted from the cells, so the ranking cannot disagree with the
matrix. Vendor evidence comes from the one-page briefs in
D:\\Atharva\\AccuKnox\\redteam-briefs\\source\\, checked 10 to 15 September 2026.

AccuKnox evidence comes from:
  HelpDocs docs/use-cases/red-teaming.md
  HelpDocs docs/getting-started/3.6-release.md
  HelpDocs docs/how-to/aiml-saas-vs-onprem.md
  HelpDocs references/technical-reference/AccuKnox AI Security _ Macro Deck _ June_2026.pptx
    (red teaming slides 25, 69, 108 to 111, 119)
  HelpDocs references/technical-reference/knox-rt-red-teaming-module.md
  AccuKnox product team figures supplied 15 September 2026 (probe count,
    category count, input methods, deployment options)

Flat colors only. Emits HTML with logo and screenshots inlined, then prints to
PDF with headless Edge.
"""
import base64
import io
import os
import subprocess
import sys

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(REPO, "output", "comparisons")
OUT = os.path.join(REPO, "output")
NAME = "AccuKnox_AI_Red_Teaming_Stack_Ranking"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SHOTS = r"D:\Atharva\AccuKnox\HelpDocs\docs\getting-started\images\release-notes\v3.6"

NAVY = "#11206D"
BLUE = "#0046FF"
SEC = "#6464FF"
RED = "#C80019"
GREEN = "#16A55C"
MUTE = "#6A749A"
INK = "#1A1D2E"
GREY_BG = "#EEF0F6"
GREY_BD = "#C4CCDE"
TINT = "#F7F9FF"
LAV = "#E6E8FF"

READ_ON = "15 September 2026"


def logo(name):
    with open(os.path.join(REPO, "assets", "logos", name), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def shot(fname, width=1400):
    im = Image.open(os.path.join(SHOTS, fname)).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=86)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


LOGO_DARK = logo("accuknox-logo-dark-bg.png")
LOGO_LIGHT = logo("accuknox-logo-light-bg.png")

# --------------------------------------------------------------------------
# vendors, in column order
# --------------------------------------------------------------------------
VENDORS = [
    ("ak", "AccuKnox", "AI Red Teaming"),
    ("hl", "HiddenLayer", "AI Attack Simulation"),
    ("mg", "Mindgard", "Automated AI Red Teaming"),
    ("lk", "Lakera", "AI Red Teaming, owned by Check Point"),
    ("pa", "Palo Alto Networks", "Prisma AIRS AI Red Teaming"),
    ("zs", "Zscaler", "SPLX Probe"),
]

# --------------------------------------------------------------------------
# criteria. state: y = Yes (2), p = Partial (1), n = Not stated (0)
# --------------------------------------------------------------------------
CRITERIA = [
    ("Published attack library", "Attack set size the vendor states in public", {
        "ak": ("y", "30,000+ probes across 20+ categories"),
        "hl": ("p", "About 40 techniques. Catalog size not stated"),
        "mg": ("p", "150+ disclosed flaws feed it. No attack count"),
        "lk": ("p", "85M+ Gandalf prompts. No test count"),
        "pa": ("y", "500+ attack vectors across 50+ techniques"),
        "zs": ("p", "25+ probes vs 5,000+ simulations"),
    }),
    ("Context-aware attacks", "Attacks written for what the target does", {
        "ak": ("y", "Probes from purpose, JSON, documents or typed input"),
        "hl": ("p", "Custom prompt sets and prompt mutation"),
        "mg": ("y", "Recon first, then targeted attacks"),
        "lk": ("p", "Engineers adapt attacks in the service"),
        "pa": ("y", "A profiler agent feeds an attacker agent"),
        "zs": ("y", "Custom and domain-specific probes"),
    }),
    ("Agents, RAG and MCP", "Tests beyond a single chat model", {
        "ak": ("y", "Agentic, MCP and RAG poisoning probes"),
        "hl": ("p", "Agents. RAG and MCP not stated"),
        "mg": ("y", "Agents, tools, APIs and workflows"),
        "lk": ("y", "RAG poisoning, tool misuse, MCP tools"),
        "pa": ("p", "Multi-agent. RAG and MCP not stated"),
        "zs": ("p", "RAG poisoning. Agents via a separate mapper"),
    }),
    ("Multimodal and ML models", "Image, audio or predictive ML targets", {
        "ak": ("p", "LLM and ML. Image, audio not stated"),
        "hl": ("p", "Predictive ML. Image, audio not stated"),
        "mg": ("y", "Image, audio and multimodal models"),
        "lk": ("y", "Text, audio, image and multimodal"),
        "pa": ("p", "Text and file-upload attacks"),
        "zs": ("y", "Text, voice, images and documents"),
    }),
    ("Compliance mapping", "Framework tags in the product, no service deal", {
        "ak": ("y", "OWASP LLM, ATLAS, NIST AI RMF, EU AI Act, ISO 42001"),
        "hl": ("n", "NIST and EU AI Act via services only"),
        "mg": ("y", "OWASP LLM, ATLAS, NIST AI RMF, EU AI Act"),
        "lk": ("p", "OWASP, ATLAS. NIST, EU AI Act not stated"),
        "pa": ("p", "OWASP, NIST, MITRE. EU AI Act not stated"),
        "zs": ("y", "8 frameworks, with ISO 42001 and DORA"),
    }),
    ("Self-hosted and air-gapped", "Prompts and findings stay in your network", {
        "ak": ("y", "SaaS, private cloud, on-prem, air-gapped"),
        "hl": ("n", "No deployment model stated"),
        "mg": ("p", "Private cloud. Air-gapped not stated"),
        "lk": ("n", "Red teaming runs SaaS only"),
        "pa": ("n", "SaaS through Strata Cloud Manager"),
        "zs": ("p", "On-prem in Enterprise tier. Air-gap not stated"),
    }),
    ("Continuous testing", "Retests without a person starting each scan", {
        "ak": ("y", "Cron schedules, rescan on model change"),
        "hl": ("y", "Scheduled or ad hoc scans"),
        "mg": ("y", "Continuous reruns, CI/CD, GitHub"),
        "lk": ("n", "Not stated in red teaming docs"),
        "pa": ("n", "Not stated in scan docs"),
        "zs": ("y", "CI/CD pipelines and REST API"),
    }),
    ("Findings you can act on", "Evidence plus a path to the fix", {
        "ak": ("y", "Prompt, response, Ask AI fix steps, export"),
        "hl": ("y", "Guardrail advice and trend metrics"),
        "mg": ("y", "Evidence, fix guidance, one-click retest"),
        "lk": ("y", "Repro steps, fix guidance, review call"),
        "pa": ("p", "Risk score. Fix steps not stated"),
        "zs": ("y", "Prompt Hardening, Jira, ServiceNow"),
    }),
]

PTS = {"y": 2, "p": 1, "n": 0}
LABEL = {"y": "Yes", "p": "Partial", "n": "Not stated"}
MAX = 2 * len(CRITERIA)

VERDICT = {
    "ak": "30,000+ probes, intelligent probes, air-gapped",
    "mg": "Multimodal testing, no attack count",
    "zs": "8 frameworks, conflicting probe counts",
    "lk": "85M+ prompts, SaaS only",
    "hl": "Predictive ML, no deployment stated",
    "pa": "500+ vectors, SaaS only",
}


def scores():
    return {k: sum(PTS[c[2][k][0]] for c in CRITERIA) for k, _n, _p in VENDORS}


def ranked():
    s = scores()
    order = sorted(VENDORS, key=lambda v: (-s[v[0]], v[1]))
    res, prev, rank = [], None, 0
    for i, v in enumerate(order):
        if s[v[0]] != prev:
            rank, prev = i + 1, s[v[0]]
        tie = sum(1 for w in order if s[w[0]] == s[v[0]]) > 1
        res.append((rank, tie, v, s[v[0]]))
    return res


def mark(state, size="4.2mm"):
    if state == "y":
        body = ('<circle cx="8" cy="8" r="8" fill="%s"/><path d="M4.3 8.2 6.8 10.7 '
                '11.8 5.4" stroke="#fff" stroke-width="2" fill="none" '
                'stroke-linecap="round" stroke-linejoin="round"/>' % GREEN)
    elif state == "p":
        body = ('<circle cx="8" cy="8" r="8" fill="%s"/><path d="M4.9 8 11.1 8" '
                'stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/>' % SEC)
    else:
        body = ('<circle cx="8" cy="8" r="6.8" fill="#fff" stroke="%s" stroke-width="2.4"/>'
                '<path d="M5.6 8 10.4 8" stroke="%s" stroke-width="2" stroke-linecap="round"/>'
                % (RED, RED))
    return ('<svg class="mk" style="width:%s;height:%s" viewBox="0 0 16 16">%s</svg>'
            % (size, size, body))


# --------------------------------------------------------------------------
# head to head: vendor, where the vendor leads, where AccuKnox leads, POC question
# --------------------------------------------------------------------------
H2H = [
    ("HiddenLayer",
     ["Human-led red team services", "Predictive ML model testing"],
     ["Framework mapping in the product", "On-premises and air-gapped deployment"],
     "Does OWASP mapping need a services contract?"),
    ("Mindgard",
     ["150+ disclosed AI vulnerabilities", "Image, audio and multimodal testing"],
     ["30,000+ probes, a published count", "Air-gapped deployment"],
     "How many attacks run in a standard scan?"),
    ("Lakera",
     ["85M+ Gandalf adversarial prompts", "Expert-validated findings"],
     ["Self-hosted red teaming", "Scheduled scans"],
     "Can automated red teaming run self-hosted?"),
    ("Palo Alto Networks",
     ["500+ vectors, refreshed every two weeks", "Multi-agent testing"],
     ["On-premises and air-gapped deployment", "EU AI Act and ISO 42001 tags"],
     "Can red teaming run without Strata Cloud Manager?"),
    ("Zscaler",
     ["8 compliance frameworks", "Prompt Hardening from findings"],
     ["Air-gapped deployment", "One consistent probe count"],
     "Is a standard scan 25+ probes or 5,000+?"),
]

# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------
PAN_DOCS = ("https://docs.paloaltonetworks.com/ai-runtime-security/ai-red-teaming/"
            "identify-ai-system-risks-with-ai-red-teaming/get-started-with-prisma-airs-ai-red-teaming")
SOURCES = [
    ("AccuKnox", [
        ("help.accuknox.com/use-cases/red-teaming", "https://help.accuknox.com/use-cases/red-teaming/"),
        ("help.accuknox.com/getting-started/3.6-release", "https://help.accuknox.com/getting-started/3.6-release/"),
        ("help.accuknox.com/how-to/aiml-saas-vs-onprem", "https://help.accuknox.com/how-to/aiml-saas-vs-onprem/"),
        ("AccuKnox product team, September 2026", ""),
    ]),
    ("HiddenLayer", [
        ("hiddenlayer.com/platform/ai-attack-simulation", "https://www.hiddenlayer.com/platform/ai-attack-simulation"),
        ("hiddenlayer.com/solutions/red-teaming", "https://www.hiddenlayer.com/solutions/red-teaming"),
        ("hiddenlayer.com/services", "https://www.hiddenlayer.com/services"),
    ]),
    ("Mindgard", [
        ("mindgard.ai/automated-ai-red-teaming", "https://mindgard.ai/automated-ai-red-teaming"),
        ("mindgard.ai/ai-attack-library", "https://mindgard.ai/ai-attack-library"),
        ("mindgard.ai/compare/mindgard-vs-promptfoo", "https://mindgard.ai/compare/mindgard-vs-promptfoo"),
    ]),
    ("Lakera", [
        ("lakera.ai/ai-red-teaming", "https://www.lakera.ai/ai-red-teaming"),
        ("lakera.ai/ai-red-teaming-services", "https://www.lakera.ai/ai-red-teaming-services"),
        ("docs.lakera.ai/red", "https://docs.lakera.ai/red"),
        ("docs.lakera.ai/docs/selfhosting", "https://docs.lakera.ai/docs/selfhosting"),
    ]),
    ("Palo Alto Networks", [
        ("paloaltonetworks.com/ai-security/ai-red-teaming", "https://www.paloaltonetworks.com/ai-security/ai-red-teaming"),
        ("Prisma AIRS AI Red Teaming docs", PAN_DOCS),
        ("Prisma AIRS docs, Start a Scan", PAN_DOCS + "/scans/start-a-scan"),
    ]),
    ("Zscaler", [
        ("zscaler.com, Automated AI Red Teaming", "https://www.zscaler.com/products-and-solutions/continuous-automated-red-teaming"),
        ("zscaler.com, SPLX acquisition", "https://www.zscaler.com/press/zscaler-secures-enterprise-ai-lifecycle-acquisition-innovative-ai-security-pioneer-splx"),
        ("splx.ai/pricing", "https://splx.ai/pricing"),
    ]),
]

GALLERY = [
    ("getting-started/images/release-notes/v3.6/redteam-assets-page.png", "Models and Scan Risk"),
    ("getting-started/images/release-notes/v3.6/redteam-model-purpose.png", "Intelligent Scan by Model Purpose"),
    ("getting-started/images/release-notes/v3.6/redteam-scan-configurations.png", "Scan Configurations Across Models"),
    ("how-to/image-22.png", "Ask AI Remediation With OWASP Tags"),
]
DOCS = r"D:\Atharva\AccuKnox\HelpDocs\docs"


def img(path, width=1500):
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# --------------------------------------------------------------------------
CSS = """
@page { size: A4 landscape; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { font-family: 'Space Grotesk', 'Inter', 'Segoe UI', sans-serif; color: INK;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: BLUE; text-decoration: none; }
.pg { width: 297mm; height: 210mm; padding: 11mm 13mm; position: relative;
  page-break-after: always; break-after: page; overflow: hidden; }
.pg:last-child { page-break-after: auto; break-after: auto; }
.hd { display: flex; justify-content: space-between; align-items: center;
  border-bottom: 3px solid BLUE; padding-bottom: 2.2mm; margin-bottom: 4.4mm; }
.hd h2 { font-size: 24pt; font-weight: 700; color: NAVY; line-height: 1.1; }
.hd img { height: 6.4mm; }
.mk { display: inline-block; vertical-align: middle; }

/* page 1 */
.band { background: NAVY; color: #fff; border-radius: 3mm; padding: 6mm 9mm;
  display: flex; justify-content: space-between; align-items: center; }
.band h1 { font-size: 30pt; font-weight: 700; line-height: 1.05; }
.band img { height: 9mm; }
.p1 { display: grid; grid-template-columns: 1fr 1.25fr; gap: 8mm; margin-top: 6mm; height: 128mm; }
.win { background: BLUE; color: #fff; border-radius: 3mm; padding: 7mm 8mm; display: flex;
  flex-direction: column; justify-content: space-between; }
.win .tag { font-size: 11pt; font-weight: 700; letter-spacing: 2px; color: #CFE0FF; }
.win .nm { font-size: 40pt; font-weight: 700; line-height: 1; margin-top: 3mm; }
.win .sc { font-size: 80pt; font-weight: 700; line-height: 1; margin-top: 5mm; }
.win .sc small { font-size: 24pt; color: #CFE0FF; }
.win ul { list-style: none; margin-top: 5mm; }
.win li { font-size: 14pt; line-height: 1.35; padding: 2.4mm 0; border-top: 1px solid rgba(255,255,255,.25); }
.win li b { color: #fff; }
.rest { list-style: none; display: flex; flex-direction: column; height: 118mm; justify-content: space-between; }
.rest li { display: grid; grid-template-columns: 11mm 1fr 44mm; align-items: center; gap: 3mm;
  padding: 2mm 0; border-bottom: 1px solid GREY_BD; flex: 1; }
.rest .no { font-size: 22pt; font-weight: 700; color: MUTE; text-align: center; }
.rest .vn { font-size: 17pt; font-weight: 700; color: INK; }
.rest .vd { font-size: 11.5pt; color: MUTE; margin-top: .6mm; }
.rest .sc { font-size: 19pt; font-weight: 700; color: NAVY; text-align: right; }
.rest .sc small { font-size: 10pt; color: MUTE; }
.bar { height: 2.4mm; background: GREY_BG; border-radius: 2mm; margin-top: 1.2mm; overflow: hidden; }
.bar i { display: block; height: 100%; background: GREY_BD; }
.legend { display: flex; gap: 5mm; font-size: 11pt; color: MUTE; margin-top: 3mm; align-items: center; }
.scope { margin-top: 6mm; background: LAV; border-left: 5px solid BLUE; border-radius: 2.4mm; padding: 4mm 6mm; font-size: 12.5pt; color: NAVY; }
.scope b { font-weight: 700; }
.legend span { display: flex; align-items: center; gap: 1.4mm; }

/* matrix */
table.mx { width: 100%; border-collapse: collapse; table-layout: fixed; }
.mx th { background: NAVY; color: #fff; font-size: 11pt; font-weight: 700; padding: 2mm; text-align: left; }
.mx th.ak { background: BLUE; font-size: 12.5pt; }
.mx td { border-bottom: 1px solid GREY_BD; padding: 1.5mm 1.8mm; vertical-align: top; font-size: 9.4pt;
  line-height: 1.24; color: #3A4064; }
.mx td.cr { font-size: 10.8pt; font-weight: 700; color: NAVY; }
.mx td.ak { background: LAV; color: NAVY; font-weight: 600; border-left: 2px solid BLUE; border-right: 2px solid BLUE; }
.mx .c { display: flex; gap: 1.6mm; align-items: flex-start; }
.mx .c .mk { flex: none; margin-top: .2mm; }
.mx tr.tot td { font-size: 14pt; font-weight: 700; color: NAVY; background: GREY_BG; border-bottom: none; }
.mx tr.tot td.ak { background: BLUE; color: #fff; border-bottom: 2px solid BLUE; }

/* accuknox */
.three { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; height: 112mm; }
.card { border-radius: 3mm; overflow: hidden; border: 1px solid GREY_BD; }
.card .top { background: NAVY; color: #fff; padding: 7mm 6mm 6mm; }
.card:nth-child(1) .top { background: BLUE; }
.card:nth-child(2) .top { background: SEC; }
.card .big { font-size: 40pt; font-weight: 700; line-height: 1; }
.card h3 { font-size: 16pt; font-weight: 700; margin-top: 2mm; color: #E6ECFF; }
.card ul { list-style: none; padding: 5mm 6mm; }
.card li { font-size: 14pt; line-height: 1.35; color: INK; padding: 2.2mm 0 2.2mm 5.5mm; position: relative; }
.card li:before { content: ""; position: absolute; left: 0; top: 3.4mm; width: 2mm; height: 2mm;
  border-radius: 50%; background: BLUE; }
.card li:before { top: 4.6mm; }
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; margin-top: 7mm; }
.step { background: TINT; border: 1px solid GREY_BD; border-top: 4px solid NAVY; border-radius: 2.4mm; padding: 6mm 5mm; }
.step b { display: flex; width: 8mm; height: 8mm; border-radius: 50%; background: NAVY; color: #fff;
  align-items: center; justify-content: center; font-size: 12pt; }
.step p { font-size: 14pt; font-weight: 600; color: NAVY; margin-top: 2.2mm; line-height: 1.3; }

.gal { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 5mm; height: 164mm; }
.gal figure { border: 1px solid GREY_BD; border-radius: 3mm; overflow: hidden; display: flex; flex-direction: column; background: #fff; }
.gal img { width: 100%; flex: 1; min-height: 0; object-fit: cover; object-position: top left; display: block; }
.gal img.bottom { object-position: center bottom; }
.gal figcaption { background: NAVY; color: #fff; font-size: 12pt; font-weight: 700; padding: 2.6mm 4mm;
  display: flex; gap: 3mm; align-items: center; }
.gal figcaption i { font-style: normal; background: BLUE; border-radius: 50%; width: 7mm; height: 7mm;
  display: flex; align-items: center; justify-content: center; font-size: 10.5pt; }

.two { display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; height: 164mm; }
.panel { background: TINT; border: 1px solid GREY_BD; border-radius: 3mm; padding: 6mm; }
h3.sub { font-size: 16pt; color: NAVY; margin-bottom: 4mm; }
.chips { display: flex; flex-wrap: wrap; gap: 2.4mm; }
.chip { font-size: 14pt; background: LAV; color: NAVY; font-weight: 600; border-radius: 2mm; padding: 2.6mm 4mm; }
.chip.fw { background: BLUE; color: #fff; }
.chip.st { background: #fff; color: INK; font-weight: 500; border: 1px solid GREY_BD; }
.gap { margin-top: 10mm; }
.weak { margin-top: 10mm; background: #fff; border: 1px solid GREY_BD; border-left: 5px solid MUTE; border-radius: 2.4mm; padding: 4mm 5mm; }
.weak h3 { font-size: 16pt; color: MUTE; }
.weak ul { margin: 2mm 0 0 5mm; }
.weak li { font-size: 14pt; line-height: 1.5; color: #3A4064; }

table.hh { width: 100%; border-collapse: collapse; table-layout: fixed; }
.hh th { background: NAVY; color: #fff; font-size: 13.5pt; padding: 3.6mm; text-align: left; }
.hh th.ak { background: BLUE; }
.hh td { border-bottom: 1px solid GREY_BD; padding: 5.4mm 3.4mm; vertical-align: top; font-size: 13pt; line-height: 1.35; color: #3A4064; }
.hh td.v { font-size: 16pt; font-weight: 700; color: NAVY; }
.hh td.ak { background: LAV; color: NAVY; font-weight: 600; border-left: 2px solid BLUE; border-right: 2px solid BLUE; }
.hh ul { list-style: none; }
.hh li { padding-left: 4.4mm; position: relative; }
.hh li + li { margin-top: 1.2mm; }
.hh li:before { content: ""; position: absolute; left: 0; top: 2.6mm; width: 2mm; height: 2mm; border-radius: 50%; background: MUTE; }
.hh td.ak li:before { background: BLUE; }
.hh td.q { color: NAVY; font-style: italic; }

.mods { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3.4mm; }
.mod { background: TINT; border: 1px solid GREY_BD; border-top: 4px solid BLUE; border-radius: 2.4mm; padding: 5.4mm 5mm; }
.mod b { display: block; font-size: 15pt; color: NAVY; }
.mod span { display: block; font-size: 12pt; color: #3A4064; line-height: 1.35; margin-top: 1mm; }
.srcs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm 6mm; margin-top: 3mm; }
.srcs h4 { font-size: 11.5pt; color: NAVY; margin-bottom: .6mm; }
.srcs li { font-size: 9.8pt; line-height: 1.4; list-style: none; color: #3A4064; }
.cta { margin-top: 9mm; background: NAVY; color: #fff; border-radius: 3mm; padding: 5mm 7mm;
  display: flex; justify-content: space-between; align-items: center; }
.cta b { font-size: 16pt; }
.cta span { font-size: 12pt; color: #CBD7FA; margin-left: 5mm; }
.cta img { height: 8mm; }
"""
for _k, _v in (("GREY_BG", GREY_BG), ("GREY_BD", GREY_BD), ("TINT", TINT), ("LAV", LAV),
               ("INK", INK), ("NAVY", NAVY), ("BLUE", BLUE), ("SEC", SEC),
               ("RED", RED), ("GREEN", GREEN), ("MUTE", MUTE)):
    CSS = CSS.replace(_k, _v)


def hd(title):
    return '<div class="hd"><h2>%s</h2><img src="%s" alt="AccuKnox"></div>' % (title, LOGO_LIGHT)


def page1():
    s = scores()
    rest = []
    for rank, tie, (k, name, _prod), sc in ranked():
        if k == "ak":
            continue
        rest.append('<li><div class="no">%d</div><div><div class="vn">%s</div><div class="vd">%s</div></div>'
                    '<div><div class="sc">%d<small> / %d</small></div><div class="bar"><i style="width:%.0f%%"></i></div></div></li>'
                    % (rank, name, VERDICT[k], sc, MAX, 100.0 * sc / MAX))
    legend = "".join('<span>%s%s %d</span>' % (mark(x, "4mm"), LABEL[x], PTS[x]) for x in "ypn")
    return """
<section class="pg">
  <div class="band"><h1>AI Red Teaming Stack Ranking</h1><img src="{logo}" alt="AccuKnox"></div>
  <div class="p1">
    <div class="win">
      <div><div class="tag">RANK 1</div><div class="nm">AccuKnox</div>
        <div class="sc">{ak}<small> / {mx}</small></div></div>
      <ul>
        <li><b>30,000+</b> probes across 20+ categories</li>
        <li><b>Intelligent</b> probes from your industry context</li>
        <li><b>Air-gapped</b> on-premises deployment</li>
        <li><b>7</b> compliance frameworks tagged</li>
      </ul>
    </div>
    <div>
      <ul class="rest">{rest}</ul>
      <div class="legend">{legend}<span>8 criteria, equal weight</span></div>
    </div>
  </div>
  <div class="scope"><b>Red teaming only.</b> AccuKnox also ships AI-SPM, AI-DR, Prompt Firewall, Model and Dataset Security, Agentic AI Security and CTEM.</div>
</section>""".format(logo=LOGO_DARK, ak=s["ak"], mx=MAX, rest="".join(rest), legend=legend)


def page2():
    head = "".join('<th class="%s">%s</th>' % ("ak" if k == "ak" else "", n) for k, n, _p in VENDORS)
    body = []
    for name, _hint, cells in CRITERIA:
        tds = "".join('<td class="%s"><div class="c">%s<span>%s</span></div></td>'
                      % ("ak" if k == "ak" else "", mark(cells[k][0], "4mm"), cells[k][1])
                      for k, _n, _p in VENDORS)
        body.append('<tr><td class="cr">%s</td>%s</tr>' % (name, tds))
    s = scores()
    tot = "".join('<td class="%s">%d / %d</td>' % ("ak" if k == "ak" else "", s[k], MAX) for k, _n, _p in VENDORS)
    body.append('<tr class="tot"><td>Score</td>%s</tr>' % tot)
    legend = "".join('<span>%s%s</span>' % (mark(x, "4mm"), LABEL[x]) for x in "ypn")
    return """
<section class="pg">
  {hd}
  <table class="mx"><colgroup><col style="width:13.6%">{cols}</colgroup>
    <thead><tr><th>Criterion</th>{head}</tr></thead><tbody>{body}</tbody></table>
</section>""".format(hd=hd("Capability Matrix"), cols='<col style="width:14.4%">' * 6,
                     head=head, body="".join(body), legend=legend)


def page3():
    return """
<section class="pg">
  {hd}
  <div class="three">
    <div class="card"><div class="top"><div class="big">30,000+</div><h3>Static Red Teaming</h3></div><ul>
      <li>30,000+ probes, 20+ categories</li>
      <li>Standard policy packs</li>
      <li>OWASP Top 10 for LLMs</li></ul></div>
    <div class="card"><div class="top"><div class="big">Custom</div><h3>Intelligent Red Teaming</h3></div><ul>
      <li>Probes built from your industry context</li>
      <li>JSON upload, document upload or direct input</li>
      <li>Presets for support, coding and legal</li></ul></div>
    <div class="card"><div class="top"><div class="big">3 Options</div><h3>Deployment Flexibility</h3></div><ul>
      <li>SaaS</li>
      <li>Private cloud</li>
      <li>Customer-managed on-premises, air-gapped</li></ul></div>
  </div>
  <div class="steps">
    <div class="step"><b>1</b><p>Pick Static or Intelligent Scan</p></div>
    <div class="step"><b>2</b><p>Add model purpose or context</p></div>
    <div class="step"><b>3</b><p>Review generated probes</p></div>
    <div class="step"><b>4</b><p>Schedule and rescan</p></div>
  </div>
</section>""".format(hd=hd("AccuKnox AI Red Teaming"))


def page4():
    figs = "".join('<figure><img class="%s" src="%s" alt="%s"><figcaption><i>%d</i>%s</figcaption></figure>'
                   % ("bottom" if "prompt-categories" in p else "", img(os.path.join(DOCS, p)), c, i + 1, c)
                   for i, (p, c) in enumerate(GALLERY))
    return '<section class="pg">%s<div class="gal">%s</div></section>' % (hd("AccuKnox Red Teaming Gallery"), figs)


def page5():
    cats = ("Prompt Injection", "Jailbreaks", "RAG Poisoning", "MCP and Agent Abuse", "PII Leakage",
            "Financial Hallucination", "Malware Generation", "Package Hallucination", "Toxicity", "Bias")
    strat = ("Encoding", "Crescendo Multi-Turn", "Multilingual", "Many-Shot", "Role-Play Framing")
    fw = ("OWASP LLM Top 10", "OWASP API Top 10", "MITRE ATLAS", "NIST AI RMF", "EU AI Act", "ISO/IEC 42001", "AVID")
    chip = lambda xs, c: "".join('<span class="chip %s">%s</span>' % (c, x) for x in xs)
    return """
<section class="pg">
  {hd}
  <div class="two">
    <div class="panel">
      <h3 class="sub">Attack Categories</h3><div class="chips">{cats}</div>
      <h3 class="sub gap">Attack Strategies</h3><div class="chips">{strat}</div>
    </div>
    <div class="panel">
      <h3 class="sub">Compliance Frameworks</h3><div class="chips">{fw}</div>
      <div class="weak"><h3>Gaps to Know</h3><ul>
        <li>Image and audio attacks not stated</li>
        <li>No human-led red team service</li>
        <li>No published library refresh cadence</li></ul></div>
    </div>
  </div>
</section>""".format(hd=hd("Attack Coverage and Compliance"), cats=chip(cats, ""),
                     strat=chip(strat, "st"), fw=chip(fw, "fw"))


def page6():
    rows = "".join(
        '<tr><td class="v">%s</td><td><ul>%s</ul></td><td class="ak"><ul>%s</ul></td><td class="q">%s</td></tr>'
        % (n, "".join("<li>%s</li>" % x for x in lead), "".join("<li>%s</li>" % x for x in ak), q)
        for n, lead, ak, q in H2H)
    return """
<section class="pg">
  {hd}
  <table class="hh"><colgroup><col style="width:16%"><col style="width:28%"><col style="width:28%"><col style="width:28%"></colgroup>
    <thead><tr><th>Vendor</th><th>Vendor Strengths</th><th class="ak">AccuKnox Advantage</th><th>POC Question</th></tr></thead>
    <tbody>{rows}</tbody></table>
</section>""".format(hd=hd("Head to Head"), rows=rows)


def page7():
    mods = [("AI-SPM", "AI asset discovery across clouds"),
            ("AI-DR", "AI threat detection and response"),
            ("Prompt Firewall", "Runtime prompt guardrails"),
            ("Model and Dataset Security", "Model file and PII scans"),
            ("Agentic AI Security", "Agent and MCP sandboxing"),
            ("AI Pen Testing and CTEM", "Continuous threat exposure"),
            ("Shadow AI Defense", "Unsanctioned AI discovery"),
            ("AI Model Cards", "Per-model governance")]
    mod = "".join('<div class="mod"><b>%s</b><span>%s</span></div>' % m for m in mods)
    src = "".join('<div><h4>%s</h4><ul>%s</ul></div>' % (v, "".join(
        '<li>%s</li>' % (('<a href="%s">%s</a>' % (u, t)) if u else t) for t, u in links))
        for v, links in SOURCES)
    return """
<section class="pg">
  {hd}
  <div class="mods">{mod}</div>
  <h3 class="sub" style="margin-top:7mm">Sources</h3>
  <div class="srcs">{src}</div>
  <div class="cta"><div><b>See AccuKnox Red Teaming Live</b><span>accuknox.com  \u00b7  support@accuknox.com</span></div><img src="{logo}" alt="AccuKnox"></div>
</section>""".format(hd=hd("More AccuKnox AI Security Modules"), mod=mod, src=src, logo=LOGO_DARK)


def build_html():
    return ("<!doctype html><meta charset='utf-8'><title>AI Red Teaming Stack Ranking</title>"
            "<style>%s</style>%s" % (CSS, "".join(f() for f in (page1, page2, page3, page4, page5, page6, page7))))


def main():
    os.makedirs(WORK, exist_ok=True)
    html_path = os.path.join(WORK, NAME + ".html")
    pdf_path = os.path.join(OUT, NAME + ".pdf")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_html())
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=" + pdf_path, html_path.replace("\\", "/")],
                   check=True, timeout=300)
    for rank, tie, v, sc in ranked():
        print(rank, "T" if tie else " ", v[1], sc)
    print("wrote %s (%.2f MB)" % (pdf_path, os.path.getsize(pdf_path) / 1e6))


if __name__ == "__main__":
    sys.exit(main())
