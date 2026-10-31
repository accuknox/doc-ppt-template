# -*- coding: utf-8 -*-
"""
Version 3: graphics from the accuknox.com platform pages, front-loaded as new slides,
plus bottom-of-funnel blogs (product posts and guides only) and the most viewed video
per product. Imported after veracode_specs_v2.py.

Graphics were downloaded from https://accuknox.com/wp-content/uploads/ on 2026-10-03.
Each slide's notes name the platform page that carries the graphic.
"""
import os
from veracode_specs import CONTAINER, CSPM, DSPM, API

WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "veracode", "web")
def G(d, n): return os.path.join(WEB, d, "png", n + ".png")

BLOG = "https://accuknox.com/blog/"
YT = "https://youtu.be/"

# ------------------------------------------------------------------ container
CONTAINER["web_a"] = dict(
    title="From Static Scan to Runtime Block",
    kicker="Scanning stops at admission. AccuKnox keeps enforcing while the pod runs.",
    items=[(G("container", "why-you-need-runtime-security"), "Static, admission and runtime controls in one flow",
            0.40, 1.16, 5.5, 3.3),
           (G("container", "inline-and-post-attack-animation-1-1"), "Post-attack kill versus inline block",
            6.04, 1.16, 3.56, 3.3)],
    callout="Detect-and-kill tools act after the process runs. KubeArmor denies it at the kernel first.", callout_y=4.76)
CONTAINER["web_b"] = dict(
    title="How Runtime Protection Rolls Out",
    kicker="Eight steps from onboarding to zero trust, with partner findings in the same console",
    items=[(G("container", "runtime-security-journey"), "The runtime security journey, onboarding to zero trust",
            0.40, 1.16, 3.9, 3.62),
           (G("container", "container-security-hero"), "KubeArmor and the Discovery Engine inside the cluster",
            4.44, 1.16, 5.16, 2.02),
           (G("container", "integrations-cwpp"), "Integrations ring: scanners, ticketing, registries, Veracode included",
            4.44, 3.5, 5.16, 1.28)])
CONTAINER["notes"]["web_a"] = """
Graphics from accuknox.com/platform/runtime-security (why-you-need-runtime-security.webp) and accuknox.com/platform/runtime-security (inline-and-post-attack-animation, first frame).
The right graphic names open-source tools that act after the fact (Tracee, Falco, Tetragon) next to AccuKnox inline mitigation with LSMs. It shows the difference the buyer pays for.
Inline LSM enforcement: docs/faqs/runtime-security.md Q2 and Q6.
"""
CONTAINER["notes"]["web_b"] = """
Graphics from accuknox.com/platform/cwpp: runtime-security-journey.webp (8 steps), integrations-cwpp.webp (the ring shows the Veracode logo among AppSec tools). From accuknox.com/platform/container-security: container-security-hero.gif, first frame.
The 8 steps match docs/use-cases/cwpp.md: onboard, discover posture, recommended hardening, activate hardening, keep learning, mark STABLE, enforce in BLOCK, true zero trust.
Talk track for Veracode: Veracode findings come in through SARIF or API and sit next to runtime findings (docs/getting-started/sarif-findings.md).
"""
CONTAINER["links"]["web_a"] = ["https://accuknox.com/platform/runtime-security"]
CONTAINER["links"]["web_b"] = ["https://accuknox.com/platform/cwpp", "https://accuknox.com/platform/container-security"]
CONTAINER["links"]["usecases"] = ["https://help.accuknox.com/use-cases/image-scan/",
                                  ("Guide: CNAPP in CI/CD", BLOG + "cnapp-ci-cd-pipeline-devsecops-guide"),
                                  ("Checklist: Policy as Code", BLOG + "policy-as-code-for-runtime-enforcement-a-20-point-checklist-that-ships-security-by-default")]
CONTAINER["links"]["diffs"] = ["https://accuknox.com/differentiators",
                               ("Blog: KIEM for RBAC", BLOG + "best-kubernetes-tools-for-rbac-visibility"),
                               ("Blog: React2Shell blocked", BLOG + "react2shell-vulnerability-runtime-detection-response")]
CONTAINER["links"]["deploy"] = ["https://help.accuknox.com/how-to/cluster-onboarding/",
                                ("Video: Install KubeArmor", YT + "CH0qtp5DAhs")]

# ------------------------------------------------------------------ cspm
CSPM["web_a"] = dict(
    title="From Chasing Vulnerabilities to Posture",
    kicker="AccuKnox turns a list of CVEs into one posture program across every cloud",
    items=[(G("cspm", "from-to"), "From chasing vulnerabilities to better cloud security posture",
            0.40, 1.16, 9.2, 2.62),
           (G("cspm", "4stepcompliance"), "Four steps: identify assets, generate policy, find risk, remediate and report",
            0.40, 4.1, 9.2, 0.92)])
CSPM["web_b"] = dict(
    title="How Cloud Detection and Response Works",
    kicker="Cloud events reach the control plane, and the fix runs as a workflow",
    items=[(G("cspm", "AccuKnox-cdr-Architecture"), "CDR architecture: cloud events, CNAPP, SIEM and integrations",
            0.40, 1.16, 5.5, 3.3),
           (G("cspm", "Enforcing-private-access-policy-on-S3-buckets"), "Public S3 bucket reverted to private by workflow",
            6.04, 1.16, 3.56, 1.44),
           (G("cspm", "cdr-capabilities"), "Detect, analyze, alert, investigate, remediate",
            6.04, 2.92, 3.56, 1.54)])
CSPM["notes"]["web_a"] = """
Graphics from accuknox.com/platform/cspm (from-to.webp) and accuknox.com/platform/compliance (4stepcompliance.webp).
The four steps map to the help docs: asset inventory (docs/use-cases/asset-inventory.md), policy and checks (docs/use-cases/compliance.md), risks and alerts (docs/use-cases/cloud-misconfigurations.md), remediation and reports (docs/use-cases/cdr.md, docs/how-to/custom-reports.md).
"""
CSPM["notes"]["web_b"] = """
Graphics from accuknox.com/platform/cdr: AccuKnox-cdr-Architecture.webp, Enforcing-private-access-policy-on-S3-buckets.webp and cdr-capabilities.svg.
AWS path: CloudTrail to S3 to Lambda by CloudFormation (docs/getting-started/aws-cdr.md). Remediation runs through a GitHub Actions runner (docs/getting-started/cdr-setup.md).
POC proof: public S3 bucket reverted to private within 60 seconds (cspm-poc-prereq.pdf p11).
"""
CSPM["links"]["web_a"] = ["https://accuknox.com/platform/cspm", "https://accuknox.com/platform/compliance"]
CSPM["links"]["web_b"] = ["https://accuknox.com/platform/cdr", "https://help.accuknox.com/use-cases/cdr/"]
CSPM["links"]["usecases"] = ["https://help.accuknox.com/use-cases/asset-inventory/",
                             ("Buyer's guide: SOC 2 evidence", BLOG + "cspm-evidence-automation-for-soc-2-pci-dss"),
                             ("Guide: CERT-In and ISO 27001", BLOG + "continuous-compliance-monitoring-cert-in-iso-27001")]
CSPM["links"]["diffs"] = ["https://accuknox.com/differentiators",
                          ("Blog: RBI MD-ITF compliance", BLOG + "rbi-md-itf-rbi-ucb-compliance-accuknox")]
CSPM["links"]["journey"] = ["https://accuknox.com/platform/cspm",
                            ("Video: Agentless cloud tour", YT + "TTRSGag6u48")]

# ------------------------------------------------------------------ dspm
DSPM["web_a"] = dict(
    title="What DSPM Finds and Maps",
    kicker="Four data families, each mapped to the regulation that asks for it",
    items=[(G("dspm", "compliances-dspm"), "Data families from accuknox.com/platform/dspm",
            0.40, 1.16, 9.2, 2.56)],
    stats=[("283", "Data classes", 0.40, 4.06, 2.96), ("62", "Country packs", 3.52, 4.06, 2.96),
           ("282", "Classes mapped to regulations", 6.64, 4.06, 2.96)])
DSPM["notes"]["web_a"] = """
Graphic from accuknox.com/platform/dspm (compliances-dspm.svg): PCI DSS, HIPAA and PHI, PII and GDPR, IP and trade secrets.
Stats from docs/getting-started/dspm-overview.md: 283 data classes, 62 country packs, 282 of 283 classes mapped to regulation clauses.
The DSPM platform page also carries integration-ecosystem-dspm.webp. It is left out because it shows sources the help docs list as unsupported (Google Cloud Storage, Snowflake, SMB and NFS).
No DSPM blog or video meets the bottom-of-funnel bar today, so this deck links help docs and the platform page only.
"""
DSPM["links"]["web_a"] = ["https://accuknox.com/platform/dspm", "https://help.accuknox.com/getting-started/dspm-overview/"]

# ------------------------------------------------------------------ api
API["web_a"] = dict(
    title="The API Iceberg",
    kicker="Most API risk sits below the documented surface",
    items=[(G("api", "api-discovery"), "Shadow and zombie APIs sit below the line",
            0.40, 1.16, 4.4, 3.3),
           (G("api", "sankey-diagram"), "Traffic to exploitable APIs, from AccuKnox CNAPP insights",
            4.94, 1.16, 4.66, 3.3)],
    callout="AccuKnox maps the whole iceberg from live traffic, then ranks the exploitable part.", callout_y=4.76)
API["web_b"] = dict(
    title="Works on Any Infrastructure",
    kicker="Gateways, service meshes and static specs feed one API inventory",
    items=[(G("api", "api-security-architecture"), "Clients, cloud gateways, mesh and spec inspection feed AccuKnox",
            0.40, 1.16, 5.6, 3.4),
           (G("api", "infrastructure-agnostic-api-security"), "Kubernetes, on-prem, Azure and AWS in one model",
            6.14, 1.16, 3.46, 1.5)],
    stats=[("6", "Connectors with setup guides", 6.14, 3.02, 1.66), ("0", "Code changes", 7.94, 3.02, 1.66)])
API["notes"]["web_a"] = """
Graphics from accuknox.com/platform/api-security: api-discovery.webp (the iceberg) and sankey-diagram.webp (traffic heuristics to exploitable APIs).
The Sankey values are illustrative values from the platform page, not a customer result.
Shadow, zombie and orphan definitions: docs/faqs/api-sec.md Q4.
"""
API["notes"]["web_b"] = """
Graphics from accuknox.com/platform/api-security: api-security-architecture.webp and infrastructure-agnostic-api-security.webp.
The architecture graphic shows more mesh logos than the help docs cover with setup guides. Guides exist for AWS API Gateway, the Kubernetes proxy, Istio, NGINX Ingress, Kong and F5 BIG-IP (docs/integrations). Quote only those six in a POC.
No code change: docs/faqs/api-sec.md Q2 and Q7.
"""
API["links"]["web_a"] = ["https://accuknox.com/platform/api-security"]
API["links"]["web_b"] = ["https://accuknox.com/platform/api-security", "https://help.accuknox.com/integrations/api-overview/"]
API["links"]["usecases"] = ["https://help.accuknox.com/use-cases/api-security/",
                            ("Checklist: Runtime API security", BLOG + "runtime-api-security-checklist"),
                            ("Checklist: OWASP API Top 10", BLOG + "owasp-api-security-top-10-the-complete-testing-checklist-2026")]
API["links"]["diffs"] = ["https://accuknox.com/differentiators",
                         ("Guide: API abuse prevention", BLOG + "api-abuse-prevention"),
                         ("Guide: API posture management", BLOG + "api-security-posture-management-guide")]
API["links"]["problem"] = ["https://accuknox.com/platform/api-security",
                           ("Video: Top 5 API attacks", YT + "SOZqlplLBbw")]
