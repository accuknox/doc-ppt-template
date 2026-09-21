"""Build the CertifyOS AccuKnox vs Snyk technical proposal and battlecard.

Six A4 pages. A navy cover, three content pages, one battlecard datapoints
page for review, and a closing page with a four-image gallery and the
references.

Sources, both opened:
  "CertifyOS Technical Proposal.docx"  Google Drive 16qAUBBRwcDThpgKYtTG5QI69nQmi-9yI
  "AccuKnox_vs_Snyk.xlsx"              Google Drive 1ZuF1D9myjUdkUrXldGCmvOaS2sEQ7dyP

The four gallery images are lifted from the CertifyOS proposal itself.
Every AccuKnox claim links to help.accuknox.com and every Snyk claim links
to a page Snyk published. All links returned HTTP 200 on 2026-09-08.

Emits HTML with images inlined as data URIs, then prints to PDF with
headless Edge.
"""
import base64
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(REPO, "output", "certifyos")
OUT = os.path.join(REPO, "output")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FILE = "AccuKnox_vs_Snyk_CertifyOS_Proposal_and_Battlecard"

NAVY = "#11206D"
BLUE = "#0046FF"
SEC = "#6464FF"
RED = "#C80019"
GREEN = "#16A55C"
MUTE = "#6A749A"
INK = "#1A1D2E"
GREY_BG = "#EEF0F6"
GREY_BD = "#C4CCDE"


def uri(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


LOGO_DARK = uri(os.path.join(REPO, "assets", "logos", "accuknox-logo-dark-bg.png"))
LOGO_LIGHT = uri(os.path.join(REPO, "assets", "logos", "accuknox-logo-light-bg.png"))
EMBLEM = uri(os.path.join(REPO, "assets", "logos", "accuknox-emblem.png"))

G1 = uri(os.path.join(WORK, "g1-aspm.png"))
G2 = uri(os.path.join(WORK, "g2-runtime.png"))
G3 = uri(os.path.join(WORK, "g3-apisec.png"))
G4 = uri(os.path.join(WORK, "g4-modules.png"))


# --------------------------------------------------------------------------
# links, every one checked for HTTP 200 on 2026-09-08
# --------------------------------------------------------------------------
H = {
    "aspm": "https://help.accuknox.com/use-cases/aspm/",
    "vuln": "https://help.accuknox.com/use-cases/vulnerability/",
    "epss": "https://help.accuknox.com/use-cases/epss-scoring/",
    "rules": "https://help.accuknox.com/use-cases/rules-engine-ticket-creation/",
    "reports": "https://help.accuknox.com/use-cases/aspm-reports/",
    "dast": "https://help.accuknox.com/how-to/dast-scan-types/",
    "dast_auth": "https://help.accuknox.com/how-to/dast-authenticated-scans/",
    "mfa": "https://help.accuknox.com/use-cases/mfa-dast/",
    "iac": "https://help.accuknox.com/use-cases/iac-scan/",
    "container": "https://help.accuknox.com/use-cases/container-scan/",
    "registry": "https://help.accuknox.com/how-to/registry-overview/",
    "xbom": "https://help.accuknox.com/getting-started/xbom-setup/",
    "xbom_cli": "https://help.accuknox.com/getting-started/xbom-knoxctl/",
    "ide": "https://help.accuknox.com/integrations/vscode-code-security/",
    "api": "https://help.accuknox.com/use-cases/api-security/",
    "cwpp": "https://help.accuknox.com/use-cases/cwpp/",
    "hardening": "https://help.accuknox.com/use-cases/app-hardening/",
    "zt": "https://help.accuknox.com/use-cases/zero-trust/",
    "kspm": "https://help.accuknox.com/use-cases/kspm/",
    "kiem": "https://help.accuknox.com/use-cases/kiem/",
    "cspm": "https://help.accuknox.com/use-cases/cspm/",
    "compliance": "https://help.accuknox.com/use-cases/compliance/",
    "firewall": "https://help.accuknox.com/use-cases/prompt-firewall-overview/",
    "redteam": "https://help.accuknox.com/use-cases/red-teaming/",
    "shadow": "https://help.accuknox.com/use-cases/shadow-ai-discovery/",
    "onprem": "https://help.accuknox.com/how-to/aiml-saas-vs-onprem/",
}

S = {
    "docs": "https://docs.snyk.io/",
    "code": "https://docs.snyk.io/scan-with-snyk/snyk-code",
    "oss": "https://docs.snyk.io/scan-with-snyk/snyk-open-source",
    "container": "https://docs.snyk.io/scan-with-snyk/snyk-container",
    "iac": "https://docs.snyk.io/scan-with-snyk/snyk-iac",
    "apprisk": "https://docs.snyk.io/manage-risk/snyk-apprisk",
    "broker": "https://docs.snyk.io/enterprise-setup/snyk-broker",
    "hosting": "https://docs.snyk.io/working-with-snyk/regional-hosting-and-data-residency",
    "api": "https://docs.snyk.io/snyk-api",
    "product": "https://snyk.io/product/",
    "plans": "https://snyk.io/plans/",
}


# --------------------------------------------------------------------------
# page 2, the replacement map
# --------------------------------------------------------------------------
SWAP = [
    ("Snyk Code", S["code"],
     "ASPM SAST",
     "Java, Python, .NET, C++, JS and TS, Go, Kotlin, Swift, PHP, Ruby, "
     "Scala, Apex and Dart. Engine results normalise into one findings "
     "model.",
     [("ASPM overview", H["aspm"])]),
    ("Snyk Open Source", S["oss"],
     "SCA and SBOM",
     "Direct and transitive dependency graph, license class policy, and SBOM "
     "export in SPDX 2.3 and CycloneDX.",
     [("xBOM setup", H["xbom"])]),
    ("Snyk Container", S["container"],
     "Container and registry scan",
     "Docker Hub, ECR, GCR, ACR, JFrog Artifactory, Harbor, Quay and Nexus, "
     "on a CRON schedule with tag-pattern filters.",
     [("Container scan", H["container"]), ("Registry", H["registry"])]),
    ("Snyk IaC", S["iac"],
     "IaC scan",
     "Terraform, Helm and Kubernetes manifests, gated at pull request and in "
     "the pipeline.",
     [("IaC scan", H["iac"])]),
    ("Snyk AppRisk", S["apprisk"],
     "Unified findings and prioritisation",
     "One findings page across SAST, DAST, SCA, IaC, secrets and API, ranked "
     "by CVSS, EPSS and CISA KEV.",
     [("Findings", H["vuln"]), ("EPSS scoring", H["epss"])]),
    ("Snyk IDE plugins", S["product"],
     "IDE extension",
     "VS Code, Cursor and IntelliJ, with scan on save, AI remediation and a "
     "diff preview before the fix lands.",
     [("IDE extension", H["ide"])]),
    ("Snyk Jira integration", S["docs"],
     "Rule Engine ticketing",
     "Jira Cloud and ServiceNow, with severity-to-priority mapping and "
     "condition-based auto-ticketing.",
     [("Rule Engine", H["rules"])]),
]


# --------------------------------------------------------------------------
# page 3, the four gaps and the one honest row
# --------------------------------------------------------------------------
GAPS = [
    ("Runtime enforcement", "4 of 4 rows absent",
     "KubeArmor applies eBPF and Linux Security Module policy in the kernel. "
     "A policy in block mode denies the process, the file access or the "
     "network call before it runs. Snyk documents build-time and "
     "pre-deployment scanning, and publishes no runtime enforcement engine.",
     [("CWPP", H["cwpp"]), ("App hardening", H["hardening"]),
      ("Zero Trust", H["zt"])]),
    ("API security", "4 of 6 rows absent",
     "AccuKnox reads live API traffic to surface Shadow, Zombie and Orphan "
     "endpoints, flags PII and PHI in payloads and headers, and integrates "
     "with AWS API Gateway, Istio, Kong, F5 and NGINX. Snyk API testing works "
     "from an OpenAPI specification, so an undocumented endpoint stays "
     "invisible.",
     [("API security", H["api"])]),
    ("xBOM beyond software", "1 of 4 rows absent",
     "AccuKnox generates SBOM, HBOM, CBOM for post-quantum readiness, QBOM "
     "and AI-BOM from one command. Snyk documents software SBOM export in "
     "CycloneDX and SPDX and no hardware, cryptographic or AI bill of "
     "materials.",
     [("xBOM setup", H["xbom"]), ("knoxctl xBOM", H["xbom_cli"])]),
    ("Air-gapped deployment", "1 of 3 rows absent",
     "AccuKnox runs full on-premises and air-gapped, with a customer-"
     "controlled vulnerability database update pipeline. Snyk Broker reaches "
     "a network-restricted registry, and the platform itself stays SaaS with "
     "regional hosting options.",
     [("SaaS and on-prem", H["onprem"])]),
]

LEADS = [
    ("IDE breadth", "Snyk ships VS Code, JetBrains, Eclipse and Visual "
     "Studio plugins. AccuKnox covers VS Code, Cursor and IntelliJ. A team "
     "standardised on Eclipse or Visual Studio loses inline feedback on day "
     "one."),
    ("Dependency upgrade paths", "Snyk Open Source raises the fix pull "
     "request with the upgrade path already worked out. Score this in the "
     "proof of concept against your own repositories."),
    ("Vulnerability research", "Snyk Intel is maintained by an in-house "
     "research team alongside NVD. Treat depth of intelligence as a row "
     "CertifyOS tests rather than a row this document settles."),
]


# --------------------------------------------------------------------------
# page 4, rollout
# --------------------------------------------------------------------------
PHASES = [
    ("1", "Weeks 1 and 2", "Discovery and architecture",
     "Repository inventory, Snyk organisation export, deployment model, RBAC "
     "and single sign-on design, and agreed exit criteria."),
    ("2", "Weeks 2 and 3", "Parity in the pipeline",
     "SAST, SCA, secrets, IaC and container scans wired into the same CI "
     "jobs Snyk runs in today, with soft-fail gates."),
    ("3", "Weeks 3 to 5", "Parallel run and finding reconciliation",
     "Both platforms scan the same repositories. Compare finding counts, "
     "false positives and fix guidance before any cutover."),
    ("4", "Weeks 4 to 6", "Coverage Snyk did not carry",
     "DAST with MFA and TOTP handling, API discovery from live traffic, "
     "registry scheduling, and KubeArmor in audit mode."),
    ("5", "Weeks 5 to 7", "Enforcement and evidence",
     "Move stable KubeArmor policies into block mode. Turn on Rule Engine "
     "ticketing, compliance mapping and evidence export."),
    ("6", "Weeks 6 to 8", "AI security and cutover",
     "Shadow AI discovery, red teaming and Prompt Firewall. Retire the Snyk "
     "licence once the exit criteria from phase 1 are met."),
]

EXIT = [
    "Every repository Snyk scans today produces an AccuKnox finding set, "
    "reconciled row by row.",
    "Pipeline build time stays inside the budget CertifyOS runs on Snyk "
    "today.",
    "Developers see findings in the IDE and in the pull request, not only in "
    "a console.",
    "At least one KubeArmor policy runs in block mode on a production "
    "namespace.",
]


# --------------------------------------------------------------------------
# page 5, battlecard datapoints
# --------------------------------------------------------------------------
DOMAINS = [
    ("ASPM core platform", 5, 3, 2, 0),
    ("SAST", 5, 4, 0, 1),
    ("DAST", 4, 0, 4, 0),
    ("SCA and SBOM", 5, 5, 0, 0),
    ("Container and registry", 4, 3, 1, 0),
    ("API security", 6, 0, 2, 4),
    ("CWPP and runtime", 4, 0, 0, 4),
    ("Compliance and reporting", 3, 1, 2, 0),
    ("Deployment models", 3, 1, 1, 1),
    ("Integration methods and xBOM", 4, 2, 1, 1),
    ("Unified findings page", 4, 2, 2, 0),
    ("Integrations", 4, 3, 1, 0),
    ("CSPM", 7, 4, 1, 2),
    ("KSPM", 7, 5, 0, 2),
    ("AI-SPM", 10, 6, 3, 1),
]

FACTS = [
    ("75", "rows compared", "Across 15 capability domains in the AccuKnox "
     "and Snyk research sheet."),
    ("16", "rows Snyk does not cover", "Concentrated in runtime, API "
     "security, air-gapped deployment and xBOM."),
    ("20", "rows scored partial", "DAST accounts for 4 of them, all four "
     "DAST rows in the sheet."),
    ("8", "container registries", "Docker Hub, ECR, GCR, ACR, JFrog, Harbor, "
     "Quay and Nexus, on a CRON schedule."),
    ("35+", "compliance frameworks", "PCI DSS, ISO 27001, SOC 2, HIPAA, "
     "NIST, DISA STIG and more, with evidence export."),
    ("5", "bill of materials types", "SBOM, HBOM, CBOM, QBOM and AI-BOM from "
     "one command."),
]

OBJECTIONS = [
    ("Our developers already live in Snyk",
     "Keep them there during the parallel run in phase 3. AccuKnox ships a "
     "VS Code, Cursor and IntelliJ extension with scan on save and a diff "
     "preview. Confirm Eclipse and Visual Studio needs before you commit."),
    ("Snyk fix pull requests save us time",
     "That is a real Snyk strength and it belongs in the proof of concept. "
     "Score it against AccuKnox AI remediation on your own repositories "
     "rather than on a slide."),
    ("Why change a tool that works",
     "Snyk stops at the artifact. CertifyOS handles PHI, so the same finding "
     "has to reach runtime enforcement, API traffic and audit evidence. "
     "Those are 16 rows Snyk leaves open."),
]


# --------------------------------------------------------------------------
# page 6, the gallery
# --------------------------------------------------------------------------
GALLERY = [
    (G1, "Shift-left coverage across the DevOps loop",
     "SAST, SCA and IaC on the development side, DAST and IAST on the "
     "operations side. This is the surface that replaces Snyk one for one.",
     "Diagram of the DEV and OPS loop with SAST, SCA, IaC, DAST and IAST "
     "attached to the stages each one scans."),
    (G2, "Enforcement happens in kernel space, not in a report",
     "An eBPF sensor and an LSM enforcer sit below user space, so a policy "
     "denies the call. Snyk publishes no runtime enforcement engine.",
     "Layer diagram with the AccuKnox control plane above user space, and an "
     "eBPF sensor and LSM enforcer in kernel space over Kubernetes, VMs and "
     "containers."),
    (G3, "API security starts from traffic, not from a specification",
     "Shadow, Zombie and Orphan endpoints, PII and PHI in headers, and rate "
     "limiting. Four of the six API rows are absent on the Snyk side.",
     "Panel of API security problems including Shadow, Zombie and Orphan "
     "APIs, sensitive data in headers and compliance mappings."),
    (G4, "Twelve modules on one control plane",
     "The consolidation argument in one picture. Snyk covers the "
     "application security slice of this map.",
     "Radial diagram of twelve AccuKnox security offerings around a central "
     "badge, each with the problem it solves."),
]


# --------------------------------------------------------------------------
# markup helpers
# --------------------------------------------------------------------------
def mark(state, size="3.9mm"):
    if state == "y":
        body = ('<circle cx="8" cy="8" r="8" fill="%s"/>'
                '<path d="M4.3 8.2 6.8 10.7 11.8 5.4" stroke="#fff" '
                'stroke-width="2" fill="none" stroke-linecap="round" '
                'stroke-linejoin="round"/>' % GREEN)
    elif state == "n":
        body = ('<circle cx="8" cy="8" r="8" fill="%s"/>'
                '<path d="M5.3 5.3 10.7 10.7 M10.7 5.3 5.3 10.7" stroke="#fff" '
                'stroke-width="2" fill="none" stroke-linecap="round"/>' % RED)
    else:
        body = ('<circle cx="8" cy="8" r="8" fill="%s"/>'
                '<path d="M4.9 8 11.1 8" stroke="#fff" stroke-width="2" '
                'fill="none" stroke-linecap="round"/>' % MUTE)
    return ('<svg class="mk" style="width:%s;height:%s" viewBox="0 0 16 16">%s'
            '</svg>' % (size, size, body))


def links(pairs):
    return " &nbsp;·&nbsp; ".join('<a href="%s">%s</a>' % (u, t)
                                  for t, u in pairs)


def head(label):
    return ('<div class="head"><img src="%s" alt="AccuKnox">'
            '<span>CERTIFYOS &nbsp;·&nbsp; ACCUKNOX VS SNYK &nbsp;·&nbsp; %s'
            '</span></div>' % (LOGO_LIGHT, label))


LEGEND = ('<div class="legend">%s<span>Full capability</span>%s'
          '<span>Partial</span>%s<span>Not available</span></div>'
          % (mark("y", "3.3mm"), mark("p", "3.3mm"), mark("n", "3.3mm")))


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { font-family: 'Space Grotesk', 'Inter', 'Segoe UI', sans-serif;
  color: INK; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: BLUE; text-decoration: none; }

.page { position: relative; width: 210mm; height: 297mm; overflow: hidden;
  page-break-after: always; background: #fff; }
.page:last-child { page-break-after: auto; }

.dark { color: #fff; background: #0B1240; }
.p1 { position: relative; padding: 28mm 20mm 14mm; height: 100%; }
.p1 .logo { height: 9.6mm; }
.eyebrow { margin-top: 50mm; font-size: 8.4pt; letter-spacing: 3px;
  font-weight: 700; color: #A9BEFF; }
.rule { height: 3px; width: 48mm; border-radius: 3px; margin: 5mm 0 7mm;
  background: RED; }
h1 { font-size: 38pt; line-height: 1.08; font-weight: 700; letter-spacing: -1px;
  color: #fff; }
h1 .vs { color: #A9BEFF; font-weight: 500; }
.subtitle { margin-top: 7mm; font-size: 13pt; font-weight: 500; color: #fff; }
.scope { margin-top: 4mm; font-size: 10.4pt; line-height: 1.6; color: #CBD7FA;
  max-width: 152mm; }
.nums { display: flex; gap: 12mm; margin-top: 11mm; }
.nums .n { font-size: 24pt; font-weight: 700; color: #fff; }
.nums .l { margin-top: 1.4mm; font-size: 8pt; color: #A9BEFF;
  letter-spacing: .6px; }
.p1foot { position: absolute; left: 20mm; right: 20mm; bottom: 14mm;
  font-size: 8pt; color: #A9BEFF; display: flex;
  justify-content: space-between; border-top: 1px solid rgba(169,190,255,.3);
  padding-top: 4mm; }

.p { padding: 12mm 13mm 14mm; height: 100%; position: relative; }
.head { display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1.6px solid GREY_BD; padding-bottom: 3mm; margin-bottom: 5mm; }
.head img { height: 6mm; }
.head span { font-size: 6.8pt; color: MUTE; letter-spacing: .7px; }
h2 { font-size: 17pt; font-weight: 700; color: NAVY; letter-spacing: -.5px;
  line-height: 1.18; }
h2 .accent { color: BLUE; }
.h2sub { margin-top: 2.2mm; font-size: 9pt; line-height: 1.52; color: #3A4064; }

.verdict { margin-top: 5mm; border-radius: 3mm; padding: 4.4mm 5.4mm;
  background: GREY_BG; border-left: 3.4px solid RED; }
.verdict .k { font-size: 7.4pt; letter-spacing: 1.8px; font-weight: 700;
  color: RED; }
.verdict p { margin-top: 2.4mm; font-size: 9.4pt; line-height: 1.58;
  color: #23283F; }

.legend { display: flex; align-items: center; gap: 2mm; margin: 4mm 0 3mm;
  font-size: 7.4pt; color: MUTE; }
.legend span { margin-right: 4.5mm; }
.mk { vertical-align: -.6mm; flex: none; }

table.sw { width: 100%; border-collapse: collapse; table-layout: fixed;
  margin-top: 4mm; }
table.sw th { text-align: left; padding: 3.4mm 4mm; background: NAVY;
  color: #fff; font-size: 8.2pt; font-weight: 700; }
table.sw th.a { font-size: 7.4pt; letter-spacing: 1.1px;
  text-transform: uppercase; color: #B9C6EE; }
table.sw td { padding: 3.6mm 4mm; vertical-align: top; border: 1px solid GREY_BD;
  border-top: none; font-size: 8.4pt; line-height: 1.45; color: #23283F; }
table.sw td.f { background: GREY_BG; border-left: 2.6px solid MUTE;
  font-weight: 700; color: NAVY; font-size: 8.6pt; }
table.sw td.f a { font-size: 6.8pt; font-weight: 400; display: block;
  margin-top: 1.4mm; color: MUTE; }
table.sw td.t { background: #F7F9FF; font-weight: 700; color: NAVY;
  font-size: 8.6pt; }
table.sw td .rf { display: block; margin-top: 2mm; font-size: 6.9pt;
  color: MUTE; }

.gap { margin-top: 4mm; border: 1px solid GREY_BD; border-left: 3.2px solid RED;
  border-radius: 2.6mm; padding: 4mm 5mm 4.4mm; }
.gap .t { display: flex; align-items: baseline; gap: 3mm; }
.gap h3 { font-size: 10.6pt; font-weight: 700; color: NAVY; }
.gap .cnt { font-size: 6.8pt; font-weight: 700; letter-spacing: 1.1px;
  color: #fff; background: RED; padding: 1.2mm 2.4mm; border-radius: 1.6mm;
  text-transform: uppercase; }
.gap p { margin-top: 2.4mm; font-size: 8.6pt; line-height: 1.52; color: #2B3150; }
.gap .rf { margin-top: 2.4mm; font-size: 6.9pt; color: MUTE; }

.leads { margin-top: 5mm; border-radius: 3mm; padding: 4.4mm 5.4mm;
  background: #F4F6FE; border: 1px solid #D5DDF5; border-left: 3.4px solid SEC; }
.leads h3 { font-size: 10pt; font-weight: 700; color: NAVY; }
.leads .r { margin-top: 2.8mm; display: flex; gap: 3.4mm; }
.leads .r b { flex: none; width: 40mm; font-size: 8.2pt; color: NAVY; }
.leads .r span { font-size: 8.2pt; line-height: 1.5; color: #2B3150; }

table.ph { width: 100%; border-collapse: collapse; table-layout: fixed;
  margin-top: 4mm; }
table.ph th { text-align: left; padding: 3.2mm 4mm; background: NAVY;
  color: #fff; font-size: 7.6pt; font-weight: 700; letter-spacing: 1px;
  text-transform: uppercase; }
table.ph td { padding: 3.6mm 4mm; vertical-align: top; border: 1px solid GREY_BD;
  border-top: none; font-size: 8.4pt; line-height: 1.45; color: #23283F; }
table.ph td.w { background: GREY_BG; font-weight: 700; color: NAVY;
  font-size: 8.2pt; border-left: 2.6px solid BLUE; }
table.ph td.n { background: #F7F9FF; font-weight: 700; color: NAVY; }

.exit { margin-top: 5mm; border-radius: 3mm; padding: 4.4mm 5.4mm;
  background: GREY_BG; border: 1px solid GREY_BD; }
.exit h4 { font-size: 7.4pt; letter-spacing: 1.6px; font-weight: 700;
  color: NAVY; }
.exit ol { margin-top: 2.8mm; padding-left: 4.8mm; }
.exit li { font-size: 8.4pt; line-height: 1.5; color: #2B3150;
  margin-bottom: 1.8mm; }
.exit li:last-child { margin-bottom: 0; }

.bcols { display: flex; gap: 6mm; margin-top: 4mm; }
table.dm { width: 100%; border-collapse: collapse; }
table.dm th { font-size: 7pt; color: #fff; background: NAVY;
  text-align: left; padding: 2.2mm 3mm; font-weight: 700; }
table.dm th.c { text-align: center; width: 11mm; }
table.dm td { font-size: 7.6pt; color: #23283F; padding: 1.35mm 3mm;
  border: 1px solid GREY_BD; border-top: none; }
table.dm td.c { text-align: center; font-weight: 700; }
table.dm tbody tr:nth-child(odd) td { background: #F7F9FF; }
table.dm tfoot td { background: NAVY; color: #fff; font-weight: 700;
  border-color: NAVY; }

.facts { display: flex; flex-wrap: wrap; gap: 3mm; margin-top: 3.6mm; }
.facts .f { width: 55.3mm; border: 1px solid GREY_BD; border-radius: 2.4mm;
  padding: 2.4mm 3.2mm 2.6mm; border-top: 2.6px solid BLUE; }
.facts .f .n { font-size: 14pt; font-weight: 700; color: NAVY;
  line-height: 1; }
.facts .f .l { margin-top: 1.1mm; font-size: 6.9pt; font-weight: 700;
  letter-spacing: .6px; text-transform: uppercase; color: BLUE; }
.facts .f .d { margin-top: 1.4mm; font-size: 7pt; line-height: 1.38;
  color: #3A4064; }

.obj { margin-top: 4mm; }
.obj h4 { font-size: 7.2pt; letter-spacing: 1.6px; font-weight: 700;
  color: MUTE; padding-bottom: 2mm; border-bottom: 1.4px solid GREY_BD; }
.obj .r { margin-top: 2.4mm; display: flex; gap: 4mm; }
.obj .r b { flex: none; width: 46mm; font-size: 7.9pt; color: NAVY;
  line-height: 1.32; }
.obj .r span { font-size: 7.9pt; line-height: 1.45; color: #2B3150; }

.rev { margin-top: 4mm; border-radius: 3mm; padding: 3.2mm 5mm;
  background: #FFF6F7; border: 1px solid #F0CBD1; border-left: 3.4px solid RED; }
.rev b { font-size: 7.4pt; letter-spacing: 1.2px; color: RED; }
.rev p { margin-top: 1.8mm; font-size: 7.8pt; line-height: 1.45; color: #3A2B2E; }

.gal { display: flex; flex-wrap: wrap; gap: 4mm; margin-top: 4mm; }
.gal .c { width: 88mm; border: 1px solid GREY_BD; border-radius: 2.6mm;
  overflow: hidden; background: #fff; }
.gal .c .cap { padding: 2.8mm 3.4mm 3mm; border-top: 1px solid GREY_BD;
  background: #F7F9FF; }
.gal .c h4 { font-size: 8.4pt; font-weight: 700; color: NAVY;
  line-height: 1.3; }
.gal .c p { margin-top: 1.4mm; font-size: 7.2pt; line-height: 1.42;
  color: #3A4064; }
.gal .im { height: 36mm; display: flex; align-items: center;
  justify-content: center; padding: 2.6mm; }
.gal .im img { max-width: 100%; max-height: 100%; }

.reflist { margin-top: 5mm; }
.reflist h4 { font-size: 7.6pt; letter-spacing: 1.8px; font-weight: 700;
  color: MUTE; padding-bottom: 2.4mm; border-bottom: 1.4px solid GREY_BD; }
.reflist .dom { margin-top: 2mm; font-size: 6.8pt; color: MUTE; }
.reflist ol { margin-top: 2.4mm; list-style: none; column-count: 4;
  column-gap: 5mm; }
.reflist li { font-size: 7pt; line-height: 1.35; margin-bottom: 1.5mm;
  break-inside: avoid; }
.reflist li a { color: BLUE; }

.closer { position: absolute; left: 13mm; right: 13mm; bottom: 11mm;
  border-radius: 3.4mm; padding: 4.6mm 6mm; color: #fff;
  background: linear-gradient(120deg, NAVY 0%, #182B8C 60%, #0A0E33 100%);
  display: flex; align-items: center; justify-content: space-between; }
.closer .t { font-size: 11pt; font-weight: 700; }
.closer .s { margin-top: 1.6mm; font-size: 8.2pt; color: #B9C6EE; }
.closer img { height: 10mm; }
.pnum { position: absolute; right: 13mm; bottom: 5mm; font-size: 7.4pt;
  color: MUTE; }
"""
for _k, _v in (("INK", INK), ("NAVY", NAVY), ("BLUE", BLUE), ("SEC", SEC),
               ("RED", RED), ("GREEN", GREEN), ("MUTE", MUTE),
               ("GREY_BG", GREY_BG), ("GREY_BD", GREY_BD)):
    CSS = CSS.replace(_k, _v)


# --------------------------------------------------------------------------
def build_html():
    cover = """
<div class="page dark"><div class="p1">
  <img class="logo" src="{logo}" alt="AccuKnox">
  <div class="eyebrow">TECHNICAL PROPOSAL AND BATTLECARD &nbsp;·&nbsp; CERTIFYOS</div>
  <div class="rule"></div>
  <h1>AccuKnox <span class="vs">vs</span><br>Snyk</h1>
  <div class="subtitle">Replacing Snyk with one Zero Trust CNAPP control plane</div>
  <div class="scope">A like-for-like replacement map, the four capability areas
    Snyk leaves open, an eight-week rollout, and the battlecard datapoints
    behind every claim.</div>
  <div class="nums">
    <div><div class="n">75</div><div class="l">ROWS COMPARED</div></div>
    <div><div class="n">15</div><div class="l">CAPABILITY DOMAINS</div></div>
    <div><div class="n">16</div><div class="l">ROWS SNYK LEAVES OPEN</div></div>
  </div>
  <div class="p1foot"><span>AccuKnox &nbsp;·&nbsp; Zero Trust security for AI,
    API, Application, Cloud and Supply Chain</span><span>accuknox.com</span></div>
</div></div>
""".format(logo=LOGO_DARK)

    swap_rows = ""
    for them, tu, ours, detail, refs in SWAP:
        swap_rows += ('<tr><td class="f">%s<a href="%s">%s</a></td>'
                      '<td class="t">%s</td>'
                      '<td>%s<span class="rf">%s</span></td></tr>'
                      % (them, tu, tu.replace("https://", ""), ours, detail,
                         links(refs)))

    p2 = """
<div class="page"><div class="p">
  {head}
  <h2>Every Snyk product has a <span class="accent">named replacement</span></h2>
  <div class="h2sub">Seven Snyk products map to seven AccuKnox capabilities that
    are already generally available. Each AccuKnox row links to the
    documentation that proves it. Each Snyk row links to a page Snyk
    published.</div>

  <div class="verdict"><div class="k">WHERE IT LANDS</div>
    <p>Snyk covers static analysis, open source, container and infrastructure
    as code, and covers them well. Of 75 rows in the comparison sheet, Snyk is
    full on 39, partial on 20, and absent on 16. The 16 absent rows sit in
    runtime enforcement, API security, air-gapped deployment and xBOM. Those
    are the four areas CertifyOS needs for PHI workloads.</p></div>

  <table class="sw"><colgroup><col style="width:38mm"><col style="width:40mm">
    <col style="width:106mm"></colgroup>
    <thead><tr><th class="a">Snyk today</th><th class="a">AccuKnox module</th>
      <th class="a">What it does and where it is documented</th></tr></thead>
    <tbody>{rows}</tbody></table>
  <div class="pnum">2</div>
</div></div>
""".format(head=head("PAGE 2 OF 6"), rows=swap_rows)

    gaps_html = ""
    for title, cnt, body, refs in GAPS:
        gaps_html += ('<div class="gap"><div class="t"><h3>%s</h3>'
                      '<span class="cnt">%s</span></div><p>%s</p>'
                      '<div class="rf"><b>Reference</b> %s</div></div>'
                      % (title, cnt, body, links(refs)))

    leads_html = ""
    for t, b in LEADS:
        leads_html += '<div class="r"><b>%s</b><span>%s</span></div>' % (t, b)

    p3 = """
<div class="page"><div class="p">
  {head}
  <h2>Four areas decide the <span class="accent">replacement case</span></h2>
  <div class="h2sub">The row counts below come from the comparison sheet. Each
    one states what AccuKnox does first, then what Snyk documents.</div>
  {gaps}
  <div class="leads"><h3>Where Snyk leads, and what CertifyOS should test</h3>
    {leads}</div>
  <div class="pnum">3</div>
</div></div>
""".format(head=head("PAGE 3 OF 6"), gaps=gaps_html, leads=leads_html)

    ph_rows = ""
    for num, when, title, body in PHASES:
        ph_rows += ('<tr><td class="n">%s</td><td class="w">%s</td>'
                    '<td><b>%s.</b> %s</td></tr>' % (num, when, title, body))
    exit_items = "".join("<li>%s</li>" % e for e in EXIT)

    p4 = """
<div class="page"><div class="p">
  {head}
  <h2>Eight weeks, with a <span class="accent">parallel run</span> before cutover</h2>
  <div class="h2sub">Phases follow the CertifyOS technical proposal roadmap,
    narrowed to what a Snyk replacement needs. Phase 3 runs both platforms on
    the same repositories, so the decision rests on CertifyOS data.</div>

  <table class="ph"><colgroup><col style="width:12mm"><col style="width:30mm">
    <col style="width:142mm"></colgroup>
    <thead><tr><th>#</th><th>Timing</th><th>Phase and deliverables</th></tr></thead>
    <tbody>{rows}</tbody></table>

  <div class="exit"><h4>EXIT CRITERIA BEFORE THE SNYK LICENCE IS RETIRED</h4>
    <ol>{exit}</ol></div>

  <div class="leads"><h3>Why CertifyOS chooses AccuKnox over Snyk</h3>
    <div class="r"><b>Better</b><span>The same finding reaches runtime. A
      KubeArmor policy in block mode denies an unknown process on a production
      namespace, in the kernel. Snyk documents scanning up to deployment and no
      enforcement engine past it.</span></div>
    <div class="r"><b>Faster</b><span>API discovery starts from live traffic
      rather than from a specification, so Shadow, Zombie and Orphan endpoints
      appear in week one of the rollout.</span></div>
    <div class="r"><b>Cheaper</b><span>One control plane covers ASPM, CSPM,
      KSPM, KIEM, CWPP, API security, secrets and AI security posture. The Snyk
      licence and the tooling around it both retire.</span></div>
  </div>
  <div class="pnum">4</div>
</div></div>
""".format(head=head("PAGE 4 OF 6"), rows=ph_rows, exit=exit_items)

    dm_rows = ""
    for name, rows, y, p, n in DOMAINS:
        dm_rows += ('<tr><td>%s</td><td class="c">%d</td><td class="c">%d</td>'
                    '<td class="c">%d</td><td class="c">%d</td></tr>'
                    % (name, rows, y, p, n))

    facts_html = ""
    for n, l, d in FACTS:
        facts_html += ('<div class="f"><div class="n">%s</div>'
                       '<div class="l">%s</div><div class="d">%s</div></div>'
                       % (n, l, d))

    obj_html = ""
    for q, a in OBJECTIONS:
        obj_html += '<div class="r"><b>%s</b><span>%s</span></div>' % (q, a)

    p5 = """
<div class="page"><div class="p">
  {head}
  <h2>Battlecard <span class="accent">datapoints</span></h2>
  <div class="h2sub">Every number below is countable in the AccuKnox and Snyk
    comparison sheet. AccuKnox scores full on all 75 rows in that sheet, so the
    columns show the Snyk side only.</div>

  <table class="dm"><colgroup><col><col style="width:14mm">
    <col style="width:13mm"><col style="width:13mm"><col style="width:13mm">
    </colgroup>
    <thead><tr><th>Capability domain</th><th class="c">Rows</th>
      <th class="c">Full</th><th class="c">Part</th><th class="c">None</th>
      </tr></thead>
    <tbody>{rows}</tbody>
    <tfoot><tr><td>Snyk total</td><td class="c">75</td><td class="c">39</td>
      <td class="c">20</td><td class="c">16</td></tr></tfoot></table>

  <div class="facts">{facts}</div>

  <div class="obj"><h4>OBJECTION HANDLING</h4>{obj}</div>

  <div class="rev"><b>REVIEW NOTE</b><p>Mrigakshi to confirm three items before
    this goes to CertifyOS. First, the Snyk row verdicts, which come from the
    AccuKnox research sheet rather than from a Snyk statement. Second, whether
    Eclipse and Visual Studio are in scope for CertifyOS developers. Third, the
    commercial framing, which this document leaves out entirely.</p></div>
  <div class="pnum">5</div>
</div></div>
""".format(head=head("PAGE 5 OF 6"), rows=dm_rows, facts=facts_html,
           obj=obj_html)

    gal_html = ""
    for src, title, body, alt in GALLERY:
        gal_html += ('<div class="c"><div class="im"><img src="%s" alt="%s">'
                     '</div><div class="cap"><h4>%s</h4><p>%s</p></div></div>'
                     % (src, alt, title, body))

    ref_pairs = [
        ("AccuKnox ASPM", H["aspm"]), ("Findings and vulnerabilities", H["vuln"]),
        ("EPSS scoring", H["epss"]), ("Rule Engine ticketing", H["rules"]),
        ("ASPM reports", H["reports"]), ("DAST scan types", H["dast"]),
        ("Authenticated DAST", H["dast_auth"]), ("MFA and TOTP DAST", H["mfa"]),
        ("IaC scan", H["iac"]), ("Container scan", H["container"]),
        ("Registry scan", H["registry"]), ("xBOM setup", H["xbom"]),
        ("xBOM via knoxctl", H["xbom_cli"]), ("IDE extension", H["ide"]),
        ("API security", H["api"]), ("CWPP", H["cwpp"]),
        ("App hardening", H["hardening"]), ("Zero Trust", H["zt"]),
        ("KSPM", H["kspm"]), ("KIEM", H["kiem"]), ("CSPM", H["cspm"]),
        ("Compliance", H["compliance"]), ("Prompt Firewall", H["firewall"]),
        ("AI red teaming", H["redteam"]), ("Shadow AI discovery", H["shadow"]),
        ("SaaS and on-prem", H["onprem"]),
        ("Snyk documentation", S["docs"]), ("Snyk Code", S["code"]),
        ("Snyk Open Source", S["oss"]), ("Snyk Container", S["container"]),
        ("Snyk IaC", S["iac"]), ("Snyk AppRisk", S["apprisk"]),
        ("Snyk Broker", S["broker"]), ("Snyk hosting and residency", S["hosting"]),
        ("Snyk API", S["api"]), ("Snyk product", S["product"]),
        ("Snyk plans", S["plans"]),
    ]
    ref_items = "".join('<li><a href="%s">%s</a></li>' % (u, t)
                        for t, u in ref_pairs)

    p6 = """
<div class="page"><div class="p">
  {head}
  <h2>What the platform looks like <span class="accent">in practice</span></h2>
  <div class="h2sub">Four diagrams from the CertifyOS technical proposal. The
    first replaces Snyk. The next two cover ground Snyk does not reach. The
    fourth is the consolidation argument.</div>
  <div class="gal">{gal}</div>
  <div class="reflist"><h4>REFERENCES</h4>
    <div class="dom">AccuKnox links resolve on help.accuknox.com. Snyk links
      resolve on docs.snyk.io and snyk.io.</div><ol>{refs}</ol></div>
  <div class="closer">
    <div><div class="t">See the platform against your own repositories</div>
      <div class="s">accuknox.com &nbsp;·&nbsp; support@accuknox.com
        &nbsp;·&nbsp; help.accuknox.com</div></div>
    <img src="{emblem}" alt="">
  </div>
  <div class="pnum">6</div>
</div></div>
""".format(head=head("PAGE 6 OF 6"), gal=gal_html, refs=ref_items,
           emblem=EMBLEM)

    return ("<!doctype html><meta charset='utf-8'>"
            "<title>AccuKnox vs Snyk, CertifyOS</title>"
            "<style>%s</style>%s%s%s%s%s%s"
            % (CSS, cover, p2, p3, p4, p5, p6))


def main():
    os.makedirs(WORK, exist_ok=True)
    html_path = os.path.join(WORK, FILE + ".html")
    pdf_path = os.path.join(OUT, FILE + ".pdf")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_html())
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        "--print-to-pdf=" + pdf_path, html_path.replace("\\", "/"),
    ], check=True, timeout=300)
    print("wrote %s (%.2f MB)" % (pdf_path, os.path.getsize(pdf_path) / 1e6))


if __name__ == "__main__":
    sys.exit(main())
