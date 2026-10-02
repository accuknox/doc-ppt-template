# -*- coding: utf-8 -*-
"""
ASPM Scanner SAST install guide for Arohan Dastech, on the AccuKnox Word letterhead.

Source: ASPM SAST.docx (text and three terminal screenshots, extracted to work/aspm_sast/src).
Run:  py -3.11 scripts/build_aspm_sast_guide.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from _akdoc import (AKDoc, to_pdf, add_text, shade, table_borders, MONO, NAVY, INK, MUTE,
                    PRIMARY, HEX_GREY_BG, HEX_GREY_BD)

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "work" / "aspm_sast" / "src" / "word" / "media"
OUT = ROOT / "output"
CLIENT = "Arohan Dastech"
NAME = "AccuKnox_ASPM_Scanner_SAST_Guide_Arohan_Dastech"


def code(d, lines, size=8.5):
    """A shaded monospace block, one line per command, with a blue left rule."""
    t = d._new_table(1, 1, [6.5])
    table_borders(t, color="FFFFFF", sz=0, val="nil")
    c = t.rows[0].cells[0]
    shade(c, HEX_GREY_BG)
    tcpr = c._tc.get_or_add_tcPr()
    el = OxmlElement("w:tcBorders")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "24")
    left.set(qn("w:space"), "0")
    left.set(qn("w:color"), "0046FF")
    el.append(left)
    tcpr.append(el)
    c.text = ""
    for i, line in enumerate(lines):
        para = c.paragraphs[0] if i == 0 else c.add_paragraph()
        para.paragraph_format.space_before = Pt(4 if i == 0 else 0)
        para.paragraph_format.space_after = Pt(4 if i == len(lines) - 1 else 1)
        para.paragraph_format.left_indent = Inches(0.05)
        add_text(para, line, size=size, color=NAVY, font=MONO)
    # Keep a block on one page.
    for para in c.paragraphs:
        para.paragraph_format.keep_together = True
    d.p("", after=3)


def shot(d, name, caption):
    para = d.p("", after=2, keep=True)
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.add_run().add_picture(str(MEDIA / name), width=Inches(6.3))
    d.p(caption, size=8.5, color=MUTE, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=8)


def step(d, n, title, before=10):
    d.h3(f"Step {n}. {title}", before=before)


d = AKDoc("ASPM Scanner for Windows")

d.eyebrow("Install guide")
d.title("Run SAST Scans on Windows with the AccuKnox ASPM Scanner",
        f"Install guide and first scan, prepared for {CLIENT}")
d.kv_table([
    ("Prepared for", CLIENT),
    ("Prepared by", "AccuKnox, Inc."),
    ("Date of issue", "1 October 2026"),
    ("Platform", "Windows x64"),
])

d.h1("One CLI Runs Every AccuKnox Security Scan on Windows")
d.p("The accuknox-aspm-scanner is one command line tool for AccuKnox security scans. "
    "It runs on a Windows machine or a build agent.")
d.bullets([
    ("Scans.", "IaC, SAST, SCA, Secret, SBOM, Container, ML model, API discovery, "
               "SonarQube SAST and DAST."),
    ("Upload is optional.", "Send results to the AccuKnox ASPM platform. Or pass "
                            "--skip-upload to run standalone."),
    ("Two run modes.", "Local mode uses native tools with no Docker. Container mode "
                       "uses Docker Desktop."),
])
d.callout("What you need",
          ["Windows x64 and PowerShell. Python is not required.",
           "Docker Desktop is needed only for container mode."])

d.h1("Eight Steps Take You From Download to First Scan")

step(d, 1, "Create the install folder", before=4)
code(d, ["mkdir C:\\accuknox"])

step(d, 2, "Download the executable")
dl = d.p("Download accuknox-aspm-scanner.exe from the Assets list of release v0.15.2 on "
         "GitHub releases. The same build is also published as "
         "accuknox-aspm-scanner-windows-amd64.exe. "
         "Or run this command to save the latest release to C:\\accuknox.", keep=True)
dl.paragraph_format.keep_together = True
code(d, ['curl -L -o "C:\\accuknox\\accuknox-aspm-scanner.exe" '
         '"https://github.com/accuknox/aspm-scanner-cli/releases/download/'
         'v0.15.2-rc.3/accuknox-aspm-scanner.exe"'])

step(d, 3, "Add the folder to PATH")
code(d, ["set PATH=%PATH%;C:\\accuknox"])

step(d, 4, "Validate the version")
code(d, ["accuknox-aspm-scanner.exe --version"])
shot(d, "image1.png", "The version check prints the AccuKnox ASPM Scanner banner and version.")

step(d, 5, "List the available commands")
d.p("This command shows the commands, options and usage for the scanner.")
code(d, ["accuknox-aspm-scanner --help"])

step(d, 6, "Set the upload variables (optional)")
d.p("Skip this step to run standalone. Run these commands in Command Prompt to upload "
    "results to AccuKnox. Do not put quotes around the values.")
code(d, ["set ACCUKNOX_ENDPOINT=cspm.accuknox.com",
         "set ACCUKNOX_LABEL=POC",
         "set ACCUKNOX_TOKEN=<token>"])
d.table(["Variable", "Value", "Where to get it"], [
    ["ACCUKNOX_ENDPOINT", "cspm.accuknox.com", "The AccuKnox platform address."],
    ["ACCUKNOX_LABEL", "A unique name with no spaces", "Go to Setting > Label and create it."],
    ["ACCUKNOX_TOKEN", "Your API token", "Go to Setting > Token and select Create a Token."],
], widths=[1.8, 2.1, 2.6], bold_first=True)

step(d, 7, "Install the SAST tool (local mode)")
code(d, ["accuknox-aspm-scanner.exe tool install --type sast"])
shot(d, "image2.png", "The installer reports that sast installed successfully.")

step(d, 8, "Run the SAST scan")
code(d, ['accuknox-aspm-scanner.exe scan sast --command "scan ."'])
shot(d, "image3.png", "The scanner validates the SAST scan configuration.")

d.h1("Contact")
d.p("Send questions about this guide to the AccuKnox team at support@accuknox.com.")

docx_path = d.save(ROOT / "work" / "aspm_sast" / f"{NAME}.docx")
pdf_path = OUT / f"{NAME}.pdf"
OUT.mkdir(parents=True, exist_ok=True)
to_pdf(docx_path, pdf_path)
print("wrote", pdf_path)
