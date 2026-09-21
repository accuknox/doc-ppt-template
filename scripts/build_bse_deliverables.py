# -*- coding: utf-8 -*-
"""
Build the BSE security deliverables pack on AccuKnox letterhead.

Sources live in 15-SEP-DOCs/. Output lands in output/BSE DELIVERABLES/.

  01  ISO/IEC 27001:2022 compliance summary, with the InfoGuard audit report appended
      unchanged. A SOC 2 report PDF dropped into 15-SEP-DOCs/ is detected and appended.
  02  Control Plane Architecture v3.4, copied byte for byte. No branding, no edits.
  03  SBOM report, built from the 162 CycloneDX files in sbom-final.zip, plus the zip.
  04  No Malware Certificate, from the malware line of Security Assessment v3.6.
  05  WAPT report, from the two DAST exports for app.accuknox.com and app.ind.accuknox.com.
  06  Source Code Review report, from the SAST assessment.

Run:  py -3.11 scripts/build_bse_deliverables.py
"""
import collections
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

import docx
import fitz
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.table import Table
from docx.text.paragraph import Paragraph

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _akdoc import (AKDoc, to_pdf, PRIMARY, NAVY, RED, GREEN_DK, PURPLE, MUTE, INK,  # noqa
                    HEX_GREEN_LT, HEX_GREY_BG, HEX_LAV, HEX_PRIMARY, SECOND)

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "15-SEP-DOCs"
OUT = ROOT / "output" / "BSE DELIVERABLES"
EDIT = OUT / "_editable_docx"

CLIENT = "BSE Limited"
ISSUED = "15 September 2026"
L, C, R = WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT


def control_block(d, ref, extra=()):
    d.kv_table([
        ("Document reference", ref),
        ("Prepared for", CLIENT),
        ("Prepared by", "AccuKnox, Inc."),
        ("Date of issue", ISSUED),
        *extra,
        ("Classification", "Confidential"),
    ])


def closing(d):
    d.h1("Contact")
    d.p("Send questions about this document to the AccuKnox security team at "
        "support@accuknox.com.")


def fmt(n):
    return f"{n:,}"


def build(d, name):
    docx_path = d.save(EDIT / f"{name}.docx")
    pdf_path = OUT / f"{name}.pdf"
    to_pdf(docx_path, pdf_path)
    print("wrote", pdf_path)
    return pdf_path


# =========================================================================== 01 ISO
def build_iso():
    iso_src = SRC / "AccuKnox Inc. - ISO 27001-2022 Internal Audit Report (2).pdf"
    soc2 = sorted(p for p in SRC.glob("*.pdf") if re.search(r"soc\s*-?\s*2", p.name, re.I))
    soc2 = soc2[0] if soc2 else None
    title = ("ISO/IEC 27001:2022 and SOC 2 Type II Compliance Summary" if soc2
             else "ISO/IEC 27001:2022 Compliance Summary")

    d = AKDoc("ISO/IEC 27001:2022 Compliance" + (" and SOC 2" if soc2 else ""))
    d.eyebrow("Compliance attestation")
    d.title(title, "Independent audit results for the AccuKnox Information Security "
                   "Management System")
    control_block(d, "AK-BSE-2026-01",
                  [("Attached evidence", "InfoGuard ISO/IEC 27001:2022 audit report, 25 pages"
                    + (", and the SOC 2 Type II report" if soc2 else ""))])

    d.h1("ISO/IEC 27001:2022 Audit Result")
    d.p("InfoGuard Cyber Security, Inc. audited the AccuKnox Information Security Management "
        "System (ISMS) against ISO/IEC 27001:2022. The auditors found that the ISMS conforms "
        "to the requirements of the standard.")
    d.stats([
        ("4 to 10", "ISMS clauses audited", PRIMARY),
        ("Annex A", "Controls audited", PRIMARY),
        ("1", "Non-conformity raised", PURPLE),
        ("4 months", "Audit period", PRIMARY),
    ])
    d.kv_table([
        ("Standard", "ISO/IEC 27001:2022, with the ISO/IEC 27002:2022 Annex A controls in the "
                     "Statement of Applicability v1.1"),
        ("Audit type", "Internal audit, process based, performed remotely"),
        ("Audit firm", "InfoGuard Cyber Security, Inc., San Jose, California"),
        ("Lead auditor", "Abe Rahim, ISO Certified Lead Auditor"),
        ("Audit period", "1 June 2024 to 30 September 2024"),
        ("Report review", "9 October 2024, confirmed by Robert Roohparvar, CISO, InfoGuard"),
        ("Scope", "The ISMS that supports the AccuKnox SaaS platform, its AWS hosted "
                  "technology, infrastructure and networks, and the Engineering, Security "
                  "and Human Resources departments"),
        ("Method", "Remote interviews, observation of activities, review of documents and "
                   "records, technical tests, and sampling through the AWS compliance "
                   "automation platform"),
    ])

    d.h1("Auditor Conclusions")
    d.p("The auditors answered each conclusion question in section 9.1 of the report as "
        "shown below.")
    d.table(["Audit conclusion question", "Answer"], [
        ["The management system is designed to achieve the policy objectives of the "
         "organization", "Yes"],
        ["The management system meets statutory, regulatory and contractual requirements",
         "Yes"],
        ["The internal audit and management review processes are in place and adequate", "Yes"],
        ["The audit met its stated objectives", "Yes"],
        ["Serious deviation from the audit plan", "No"],
        ["Significant issues that affect the audit program", "No"],
    ], widths=[5.3, 1.2], align=[L, C])

    d.h2("Open Item From the Audit")
    d.table(["Ref", "Control", "Requirement", "Auditor finding", "Planned completion"], [
        ["1", "8.15 Logging", "Produce, store, protect and analyze logs of activities, "
         "exceptions, faults and other relevant events",
         "Collect logs for six more months to show the maturity of the control",
         "30 December 2024"],
    ], widths=[0.4, 0.9, 2.1, 2.0, 1.1], align=[C, L, L, L, C], zebra=False)
    d.p("The auditor recommended six more months of technical control evidence before the "
        "external certification audit. Section 9.2 of the attached report gives the full "
        "recommendation.", size=9.5, color=MUTE)

    if soc2:
        d.h1("SOC 2 Type II Report")
        d.p("The SOC 2 Type II report follows the ISO/IEC 27001:2022 audit report in this "
            "document, unchanged.")

    d.h1("Attached Evidence")
    d.p("The complete InfoGuard audit report follows this summary. AccuKnox attaches it "
        "unchanged, so every page shows the audit firm's own wording and sign-off.")
    closing(d)

    name = "01_AccuKnox_ISO27001_Compliance_Summary"
    pdf = build(d, name)
    merged = fitz.open(pdf)
    for extra in [iso_src] + ([soc2] if soc2 else []):
        merged.insert_pdf(fitz.open(extra))
    tmp = OUT / f"{name}.tmp.pdf"
    merged.save(tmp, garbage=3, deflate=True)
    merged.close()
    tmp.replace(pdf)
    return soc2


# =========================================================================== 02 ARCH
def copy_architecture():
    src = SRC / "AccuKnox Control Plane Architecture Technical v3.4.pdf"
    dst = OUT / "02_AccuKnox Control Plane Architecture Technical v3.4.pdf"
    shutil.copyfile(src, dst)
    assert src.read_bytes() == dst.read_bytes()
    print("copied", dst)


# =========================================================================== 03 SBOM
ECO = {
    "golang": ("Go modules", "Application library"),
    "deb": ("Debian and Ubuntu packages", "OS package"),
    "npm": ("npm packages", "Application library"),
    "pypi": ("Python packages", "Application library"),
    "rpm": ("RPM packages", "OS package"),
    "apk": ("Alpine packages", "OS package"),
    "maven": ("Java (Maven) packages", "Application library"),
}
OS_NAMES = {"debian": "Debian", "ubuntu": "Ubuntu", "redhat": "Red Hat", "alpine": "Alpine",
            "oracle": "Oracle Linux", "wolfi": "Wolfi", "photon": "Photon OS"}
ORDER = ["network", "strong", "weak", "docs", "perm", "pd", "other"]
FAMILY = {
    "perm": "Permissive (MIT, BSD, Apache 2.0, ISC and similar)",
    "weak": "Weak copyleft (LGPL, MPL, EPL)",
    "strong": "Strong copyleft (GPL)",
    "network": "Network copyleft (AGPL, SSPL)",
    "pd": "Public domain",
    "docs": "Documentation licenses (GFDL, CC-BY)",
    "other": "Other or custom license text",
    "none": "No license declared in the package metadata",
}
PERM_KEYS = ["MIT", "BSD", "APACHE", "ISC", "ZLIB", "X11", "UNICODE", "PSF", "PYTHON", "FSF",
             "BSLA", "BEERWARE", "HPND", "ARTISTIC", "PERMISSIVE", "OPENSSL", "SSLEAY", "CURL",
             "LATEX", "W3C", "TCP-WRAPPERS", "BLUEOAK", "IJG", "LIBPNG", "NTP", "OFL", "RUBY",
             "POSTGRESQL", "VIM", "WTFPL", "JSON", "BZIP", "INFO-ZIP", "SPENCER", "TCL",
             "BOOST", "ICU", "BSL-1.0"]


def lic_family(lic):
    u = lic.upper()
    if "AGPL" in u or "SSPL" in u:
        return "network"
    if re.search(r"(^|[^L])GPL", u):
        return "strong"
    if "LGPL" in u or "MPL" in u or "EPL" in u or "CDDL" in u:
        return "weak"
    if "GFDL" in u or "CC-BY" in u:
        return "docs"
    if "PUBLIC" in u or "CC0" in u or "UNLICENSE" in u or u in ("PD", "PD-DEBIAN"):
        return "pd"
    if any(k in u for k in PERM_KEYS):
        return "perm"
    return "other"


def image_row(raw):
    base = raw.split("/")[-1]
    base = re.sub(r"\.tar$", "", base)
    name, _, tag = base.rpartition(":")
    if name.startswith("956994857092.dkr.ecr.us-east-2.amazonaws.com_"):
        return "AccuKnox private", name.split("_", 1)[1], tag
    if name.startswith("public.ecr.aws_k9v9d5v2_"):
        return "AccuKnox public ECR", name.split("_", 2)[2], tag
    first = name.split("_", 1)
    if "." in first[0] and len(first) == 2:
        return first[0], first[1].replace("_", "/"), tag
    return "docker.io", name.replace("_", "/"), tag


def build_sbom():
    zpath = SRC / "sbom-final.zip"
    z = zipfile.ZipFile(zpath)
    images, eco, osfam = [], collections.Counter(), collections.Counter()
    fam_os, fam_app = collections.Counter(), collections.Counter()
    uniq, net_pkgs, tools, specs, stamp = set(), set(), set(), set(), set()
    total = go_nolic = 0
    for n in sorted(z.namelist()):
        if not n.endswith(".json"):
            continue
        bom = json.loads(z.read(n))
        specs.add(f'{bom["bomFormat"]} {bom["specVersion"]}')
        t = bom["metadata"]["tools"]["components"][0]
        tools.add(f'{t["name"].capitalize()} {t["version"]}')
        stamp.add(bom["metadata"]["timestamp"][:10])
        osname, libs = "", 0
        for c in bom.get("components", []):
            if c.get("type") == "operating-system":
                osn = OS_NAMES.get(c.get("name", ""), c.get("name", "").capitalize())
                osname = f'{osn} {c.get("version", "")}'.strip()
                continue
            if c.get("type") != "library":
                continue
            libs += 1
            purl = c.get("purl", "")
            m = re.match(r"pkg:([^/]+)/", purl)
            e = m.group(1) if m else "other"
            eco[e if e in ECO else "other"] += 1
            uniq.add(purl.split("?")[0] if purl else c.get("name", "") + c.get("version", ""))
            is_os = e in ("deb", "rpm", "apk")
            ls = [x.get("license", {}).get("id") or x.get("license", {}).get("name")
                  or x.get("expression") for x in c.get("licenses", [])]
            ls = [x for x in ls if x]
            fam = min((lic_family(x) for x in ls), key=ORDER.index) if ls else "none"
            if fam == "none" and e == "golang":
                go_nolic += 1
            if fam == "network":
                net_pkgs.add(c.get("name"))
            (fam_os if is_os else fam_app)[fam] += 1
        total += libs
        osfam[osname.rsplit(" ", 1)[0] if osname else "None detected"] += 1
        reg, img, tag = image_row(bom["metadata"]["component"]["name"])
        images.append((img, tag, reg, osname or "None detected", libs))

    assert len(images) == 162, len(images)
    images.sort(key=lambda r: (r[2] not in ("AccuKnox private", "AccuKnox public ECR"),
                               r[2], r[0], r[1]))
    n_ak = sum(1 for r in images if r[2].startswith("AccuKnox"))
    gen_date = sorted(stamp)
    tool = ", ".join(sorted(tools))
    spec = ", ".join(sorted(specs))

    d = AKDoc("Software Bill of Materials")
    d.eyebrow("Software supply chain")
    d.title("Software Bill of Materials (SBOM) Report",
            "Component inventory of the AccuKnox platform container images")
    control_block(d, "AK-BSE-2026-03", [
        ("SBOM format", spec + " (JSON)"),
        ("Machine-readable files", "03_AccuKnox_SBOM_CycloneDX.zip, one SBOM for each image"),
    ])

    d.h1("SBOM Key Figures")
    d.stats([
        (fmt(len(images)), "Container images", PRIMARY),
        (fmt(total), "Library components", PRIMARY),
        (fmt(len(uniq)), "Unique packages", PRIMARY),
        (str(len([k for k in eco if eco[k]])), "Package ecosystems", PRIMARY),
    ])
    d.p(f"AccuKnox generated one SBOM for each of the {len(images)} container images of the "
        f"platform on 15 June 2026. {tool} produced every file in {spec} format.")
    d.p(f"AccuKnox builds {n_ak} of the images. The other {len(images) - n_ak} are upstream "
        "images that the platform deploys, for example KubeArmor, Kyverno, cert-manager, "
        "Istio, RabbitMQ and Percona databases.")
    d.callout("License and dependency review", [
        "AccuKnox reviewed the licenses and the external dependencies in these SBOMs. "
        "The review raised no action items."])

    d.h1("Scope and Method")
    d.bullets([
        ("Scope.", f"All {len(images)} container images of the platform, including the AccuKnox "
                   "services, the scanner jobs and the upstream images that the platform "
                   "deploys."),
        ("Tool.", f"{tool}, run against the exported image archive of each image."),
        ("Format.", f"{spec}, one JSON document for each image, with a unique serial number."),
        ("Content.", "Each component record holds the package name, version, package URL "
                     "(purl), declared licenses and the image layer that holds it."),
        ("Counting.", "A library component is one package in one image. A unique package is "
                      "one distinct package URL across all images."),
    ])

    d.h1("Components by Ecosystem")
    rows = []
    for key, cnt in eco.most_common():
        label, kind = ECO.get(key, ("Other package types", "Application library"))
        rows.append([label, kind, fmt(cnt), f"{cnt / total:.1%}"])
    rows.append(["Total", "", fmt(total), "100.0%"])
    d.table(["Ecosystem", "Component type", "Components", "Share"], rows,
            widths=[2.6, 1.9, 1.1, 0.9], align=[L, L, R, R], total_row=True)

    d.h1("Base Operating Systems")
    d.p("Trivy detects the base operating system of each image from its OS package database.")
    os_versions = collections.defaultdict(collections.Counter)
    for img in images:
        fam = img[3].rsplit(" ", 1)[0] if img[3] != "None detected" else "None detected"
        os_versions[fam][img[3].rsplit(" ", 1)[-1]] += 1
    rows = []
    for fam, cnt in osfam.most_common():
        label = fam
        vers = os_versions[label]
        vtxt = ", ".join(v for v, _ in sorted(vers.items())) if label != "None detected" \
            else "Distroless or scratch based images"
        rows.append([label, vtxt, fmt(cnt)])
    d.table(["Operating system", "Versions found", "Images"], rows,
            widths=[1.4, 4.1, 1.0], align=[L, L, R])

    d.h1("Declared Licenses")
    d.p("Each component counts once, under its most restrictive declared license. OS packages "
        "come from the base image distributions. Application libraries come from the service "
        "code and its dependencies.")
    rows = []
    for key in ["perm", "weak", "strong", "network", "pd", "docs", "other", "none"]:
        a, b = fam_os[key], fam_app[key]
        rows.append([FAMILY[key], fmt(a), fmt(b), fmt(a + b)])
    rows.append(["Total", fmt(sum(fam_os.values())), fmt(sum(fam_app.values())), fmt(total)])
    d.table(["License family", "OS packages", "Application libraries", "Total"], rows,
            widths=[3.2, 1.0, 1.3, 1.0], align=[L, R, R, R], total_row=True)
    strong_os = fam_os["strong"] / max(1, fam_os["strong"] + fam_app["strong"])
    d.p(f"More than {int(strong_os * 100)}% of the GPL components are OS packages of the Linux "
        f"distributions. Go modules account for {fmt(go_nolic)} of the "
        f"{fmt(fam_app['none'])} application libraries with no declared license.")
    d.p(f"{fam_os['network'] + fam_app['network']} components declare AGPL or SSPL terms. All "
        "of them are OS packages, for example Ghostscript and libwmf in Debian base images, "
        "and Percona Server for MongoDB.")

    d.page_break()
    d.h1("Appendix A. Image Inventory", before=0)
    d.p(f"The {len(images)} images below each have a matching SBOM file in the attached "
        "ZIP archive. \"AccuKnox private\" is the AccuKnox private container registry.")
    rows = [[str(i), r[0], r[1], r[2], r[3], fmt(r[4])] for i, r in enumerate(images, 1)]
    d.table(["#", "Image", "Tag", "Registry", "Base OS", "Libraries"], rows,
            widths=[0.42, 1.93, 1.25, 1.15, 1.0, 0.75], size=7.5, head_size=7.5,
            align=[C, L, L, L, L, R])
    closing(d)

    build(d, "03_AccuKnox_SBOM_Report")
    shutil.copyfile(zpath, OUT / "03_AccuKnox_SBOM_CycloneDX.zip")
    return dict(images=len(images), total=total, uniq=len(uniq))


# =========================================================================== 04 MALWARE
def build_malware():
    d = AKDoc("No Malware Certificate")
    d.spacer(4)
    frame = d._new_table(1, 1, [6.5])
    from _akdoc import table_borders, shade
    table_borders(frame, color=HEX_PRIMARY, sz=18, val="double", inside=False)
    cell = frame.rows[0].cells[0]
    cell.text = ""
    first = cell.paragraphs[0]
    first.paragraph_format.space_before = Pt(18)
    first.alignment = C
    from _akdoc import add_text
    add_text(first, "CERTIFICATE", size=10, bold=True, color=PRIMARY)
    d.p("No Malware Certificate", size=28, bold=True, color=NAVY, align=C, after=2,
        container=cell)
    d.p("Reference AK-BSE-2026-04", size=9.5, color=MUTE, align=C, after=16, container=cell)
    d.p("AccuKnox, Inc. certifies that the container images of the AccuKnox On-Prem "
        "Deployment Charts, version 3.6, passed a malware scan.", size=12, color=INK,
        align=C, after=8, container=cell)
    d.p("The scan found no malware.", size=15, bold=True, color=GREEN_DK, align=C,
        after=16, container=cell)
    inner = d.kv_table([
        ("Product", "AccuKnox On-Prem Deployment Charts"),
        ("Version", "v3.6"),
        ("Scope", "All container images that the v3.6 deployment charts install"),
        ("Scan type", "Malware scan of the container images"),
        ("Result", "0 malware findings"),
        ("Source record", "AccuKnox Security Assessment, On-Prem Deployment Charts v3.6"),
        ("Issued to", CLIENT),
        ("Date of issue", ISSUED),
    ], widths=(1.6, 4.4), container=cell)
    inner.alignment = C
    d.p("This certificate applies to the v3.6 container images only.", size=9, color=MUTE, align=C, before=4, after=6, container=cell)
    sig = d.signature(container=cell)
    sig.alignment = C
    d.p("", after=14, container=cell)
    build(d, "04_AccuKnox_No_Malware_Certificate")


# =========================================================================== 05 WAPT
FINDINGS = [
    # key (scanner name), id, display name, severity, owasp, cwe, description, recommendation
    ("Vulnerable JS Library", "Vulnerable JavaScript Library (DOMPurify 2.4.7)", "High",
     "A06:2021 Vulnerable and Outdated Components", "CWE-1395",
     ["The front-end JavaScript bundle includes DOMPurify version 2.4.7.",
      "This version has known vulnerabilities: CVE-2024-45801, CVE-2024-47875 and "
      "CVE-2025-26791."],
     "Upgrade DOMPurify to the latest 3.x release. Then rebuild and redeploy the front-end "
     "bundle."),
    ("Content Security Policy (CSP) Header Not Set", "Content Security Policy Header Not Set",
     "Medium", "A05:2021 Security Misconfiguration", "CWE-693",
     ["The response does not set a Content-Security-Policy header.",
      "This header tells the browser which sources it can load scripts and other content "
      "from. It reduces the risk of cross-site scripting and data injection."],
     "Configure the CDN or web server to send a Content-Security-Policy header on every "
     "response."),
    ("Missing Anti-clickjacking Header", "Missing Anti-Clickjacking Header", "Medium",
     "A05:2021 Security Misconfiguration", "CWE-1021",
     ["The response sets neither X-Frame-Options nor a CSP frame-ancestors directive.",
      "Another site can then show the page inside a frame for a clickjacking attack."],
     "Send Content-Security-Policy with frame-ancestors 'self', or X-Frame-Options set to "
     "DENY or SAMEORIGIN, on every page."),
    ("Sub Resource Integrity Attribute Missing", "Subresource Integrity Attribute Missing",
     "Medium", "A05:2021 Security Misconfiguration", "CWE-345",
     ["The page loads a stylesheet from fonts.googleapis.com without an integrity attribute.",
      "The browser cannot check that the external file is the expected file."],
     "Add an integrity attribute with the expected hash to each external script and "
     "stylesheet, or serve the files from the application origin."),
    ("Strict-Transport-Security Header Not Set", "Strict-Transport-Security Header Not Set",
     "Low", "A05:2021 Security Misconfiguration", "CWE-319",
     ["The response does not set the Strict-Transport-Security (HSTS) header.",
      "HSTS tells the browser to connect to the site over HTTPS only."],
     "Send Strict-Transport-Security with a max-age of at least one year on all HTTPS "
     "responses."),
    ("X-Content-Type-Options Header Missing", "X-Content-Type-Options Header Missing", "Low",
     "A05:2021 Security Misconfiguration", "CWE-693",
     ["The response does not set X-Content-Type-Options to nosniff.",
      "Older browsers can then guess the content type and handle a file as a different "
      "type."],
     "Set X-Content-Type-Options to nosniff, and set a correct Content-Type, on every "
     "response."),
    ('Server Leaks Version Information via "Server" HTTP Response Header Field',
     "Server Header Discloses the Hosting Service", "Low",
     "A05:2021 Security Misconfiguration", "CWE-497",
     ["The Server response header returns the value AmazonS3.",
      "The value tells an attacker which service hosts the static content."],
     "Remove the Server header, or replace it with a generic value, at the CDN edge."),
    ("Private IP Disclosure", "Private IP Address Disclosure", "Low",
     "A01:2021 Broken Access Control", "CWE-497",
     ["The JavaScript bundle contains the private address range 10.0.0.0."],
     "Remove private IP addresses from all content that the browser receives."),
    ("Information Disclosure - Suspicious Comments", "Suspicious Comments in Responses",
     "Informational", "A01:2021 Broken Access Control", "CWE-615",
     ["The response contains code comments that can give an attacker information about "
      "the application."],
     "Remove developer comments from the production HTML and JavaScript."),
    ("Re-examine Cache-control Directives", "Cache-Control Directives to Review",
     "Informational", "A07:2021 Identification and Authentication Failures", "CWE-525",
     ["The Cache-Control header is missing or permits caching of the response."],
     "Use no-cache, no-store, must-revalidate for sensitive content. Use public, max-age "
     "and immutable for static assets."),
    ("Retrieved from Cache", "Content Retrieved From a Shared Cache", "Informational",
     "A07:2021 Identification and Authentication Failures", "CWE-525",
     ["The response came from a shared cache, because the Age header is present.",
      "The finding matters only when the response holds user-specific data."],
     "Confirm that cached responses hold no sensitive or user-specific data."),
    ("Modern Web Application", "Single-Page Web Application Detected", "Informational",
     "A05:2021 Security Misconfiguration", "None",
     ["The scanner detected a single-page web application. The finding is informational."],
     "No action needed."),
]
SEV_ORDER = ["Critical", "High", "Medium", "Low", "Informational"]


def read_dast(path):
    labels = {"Key Information", "Description", "Evidence", "Solution", "References",
              "HTTP Request", "HTTP Response", "Additional Information", "Other Information"}
    doc = docx.Document(path)
    out = []
    for t in doc.tables:
        c = t.rows[0].cells[0]
        if not c.text.startswith("FINDING #"):
            continue
        blocks, cur, kv = collections.defaultdict(list), "head", {}
        for el in c._tc.iterchildren():
            tag = el.tag.split("}")[1]
            if tag == "p":
                txt = Paragraph(el, c).text.strip()
                if not txt:
                    continue
                if txt in labels:
                    cur = txt
                    continue
                blocks[cur].append(txt)
            elif tag == "tbl":
                for r in Table(el, c).rows:
                    cells = [x.text.strip() for x in r.cells]
                    if len(cells) == 2 and cells[0] != cells[1]:
                        kv[cells[0]] = cells[1]
        h = blocks["head"]
        loc = kv.get("Location", "").split(",")
        out.append(dict(name=h[1], sev=h[2].split()[0].capitalize(),
                        url=loc[1].strip() if len(loc) > 1 else "",
                        param=loc[2].strip() if len(loc) > 2 else "",
                        evidence=" ".join(blocks["Evidence"]),
                        date=kv.get("Date Discovered", "")[:10]))
    return out


def build_wapt():
    targets = [
        ("app.accuknox.com", read_dast(SRC / "accuknox app.docx")),
        ("app.ind.accuknox.com", read_dast(SRC / "Finding_2026-06-14_17-30-17_672624[1].docx")),
    ]
    for host, fs in targets:
        known = {f[0] for f in FINDINGS}
        missing = {f["name"] for f in fs} - known
        assert not missing, missing
    counts = {h: collections.Counter(f["sev"] for f in fs) for h, fs in targets}
    total = collections.Counter()
    for h in counts:
        total.update(counts[h])
    n_all = sum(total.values())
    dates = {h: sorted({f["date"] for f in fs}) for h, fs in targets}

    def nice_date(iso):
        y, m, dd = iso.split("-")
        months = ["January", "February", "March", "April", "May", "June", "July", "August",
                  "September", "October", "November", "December"]
        return f"{int(dd)} {months[int(m) - 1]} {y}"

    d = AKDoc("WAPT Report")
    d.eyebrow("Security testing report")
    d.title("Web Application Penetration Testing (WAPT) Report",
            "AccuKnox SaaS web applications: app.accuknox.com and app.ind.accuknox.com")
    control_block(d, "AK-BSE-2026-05", [
        ("Targets", "https://app.accuknox.com\nhttps://app.ind.accuknox.com"),
        ("Test dates", "; ".join(f"{h}: {nice_date(dates[h][0])}" for h, _ in targets)
         .replace("; ", "\n")),
    ])

    d.h1("Executive Summary")
    d.stats([
        (str(total["Critical"]), "Critical", GREEN_DK),
        (str(total["High"]), "High", PURPLE),
        (str(total["Medium"]), "Medium", MUTE),
        (str(total["Low"]), "Low", GREEN_DK),
        (str(total["Informational"]), "Informational", MUTE),
    ])
    d.p(f"AccuKnox tested two AccuKnox web applications with dynamic application security "
        f"testing (DAST). The test produced {n_all} findings of {len(FINDINGS)} distinct "
        f"types. It found no Critical findings.")
    d.p("Each target has one High finding, and both come from the same outdated JavaScript "
        "library. Most Medium and Low findings are missing HTTP security response headers.")
    d.callout("Remediation status", [
        "AccuKnox mitigated all Medium findings after the test. Two Low findings remain, and "
        "they pose no threat to the platform."], fill=HEX_GREEN_LT, accent="16A55C",
        color=GREEN_DK)

    d.h1("Scope and Method")
    d.table(["Target", "Test date", "Assets", "Findings"],
            [[f"https://{h}", nice_date(dates[h][0]), "1", str(len(fs))] for h, fs in targets],
            widths=[2.8, 1.6, 0.9, 1.2], align=[L, L, C, C])
    d.bullets([
        ("Approach.", "Dynamic testing of the running applications from the outside, "
                      "the way an external attacker sees them."),
        ("Coverage.", "The application pages, JavaScript bundles and static files such as "
                      "manifest.json, robots.txt and sitemap.xml."),
        ("Classification.", "Each finding maps to the OWASP Top 10 2021 and to a CWE "
                            "identifier."),
        ("Severity.", "High, Medium, Low and Informational, as the scanner assigned them."),
    ])

    d.h1("Results by Target")
    rows = []
    for sev in SEV_ORDER:
        rows.append([sev] + [str(counts[h][sev]) for h, _ in targets] + [str(total[sev])])
    rows.append(["Total"] + [str(len(fs)) for _, fs in targets] + [str(n_all)])
    d.table(["Severity", "app.accuknox.com", "app.ind.accuknox.com", "Total"], rows,
            widths=[1.9, 1.7, 1.9, 1.0], align=[L, C, C, C], total_row=True, bold_first=True)

    d.h1("Findings Register")
    rows = []
    for i, (key, disp, sev, owasp, cwe, _, _) in enumerate(FINDINGS, 1):
        per = [str(sum(1 for f in fs if f["name"] == key)) for _, fs in targets]
        rows.append([f"W-{i:02d}", disp, sev, owasp.split(" ", 1)[0], cwe] + per)
    d.table(["ID", "Finding", "Severity", "OWASP", "CWE", "app", "app.ind"], rows,
            widths=[0.5, 2.3, 1.0, 0.75, 0.8, 0.45, 0.7], size=8.5, head_size=8,
            align=[C, L, C, C, C, C, C], sev_col=2)
    d.p("The app and app.ind columns count the instances on app.accuknox.com and "
        "app.ind.accuknox.com.", size=8.5, color=MUTE)

    d.h1("Finding Details")
    for i, (key, disp, sev, owasp, cwe, desc, fix) in enumerate(FINDINGS, 1):
        d.h2(f"W-{i:02d}  {disp}", before=14)
        d.table(["Severity", "OWASP Top 10 2021", "CWE"], [[sev, owasp, cwe]],
                widths=[1.2, 3.8, 1.5], align=[C, L, C], sev_col=0, zebra=False)
        d.rich([("Description. ", dict(bold=True, color=NAVY)), (" ".join(desc), {})])
        ev = next((f["evidence"] for _, fs in targets for f in fs
                   if f["name"] == key and f["evidence"]), "")
        if ev and key not in ("Information Disclosure - Suspicious Comments",
                              "Sub Resource Integrity Attribute Missing"):
            ev = ev.split("\n")[0].strip()[:110]
            d.rich([("Evidence. ", dict(bold=True, color=NAVY)), (ev, dict(font="Consolas",
                                                                             size=8.5))])
        locs = []
        for host, fs in targets:
            seen = []
            for f in fs:
                if f["name"] == key:
                    u = f["url"].replace(f"https://{host}", "") or "/"
                    if u not in seen:
                        seen.append(u)
            locs.append([host, ", ".join(seen)])
        d.table(["Target", "Affected paths"], locs, widths=[1.8, 4.7], size=8.5,
                head_size=8, align=[L, L], zebra=False, bold_first=True)
        d.rich([("Recommendation. ", dict(bold=True, color=NAVY)), (fix, {})], after=4)
    closing(d)
    build(d, "05_AccuKnox_WAPT_Report")
    return total, n_all


# =========================================================================== 06 SAST
def build_sast():
    d = AKDoc("Source Code Review Report")
    d.eyebrow("Security assessment report")
    d.title("Source Code Review Report",
            "Static Application Security Testing (SAST) of the AccuKnox source repositories")
    control_block(d, "AK-BSE-2026-06", [
        ("Assessment type", "Static Application Security Testing (SAST), source code analysis"),
        ("Scope", "36 AccuKnox deployment repositories"),
    ])

    d.h1("Executive Summary")
    d.stats([
        ("36", "Repositories scanned", PRIMARY),
        ("2,174", "Total findings", PRIMARY),
        ("139", "High", PURPLE),
        ("1,121", "Medium", MUTE),
        ("914", "Low", GREEN_DK),
    ])
    d.p("AccuKnox ran a static application security test across 36 AccuKnox deployment "
        "repositories. The scan produced 2,174 findings: 139 High, 1,121 Medium and 914 Low.")
    d.p("The existing AccuKnox compensatory controls cover 1,164 of the 1,260 High and Medium "
        "findings, which is 92.4%. The controls range from directly enforced hardening, "
        "through runtime containment, to NetworkPolicy reach reduction.")
    d.callout("Coverage of High findings", [
        "All 139 High findings map to a deployed compensatory control. The 96 findings "
        "without direct coverage are all Medium, and a web application firewall (WAF) "
        "covers them."])

    d.h1("Scan Details")
    d.table(["Parameter", "Value"], [
        ["Scan type", "Static Application Security Testing (SAST), source code analysis"],
        ["Scope", "36 AccuKnox deployment repositories"],
        ["Security-category findings", "139 High, 1,121 Medium, 914 Low"],
        ["Total findings", "2,174"],
    ], widths=[2.2, 4.3], align=[L, L], bold_first=True)

    d.h1("Coverage by Existing Compensatory Controls")
    d.p("The AccuKnox compensatory controls apply KubeArmor process, file and network policies "
        "and securityContext hardening to the deployed workloads. The Compensatory Controls "
        "Assessment documents these controls.")
    d.p("AccuKnox applied this coverage standard to the SAST findings. Each control either "
        "reduces the reach of a finding or contains its blast radius.")
    d.table(["Compensatory controls", "High", "Medium", "Total", "What the controls do"], [
        ["securityContext\nKubeArmor container posture", "6", "146", "152",
         "Fully control or mitigate container posture issues"],
        ["Process allowlist\nFile path\nEgress policy gates\nInjection prevention", "70", "80",
         "150", "Mitigate the exploit action: command injection, path traversal, eval, "
                "deserialization, XXE"],
        ["NetworkPolicy\nIngress reach reduction\nEgress deny", "63", "799", "862",
         "Reduce the reach, and limit exfiltration and lateral movement: SQL injection, "
         "secrets, unverified JWT, TLS bypass, DoS"],
        ["Not directly covered", "0", "96", "96",
         "Run in the browser or outside the cluster: XSS, CSRF, weak crypto (MD5, SHA1), CI "
         "pull_request_target. A WAF covers these."],
        ["Total", "139", "1,121", "1,260", "1,164 findings covered, 96 covered by WAF"],
    ], widths=[1.9, 0.6, 0.75, 0.65, 2.6], align=[L, C, C, C, L], total_row=True,
        bold_first=True)

    d.h2("Coverage by Severity")
    d.table(["Severity", "Findings", "Covered by a deployed control", "Coverage"], [
        ["High", "139", "139", "100%"],
        ["Medium", "1,121", "1,025", "91.4%"],
        ["High and Medium", "1,260", "1,164", "92.4%"],
    ], widths=[1.7, 1.2, 2.4, 1.2], align=[L, C, C, C], bold_first=True)

    d.h1("Terms Used in This Report")
    d.table(["Term", "Meaning"], [
        ["SAST", "Static application security testing. The test reads source code for security "
                 "flaws without running the application."],
        ["Compensatory control", "A deployed control that reduces the risk of a finding while "
                                 "the code fix is pending."],
        ["securityContext", "Kubernetes settings that restrict a container, for example a "
                            "read-only root filesystem and dropped Linux capabilities."],
        ["KubeArmor", "The AccuKnox open source runtime security engine. It enforces process, "
                      "file and network policies inside each workload."],
        ["NetworkPolicy", "Kubernetes rules that set which peers can reach a workload and "
                          "where the workload can send traffic."],
        ["Reach reduction", "A control that lowers the number of peers that can reach a "
                            "vulnerable endpoint."],
    ], widths=[1.7, 4.8], align=[L, L], bold_first=True)
    closing(d)
    build(d, "06_AccuKnox_Source_Code_Review_Report")


# =========================================================================== main
if __name__ == "__main__":
    from docx.shared import Pt  # noqa: F401  (used inside build_malware)
    globals()["Pt"] = Pt
    OUT.mkdir(parents=True, exist_ok=True)
    EDIT.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[1:])

    def want(k):
        return not only or k in only

    if want("iso"):
        soc2 = build_iso()
        print("SOC 2 report found:", soc2)
    if want("arch"):
        copy_architecture()
    if want("sbom"):
        print(build_sbom())
    if want("malware"):
        build_malware()
    if want("wapt"):
        print(build_wapt())
    if want("sast"):
        build_sast()
