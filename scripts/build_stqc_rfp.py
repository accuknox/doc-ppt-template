"""Build an AccuKnox-branded A4 landscape PDF from the STQC RFP compliance matrix.

Reads the RFP xlsx, emits branded HTML, then prints to PDF with headless Edge.
"""
import base64
import html
import os
import re
import subprocess
import sys

import openpyxl

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = r"C:\Users\AtharvaShah\Downloads\RFP for STQC (via partner Samar Infotech Delhi) - 24 June 2026.xlsx"
OUTDIR = os.path.join(REPO, "output")
HTML_OUT = os.path.join(OUTDIR, "STQC_RFP_AccuKnox_Compliance.html")
PDF_OUT = os.path.join(OUTDIR, "STQC_RFP_AccuKnox_Compliance.pdf")
LOGO = os.path.join(REPO, "assets", "logos", "accuknox-logo-dark-bg.png")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

NAVY = "#11206D"
BLUE = "#0046FF"
SEC_BLUE = "#6464FF"
RED = "#C80019"


STATUS_LABEL = {
    "AccuKnox Can Deliver Now": "Compliant",
    "Partially Compliant": "Partially compliant",
    "We do not do this": "Not offered",
}


def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def bullets(text):
    """Turn a cell of bullet lines into <li> items."""
    if not text:
        return ""
    lines = [l.strip(" \t•-") for l in str(text).split("\n")]
    lines = [l for l in lines if l]
    # join continuation lines (originals wrap with leading spaces)
    return "<ul>" + "".join("<li>%s</li>" % html.escape(l) for l in lines) + "</ul>"


def paras(text):
    if not text:
        return '<span class="na">Not applicable</span>'
    out = []
    for block in str(text).split("\n"):
        block = block.strip()
        if not block:
            continue
        block = html.escape(block)
        block = re.sub(r"(https?://\S+)", r'<span class="ref">\1</span>', block)
        out.append("<p>%s</p>" % block)
    return "".join(out)


def status_class(s):
    s = (s or "").lower()
    if "partial" in s:
        return "partial"
    if "compliant" in s or "can deliver" in s:
        return "ok"
    return "no"


def main():
    wb = openpyxl.load_workbook(XLSX)
    ws = wb["Sheet1"]
    rows = []
    for r in ws.iter_rows(min_row=3, values_only=True):
        if not r or not r[0]:
            continue
        rows.append({
            "sl": str(r[0]).replace(".0", ""),
            "item": (r[1] or "").replace("\n", " ").strip(),
            "spec": r[2],
            "lic": (r[3] or "").replace("\n", " ").strip(),
            "gom": (r[4] or "").strip(),
            "status": STATUS_LABEL.get((r[5] or "").strip(), (r[5] or "Not offered").strip()),
            "remark": r[6],
        })

    counts = {"ok": 0, "partial": 0, "no": 0}
    for row in rows:
        counts[status_class(row["status"])] += 1

    cards = []
    for row in rows:
        cls = status_class(row["status"])
        cards.append(f"""
    <section class="card">
      <div class="card-head">
        <div class="sl">{html.escape(row['sl'])}</div>
        <h2>{html.escape(row['item'])}</h2>
        <div class="meta">
          <span class="chip">{html.escape(row['lic'])}</span>
          <span class="chip">GeM: {html.escape(row['gom'] or '-')}</span>
        </div>
        <div class="status {cls}">{html.escape(row['status'])}</div>
      </div>
      <div class="card-body">
        <div class="col spec">
          <h3>Requirement</h3>
          {bullets(row['spec'])}
        </div>
        <div class="col resp">
          <h3>AccuKnox response</h3>
          {paras(row['remark'])}
        </div>
      </div>
    </section>""")

    doc = f"""<meta charset="utf-8">
<title>STQC RFP - AccuKnox Compliance Matrix</title>
<style>
  @page {{ size: A4 landscape; margin: 0; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: "Space Grotesk", "Segoe UI", sans-serif;
    color: #1B1F3B; font-size: 9.4pt; line-height: 1.42; background: #fff;
  }}
  .page {{
    width: 297mm; height: 210mm; padding: 12mm 13mm 11mm;
    page-break-after: always; position: relative; overflow: hidden;
  }}
  .page:last-child {{ page-break-after: auto; }}

  /* ---------- cover ---------- */
  .cover {{ background: {NAVY}; color: #fff; padding: 0; }}
  .cover .inner {{ padding: 20mm 18mm; height: 100%; display: flex; flex-direction: column; }}
  .cover img.logo {{ height: 11mm; width: auto; align-self: flex-start; flex: none; }}
  .cover .eyebrow {{
    margin-top: auto; letter-spacing: .18em; text-transform: uppercase;
    font-size: 9pt; color: {SEC_BLUE}; font-weight: 600;
  }}
  .cover h1 {{ font-size: 30pt; line-height: 1.15; margin: 4mm 0 3mm; max-width: 190mm; font-weight: 700; }}
  .cover .sub {{ font-size: 12pt; color: #C9D2FF; max-width: 175mm; }}
  .cover .rule {{ height: 3px; width: 46mm; background: {BLUE}; margin: 7mm 0; }}
  .cover .facts {{ display: flex; gap: 10mm; margin-top: 3mm; }}
  .cover .fact .n {{ font-size: 24pt; font-weight: 700; color: #fff; }}
  .cover .fact .l {{ font-size: 8.5pt; color: #A9B6EE; text-transform: uppercase; letter-spacing: .09em; }}
  .cover .foot {{ margin-top: auto; font-size: 8.5pt; color: #93A0DA; display: flex; justify-content: space-between; }}

  /* ---------- running header / footer ---------- */
  .hdr {{
    position: absolute; top: 0; left: 0; right: 0; height: 13mm; background: {NAVY};
    display: flex; align-items: center; justify-content: space-between; padding: 0 13mm; color: #fff;
  }}
  .hdr .t {{ font-size: 9pt; font-weight: 500; letter-spacing: .04em; }}
  .hdr img {{ height: 6.2mm; }}
  .ftr {{
    position: absolute; bottom: 6mm; left: 13mm; right: 13mm; display: flex;
    justify-content: space-between; font-size: 7.6pt; color: #6B7392;
    border-top: 1px solid #E1E5F2; padding-top: 2mm;
  }}
  .body {{ margin-top: 8mm; }}

  /* ---------- summary table ---------- */
  h2.sec {{ font-size: 15pt; color: {NAVY}; margin: 0 0 1mm; }}
  p.lede {{ color: #4A5170; margin: 0 0 4mm; max-width: 210mm; font-size: 9.4pt; }}
  .tile .n {{ font-size: 17pt; }}
  table.sum {{ width: 100%; border-collapse: collapse; }}
  table.sum th {{
    background: {NAVY}; color: #fff; text-align: left; font-size: 8.4pt; font-weight: 600;
    padding: 2.6mm 3mm; text-transform: uppercase; letter-spacing: .07em;
  }}
  table.sum td {{ padding: 1.5mm 3mm; border-bottom: 1px solid #E4E8F4; vertical-align: middle; }}
  table.sum tr:nth-child(even) td {{ background: #F6F8FE; }}
  table.sum td.n {{ color: {BLUE}; font-weight: 700; width: 10mm; }}
  table.sum td.name {{ font-weight: 600; width: 85mm; }}

  .pill {{
    display: inline-block; padding: 1mm 2.6mm; border-radius: 20px;
    font-size: 7.6pt; font-weight: 600; white-space: nowrap;
  }}
  .pill.ok {{ background: #E4EDFF; color: {BLUE}; }}
  .pill.partial {{ background: #EDEBFF; color: #4B3FC4; }}
  .pill.no {{ background: #FCE7E9; color: {RED}; }}

  .tiles {{ display: flex; gap: 5mm; margin-bottom: 4mm; }}
  .tile {{ flex: 1; border: 1px solid #E1E5F2; border-left: 3px solid {BLUE}; padding: 2.5mm 4mm; border-radius: 2px; }}
  .tile.p {{ border-left-color: {SEC_BLUE}; }}
  .tile.r {{ border-left-color: {RED}; }}
  .tile .n {{ font-size: 20pt; font-weight: 700; color: {NAVY}; line-height: 1; }}
  .tile .l {{ font-size: 8.2pt; color: #5A6180; margin-top: 1.5mm; }}

  /* ---------- detail cards ---------- */
  .card {{ border: 1px solid #E1E5F2; border-radius: 2px; overflow: hidden; }}
  .card-head {{
    background: #F4F7FE; border-bottom: 1px solid #E1E5F2; padding: 3mm 4mm;
    display: flex; align-items: center; gap: 4mm;
  }}
  .card-head .sl {{
    background: {BLUE}; color: #fff; width: 9mm; height: 9mm; border-radius: 2px;
    display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 11pt; flex: none;
  }}
  .card-head h2 {{ font-size: 13pt; margin: 0; color: {NAVY}; flex: none; }}
  .card-head .meta {{ display: flex; gap: 2mm; }}
  .chip {{ background: #E7ECFA; color: #3B4370; font-size: 7.4pt; padding: 1mm 2.4mm; border-radius: 2px; }}
  .card-head .status {{ margin-left: auto; font-size: 8.4pt; font-weight: 600; padding: 1.4mm 3.4mm; border-radius: 20px; }}
  .status.ok {{ background: #E4EDFF; color: {BLUE}; }}
  .status.partial {{ background: #EDEBFF; color: #4B3FC4; }}
  .status.no {{ background: #FCE7E9; color: {RED}; }}

  .card-body {{ display: flex; }}
  .col {{ padding: 4mm 4.5mm; }}
  .col.spec {{ width: 45%; background: #FAFBFF; border-right: 1px solid #E1E5F2; }}
  .col.resp {{ width: 55%; }}
  .col h3 {{
    font-size: 7.8pt; text-transform: uppercase; letter-spacing: .1em;
    color: #7A82A3; margin: 0 0 2.5mm; font-weight: 600;
  }}
  .col ul {{ margin: 0; padding-left: 4mm; }}
  .col li {{ margin-bottom: 1.1mm; }}
  .col p {{ margin: 0 0 2mm; }}
  .col .ref {{ color: {BLUE}; word-break: break-all; }}
  .na {{ color: #8A90AB; font-style: italic; }}
</style>

<div class="page cover">
  <div class="inner">
    <img class="logo" src="{data_uri(LOGO)}">
    <div class="eyebrow">RFP Compliance Response</div>
    <h1>STQC Application Security &amp; Testing Tools</h1>
    <div class="sub">Item-wise technical compliance matrix submitted by AccuKnox via partner Samar Infotech, Delhi</div>
    <div class="rule"></div>
    <div class="facts">
      <div class="fact"><div class="n">{len(rows)}</div><div class="l">Line items</div></div>
      <div class="fact"><div class="n">{counts['ok']}</div><div class="l">Deliverable now</div></div>
      <div class="fact"><div class="n">{counts['partial']}</div><div class="l">Partially compliant</div></div>
      <div class="fact"><div class="n">{counts['no']}</div><div class="l">Out of scope</div></div>
    </div>
    <div class="foot"><span>AccuKnox, Inc.</span><span>24 June 2026</span></div>
  </div>
</div>

<div class="page">
  <div class="hdr"><span class="t">STQC RFP Compliance Matrix</span><img src="{data_uri(LOGO)}"></div>
  <div class="body">
    <h2 class="sec">Compliance summary</h2>
    <p class="lede">Coverage across all {len(rows)} requirement lines in the STQC tender. Detailed
      requirement text and the corresponding AccuKnox capability follow on the next pages.</p>
    <div class="tiles">
      <div class="tile"><div class="n">{counts['ok']}</div><div class="l">Items AccuKnox can deliver today</div></div>
      <div class="tile p"><div class="n">{counts['partial']}</div><div class="l">Partially compliant, balance on roadmap</div></div>
      <div class="tile r"><div class="n">{counts['no']}</div><div class="l">Outside AccuKnox scope</div></div>
    </div>
    <table class="sum">
      <tr><th>Sl.</th><th>Item</th><th>License type</th><th>GeM</th><th>Compliance</th></tr>
      {"".join(f'''<tr><td class="n">{html.escape(r['sl'])}</td><td class="name">{html.escape(r['item'])}</td>
        <td>{html.escape(r['lic'])}</td><td>{html.escape(r['gom'] or '-')}</td>
        <td><span class="pill {status_class(r['status'])}">{html.escape(r['status'])}</span></td></tr>''' for r in rows)}
    </table>
  </div>
  <div class="ftr"><span>AccuKnox, Inc. | Confidential</span><span>STQC RFP, 24 June 2026</span></div>
</div>

{"".join(f'''<div class="page">
  <div class="hdr"><span class="t">STQC RFP Compliance Matrix</span><img src="{data_uri(LOGO)}"></div>
  <div class="body">{c}</div>
  <div class="ftr"><span>AccuKnox, Inc. | Confidential</span><span>STQC RFP, 24 June 2026</span></div>
</div>''' for c in cards)}
"""

    os.makedirs(OUTDIR, exist_ok=True)
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(doc)

    if os.path.exists(PDF_OUT):
        os.remove(PDF_OUT)
    subprocess.run([
        EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
        "--print-to-pdf=" + PDF_OUT, "--print-to-pdf-no-header",
        HTML_OUT.replace("\\", "/"),
    ], check=True, timeout=180)
    print("wrote", PDF_OUT, os.path.getsize(PDF_OUT), "bytes")


if __name__ == "__main__":
    sys.exit(main())
