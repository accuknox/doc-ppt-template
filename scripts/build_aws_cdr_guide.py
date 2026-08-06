"""Build an AccuKnox-branded PDF of the AWS CDR Manual Deployment Guide.

Source is a Confluence MHTML export (`.doc`) that carries both the prose and the
screenshots. This script pulls the HTML and the embedded PNGs out of the MIME
container, rewrites them into brand-styled HTML with a cover page and a roadmap
page, prints to PDF with headless Edge, then stamps the running header, footer
and page numbers on every body page with PyMuPDF.

Run: py -3.11 scripts/build_aws_cdr_guide.py
"""
import base64
import email
import io
import os
import re
import subprocess
import sys
from email import policy

import fitz
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DOC = r"C:\Users\AtharvaShah\Downloads\AWS+CDR+Deployment+Guide.doc"
OUTDIR = os.path.join(REPO, "output")
WORK = os.path.join(OUTDIR, "awscdr")
HTML_OUT = os.path.join(WORK, "AccuKnox_AWS_CDR_Deployment_Guide.html")
PDF_RAW = os.path.join(WORK, "_raw.pdf")
PDF_OUT = os.path.join(OUTDIR, "AccuKnox_AWS_CDR_Deployment_Guide.pdf")

LOGO_DARK = os.path.join(REPO, "assets", "logos", "accuknox-logo-dark-bg.png")
LOGO_LIGHT = os.path.join(REPO, "assets", "logos", "accuknox-logo-light-bg.png")
EMBLEM = os.path.join(REPO, "assets", "logos", "accuknox-emblem.png")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

FONTDIR = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Windows", "Fonts")
FONTS = {
    400: "SpaceGrotesk-Regular.ttf",
    500: "SpaceGrotesk-Medium.ttf",
    600: "SpaceGrotesk-SemiBold.ttf",
    700: "SpaceGrotesk-Bold.ttf",
}
MONO = "SpaceMono-Regular.ttf"
MONO_BOLD = "SpaceMono-Bold.ttf"

NAVY = "#11206D"
BLUE = "#0046FF"
SEC_BLUE = "#6464FF"
RED = "#C80019"
DEEP_NAVY = "#0000C8"

DOC_TITLE = "AWS CDR Deployment Guide"
DOC_SUB = "Standalone AWS Account"
DOC_DATE = "August 2026"
DOC_VER = "1.1"

# Screenshots the export embedded at 250 px tall. Upscale factor applied before
# printing so the glyph edges survive rasterisation at print size.
UPSCALE = 2
# Target print width in mm for a screenshot of a given pixel width.
CONTENT_MM = 178.0


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def font_face(name, weight, filename, style="normal"):
    path = os.path.join(FONTDIR, filename)
    if not os.path.exists(path):
        path = os.path.join(r"C:\Windows\Fonts", filename)
    return (
        "@font-face{font-family:'%s';font-style:%s;font-weight:%d;"
        "src:url(data:font/ttf;base64,%s) format('truetype');}"
        % (name, style, weight, b64(path))
    )


def load_mhtml(path):
    """Return (html_text, {content_location_key: png_bytes})."""
    msg = email.message_from_binary_file(open(path, "rb"), policy=policy.default)
    html_text = None
    blobs = {}
    for part in msg.walk():
        ctype = part.get_content_type()
        if ctype.startswith("multipart/"):
            continue
        data = part.get_payload(decode=True)
        if data is None:
            continue
        if ctype == "text/html":
            html_text = data.decode("utf-8", errors="replace")
            continue
        loc = (part.get("Content-Location") or "").strip()
        key = loc.rsplit("/", 1)[-1]
        if key:
            blobs[key] = data
    if html_text is None:
        raise SystemExit("no text/html part found in %s" % path)
    return html_text, blobs


def prep_image(data):
    """Upscale + sharpen a thumbnail screenshot, return (data_uri, w, h)."""
    im = Image.open(io.BytesIO(data))
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    w, h = im.size
    if w * h > 1024:  # skip the 16x16 expand-control icon
        im = im.resize((w * UPSCALE, h * UPSCALE), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=3))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), w, h


def set_html(soup, name, inner, cls=None):
    """Build a new tag whose children come from an HTML fragment."""
    tag = soup.new_tag(name)
    if cls:
        tag["class"] = cls
    frag = BeautifulSoup(inner, "lxml")
    holder = frag.body or frag
    for child in list(holder.contents):
        if getattr(child, "name", None) == "p":
            for sub in list(child.contents):
                tag.append(sub.extract())
        else:
            tag.append(child.extract())
    return tag


DASH = re.compile(r"\s*[\u2013\u2014]\s*")


def clean_heading(text):
    """Normalise the 'Step 1 - Title' separator to a period, per brand voice."""
    text = text.strip()
    text = re.sub(r"^(Step\s+\d+|Use Case\s+\d+)" + DASH.pattern, r"\1. ", text)
    text = DASH.sub(", ", text)
    text = re.sub(r"\s+", " ", text)
    return text.rstrip(":").strip()


STEPS = [
    ("01", "Create the Lambda execution IAM role",
     "An execution role Lambda can assume, with CloudWatch Logs write access."),
    ("02", "Add the S3 read inline policy",
     "Scoped s3:GetObject on the CloudTrail log bucket only."),
    ("03", "Create the Lambda function",
     "Python 3.10 function on x86_64, wired to the execution role."),
    ("04", "Upload the Lambda function code",
     "The forwarder that unzips, batches and POSTs CloudTrail records."),
    ("05", "Configure Lambda environment variables",
     "Ingestion URL and Basic Auth credentials from the AccuKnox team."),
    ("06", "Configure the Amazon S3 trigger",
     "ObjectCreated notifications invoke the function on every new log file."),
    ("07", "Validate the Lambda invocation",
     "Read the CloudWatch log stream and confirm batches were posted."),
    ("08", "Verify CloudTrail logs in the SIEM UI",
     "Filter on cloud = aws and confirm events are searchable."),
    ("09", "Configure the GitHub remediation repository",
     "Actions workflow plus repository secrets for the target cloud."),
    ("10", "Verify alerts in the AccuKnox platform",
     "Confirm CDR alerts fire for the rules you plan to remediate."),
    ("11", "Configure the GitHub webhook integration",
     "Repository Dispatch call that starts the remediation workflow."),
    ("12", "Review the out-of-the-box AWS rules",
     "Seven pre-built detections, each with an automated response."),
]

RULES_COUNT = 7

USECASES = [
    ("Public S3 buckets", "Block Public Access re-enabled by Cloud Custodian."),
    ("Exposed security group ports", "Inbound 0.0.0.0/0 rule revoked automatically."),
    ("EC2 with public IPs", "Public IP disassociated, instance keeps running."),
]

FLOW = ["CloudTrail", "Amazon S3", "Lambda forwarder", "AccuKnox CDR",
        "Automated response"]

# High-level deployment architecture, redrawn from the source diagram so it stays
# sharp in print. (label, note, zone)
ARCH = [
    ("AWS Account", "The account you are onboarding", "aws"),
    ("AWS CloudTrail", "Management API activity captured as events", "aws"),
    ("Amazon S3", "Trail delivers gzipped log files to the bucket", "aws"),
    ("Lambda Forwarder", "ObjectCreated fires, records batched as NDJSON and POSTed", "aws"),
    ("AccuKnox CDR", "Cloud Detection and Response ingests the events", "ak"),
    ("Detection and Alerts", "Pre-built rules match, CDR alerts are raised", "ak"),
    ("Automated Response", "Review, isolate, remediate through GitHub Actions", "ak"),
]


ZONE_LABEL = {"aws": "In your AWS account", "ak": "AccuKnox platform"}


def arch_diagram():
    """Vertical flow, grouped into the AWS-side and AccuKnox-side zones."""
    groups = []
    for label, note, zone in ARCH:
        if not groups or groups[-1][0] != zone:
            groups.append((zone, []))
        groups[-1][1].append((label, note))

    out = []
    for gi, (zone, nodes) in enumerate(groups):
        if gi:
            out.append('<div class="astem zonestem"></div>')
        rows = []
        for i, (label, note) in enumerate(nodes):
            if i:
                rows.append('<div class="astem"></div>')
            rows.append('<div class="anode"><div class="al">%s</div>'
                        '<div class="an">%s</div></div>' % (label, note))
        out.append('<div class="azone %s"><div class="azlabel">%s</div>'
                   '<div class="acol">%s</div></div>'
                   % (zone, ZONE_LABEL[zone], "".join(rows)))
    return '<div class="arch">%s</div>' % "".join(out)


def flow_strip(dark=False):
    out = []
    for i, node in enumerate(FLOW):
        if i:
            out.append('<span class="farrow"></span>')
        cls = "fchip last" if i == len(FLOW) - 1 else "fchip"
        out.append('<span class="%s">%s</span>' % (cls, node))
    return '<div class="flowline%s">%s</div>' % (
        " dark" if dark else "", "".join(out))


def build_body(html_text, blobs):
    """Rewrite the Confluence HTML into brand-styled markup. Returns (html, n_figs)."""
    soup = BeautifulSoup(html_text, "lxml")
    root = soup.find("div", class_="Section1") or soup.body

    # Drop the page title heading; the cover carries it.
    h1 = root.find("h1")
    if h1 and "AWS CDR Manual Deployment" in h1.get_text():
        h1.decompose()

    # Swap the ASCII architecture block for the brand flow strip, and drop the
    # source's step list: it numbered the bucket and trail as steps 1 and 2, which
    # collides with the body's own numbering, and the roadmap page already lists them.
    for h in list(root.find_all(["h1", "h2", "h3"])):
        label = h.get_text(" ", strip=True).strip().lower()
        if label not in ("deployment architecture", "deployment steps"):
            continue
        node = h.find_next_sibling()
        while node is not None and getattr(node, "name", None) not in (
                "h1", "h2", "h3", None):
            nxt = node.find_next_sibling()
            node.decompose()
            node = nxt
        if label == "deployment architecture":
            h.string = "High-Level Deployment Architecture"
            h.insert_after(set_html(soup, "div", arch_diagram(), cls="archwrap"))
        else:
            h.decompose()

    # Keep the prerequisite prose in step with the relabelled headings.
    for p in list(root.find_all("p")):
        txt = p.get_text()
        if "you can skip Step 1" in txt:
            p.replace_with(set_html(soup, "p",
                "If you already have an <strong>Amazon S3 bucket</strong> and an "
                "<strong>AWS CloudTrail</strong> trail configured, skip the two "
                "prerequisite steps below and start at Step 1, the Lambda execution "
                "IAM role."))
        elif "expand the section below" in txt:
            p.replace_with(set_html(soup, "p",
                "Already have both? Use the section below only to check the existing "
                "configuration. Otherwise follow its two prerequisite steps to create "
                "the bucket and the trail."))
        elif "Before proceeding to" in txt and "Step 3" in txt:
            p.replace_with(set_html(soup, "p",
                "<strong>Note:</strong> Before you start Step 1, check that your "
                "existing CloudTrail trail delivers logs to the existing Amazon S3 "
                "bucket.", cls="note"))

    # Unwrap the collapsed prerequisite macro into a labelled optional section.
    for cont in root.select("div.expand-container"):
        ctrl = cont.find("div", class_="expand-control")
        label = ctrl.get_text(" ", strip=True) if ctrl else "Optional section"
        content = cont.find("div", class_="expand-content")
        if ctrl:
            ctrl.decompose()
        wrap = soup.new_tag("section")
        wrap["class"] = "optional"
        bar = soup.new_tag("div")
        bar["class"] = "optional-bar"
        tag = soup.new_tag("span")
        tag["class"] = "optional-tag"
        tag.string = "Only if not already configured"
        bar.append(tag)
        head = soup.new_tag("span")
        head["class"] = "optional-title"
        head.string = clean_heading(label)
        bar.append(head)
        wrap.append(bar)
        if content:
            content.name = "div"
            content["class"] = "optional-body"
            wrap.append(content.extract())
        cont.replace_with(wrap)

    # Inside the optional section the source repeats "Step 1" / "Step 2", which
    # collide with the main sequence. Relabel them as prerequisite steps.
    for sec in root.select("section.optional"):
        for h in sec.find_all(["h1", "h2", "h3", "h4"]):
            txt = h.get_text(" ", strip=True)
            m = re.match(r"^Step\s+(\d+)", txt)
            if m:
                h.string = clean_heading("Prerequisite " + txt)

    # Normalise heading levels: "Step N." / "Use Case N." become h1 sections,
    # everything else drops to h2/h3 so the visual hierarchy is consistent.
    for h in root.find_all(["h1", "h2", "h3", "h4", "h5"]):
        txt = clean_heading(h.get_text(" ", strip=True))
        if not txt:
            h.decompose()
            continue
        top = re.match(r"^(Step\s+\d+\.|Use Case\s+\d+\.|Prerequisite Step\s+\d+\.)", txt)
        if top:
            h.name = "h1"
        elif h.name in ("h1", "h2"):
            h.name = "h2"
        else:
            h.name = "h3"
        h.clear()
        h.append(txt)
        if h.name == "h1":
            h["class"] = "step"

    # Two source phrasings use "ensure", which the brand writing rules ban.
    for node in root.find_all(string=re.compile(r"[Ee]nsures? ")):
        txt = str(node)
        fixed = txt.replace("Ensures CloudTrail log integrity",
                            "Confirms CloudTrail log integrity")
        fixed = re.sub(r"Ensure that the\b", "Confirm that the", fixed)
        fixed = re.sub(r"ensure that (your|the)\b", r"confirm that \1", fixed)
        fixed = fixed.replace(
            "to ensure continuous audit logging of AWS API activity",
            "so audit logging of AWS API activity keeps running")
        if fixed != txt:
            node.replace_with(fixed)

    # Callouts: paragraphs that open with "Note:" get a box.
    for p in root.find_all("p"):
        txt = p.get_text(" ", strip=True)
        if re.match(r"^(Note|Important|Warning)\s*:", txt):
            p["class"] = "note"

    # Result paragraphs read as outcomes, tint them.
    for h in root.find_all(["h2", "h3"]):
        if h.get_text(strip=True).lower().startswith("result"):
            h["class"] = "result-h"

    # Code blocks. Confluence wraps them in div.code > div.codeContent > pre.
    for div in root.select("div.code"):
        pre = div.find("pre")
        if pre is None:
            div.decompose()
            continue
        text = pre.get_text()
        new = soup.new_tag("pre")
        new["class"] = "code"
        # Short navigation breadcrumbs render better as a path chip than a block.
        lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
        if len(lines) <= 8 and all(len(l) < 70 for l in lines) and any(
                l.startswith(("\u2192", "->")) for l in lines):
            nav = soup.new_tag("div")
            nav["class"] = "nav"
            for i, line in enumerate(lines):
                chip = soup.new_tag("span")
                chip["class"] = "navchip"
                chip.string = line.lstrip("\u2192-> ").strip()
                if i:
                    arrow = soup.new_tag("span")
                    arrow["class"] = "navarrow"
                    nav.append(arrow)
                nav.append(chip)
            div.replace_with(nav)
            continue
        new.string = text.strip("\n")
        div.replace_with(new)

    # Tables: strip Confluence classes, keep structure, add zebra hook.
    for wrap in root.select("div.table-wrap"):
        wrap["class"] = "tbl"
    for t in root.select("table"):
        t.attrs = {}
        for cg in t.find_all("colgroup"):
            cg.decompose()
        for cell in t.find_all(["td", "th"]):
            cell.attrs = {}
        first = t.find("tr")
        if first and not t.find("thead"):
            ths = first.find_all("th")
            if ths:
                thead = soup.new_tag("thead")
                thead.append(first.extract())
                t.insert(0, thead)
        head_cell = t.find("th")
        if head_cell and head_cell.get_text(strip=True) == "Detection Rule":
            wrap = t.find_parent(class_="tbl")
            (wrap or t)["class"] = "tbl rules"

    # Images: swap in the extracted bytes, wrap in a captioned figure.
    figs = 0
    for span in root.select("span.confluence-embedded-file-wrapper"):
        span.unwrap()
    for img in root.find_all("img"):
        key = (img.get("src") or "").rsplit("/", 1)[-1]
        data = blobs.get(key)
        if data is None:
            img.decompose()
            continue
        uri, w, h = prep_image(data)
        if w * h <= 1024:  # expand-control icon
            img.decompose()
            continue
        figs += 1
        # Cap the print width so the upscaled pixels stay dense enough to read.
        native_mm = min(CONTENT_MM, w / 96.0 * 25.4 * 1.02)
        fig = soup.new_tag("figure")
        fig["class"] = "shot"
        new_img = soup.new_tag("img")
        new_img["src"] = uri
        new_img["style"] = "width:%.1fmm" % native_mm
        fig.append(new_img)
        cap = soup.new_tag("figcaption")
        cap.string = "Figure %d. %s" % (figs, figure_context(img))
        fig.append(cap)
        img.replace_with(fig)

    # Empty paragraphs left behind by the export.
    for p in root.find_all("p"):
        if not p.get_text(strip=True) and not p.find("img"):
            p.decompose()

    # Wrap each h1 step and its content in a section for page-break control.
    out = []
    current = None
    for el in list(root.children):
        if getattr(el, "name", None) == "h1":
            if current is not None:
                out.append(current)
            current = ['<section class="stepsec">', str(el)]
        elif current is not None:
            current.append(str(el))
        else:
            out.append(["", str(el)])
    if current is not None:
        out.append(current)
    parts = []
    for chunk in out:
        if chunk[0]:
            parts.append("".join(chunk) + "</section>")
        else:
            parts.append("".join(chunk[1:]))
    return "".join(parts), figs


def figure_context(img):
    """Nearest preceding heading, used as the figure caption."""
    node = img
    while node is not None:
        prev = node.find_previous(["h1", "h2", "h3"])
        if prev is None:
            return "AWS console"
        txt = prev.get_text(" ", strip=True)
        if txt.lower() in ("result", "procedure", "purpose", "explanation",
                           "configuration", "configuration:", "navigate to:"):
            node = prev
            continue
        return txt
    return "AWS console"


def css():
    faces = "".join(font_face("Space Grotesk", w, f) for w, f in FONTS.items())
    faces += font_face("Space Mono", 400, MONO)
    faces += font_face("Space Mono", 700, MONO_BOLD)
    return faces + """
*{box-sizing:border-box;margin:0;padding:0}
@page{size:A4;margin:26mm 16mm 18mm 16mm}
@page cover{size:A4;margin:0}
@page roadmap{size:A4;margin:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font:400 9.6pt/1.55 'Space Grotesk',Inter,sans-serif;color:#1b2033}

/* ---------- cover ---------- */
.cover{page:cover;width:210mm;height:297mm;position:relative;overflow:hidden;
  background:radial-gradient(120% 90% at 88% -10%,#2a3ae0 0%,#0000C8 38%,#11206D 74%,#0a1146 100%);
  color:#fff;padding:20mm 18mm 16mm 18mm;display:flex;flex-direction:column;
  break-after:page}
.cover .mesh{position:absolute;inset:0;opacity:.16;
  background-image:linear-gradient(#fff 1px,transparent 1px),linear-gradient(90deg,#fff 1px,transparent 1px);
  background-size:14mm 14mm;mask-image:radial-gradient(80% 60% at 20% 15%,#000 0%,transparent 70%)}
.cover .glow{position:absolute;width:130mm;height:130mm;right:-40mm;bottom:-50mm;border-radius:50%;
  background:radial-gradient(circle,rgba(200,0,25,.55) 0%,rgba(100,100,255,.18) 45%,transparent 70%)}
.cover>*{position:relative;z-index:2}
.cvtop{display:flex;align-items:flex-start;justify-content:space-between}
.cvtop img{height:11mm}
.pill{border:1px solid rgba(255,255,255,.5);border-radius:20px;padding:1.6mm 4.5mm;
  font:600 7.6pt/1 'Space Grotesk';letter-spacing:.16em;text-transform:uppercase}
.cvmid{margin-top:26mm}
.eyebrow{font:600 8.4pt/1 'Space Grotesk';letter-spacing:.28em;text-transform:uppercase;
  color:#9fb0ff;margin-bottom:6mm}
.cvmid h1{font:700 34pt/1.06 'Space Grotesk';letter-spacing:-.02em;max-width:150mm}
.cvmid h2{font:500 15pt/1.3 'Space Grotesk';color:#b9c6ff;margin-top:5mm}
.rule{width:38mm;height:1.6mm;margin:9mm 0 7mm;border-radius:2px;
  background:linear-gradient(90deg,#C80019,#6464FF 55%,#0046FF)}
.lede{font:400 11pt/1.62 'Space Grotesk';color:#dfe5ff;max-width:158mm}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:11mm}
.card{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.2);
  border-radius:3mm;padding:6mm 5.5mm}
.card .k{font:600 7.4pt/1 'Space Grotesk';letter-spacing:.18em;text-transform:uppercase;
  color:#8fa4ff;margin-bottom:3.5mm}
.card p{font:400 9pt/1.5 'Space Grotesk';color:#eef1ff}
.flow{margin-top:auto;padding-top:12mm}
.flow .k{font:600 7.4pt/1 'Space Grotesk';letter-spacing:.18em;text-transform:uppercase;
  color:#8fa4ff;margin-bottom:4.5mm}
.flowline{display:flex;align-items:center;gap:2.2mm;flex-wrap:nowrap}
.fchip{background:#eef1fb;border:1px solid #c4ccde;color:#11206D;
  border-radius:2mm;padding:2.2mm 3.2mm;font:500 8.2pt/1.1 'Space Grotesk';white-space:nowrap}
.fchip.last{background:#0046FF;border-color:#0046FF;color:#fff}
.flowline.dark .fchip{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.3);
  color:#fff}
.flowline.dark .fchip.last{background:#0046FF;border-color:#5f7dff}
.farrow{width:0;height:0;flex:none;border-top:1.5mm solid transparent;
  border-bottom:1.5mm solid transparent;border-left:2.2mm solid #0046FF}
.flowline.dark .farrow{border-left-color:#8fa4ff}
.flowbody{margin:0 0 5mm}

/* ---------- high-level architecture ---------- */
.archwrap{margin:0 0 6mm;break-inside:avoid}
.arch{display:flex;flex-direction:column;align-items:center}
.azone{width:100%;border-radius:2.5mm;padding:4mm 5mm 5mm;position:relative}
.azone.aws{background:#f6f8fd;border:1px solid #dde2f0}
.azone.ak{background:#eef2ff;border:1px solid #c3cff5}
.azlabel{font:600 7pt/1 'Space Grotesk';letter-spacing:.14em;text-transform:uppercase;
  color:#11206D;margin-bottom:3.5mm}
.azone.ak .azlabel{color:#0046FF}
.acol{display:flex;flex-direction:column;align-items:center}
.anode{width:112mm;border:1px solid #c4ccde;border-left:2mm solid #6464FF;background:#fff;
  border-radius:1.8mm;padding:2.6mm 4mm;text-align:left}
.azone.ak .anode{border-left-color:#0046FF;border-color:#b9c6f5}
.anode .al{font:600 9.4pt/1.2 'Space Grotesk';color:#11206D}
.anode .an{font:400 7.9pt/1.35 'Space Grotesk';color:#5b6483;margin-top:1mm}
.astem{width:0;height:0;margin:1.5mm 0;border-left:1.6mm solid transparent;
  border-right:1.6mm solid transparent;border-top:2.2mm solid #0046FF}
.astem.zonestem{margin:2.6mm 0;border-left-width:2.2mm;border-right-width:2.2mm;
  border-top-width:3mm}

/* ---------- out-of-the-box rules table ---------- */
.rules{break-inside:auto}
.rules thead{display:table-header-group}
.rules table{font-size:8.3pt}
.rules thead th:first-child{width:26%}
.rules thead th:nth-child(2){width:37%}
.rules td:first-child{font-weight:600;color:#11206D}
.rules tbody tr{break-inside:avoid}
.cvfoot{margin-top:10mm;padding-top:5mm;border-top:1px solid rgba(255,255,255,.22);
  display:flex;justify-content:space-between;font:400 8pt/1.4 'Space Grotesk';color:#aab8ff}

/* ---------- roadmap ---------- */
.roadmap{page:roadmap;width:210mm;height:297mm;padding:18mm 18mm 14mm;position:relative;
  overflow:hidden;break-after:page;background:#fff}
.rmhead{display:flex;justify-content:space-between;align-items:flex-end;
  border-bottom:2px solid #11206D;padding-bottom:5mm}
.rmhead h2{font:700 19pt/1.15 'Space Grotesk';color:#11206D}
.rmhead img{height:8.5mm}
.rmintro{font:400 9.6pt/1.55 'Space Grotesk';color:#3a4260;margin:5mm 0 5mm;max-width:168mm}
.prebox{border-left:3.5mm solid #0046FF;background:#f1f4ff;border-radius:0 2mm 2mm 0;
  padding:4mm 5mm;margin-bottom:5.5mm}
.prebox h3{font:600 9.6pt/1.3 'Space Grotesk';color:#11206D;margin-bottom:2mm}
.prebox p{font:400 8.9pt/1.5 'Space Grotesk';color:#3a4260}
.steplist{display:grid;grid-template-columns:1fr 1fr;gap:2.6mm 6mm}
.srow{display:flex;gap:3.4mm;align-items:flex-start;border-top:1px solid #e3e7f2;padding-top:2.8mm}
.snum{font:700 9pt/1 'Space Grotesk';color:#0046FF;min-width:7mm;padding-top:.6mm}
.srow .t{font:600 9pt/1.35 'Space Grotesk';color:#11206D}
.srow .d{font:400 8.1pt/1.4 'Space Grotesk';color:#5b6483;margin-top:1mm}
.ucwrap{margin-top:6mm}
.ucwrap>.k{font:600 7.8pt/1 'Space Grotesk';letter-spacing:.18em;text-transform:uppercase;
  color:#8b93b3;margin-bottom:4mm}
.ucs{display:grid;grid-template-columns:repeat(3,1fr);gap:4.5mm}
.uc{border:1px solid #dde2f0;border-top:2.5mm solid #C80019;border-radius:2mm;padding:4.5mm}
.uc.b{border-top-color:#6464FF}.uc.c{border-top-color:#0046FF}
.uc .t{font:600 9.2pt/1.3 'Space Grotesk';color:#11206D}
.uc .d{font:400 8.2pt/1.45 'Space Grotesk';color:#5b6483;margin-top:2mm}
.convey{margin-top:6.5mm;border-top:1px solid #e3e7f2;padding-top:4mm;
  font:400 8.2pt/1.5 'Space Grotesk';color:#5b6483}
.convey .navchip{font-size:7.6pt;padding:.9mm 1.8mm}
.convey b{color:#11206D;font-weight:600}

/* ---------- body ---------- */
.stepsec{break-before:page}
h1.step{font:700 17pt/1.2 'Space Grotesk';color:#11206D;padding-bottom:3.5mm;
  margin-bottom:5mm;border-bottom:2px solid #0046FF;break-after:avoid}
h2{font:600 12pt/1.3 'Space Grotesk';color:#003BF6;margin:7mm 0 2.8mm;break-after:avoid}
h2.result-h,h3.result-h{color:#0B7A42}
h3{font:600 10.2pt/1.35 'Space Grotesk';color:#11206D;margin:5.5mm 0 2.2mm;break-after:avoid}
p{margin:0 0 2.8mm}
strong{font-weight:600;color:#11206D}
ul,ol{margin:0 0 3.2mm 5mm}
li{margin-bottom:1.4mm}
li::marker{color:#0046FF}
code{font:400 8.6pt/1.4 'Space Mono',monospace;background:#eef0f6;border:1px solid #dfe3ef;
  border-radius:1mm;padding:.3mm 1.2mm;color:#11206D}
pre.code{font:400 8.1pt/1.5 'Space Mono',monospace;background:#0e1430;color:#dbe2ff;
  border-radius:2mm;padding:4mm 5mm;margin:0 0 4mm;white-space:pre-wrap;word-break:break-word;
  border-left:2mm solid #0046FF;break-inside:avoid}
.nav{display:flex;flex-wrap:wrap;align-items:center;gap:1.8mm;margin:0 0 4mm}
.navchip{background:#eef0f6;border:1px solid #c4ccde;border-radius:1.4mm;padding:1.4mm 2.6mm;
  font:500 8.4pt/1 'Space Grotesk';color:#11206D}
.navarrow{display:inline-block;width:0;height:0;vertical-align:middle;
  border-top:1.3mm solid transparent;border-bottom:1.3mm solid transparent;
  border-left:1.9mm solid #0046FF}
p.note{border-left:2.5mm solid #C80019;background:#fdf1f2;border-radius:0 1.6mm 1.6mm 0;
  padding:3.2mm 4mm;margin:0 0 3.6mm;font-size:9.1pt;color:#4a2126;break-inside:avoid}
.tbl{margin:0 0 4.5mm;break-inside:avoid}
table{width:100%;border-collapse:collapse;font-size:8.8pt}
thead th{background:#11206D;color:#fff;font-weight:600;text-align:left;
  padding:2.4mm 3mm;border:1px solid #11206D}
td,th{border:1px solid #d5dbeb;padding:2.2mm 3mm;vertical-align:top;text-align:left}
tbody tr:nth-child(even){background:#f6f8fd}
td strong{color:#11206D}
figure.shot{margin:0 auto 5mm;text-align:center;break-inside:avoid}
figure.shot img{display:block;margin:0 auto;border:1px solid #c4ccde;border-radius:1.6mm}
figcaption{font:400 7.8pt/1.4 'Space Grotesk';color:#7a83a1;margin-top:2mm;text-align:center}
section.optional{border:1px solid #c9d2ea;border-radius:2.5mm;overflow:hidden;margin:0 0 6mm;
  background:#fafbff}
.optional-bar{background:#eaeefc;border-bottom:1px solid #c9d2ea;padding:3.5mm 5mm;
  display:flex;align-items:center;gap:4mm;break-after:avoid}
.optional-tag{background:#0046FF;color:#fff;border-radius:1.4mm;padding:1.2mm 2.6mm;
  font:600 7pt/1 'Space Grotesk';letter-spacing:.1em;text-transform:uppercase;white-space:nowrap}
.optional-title{font:600 10.5pt/1.2 'Space Grotesk';color:#11206D}
.optional-body{padding:5mm}
.optional-body h1.step{font-size:13pt;border-bottom-width:1px}
.optional-body .stepsec{break-before:auto}
"""


def cover_html():
    flow = flow_strip(dark=True)
    return f"""
<div class="cover">
  <div class="mesh"></div><div class="glow"></div>
  <div class="cvtop">
    <img src="data:image/png;base64,{b64(LOGO_DARK)}">
    <span class="pill">Deployment Guide</span>
  </div>
  <div class="cvmid">
    <div class="eyebrow">Cloud Detection and Response</div>
    <h1>{DOC_TITLE}</h1>
    <h2>{DOC_SUB}</h2>
    <div class="rule"></div>
    <p class="lede">A step by step build of the AWS CDR integration by hand, without
      Terraform. You create the S3 bucket and CloudTrail trail, stand up a Lambda log
      forwarder, point CloudTrail at it, and confirm the events land in the AccuKnox
      SIEM. The last part wires alerts to GitHub Actions so common AWS
      misconfigurations get fixed automatically, using the {RULES_COUNT} detection rules
      that ship with the deployment.</p>
    <div class="cards">
      <div class="card"><div class="k">What you build</div>
        <p>A CloudTrail to Lambda to AccuKnox log pipeline in one AWS account, plus an
        automated remediation path through GitHub Actions.</p></div>
      <div class="card"><div class="k">Who it is for</div>
        <p>Cloud and security engineers with console access to the target AWS account
        and admin rights on a GitHub repository.</p></div>
      <div class="card"><div class="k">Before you start</div>
        <p>Get the ingestion URL and Basic Auth credentials from the AccuKnox team.
        Budget about 90 minutes for the full walkthrough.</p></div>
    </div>
  </div>
  <div class="flow">
    <div class="k">Deployment architecture</div>
    {flow}
  </div>
  <div class="cvfoot">
    <span>AccuKnox, Inc. &nbsp;|&nbsp; Confidential</span>
    <span>Version {DOC_VER} &nbsp;|&nbsp; {DOC_DATE}</span>
  </div>
</div>"""


def roadmap_html(n_figs):
    rows = "".join(
        f'<div class="srow"><div class="snum">{n}</div><div><div class="t">{t}</div>'
        f'<div class="d">{d}</div></div></div>' for n, t, d in STEPS)
    ucs = "".join(
        f'<div class="uc {c}"><div class="t">Use case {i}. {t}</div><div class="d">{d}</div></div>'
        for i, ((t, d), c) in enumerate(zip(USECASES, ["a", "b", "c"]), start=1))
    return f"""
<div class="roadmap">
  <div class="rmhead">
    <h2>What this guide covers</h2>
    <img src="data:image/png;base64,{b64(LOGO_LIGHT)}">
  </div>
  <p class="rmintro">Twelve steps, in order. Each one opens with why it exists, then the
    console path, then the exact values to enter. {n_figs} annotated console screenshots
    show what the screen should look like when the step is done. Step 12 lists the
    {RULES_COUNT} detection rules that ship with the deployment, and three worked use
    cases close the guide.</p>
  <div class="prebox">
    <h3>Skip ahead if your account is already logging</h3>
    <p>Already have an S3 bucket and a CloudTrail trail writing to it? Start at step 1,
      the Lambda execution role. The bucket and trail setup sits in an optional section
      just before it, marked <b>Only if not already configured</b>. Check first that the
      existing trail delivers to the existing bucket with an empty log prefix.</p>
  </div>
  <div class="steplist">{rows}</div>
  <div class="ucwrap">
    <div class="k">Automated remediation, proven end to end</div>
    <div class="ucs">{ucs}</div>
  </div>
  <div class="convey">
    <b>Conventions.</b> Console paths render as chips, for example
    <span class="navchip">AWS Console</span> <span class="navarrow"></span>
    <span class="navchip">Lambda</span>. Values you type appear in a table next to the
    setting name. Red bordered boxes are notes you should read before clicking.
    Screenshots came from the source export at reduced resolution, so fine console text
    may look soft in print.
  </div>
</div>"""


def stamp(raw, out, n_figs):
    doc = fitz.open(raw)
    sg = os.path.join(FONTDIR, FONTS[500])
    sgb = os.path.join(FONTDIR, FONTS[600])
    navy = fitz.utils.getColor("white")
    total = doc.page_count
    logo = open(LOGO_DARK, "rb").read()
    emblem = open(EMBLEM, "rb").read()
    for i, page in enumerate(doc):
        if i < 2:  # cover and roadmap carry their own furniture
            continue
        w, h = page.rect.width, page.rect.height
        # header bar
        bar = fitz.Rect(0, 0, w, 48)
        page.draw_rect(bar, color=None, fill=fitz.sRGB_to_pdf(0x11206D))
        accent = fitz.Rect(0, 48, w, 50.2)
        page.draw_rect(accent, color=None, fill=fitz.sRGB_to_pdf(0x0046FF))
        page.insert_font(fontname="SGM", fontfile=sg)
        page.insert_font(fontname="SGB", fontfile=sgb)
        page.insert_text((45, 23), DOC_TITLE, fontname="SGB", fontsize=9.5, color=navy)
        page.insert_text((45, 36), "%s  |  Version %s" % (DOC_SUB, DOC_VER),
                         fontname="SGM", fontsize=7.5,
                         color=fitz.sRGB_to_pdf(0x9FB0FF))
        lw, lh = 96, 14
        page.insert_image(fitz.Rect(w - 45 - lw, 18, w - 45, 18 + lh), stream=logo)
        # footer
        fy = h - 30
        page.draw_line(fitz.Point(45, fy), fitz.Point(w - 45, fy),
                       color=fitz.sRGB_to_pdf(0xD5DBEB), width=.7)
        page.insert_image(fitz.Rect(45, fy + 7, 45 + 10, fy + 17), stream=emblem)
        page.insert_text((60, fy + 15), "AccuKnox, Inc.   |   Confidential",
                         fontname="SGM", fontsize=7.4,
                         color=fitz.sRGB_to_pdf(0x7A83A1))
        label = "Page %d of %d" % (i + 1, total)
        tw = fitz.get_text_length(label, fontname="helv", fontsize=7.4)
        page.insert_text((w - 45 - tw - 4, fy + 15), label, fontname="SGB",
                         fontsize=7.4, color=fitz.sRGB_to_pdf(0x11206D))
    doc.set_metadata({
        "title": "%s, %s" % (DOC_TITLE, DOC_SUB),
        "author": "AccuKnox, Inc.",
        "subject": "Manual deployment of the AccuKnox AWS CDR integration",
        "keywords": "AccuKnox, AWS, CloudTrail, CDR, SIEM, Lambda, remediation",
        "creator": "AccuKnox document toolchain",
    })
    if os.path.exists(out):
        os.remove(out)
    doc.save(out, garbage=4, deflate=True)
    doc.close()
    return total


def main():
    os.makedirs(WORK, exist_ok=True)
    html_text, blobs = load_mhtml(SRC_DOC)
    body, n_figs = build_body(html_text, blobs)
    doc = ("<meta charset='utf-8'><title>%s</title><style>%s</style>%s%s%s"
           % (DOC_TITLE, css(), cover_html(), roadmap_html(n_figs), body))
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print("html %.1f MB, %d figures" % (os.path.getsize(HTML_OUT) / 1e6, n_figs))

    if os.path.exists(PDF_RAW):
        os.remove(PDF_RAW)
    subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        "--print-to-pdf=" + PDF_RAW, HTML_OUT.replace("\\", "/"),
    ], check=True, timeout=600)
    pages = stamp(PDF_RAW, PDF_OUT, n_figs)
    print("wrote %s  (%d pages, %.2f MB)"
          % (PDF_OUT, pages, os.path.getsize(PDF_OUT) / 1e6))


if __name__ == "__main__":
    sys.exit(main())
