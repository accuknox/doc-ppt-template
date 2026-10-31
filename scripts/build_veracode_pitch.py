# -*- coding: utf-8 -*-
"""
AccuKnox pitch deck for Veracode. Four selected products: Container Security and IaC,
CSPM, DSPM and API Security.

Sources, and nothing else:
  1. help.accuknox.com pages in D:\\AccuKnox\\help\\docs (paths in each slide's notes).
  2. accuknox.com/differentiators, read 2026-10-03 (deployment tabs, stats, differentiators).
  3. "AccuKnox - Pricing & Sizing - SEP 2026.xlsx" (Google Drive 1qjJG7cNNFB6rtEEah0wpVqt5TwCV-z5Y).
  4. references/technical-reference/playbooks-and-poc PDFs in the help repo (CSPM and CWPP POC).
  5. references/PRODUCT UI screenshots in the help repo (demo tenant data).
Facts with no source get a red todo_panel.

Build:   py -3.11 scripts/veracode_svg.py && py -3.11 scripts/build_veracode_pitch.py
Render:  powershell -File scripts/render.ps1 -Pptx <abs>/output/AccuKnox_Veracode_Pitch.pptx -Out <abs>/output/render/veracode
"""
import os, shutil, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import *  # noqa: F401,F403

google_safe()

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "PPT Template.pptx")
OUT = os.path.join(HERE, "..", "output", "AccuKnox_Veracode_Pitch.pptx")
DIAG = os.path.join(HERE, "..", "work", "veracode", "diagrams")
IMG = os.path.join(HERE, "..", "work", "veracode", "img")

shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_STD = prs.slide_layouts[4]
for sid in list(prs.slides._sldIdLst):
    try:
        prs.part.drop_rel(sid.get(qn("r:id")))
    except Exception:
        pass
    prs.slides._sldIdLst.remove(sid)


# ------------------------------------------------------------------ helpers
def std(title, kicker, notes_text):
    s = prs.slides.add_slide(L_STD)
    set_title(s, title)
    blank_footer(s)
    eyebrow(s, kicker, y=0.84, w=9.2, size=10.5)
    notes(s, notes_text)
    return s


def dg(s, name, x, y, w):
    return diagram(s, os.path.join(DIAG, name + ".png"), x, y, w)


def img(name):
    return os.path.join(IMG, name)


def row(s, x, y, w, icn, head, sub, ts=0.46, hs=12.5, bs=10.5, h=0.72, bg=None):
    """Icon tile, bold head, one short line under it."""
    icon_tile(s, icn, x, y + 0.04, ts, bg=bg)
    box(s, x + ts + 0.14, y, w - ts - 0.14, 0.3, text=head, size=hs, color=NAVY, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + ts + 0.14, y + 0.29, w - ts - 0.14, h - 0.3, text=sub, size=bs, color=MUTE, ml=0, mt=0)


def logos(s, names, x, y, sz, gap):
    for i, n in enumerate(names):
        icon_img(s, n, x + i * (sz + gap), y, sz)


def shot(s, name, x, y, w, h, caption):
    return image_fit(s, img(name), x, y, w, h, caption=caption, capsize=9.5)


# ================================================================ 1. cover
cover_slide(prs, "AccuKnox for Veracode\nContainer, IaC, CSPM, DSPM\nand API Security",
            subtitle="Partner briefing, October 2026", tsize=22, h=1.3)


# ================================================================ 2. agenda
s = std("Agenda", "Six parts, slides 3 to 16", """
Agenda. Six parts.
Part 1, the problem: risk that appears after the code commit.
Part 2, the four products in scope for Veracode: Container Security and IaC, CSPM, DSPM, API Security.
Part 3, architecture: how findings flow, where each component runs, and the four deployment modes.
Part 4, use cases and POC scenarios with pass checks.
Part 5, the user journey in the AccuKnox console.
Part 6, differentiators, the recommended stack ranking of the four modules, and list pricing.
""")
toc = [("alert-triangle", "The Problem", "Risk after the commit", "Slide 3"),
       ("stack-2", "Our Solution", "Four products, one platform", "Slides 4 to 7"),
       ("sitemap", "Architecture", "Technical, deployment, modes", "Slides 8 to 10"),
       ("target", "Use Cases and POC", "Scenarios with pass checks", "Slides 11 and 12"),
       ("device-desktop", "User Journey", "The console, step by step", "Slide 13"),
       ("trophy", "Why AccuKnox", "Differentiators, ranking, pricing", "Slides 14 to 16")]
for i, (icn, h, sub, rng) in enumerate(toc):
    x = 0.40 + (i % 3) * 3.1
    y = 1.22 + (i // 3) * 2.0
    box(s, x, y, 2.96, 1.82, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    icon_tile(s, icn, x + 0.18, y + 0.2, 0.74)
    box(s, x + 1.9, y + 0.16, 0.9, 0.6, text=f"0{i+1}", size=28, color=LAV, bold=True, align=PP_ALIGN.RIGHT)
    box(s, x + 0.18, y + 1.0, 2.7, 0.36, text=h, size=16, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.18, y + 1.34, 2.7, 0.26, text=sub, size=10.5, color=MUTE)
    box(s, x + 0.18, y + 1.56, 2.7, 0.24, text=rng, size=9.5, color=PRIMARY, bold=True)


# ================================================================ 3. problem
s = std("The Problem We Solve", "Code findings stop at the commit. Risk keeps moving to production.", """
Talk track. A code scanner sees the source. After the commit, the application becomes an IaC template, an image and a running pod. It also lives in a cloud account, a data store and a live API. Each stage adds risk that a source scan does not see.
Risks shown, each from a help page:
IaC: public buckets and hardcoded secrets (docs/use-cases/iac-scan.md, docs/support-matrix/iac.md).
CI/CD: vulnerable base images, for example node:18-alpine blocked in GitHub Actions (docs/use-cases/container-scan.md).
Runtime: execution from /tmp and crypto-mining, both POC scenarios (references/technical-reference/playbooks-and-poc/accuknox-container-security-poc-cwpp-kspm.pdf).
Cloud: misconfiguration and drift (docs/use-cases/cloud-misconfigurations.md).
Data: PII and PCI data in exposed buckets (docs/getting-started/dspm-overview.md).
APIs: Shadow, Zombie and Orphan APIs and unauthenticated endpoints (docs/use-cases/api-security.md).
Callout source: accuknox.com/differentiators, "Tracks every finding from first commit to live production".
""")
dg(s, "problem", CX, 1.2, CW)
callout(s, CX, 4.18, CW, 0.62, "route",
        "AccuKnox tracks each finding from the first commit to live production, in one console.", size=13)


# ================================================================ 4. container + IaC
s = std("Container Security and IaC", "Scan in the pipeline, block at runtime, rank CVEs by what really executes", """
Sources.
KubeArmor blocks inline with AppArmor, BPF-LSM and SELinux, before the process runs (docs/faqs/runtime-security.md). KubeArmor is a CNCF Sandbox project, 2M+ downloads (docs/faqs/general.md).
Runtime Verified flag: eBPF telemetry flags vulnerabilities that actually execute in production, CVE noise down by up to 100x (docs/getting-started/3.4-release.md).
Registries, 8: ECR, GAR, ACR, Nexus, Docker Hub, Harbor, Quay, JFrog (docs/support-matrix/registry.md).
CI/CD, 10: GitHub Actions, GitLab, Jenkins, Azure DevOps, AWS CodePipeline, Bitbucket, CircleCI, GCP Cloud Build, Harness, Bamboo (docs/support-matrix/cicd-support-matrix.md). Harness plugins are listed as Coming Soon.
IaC, 13 formats: Terraform HCL, JSON and Plan, Kubernetes YAML, Helm, Dockerfile, CloudFormation, Kustomize, Serverless Framework, Ansible, Bicep, ARM, AWS CDK (docs/support-matrix/iac.md). Finds misconfigurations, hardcoded secrets and drift.
KSPM is agentless: CIS Kubernetes benchmark, KIEM, Pod Security Admission (docs/use-cases/kspm.md).
Admission control: KnoxGuard on Kyverno restricts registries and denies privileged pods. Blocking by vulnerability threshold is in the pipeline, so do not promise it (docs/use-cases/admission-controller-knoxguard.md).
Screenshots: Container Images dashboard and IaC Findings dashboard, demo tenant data (references/PRODUCT UI/1_dashboard).
""")
items = [("shield-lock", "Inline runtime blocking", "KubeArmor stops the attack before the process runs"),
         ("target", "Runtime Verified CVEs", "Flags CVEs that execute in production, up to 100x less noise"),
         ("package", "Registry and CI/CD scans", "8 registries and 10 CI/CD platforms"),
         ("file-code", "IaC scanning in 13 formats", "Terraform, Helm, CloudFormation and more"),
         ("list-check", "Agentless KSPM", "CIS Kubernetes benchmark, KIEM, Pod Security")]
for i, (icn, h, sub) in enumerate(items):
    row(s, CX, 1.24 + i * 0.76, 4.35, icn, h, sub)
shot(s, "container.png", 4.95, 1.2, 4.65, 1.62, None)
shot(s, "iac.png", 4.95, 2.92, 4.65, 1.62, None)
logos(s, ["kubernetes-original", "docker-original", "helm-original", "terraform-original",
          "github-original", "gitlab-original", "jenkins-original", "si-harbor"], 5.12, 4.72, 0.4, 0.17)


# ================================================================ 5. CSPM
s = std("Cloud Security Posture (CSPM)", "Agentless, read-only posture and compliance across every cloud account", """
Sources.
40+ compliance frameworks: accuknox.com/differentiators. The compliance matrix lists 42 rows (docs/support-matrix/compliance-matrix.md). Older pages say 30+ or 33+.
1,500+ policies and 50+ asset types: CSPM POC prerequisites guide (references/technical-reference/playbooks-and-poc/cspm-poc-prereq.pdf). These two figures appear only in that guide.
Agentless onboarding through cloud APIs with read-only access. AWS uses ReadOnlyAccess plus SecurityAudit (docs/faqs/cspm.md).
Asset inventory with list and hierarchy views (docs/use-cases/asset-inventory.md).
Misconfiguration and drift against baselines, Monitors on critical assets (docs/use-cases/cloud-misconfigurations.md).
Compliance Summary with pass percentage per control and a Detailed View (docs/use-cases/compliance.md).
Tickets: Jira, Freshservice, ConnectWise (docs/faqs/cspm.md). GitOps pull requests for IaC-managed resources (docs/faqs/compliance.md).
Clouds: AWS, Azure and GCP (docs/faqs/cspm.md). Oracle Cloud is listed in docs/support-matrix/public-cloud.md.
Screenshot: CSPM Report dashboard, demo tenant data.
""")
stat(s, CX, 1.2, 1.42, "40+", "Compliance frameworks", nsize=24, lsize=10)
stat(s, CX + 1.53, 1.2, 1.42, "1,500+", "Policies and controls", nsize=24, lsize=10)
stat(s, CX + 3.06, 1.2, 1.42, "50+", "Cloud asset types", nsize=24, lsize=10)
shot(s, "cspm.png", CX, 2.5, 4.48, 1.6, None)
logo_row(s, [("amazonwebservices-original-wordmark", "AWS"), ("azure-original", "Azure"),
             ("googlecloud-original", "GCP"), ("oracle-original", "Oracle")], CX, 4.28, 4.48, size=0.42)
items = [("cloud-lock", "Agentless onboarding", "Read-only cloud APIs. AWS uses ReadOnlyAccess and SecurityAudit"),
         ("list-details", "One asset inventory", "List and hierarchy views across all clouds"),
         ("alert-triangle", "Misconfig and drift", "Checks against baselines, Monitors on critical assets"),
         ("certificate", "Compliance per control", "Pass rate per control, drill-down per framework"),
         ("git-pull-request", "Tickets and fixes", "Jira, Freshservice, ConnectWise. GitOps pull requests")]
for i, (icn, h, sub) in enumerate(items):
    row(s, 5.1, 1.22 + i * 0.78, 4.5, icn, h, sub)


# ================================================================ 6. DSPM
s = std("Data Security Posture (DSPM)", "Find sensitive data where it lives. The scanner stays in your region.", """
Sources, all docs/getting-started/dspm-overview.md unless noted.
Scanner runs as a VM with systemd timers, a Kubernetes CronJob (IRSA or workload identity), or an event-driven AWS Lambda. Read-only, no write path, no inbound ports. Only a findings file leaves.
283 data classes: 117 regional, 114 credentials and secrets, 21 PHI, 19 PII, 10 financial. 282 of the 283 map to regulations. 62 country packs.
Confidence tiers: Very likely, Likely, Possible.
Matched values masked to the last four characters. Rows and files discarded after classification.
Frameworks: GDPR (78 classes), PCI DSS (107), HIPAA (26), DPDP (17), CCPA and others. Each class cites CWE and MITRE ATT&CK.
Sources: AWS S3, RDS and Aurora, DocumentDB, DynamoDB (event-driven only), Secrets Manager. Azure Blob, ADLS Gen2, Azure Database for PostgreSQL and MySQL, Azure SQL, Cosmos DB, Key Vault. Self-managed PostgreSQL, MySQL, MariaDB, SQL Server, MongoDB. SaaS: Google Workspace Drive, Salesforce.
Not supported per the same page: Google Cloud Storage, SMB and NFS, Oracle, Snowflake. Do not use the DSPM arch-diagram.png in PRODUCT UI, because it shows those sources.
Findings UI: severity, SLA, Create Ticket, Ask AI (docs/getting-started/dspm-onboarding.md).
Screenshot: DSPM dashboard, demo tenant data.
""")
items = [("scan", "Scanner in your region", "VM, Kubernetes CronJob or Lambda. Read-only, no inbound ports"),
         ("fingerprint", "PII, PHI, PCI and secrets", "Each finding has a confidence tier"),
         ("eye-off", "Values stay masked", "Last 4 characters only. Rows discarded after classification"),
         ("gavel", "Mapped to regulations", "GDPR, PCI DSS, HIPAA, CCPA, DPDP, with CWE and MITRE")]
for i, (icn, h, sub) in enumerate(items):
    row(s, CX, 1.26 + i * 0.86, 4.3, icn, h, sub, h=0.8)
shot(s, "dspm.png", 4.92, 1.2, 4.68, 1.78, None)
stat(s, 4.92, 3.12, 1.5, "283", "Data classes", nsize=22, lsize=10, h=0.9)
stat(s, 6.51, 3.12, 1.5, "62", "Country packs", nsize=22, lsize=10, h=0.9)
stat(s, 8.10, 3.12, 1.5, "282", "Mapped to rules", nsize=22, lsize=10, h=0.9)
label(s, 4.92, 4.17, 4.68, "DATA SOURCES")
logos(s, ["amazonwebservices-original-wordmark", "azure-original", "postgresql-original",
          "mysql-original", "mongodb-original"], 4.95, 4.47, 0.44, 0.22)
box(s, 8.16, 4.47, 1.44, 0.44, text="+ Salesforce,\nGoogle Drive", size=9.5, color=MUTE, anchor=MSO_ANCHOR.MIDDLE, ml=0)


# ================================================================ 7. API security
s = std("API Security", "Discover every live endpoint, then rank it by data, auth and exposure", """
Sources.
Live inventory: method, path, request and response bodies, sensitive data labels, internal and external calls (docs/use-cases/api-security.md).
Classifies Shadow, Zombie, Orphan and Active APIs against an uploaded OpenAPI spec (docs/use-cases/api-security.md). Spec files up to 3 MB (docs/how-to/api-security-onboarding.md).
Generates an OpenAPI spec from observed traffic (docs/getting-started/3.4-release.md).
API Scan collector, under Web Application DAST Scan, runs active tests on a live target URL (docs/how-to/api-security-onboarding.md).
Risk score by authentication, sensitive data, exposure and API category (docs/faqs/api-sec.md).
Rate limiting per user or IP per endpoint, per user or IP globally, and global (docs/use-cases/api-security.md).
Traffic sources with guides: AWS API Gateway, Kubernetes API proxy (SentryFlow), Istio sidecar and gateway, NGINX Ingress, Kong, F5 BIG-IP (docs/integrations/api-*.md, f5.md, kong.md).
Do not claim eBPF API capture. The 3.5 release notes list the API Security eBPF Collector as in progress.
OWASP API Top 10 coverage appears only in the FAQ (docs/faqs/api-sec.md Q12). Use it as a talking point, not a slide claim.
Unit: 50 endpoints, priced on unique endpoints, not traffic (docs/faqs/api-sec.md Q11).
Screenshot: API inventory, demo tenant data.
""")
shot(s, "api.png", CX, 1.2, 5.0, 2.27, None)
label(s, CX, 3.62, 5.0, "TRAFFIC SOURCES WITH SETUP GUIDES")
logo_row(s, [("amazonwebservices-original-wordmark", "API Gateway"), ("kubernetes-original", "K8s proxy"),
             ("si-istio", "Istio"), ("nginx-original", "NGINX")], CX, 3.92, 3.6, size=0.4, label_size=9.5)
box(s, 4.05, 3.92, 1.35, 0.7, text="+ Kong,\nF5 BIG-IP", size=10.5, color=MUTE, anchor=MSO_ANCHOR.MIDDLE, ml=0)
callout(s, CX, 4.74, 5.0, 0.48, "currency-dollar",
        "Priced on unique endpoints, not traffic. 1 unit is 50 endpoints.", size=11.5)
items = [("search", "Discover every endpoint", "Method, path, bodies, sensitive data labels"),
         ("eye-off", "Shadow and zombie APIs", "Shadow, Zombie, Orphan, Active, against your spec"),
         ("file-code", "Spec from traffic", "Generates an OpenAPI spec from live calls"),
         ("bug", "Active API tests", "Tests a live target URL for vulnerabilities"),
         ("chart-bar", "Risk score per API", "Auth, sensitive data, exposure, category")]
for i, (icn, h, sub) in enumerate(items):
    row(s, 5.62, 1.22 + i * 0.78, 3.98, icn, h, sub)


# ================================================================ 8. technical architecture
s = std("Technical Architecture", "Partner findings enter by SARIF or API and get the same correlation as native ones", """
Walk left to right.
1 Sources. Code scanners export SARIF. AccuKnox imports SARIF from any tool that produces it (docs/getting-started/sarif-findings.md, Universal SARIF Parser in docs/getting-started/3.4-release.md). Checkmarx and Nessus already connect by API (docs/getting-started/accuknox-arch.md).
2 Collect. CLI-based collectors cover secret scanning, SAST, container and vulnerability scanning, DAST and the Kubernetes CIS benchmark. KubeArmor is the only runtime agent. CSPM, CDR and KSPM are agentless (accuknox-control-plane-architecture-review-v3.5.txt).
3 Control plane. Triage dedupes, correlates and enriches. Prioritization uses AI risk scoring (docs/faqs/general.md Q14). Runtime Verified, CISA KEV and EPSS enrich CVEs (docs/getting-started/3.4-release.md). The rules engine raises tickets and notifications (docs/getting-started/accuknox-arch.md). Finding lifecycle: Active, Waiting for Verification, Fixed after 3 scans (docs/how-to/findings-lifecycle.md).
4 Act. Ticketing: Jira Cloud, Jira Server, ServiceNow, Freshservice, ServiceDesk Plus, ConnectWise. SIEM: Splunk, QRadar, Sentinel, CloudWatch, RSyslog, webhook. Notification: Slack, email, webhook (docs/integrations/support-matrix.md).
Integration build times from docs/getting-started/accuknox-arch.md: CLI-based 1 sprint, API-based 2 to 3 weeks, SIEM 1 sprint, ticketing (two-way) 3 to 5 sprints.
""")
dg(s, "architecture", CX, 1.18, CW)


# ================================================================ 9. deployment architecture
s = std("Deployment Architecture", "Posture scans need no agent. Only runtime enforcement runs one.", """
Where each component runs.
Kubernetes: KubeArmor DaemonSet and the KSPM job, both installed by Helm (accuknox-control-plane-architecture-review-v3.5.txt, docs/how-to/cluster-onboarding.md).
CI/CD: image and IaC scans run as pipeline steps. SARIF files upload from the pipeline (docs/support-matrix/cicd-support-matrix.md, docs/getting-started/sarif-findings.md).
Cloud accounts: agentless, read-only. AWS role uses ReadOnlyAccess plus SecurityAudit (docs/faqs/cspm.md).
Data region: DSPM scanner as a VM or Kubernetes CronJob, read-only, no inbound ports (docs/getting-started/dspm-overview.md).
API gateways: AWS API Gateway, Istio, NGINX Ingress, Kong, F5 BIG-IP connectors (docs/integrations).
Control plane: runs on Kubernetes. Data arrives through token-authenticated APIs (docs/getting-started/accuknox-arch.md).
Runtime enforcement keeps working if the control plane goes down (docs/faqs/deployment.md Q3, docs/faqs/general.md Q16).
""")
dg(s, "deploy_arch", CX, 1.2, CW)
callout(s, CX, 4.66, CW, 0.52, "shield-check",
        "The same components install for SaaS, your cloud, on-premises and air-gapped.", size=12)


# ================================================================ 10. deployment modes
s = std("Deployment Modes", "Run AccuKnox as SaaS, in your cloud, on-premises or air-gapped", """
Source: accuknox.com/differentiators, section "Your Cloud. Your data. Your AI.", read 2026-10-03.
Line from the page: Run AccuKnox as SaaS, in your cloud, on premise or air-gapped. The Platform and the policies stay the same.
SaaS: control plane in AccuKnox cloud. Setup the same day, no install. Best for a fast proof of concept. SaaS regions: US, EU, Middle East, India (docs/faqs/deployment.md Q10).
Your Cloud: control plane in your cloud account. Data egress none. Best for data residency. Managed Kubernetes: EKS, AKS, GKE (docs/getting-started/onprem-eks-aks-gke.md).
On-Premises: control plane on your servers. Native install, not a SaaS agent. Best for banking, healthcare, telecom. Single node: 8 vCPU, 32 GB, 256 GB disk (docs/getting-started/on-prem-single-node-installation.md). Multi-node: 3 nodes (docs/getting-started/on-prem-installation-guide.md).
Air-Gapped: control plane in your isolated network. Outbound traffic none. Best for federal, defense, ITAR. All modules stay available (docs/faqs/general.md Q16).
AI CoPilot (AskADA) is SaaS only (docs/getting-started/deployment-models.md).
Pricing: the sample quote says pricing is the same for on-premises and cloud deployment (Pricing and Sizing sheet, SEP 2026).
""")
dg(s, "modes", CX, 1.18, CW)
modes = [("SaaS", PRIMARY, [("Control plane", "AccuKnox cloud"), ("Setup", "Same day, no install"), ("Best for", "Fast proof of concept")]),
         ("Your Cloud", PRIMARY, [("Control plane", "Your cloud account"), ("Data egress", "None"), ("Best for", "Data residency")]),
         ("On-Premises", PRIMARY, [("Control plane", "Your servers"), ("Install", "Native, no SaaS agent"), ("Best for", "Banking, healthcare, telecom")]),
         ("Air-Gapped", RED, [("Control plane", "Isolated network"), ("Outbound traffic", "None"), ("Best for", "Federal, defense, ITAR")])]
k = CW / 1280.0
for i, (name, col, facts) in enumerate(modes):
    x = CX + (10 + i * 320) * k
    w = 296 * k
    box(s, x, 3.04, w, 0.34, text=name, size=14, color=col, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0.04)
    box(s, x, 3.4, w, 1.52, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    for j, (lab, val) in enumerate(facts):
        box(s, x + 0.1, 3.44 + j * 0.44, w - 0.2, 0.2, text=lab, size=9.5, color=MUTE, ml=0, mt=0, mb=0)
        box(s, x + 0.1, 3.62 + j * 0.44, w - 0.2, 0.24, text=val, size=11.5, color=NAVY, bold=True, ml=0, mt=0, mb=0)
callout(s, CX, 4.98, CW, 0.36, "currency-dollar",
        "The platform, the policies and the price stay the same in all four modes.", size=12)


# ================================================================ 11. use cases
s = std("Use Cases", "Six scenarios, each taken from an AccuKnox help page", """
Sources.
1 Container: GitHub Actions scan blocks the vulnerable node:18-alpine image (docs/use-cases/container-scan.md).
2 IaC: IaC scan flags a Terraform S3 bucket set to public-read (docs/use-cases/iac-scan.md).
3 CSPM: misconfigured public S3 bucket walkthrough (docs/use-cases/cloud-misconfigurations.md). Auto-remediation can close public S3 access (docs/faqs/compliance.md).
4 DSPM: point the scanner at a read replica of a production database, then filter findings by framework (docs/getting-started/dspm-onboarding.md, dspm-overview.md).
5 API: upload a spec, run a scan, get Shadow and Orphan endpoints (docs/how-to/api-security-onboarding.md, Path 1).
6 Partner findings: SARIF import from any tool, grouped and filtered by severity, tool name and file location, next to native findings (docs/getting-started/sarif-findings.md).
""")
cards = [("container", "Block a vulnerable image", "A GitHub Actions scan stops node:18-alpine before release", "Container"),
         ("file-code", "Catch a public bucket in IaC", "The IaC scan flags a Terraform bucket set to public-read", "IaC"),
         ("cloud", "Close a public S3 bucket", "CSPM finds the bucket. Remediation closes public access", "CSPM"),
         ("database", "Find PCI data before an audit", "Scan a database replica, then filter by framework", "DSPM"),
         ("api", "Expose shadow APIs", "Upload a spec, scan, and list Shadow and Orphan APIs", "API Security"),
         ("file-search", "One view for partner findings", "Import SARIF from any tool next to native findings", "Platform")]
for i, (icn, h, b, tag) in enumerate(cards):
    x = CX + (i % 3) * 3.1
    y = 1.22 + (i // 3) * 2.0
    box(s, x, y, 3.0, 1.86, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    icon_tile(s, icn, x + 0.14, y + 0.16, 0.52)
    box(s, x + 0.78, y + 0.12, 2.12, 0.62, text=h, size=12.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.16, y + 0.82, 2.7, 0.66, text=b, size=11, color=MUTE, ml=0)
    pill(s, x + 1.68, y + 1.5, 1.2, 0.26, tag, fill=LAV, tcolor=NAVY, size=9.5)


# ================================================================ 12. POC
s = std("POC Scenarios", "A five-day SaaS POC, with one pass check per product", """
Timeline sources.
Five-day plan: Day 1 onboarding, Days 2 and 3 scan results, Days 3 and 4 asset inventory, Days 4 and 5 findings categorization (docs/faqs/general.md Q19).
Duration: SaaS POC about 1 to 2 weeks, on-prem POC about 2 to 3 weeks, longer for air-gapped (docs/faqs/deployment.md Q7). The FAQ links a POC Checklist Questionnaire.
Scenario sources.
Container: block execution from /tmp and crypto-mining, from the CWPP and KSPM POC guide (references/technical-reference/playbooks-and-poc/accuknox-container-security-poc-cwpp-kspm.pdf). Policies start in audit mode and switch to block (docs/use-cases/cwpp.md).
CSPM: top 20 misconfigurations ranked by Day 3, public S3 bucket reverted within 60 seconds, from the 2-week CSPM POC sprint (references/technical-reference/playbooks-and-poc/cspm-poc-prereq.pdf).
DSPM: scope S3 by tag or name pattern, include public buckets, triage Critical findings first (docs/getting-started/dspm-onboarding.md).
API: Path 1 in docs/how-to/api-security-onboarding.md, upload a spec and scan.
The help docs define no formal POC success criteria. The pass checks come from the POC guides above. Agree final criteria with Veracode before Day 1.
""")
steps = [("plug-connected", "Day 1", "Onboard"), ("scan", "Days 2 to 3", "Scan results"),
         ("list-details", "Days 3 to 4", "Asset inventory"), ("filter", "Days 4 to 5", "Findings by category")]
for i, (icn, d, t) in enumerate(steps):
    x = CX + i * 1.82
    icon_tile(s, icn, x, 1.24, 0.5)
    box(s, x + 0.6, 1.2, 1.2, 0.28, text=d, size=10, color=PRIMARY, bold=True, ml=0)
    box(s, x + 0.6, 1.46, 1.2, 0.3, text=t, size=11.5, color=NAVY, bold=True, ml=0)
    if i < 3:
        arrow(s, x + 1.56, 1.36, 0.24, 0.26)
pill(s, 7.75, 1.22, 1.85, 0.27, "SaaS: 1 to 2 weeks", size=10)
pill(s, 7.75, 1.55, 1.85, 0.27, "On-prem: 2 to 3 weeks", fill=LAV, tcolor=NAVY, size=10)
scen = [("container", "Container", "Run /tmp execution and a crypto-miner under a block policy", "Both processes blocked"),
        ("cloud", "CSPM", "Onboard read-only, then make one S3 bucket public", "Top 20 ranked by Day 3. Bucket reverted in 60 s"),
        ("database", "DSPM", "Scope S3 by tag, include public buckets", "PII and PCI findings per bucket"),
        ("api", "API Security", "Upload an OpenAPI spec and connect a gateway", "Shadow and Orphan APIs listed")]
for i, (icn, h, test, ok) in enumerate(scen):
    x = CX + i * 2.33
    box(s, x, 2.06, 2.2, 3.1, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    icon_tile(s, icn, x + 0.14, 2.2, 0.5)
    box(s, x + 0.74, 2.2, 1.4, 0.5, text=h, size=13, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    label(s, x + 0.14, 2.82, 1.9, "TEST", size=9.5)
    box(s, x + 0.14, 3.06, 1.95, 0.9, text=test, size=11, color=INK, ml=0)
    box(s, x + 0.1, 4.02, 2.0, 1.04, fill=GREEN_LT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    label(s, x + 0.2, 4.06, 1.8, "PASS CHECK", size=9.5, color=GREEN_DK)
    box(s, x + 0.2, 4.3, 1.82, 0.72, text=ok, size=11, color=GREEN_DK, bold=True, ml=0)


# ================================================================ 13. user journey
s = std("User Journey in the Console", "Six screens take a team from a new source to a ticket", """
Screens from references/PRODUCT UI, demo tenant data. Doc pages for each step:
1 Add a collector: SAST, DAST, host, image and cloud collectors (docs/how-to/sca.md). The picker shows SonarQube, Zap, Nessus, Trivy.
2 Dashboard: accounts, clusters, registries and repos in one view (docs/use-cases/cnapp-security-overview.md).
3 Inventory and security graph (docs/use-cases/asset-inventory.md).
4 Findings: filter by cloud, status, severity, exploit availability, then group and assign (docs/how-to/findings-lifecycle.md).
5 Compliance: average score and passed controls per framework and account (docs/use-cases/compliance.md).
6 Reports: scheduled CSPM, CWPP and ASPM reports (docs/how-to/custom-reports.md). Tickets go to Jira through the rules engine (docs/use-cases/rules-engine-ticket-creation.md).
Ask AI is available on findings (docs/getting-started/3.3-release.md). The Ask AI screenshot shows a user name, so it stays out of the deck.
""")
jr = [("j_collectors.png", "Add a source", "Collectors for SAST, DAST, images, clouds"),
      ("j_dashboard.png", "See the posture", "Accounts, clusters, registries, repos"),
      ("j_graph.png", "Walk the assets", "Security graph per cloud asset"),
      ("j_issues.png", "Rank the findings", "Filter by severity, exploit, status"),
      ("j_compliance.png", "Score compliance", "Score per framework and account"),
      ("j_reports.png", "Report and ticket", "Scheduled reports, Jira tickets")]
for i, (pic, h, sub) in enumerate(jr):
    x = CX + (i % 3) * 3.1
    y = 1.2 + (i // 3) * 2.02
    shot(s, pic, x, y, 3.0, 1.32, None)
    box(s, x, y + 1.4, 0.36, 0.36, text=str(i + 1), size=12, color=WHITE, bold=True, fill=PRIMARY,
        shape=MSO_SHAPE.OVAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0, mt=0, mb=0)
    box(s, x + 0.44, y + 1.36, 2.56, 0.26, text=h, size=12, color=NAVY, bold=True, ml=0)
    box(s, x + 0.44, y + 1.6, 2.56, 0.24, text=sub, size=10, color=MUTE, ml=0)


# ================================================================ 14. differentiators
s = std("Key Differentiators", "Prevention first, one data layer, and any deployment", """
Sources.
Stats: 3 to 5x tools replaced, 80% alert reduction, 40+ frameworks (accuknox.com/differentiators). The page says runtime context cuts actionable findings by up to 80 percent.
Inline prevention: blocks threats before execution, zero trust at the kernel level through eBPF (accuknox.com/differentiators). KubeArmor uses AppArmor, BPF-LSM and SELinux (docs/faqs/runtime-security.md).
Code to cloud: every finding tracked from commit to production (accuknox.com/differentiators).
One data layer: CNAPP, API Security and AI Security share one data layer. Start with one module and expand without re-integration (accuknox.com/differentiators).
Runs anywhere: public, private, on-prem and edge from one console. Air-gapped with no telemetry and no call-home (accuknox.com/differentiators). The narrative file calls AccuKnox the only vendor that runs on all public, private and air-gapped clouds (references/source-of-truth/accuknox-summary-and-narrative.md).
Open formats: SARIF, syslog, CEF and MCP connect whole tool categories (docs/integrations/support-matrix.md).
Open source: AccuKnox created and maintains KubeArmor, 2M+ downloads, 1,000+ GitHub stars (docs/faqs/general.md).
""")
stat(s, CX, 1.2, 2.96, "3 to 5x", "Tools replaced", nsize=26, lsize=10.5, h=1.0)
stat(s, CX + 3.12, 1.2, 2.96, "80%", "Alert reduction with runtime context", nsize=26, lsize=10.5, h=1.0)
stat(s, CX + 6.24, 1.2, 2.96, "40+", "Compliance frameworks out of the box", nsize=26, lsize=10.5, h=1.0)
diffs = [("shield-lock", "Inline prevention", "Blocks threats before they run, at the kernel"),
         ("route", "Code to cloud", "Tracks each finding from commit to production"),
         ("stack-2", "One data layer", "Add a module with no re-integration"),
         ("world", "Runs anywhere", "Public, private, on-prem, air-gapped"),
         ("file-search", "Open formats", "SARIF, syslog, CEF and webhooks"),
         ("code", "Open source core", "KubeArmor, 2M+ downloads")]
for i, (icn, h, b) in enumerate(diffs):
    x = CX + (i % 3) * 3.12
    y = 2.36 + (i // 3) * 1.42
    icon_card(s, x, y, 2.96, 1.3, icn, h, b, hsize=13, bsize=11)


# ================================================================ 15. stack ranking
s = std("Stack Ranking for Veracode", "Recommended order to add the four modules next to code findings", """
This is AccuKnox's recommended order for a code-scanning partner. It is not a third-party ranking.
Order logic: start in the pipeline, where code findings already flow. Next come the live endpoints the code becomes. Then add the cloud the code deploys into, and last the data behind the application.
Footprint sources: CI plugins and Helm agent (docs/support-matrix/cicd-support-matrix.md, docs/how-to/cluster-onboarding.md). API gateway connectors (docs/integrations). Agentless read-only CSPM (docs/faqs/cspm.md). DSPM scanner in region (docs/getting-started/dspm-overview.md).
Unit sources: Pricing and Sizing sheet SEP 2026, Step 1 units calculator. CWPP and KSPM 1 node per unit. Container images 40 images per unit. SAST, secret scanning and IaC 30 code repos per unit. API Security 50 endpoints per unit. CSPM 10 assets per unit.
The sheet has no unit divisor for DSPM. The Cloud SKU tab counts bucket, data warehouse and PaaS DB scans per month. Sales to confirm the DSPM unit.
Website line: Start with one module and expand without re-integration (accuknox.com/differentiators).
""")
rows = [["Rank", "Module", "Why in this order", "Footprint", "1 unit"],
        ["1", "Container + IaC", "Runs in the same pipelines as code scans", "CI plugin, Helm agent", "1 node, 40 images, 30 repos"],
        ["2", "API Security", "Tests the live endpoints the code becomes", "Gateway connector", "50 endpoints"],
        ["3", "CSPM", "Checks the cloud the code deploys into", "Agentless, read-only", "10 assets"],
        ["4", "DSPM", "Finds the sensitive data behind the app", "Scanner in your region", "[Sales to confirm]"]]
t = table(s, CX, 1.24, CW, 3.0, rows, colw=[0.7, 1.75, 3.25, 1.8, 1.7], hsize=11.5, bsize=11,
          aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])
for r in range(1, 5):
    for c in (0,):
        cell = t.cell(r, c)
        cell.fill.solid(); cell.fill.fore_color.rgb = PRIMARY
        for p in cell.text_frame.paragraphs:
            for rn in p.runs:
                rn.font.color.rgb = WHITE; rn.font.size = Pt(16)
cell = t.cell(4, 4)
for p in cell.text_frame.paragraphs:
    for rn in p.runs:
        rn.font.color.rgb = RED
callout(s, CX, 4.5, CW, 0.62, "stack-2",
        "Start with one module. Add the next one on the same data layer, with no re-integration.", size=12.5)


# ================================================================ 16. pricing
s = std("Pricing", "One unit price across modules, with volume tiers", """
Source: AccuKnox - Pricing and Sizing - SEP 2026.xlsx, effective August 2026.
Step 2, tiered price per unit per month in USD: Tier 1, 10 to 50 units, 40 dollars. Tier 2, 51 to 250, 34 dollars. Tier 3, 251 to 750, 29 dollars. Tier 4, 751 to 2,500, 25 dollars. Tier 5, 2,501 to 5,000, 21 dollars. Tier 6, 5,001 and up, negotiated. Tier decay 15 percent. INR prices are on the same tab.
Step 1, units: CSPM and CDR 10 assets per unit. CWPP, KSPM and KIEM 1 node per unit. Container image scanning 40 images per unit. SAST, secret scanning and IaC 30 code repos per unit. API Security 50 endpoints per unit.
Step 3, support: Silver included, 9 hours x 5 days. Gold 10 percent of subscription, 12 x 6. Platinum 25 percent, 24 x 7 with a TAM.
Step 5, deployment: On-premises 0 dollars. Shared tenant SaaS 0 dollars. Dedicated tenant 3,000 dollars a month plus 10 percent of subscription.
Professional services: 250 dollars an hour onsite, 125 offsite.
Sample quote terms: 3-year subscription, Net 30, implementation 15 to 45 days from contract.
DSPM has no unit divisor in the sheet. Sales to confirm before this slide goes to Veracode.
""")
label(s, CX, 1.18, 4.3, "PRICE PER UNIT PER MONTH (USD)")
tiers = [["Tier", "Units", "Price"], ["1", "10 to 50", "$40"], ["2", "51 to 250", "$34"],
         ["3", "251 to 750", "$29"], ["4", "751 to 2,500", "$25"], ["5", "2,501 to 5,000", "$21"],
         ["6", "5,001 and up", "Negotiated"]]
table(s, CX, 1.46, 4.3, 2.66, tiers, colw=[0.8, 2.0, 1.5], hsize=11, bsize=11,
      aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT])
label(s, 4.95, 1.18, 4.65, "WHAT ONE UNIT COVERS")
units = [["Module", "1 unit equals"], ["CSPM", "10 cloud assets"], ["CWPP and KSPM", "1 node"],
         ["Container images", "40 images"], ["IaC, SAST, secrets", "30 code repos"],
         ["API Security", "50 endpoints"]]
table(s, 4.95, 1.46, 4.65, 2.28, units, colw=[2.25, 2.4], hsize=11, bsize=11)
todo_panel(s, 4.95, 3.8, 4.65, 0.52, "DSPM unit", "Not in the sheet. Sales to confirm.", size=10.5)
label(s, CX, 4.42, 1.3, "SUPPORT", size=9.5)
for i, t1 in enumerate(["Silver: included, 9x5", "Gold: +10%, 12x6", "Platinum: +25%, 24x7"]):
    pill(s, CX + 1.35 + i * 2.62, 4.42, 2.5, 0.3, t1, fill=LAV, tcolor=NAVY, size=10)
label(s, CX, 4.8, 1.3, "DEPLOYMENT", size=9.5)
for i, t1 in enumerate(["On-premises: $0", "Shared SaaS: $0", "Dedicated: $3,000/mo + 10%"]):
    pill(s, CX + 1.35 + i * 2.62, 4.8, 2.5, 0.3, t1, fill=PRIMARY, size=10)
footer_note(s, "List prices from the AccuKnox Pricing and Sizing sheet, September 2026. Partner terms are separate.", y=5.12, size=9.5)


# ================================================================ 17. closing
closing_slide(prs)

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
