# Build the AccuKnox-branded v3.6 On-Prem Single Node Deployment Guide from
# WORD_TEMPLATE_ACCUKNOX.docx.
#
# Source: D:\Downloads\AccuKnox-v3.6 On-Prem Single Node Deployment Guide.pdf
# Content is kept as-is. Two source defects are corrected:
#   1. Step numbering skipped 6 (1,2,3,4,5,7,8). Renumbered 1 to 7.
#   2. The wget URL points at AccuKnox-cp-v3.6.tar.gz, the tar step used the
#      same name, so both now read AccuKnox-cp-v3.6.tar.gz.
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(REPO, "WORD_TEMPLATE_ACCUKNOX.docx")
LOGOS = os.path.join(REPO, "assets", "logos")
OUT = os.path.join(REPO, "output", "AccuKnox_v3.6_OnPrem_Single_Node_Deployment_Guide.docx")

NAVY = "11206D"
PRIMARY = "0046FF"
BORDER = "C4CCDE"
GREY_FILL = "EEF0F6"
MUTED = "5A6478"
BODY_FONT = "Space Grotesk"
MONO_FONT = "Consolas"

DOC_TITLE = "AccuKnox v3.6 On-Prem Single Node Deployment Guide"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc = Document(TEMPLATE)


# ---------------------------------------------------------------- helpers
def shade(el, hexval):
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hexval)
    el.append(sh)


def set_cell_margins(table_, top=90, bottom=90, left=120, right=120):
    mar = OxmlElement("w:tblCellMar")
    for name, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        e = OxmlElement("w:" + name)
        e.set(qn("w:w"), str(val))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    table_._tbl.tblPr.append(mar)


def set_borders(table_, color=BORDER, sz=6):
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        borders.append(e)
    table_._tbl.tblPr.append(borders)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement("w:tblHeader")
    e.set(qn("w:val"), "true")
    trPr.append(e)


def style_run(run, size=10.5, bold=False, color=None, italic=False, font=BODY_FONT):
    run.font.name = font
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    rPr = run._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rPr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), font)
    return run


def para(text="", style="normal", size=10.5, bold=False, color=None, italic=False,
         align=None, space_after=6, space_before=0, indent=None, hanging=None):
    p = doc.add_paragraph(style=style)
    if text:
        style_run(p.add_run(text), size=size, bold=bold, color=color, italic=italic)
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = 1.15
    if align is not None:
        p.alignment = align
    if indent is not None:
        pf.left_indent = Inches(indent)
    if hanging is not None:
        pf.first_line_indent = Inches(-hanging)
    return p


def rich(parts, size=10.5, space_after=6, indent=None, hanging=None, style="normal"):
    p = doc.add_paragraph(style=style)
    for text, bold in parts:
        style_run(p.add_run(text), size=size, bold=bold)
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.15
    if indent is not None:
        pf.left_indent = Inches(indent)
    if hanging is not None:
        pf.first_line_indent = Inches(-hanging)
    return p


def h1(text, newpage=False):
    p = doc.add_paragraph(style="Heading 1")
    style_run(p.add_run(text), size=18, bold=True)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0 if newpage else 20)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.page_break_before = newpage
    p.paragraph_format.keep_with_next = True
    return p


def h2(text):
    p = doc.add_paragraph(style="Heading 2")
    style_run(p.add_run(text), size=13.5, bold=True)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(5)
    return p


def bullet(text_or_parts, size=10.5):
    parts = [(text_or_parts, False)] if isinstance(text_or_parts, str) else list(text_or_parts)
    parts = [("\u2022\t", False)] + parts
    p = rich(parts, size=size, space_after=4, indent=0.28, hanging=0.28)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(0.28))
    return p


def code(lines, space_after=10):
    """A shaded single-cell table holding a monospace command block."""
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    set_borders(t)
    set_cell_margins(t, top=110, bottom=110, left=160, right=160)
    cell = t.rows[0].cells[0]
    cell.width = Inches(6.5)
    shade(cell._tc.get_or_add_tcPr(), GREY_FILL)
    for i, line in enumerate(lines):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        is_comment = line.strip().startswith("#")
        style_run(p.add_run(line), size=9.5, font=MONO_FONT,
                  color=MUTED if is_comment else NAVY,
                  italic=is_comment)
    para("", space_after=space_after)
    return t


def table(headers, rows, widths):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    set_borders(t)
    set_cell_margins(t)
    hdr = t.rows[0]
    repeat_header(hdr)
    for i, htext in enumerate(headers):
        cell = hdr.cells[i]
        shade(cell._tc.get_or_add_tcPr(), NAVY)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        style_run(p.add_run(htext), size=10, bold=True, color="FFFFFF")
    for r_i, row in enumerate(rows):
        cells = t.add_row().cells
        for i, val in enumerate(row):
            if r_i % 2 == 1:
                shade(cells[i]._tc.get_or_add_tcPr(), GREY_FILL)
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            style_run(p.add_run(val), size=10, bold=(i == 0))
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Inches(w)
    para("", space_after=8)
    return t


# ---------------------------------------------------------------- reset body
for p in list(doc.paragraphs):
    p._element.getparent().remove(p._element)

# ---------------------------------------------------------------- header / footer
sec = doc.sections[0]
hdr_p = sec.header.paragraphs[0]
for r in hdr_p.runs:
    if r.text.strip():
        r.text = DOC_TITLE
        style_run(r, size=10, bold=True, color=NAVY)

ftr = sec.footer.paragraphs[0]
ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in ftr.runs:
    style_run(r, size=9, color=MUTED)

# ---------------------------------------------------------------- cover page
sec.different_first_page_header_footer = True
if sec.first_page_header.paragraphs:
    sec.first_page_header.paragraphs[0].text = ""

para("", space_after=150)

lock = doc.add_paragraph(style="normal")
lock.alignment = WD_ALIGN_PARAGRAPH.CENTER
lock.paragraph_format.space_after = Pt(44)
lock.paragraph_format.line_spacing = 1.0
lock.add_run().add_picture(os.path.join(LOGOS, "accuknox-logo-light-bg.png"), width=Inches(2.4))

for line, gap in (("AccuKnox v3.6 On-Prem", 2), ("Single Node Deployment Guide", 12)):
    t = doc.add_paragraph(style="Title")
    style_run(t.add_run(line), size=30, bold=True, color=PRIMARY)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.paragraph_format.line_spacing = 1.0
    t.paragraph_format.space_before = Pt(0)
    t.paragraph_format.space_after = Pt(gap)

s = doc.add_paragraph(style="Subtitle")
style_run(s.add_run("Installation Guide"), size=17, color=NAVY)
s.alignment = WD_ALIGN_PARAGRAPH.CENTER
s.paragraph_format.line_spacing = 1.0
s.paragraph_format.space_after = Pt(6)

para("Tested on Ubuntu 24.04", size=11.5, color=MUTED,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)

para("Confidential & Proprietary  |  AccuKnox", size=9, color=MUTED,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=190, space_after=0)

# ---------------------------------------------------------------- prerequisites
h1("Hardware Prerequisites", newpage=True)
para("Check the node against these figures before you start. The installation was tested "
     "on Ubuntu 24.04.", size=11, space_after=10)

table(
    ["Deployment", "vCPU", "RAM", "Storage"],
    [
        ["Standard", "8", "32 GB", "256 GB"],
        ["AI-SPM and Ask-AI enabled", "12", "48 GB", "500 GB"],
    ],
    widths=[3.0, 1.0, 1.2, 1.3],
)

h2("Required binaries")
para("The node must have tar and wget available before step 1.", size=10.5, space_after=4)

# ---------------------------------------------------------------- 1
h1("1. Download the AccuKnox Installation Bundle")
code(["wget https://accuknox-onprem-artifacts.nbg1.your-objectstorage.com/\\",
      "     releases/AccuKnox-cp-v3.6.tar.gz"])

# ---------------------------------------------------------------- 2
h1("2. Extract the Bundle and Helm Chart")
code(["tar -xvf AccuKnox-cp-v3.6.tar.gz",
      "cd AccuKnox/",
      "",
      "tar -xvf Helm-charts-xxx.tar.gz",
      "cd Helm-charts-xxx/"])

# ---------------------------------------------------------------- 3
h1("3. Download the Required Container Images")
code(["cd image-downloader/"])

h2("Standard deployment images")
code(["./tar_download.sh --cspm"])

h2("Standard deployment with AI-SPM images")
code(["./tar_download.sh --cspm --aispm"])

h2("Private or local container registry (optional)")
para("Use this only if the node pulls from an air-gapped registry.", size=10.5, space_after=6)
code(["# connect to the air-gapped registry",
      "docker login --username <username> --password \"<pwd>\" \\",
      "    <registry_address>/<reponame>",
      "",
      "# upload the images to the private registry",
      "sudo ./push_tar_images.sh <registry_address>/<reponame>"])

# ---------------------------------------------------------------- 4
h1("4. Install the Required Binaries")
code(["cd ..", "./binaries.sh"])

# ---------------------------------------------------------------- 5
h1("5. Install K3s (Air-Gapped Setup)")
code(["./airgapped_k3s.sh server"])

# ---------------------------------------------------------------- 6
h1("6. Install the AccuKnox Helm Charts")
para("Prerequisite: the VM or node IP address.", size=10.5, space_after=8)

h2("Standard installation")
code(["./install_chart.sh"])
para("Give the server IP address or the DNS name as the input.", size=10.5, space_after=6)

h2("Enable AI-SPM (optional)")
para("Give the required API keys during the installation to enable the AI-SPM features.",
     size=10.5, space_after=6)
code(["./install_chart.sh --aispm"])

h2("Enable Ask-AI and the AI Copilot (optional)")
para("Give the required API keys to enable Ask-AI and Ask-Ada, the AI copilot.",
     size=10.5, space_after=6)
code(["./install_chart.sh --askai"])

# ---------------------------------------------------------------- 7
h1("7. Access the AccuKnox UI")
bullet("Open https://<SERVER-IP OR DNS>/ in a browser.")
bullet("Contact the AccuKnox team to complete the sign-up.")
para("", space_after=4)
code(["kubectl logs deploy/celery -n accuknox-divy"])
bullet("Use the generated link to complete the account activation. Contact the AccuKnox "
       "team if you need help.")

para("", space_after=6)
para("Confidential & Proprietary  |  AccuKnox", size=9, color=MUTED, space_before=14)

doc.save(OUT)
print("wrote", OUT)
