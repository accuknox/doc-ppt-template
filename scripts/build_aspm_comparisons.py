"""Build the four AccuKnox ASPM comparison briefs as branded A4 PDFs.

One PDF per competitor: Invicti, OpenText Fortify, HCL AppScan and Black Duck.
Each brief runs five pages. A minimal navy cover, an At a glance page with the
scorecard, two capability matrix pages, and a closing page with the AgentZ
argument and the references.

Source: the four tabs of the "ASPM focused comparison" Google Doc. The SEO
metadata block in that doc is deliberately left out.

Emits HTML with the logos inlined as data URIs, then prints to PDF with
headless Edge.
"""
import base64
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(REPO, "output", "comparisons")
OUT = os.path.join(REPO, "output")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

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


# --------------------------------------------------------------------------
# links used across every brief
# --------------------------------------------------------------------------
L = {
    "agentz": "https://accuknox.com/platform/agentz",
    "agentz_docs": "https://docs.agentzharness.ai/",
    "agentz_gh": "https://github.com/accuknox/agentZ",
    "rules": "https://help.accuknox.com/use-cases/rules-engine-ticket-creation/",
    "aspm": "https://help.accuknox.com/how-to/aspm-overview/",
    "aspm_uc": "https://help.accuknox.com/use-cases/aspm/",
    "dast": "https://help.accuknox.com/how-to/dast-scan-types/",
    "dast_auth": "https://help.accuknox.com/how-to/dast-authenticated-scans/",
    "epss": "https://help.accuknox.com/use-cases/epss-scoring/",
    "vuln": "https://help.accuknox.com/use-cases/vulnerability/",
    "reports": "https://help.accuknox.com/use-cases/aspm-reports/",
}

AREAS = [
    ("Agentic AI Platform",
     "Can the platform build, run and govern production AI agents?"),
    ("Workflow Automation",
     "How far past ticket creation does the automation reach?"),
    ("ASPM Coverage",
     "Which scanners feed one correlated view of application risk?"),
    ("Dynamic Testing (DAST)",
     "Depth of dynamic web, API and CI/CD testing."),
    ("Vulnerability Prioritization",
     "What decides which finding a team fixes first?"),
    ("Reporting and Evidence",
     "How reports are built, filtered and delivered."),
]

# AccuKnox side of the matrix. Identical in all four briefs.
AK = [
    {"state": "y", "points": [
        ("y", "Builds, runs and governs production agents in a Zero Trust sandbox"),
        ("y", "Default-deny network policy, so every outbound call is checked"),
        ("y", "Replayable audit trace for every agent action"),
        ("y", "Model-independent: OpenAI, Anthropic, Gemini and open-source models"),
     ], "refs": [("AgentZ platform", L["agentz"]), ("AgentZ docs", L["agentz_docs"])]},
    {"state": "y", "points": [
        ("y", "Skills chain into Workflows on a cron, an event or an API trigger"),
        ("y", "Sequence or parallel execution, with no rewiring between runs"),
        ("y", "Condition-based auto-ticketing into Jira and ServiceNow"),
     ], "refs": [("Rules engine", L["rules"])]},
    {"state": "y", "points": [
        ("y", "One ASPM view over SAST, DAST, SCA, IaC, secrets and containers"),
        ("y", "Code-to-runtime context in a single control plane"),
        ("y", "Kernel-level runtime enforcement through KubeArmor"),
     ], "refs": [("ASPM overview", L["aspm"]), ("ASPM use case", L["aspm_uc"])]},
    {"state": "y", "points": [
        ("y", "Web, API and CI/CD dynamic testing"),
        ("y", "Four scan types: Baseline, Standard, Extended and Comprehensive"),
        ("y", "Authenticated scans with MFA and TOTP support"),
     ], "refs": [("DAST scan types", L["dast"]),
                 ("Authenticated DAST", L["dast_auth"])]},
    {"state": "y", "points": [
        ("y", "EPSS, CISA KEV, CWE, exploitability and live runtime context"),
        ("y", "Correlated across SAST, DAST, SCA, IaC and containers"),
     ], "refs": [("EPSS scoring", L["epss"]),
                 ("Vulnerability management", L["vuln"])]},
    {"state": "y", "points": [
        ("y", "On-demand and scheduled ASPM reports"),
        ("y", "Filter by label, repository, category, tool or date"),
        ("y", "Email delivery straight from the reports dashboard"),
     ], "refs": [("ASPM reporting", L["reports"])]},
]

AGENTZ_REFS = [("AgentZ platform", L["agentz"]),
               ("AgentZ documentation", L["agentz_docs"]),
               ("AgentZ on GitHub", L["agentz_gh"])]


# --------------------------------------------------------------------------
# per competitor content
# --------------------------------------------------------------------------
BRIEFS = [
{
 "slug": "Invicti",
 "take": [
   "Invicti automates the ticket. AccuKnox automates the work that follows the ticket, inside a sandbox that records every step.",
   "On raw dynamic testing the two platforms are close. The gap opens on runtime context and on what happens after the report.",
 ],
 "vendor": "Invicti",
 "file": "AccuKnox_vs_Invicti_ASPM_Comparison",
 "them_desc": "A DAST-led application security testing suite. ASPM arrived "
              "through the Kondukto acquisition.",
 "verdict": "Invicti is strong at dynamic testing. AccuKnox covers the same "
            "ground and then carries a finding into runtime enforcement and "
            "governed agent action.",
 "chip3": ("AgentZ", "the agentic platform Invicti has no answer to"),
 "them": [
   {"state": "n", "points": [
     ("n", "No agentic AI platform"),
     ("p", "Product scope stays inside application security testing"),
   ]},
   {"state": "p", "points": [
     ("p", "Ticketing automation into Jira, ServiceNow and GitHub"),
     ("n", "No condition-based rules engine"),
     ("n", "No agent-driven orchestration"),
   ]},
   {"state": "p", "points": [
     ("p", "ASPM comes from the Kondukto acquisition, which aggregates 110+ "
           "third-party tools"),
     ("p", "Native SAST is powered by Mend, so it is not first-party"),
     ("n", "No runtime enforcement layer"),
   ]},
   {"state": "y", "points": [
     ("y", "DAST-led, running the Acunetix and Invicti engines"),
     ("y", "Proof-Based Scanning confirms a finding before it is reported"),
     ("y", "Strong authenticated scanning with OAuth2 and SAML"),
     ("n", "No tiered scan modes"),
   ]},
   {"state": "y", "points": [
     ("y", "Machine-learning risk scoring with proof-based validation"),
     ("y", "CISA KEV and EPSS feed the score"),
     ("p", "Cross-tool correlation runs through the aggregated ASPM layer"),
   ]},
   {"state": "y", "points": [
     ("y", "Technical and compliance reporting"),
     ("y", "PCI DSS, ISO 27001, HIPAA, OWASP Top 10 and NIST mappings"),
   ]},
 ],
 "edge": [
   "AgentZ governs production agents inside a default-deny sandbox. Every "
   "outbound call is checked against an allowlist before it leaves. "
   "Credentials are scoped and injected at runtime, so they never sit in "
   "agent context.",
   "Invicti automates ticket creation from scan findings. That is the step "
   "before orchestration, not the orchestration itself.",
 ],
 "why": [
   ("Better",
    "AccuKnox pairs ASPM with runtime enforcement and the AgentZ agentic "
    "platform. A finding correlated in ASPM can be enforced at the kernel "
    "through KubeArmor, then acted on by a governed agent. Invicti stops at "
    "the test report and the ticket."),
   ("Faster",
    "AgentZ turns a described job into a running workflow. Skills chain on a "
    "cron, an event or an API call. A runtime alert investigation runs as one "
    "traced workflow instead of a manual handoff between the scanner and the "
    "ticket queue."),
   ("ROI-Driven",
    "AccuKnox holds ASPM, DAST, SCA, container security, runtime protection "
    "and the agentic platform in one control plane. Invicti covers the "
    "testing slice and reaches ASPM breadth by aggregating 110+ third-party "
    "tools, each one a separate invoice line."),
 ],
 "note": None,
},
{
 "slug": "OpenText Fortify",
 "take": [
   "Fortify enriches and deduplicates findings well. Its reach stops where the cluster begins, because runtime and Kubernetes enforcement sit outside the portfolio.",
   "Fortify reports and prioritizes to an enterprise standard. AccuKnox feeds live runtime context into the same score.",
 ],
 "vendor": "OpenText Fortify",
 "file": "AccuKnox_vs_OpenText_Fortify_ASPM_Comparison",
 "them_desc": "An enterprise AppSec suite built around SAST, DAST, SCA and "
              "AppSec-as-a-Service.",
 "verdict": "Fortify is a deep testing portfolio with real ASPM context. "
            "AccuKnox matches that context and adds runtime enforcement plus "
            "a governed agent runtime.",
 "chip3": ("AgentZ", "the agentic platform Fortify has no answer to"),
 "them": [
   {"state": "n", "points": [
     ("n", "No agentic AI platform"),
     ("p", "AI is limited to Remediation Aviator, which audits and fixes SAST "
           "findings"),
   ]},
   {"state": "p", "points": [
     ("p", "Issue-tracker integration with Jira and Azure DevOps"),
     ("n", "No condition-based rules engine"),
     ("n", "No agent-driven orchestration"),
   ]},
   {"state": "y", "points": [
     ("y", "OpenText ASPM aggregates SAST, DAST, SCA and IaC"),
     ("y", "Contextual enrichment, deduplication and custom risk scoring"),
     ("n", "Runtime and Kubernetes enforcement sit outside the portfolio"),
   ]},
   {"state": "y", "points": [
     ("y", "Fortify DAST and ScanCentral DAST with CI/CD automation"),
     ("y", "WebInspect adds workflow macros and MFA scanning"),
   ]},
   {"state": "y", "points": [
     ("y", "Contextual enrichment and deduplication across tools"),
     ("y", "Custom risk scoring with asset context"),
     ("y", "Exploitability-based prioritization through OpenText ASPM"),
   ]},
   {"state": "y", "points": [
     ("y", "AppSec compliance and technical reporting"),
     ("y", "OWASP, PCI and NIST mappings"),
     ("y", "Fortify on Demand is FedRAMP authorized"),
   ]},
 ],
 "edge": [
   "AgentZ governs production agents inside a default-deny sandbox. Every "
   "tool call, memory read and model response is stored with a deterministic "
   "replay ID, so an auditor can rerun the exact sequence.",
   "Fortify ships Remediation Aviator, which generates validated fixes for "
   "eligible SAST findings. That is finding-level remediation inside the "
   "scanner. AgentZ is a runtime for agents that act across AWS, Kubernetes, "
   "GitHub, Jira and Slack.",
 ],
 "why": [
   ("Better",
    "AccuKnox extends application security into runtime enforcement and adds "
    "the AgentZ agentic platform. A finding correlated in ASPM can be "
    "enforced at the kernel through KubeArmor, then acted on by a governed "
    "agent. Fortify stops at application testing and ASPM context."),
   ("Faster",
    "AgentZ turns a described job into a running workflow. Skills chain on a "
    "cron, an event or an API call. Assembling compliance evidence or "
    "investigating a runtime alert runs as one traced workflow instead of a "
    "handoff between the scanner and the ticket queue."),
   ("ROI-Driven",
    "AccuKnox holds ASPM, DAST, SCA, container security, runtime protection "
    "and the agentic platform in one control plane. Fortify spans SAST, DAST, "
    "SCA and Fortify on Demand as separate products plus a managed service."),
 ],
 "note": None,
},
{
 "slug": "HCL AppScan",
 "take": [
   "AppScan's AI reads and fixes its own findings. AgentZ runs and governs agents that act across AWS, Kubernetes, GitHub, Jira and Slack.",
   "AppScan is strong on testing depth and machine-learning triage. Reporting detail varies by edition, while AccuKnox keeps one reports dashboard.",
 ],
 "vendor": "HCL AppScan",
 "file": "AccuKnox_vs_HCL_AppScan_ASPM_Comparison",
 "them_desc": "An AI-assisted application security testing suite spanning "
              "SAST, DAST, IAST, SCA and API security.",
 "verdict": "AppScan has a genuine AI story, but it operates on AppScan's own "
            "findings. AccuKnox governs agents that act across the wider "
            "estate and enforces policy at the kernel.",
 "chip3": ("AgentZ", "governs agents at runtime, not only findings in a database"),
 "them": [
   {"state": "p", "points": [
     ("p", "An MCP Server lets AI assistants query AppScan on Cloud findings"),
     ("p", "Agentic AI triages findings and generates fixes"),
     ("n", "No sandbox to build, run and govern production agents"),
   ]},
   {"state": "p", "points": [
     ("p", "Auto Issue Correlation plus CI/CD integration"),
     ("p", "RapidFix generates code fixes and opens Jira tickets"),
     ("n", "No general agent orchestration across arbitrary tools"),
   ]},
   {"state": "y", "points": [
     ("y", "SAST, DAST, IAST, SCA, API, secrets, container and IaC scanning"),
     ("y", "Posture management with Auto Issue Correlation"),
     ("n", "No kernel-level runtime enforcement layer"),
   ]},
   {"state": "y", "points": [
     ("y", "Mature DAST across AppScan Standard and AppScan on Cloud"),
     ("y", "Recorded login and manual explore for authenticated scans"),
     ("y", "Dynamic testing is a core AppScan strength"),
   ]},
   {"state": "y", "points": [
     ("y", "Intelligent Finding Analytics cuts false positives with machine "
           "learning"),
     ("y", "Agentic AI ranks risk and generates candidate fixes"),
   ]},
   {"state": "p", "points": [
     ("p", "Reporting runs from the AppScan Enterprise and on Cloud "
           "dashboards"),
     ("p", "Scheduling and export options vary by AppScan edition"),
   ]},
 ],
 "edge": [
   "The AppScan AI story is real. The MCP Server turns findings into a "
   "conversation, so a CISO or a developer can ask about risk, hunt for a CVE "
   "or open a remediation ticket in plain language. RapidFix writes the fix. "
   "All of it works on AppScan's own data.",
   "AgentZ operates one layer out. It is a runtime that builds, runs and "
   "governs agents across AWS, Kubernetes, GitHub, Jira and Slack, inside a "
   "default-deny sandbox where every egress is checked and recorded.",
 ],
 "why": [
   ("Better",
    "AccuKnox extends application security into kernel-level runtime "
    "enforcement through KubeArmor and adds the AgentZ agentic platform. "
    "AppScan covers a broad testing suite with code-to-cloud visibility, but "
    "its AI acts on findings rather than governing agents at runtime."),
   ("Faster",
    "AgentZ turns a described job into a running workflow. Skills chain on a "
    "cron, an event or an API call. A runtime alert investigation runs as one "
    "traced workflow instead of a query against a findings database."),
   ("ROI-Driven",
    "AccuKnox holds ASPM, DAST, SCA, container security, runtime protection "
    "and the agentic platform in one control plane. AppScan lands as a set of "
    "products, on Cloud, 360, Enterprise, Standard and Source, priced by the "
    "capabilities a team turns on."),
 ],
 "note": None,
},
{
 "slug": "Black Duck",
 "take": [
   "Software Risk Manager correlates 150+ tools well. Nothing in the portfolio enforces policy on a running workload.",
   "Black Duck leads on open-source intelligence. AccuKnox leads on tiered dynamic testing and runtime-aware prioritization.",
 ],
 "vendor": "Black Duck",
 "file": "AccuKnox_vs_Black_Duck_ASPM_Comparison",
 "them_desc": "An application security and software supply chain suite led by "
              "SCA and the Software Risk Manager ASPM product.",
 "verdict": "Black Duck leads on open-source composition analysis. AccuKnox "
            "leads on unified ASPM, runtime enforcement and governed agents.",
 "chip3": ("AgentZ", "the agentic platform Black Duck has no answer to"),
 "them": [
   {"state": "n", "points": [
     ("n", "No agentic AI platform"),
     ("p", "The portfolio covers AppSec testing and supply chain security"),
   ]},
   {"state": "p", "points": [
     ("p", "Policy-based open-source governance with CI/CD integration"),
     ("p", "Software Risk Manager pushes findings into developer workflows"),
     ("n", "No general agent orchestration"),
   ]},
   {"state": "y", "points": [
     ("y", "Software Risk Manager integrates 150+ third-party tools"),
     ("y", "Correlates, deduplicates and maps to 20+ compliance standards"),
     ("n", "No kernel-level runtime enforcement"),
   ]},
   {"state": "p", "points": [
     ("p", "Dynamic testing runs through Continuous Dynamic and Polaris fAST "
           "Dynamic"),
     ("p", "Scan depth and authentication support vary by service tier"),
   ]},
   {"state": "y", "points": [
     ("y", "Software Risk Manager correlates and prioritizes across tools"),
     ("y", "Black Duck Security Advisories give same-day open-source "
           "intelligence beyond the NVD"),
   ]},
   {"state": "y", "points": [
     ("y", "SBOM export in SPDX and CycloneDX"),
     ("y", "Policy and compliance reporting"),
     ("y", "KPI dashboards inside Software Risk Manager"),
   ]},
 ],
 "edge": [
   "AgentZ governs production agents inside a default-deny sandbox. Every "
   "tool call, memory read and model response is stored with a deterministic "
   "replay ID.",
   "Software Risk Manager consolidates and prioritizes findings, which is "
   "ASPM correlation. AgentZ acts on the result. It triages a cloud "
   "misconfiguration, finds the change that caused it, and opens an incident "
   "in Slack, tracing every model and tool call on the way.",
 ],
 "why": [
   ("Better",
    "AccuKnox extends application security into kernel-level runtime "
    "enforcement through KubeArmor and adds the AgentZ agentic platform. "
    "Where a team's center of gravity is open-source composition analysis, "
    "Black Duck remains the stronger fit."),
   ("Faster",
    "AgentZ turns a described job into a running workflow. Skills chain on a "
    "cron, an event or an API call. A runtime alert investigation runs as one "
    "traced workflow instead of a report assembled by hand from the ASPM "
    "console."),
   ("ROI-Driven",
    "AccuKnox holds ASPM, DAST, SCA, container security, runtime protection "
    "and the agentic platform in one control plane. Black Duck reaches "
    "comparable breadth across separate products: Coverity for SAST, Black "
    "Duck SCA, Seeker for IAST, Continuous Dynamic for DAST and Software Risk "
    "Manager for ASPM."),
 ],
 "note": "Black Duck leads on software composition analysis. Its KnowledgeBase "
         "covers 8.7M+ open-source components with same-day vulnerability "
         "intelligence. A team whose primary need is deep open-source and "
         "supply-chain analysis should weigh that strength directly.",
},
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


def points_html(points):
    out = []
    for state, text in points:
        out.append('<li>%s<span>%s</span></li>' % (mark(state), text))
    return '<ul class="pts">%s</ul>' % "".join(out)


def refs_html(refs):
    if not refs:
        return ""
    links = " &nbsp;·&nbsp; ".join(
        '<a href="%s">%s</a>' % (u, t) for t, u in refs)
    return '<div class="ref"><b>Reference</b> %s</div>' % links


def matrix_rows(b, lo, hi):
    out = []
    for i in range(lo, hi):
        area, note = AREAS[i]
        out.append(
            '<tr><td class="area"><div class="an">%s</div>'
            '<div class="aq">%s</div></td>'
            '<td class="ak">%s%s</td>'
            '<td class="them">%s</td></tr>'
            % (area, note, points_html(AK[i]["points"]),
               refs_html(AK[i]["refs"]), points_html(b["them"][i]["points"])))
    return "".join(out)


def matrix_table(b, lo, hi):
    return (
        '<table class="mx"><colgroup><col style="width:40mm">'
        '<col style="width:72mm"><col style="width:72mm"></colgroup>'
        '<thead><tr><th class="th-area">Capability Area</th>'
        '<th class="th-ak"><img src="%s" alt="AccuKnox"></th>'
        '<th class="th-them">%s</th></tr></thead>'
        '<tbody>%s</tbody></table>'
        % (LOGO_DARK, b["vendor"], matrix_rows(b, lo, hi)))


LEGEND = ('<div class="legend">%s<span>Full capability</span>%s'
          '<span>Partial or indirect</span>%s<span>Not available</span></div>'
          % (mark("y", "3.3mm"), mark("p", "3.3mm"), mark("n", "3.3mm")))


def head(b, label):
    return ('<div class="head"><img src="%s" alt="AccuKnox">'
            '<span>ASPM COMPARISON &nbsp;·&nbsp; ACCUKNOX VS %s &nbsp;·&nbsp; %s'
            '</span></div>' % (LOGO_LIGHT, b["vendor"].upper(), label))


def scorecard(b):
    rows = []
    for i, (area, _n) in enumerate(AREAS):
        rows.append('<tr><td>%s</td><td>%s</td><td>%s</td></tr>'
                    % (area, mark(AK[i]["state"], "3.5mm"),
                       mark(b["them"][i]["state"], "3.5mm")))
    return ('<table class="score"><thead><tr><th>Capability Area</th>'
            '<th>AccuKnox</th><th>%s</th></tr></thead><tbody>%s</tbody></table>'
            % (b["vendor"], "".join(rows)))


def all_refs(b):
    seen, out = set(), []
    for cell in AK:
        for t, u in cell["refs"]:
            if u not in seen:
                seen.add(u)
                out.append((t, u))
    for t, u in AGENTZ_REFS:
        if u not in seen:
            seen.add(u)
            out.append((t, u))
    return out


# --------------------------------------------------------------------------
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { font-family: 'Space Grotesk', 'Inter', 'Segoe UI', sans-serif;
  color: INK; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: BLUE; text-decoration: none; }

.page { position: relative; width: 210mm; height: 297mm; overflow: hidden;
  page-break-after: always; background: #fff; }
.page:last-child { page-break-after: auto; }

/* ---------------- cover ---------------- */
.dark { color: #fff; background: #0B1240; }
.p1 { position: relative; padding: 28mm 20mm 14mm; height: 100%; }
.p1 .logo { height: 9.6mm; }
.eyebrow { margin-top: 56mm; font-size: 8.4pt; letter-spacing: 3px;
  font-weight: 700; color: #A9BEFF; }
.rule { height: 3px; width: 48mm; border-radius: 3px; margin: 5mm 0 7mm;
  background: RED; }
h1 { font-size: 38pt; line-height: 1.08; font-weight: 700; letter-spacing: -1px;
  color: #fff; }
h1 .vs { color: #A9BEFF; font-weight: 500; }
.subtitle { margin-top: 7mm; font-size: 13pt; font-weight: 500; color: #fff; }
.scope { margin-top: 4mm; font-size: 10.4pt; line-height: 1.6; color: #CBD7FA;
  max-width: 150mm; }

.p1foot { position: absolute; left: 20mm; right: 20mm; bottom: 14mm;
  font-size: 8pt; color: #A9BEFF; display: flex;
  justify-content: space-between; border-top: 1px solid rgba(169,190,255,.3);
  padding-top: 4mm; }

/* ---------------- at a glance ---------------- */
.gl { display: flex; gap: 7mm; margin-top: 6mm; }
.gl .c { flex: 1; }
.gl .n { font-size: 12pt; font-weight: 700; color: NAVY;
  padding-bottom: 2.4mm; border-bottom: 2.4px solid BLUE; }
.gl .c.tm .n { border-bottom-color: GREY_BD; }
.gl .d { margin-top: 3.2mm; font-size: 9.4pt; line-height: 1.6; color: #2B3150; }

.verdict { margin-top: 8mm; border-radius: 3mm; padding: 5mm 5.6mm;
  background: GREY_BG; border-left: 3.4px solid RED; }
.verdict .k { font-size: 7.4pt; letter-spacing: 1.8px; font-weight: 700;
  color: RED; }
.verdict p { margin-top: 2.6mm; font-size: 10pt; line-height: 1.6;
  color: #23283F; }

.sc-wrap { margin-top: 9mm; }
table.score { width: 100%; border-collapse: collapse; margin-top: 4mm; }
table.score th { font-size: 8.4pt; color: #fff; background: NAVY;
  text-align: left; padding: 3.4mm 4mm; font-weight: 700; }
table.score th:nth-child(2), table.score th:nth-child(3) { text-align: center;
  width: 36mm; }
table.score td { font-size: 9.4pt; color: #23283F; padding: 4.2mm 4mm;
  border: 1px solid GREY_BD; border-top: none; }
table.score td:nth-child(2), table.score td:nth-child(3) { text-align: center; }
table.score tbody tr:nth-child(odd) td { background: #F7F9FF; }

.ask { margin-top: 6mm; border-radius: 3mm; padding: 4.4mm 5.4mm;
  background: GREY_BG; border: 1px solid GREY_BD; }
.ask h4 { font-size: 7.4pt; letter-spacing: 1.6px; font-weight: 700;
  color: NAVY; }
.ask ol { margin-top: 2.8mm; padding-left: 4.6mm; }
.ask li { font-size: 8.4pt; line-height: 1.5; color: #2B3150;
  margin-bottom: 1.6mm; }
.ask li:last-child { margin-bottom: 0; }

/* ---------------- light pages ---------------- */
.p { padding: 12mm 13mm 14mm; height: 100%; position: relative; }
.head { display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1.6px solid GREY_BD; padding-bottom: 3mm; margin-bottom: 5mm; }
.head img { height: 6mm; }
.head span { font-size: 6.8pt; color: MUTE; letter-spacing: .7px; }
h2 { font-size: 17pt; font-weight: 700; color: NAVY; letter-spacing: -.5px; }
h2 .accent { color: BLUE; }
.h2sub { margin-top: 2.2mm; font-size: 9pt; line-height: 1.55; color: #3A4064; }

.legend { display: flex; align-items: center; gap: 2mm; margin: 3.6mm 0 3.2mm;
  font-size: 7.4pt; color: MUTE; }
.legend span { margin-right: 4.5mm; }
.mk { vertical-align: -.6mm; flex: none; }

table.mx { width: 100%; border-collapse: collapse; table-layout: fixed; }
table.mx th { text-align: left; padding: 3.6mm 4mm; background: NAVY;
  color: #fff; font-size: 8.6pt; font-weight: 700; vertical-align: middle; }
table.mx th img { height: 4.8mm; display: block; }
table.mx th.th-area { font-size: 7.6pt; letter-spacing: 1.2px;
  text-transform: uppercase; color: #B9C6EE; }
table.mx td { padding: 5.4mm 4mm 5.8mm; vertical-align: top;
  border: 1px solid GREY_BD; border-top: none; }
table.mx td.area { background: GREY_BG; border-left: 2.6px solid BLUE; }
table.mx td.ak { background: #F7F9FF; }
table.mx tbody tr:first-child td { border-top: none; }
.an { font-size: 9.4pt; font-weight: 700; color: NAVY; line-height: 1.25; }
.aq { margin-top: 2.2mm; font-size: 7.6pt; line-height: 1.45; color: #565F86; }

ul.pts { list-style: none; }
ul.pts li { display: flex; gap: 2.4mm; align-items: flex-start;
  margin-bottom: 3mm; }
ul.pts li:last-child { margin-bottom: 0; }
ul.pts li span { font-size: 8.6pt; line-height: 1.48; color: #23283F; }
.ref { margin-top: 3mm; padding-top: 2.4mm; border-top: 1px dashed GREY_BD;
  font-size: 7.2pt; line-height: 1.5; color: MUTE; }
.ref a { white-space: nowrap; }
.ref b { color: MUTE; letter-spacing: .8px; font-weight: 700;
  margin-right: 1.4mm; }

.take { position: absolute; left: 13mm; right: 13mm; bottom: 13mm;
  border-radius: 3mm; padding: 4.2mm 5mm;
  background: NAVY; color: #fff; display: flex; gap: 4mm;
  align-items: baseline; }
.take b { flex: none; font-size: 7.2pt; letter-spacing: 1.6px; color: #9BB4FF; }
.take span { font-size: 8.8pt; line-height: 1.5; color: #EAEFFC; }

.hook { margin-top: 3.4mm; border-radius: 3.4mm; padding: 4.2mm 5.4mm 4.4mm;
  background: #F4F6FE; border: 1px solid #D5DDF5; border-left: 3.4px solid SEC; }
.hook .hk { display: flex; align-items: baseline; gap: 3.4mm; }
.hook .tag { flex: none; font-size: 6.6pt; letter-spacing: 1.4px;
  font-weight: 700; color: #fff; background: SEC; padding: 1.3mm 2.4mm;
  border-radius: 1.6mm; }
.hook h3 { font-size: 10.4pt; font-weight: 700; color: NAVY; }
.hook .cols { margin-top: 2.8mm; column-count: 2; column-gap: 7mm; }
.hook p { font-size: 8.2pt; line-height: 1.5; color: #2B3150;
  break-inside: avoid; }
.hook p + p { margin-top: 0; }

.take.flow { position: static; margin-top: 3mm; }

/* ---------------- closing page ---------------- */
.edge { margin-top: 5mm; border-radius: 3.4mm; padding: 5mm 5.6mm;
  background: #F4F6FE; border: 1px solid #D5DDF5; border-left: 3.4px solid SEC; }
.edge h3 { font-size: 12pt; font-weight: 700; color: NAVY; }
.edge p { margin-top: 3mm; font-size: 9pt; line-height: 1.6; color: #2B3150; }
.edge .lk { margin-top: 4mm; font-size: 7.6pt; color: MUTE; }

.why { margin-top: 6mm; }
.why .row { display: flex; gap: 4mm; margin-bottom: 4mm; }
.why .tag { flex: none; width: 27mm; }
.why .tag i { display: inline-block; font-style: normal; font-size: 8pt;
  font-weight: 700; letter-spacing: .8px; text-transform: uppercase;
  color: #fff; background: BLUE; padding: 1.7mm 3mm; border-radius: 2mm; }
.why .row.b .tag i { background: BLUE; }
.why .row.f .tag i { background: SEC; }
.why .row.r .tag i { background: GREEN; }
.why .txt { flex: 1; font-size: 9pt; line-height: 1.6; color: #2B3150;
  padding-top: .6mm; }

.note { margin-top: 5mm; border-radius: 3mm; padding: 4.2mm 5mm;
  background: #FFF6F7; border: 1px solid #F0CBD1; border-left: 3.4px solid RED; }
.note b { font-size: 8pt; letter-spacing: 1px; color: RED; }
.note p { margin-top: 2.2mm; font-size: 8.6pt; line-height: 1.55; color: #3A2B2E; }

.reflist { margin-top: 6mm; }
.reflist h4 { font-size: 8pt; letter-spacing: 1.8px; font-weight: 700;
  color: MUTE; padding-bottom: 2.6mm; border-bottom: 1.4px solid GREY_BD; }
.reflist ol { margin-top: 3.2mm; list-style: none; column-count: 3;
  column-gap: 6mm; }
.reflist li { font-size: 6.8pt; line-height: 1.5; margin-bottom: 2mm;
  break-inside: avoid; color: MUTE; }
.reflist li b { display: block; color: NAVY; font-weight: 600; font-size: 7.4pt;
  margin-bottom: .4mm; }
.reflist li a { word-break: break-all; }

.closer { position: absolute; left: 13mm; right: 13mm; bottom: 13mm;
  border-radius: 3.4mm; padding: 5mm 6mm; color: #fff;
  background: linear-gradient(120deg, NAVY 0%, #182B8C 60%, #0A0E33 100%);
  display: flex; align-items: center; justify-content: space-between; }
.closer .t { font-size: 11pt; font-weight: 700; }
.closer .s { margin-top: 1.8mm; font-size: 8.2pt; color: #B9C6EE; }
.closer img { height: 11mm; }
.pnum { position: absolute; right: 13mm; bottom: 6mm; font-size: 7.4pt;
  color: MUTE; }
"""
for _k, _v in (("INK", INK), ("NAVY", NAVY), ("BLUE", BLUE), ("SEC", SEC),
               ("RED", RED), ("GREEN", GREEN), ("MUTE", MUTE),
               ("GREY_BG", GREY_BG), ("GREY_BD", GREY_BD)):
    CSS = CSS.replace(_k, _v)


def build_html(b):
    v = b["vendor"]

    cover = """
<div class="page dark"><div class="p1">
  <img class="logo" src="{logo}" alt="AccuKnox">
  <div class="eyebrow">ASPM COMPARISON BRIEF</div>
  <div class="rule"></div>
  <h1>AccuKnox <span class="vs">vs</span><br>{v}</h1>
  <div class="subtitle">ASPM and Application Security Comparison</div>
  <div class="scope">Six capability areas, scored side by side, with a reference
    link behind every AccuKnox claim.</div>

  <div class="p1foot"><span>AccuKnox &nbsp;·&nbsp; Zero Trust security for AI,
    API, Application, Cloud and Supply Chain</span>
    <span>accuknox.com</span></div>
</div></div>
""".format(logo=LOGO_DARK, v=v)

    p2 = """
<div class="page"><div class="p">
  {head}
  <h2>At a <span class="accent">glance</span></h2>
  <div class="h2sub">This brief compares both platforms on Application Security
    Posture Management, the discipline that correlates SAST, DAST, SCA, IaC,
    secrets and container findings into one prioritized view.</div>

  <div class="gl">
    <div class="c ak"><div class="n">AccuKnox</div>
      <div class="d">A unified ASPM and CNAPP platform. Code-to-runtime context
        in one control plane, with kernel-level enforcement through KubeArmor
        and the AgentZ agentic platform.</div></div>
    <div class="c tm"><div class="n">{v}</div><div class="d">{td}</div></div>
  </div>

  <div class="verdict"><div class="k">WHERE IT LANDS</div><p>{verdict}</p></div>

  <div class="sc-wrap"><h2 style="font-size:14pt">Scorecard</h2>
    {legend}
    {score}</div>
  <div class="pnum">2</div>
</div></div>
""".format(head=head(b, "PAGE 2 OF 5"), v=v, td=b["them_desc"],
           verdict=b["verdict"], legend=LEGEND, score=scorecard(b))

    p3 = """
<div class="page"><div class="p">
  {head}
  <h2>Capability <span class="accent">Matrix</span></h2>
  <div class="h2sub">Areas one to three cover the agentic platform, the
    automation model and the breadth of the correlated view.</div>
  {legend}
  {table}
  <div class="take"><b>TAKEAWAY</b><span>{take}</span></div>
  <div class="pnum">3</div>
</div></div>
""".format(head=head(b, "PAGE 3 OF 5"), legend=LEGEND, table=matrix_table(b, 0, 3),
           take=b["take"][0])

    p4 = """
<div class="page"><div class="p">
  {head}
  <h2>Capability Matrix <span class="accent">continued</span></h2>
  <div class="h2sub">Areas four to six cover dynamic testing depth, how a
    platform ranks what to fix first, and the evidence it produces for
    auditors.</div>
  {legend}
  {table}
  <div class="hook">
    <div class="hk"><span class="tag">AGENTZ + ACCUKNOX</span>
      <h3>AgentZ connects to your AccuKnox tenant</h3></div>
    <div class="cols">
      <p>AgentZ talks to AccuKnox SaaS through the platform API, so it works on
        your own ASPM data. Ask it to reprioritize findings against your asset
        criticality. Or have it shape a report the way your auditor wants it,
        then chain that Skill into a Workflow that runs on a cron or a
        webhook.</p>
      <p>Through MCP, AgentZ also reaches the tools you already run: Jira,
        ServiceNow, GitHub, Slack, AWS and Kubernetes. A custom need lands as a
        new Skill rather than a support ticket. Security operations then run as
        governed agent workflows instead of manual handoffs.</p>
    </div>
  </div>
  <div class="take flow"><b>TAKEAWAY</b><span>{take}</span></div>
  <div class="pnum">4</div>
</div></div>
""".format(head=head(b, "PAGE 4 OF 5"), legend=LEGEND, table=matrix_table(b, 3, 6),
           take=b["take"][1])

    edge_paras = "".join("<p>%s</p>" % p for p in b["edge"])
    edge_links = " &nbsp;·&nbsp; ".join(
        '<a href="%s">%s</a>' % (u, t) for t, u in AGENTZ_REFS)

    why_rows = ""
    for cls, (tag, txt) in zip(("b", "f", "r"), b["why"]):
        why_rows += ('<div class="row %s"><div class="tag"><i>%s</i></div>'
                     '<div class="txt">%s</div></div>' % (cls, tag, txt))

    ASK = ('<div class="ask"><h4>THREE QUESTIONS TO TAKE INTO YOUR '
           'EVALUATION</h4><ol>'
           '<li>Can the platform run and govern an agent in production, or does '
           'its AI only annotate findings?</li>'
           '<li>Does one control plane correlate SAST, DAST, SCA, IaC, secrets '
           'and containers, or does breadth come from aggregating other '
           "vendors' tools?</li>"
           '<li>Can a correlated finding be enforced at runtime, or does the '
           'trail end at a ticket?</li></ol></div>')

    note_html = ""
    if b["note"]:
        note_html = ('<div class="note"><b>WHERE %s LEADS</b><p>%s</p>'
                     '</div>' % (v.upper(), b["note"]))

    ref_items = "".join('<li><b>%s</b><a href="%s">%s</a></li>' % (t, u, u)
                        for t, u in all_refs(b))

    p5 = """
<div class="page"><div class="p">
  {head}
  <h2>Why customers choose <span class="accent">AccuKnox</span> over {v}</h2>

  <div class="edge">
    <h3>AgentZ is the competitive edge</h3>
    {edge}
    <div class="lk">{links}</div>
  </div>

  <div class="why">{why}</div>
  {note}

  {ask}

  <div class="reflist"><h4>REFERENCES</h4><ol>{refs}</ol></div>

  <div class="closer">
    <div><div class="t">See the platform in action</div>
      <div class="s">accuknox.com &nbsp;·&nbsp; support@accuknox.com</div></div>
    <img src="{emblem}" alt="">
  </div>
  <div class="pnum">5</div>
</div></div>
""".format(head=head(b, "PAGE 5 OF 5"), v=v, edge=edge_paras, links=edge_links,
           why=why_rows, note=note_html, refs=ref_items, emblem=EMBLEM,
           ask="" if b["note"] else ASK)

    return ("<!doctype html><meta charset='utf-8'><title>AccuKnox vs %s</title>"
            "<style>%s</style>%s%s%s%s%s" % (v, CSS, cover, p2, p3, p4, p5))


def main():
    os.makedirs(WORK, exist_ok=True)
    for b in BRIEFS:
        html_path = os.path.join(WORK, b["file"] + ".html")
        pdf_path = os.path.join(OUT, b["file"] + ".pdf")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(build_html(b))
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        subprocess.run([
            EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--print-to-pdf=" + pdf_path, html_path.replace("\\", "/"),
        ], check=True, timeout=300)
        print("wrote %s (%.2f MB)" % (pdf_path, os.path.getsize(pdf_path) / 1e6))


if __name__ == "__main__":
    sys.exit(main())
