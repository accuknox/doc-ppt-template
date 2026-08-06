# Build the AccuKnox-branded SIEM Deployment Proposal from WORD_TEMPLATE_ACCUKNOX.docx.
# Source content: D:\AccuKnox_SIEM_Proposal.pdf (text + figures extracted with pymupdf).
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(REPO, "WORD_TEMPLATE_ACCUKNOX.docx")
LOGOS = os.path.join(REPO, "assets", "logos")
FIGS = r"C:\Users\ATHARV~1\AppData\Local\Temp\claude\D--Atharva-AccuKnox-doc-ppt-template\ddf40db5-cda5-4f9d-828d-005292061f4e\scratchpad\figs"
OUT = os.path.join(REPO, "output", "AccuKnox_SIEM_Proposal_Branded.docx")

NAVY = "11206D"
PRIMARY = "0046FF"
BORDER = "C4CCDE"
GREY_FILL = "EEF0F6"
BODY_FONT = "Space Grotesk"

DOC_TITLE = "AccuKnox SIEM Proposal"

doc = Document(TEMPLATE)

# ---------------------------------------------------------------- helpers
def shade(el, hexval):
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hexval)
    el.append(sh)

def set_cell_margins(table, top=80, bottom=80, left=110, right=110):
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
    """parts: list of (text, bold) tuples."""
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
    p.paragraph_format.space_before = Pt(13)
    p.paragraph_format.space_after = Pt(5)
    return p

def h3(text):
    p = doc.add_paragraph(style="Heading 3")
    style_run(p.add_run(text), size=11.5, bold=True)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    return p

def bullet(text_or_parts, size=10.5):
    parts = [(text_or_parts, False)] if isinstance(text_or_parts, str) else list(text_or_parts)
    parts = [("•\t", False)] + parts
    p = rich(parts, size=size, space_after=4, indent=0.28, hanging=0.28)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(0.28))
    return p

def figure(fname, caption, width=6.0):
    p = doc.add_paragraph(style="normal")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.add_run().add_picture(os.path.join(FIGS, fname), width=Inches(width))
    c = para(caption, size=9, italic=True, color="5A6478",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    return c

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
            style_run(p.add_run(val), size=9.5, bold=(i == 0))
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Inches(w)
    para("", space_after=6)
    return t

def page_break():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# ---------------------------------------------------------------- reset body
body = doc.element.body
for p in list(doc.paragraphs):
    p._element.getparent().remove(p._element)

# ---------------------------------------------------------------- header / footer
hdr_p = doc.sections[0].header.paragraphs[0]
for r in hdr_p.runs:
    if r.text.strip():
        r.text = DOC_TITLE
        style_run(r, size=10, bold=True, color=NAVY)

sec = doc.sections[0]
sec.different_first_page_header_footer = True
first = sec.first_page_header
if first.paragraphs:
    first.paragraphs[0].text = ""

ftr = sec.footer.paragraphs[0]
ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in ftr.runs:
    style_run(r, size=9, color="5A6478")

# ---------------------------------------------------------------- cover
para("", space_after=90)
cover = doc.add_paragraph(style="normal")
cover.alignment = WD_ALIGN_PARAGRAPH.CENTER
cover.add_run().add_picture(os.path.join(LOGOS, "accuknox-logo-light-bg.png"), width=Inches(2.6))
cover.paragraph_format.space_after = Pt(36)

t = doc.add_paragraph(style="Title")
style_run(t.add_run("AccuKnox SIEM"), size=34, bold=True, color=PRIMARY)
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
t.paragraph_format.space_after = Pt(4)

s = doc.add_paragraph(style="Subtitle")
style_run(s.add_run("SIEM Deployment Proposal"), size=19, color=NAVY)
s.alignment = WD_ALIGN_PARAGRAPH.CENTER
s.paragraph_format.space_after = Pt(10)

para("Unified Log Ingestion, Threat Detection & Compliance-Ready Retention",
     size=11.5, color="5A6478", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=200)

para("Confidential & Proprietary  |  AccuKnox", size=9, color="5A6478",
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)

# ---------------------------------------------------------------- TOC
h1("Table of Contents")
TOC = [
    "Executive Summary", "Requirements Traceability", "AccuKnox SIEM: Solution Overview",
    "Scope of Work: Log Source Mapping", "Technical Architecture", "Platform Walkthrough",
    "Data Retention & Storage Management", "Product Capabilities",
    "Integration & Interoperability Strategy", "Phased Deployment Roadmap",
    "Security, Compliance & Auditability", "Business Impact",
    "Support & Service-Level Commitment", "Proposal Summary",
    "Appendix A: AccuKnox Multi-tenancy & Scalability", "Appendix B: Integration Ecosystem",
    "Appendix C: POC Timeline & Checklist",
    "Appendix D: Syslog Integration Approach for Firewalls",
]
for item in TOC:
    p = para(item, size=11, color=NAVY, space_after=7)
    p.paragraph_format.left_indent = Inches(0.15)

# ---------------------------------------------------------------- Executive Summary
h1("Executive Summary", newpage=True)
para("The organization is consolidating log visibility across its cloud, SaaS, endpoint, and "
     "network estate into a single SIEM platform, with a one-year retention window and six months "
     "of searchable data to meet audit and compliance obligations. This proposal outlines how "
     "AccuKnox SIEM meets that requirement for the fifteen log sources identified during discovery.")
rich([("Scope of this proposal: ", True),
      ("AccuKnox SIEM covers log ingestion, normalization, correlation, threat detection, dashboards, "
       "alerting, and compliance-ready retention and search. Automated remediation (Cloud Detection & "
       "Response) is out of scope for this engagement. The organization's requirement, as scoped, is "
       "detection and monitoring only. No auto-remediation actions, playbooks, or write-access to the "
       "organization's cloud accounts are configured as part of this deployment.", False)])

h2("What AccuKnox SIEM delivers")
bullet([("Unified log ingestion: ", True),
        ("AWS (CloudTrail, VPC Flow Logs, WAF, Config, Route 53, Network Firewall), GCP audit/activity "
         "logs, OCI audit logs, Google Workspace, MongoDB, Slack, Jamf, Cisco Meraki, CrowdStrike FDR, "
         "AquaSec, and Palo Alto firewalls, all fifteen sources from discovery.", False)])
bullet([("Retention that meets the compliance requirement: ", True),
        ("1-year log retention with 6 months of searchable, metadata-indexed data, plus on-demand "
         "audit log export.", False)])
bullet([("Threat detection and correlation: ", True),
        ("out-of-the-box detectors for AWS CloudTrail, GCP, and Kubernetes, custom detectors for the "
         "organization's SaaS and endpoint sources, threat intelligence enrichment, and MITRE ATT&CK "
         "mapping.", False)])
bullet([("Purpose-built dashboards and alerting: ", True),
        ("custom SOC dashboards, saved searches, and notifications to Slack, Jira, ServiceNow, or "
         "email.", False)])
bullet([("Native hand-off to AccuKnox CNAPP: ", True),
        ("SIEM findings surface in AccuKnox CNAPP's unified asset and findings view for teams already "
         "using AccuKnox CSPM/CWPP.", False)])

h2("Why AccuKnox")
bullet("We meet the ingestion, retention, and detection requirements the organization outlined during "
       "discovery, using the same log sources and methods already validated on the AccuKnox platform.")
bullet("AccuKnox was founded in partnership with SRI International, the R&D lab behind the computer "
       "mouse, the modem, and some of the earliest intrusion detection research, giving the detection "
       "engine a strong technical foundation.")
bullet("We run a structured, time-boxed POC so the organization can validate ingestion, detection, and "
       "retention against its own data before committing to a full rollout.")
bullet("Cloud-native ingestion pipelines scale to 100K events/second and 1TB/day per tenant, so the "
       "organization's log volumes are handled with headroom.")

# ---------------------------------------------------------------- Requirements Traceability
h1("Requirements Traceability")
para("A quick reference confirming how this proposal addresses each requirement the organization "
     "outlined during discovery.")
table(["Customer Requirement", "How AccuKnox SIEM Meets It"], [
    ["All 15 log sources ingested (AWS x6, GCP, OCI, Google Workspace, MongoDB, Slack, Jamf, Meraki, "
     "CrowdStrike FDR, AquaSec, Palo Alto)",
     "Scope of Work table maps every source to a specific ingestion method, see the next section."],
    ["1-year log retention",
     "Confirmed platform default for all onboarded sources; see Data Retention & Storage Management."],
    ["6 months of searchable data",
     "Metadata-based indexing keeps the most recent 6 months fully searchable; see Data Retention & "
     "Storage Management."],
    ["Compliance/audit readiness",
     "On-demand and scheduled audit log export (JSON/CSV); see Security, Compliance & Auditability."],
    ["Syslog-only firewalls (Meraki, Palo Alto) supported",
     "Syslog-to-JSON middleware VM architecture; see Appendix D."],
], [2.4, 4.1])

# ---------------------------------------------------------------- Solution Overview
h1("AccuKnox SIEM: Solution Overview")
para("AccuKnox SIEM is a cloud-native log ingestion, correlation, and threat-detection platform, "
     "available as a SaaS deployment at siem.accuknox.com. It is a distinct product from AccuKnox "
     "CNAPP, with a native integration between the two: SIEM detections and threat-analysis alerts "
     "surface directly inside the CNAPP console, so teams already using AccuKnox for CSPM or CWPP get "
     "a single pane of glass for findings.")
figure("p05_x23.png",
       "Figure 1. AccuKnox SIEM data flow: sources, ingestion, detection, and downstream channels.")

h2("Core capabilities")
bullet([("Data/log ingestion: ", True),
        ("LogStash, Bulk API, and Data Prepper connectors covering HTTP, Kafka, OTel, S3, Kinesis, "
         "DynamoDB, DocumentDB, and Fluentd inputs, in addition to native cloud log sinks and vendor "
         "APIs.", False)])
bullet([("Extensive integration coverage: ", True),
        ("cloud platforms, identity providers, SaaS applications, endpoint agents, firewalls (via "
         "syslog), and Kubernetes. See the Scope of Work below for the organization's specific set, "
         "and Appendix B for the full platform catalog.", False)])
bullet([("Threat analysis: ", True),
        ("multivector correlation across cloud, identity, and network events, with anomaly detection "
         "and threat hunting built in.", False)])
bullet([("Threat intelligence enrichment: ", True),
        ("alerts are enriched against external threat intel sources (including AlienVault) for IP and "
         "domain reputation.", False)])
bullet([("Snapshots: ", True),
        ("periodic snapshots of indexed data support recoverability and business continuity.", False)])
bullet([("Native CNAPP integration: ", True),
        ("SIEM alerts and cloud telemetry feed directly into AccuKnox CNAPP's asset and findings "
         "views. CNAPP calls SIEM APIs for CloudTrail and cloud access data, and KubeArmor runtime "
         "events flow in as a custom SIEM log type with purpose-built detectors.", False)])
bullet([("External channel integrations: ", True),
        ("Slack, webhooks, and Amazon SNS for downstream notification and ticketing workflows.", False)])

h2("Ingestion at scale, per tenant")
para("Each tenant's ingestion runs through its own isolated pipeline inside the AccuKnox SIEM "
     "Kubernetes cluster. The organization's data would land in its own namespace (for example, "
     "tenant.accuknox.com) with a dedicated ingestion pipeline, separate from every other tenant on "
     "the platform. Cloud telemetry, endpoint data, and syslog sources all flow through this "
     "per-tenant pipeline into the shared storage backend, which is what lets the platform scale to "
     "100K events/second and 1TB/day per tenant without one tenant's volume affecting another's.")

h2("AskADA: GenAI-powered SOC copilot")
para("AccuKnox AskADA is a GenAI copilot that runs on top of SIEM and CNAPP data. It performs "
     "multivector threat analysis by combining the organization's own findings and telemetry with "
     "external threat-intelligence sources, giving the organization's SOC analysts faster triage and "
     "analysis across cloud and endpoint assets without manually pivoting between tools.")

h2("Platform differentiation")
bullet("Custom rules and detectors across syslog, KubeArmor, EDR, CloudTrail, and O365 log types, not "
       "just a fixed rule pack.")
bullet("MITRE ATT&CK alignment spans Cloud, Container, and Endpoint tactics, not just cloud API calls.")
bullet("Low-cost ingestion, storage, and processing architecture, which is what keeps per-GB retention "
       "costs down over a 1-year window.")
bullet("Correlation and prioritization are built to reduce SOC analyst hours spent triaging noise, not "
       "just to generate more alerts.")

# ---------------------------------------------------------------- Scope of Work
h1("Scope of Work: Log Source Mapping", newpage=True)
para("The table below maps each of the fifteen log sources identified during discovery to its "
     "ingestion method on AccuKnox SIEM. Sources fall into three categories: cloud platforms ingested "
     "through each provider's native logging service, SaaS/endpoint tools connected through vendor "
     "APIs, and syslog-only firewalls that route through a lightweight middleware VM.")
table(["Log Source", "Ingestion Method", "Notes"], [
    ["AWS CloudTrail", "Native, AWS CloudTrail via scoped IAM role",
     "Management and data events; onboarded via the standard AWS CloudFormation onboarding stack."],
    ["AWS VPC Flow Logs", "Native, CloudWatch Logs / S3 export",
     "Same AWS onboarding stack as CloudTrail; no separate agent."],
    ["AWS WAF", "Native, S3 / Kinesis Firehose log export",
     "Web ACL logs delivered via existing AWS onboarding."],
    ["AWS Config", "Native, S3 export of Config snapshots and history", "Same AWS onboarding stack."],
    ["Route 53", "Native, CloudWatch Logs (query logging)", "Same AWS onboarding stack."],
    ["AWS Network Firewall", "Native, CloudWatch Logs / S3 export",
     "Flow and alert logs; same AWS onboarding stack."],
    ["GCP Audit / Activity Logs", "Native, Cloud Logging log sink to Pub/Sub",
     "AccuKnox SIEM consumes the sink directly; no forwarder required."],
    ["OCI Audit Logs", "Native, OCI Logging via Streaming / Object Storage export",
     "Read-only export configuration in the OCI tenancy."],
    ["Google Workspace", "API, Admin SDK Reports API", "Login, admin, and application audit events."],
    ["MongoDB (Atlas)", "API, Atlas Audit Log / Atlas Administration API",
     "Database and project-level audit events."],
    ["Slack", "API, Enterprise Grid Audit Logs API", "Workspace and admin audit events."],
    ["Jamf", "API, Jamf Pro API / webhook events", "Device management and compliance events."],
    ["CrowdStrike FDR", "Native, Falcon Data Replicator (S3-based)",
     "AccuKnox SIEM reads directly from the FDR S3 bucket."],
    ["AquaSec", "API, Aqua Platform API / webhook", "Container and workload security events."],
    ["Cisco Meraki", "Syslog → Syslog VM middleware → AccuKnox SIEM",
     "See Appendix D for the syslog-to-JSON middleware architecture."],
    ["Palo Alto Firewall", "Syslog → Syslog VM middleware → AccuKnox SIEM",
     "See Appendix D for the syslog-to-JSON middleware architecture."],
], [1.5, 2.1, 2.9])

h2("How cloud-native ingestion works")
para("For AWS, GCP, and OCI, AccuKnox SIEM ingests logs directly through each provider's native "
     "logging and monitoring service: CloudTrail for AWS, Cloud Logging log sinks for GCP, and the "
     "Logging service for OCI. No forwarders or agents run on the organization's infrastructure for "
     "these three platforms. Onboarding follows AccuKnox's standard SIEM onboarding workflow:")
bullet("AWS SIEM Onboarding Guide")
bullet("GCP SIEM Onboarding Guide")
para("AccuKnox uses one shared cloud-connection workflow for both log ingestion and (where separately "
     "licensed) automated response, so the same onboarding steps apply regardless of which capability "
     "is enabled. For this engagement, only detection and monitoring are configured. No remediation "
     "actions are enabled on the organization's cloud accounts.",
     size=9.5, italic=True, color="5A6478", space_before=6)

# ---------------------------------------------------------------- Technical Architecture
h1("Technical Architecture", newpage=True)
para("AccuKnox SIEM ingests events from the organization's cloud accounts, SaaS applications, and "
     "network appliances, normalizes them into a common schema, and runs them through detectors, "
     "correlation, and threat-intelligence enrichment before surfacing results in dashboards and "
     "external channels.")
figure("p05_x23.png",
       "Figure 2. AccuKnox SIEM architecture, as deployed for the organization's scope "
       "(log ingestion, detection, dashboards and channels).")

h2("Architecture layers")
bullet([("Sources: ", True),
        ("AWS, Google Workspace, and the AccuKnox CNAPP events feed connect through their native "
         "APIs; VMs, EDR tools, and syslog-only appliances (Cisco Meraki, Palo Alto) forward through "
         "syslog.", False)])
bullet([("Data ingestion: ", True),
        ("LogStash, Bulk API, and Data Prepper receive and normalize events across all supported log "
         "types before they are written to the data store.", False)])
bullet([("Data store: ", True),
        ("logs are indexed with enriched metadata (source, timestamp, event type, severity, account, "
         "region), which is what makes 6-month search fast without scanning raw log volumes.", False)])
bullet([("Detectors and intelligence: ", True),
        ("detection rules and threat-intelligence sources (including AlienVault) run continuously "
         "against ingested data, feeding threat analysis, correlations, threat hunting, and the MITRE "
         "ATT&CK mapping.", False)])
bullet([("Dashboards and API layer: ", True),
        ("the AccuKnox SIEM Portal and API layer expose search, dashboards, and snapshots; AccuKnox "
         "AskADA adds GenAI-assisted multivector threat analysis on top of the same data.", False)])
bullet([("Channels: ", True),
        ("detections and snapshots can notify out to Slack, webhooks, and Amazon SNS for the "
         "organization's SOC workflows.", False)])
bullet([("Data archival: ", True),
        ("logs beyond the 6-month searchable window move to archival storage and remain retrievable "
         "through the 1-year retention period.", False)])

# ---------------------------------------------------------------- Platform Walkthrough
h1("Platform Walkthrough", newpage=True)
para("A look at the two layers the organization's team would work in day to day: the SIEM backend, "
     "where logs are stored, queried, and visualized, and the AccuKnox UI, where alerts are triaged.")

h2("SIEM backend: log storage and query layer")
para("The SIEM backend is where ingested logs are stored and queried directly. Access is "
     "tenant-scoped and authenticated per user.")
figure("p09_x35.png", "Figure 3. AccuKnox SIEM backend login.", width=5.4)
para("Once logged in, the backend exposes purpose-built dashboards per log source. The example below "
     "is an AWS CloudTrail operations dashboard, showing total event volume, error/access-denied "
     "counts, unique identities, and activity trends over a selected time window.")
figure("p10_x38.png", "Figure 4. AWS CloudTrail operations dashboard on the AccuKnox SIEM backend.")

h2("AccuKnox UI: alerts")
para("Detections surface as alerts in the main AccuKnox UI, where the organization's SOC team would "
     "triage them day to day, filterable by module, status, log source, and severity, with saved "
     "filters and export.")
figure("p10_x39.png",
       "Figure 5. AccuKnox UI, Alerts page: active syslog-sourced alerts filtered by severity.")
para("Each alert opens into full detail, including the raw log payload, for investigation and audit "
     "purposes.")
figure("p11_x42.png", "Figure 6. AccuKnox UI, alert detail view with raw log payload.")

# ---------------------------------------------------------------- Retention
h1("Data Retention & Storage Management", newpage=True)
para("The organization's stated requirement is 1-year log retention with 6 months of searchable data "
     "for compliance and audit purposes. AccuKnox SIEM's storage model is built around exactly this "
     "pattern:")
bullet([("1-year retention: ", True),
        ("all ingested logs from every source in the Scope of Work above are retained for a full "
         "year.", False)])
bullet([("6-month searchable window: ", True),
        ("the most recent 6 months of data is indexed and fully searchable through metadata-based "
         "storage, so investigations and audits query fast without scanning raw log volumes.", False)])
bullet([("Metadata-based indexing: ", True),
        ("logs are enriched with source, timestamp, event type, severity, account, and region "
         "metadata at ingestion, which is what keeps 6-month search performant.", False)])
bullet([("Data archival: ", True),
        ("logs beyond the 6-month searchable window move to cold, S3-compatible archival storage and "
         "remain restorable on demand through month 12.", False)])
bullet([("Ingestion and storage controls: ", True),
        ("per-tenant ingestion limits and storage quotas are configurable, so upper limits are "
         "enforced and costs stay predictable.", False)])
bullet([("Snapshots and backup: ", True),
        ("periodic snapshots of indexed data protect against data loss and support recoverability.",
         False)])
bullet([("Audit log exports: ", True),
        ("scheduled or on-demand export of logs in JSON or CSV format for compliance reviews and "
         "regulatory submissions.", False)])
bullet([("Tenant isolation: ", True),
        ("the organization's log data is isolated from other AccuKnox tenants at the storage layer, "
         "with separate index namespaces and separate database collections/tables.", False)])

# ---------------------------------------------------------------- Product Capabilities
h1("Product Capabilities", newpage=True)
table(["Capability", "Details"], [
    ["Log Ingestion & Retention",
     "LogStash, Bulk API, Data Prepper (HTTP, Kafka, OTel, S3, Kinesis, DynamoDB, DocumentDB, "
     "Fluentd) plus native cloud and vendor-API connectors. 100K events/sec, 1TB/day/tenant, 1-year "
     "retention with a 6-month searchable window."],
    ["Threat Detection & Rules",
     "Out-of-the-box detectors for AWS CloudTrail, GCP, and Kubernetes, plus custom detectors "
     "authored for the organization's CrowdStrike, AquaSec, MongoDB, Google Workspace, Meraki, and "
     "Palo Alto sources."],
    ["Correlation & Analytics",
     "Multivector correlation, anomaly detection, and threat hunting across cloud, identity, and "
     "network sources, with MITRE ATT&CK framework alignment."],
    ["Threat Intelligence",
     "Alerts enriched against external threat intelligence sources (including AlienVault) for IP and "
     "domain reputation."],
    ["Dashboards & Reporting",
     "Custom dashboards, saved searches, metadata-based log storage, and scheduled or on-demand audit "
     "log exports."],
    ["Alerting & Notifications",
     "Slack, webhook, and Amazon SNS notification channels for the organization's SOC workflows. No "
     "automated remediation actions are configured. Alerts are informational and route to the "
     "organization's own response process."],
    ["Native CNAPP Integration",
     "SIEM alerts and cloud telemetry feed into AccuKnox CNAPP's asset and findings views for teams "
     "already using AccuKnox CSPM/CWPP."],
    ["RBAC & Multi-tenancy",
     "Multi-tenant architecture with granular role-based access control and SSO/SAML/MFA support; "
     "per-tenant custom views and reports."],
], [1.8, 4.7])

# ---------------------------------------------------------------- Integration strategy
h1("Integration & Interoperability Strategy", newpage=True)
para("AccuKnox SIEM covers all fifteen of the organization's priority log sources identified during "
     "discovery, alongside 70+ additional integrations available on the platform (Appendix B has a "
     "snapshot).")
h3("1. Cloud platforms, native onboarding")
bullet([("AWS: ", True), ("CloudTrail, VPC Flow Logs, WAF, Config, Route 53, Network Firewall, "
                          "onboarded together via the standard CloudFormation onboarding template.",
                          False)])
bullet([("GCP: ", True), ("audit and activity logs via Cloud Logging log sink.", False)])
bullet([("OCI: ", True), ("audit logs via the OCI Logging service.", False)])
h3("2. SaaS and endpoint, API connectors")
bullet([("Identity & collaboration: ", True), ("Google Workspace, Slack, Jamf.", False)])
bullet([("Data & workload: ", True), ("MongoDB Atlas, CrowdStrike FDR, AquaSec.", False)])
h3("3. Network appliances, syslog middleware")
bullet("Cisco Meraki and Palo Alto firewalls forward Syslog to a dedicated Syslog VM, which converts "
       "events to JSON before AccuKnox SIEM ingests them via Bulk API. Full architecture in Appendix D.")
h3("4. Notification and ticketing (informational only)")
bullet("Slack, webhooks, and Amazon SNS route alerts to the organization's existing SOC workflow. As "
       "scoped, these channels are for notification. No automated remediation or write-back actions "
       "are configured.")

# ---------------------------------------------------------------- Roadmap
h1("Phased Deployment Roadmap", newpage=True)
para("We recommend a time-boxed, three-phase rollout. Each phase is scoped to minimize risk and "
     "validate results before moving to the next.")
h2("Phase 1: Log Source Onboarding & Ingestion")
bullet("Onboard AWS CloudTrail, VPC Flow Logs, WAF, Config, Route 53, and Network Firewall via the "
       "CloudFormation onboarding template.")
bullet("Connect GCP audit/activity logs and OCI audit logs through their native log-export services.")
bullet("Connect Google Workspace, MongoDB, Slack, Jamf, CrowdStrike FDR, and AquaSec via their "
       "respective APIs.")
bullet("Deploy the Syslog VM middleware and onboard Cisco Meraki and Palo Alto firewall logs.")
bullet("Validate ingestion rates and confirm 1-year retention with the 6-month searchable window is "
       "indexing correctly.")
h2("Phase 2: Threat Detection & Threat Intelligence")
bullet("Enable out-of-the-box detection rules for AWS CloudTrail, GCP, and Kubernetes.")
bullet("Author and tune custom detectors for CrowdStrike, AquaSec, MongoDB, Google Workspace, Meraki, "
       "and Palo Alto log patterns.")
bullet("Enable threat-intelligence enrichment (AlienVault and others) and MITRE ATT&CK mapping.")
bullet("Configure anomaly-detection baselines and multivector correlations across identity, cloud, "
       "and network sources.")
bullet("Push detection alerts into AccuKnox CNAPP for a unified findings view, where applicable.")
h2("Phase 3: Dashboards, Alerting & Compliance Reporting")
bullet("Build organization-specific dashboards: SOC overview, per-source detections, MITRE heatmap, "
       "and compliance widgets.")
bullet("Configure alerting to Slack, Jira, ServiceNow, or email with tuned thresholds and "
       "de-duplication.")
bullet("Enable scheduled audit log exports (JSON/CSV) for compliance reviews and validate retention "
       "exports end to end.")

# ---------------------------------------------------------------- Compliance
h1("Security, Compliance & Auditability", newpage=True)
para("AccuKnox SIEM's retention, search, and export model is built to support standard audit and "
     "compliance workflows. The platform's design aligns with:")
bullet([("ISO/IEC 27001: ", True), ("information security management", False)])
bullet([("SOC 2: ", True), ("security, availability, and confidentiality trust principles", False)])
bullet([("PCI DSS: ", True), ("logging and monitoring requirements for cardholder data environments",
                              False)])
bullet([("GDPR: ", True), ("data protection and audit-trail requirements", False)])
bullet([("NIST SP 800-207: ", True), ("Zero Trust architecture principles", False)])
para("For the organization's specific compliance program, we recommend confirming applicable "
     "frameworks during the POC so dashboards and audit-export formats can be tuned accordingly from "
     "day one.", space_before=6)

# ---------------------------------------------------------------- Business Impact
h1("Business Impact")
bullet([("Tool consolidation: ", True),
        ("replace fragmented log tooling across AWS, GCP, OCI, SaaS, and network appliances with a "
         "single cloud-native SIEM. One platform, one retention policy, one search experience.",
         False)])
bullet([("Reduced infrastructure overhead: ", True),
        ("cloud-native ingestion pipelines scale to 100K events/sec and 1TB/day per tenant without "
         "forwarder farms or heavy on-prem infrastructure. The syslog VM is the only piece of "
         "infrastructure the organization needs to run.", False)])
bullet([("Operational efficiency: ", True),
        ("correlation and MITRE-aligned prioritization reduce alert noise, cutting the time SOC "
         "analysts spend triaging low-value alerts.", False)])
bullet([("Faster investigations: ", True),
        ("metadata-based indexing keeps 6-month search fast, so audits and incident investigations "
         "don't wait on raw log scans.", False)])
bullet([("Audit and retention cost reduction: ", True),
        ("1-year retention with a 6-month searchable window and one-click audit log exports cut "
         "audit-preparation time.", False)])
bullet([("Scalable for growth: ", True),
        ("per-tenant RBAC, dashboards, and ingestion controls scale cleanly as the organization adds "
         "business units, environments, or geographies.", False)])

# ---------------------------------------------------------------- Support
h1("Support & Service-Level Commitment")
bullet("24/7 product support, per the agreed commercial terms.")
bullet("A dedicated Technical Account Manager (TAM).")
bullet("Quarterly health checks and improvement recommendations.")

# ---------------------------------------------------------------- Summary
h1("Proposal Summary")
para("AccuKnox SIEM meets the organization's requirements across all fifteen log sources identified "
     "during discovery, with a retention and search model built specifically around the 1-year / "
     "6-month compliance requirement.")
bullet([("Log ingestion & search: ", True),
        ("AWS (CloudTrail, VPC, WAF, Config, Route 53, Network Firewall), GCP, OCI, Google Workspace, "
         "MongoDB, Slack, Jamf, Cisco Meraki, CrowdStrike FDR, AquaSec, and Palo Alto, ingested at "
         "scale (100K events/sec, 1TB/day/tenant).", False)])
bullet([("Threat detection & MITRE ATT&CK: ", True),
        ("out-of-the-box AWS CloudTrail detection rules plus custom detectors for the organization's "
         "stack, enriched with threat intelligence.", False)])
bullet([("Retention & search: ", True),
        ("1-year retention, 6-month searchable window, metadata-based indexing, and on-demand audit "
         "log export.", False)])
bullet([("Native CNAPP hand-off & multi-tenancy: ", True),
        ("SIEM alerts feed AccuKnox CNAPP's asset/findings views; per-tenant RBAC and dashboards for "
         "the organization's teams and business units.", False)])
para("We would be glad to run a structured POC with the organization to validate ingestion, "
     "detection, and retention against real data before a full commercial rollout. See Appendix C for "
     "the proposed timeline.", space_before=6)

# ---------------------------------------------------------------- Appendix A
h1("Appendix A: AccuKnox Multi-tenancy & Scalability", newpage=True)
para("AccuKnox is built on a multi-tenant architecture from the ground up, which is what allows the "
     "organization's environment to scale horizontally without a dedicated control plane per business "
     "unit.")
h2("Isolation model")
bullet([("Hard isolation: ", True),
        ("a dedicated instance of the app and database per customer. Strong isolation, higher "
         "operational cost.", False)])
bullet([("Soft isolation: ", True),
        ("customers share a database, but each has its own set of tables, a balance of isolation and "
         "cost. This is the default for most deployments.", False)])
h2("Layered architecture")
bullet([("Layer 1: ", True), ("Users, RBAC, and tenants.", False)])
bullet([("Layer 2: ", True), ("Backend jobs and execution management.", False)])
bullet([("Layer 3: ", True), ("Data isolation between tenants.", False)])
bullet([("Layer 4: ", True), ("Custom reporting, dashboards, and layouts per tenant.", False)])
para("A single user can belong to multiple tenants with different permissions in each, useful if, for "
     "example, a security team needs read access across two regional business units while engineering "
     "teams stay segregated.", space_before=6)
figure("p17_x57.png", "Figure 7. A user can hold different RBAC roles across multiple tenants.",
       width=5.8)
figure("p16_x53.png",
       "Figure 8. Regional tenant separation with shared or segregated team access.", width=3.3)
h2("Resource allocation and the noisy-neighbor problem")
para("AccuKnox uses a hybrid allocation model: customers requiring hard isolation get a dedicated "
     "control plane, while multiple small or mid-size tenants share compute through Kubernetes-native "
     "soft isolation. To prevent one tenant's workload from starving another's, the classic “noisy "
     "neighbor” problem, AccuKnox uses Kueue for cluster-wide job scheduling and isolated, "
     "namespace-based replica sets for parser tasks.")
h2("Data isolation")
para("Tenant data is isolated at the storage layer without spinning up a separate database instance "
     "per customer: each tenant gets its own PostgreSQL tables, and its own MongoDB collections, each "
     "with independent access control, which keeps the blast radius contained if one tenant's access "
     "is compromised.")
figure("p18_x60.png", "Figure 9. Per-tenant data isolation at the storage layer.", width=3.1)
h2("Deployment models")
bullet("SaaS")
bullet("Customer cloud (AccuKnox control plane deployed in the customer's AWS/Azure/GCP)")
bullet("On-premises / air-gapped")
para("The same multi-tenancy architecture applies across all three models, and AccuKnox's control "
     "plane is already battle-tested at MSSP scale. One OEM partner alone onboards hundreds of "
     "tenants on a shared control plane.", space_before=6)

# ---------------------------------------------------------------- Appendix B
h1("Appendix B: Integration Ecosystem", newpage=True)
para("AccuKnox integrates with 80+ ecosystem tools and frameworks across cloud, SIEM, CI/CD, and "
     "container platforms. The organization's committed scope is the fifteen sources in the Scope of "
     "Work section; the categories below show the broader AccuKnox SIEM integration catalog available "
     "if the organization's needs expand. The latest full list is available at "
     "accuknox.com/integrations.")
h2("AccuKnox SIEM integration categories")
bullet([("Identity: ", True), ("AD/LDAP, Okta, Microsoft O365, GitHub, and AccuKnox CNAPP cloud "
                               "findings.", False)])
bullet([("Firewalls & network appliances: ", True),
        ("FortiGate, Palo Alto, and any syslog-capable firewall; routers and managed switches.",
         False)])
bullet([("Cloud service providers: ", True), ("AWS CloudTrail, Azure Logs, GCP Logs.", False)])
bullet([("Endpoints: ", True), ("Syslog, KubeArmor, Microsoft Defender, Microsoft Windows.", False)])
bullet([("Kubernetes: ", True), ("KubeArmor and Kubernetes API server logs.", False)])
figure("p19_x63.png", "Figure 10. AccuKnox platform integration ecosystem.", width=5.0)

# ---------------------------------------------------------------- Appendix C
h1("Appendix C: POC Timeline & Checklist", newpage=True)
para("The proposed POC validates AccuKnox SIEM against the organization's fifteen log sources and its "
     "1-year / 6-month retention requirement in a structured, milestone-driven approach. SIEM "
     "ingestion and detection only, with no automated remediation actions in scope.")
h2("Checklist")
table(["Checklist Item", "Validation Criteria"], [
    ["Log Ingestion", "Validate ingestion from AWS, GCP, OCI, all SaaS/API sources, and the Syslog VM "
                      "middleware for Meraki and Palo Alto."],
    ["Threat Detection", "Confirm out-of-the-box and custom detectors trigger correctly against "
                         "sample and live events."],
    ["Threat Intelligence", "Validate IP/domain reputation enrichment against known indicators."],
    ["Dashboards", "Build and validate a sample custom dashboard and saved search."],
    ["Alerting", "Validate notification delivery to Slack, email, and/or Jira."],
    ["Retention & Search", "Confirm 1-year retention configuration, 6-month searchable window, and "
                           "audit log export in JSON/CSV."],
    ["RBAC & Multi-tenancy", "Validate tenant isolation and role-based access for the organization's "
                             "teams."],
], [1.8, 4.7])
tl = h2("Timeline")
tl.paragraph_format.page_break_before = True
tl.paragraph_format.space_before = Pt(0)
table(["Phase", "Activities", "Duration"], [
    ["Phase 1", "Log source onboarding across AWS, GCP, OCI, and SaaS/API sources, plus Syslog VM "
                "setup for Meraki and Palo Alto.", "2 business days"],
    ["Phase 2", "Threat detection and threat-intelligence validation across onboarded sources.",
     "1 business day"],
    ["Phase 3", "Dashboards, alerting, and audit log export validation.", "1 business day"],
    ["Wrap-up", "End-to-end validation, fine-tuning, knowledge transfer, and next-steps planning.",
     "1 business day"],
], [0.9, 4.3, 1.3])

# ---------------------------------------------------------------- Appendix D
h1("Appendix D: Syslog Integration Approach for Firewalls", newpage=True)
para("AccuKnox SIEM does not parse the Syslog protocol directly. For the organization's Palo Alto "
     "Firewall and Cisco Meraki sources, both of which emit Syslog, AccuKnox uses a lightweight "
     "middleware VM to convert Syslog to JSON before ingestion.")
h2("Approach")
p = para("", space_after=10)
style_run(p.add_run("Source device (Syslog)  →  Syslog VM (Rsyslog + JSON conversion script)  "
                    "→  AccuKnox SIEM (JSON ingestion via Bulk API)"),
          size=10.5, bold=True, color=PRIMARY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
shade(p._p.get_or_add_pPr(), GREY_FILL)
p.paragraph_format.space_before = Pt(8)

h2("Step by step")
bullet([("1. Source configuration: ", True),
        ("point the Palo Alto Firewall and Cisco Meraki dashboard to forward Syslog to the Syslog "
         "VM's IP and port (default UDP/TCP 514).", False)])
bullet([("2. Syslog VM setup: ", True),
        ("deploy an Ubuntu VM in the same network segment or VPC as the source devices, and install "
         "Rsyslog to receive messages from both sources.", False)])
bullet([("3. JSON conversion: ", True),
        ("a script on the Syslog VM parses each incoming line and converts it to a JSON object "
         "(source IP, timestamp, event type, message body, device name).", False)])
bullet([("4. Forward to AccuKnox SIEM: ", True),
        ("the JSON payload is sent to AccuKnox SIEM's ingestion endpoint via Bulk API or LogStash "
         "HTTP output.", False)])
bullet([("5. Indexing & detection: ", True),
        ("AccuKnox SIEM indexes events under the organization's tenant namespace and applies "
         "detection rules: port-scan and policy-violation detectors for Palo Alto, "
         "client-association and unauthorized-SSID detectors for Meraki.", False)])
para("The Syslog VM is a small piece of onboarding infrastructure that lives in the organization's "
     "environment. AccuKnox does not require inbound access to the organization's network to operate "
     "it.", size=9.5, italic=True, color="5A6478", space_before=8)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print("wrote", OUT)
