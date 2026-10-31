# -*- coding: utf-8 -*-
"""
Version 2 content for the four Veracode product decks: problem heroes, solution hubs,
outcome tiles and sourced stack-ranking scorecards. Imported after veracode_specs.py.

Scorecard sources:
  Container: accuknox.com/comparisons/red-hat-rhacs-vs-suse-neuvector-vs-accuknox and
             accuknox.com/comparisons/accuknox-vs-sysdig, read 2026-10-03. The pages give a
             value for every cell and do not link competitor docs.
  CSPM:      accuknox.com/comparisons/wiz-vs-prisma-cloud-vs-accuknox and
             accuknox.com/comparisons/accuknox-vs-orca-security, read 2026-10-03. Same caveat.
  DSPM:      comparison table in help.accuknox.com/getting-started/dspm-overview/, vendor
             facts from public documentation as of September 2026.
  API:       each competitor's own pages, read 2026-10-03 (URLs in the notes).
"""
from veracode_specs import CONTAINER, CSPM, DSPM, API

HUB = {
    "container": ["kubernetes-original", "docker-original", "helm-original", "terraform-original",
                  "github-original", "gitlab-original", "jenkins-original"],
    "cspm": ["amazonwebservices-original-wordmark", "azure-original", "googlecloud-original", "oracle-original",
             "jira-original", "slack-original"],
    "dspm": ["amazonwebservices-original-wordmark", "azure-original", "postgresql-original", "mysql-original",
             "mongodb-original"],
    "api": ["amazonwebservices-original-wordmark", "kubernetes-original", "si-istio", "nginx-original"],
}

# ------------------------------------------------------------------ container
CONTAINER["problem"].update(
    hero=dict(eyebrow="THE COST TODAY", big="100x", lines=["Up to 100x more CVE alerts", "than CVEs that really run"],
              source="help.accuknox.com, release 3.4"),
    cards2=[("bolt", "Attacks happen at runtime", ["Most tools only scan static", "posture before deploy"]),
            ("alert-octagon", "Kill comes too late", ["Post-exploit tools stop a process", "after it runs. Data may be gone"]),
            ("file-code", "Misconfig hides in YAML", ["Hardcoded passwords and privileged", "pods slip past code review"]),
            ("bug", "CVE noise buries real risk", ["Teams cannot tell which image", "CVEs actually execute"])],
    callout="AccuKnox scans the pipeline and the image, then blocks the attack inline at runtime.")
CONTAINER["overview"].update(
    kicker="Six capabilities, one agent, one console",
    title_lines=["Container", "Security + IaC"], hub_logos=HUB["container"],
    hub=[("shield-lock", "Inline runtime blocking", ["KubeArmor stops attacks", "before the process runs"]),
         ("sparkles", "Auto-discovered policy", ["Learns behavior, audits,", "then switches to block"]),
         ("target", "Runtime Verified CVEs", ["Ranks CVEs that execute,", "with KEV and EPSS"]),
         ("package", "Image and registry scans", ["8 registries, plus scans", "of running images"]),
         ("file-code", "IaC scanning", ["13 formats in 9 CI/CD tools,", "misconfig and secrets"]),
         ("list-check", "Agentless KSPM", ["CIS, STIG and KIEM checks,", "installed by Helm"])],
    outcomes=[("Block inline", "Before the attack runs"), ("Up to 100x", "Less CVE noise to triage"),
              ("1 Helm chart", "Per cluster, egress only")])
CONTAINER["ranking"] = dict(
    kicker="Who stops a container attack before it runs",
    vendors=["AccuKnox", "Red Hat ACS", "SUSE NeuVector", "Sysdig Secure"],
    rows=[("Blocks attacks before they run", [("yes", "Inline, kernel LSM"), ("no", "Kills pod after"),
                                              ("partial", "Network DPI only"), ("partial", "Alerts after activity")]),
          ("Process allow-list lockdown", [("yes", "Per binary, in kernel"), ("no", "Coarse, kills pod"),
                                           ("yes", "Per namespace rules"), ("partial", "Rule-based, coarser")]),
          ("One scanner for all registries", [("yes", "Public registries too"), ("yes", "ECR, ACR, GAR, Quay"),
                                              ("yes", "Inactive images too"), ("partial", "One per registry")]),
          ("Kubernetes identity risk (KIEM)", [("yes", "Overprivileged accounts"), ("no", "RBAC misconfig only"),
                                               ("no", "No KIEM module"), ("no", "No identity graph")]),
          ("Shadow API discovery", [("yes", "From live traffic"), ("no", "No API inspection"),
                                    ("no", "No API discovery"), ("partial", "Limited native")]),
          ("AI workload sandboxing", [("yes", "Ollama, vLLM, CUDA"), ("no", "No AI sandboxing"),
                                      ("no", "No AI sandboxing"), ("partial", "Infra posture only")])],
    callout="Only AccuKnox blocks inline at the kernel, before the attack executes.")
CONTAINER["links"]["ranking"] = [("AccuKnox vs RHACS vs NeuVector", "https://accuknox.com/comparisons/red-hat-rhacs-vs-suse-neuvector-vs-accuknox"),
                                 ("AccuKnox vs Sysdig", "https://accuknox.com/comparisons/accuknox-vs-sysdig")]
CONTAINER["notes"]["ranking"] = """
Sources: accuknox.com/comparisons/red-hat-rhacs-vs-suse-neuvector-vs-accuknox (RHACS, NeuVector) and accuknox.com/comparisons/accuknox-vs-sysdig (Sysdig), both read 2026-10-03. Icons follow each page's tick, dash and cross.
NeuVector: the page gives a tick for Threat Response (DPI blocking in Protect mode) and a cross for Preemptive Mitigation, merged here as Partial.
Sysdig registry: the page also gives Sysdig No for public registries.
The 102-feature battlecard agrees on the RHACS and NeuVector rows: AccuKnox 99.5 percent, RHACS 43.1 percent, NeuVector 49.0 percent (references/competitive/battlecards/accuknox-vs-rhacs-vs-neuvector-k8s-security.xlsx).
The live pages give a value for every cell but do not link competitor documentation. Before a public version, link each competitor cell to that vendor's own docs.
Admission control is Yes for AccuKnox, RHACS and NeuVector, so it shows no edge and is left off.
"""

# ------------------------------------------------------------------ cspm
CSPM["problem"].update(
    hero=dict(eyebrow="THE COST TODAY", big="60 h", lines=["of audit prep a quarter,", "across 200+ cloud accounts"],
              source="AccuKnox compliance FAQ, before AccuKnox"),
    cards2=[("alert-triangle", "Misconfig leads cloud risk", ["The NSA names misconfiguration", "the leading cloud vulnerability"]),
            ("layers-subtract", "Console sprawl", ["Teams switch between consoles", "to see their own assets"]),
            ("refresh", "Drift after deploy", ["Public buckets and public IPs", "appear after the change ships"]),
            ("clock", "Audit evidence goes stale", ["Point-in-time screenshots age", "before the auditor reads them"])])
CSPM["overview"].update(
    kicker="Six capabilities, read-only and agentless, across four clouds",
    title_lines=["Cloud Security", "Posture (CSPM)"], hub_logos=HUB["cspm"],
    hub=[("list-details", "One asset inventory", ["Accounts, assets, workloads", "across four clouds"]),
         ("alert-triangle", "Misconfig and drift", ["1,000+ checks against", "baselines, live Monitors"]),
         ("certificate", "Continuous compliance", ["40+ frameworks, scored", "per control"]),
         ("hierarchy-2", "Security Graph", ["Asset and finding edges", "with blast radius"]),
         ("bolt", "Detect and respond", ["Cloud audit events", "trigger automatic fixes"]),
         ("settings-automation", "Rules engine", ["Jira tickets open and", "close with the finding"])],
    outcomes=[("60 h to under 5 h", "Audit prep per quarter"), ("60 s", "Public S3 bucket reverted"),
              ("Read-only", "Agentless, four clouds")])
CSPM["ranking"] = dict(
    kicker="Who covers the clouds that SaaS-only tools cannot reach",
    vendors=["AccuKnox", "Wiz", "Prisma Cloud", "Orca Security"],
    rows=[("Air-gapped and on-prem", [("yes", "Full platform"), ("no", "SaaS only"),
                                      ("partial", "On-prem, with limits"), ("no", "No self-hosted plane")]),
          ("Private and hybrid cloud", [("yes", "OpenShift, Nutanix, Tanzu"), ("partial", "VMware vSphere only"),
                                        ("partial", "Partial coverage"), ("yes", "OpenShift, Nutanix")]),
          ("Blocks runtime attacks inline", [("yes", "Kernel-layer deny"), ("partial", "Detect and react"),
                                             ("no", "Cannot block file change"), ("no", "Detect and respond")]),
          ("Kernel-level hardening", [("yes", "MITRE and NIST policies"), ("no", "Detection rules only"),
                                      ("no", "Not offered"), ("partial", "Detection, no lockdown")]),
          ("Code to cloud, with DAST", [("yes", "SCA, SAST, DAST"), ("partial", "No DAST"),
                                        ("partial", "Limited SAST, no DAST"), ("partial", "SAST via partners")]),
          ("Imports partner findings", [("yes", "SARIF, open and commercial"), ("no", "Commercial tools only"),
                                        ("partial", "Proprietary tools only"), ("no", "No SARIF ingestion")])],
    callout="AccuKnox is the CSPM that also runs air-gapped, blocks inline and imports SARIF.")
CSPM["links"]["ranking"] = [("Wiz vs Prisma Cloud vs AccuKnox", "https://accuknox.com/comparisons/wiz-vs-prisma-cloud-vs-accuknox"),
                            ("AccuKnox vs Orca", "https://accuknox.com/comparisons/accuknox-vs-orca-security")]
CSPM["notes"]["ranking"] = """
Sources: accuknox.com/comparisons/wiz-vs-prisma-cloud-vs-accuknox (Wiz, and Prisma under the column label Palo Alto Cortex Cloud) and accuknox.com/comparisons/accuknox-vs-orca-security (Orca), both read 2026-10-03.
Private cloud for Orca comes from the row Private Cloud (OpenShift / Nutanix). Kernel hardening for Orca comes from Process-Level Allow/Deny Lockdown. Code to cloud merges the SAST and DAST rows. Partner findings uses the Integrations row.
The Prisma private cloud cell has no qualifier on the page, so it reads Partial coverage.
Veracode angle: the Imports partner findings row is where Veracode SARIF output lands next to cloud findings (help.accuknox.com/getting-started/sarif-findings/).
The live pages give a value for every cell but do not link competitor documentation. Before a public version, link each competitor cell to that vendor's own docs.
On KSPM and AI-SPM the Wiz page gives Wiz and Prisma Yes, so those rows are left off. Orca leads on DSPM on the Orca page, so DSPM rows are left off.
"""

# ------------------------------------------------------------------ dspm
DSPM["problem"].update(
    hero=dict(eyebrow="THE RISK TODAY", big="3 of 4", big_size=100,
              lines=["leading DSPM tools send", "metadata to their cloud"],
              source="Vendor docs, September 2026"),
    cards2=[("map-2", "No map of sensitive data", ["PII, PHI and card data spread", "across buckets, DBs and SaaS"]),
            ("cloud-off", "Data leaves to be scanned", ["Most DSPM tools move metadata", "outside your boundary"]),
            ("lock-open", "Exposed stores", ["Public or unencrypted stores", "hold regulated records"]),
            ("gavel", "Audits need evidence", ["GDPR, PCI DSS, HIPAA, DPDP", "ask where the data sits"])])
DSPM["overview"].update(
    kicker="Six capabilities, with a scanner that never leaves your region",
    title_lines=["Data Security", "Posture (DSPM)"], hub_logos=HUB["dspm"],
    hub=[("scan", "Read-only scanner", ["Runs in the data's region,", "no inbound ports"]),
         ("fingerprint", "283 data classes", ["PII, PHI, financial,", "secrets, 117 regional"]),
         ("target", "Confidence per finding", ["Very likely, Likely or", "Possible, floor Likely"]),
         ("eye-off", "Masked evidence", ["The console shows only", "the last 4 characters"]),
         ("gavel", "Regulation mapping", ["GDPR, PCI DSS, HIPAA,", "CCPA and DPDP"]),
         ("world", "Data residency view", ["Sensitive records", "mapped by region"])],
    outcomes=[("Findings only", "Leave your region"), ("62 countries", "Covered by data-class packs"),
              ("Air-gapped", "Console included")])
DSPM["ranking"] = dict(
    kicker="Where each DSPM scans, and what leaves your environment",
    vendors=["AccuKnox", "Cyera", "Varonis", "BigID"],
    rows=[("Scanner runs in your account", [("yes", "VM or CronJob, in region"), ("partial", "Vendor cloud or outpost"),
                                            ("partial", "Analysis in SaaS"), ("yes", "Local scanners")]),
          ("Console can run on-prem", [("yes", "On-prem or air-gapped"), ("no", "SaaS only"),
                                       ("no", "SaaS only"), ("yes", "Self-hosted on K8s")]),
          ("Nothing leaves your boundary", [("yes", "With on-prem console"), ("no", "Metadata and results"),
                                            ("no", "Collector metadata"), ("yes", "When self-hosted")]),
          ("Air-gapped operation", [("yes", "Console included"), ("no", "Not offered"),
                                    ("partial", "Offline collectors only"), ("partial", "Possible on your K8s")])],
    callout="AccuKnox is the only DSPM here that ships an air-gapped console.")
DSPM["links"]["ranking"] = [("DSPM comparison in the help docs", "https://help.accuknox.com/getting-started/dspm-overview/")]
DSPM["notes"]["ranking"] = """
Source: comparison table in help.accuknox.com/getting-started/dspm-overview/. Vendor facts come from public documentation as of September 2026.
Exact cells: Cyera scans in Cyera's cloud or an outpost cluster in your cloud, console is Cyera SaaS, metadata and results leave, no air-gapped mode. Varonis runs collectors in your environment with analysis in Varonis SaaS, console is SaaS, collector metadata leaves, offline collector installs only. BigID runs cloud scanners or local scanners, console is SaaS or self-hosted on your Kubernetes, nothing leaves when self-hosted, air-gapped possible on your own Kubernetes.
IBM Guardium DSPM is in the source table and left off here to keep the slide to three competitors. Its cells: analyzer in your cloud account, IBM SaaS console, metadata leaves, no air-gapped mode.
Varonis self-hosted ends 31 December 2026, per the same footnote.
"""

# ------------------------------------------------------------------ api
API["problem"].update(
    hero=dict(eyebrow="THE GAP TODAY", big="3", lines=["kinds of API your spec", "never shows: shadow,", "zombie and orphan"],
              source="AccuKnox API Security FAQ"),
    cards2=[("eye-off", "Shadow APIs", ["Debug hooks and forgotten", "routes that nobody monitors"]),
            ("history", "Zombie APIs", ["Old versions still take", "traffic, often with weaker auth"]),
            ("file-text", "Orphan specs", ["Documented endpoints that", "no longer exist mislead tests"]),
            ("network", "Blind east-west traffic", ["WAFs and perimeter tools", "miss internal service calls"])])
API["overview"].update(
    kicker="Six capabilities, built from live traffic with no code change",
    title_lines=["API", "Security"], hub_logos=HUB["api"],
    hub=[("search", "Live inventory", ["Method, path, bodies and", "sensitive data per call"]),
         ("eye-off", "Shadow, Zombie, Orphan", ["Live traffic compared", "with your OpenAPI spec"]),
         ("file-code", "Spec from traffic", ["Generates OpenAPI for", "undocumented services"]),
         ("fingerprint", "Sensitive data", ["PII, PHI and financial", "data in each response"]),
         ("bug", "Active API tests", ["The API Scan collector", "tests a live target URL"]),
         ("filter", "Rate limiting", ["Block or alert per", "endpoint, user or IP"])],
    outcomes=[("30 s", "From live traffic to inventory"), ("No code change", "Connectors at gateway or mesh"),
              ("Per endpoint", "Not per API call")])
API["ranking"] = dict(
    kicker="Discovery is table stakes. Deployment, testing and price decide it.",
    vendors=["AccuKnox", "Salt Security", "Traceable", "Akamai API Sec."],
    rows=[("Shadow and zombie discovery", [("yes", "Plus spec from traffic"), ("yes", "Spec drift, OAS compare"),
                                           ("yes", "Conformance analysis"), ("yes", "Spec vs traffic")]),
          ("API testing (DAST) included", [("yes", "API Scan collector"), ("partial", "Via partner DAST"),
                                           ("yes", "API Testing module"), ("partial", "Separate Active Testing")]),
          ("Native rate limiting", [("yes", "Block or alert"), ("partial", "Via WAF or gateway"),
                                    ("yes", "Rate-limit rules"), ("partial", "Needs App and API Protector")]),
          ("Self-hosted, air-gapped", [("yes", "On-prem and air-gapped"), ("partial", "Hybrid needs Salt cloud"),
                                       ("partial", "On-prem via sales"), ("partial", "Self-hosted, offline not stated")]),
          ("Billed per endpoint", [("yes", "50 endpoints per unit"), ("no", "Per API calls a month"),
                                   ("partial", "Price not public"), ("no", "Per million requests")]),
          ("CSPM and runtime, same console", [("yes", "Full CNAPP"), ("no", "Not on vendor site"),
                                              ("no", "Not on WAAP page"), ("no", "Not on product page")])],
    callout="AccuKnox bills per endpoint, runs air-gapped and adds CNAPP in one console.")
API["links"]["ranking"] = [("Salt", "https://salt.security/blog/hybrid-api-security-the-best-of-both-worlds"),
                           ("Harness Traceable", "https://developer.harness.io/web-application-and-api-protection-waap/product-overview/readme/traceable-deployment"),
                           ("Akamai", "https://www.akamai.com/site/en/documents/corporate/akamai-services-descriptions.pdf")]
API["notes"]["ranking"] = """
Every competitor cell comes from that vendor's own pages, read 2026-10-03.
Salt Security: hybrid server that needs the Salt cloud (salt.security/blog/hybrid-api-security-the-best-of-both-worlds). Shadow and zombie discovery and spec generation (salt.security/use-cases/shift-left-with-proactive-api-security). Testing feeds specs to partner DAST tools, Salt Surface is reconnaissance only (same page and the API attack assessment press release). Blocking through a WAF or gateway (salt.security/use-cases/stop-api-attacks). Billing per API calls a month, from Salt's own AWS Marketplace listing (aws.amazon.com/marketplace/pp/prodview-rhcbxzqryobuy).
Traceable (Harness): SaaS backend, on-prem via sales, air-gapped not stated (developer.harness.io traceable-deployment). Shadow, orphan and drift by conformance analysis (developer.harness.io conformance-analysis). API Testing module (harness.io/products/web-application-api-protection/api-testing). Native rate-limit rules (developer.harness.io rate-limiting). Pricing is Contact Sales (harness.io/pricing).
Akamai API Security: SaaS, hybrid or self-hosted, offline mode not stated, Active Testing listed as its own service, billing per million API requests a month (akamai.com services descriptions PDF). Shadow and zombie discovery (akamai.com/blog/security/akamai-api-security-enhancements). Inline enforcement needs App and API Protector (akamai.com/products/api-security).
CNAPP row: CSPM and workload runtime were not found on any of the three vendors' product pages. None of them states it lacks CSPM. Akamai sells Guardicore microsegmentation, which is not CSPM.
AccuKnox cells: help.accuknox.com/use-cases/api-security/, how-to/api-security-onboarding/, faqs/api-sec/ and the Pricing and Sizing sheet.
"""
