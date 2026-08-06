# Build the AccuKnox-branded Control Plane Hardware Prerequisites doc from
# WORD_TEMPLATE_ACCUKNOX.docx.
#
# Source: C:\Users\AtharvaShah\Downloads\AccuKnox ControlPlane hardware_prerequisites.pdf
# Two reviewer comments from the source doc are applied to the PVC table:
#   1. "divy backend requires 25GB of data"  -> celeryflower + divy-media + divy-staticfiles
#      collapse into one "divy" row at 25 Gi.
#   2. "same as above, use service name and combine the disk space" -> every multi-replica
#      PVC set (mongod, vault, rabbitmq) collapses to one service row with summed storage.
# Also corrected: total CPU read 112 vCPUs for "8 x 15 nodes", which is 120.
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
OUT = os.path.join(REPO, "output", "AccuKnox_ControlPlane_Hardware_Prerequisites.docx")

NAVY = "11206D"
PRIMARY = "0046FF"
BORDER = "C4CCDE"
GREY_FILL = "EEF0F6"
MUTED = "5A6478"
BODY_FONT = "Space Grotesk"

DOC_TITLE = "Control Plane Hardware Prerequisites"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc = Document(TEMPLATE)


# ---------------------------------------------------------------- helpers
def shade(el, hexval):
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hexval)
    el.append(sh)


def set_cell_margins(table, top=90, bottom=90, left=120, right=120):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for name, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        e = OxmlElement("w:" + name)
        e.set(qn("w:w"), str(val))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tblPr.append(mar)


def set_borders(table, color=BORDER, sz=6):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        borders.append(e)
    tblPr.append(borders)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement("w:tblHeader")
    e.set(qn("w:val"), "true")
    trPr.append(e)


def style_run(run, size=10.5, bold=False, color=None, italic=False):
    run.font.name = BODY_FONT
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
        rf.set(qn(a), BODY_FONT)
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


def table(headers, rows, widths, total_row=False, right_align_last=True):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    set_borders(t)
    set_cell_margins(t)
    hdr = t.rows[0]
    repeat_header(hdr)
    last = len(headers) - 1
    for i, htext in enumerate(headers):
        cell = hdr.cells[i]
        shade(cell._tc.get_or_add_tcPr(), NAVY)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        if right_align_last and i == last:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        style_run(p.add_run(htext), size=10, bold=True, color="FFFFFF")
    for r_i, row in enumerate(rows):
        cells = t.add_row().cells
        is_total = total_row and r_i == len(rows) - 1
        for i, val in enumerate(row):
            if is_total:
                shade(cells[i]._tc.get_or_add_tcPr(), "DDE3F5")
            elif r_i % 2 == 1:
                shade(cells[i]._tc.get_or_add_tcPr(), GREY_FILL)
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            if right_align_last and i == last:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            style_run(p.add_run(val), size=10,
                      bold=(i == 0 or is_total),
                      color=NAVY if is_total else None)
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

# ---------------------------------------------------------------- title block
# The template header already carries the logo on every page, so the title block
# stays type-only. No second lockup.
t = doc.add_paragraph(style="Title")
t.paragraph_format.space_before = Pt(18)
style_run(t.add_run("Hardware Prerequisites"), size=30, bold=True, color=PRIMARY)
t.alignment = WD_ALIGN_PARAGRAPH.LEFT
t.paragraph_format.space_after = Pt(2)

s = doc.add_paragraph(style="Subtitle")
style_run(s.add_run("AccuKnox Control Plane, Production Deployment"), size=15, color=NAVY)
s.alignment = WD_ALIGN_PARAGRAPH.LEFT
s.paragraph_format.space_after = Pt(14)

para("These are the minimum hardware resources needed to deploy and run the AccuKnox "
     "control plane in production mode. Check your infrastructure against these numbers "
     "before you start the installation.", size=11, space_after=4)

# ---------------------------------------------------------------- per-node
h1("Per-Node Requirements")
table(
    ["Resource", "Minimum Requirement"],
    [
        ["CPU", "8 vCPUs / cores"],
        ["Memory", "32 GB RAM"],
        ["Node Storage", "80 GB"],
        ["Number of Nodes", "15"],
    ],
    widths=[3.4, 3.1],
)

# ---------------------------------------------------------------- cluster-wide
h1("Cluster-Wide Requirements")
table(
    ["Resource", "Minimum Requirement"],
    [
        ["Total CPU", "120 vCPUs / cores (8 \u00d7 15 nodes)"],
        ["Total Memory", "480 GB RAM (32 GB \u00d7 15 nodes)"],
        ["PVC Storage", "1.36 TB (1,396 Gi of PVCs)"],
    ],
    widths=[3.4, 3.1],
)

# ---------------------------------------------------------------- PVC breakdown
h1("PVC Storage Breakdown", newpage=True)
para("Storage is listed per service, with every replica of a service summed into a single "
     "figure. The divy backend line covers its media, static file, and Celery Flower volumes.",
     size=10.5, space_after=10)

table(
    ["Service", "Storage"],
    [
        ["divy backend", "25 Gi"],
        ["mongod", "600 Gi"],
        ["postgres", "200 Gi"],
        ["neo4j", "150 Gi"],
        ["rabbitmq", "300 Gi"],
        ["keydb", "70 Gi"],
        ["redis", "20 Gi"],
        ["vault", "30 Gi"],
        ["obs-nfs", "1 Gi"],
        ["Total", "1,396 Gi (1.36 TB)"],
    ],
    widths=[3.4, 3.1],
    total_row=True,
)

h2("Replica counts behind the totals")
para("Three services run as multi-replica stateful sets, so their storage figure above is the "
     "sum of the per-replica volumes.", size=10.5, space_after=6)
bullet([("mongod: ", True), ("3 replicas \u00d7 200 Gi", False)])
bullet([("rabbitmq: ", True), ("3 replicas \u00d7 100 Gi", False)])
bullet([("vault: ", True), ("3 replicas \u00d7 10 Gi", False)])

para("", space_after=6)
para("Confidential & Proprietary  |  AccuKnox", size=9, color=MUTED, space_before=14)

doc.save(OUT)
print("wrote", OUT)
