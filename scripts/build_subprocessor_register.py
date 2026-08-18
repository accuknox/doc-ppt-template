"""Build the AccuKnox Sub-Processor Register as a ready-to-fill branded Word doc.

Source: AccuKnox_SubProcessor_Register.html export (Trust & Compliance draft).
All internal notices, illustrative examples, version stamps and page numbers are
stripped. What remains is the structure plus empty cells for teams to fill in.
"""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "WORD_TEMPLATE_ACCUKNOX.docx"
OUT = ROOT / "output" / "AccuKnox_SubProcessor_Register_Template.docx"

NAVY = RGBColor(0x11, 0x20, 0x6D)
PRIMARY = RGBColor(0x00, 0x46, 0xFF)
GREY_TEXT = RGBColor(0x55, 0x5B, 0x6E)
HEADER_FILL = "11206D"
LABEL_FILL = "EEF0F6"
BORDER = "C4CCDE"

doc = Document(TEMPLATE)


# ---------------------------------------------------------------- helpers
def set_header_title(text):
    p = doc.sections[0].header.paragraphs[0]
    for run in p.runs:
        if "Document Title" in run.text:
            run.text = text


def clear_footer():
    footer = doc.sections[0].footer
    for p in list(footer.paragraphs):
        p._p.getparent().remove(p._p)
    footer.add_paragraph()


def clear_body():
    for p in list(doc.paragraphs):
        p._p.getparent().remove(p._p)


def para(text="", style="normal", size=None, bold=None, color=None,
         space_before=None, space_after=None, italic=None):
    p = doc.add_paragraph(style=style)
    run = p.add_run(text)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    if space_before is not None:
        p.paragraph_format.space_before = Pt(space_before)
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p


def eyebrow(text):
    p = para(text.upper(), size=8.5, bold=True, color=PRIMARY,
             space_before=14, space_after=2)
    p.runs[0].font.name = "Space Grotesk"
    return p


def label_value(p, label, value):
    """Bold label, then the value (or a blank rule) on the same paragraph."""
    r = p.add_run(label)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r2 = p.add_run("  " + value)
    r2.font.size = Pt(9.5)
    return p


def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexfill)
    tcPr.append(shd)


def borders(table, color=BORDER, sz=4):
    tbl = table._tbl
    tblPr = tbl.tblPr
    for existing in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(existing)
    el = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        el.append(e)
    tblPr.append(el)


def cell_text(cell, text, size=9.5, bold=False, color=None, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    if align:
        p.alignment = align
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = "Space Grotesk"
    if color is not None:
        run.font.color.rgb = color
    return cell


def new_table(rows, cols, widths=None):
    t = doc.add_table(rows=rows, cols=cols)
    t.style = "TableNormal"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    borders(t)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
    return t


def header_row(table, headings):
    for i, h in enumerate(headings):
        c = table.rows[0].cells[i]
        cell_text(c, h.upper(), size=8, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        shade(c, HEADER_FILL)
    trPr = table.rows[0]._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:tblHeader"))


def blank_run(p, length=26, size=10):
    r = p.add_run("_" * length)
    r.font.size = Pt(size)
    r.font.color.rgb = GREY_TEXT
    return r


def field_table(fields, label_w=1.9, value_w=4.6):
    """Two-column label / blank-value grid."""
    t = new_table(len(fields), 2, widths=[label_w, value_w])
    for i, label in enumerate(fields):
        lc, vc = t.rows[i].cells
        cell_text(lc, label, size=9, bold=True, color=NAVY)
        shade(lc, LABEL_FILL)
        cell_text(vc, "")
    return t


def rule():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), BORDER)
    bdr.append(bottom)
    pPr.append(bdr)
    return p


# ---------------------------------------------------------------- build
set_header_title("Sub-Processor Register")
clear_footer()
clear_body()

para("", space_after=0)
eyebrow("DPA sub-processor disclosure")
title = para("Sub-Processor Register", style="Heading 1", space_before=0, space_after=6)
para(
    "Third parties engaged by AccuKnox, Inc. to process personal data on behalf of "
    "customers in the course of delivering the AccuKnox platform and related services, "
    "disclosed pursuant to the Data Processing Addendum (DPA).",
    size=10.5, color=GREY_TEXT, space_after=12,
)

# Document control block
t = field_table([
    "Effective date",
    "Document owner",
    "Review cadence",
    "Total sub-processors",
    "Primary data residency",
])
cell_text(t.rows[1].cells[1], "Legal / GRC")
cell_text(t.rows[2].cells[1], "Quarterly")

# ---- Overview
para("Overview", style="Heading 2", space_before=18, space_after=4)
para(
    "Counts below cover every service category in scope. Confirm the control-plane "
    "and customer-data storage regions with Infra/DevOps before release.",
    size=10, color=GREY_TEXT, space_after=8,
)
field_table([
    "Total sub-processors",
    "Infrastructure & hosting",
    "Cross-border transfers (SCCs / DPF)",
    "Primary data residency",
])

# ---- Category distribution
para("Category distribution", style="Heading 3", space_before=16, space_after=4)
cats = [
    "Infrastructure & hosting",
    "Communications / email",
    "Customer support",
    "Analytics & monitoring",
    "Payments / billing",
]
t = new_table(len(cats) + 1, 2, widths=[4.9, 1.6])
header_row(t, ["Processing category", "Count"])
for i, name in enumerate(cats, start=1):
    cell_text(t.rows[i].cells[0], name)
    cell_text(t.rows[i].cells[1], "", align=WD_ALIGN_PARAGRAPH.CENTER)

# ---- Summary register
para("Sub-processor register summary", style="Heading 2", space_before=20, space_after=4)
para(
    "One row per sub-processor. Add or remove rows so the table matches the vendors "
    "actually engaged.",
    size=10, color=GREY_TEXT, space_after=8,
)
summary_cols = ["Sub-processor", "Category", "Purpose of processing",
                "Data categories", "Location", "Transfer mechanism"]
summary_rows = [
    ("Infrastructure", "Cloud infrastructure hosting and data storage for the SaaS platform",
     "Account data, usage data, customer-uploaded content"),
    ("Communications", "Delivery of system and notification emails", "Name, email address"),
    ("Support", "Customer support case management", "Name, email, ticket contents"),
    ("Analytics", "Product usage analytics and error monitoring", "Usage and diagnostic data"),
    ("Payments", "Subscription billing and payment processing",
     "Billing contact, transaction data"),
]
t = new_table(len(summary_rows) + 1, 6, widths=[1.0, 1.45, 1.25, 1.2, 0.7, 0.9])
header_row(t, summary_cols)
for i, (cat, purpose, data) in enumerate(summary_rows, start=1):
    r = t.rows[i].cells
    cell_text(r[0], "", size=9)
    cell_text(r[1], cat, size=8, bold=True, color=NAVY)
    cell_text(r[2], purpose, size=8.5)
    cell_text(r[3], data, size=8.5)
    cell_text(r[4], "", size=8.5)
    cell_text(r[5], "", size=8.5)

# ---- Detail blocks
para("Sub-processor detail", style="Heading 2", space_before=20, space_after=4)
para(
    "One block per sub-processor. Copy a block for each additional vendor and delete "
    "any category that does not apply.",
    size=10, color=GREY_TEXT, space_after=10,
)

detail_fields = [
    "Sub-processor name",
    "Processing category",
    "Legal entity / HQ",
    "Processing location(s)",
    "Purpose of processing",
    "Data categories",
    "Transfer mechanism",
    "Why disclosed",
]
for n in range(1, 6):
    para("Sub-processor %d" % n, style="Heading 4", space_before=14, space_after=4)
    field_table(detail_fields)

# ---- Governance
para("Governance and customer rights", style="Heading 2", space_before=22, space_after=6)

gov = [
    ("Notification of change.",
     "AccuKnox will update this register and notify customers of any intended addition "
     "or replacement of a sub-processor with prior notice of ", ", per the DPA."),
    ("Right to object.",
     "Customers may object in writing to a new sub-processor within ",
     " of notice, stating reasonable data-protection grounds. The DPA governs the "
     "resolution and any termination rights."),
]
for label, before, after in gov:
    p = doc.add_paragraph(style="normal")
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(label + " ")
    r.font.bold = True
    r.font.size = Pt(10)
    r = p.add_run(before)
    r.font.size = Pt(10)
    blank_run(p, 18)
    r = p.add_run(after)
    r.font.size = Pt(10)

for label, body in [
    ("Due diligence.",
     "Each sub-processor is engaged under contract terms imposing data-protection "
     "obligations consistent with the DPA, and is reviewed as part of AccuKnox's "
     "third-party risk management program."),
    ("Scope.",
     "Not all sub-processors are used for all services or all deployments. On-premise "
     "and air-gapped deployments may involve few or no sub-processors, as data remains "
     "within the customer environment."),
    ("Integrations are not sub-processors.",
     "Tools a customer connects themselves, such as Jira, Slack, Splunk or Jenkins, do "
     "not belong in this register. Only third parties that process personal data on "
     "AccuKnox's behalf do."),
]:
    p = doc.add_paragraph(style="normal")
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(label + " ")
    r.font.bold = True
    r.font.size = Pt(10)
    r = p.add_run(body)
    r.font.size = Pt(10)

p = doc.add_paragraph(style="normal")
p.paragraph_format.space_after = Pt(8)
r = p.add_run("Questions and change notifications. ")
r.font.bold = True
r.font.size = Pt(10)
blank_run(p, 40)

rule()
p = para("AccuKnox, Inc.  ·  Sub-Processor Register", size=8.5, color=GREY_TEXT)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print("wrote", OUT)
