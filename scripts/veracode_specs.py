# -*- coding: utf-8 -*-
"""
Content for the four standalone AccuKnox product decks prepared for Veracode.
Every fact traces to a file named in the slide notes. Paths are relative to
D:\\AccuKnox\\help unless marked otherwise.
"""
import os
from _akdeck import PRIMARY, LAV, NAVY, WHITE

UI = r"D:\AccuKnox\help\references\PRODUCT UI"
DOC = r"D:\AccuKnox\help\docs"
def U(*p): return os.path.join(UI, *p)
def D(*p): return os.path.join(DOC, *p)

SUB = "Briefing for Veracode, October 2026"
AGENDA = "Six parts, slides 3 to 13"
AGENDA_NOTE = """
Agenda. Six parts, every one on this product only.
Part 1, the problem the buyer has today.
Part 2, the solution: what it does (slides 4 and 5) and how it works (slide 6).
Part 3, deployment architecture and the four deployment modes.
Part 4, six use cases and a POC plan with pass checks.
Part 5, the user journey in the AccuKnox console.
Part 6, differentiators, a sourced stack ranking against named alternatives, and list pricing.
"""
PRICE_NOTE = """
Source: AccuKnox - Pricing and Sizing - SEP 2026.xlsx (Google Drive 1qjJG7cNNFB6rtEEah0wpVqt5TwCV-z5Y), effective August 2026.
Step 2 tiers, USD per unit per month: 10 to 50 units 40 dollars, 51 to 250 34, 251 to 750 29, 751 to 2,500 25, 2,501 to 5,000 21, 5,001 and up negotiated. Tier decay 15 percent.
Step 3 support: Silver included (9 x 5), Gold 10 percent of subscription (12 x 6), Platinum 25 percent (24 x 7 with a TAM).
Step 5 deployment: on-premises 0 dollars, shared tenant SaaS 0 dollars, dedicated tenant 3,000 dollars a month plus 10 percent.
On-prem customers are expected to procure Platinum Support (docs/faqs/pricing.md Q5).
Usage above quota is not blocked. Support reaches out if usage stays more than 30 percent over (docs/faqs/pricing.md Q3).
The example is list price before any discount or partner terms.
"""
JOURNEY_NOTE_TAIL = "\nScreenshots show demo tenant data from references/PRODUCT UI or the help docs images."


# =========================================================================
CONTAINER = dict(
    key="container", file="AccuKnox_Container_Security_IaC.pptx",
    title_drive="AccuKnox Container Security and IaC - Veracode Briefing",
    cover_title="AccuKnox Container Security\nand IaC Scanning", cover_sub=SUB, short="Container Security",
    agenda_kicker=AGENDA,
    problem=dict(
        kicker="All advanced attacks are runtime attacks, yet most tools only check static posture",
        cards=[("bolt", "Attacks happen at runtime", "Most tools detect static posture. Advanced attacks run in live workloads"),
               ("alert-octagon", "Kill comes too late", "Post-exploit tools stop a process after it runs. Data may be gone"),
               ("file-code", "Misconfig hides in manifests", "Hardcoded passwords and privileged pods slip past reviews"),
               ("bug", "CVE noise", "Teams cannot tell which image CVEs actually execute")],
        stats=[("100x", "Less CVE noise with Runtime Verified"), (">50%", "Savings from one platform"),
               ("2M+", "KubeArmor downloads")],
        callout="AccuKnox scans the pipeline and the image, then blocks the attack inline at runtime."),
    overview=dict(
        kicker="Scan, harden and enforce, from the pipeline to the running pod",
        cards=[("shield-lock", "Inline runtime blocking", "KubeArmor blocks before execution with AppArmor, BPF-LSM, SELinux"),
               ("sparkles", "Auto-discovered policies", "Learns app behavior, audits, then switches to block"),
               ("target", "Runtime Verified CVEs", "Flags CVEs that execute, enriched with KEV and EPSS"),
               ("package", "Image and registry scans", "8 registries, plus in-cluster scans of running images"),
               ("file-code", "IaC scanning", "13 formats. Misconfig, secrets and drift in 9 CI/CD tools"),
               ("list-check", "Agentless KSPM", "CIS, STIG, KIEM and misconfig jobs, installed by Helm")],
        logos=["kubernetes-original", "docker-original", "helm-original", "terraform-original", "github-original",
               "gitlab-original", "jenkins-original", "si-harbor", "si-redhatopenshift"]),
    detail=dict(
        title="Our Solution, Runtime Protection", kicker="Discovered policies move from audit to block with no app change",
        rows=[("eye", "1  Observe", "eBPF telemetry on file, process and network events"),
              ("sparkles", "2  Discover", "Discovery Engine writes least-permissive policies"),
              ("clock", "3  Audit", "Policies run in audit mode until no deviation shows"),
              ("shield-check", "4  Block", "Namespace posture set to block. Violations stop inline"),
              ("wifi-off", "5  Keep enforcing", "Enforcement continues if the control plane is unreachable")],
        shot=U("1_dashboard", "Runtime sec dash.png"), shot_h=2.5,
        stats=[("200m", "KubeArmor CPU request"), ("200Mi", "KubeArmor memory"), ("0", "Host or CRI changes")]),
    tech=dict(
        kicker="Agents enforce in the kernel. Scanners feed one findings view.",
        cols=[("Sources", [("git-merge", "CI/CD pipelines", False), ("file-code", "IaC repositories", False),
                           ("package", "Container registries", False), ("container", "Kubernetes clusters", False),
                           ("server", "VMs and bare metal", False)]),
              ("Collect", [("terminal-2", "CI plugins, 9 tools", False), ("scan", "Registry scanner", False),
                           ("shield-lock", "KubeArmor DaemonSet", False), ("sparkles", "Discovery Engine", False),
                           ("list-check", "KSPM CronJobs", False), ("upload", "Feeder over TLS", False)]),
              ("Act", [("shield-x", "Block inline", False), ("alert-triangle", "Audit, drift alerts", False),
                       ("jira-original", "Jira tickets", True), ("slack-original", "Slack, SIEM", True),
                       ("report-analytics", "Reports", False)])],
        cp_title="AccuKnox control plane",
        cp_rows=[("filter", "Normalize and dedupe", None), ("target", "Runtime Verified,", "KEV and EPSS"),
                 ("certificate", "CIS, MITRE ATT&CK,", "NIST 800-53"), ("settings-automation", "Versioned policies,", "CLI, UI or GitOps")]),
    deploy=dict(
        kicker="One Helm chart per cluster. Egress only, no inbound ports.", env="Your clusters and pipelines",
        rows=[("helm-original", True, "Helm install", "KubeArmor DaemonSet plus agent Deployments in one chart"),
              ("kubernetes-original", True, "Kubernetes 1.18+, kernel 4.15+", "EKS, AKS, GKE Autopilot, OCI, OpenShift, Talos"),
              ("network", False, "Egress only", "Ports 443 and 3000, plus 8081 and 9090 for SPIRE"),
              ("server", False, "VMs and bare metal", "KubeArmor in systemd mode. containerd, CRI-O, Podman"),
              ("github-original", True, "CI/CD plugins", "IaC and image scans in 9 pipeline tools")],
        cp_lines=["Runs on Kubernetes", "SaaS, your cloud,", "on-prem or air-gapped", "Air-gapped: 16 vCPU, 64 GB"],
        note=["Enforcement keeps working", "while disconnected"]),
    usecases=dict(
        kicker="Six scenarios, each from an AccuKnox help page",
        cards=[("package", "Container image scan", "Find CVEs and sensitive data in image layers", "Image"),
               ("file-code", "IaC scan in CI/CD", "Catch a Terraform bucket set to public-read", "IaC"),
               ("list-check", "Cluster misconfig scan", "Find a hardcoded password in a manifest", "KSPM"),
               ("shield-x", "Admission control", "Deny privileged pods and untrusted registries", "KnoxGuard"),
               ("lock", "Workload hardening", "FIM, noexec on /tmp, block package tools", "Hardening"),
               ("shield-check", "Zero trust runtime", "Allow only the processes each workload needs", "Zero trust")]),
    poc=dict(
        kicker="A two-week POC, with attack simulations in week 2",
        steps=[("list-check", "Week 1", "Prereqs and setup"), ("container", "Week 1", "Onboard, inventory"),
               ("bug", "Week 2", "Attack simulation"), ("report-analytics", "Week 2", "Executive report")],
        pills=[("Plan: 2 weeks", PRIMARY, WHITE), ("On-prem: 2 to 3 weeks", LAV, NAVY)],
        tests=[("file-search", "File integrity", "Write to /bin and /boot from inside a pod", "Permission Denied, violation reported"),
               ("cpu", "Cryptominer", "Start a crypto-miner in a container", "Process blocked"),
               ("terminal-2", "Tools in a pod", "Run kubectl, nmap or masscan inside a pod", "Blocked and reported"),
               ("package", "New critical CVE", "Deploy an image with a new critical CVE", "Alert with cluster context")]),
    journey=dict(
        kicker="Six screens take a team from a new cluster to a blocked attack",
        steps=[(D("how-to", "images", "cluster-onboarding", "image-2.png"), "Onboard a cluster", "Settings, Manage Cluster, Helm"),
               (U("2_inventory", "Clusters 1.png"), "See the clusters", "Findings, nodes, workloads, alerts"),
               (U("1_dashboard", "KSPM Dash 1.png"), "Check posture", "KSPM findings and CIS checks"),
               (U("1_dashboard", "ASPM_Container Image_Dash 1.png"), "Rank image CVEs", "Vulnerable packages, registries"),
               (U("6_runtime", "Runtime 1.png"), "Set policies", "Admission and KSPM policies"),
               (U("1_dashboard", "Runtime sec dash.png"), "Watch enforcement", "Audited and blocked alerts")]),
    diffs=dict(
        kicker="Prevention in the kernel, not a kill after the damage",
        stats=[("99.5%", "Feature score across 102 features"), ("100x", "Less CVE noise"), ("2M+", "KubeArmor downloads")],
        cards=[("shield-lock", "Block before execute", "LSM enforcement, not kill-after-detect"),
               ("code", "Creator of KubeArmor", "CNCF Sandbox project, open source"),
               ("target", "Runtime CVE reachability", "Patented in-kernel aggregation"),
               ("sparkles", "Zero trust, discovered", "Least-permissive policies written for you"),
               ("wifi-off", "Works disconnected", "Enforcement runs without the control plane"),
               ("package", "Running images only", "In-cluster scans need no registry access")]),
    ranking=dict(
        kicker="102-feature comparison against Red Hat ACS and SUSE NeuVector",
        rows=[["Capability", "AccuKnox", "Red Hat ACS", "SUSE NeuVector"],
              ["Inline threat response", "Yes", "Partial", "Yes"],
              ["Preemptive mitigation", "Yes", "No", "No"],
              ["Process whitelisting", "Yes", "No", "Yes"],
              ["Virtual patching", "Yes", "No", "No"],
              ["Cryptominer protection", "Yes", "Partial", "No"],
              ["Disconnected mode", "Yes", "No", "Yes"],
              ["Runtime CVE reachability", "Yes", "No", "No"],
              ["KIEM", "Yes", "No", "No"],
              ["Overall score, 102 features", "99.5%", "43.1%", "49.0%"]],
        colw=[3.2, 2.0, 2.0, 2.0], h=3.3,
        callout="AccuKnox scores 99.5% across 102 features. RHACS scores 43.1% and NeuVector 49.0%."),
    pricing=dict(
        kicker="Runtime priced per node, scans per image, IaC per repo",
        unit_big="1 node\n= 1 unit",
        unit_sub="40 container images = 1 unit. 30 code repos for IaC = 1 unit.",
        unit_rows=["Filter images by regex or date", "Scan only running images", "No hard stop above quota"],
        example=[("100 nodes = 100 units", False), ("400 images = 10 units", False), ("60 repos = 2 units", False),
                 ("112 units, Tier 2 at $34", False), ("$3,808 / month", True), ("$45,696 / year", False)]),
    notes=dict(
        agenda=AGENDA_NOTE,
        problem="""
Sources.
"All advanced attacks are runtime attacks" and disparate tools add about 100 percent higher costs, a unified platform gives more than 50 percent savings (docs/faqs/general.md).
Post-exploit tools kill a process after it runs, when data may be deleted, encrypted or transmitted (docs/faqs/runtime-security.md Q6).
Hardcoded passwords in manifests go unnoticed by developers and DevOps teams (docs/use-cases/cluster-misconfiguration-scanning.md).
Runtime Verified reduces CVE noise by up to 100x (docs/getting-started/3.4-release.md).
KubeArmor 2 million plus downloads (docs/faqs/general.md).
""",
        overview="""
Sources.
KubeArmor enforces through AppArmor, SELinux and BPF-LSM (docs/getting-started/accuknox-agents.md).
Discovery Engine auto-generates policies from observed behavior. Policies start in audit mode, are marked STABLE, then the namespace moves to Block (cwpp-playbook.pdf p8 to 9, docs/use-cases/zero-trust.md).
Runtime Verified with CISA KEV, EPSS and PoC enrichment (docs/getting-started/3.4-release.md).
Registries: ECR, GAR, ACR, Nexus, Docker Hub, Harbor, Quay, JFrog (docs/support-matrix/registry.md).
IaC: 13 formats (docs/support-matrix/iac.md). CI/CD with IaC and container scans: GitHub, GitLab, Bitbucket, Azure DevOps, CircleCI, AWS CodePipeline, Jenkins, Google Cloud Build, Bamboo. Harness is Coming Soon (docs/support-matrix/cicd-support-matrix.md).
KSPM jobs for misconfiguration, KIEM, CIS and STIG run as CronJobs installed by Helm (docs/how-to/k8s-security-onboarding.md).
""",
        detail="""
Policy flow: telemetry on file, process and network, then discovered policies in audit mode, STABLE, then Block (cwpp-playbook.pdf p8 to 9 and p23).
Enforcement keeps working when disconnected from the control plane (accuknox-vs-rhacs-vs-neuvector-k8s-security.xlsx, Disconnected Mode, and docs/faqs/deployment.md Q3).
Resource requests: KubeArmor 200m CPU and 200Mi memory. Discovery Engine 200m and 200Mi. Agents Operator 50m and 50Mi. Feeder 50m and 100Mi. Shared Informer 20m and 50Mi. Policy Enforcement 10m and 20Mi (docs/getting-started/cwpp-prereq.md).
KubeArmor runs as a non-privileged DaemonSet with no change at the host or CRI level (docs/faqs/runtime-security.md Q3).
Screenshot: Runtime Security dashboard, demo tenant data.
""",
        tech="""
KubeArmor runs as a DaemonSet. Shared Informer, Feeder, Policy Enforcement and Discovery Engine run as Deployments (docs/getting-started/cwpp-prereq.md).
The Feeder posts to the control plane over TLS with a per-tenant key in a Kubernetes secret (docs/getting-started/accuknox-agents.md).
KSPM jobs install as CronJobs by Helm (docs/how-to/k8s-security-onboarding.md).
Compliance mapping: CIS, MITRE ATT&CK, NIST 800-53 (accuknox-container-security-poc-cwpp-kspm.pdf p8).
Policies apply through CLI, UI or GitOps and are versioned (same PDF p6 to 7).
Alerts: audit, block and drift (cwpp-playbook.pdf p23).
""",
        deploy="""
Helm: helm upgrade --install agents oci://public.ecr.aws/k9v9d5v2/kspm-runtime, version v0.1.16 in docs/how-to/cluster-onboarding.md. docs/how-to/k8s-security-onboarding.md names agents-chart v0.10.0. Confirm the chart before you quote it.
Requirements: Kubernetes 1.18 or later, Linux kernel 4.15 or later for runtime, egress only. Ports 443 and 3000, plus 8081 and 9090 for SPIRE. EKS, AKS, OCI and on-prem (docs/how-to/k8s-security-onboarding.md). OpenShift needs the REDHAT_CERTIFIED_OP flags (docs/how-to/cluster-onboarding.md).
3.5 adds Talos Linux, GKE Autopilot, CRI auto-detection for containerd and CRI-O. 3.6 adds ECS Fargate (release notes).
VM and bare metal: KubeArmor in systemd mode (docs/support-matrix/kubearmor-support-matrix.md).
Air-gapped hardware: 16 vCPU or more, 64 GB RAM or more, 512 GB disk (accuknox-container-security-poc.pdf p11). Page 5 of the same PDF says 32 GB, so confirm.
Deployment modes from accuknox.com/differentiators.
""",
        usecases="""
Sources: docs/use-cases/image-scan.md, iac-scan.md, cluster-misconfiguration-scanning.md, admission-controller-knoxguard.md (Kyverno, vulnerability-threshold blocking is still in the pipeline), hardening.md, zero-trust.md.
""",
        poc="""
Source: references/technical-reference/playbooks-and-poc/accuknox-container-security-poc-cwpp-kspm.pdf.
Two-week plan (p10). Week 1: prerequisites, control plane, onboarding, inventory. Week 2: attack simulation, reporting, executive report.
Runtime scenarios (p6 to 7): FIM writes to bin and boot return Permission Denied. Cryptominers blocked. docker, crictl, kubectl in a container blocked. nmap and masscan blocked. Also root cert tampering, /tmp execution, env variable access, Vault protection, process whitelisting, nano-segmentation.
Vulnerability (p9): alert on a new critical CVE, findings in cluster context.
On-prem POC 2 to 3 weeks (docs/faqs/deployment.md Q7).
""",
        journey="""
1 docs/how-to/cluster-onboarding.md. 2 Inventory, Clusters. 3 KSPM dashboard. 4 Container Images dashboard. 5 Policies list with admission and KSPM policies. 6 Runtime Security dashboard.
Journey order follows cwpp-playbook.pdf p3 to 21.""" + JOURNEY_NOTE_TAIL,
        diffs="""
99.5 percent overall score across 102 features (references/competitive/battlecards/accuknox-vs-rhacs-vs-neuvector-k8s-security.xlsx).
Block before execute versus kill after detect (docs/faqs/runtime-security.md Q2 and Q6).
AccuKnox created KubeArmor, a CNCF Sandbox project (docs/faqs/general.md).
Patented in-kernel aggregation behind Runtime Verified (docs/getting-started/3.4-release.md).
Patented runtime zero trust (docs/use-cases/zero-trust.md).
In-cluster scanning covers running images with no registry access (docs/how-to/k8s-security-onboarding.md).
""",
        ranking="""
Source: references/competitive/battlecards/accuknox-vs-rhacs-vs-neuvector-k8s-security.xlsx, Feature Comparison, 102 features. Overall: AccuKnox 99.5 percent, RHACS 43.1 percent, NeuVector 49.0 percent.
The SBOM row is left out because its note is out of date.
""",
        pricing="""
Units: CWPP, KSPM and KIEM 1 node per unit. Container image scanning 40 images per unit. SAST, secret scanning and IaC 30 code repos per unit (Pricing and Sizing sheet, Step 1).
Image filters: regex on repo/image:tag, updated or pulled within X or Y days, in-cluster runtime images only. Notification above 5,000 images (docs/faqs/pricing.md Q4).
Example: 100 + 10 + 2 = 112 units, Tier 2, 34 dollars, 3,808 dollars a month, 45,696 a year.
""" + PRICE_NOTE),
)


# =========================================================================
CSPM = dict(
    key="cspm", file="AccuKnox_CSPM.pptx",
    title_drive="AccuKnox CSPM - Veracode Briefing",
    cover_title="AccuKnox CSPM\nCloud Security Posture Management", cover_sub=SUB, short="CSPM",
    agenda_kicker=AGENDA,
    problem=dict(
        kicker="Misconfiguration leads cloud risk, and audit evidence ages between checks",
        cards=[("alert-triangle", "Misconfig leads", "The NSA names misconfiguration the leading cloud vulnerability"),
               ("layers-subtract", "Console sprawl", "Teams switch between cloud consoles to see their own assets"),
               ("refresh", "Drift at runtime", "Public buckets and new public IPs appear after deploy"),
               ("clock", "Audits go stale", "Point-in-time evidence ages before the auditor reads it")],
        stats=[("60h to 5h", "Audit prep per quarter, 200+ accounts"), ("40+", "Compliance frameworks"),
               ("4", "Clouds: AWS, Azure, GCP, OCI")],
        callout="AccuKnox CSPM watches every account read-only and maps each check to your framework."),
    overview=dict(
        kicker="Inventory, misconfiguration, compliance and response, agentless and read-only",
        cards=[("list-details", "One asset inventory", "Accounts, assets and workloads across four clouds"),
               ("alert-triangle", "Misconfig and drift", "1,000+ checks against baselines, Monitors on key assets"),
               ("certificate", "Continuous compliance", "Each check mapped to programs and sub-controls"),
               ("hierarchy-2", "Security Graph", "Asset and finding edges with blast radius"),
               ("bolt", "Detect and respond", "Cloud audit events trigger automatic fixes"),
               ("settings-automation", "Rules engine", "Opens Jira tickets. Two clean scans close them")],
        logos=["amazonwebservices-original-wordmark", "azure-original", "googlecloud-original", "oracle-original",
               "jira-original", "slack-original"], logos_label="CLOUDS AND TOOLS"),
    detail=dict(
        title="Our Solution, Continuous Compliance", kicker="Every check maps to a framework control, with a live score",
        rows=[("certificate", "40+ frameworks", "CIS, NIST 800-53, SOC 2, HIPAA, PCI DSS, ISO 27001"),
              ("building-bank", "Regional frameworks", "RBI MD-ITF, SAMA, SEBI CSCRF and DPDP"),
              ("chart-pie", "Score per framework", "Passed over passed, failed, warning and N/A"),
              ("adjustments-horizontal", "Checks management", "Turn checks off or re-rate severity per account"),
              ("report-analytics", "Scheduled reports", "Multi-framework compliance reports")],
        shot=U("5_compliance", "Compliance 1.png"), shot_h=2.5,
        stats=[("200+", "CIS v2.0 controls"), ("110+", "NIST controls"), ("80+", "PCI DSS v4.0 controls")]),
    tech=dict(
        kicker="Read-only APIs feed one asset graph. Cloud events drive response.",
        cols=[("Sources", [("amazonwebservices-original-wordmark", "AWS and GovCloud", True), ("azure-original", "Microsoft Azure", True),
                           ("googlecloud-original", "Google Cloud", True), ("oracle-original", "Oracle Cloud", True),
                           ("history", "Cloud audit logs", False)]),
              ("Collect", [("cloud-lock", "Read-only API scans", False), ("users-group", "Org onboarding", False),
                           ("bolt", "CloudTrail to Lambda", False), ("bolt", "Activity Log, EventHub", False),
                           ("bolt", "Log Sink, Pub/Sub", False)]),
              ("Act", [("jira-original", "Jira, ServiceNow", True), ("slack-original", "Slack, email", True),
                       ("rotate-clockwise", "Auto-remediation", False), ("report-analytics", "Compliance reports", False),
                       ("message-chatbot", "Ask AI", False)])],
        cp_title="AccuKnox control plane",
        cp_rows=[("list-details", "Asset inventory", None), ("hierarchy-2", "Security Graph,", "blast radius"),
                 ("certificate", "1,000+ checks to", "40+ frameworks"), ("settings-automation", "Rules engine and", "finding lifecycle")]),
    deploy=dict(
        kicker="Agentless. One read-only role per account, or one StackSet per org.", env="Your cloud accounts",
        rows=[("amazonwebservices-original-wordmark", True, "AWS", "ReadOnlyAccess + SecurityAudit. Assume Role, External ID"),
              ("users-group", False, "AWS Organizations", "CloudFormation StackSet, auto-connect new accounts"),
              ("azure-original", True, "Azure", "Security Reader, Log Analytics Reader, Directory.Read.All"),
              ("googlecloud-original", True, "Google Cloud", "Project Viewer plus a custom role, 7 APIs enabled"),
              ("oracle-original", True, "Oracle Cloud", "SecurityAudit group, read all-resources in tenancy")],
        cp_lines=["Read-only permissions", "AWS 403, Azure 209,", "GCP 901", "SaaS, on-prem, air-gapped"],
        note=["A denied permission blinds", "only that one service"]),
    usecases=dict(
        kicker="Six scenarios, each from an AccuKnox help page",
        cards=[("list-details", "Asset inventory", "One list and hierarchy view across clouds", "Inventory"),
               ("alert-triangle", "Misconfig and drift", "Detect drift from baseline on critical assets", "Posture"),
               ("certificate", "Continuous compliance", "Live scores for CIS, NIST, SOC 2, HIPAA", "GRC"),
               ("lock", "Enforce private S3", "CDR reverts a public bucket to private", "CDR"),
               ("settings-automation", "Ticket automation", "The rules engine opens a Jira ticket per finding", "Workflow"),
               ("hierarchy-2", "Security Graph", "Trace the blast radius from one asset", "Graph")]),
    poc=dict(
        kicker="A two-week sprint, with pass checks from the CSPM POC guide",
        steps=[("cloud-lock", "Days 1 to 3", "Onboard, discover"), ("alert-triangle", "Day 3", "Top 20 ranked"),
               ("bolt", "Week 2", "CDR simulations"), ("report-analytics", "Day 14", "Executive report")],
        pills=[("Plan: 2 weeks", PRIMARY, WHITE), ("SaaS: 1 to 2 weeks", LAV, NAVY)],
        tests=[("list-details", "Discovery", "Onboard every in-scope account", "100% of assets discovered"),
               ("alert-triangle", "Prioritization", "Rank critical misconfigurations", "Top 20 risk-ranked by Day 3"),
               ("lock", "CDR, S3", "Make one S3 bucket public", "Reverted to private in 60 s"),
               ("network", "CDR, public IP", "Attach a public IP to an EC2 instance", "Detached within 90 s")]),
    journey=dict(
        kicker="Six screens take a team from a new account to a closed ticket",
        steps=[(D("getting-started", "images", "release-notes", "v3.6", "aws-assume-role-cloudformation.png"), "Connect an account", "Assume Role by CloudFormation"),
               (U("1_dashboard", "CSPM Dash 1.png"), "Read the dashboard", "Accounts, assets, findings"),
               (U("3_issues", "Issues_2.png"), "Triage findings", "Filter by account, status, severity"),
               (U("security graph", "Security Graph 1.png"), "Trace blast radius", "Asset and finding graph"),
               (U("5_compliance", "Compliance 2.png"), "Prove compliance", "Score and failed controls"),
               (U("1_dashboard", "CDR dash 1.png"), "Respond to events", "CDR alerts by rule and severity")]),
    diffs=dict(
        kicker="Read-only access, four clouds, regional frameworks and closed-loop fixes",
        stats=[("4", "Clouds, including Oracle"), ("40+", "Frameworks out of the box"), ("60 s", "Public S3 bucket reverted")],
        cards=[("lock", "Read-only by design", "Every permission listed with its reason"),
               ("world", "Four clouds", "AWS, Azure, GCP and Oracle, plus GovCloud"),
               ("building-bank", "Regional frameworks", "RBI, SAMA, SEBI CSCRF and DPDP"),
               ("refresh", "Closed-loop fixes", "CDR auto-remediation, two-scan auto-close"),
               ("wifi-off", "Air-gapped CSPM", "Run the whole console on-prem"),
               ("server", "Private cloud too", "OpenShift, Nutanix and Tanzu")]),
    ranking=dict(
        kicker="Cloud posture rows from the AccuKnox vs Prisma Cloud Enterprise comparison",
        rows=[["Capability", "AccuKnox", "Prisma Cloud Enterprise"],
              ["Multi-cloud inventory", "Yes, one inventory", "Yes, 5 clouds, 24h refresh"],
              ["Public S3 detection and fix", "Yes, CloudTrail event reverts it", "Yes, config policy and CLI fix"],
              ["Real-time event automation", "Yes, CloudTrail triggers the fix", "Limited, alerts can lag hours"],
              ["Private cloud", "Yes, OpenShift, Nutanix, Tanzu", "Limited, OpenShift v4"],
              ["Compliance coverage", "42 framework versions", "60+ standards"],
              ["Air-gapped deployment", "Yes, supported", "No, not in Enterprise Edition"]],
        colw=[2.6, 3.3, 3.3], h=3.1,
        callout="AccuKnox leads on real-time response, private cloud and air-gapped. Prisma lists more standards."),
    pricing=dict(
        kicker="Priced per billable cloud asset, normalized into units",
        unit_big="10 assets\n= 1 unit",
        unit_sub="Billable: compute, databases, storage, serverless, Kubernetes. Not billable: VPCs, subnets, IAM roles.",
        unit_rows=["Count with ak-asset-check, 30 s", "Runs locally and read-only", "No hard stop above quota"],
        example=[("2,000 billable assets", False), ("= 200 units, Tier 2", False), ("$34 x 200 units", False),
                 ("$6,800 / month", True), ("$81,600 / year", False)]),
    notes=dict(
        agenda=AGENDA_NOTE,
        problem="""
Sources.
The NSA calls misconfiguration the leading vulnerability reason in a cloud environment (docs/use-cases/cloud-misconfigurations.md). The page gives no link.
Console sprawl (docs/use-cases/asset-inventory.md). Runtime drift such as public buckets and public IPs (docs/use-cases/cdr.md).
Audit prep fell from 60 hours to under 5 hours per quarter for a financial services client with 200+ cloud accounts. The client is not named (docs/faqs/compliance.md Q3 and Q10).
40+ frameworks from accuknox.com/differentiators. The compliance matrix lists 42 rows (docs/support-matrix/compliance-matrix.md). Older pages say 30+ or 33+.
Four clouds including OCI (docs/support-matrix/public-cloud.md, docs/how-to/oracle-onboarding.md).
""",
        overview="""
Sources.
Inventory with list and hierarchy views (docs/use-cases/asset-inventory.md).
Over 1,000 checks, each mapped to programs and sub-controls (docs/use-cases/compliance.md).
Security Graph: asset and finding graphs, blast radius, AWS, Azure and GCP (docs/getting-started/3.6-release.md).
CDR: CloudTrail to S3 to Lambda by CloudFormation for AWS. Log Sink to Pub/Sub by Terraform for GCP. Activity Log to EventHub by Terraform for Azure (docs/getting-started/aws-cdr.md, gcp-cdr.md, azure-cdr.md).
Rules engine creates tickets (docs/use-cases/rules-engine-ticket-creation.md). A finding moves to Fixed when two scans agree, and the linked ticket closes (docs/getting-started/3.6-release.md).
CIEM is Coming Soon and supports standalone accounts only, so it is left off the slide (docs/getting-started/ciem-overview.md).
""",
        detail="""
Frameworks: compliance matrix (docs/support-matrix/compliance-matrix.md). Regional frameworks RBI MD-ITF, SAMA, CSCRF SEBI, DPDP (docs/getting-started/3.4-release.md and 3.6-release.md).
Score formula: passed divided by passed plus failed plus warning plus N/A (docs/use-cases/compliance.md).
Checks Management, off or re-rated per account (docs/getting-started/3.6-release.md).
Control counts per framework: CIS v2.0 200+, NIST 110+, SOC2 64+, HIPAA 54+, PCI v4.0 80+, ISO 114+, AWS Well-Architected 50+ (references/technical-reference/playbooks-and-poc/cspm-poc-prereq.pdf p9).
Screenshot: Compliance page, demo tenant data.
""",
        tech="""
Read-only, agentless, through cloud APIs (docs/faqs/cspm.md Q6).
Org onboarding: AWS Organizations StackSet (docs/how-to/aws-org-onboard.md). Azure management groups (docs/how-to/azure-org-onboard.md).
CDR log paths as on slide 4 notes. Remediation runs through a GitHub Actions runner and needs elevated rights in the cloud account (docs/getting-started/cdr-setup.md). Say this to a technical lead before the POC.
Tickets: Jira, Freshservice, ConnectWise (docs/faqs/cspm.md). ServiceNow (docs/integrations/support-matrix.md).
The docs give no fixed scan interval. Scans run on a periodic schedule (docs/use-cases/asset-inventory.md).
""",
        deploy="""
AWS: IAM user with ReadOnlyAccess and SecurityAudit (docs/how-to/aws-onboarding.md). v3.6 adds STS Assume Role with External ID by CloudFormation, standalone accounts only (docs/getting-started/3.6-release.md). GovCloud (3.4-release.md).
AWS Organizations: StackSet, include or exclude filter, optional auto-connect (docs/how-to/aws-org-onboard.md).
Azure: app registration, Directory.Read.All, Security Reader, Log Analytics Reader (docs/how-to/azure-onboarding.md).
GCP: 7 APIs, service account with Project Viewer plus a custom role with storage.buckets.getIamPolicy (docs/how-to/gcp-onboarding.md).
OCI: SecurityAudit group with read all-resources in tenancy (docs/how-to/oracle-onboarding.md).
Permission counts AWS 403, Azure 209, GCP 901. A denied permission only blinds that service (docs/how-to/cspm-permissions-overview.md).
""",
        usecases="""
Sources: docs/use-cases/asset-inventory.md, cloud-misconfigurations.md, compliance.md, cdr.md (Enforcing Private S3 Buckets), rules-engine-ticket-creation.md, docs/getting-started/3.6-release.md (Security Graph).
""",
        poc="""
Source: references/technical-reference/playbooks-and-poc/cspm-poc-prereq.pdf.
Plan D1 to D14 (p12). Week 1 onboarding and discovery. Week 2 findings, CDR simulations, executive report.
Success criteria (p11): 100 percent asset discovery. Top 20 critical misconfigurations ranked by Day 3. At least one chained attack path per account. CIS, NIST 800-53, SOC2 and HIPAA scores. S3 reverted to private within 60 seconds. EC2 public IP detached within 90 seconds. Geo-fencing alert within 30 seconds. Root MFA, stale keys, over-privileged roles. Bedrock audit. Jira ticket and Slack alert per finding.
SaaS POC 1 to 2 weeks (docs/faqs/deployment.md Q7).
""",
        journey="""
1 Assume Role onboarding by CloudFormation (docs/getting-started/3.6-release.md image). 2 CSPM dashboard. 3 Cloud findings. 4 Security Graph. 5 Compliance framework detail. 6 CDR dashboard.
There is no Cloud Assets inventory screenshot in references/PRODUCT UI.""" + JOURNEY_NOTE_TAIL,
        diffs="""
Read-only with every permission and its reason listed (docs/how-to/cspm-permissions-overview.md).
Four clouds including OCI (docs/support-matrix/public-cloud.md). Asset types: AWS 125, Azure 88, GCP 37 (count of docs/support-matrix/assets-list.md).
Regional frameworks (release notes 3.4 and 3.6). Closed loop: CDR plus two-scan auto-close (docs/use-cases/cdr.md, 3.6-release.md).
Air-gapped (docs/faqs/general.md). Private cloud OpenShift, Nutanix, Tanzu (docs/support-matrix/private-cloud.md).
60 seconds: CSPM POC success criterion (cspm-poc-prereq.pdf p11).
""",
        ranking="""
Source: references/competitive/battlecards/prisma-enterprise/Accuknox-vs-Prisma-Enterprise-Comparison.md, Cloud Security Posture section and compliance rows. The document carries no date.
This is the only sourced CSPM comparison in the repo. There is no CSPM-only comparison against Wiz, Orca or Lacework.
The same document says AccuKnox covers 33+ frameworks in 42 versions. The deck uses 40+ from accuknox.com elsewhere, so this row shows the 42 versions.
""",
        pricing="""
Units: CSPM and CDR 10 assets per unit (Pricing and Sizing sheet, Step 1).
Billable: AWS EC2, RDS, Aurora, DynamoDB, Lambda, EKS, ECS, S3, Bedrock. Azure VMs and scale sets, AKS, Functions, SQL, Cosmos DB, ACR, MySQL, Postgres, MariaDB, Redis, Azure OpenAI, AI Foundry. GCP Compute, GKE, Functions, Cloud SQL, Storage, Cloud Run. OCI Compute, Autonomous DB, Object Storage, OKE, MySQL. Not billable: VPCs, subnets, security groups, IAM roles (docs/resources/asset-billable-check.md).
ak-asset-check runs locally and read-only. A billable scan takes about 30 seconds (same page).
Example: 2,000 assets, 200 units, Tier 2, 34 dollars, 6,800 dollars a month, 81,600 a year.
""" + PRICE_NOTE),
)


# =========================================================================
DSPM = dict(
    key="dspm", file="AccuKnox_DSPM.pptx",
    title_drive="AccuKnox DSPM - Veracode Briefing",
    cover_title="AccuKnox DSPM\nData Security Posture Management", cover_sub=SUB, short="DSPM",
    agenda_kicker=AGENDA,
    problem=dict(
        kicker="Regulated data spreads across buckets, databases and SaaS apps, with no single map",
        cards=[("map-2", "No map of sensitive data", "PII, PHI and card data sit in buckets, databases and SaaS apps"),
               ("cloud-off", "Data leaves to be scanned", "Many DSPM tools send metadata to the vendor cloud"),
               ("lock-open", "Exposed stores", "Public or unencrypted stores hold regulated records"),
               ("gavel", "Audits need evidence", "GDPR, PCI DSS, HIPAA and DPDP ask where the data is")],
        stats=[("283", "Data classes"), ("62", "Country packs"), ("282", "Classes mapped to regulations")],
        callout="AccuKnox DSPM classifies data inside your region. Only a findings file leaves."),
    overview=dict(
        kicker="Discover, classify and map sensitive data, with a read-only scanner you own",
        cards=[("scan", "Read-only scanner", "Runs in the data's region. No write path, no inbound ports"),
               ("fingerprint", "283 data classes", "PII, PHI, financial, secrets and 117 regional classes"),
               ("target", "Confidence per finding", "Very likely, Likely or Possible. Default floor is Likely"),
               ("eye-off", "Masked evidence", "The console shows the last 4 characters. Rows discarded"),
               ("gavel", "Regulation mapping", "GDPR, PCI DSS, HIPAA, CCPA, DPDP, with CWE and MITRE"),
               ("world", "Data residency view", "Sensitive records mapped by region")],
        logos=["amazonwebservices-original-wordmark", "azure-original", "postgresql-original", "mysql-original",
               "mongodb-original"], logos_label="DATA SOURCES"),
    detail=dict(
        title="Our Solution, Supported Sources", kicker="Cloud stores, databases and SaaS apps, scanned in place",
        rows=[("cloud", "AWS", "S3, RDS and Aurora, DocumentDB, DynamoDB, Secrets Manager"),
              ("cloud", "Azure", "Blob, ADLS Gen2, Azure SQL, PostgreSQL, MySQL, Cosmos DB, Key Vault"),
              ("database", "Self-managed databases", "PostgreSQL, MySQL, MariaDB, SQL Server, MongoDB"),
              ("folders", "SaaS apps", "Google Workspace Drive, Salesforce")],
        shot=D("getting-started", "images", "dspm", "preview", "dspm-proto-configure-s3.png"), shot_h=2.76,
        caption="Formats: CSV, Excel, Parquet, JSON, XML, PDF, Office, OCR images, archives.",
        note="Not supported today: Google Cloud Storage, SMB and NFS shares, Oracle Database, Snowflake."),
    tech=dict(
        kicker="Rows never touch disk. Only a findings file leaves the region.",
        cols=[("Sources", [("bucket", "S3, Blob, ADLS Gen2", False), ("database", "RDS, Azure SQL, Cosmos", False),
                           ("database", "Self-managed DBs", False), ("folders", "Drive, Salesforce", False),
                           ("key", "Secrets Manager, Key Vault", False)]),
              ("Scan in region", [("server", "VM, systemd timers", False), ("container", "Kubernetes CronJob", False),
                                  ("bolt", "Event-driven Lambda", False), ("file-search", "Parse files, OCR", False),
                                  ("filter", "10,000 rows, 100 MB", False)]),
              ("Act", [("device-desktop", "Console findings", False), ("clock", "Severity and SLA", False),
                       ("jira-original", "Create ticket", True), ("message-chatbot", "Ask AI", False),
                       ("gavel", "Framework filter", False)])],
        cp_title="Classify, then report",
        cp_rows=[("fingerprint", "Classify in memory,", "283 data classes"), ("target", "Confidence tier", "per finding"),
                 ("eye-off", "Mask matches to the", "last 4 characters"), ("upload", "One findings file per", "store, over HTTPS")]),
    deploy=dict(
        kicker="One read-only scanner per region, with no inbound ports", env="Your account, in the data's region",
        rows=[("server", False, "Scanner host", "Linux with Docker or Podman, about 20 GB disk"),
              ("cpu", False, "Sizing", "4 vCPU, 8 GB for one store. 8 vCPU, 32 GB for four"),
              ("lock", False, "Read-only grants", "Storage Blob Data Reader, pg_read_all_data, db_datareader"),
              ("network", False, "Network", "No inbound. Outbound 443 to console and registry"),
              ("hierarchy-2", False, "One instance per store", "A failure in one store never touches another")],
        cp_lines=["Receives findings only", "SaaS, on-prem or", "air-gapped console", "Assets show in minutes"],
        note=["On-prem console: nothing", "leaves your boundary"]),
    usecases=dict(
        kicker="Six scenarios built from the DSPM help pages",
        cards=[("gavel", "Scope a compliance audit", "Filter findings by GDPR, PCI DSS, HIPAA or DPDP", "Compliance"),
               ("key", "Find plaintext secrets", "114 credential and secret classes, cloud keys included", "Secrets"),
               ("lock-open", "Scan public buckets", "Put every publicly exposed S3 bucket in scope", "Exposure"),
               ("bolt", "Scan objects as they land", "Event-driven mode on S3 events, SQS or DynamoDB", "Event-driven"),
               ("building-bank", "Keep data sovereign", "Run scanner and console on-prem or air-gapped", "Sovereignty"),
               ("world", "Show data residency", "Map sensitive records by region", "Residency")]),
    poc=dict(
        kicker="Five onboarding steps, then findings in the console on day 1",
        steps=[("key", "Step 1", "Token, label, VM"), ("lock", "Step 2", "Read-only grants"),
               ("settings", "Step 3", "One file per store"), ("player-play", "Step 4", "First run, upload")],
        pills=[("Day 1: first findings", PRIMARY, WHITE), ("Critical SLA: 10 days", LAV, NAVY)],
        tests=[("bucket", "S3 scope", "Scope S3 by tag, include public buckets", "PII and PCI findings per bucket"),
               ("database", "Database replica", "Point the scanner at a read replica", "Findings filtered by PCI DSS"),
               ("eye-off", "Evidence masking", "Open the evidence tab of one finding", "Only the last 4 characters show"),
               ("wifi-off", "Boundary check", "Watch the scanner's network traffic", "Outbound 443 only, findings file")]),
    journey=dict(
        kicker="Six screens take a team from a new account to masked evidence",
        steps=[(D("getting-started", "images", "dspm", "preview", "dspm-proto-cloud-accounts.png"), "Connect the account", "Cloud Accounts, Data Security"),
               (D("getting-started", "images", "dspm", "preview", "dspm-proto-configure-s3.png"), "Scope the stores", "S3 by tag, name, public buckets"),
               (D("getting-started", "images", "dspm", "preview", "dspm-proto-dashboard-risk.png"), "Read the dashboard", "Risk, region and coverage"),
               (D("getting-started", "images", "dspm", "preview", "dspm-proto-findings-list.png"), "Triage findings", "Severity, SLA, framework filters"),
               (D("getting-started", "images", "dspm", "preview", "dspm-proto-finding-evidence.png"), "Check the evidence", "Masked values per file"),
               (D("getting-started", "images", "dspm", "preview", "dspm-proto-asset-overview.png"), "Open the asset", "Records, encryption, exposure")]),
    diffs=dict(
        kicker="Your scanner, your region, and a console that can run air-gapped",
        stats=[("283", "Data classes"), ("62", "Country packs, check-digit validated"), ("282", "Classes mapped to clauses")],
        cards=[("building", "Air-gapped console", "Scanner and console on-prem. Nothing leaves"),
               ("lock", "Read-only by design", "No write path, no inbound ports"),
               ("world", "Data stays in region", "Each region runs its own scanner"),
               ("brain", "Model in the container", "Name detection runs inside the scanner"),
               ("eye-off", "Masked by default", "The console shows the last 4 characters"),
               ("hierarchy-2", "Isolated per store", "One failing store never blocks another")]),
    ranking=dict(
        kicker="Where each DSPM scans, and what leaves your environment",
        rows=[["Criterion", "AccuKnox DSPM", "Cyera", "Varonis", "BigID", "IBM Guardium"],
              ["Where scanning runs", "VM or CronJob you own, in region", "Cyera cloud, or outpost in your cloud",
               "Local collectors, analysis in SaaS", "Cloud or local scanners", "Analyzer in your account"],
              ["Where the console lives", "SaaS, on-prem or air-gapped", "SaaS", "SaaS", "SaaS or your Kubernetes", "SaaS"],
              ["What leaves", "Nothing on-prem. One file per store on SaaS", "Metadata and results",
               "Collector metadata", "Nothing when self-hosted", "Metadata"],
              ["Air-gapped", "Yes, console included", "No", "Partial, offline collectors", "Partial, your own Kubernetes", "No"]],
        colw=[1.5, 1.86, 1.46, 1.46, 1.46, 1.46], h=3.2,
        callout="AccuKnox is the only DSPM in this table that ships an air-gapped console."),
    pricing=dict(
        kicker="Priced on data-store scans, from the Cloud SKU calculator",
        unit_big="Data-store\nscans / month",
        unit_sub="Buckets scanned weekly, 4 a month. Warehouse and PaaS databases every 14 days, 2 a month.",
        todo=("Unit price", "The sheet counts scans with no divisor. Sales to confirm."),
        example=[("50 buckets x 4 = 200 scans", False), ("10 PaaS DBs x 2 = 20 scans", False),
                 ("Total: 220 scans / month", True), ("Price per scan unit:", False), ("[Sales to confirm]", False)]),
    notes=dict(
        agenda=AGENDA_NOTE,
        problem="""
Sources, all docs/getting-started/dspm-overview.md unless noted.
DSPM finds sensitive data in buckets, databases and SaaS apps and shows where it sits.
Vendor comparison: Cyera sends metadata and results, Varonis collector metadata, IBM Guardium metadata.
Public and unencrypted stores: finding titles in the product UI, such as A data asset is public, and the asset view with encryption and public-access fields (references/PRODUCT UI/DSPM (Data Security)/asset and finding).
Data classes: 283 total. 117 regional compliance, 114 credentials and secrets, 21 PHI, 19 PII, 10 financial. 282 of 283 map to regulation clauses. 62 country packs.
""",
        overview="""
Scanner is read-only with no write path, runs as a VM or Kubernetes job in the data's region (dspm-overview.md).
Confidence tiers Very likely, Likely, Possible. Possible is never reported alone. Default floor Likely.
Masking: rows and files discarded after classification. Matches cut at 200 characters, console shows the last 4.
Frameworks: GDPR 78 classes, PCI DSS 107, HIPAA 26, DPDP 17, plus CCPA. Each class cites CWE and MITRE ATT&CK.
Region view: dspm-proto-dashboard-region.png in the docs images.
""",
        detail="""
Supported and unsupported sources: docs/getting-started/dspm-overview.md, supported sources table.
DynamoDB works in event-driven mode only. Skipped: archive-tier, page and soft-deleted blobs, Salesforce history, share and feed objects (docs/getting-started/dspm-onboarding.md).
Do not use references/PRODUCT UI/DSPM (Data Security)/arch-diagram.png. It shows GCS, Snowflake, NFS, M365 and Slack, which the docs list as unsupported or do not list.
Do not use onboarding/2.png or onboarding/3.png in that folder. They show an unmasked AWS access key ID.
""",
        tech="""
Pipeline from the dspm-overview.md diagram: databases stream rows to classify in memory. Object stores and SaaS go through parse files first (CSV, Excel, Parquet, JSON, PDF, Office, archives, OCR). Findings file, then HTTPS findings only, then the console.
Sampling: up to 10,000 rows or documents per table, files up to 100 MB. Archives unpacked.
Rows never touch disk. Parsed files sit in memory-backed scratch space.
The diagram says 159 detectors and the text says 283 data classes. The deck uses 283 data classes only.
Name detection uses a language model inside the container. Read-only root filesystem, all capabilities dropped.
Findings upload: one zipped file per store over HTTPS with a bearer token.
""",
        deploy="""
Deployment options: VM with systemd timers (default), Kubernetes CronJob with IRSA or workload identity, event-driven AWS Lambda (dspm-overview.md).
Sizing and network: Linux with Docker or Podman, about 20 GB disk. 4 vCPU and 8 GB for one store, 8 vCPU and 32 GB for four in parallel. No inbound. Outbound 443 to the console and the registry, plus database ports (dspm-onboarding.md).
Grants: Azure Storage Blob Data Reader, Cosmos DB Built-in Data Reader, Key Vault Secrets User. Databases pg_read_all_data and db_datareader. Google Drive domain-wide delegation, read-only scope. Salesforce API Enabled, View All Data, Query All Files. S3: list and read objects, KMS decrypt, instance role plus a read-only role with an external ID. No AWS managed policy names in the docs.
Assets appear within minutes of the first upload (dspm-onboarding.md). On-prem console: nothing leaves your boundary (dspm-overview.md).
""",
        usecases="""
The DSPM docs have no use-case section. These six come from features on dspm-overview.md (framework filter, credential classes, event-driven mode, on-prem console) and docs images (public buckets in dspm-proto-configure-s3.png, region map in dspm-proto-dashboard-region.png).
""",
        poc="""
Steps from docs/getting-started/dspm-onboarding.md: create a token and a label, create the VM with no inbound rules, apply read-only grants, configure shared settings plus one file per store, install and run one instance, follow the log until the upload succeeds.
Day 1: findings in Issues, Findings, under the Data Security Findings filter. Triage Critical and Restricted first, then largest match counts, then oldest against SLA. Critical SLA 10 days.
A few dozen tables take minutes. Archives and OCR take longest. No total POC duration is documented.
""",
        journey="""
All six screens come from docs/getting-started/images/dspm/preview. They are the masked versions of the product screens.""" + JOURNEY_NOTE_TAIL,
        diffs="""
Sources: docs/getting-started/dspm-overview.md. On-prem or air-gapped console, nothing leaves. Read-only, no write path. Data does not cross regions. Language model inside the container. 62 country packs with check-digit validation. 282 of 283 classes map to regulation clauses. One instance per data store, a failure in one never touches another (dspm-onboarding.md).
""",
        ranking="""
Source: comparison table in docs/getting-started/dspm-overview.md. Vendor facts come from public documentation as of September 2026. Varonis self-hosted ends 31 December 2026. The IBM column shows the last documented DSPM analyzer model.
""",
        pricing="""
The Pricing and Sizing sheet has no DSPM divisor in Step 1. The Cloud SKU calculator counts data resources: bucket scans every 7 days (4 a month), data warehouse DBs and PaaS DBs every 14 days (2 a month). Total monthly scans feed AccuKnox Cloud total billable units.
docs/faqs/pricing.md lists no DSPM metric. Sales to confirm the unit before this slide goes out.
""" + PRICE_NOTE),
)


# =========================================================================
API = dict(
    key="api", file="AccuKnox_API_Security.pptx",
    title_drive="AccuKnox API Security - Veracode Briefing",
    cover_title="AccuKnox API Security\nDiscovery, Testing and Protection", cover_sub=SUB, short="API Security",
    agenda_kicker=AGENDA,
    problem=dict(
        kicker="APIs ship faster than anyone documents them, and the undocumented ones carry the risk",
        cards=[("eye-off", "Shadow APIs", "Debug hooks, quick fixes and forgotten routes nobody monitors"),
               ("history", "Zombie APIs", "Old versions still take traffic, often with weaker auth"),
               ("file-text", "Orphan specs", "Documented endpoints that no longer exist mislead testers"),
               ("network", "Blind east-west traffic", "WAFs and perimeter tools miss internal service calls")],
        stats=[("4", "API states tracked"), ("6", "Traffic connectors with guides"),
               ("30 s", "From live traffic to inventory")],
        callout="AccuKnox builds the inventory from live traffic and compares it to the spec you ship."),
    overview=dict(
        kicker="Discover, classify, test and rate-limit every API from live traffic",
        cards=[("search", "Live inventory", "Method, path, bodies and sensitive data, internal or external"),
               ("eye-off", "Shadow, Zombie, Orphan", "Compared against your uploaded OpenAPI spec"),
               ("file-code", "Spec from traffic", "Generates an OpenAPI spec from observed calls"),
               ("fingerprint", "Sensitive data", "PII, PHI and financial data in requests and responses"),
               ("bug", "Active API tests", "The API Scan collector tests a live target URL"),
               ("filter", "Rate limiting", "Per endpoint, per user or IP, global. Block or Alert")],
        logos=["amazonwebservices-original-wordmark", "kubernetes-original", "si-istio", "nginx-original"],
        logos_label="TRAFFIC SOURCES"),
    detail=dict(
        title="Our Solution, Endpoint Risk", kicker="Each endpoint gets a risk score you can sort and act on",
        rows=[("lock-access", "Authentication", "Auth type per endpoint, unauthenticated filter"),
              ("fingerprint", "Sensitive data", "Data class in request and response parameters"),
              ("world", "Exposure", "External or internal, public accessibility"),
              ("clock", "Recent discovery", "New endpoints count toward risk"),
              ("folders", "Collections", "Auto-grouped by host, custom rules by regex or method")],
        shot=U("API security", "4.png"), shot_h=2.5,
        stats=[("50", "Endpoints per unit"), ("3 MB", "Spec upload limit"), ("30 s", "Traffic to inventory")]),
    tech=dict(
        kicker="Connectors stream API calls. AccuKnox builds inventory, risk and findings.",
        cols=[("Sources", [("amazonwebservices-original-wordmark", "AWS API Gateway", True), ("kubernetes-original", "Kubernetes API proxy", True),
                           ("si-istio", "Istio sidecar, gateway", True), ("nginx-original", "NGINX Ingress", True),
                           ("api", "Kong, F5 BIG-IP", False), ("file-code", "OpenAPI specs", False)]),
              ("Collect", [("cloud", "CloudWatch to Lambda", False), ("plug-connected", "SentryFlow events", False),
                           ("puzzle", "Envoy WASM filter", False), ("plug", "Kong log plugin", False),
                           ("route", "F5 iRule over HSL", False), ("upload", "Spec upload, 3 MB", False)]),
              ("Act", [("bug", "API Scan tests", False), ("filter", "Rate-limit policy", False),
                       ("alert-triangle", "Findings, severity", False), ("jira-original", "Jira tickets", True),
                       ("report-analytics", "Reports", False)])],
        cp_title="AccuKnox control plane",
        cp_rows=[("list-details", "Inventory and", "collections"), ("eye-off", "Shadow, Zombie and", "Orphan detection"),
                 ("fingerprint", "Sensitive data", "classification"), ("chart-bar", "Risk score per", "endpoint")]),
    deploy=dict(
        kicker="One connector per traffic source, and no code change in the app", env="Your API traffic paths",
        rows=[("amazonwebservices-original-wordmark", True, "AWS API Gateway", "Two CloudFormation stacks, one per stage. REST and HTTP"),
              ("kubernetes-original", True, "Kubernetes proxy", "SentryFlow in its own namespace. Kubernetes 1.28+"),
              ("si-istio", True, "Istio", "Helm adds WasmPlugins for sidecar and gateway"),
              ("api", False, "Kong", "Helm adds the sentryflow-log plugin to Kong"),
              ("route", False, "F5 BIG-IP", "An iRule streams calls to a sentryflow pool")],
        cp_lines=["Endpoints deduplicated", "across all sources", "SaaS, on-prem or", "air-gapped"],
        note=["Logs reach the console", "in 30 s to 1 minute"]),
    usecases=dict(
        kicker="Six scenarios, each from an AccuKnox help page",
        cards=[("search", "Real-time API inventory", "A live list of every endpoint, by host", "Inventory"),
               ("eye-off", "Shadow and zombie APIs", "Compare live traffic to the uploaded spec", "Spec drift"),
               ("fingerprint", "Sensitive data exposure", "Find PII and card data in responses", "Data"),
               ("file-code", "Spec from traffic", "Generate OpenAPI for undocumented services", "Docs"),
               ("filter", "Rate limiting", "Block or alert per user, IP or endpoint", "Protection"),
               ("bug", "Active API testing", "Scan a live URL with the API Scan collector", "Testing")]),
    poc=dict(
        kicker="Two onboarding paths, both with findings on day 1",
        steps=[("upload", "Path 1", "Upload a spec"), ("scan", "Path 1", "Scan, read findings"),
               ("plug-connected", "Path 2", "Add a collector"), ("bug", "Path 2", "Test a live URL")],
        pills=[("SaaS: 1 to 2 weeks", PRIMARY, WHITE), ("Traffic in 30 s", LAV, NAVY)],
        tests=[("file-code", "Spec drift", "Upload an OpenAPI spec and run a scan", "Shadow and Orphan APIs by severity"),
               ("bug", "Active test", "Point API Scan at a live target URL", "Findings per endpoint, 154 in the doc"),
               ("plug-connected", "Live traffic", "Connect Istio or AWS API Gateway", "Inventory fills in 30 s to 1 min"),
               ("fingerprint", "Data exposure", "Filter to unauthenticated and sensitive", "Endpoints leaking data with no auth")]),
    journey=dict(
        kicker="Six screens take a team from live traffic to a ranked finding",
        steps=[(U("API security", "3.png"), "See the inventory", "Discovered APIs, sensitive data"),
               (U("API security", "4.png"), "Open an endpoint", "Sensitive params and risk factors"),
               (U("API security", "7.png"), "Group collections", "Collections created by host"),
               (D("how-to", "images", "api-sec-onboarding", "03-upload-specifications-dialog.png"), "Upload a spec", "OpenAPI JSON or YAML, 3 MB"),
               (D("how-to", "images", "api-sec-onboarding", "06-new-scan-form.png"), "Run a scan", "On-demand or scheduled"),
               (D("how-to", "images", "api-sec-onboarding", "08-api-security-findings.png"), "Act on findings", "Shadow and Orphan APIs")]),
    diffs=dict(
        kicker="Live traffic, no code change, and one price per endpoint",
        stats=[("50", "Unique endpoints per unit, not per call"), ("6", "Traffic connectors with guides"),
               ("4", "Compliance mappings")],
        cards=[("code", "No code change", "Connectors read traffic at the gateway or mesh"),
               ("currency-dollar", "Fair billing", "Endpoints deduplicated across gateways"),
               ("shield-lock", "Runtime enforcement", "KubeArmor links API access to KIEM and RBAC"),
               ("certificate", "Compliance mapping", "PCI DSS 4.0.1, HIPAA, GDPR and DORA"),
               ("wifi-off", "On-prem and air-gapped", "Full control plane on a single node"),
               ("filter", "Built-in rate limits", "Block or alert at three scopes")]),
    ranking=dict(
        kicker="API rows from the AccuKnox battlecards against Invicti and Prisma Cloud",
        rows=[["Capability", "AccuKnox", "Invicti", "Prisma Cloud Enterprise"],
              ["API inventory and detection", "Yes", "Partial, scan-time only", "Not compared"],
              ["Runtime API monitoring", "Yes", "No", "Not compared"],
              ["North-south, NGINX Ingress", "Yes", "Not compared", "Limited"],
              ["TLS classification at ingress", "Yes", "Not compared", "Limited"],
              ["Sensitive data in APIs", "Yes", "Not compared", "Yes"],
              ["Shadow API detection", "Yes", "Not compared", "Yes"],
              ["Zombie API detection", "Yes", "Not compared", "Limited"]],
        colw=[3.0, 1.8, 2.2, 2.2], h=3.2,
        callout="AccuKnox covers runtime monitoring and zombie APIs, where these alternatives are partial."),
    pricing=dict(
        kicker="Priced on unique endpoints, not on traffic",
        unit_big="50 endpoints\n= 1 unit",
        unit_sub="An endpoint called 1M times a day counts once. Seen in two gateways, it still counts once.",
        unit_rows=["No traffic-volume fees", "Dedupe across all sources", "No hard stop above quota"],
        example=[("5,000 unique endpoints", False), ("= 100 units, Tier 2", False), ("$34 x 100 units", False),
                 ("$3,400 / month", True), ("$40,800 / year", False)]),
    notes=dict(
        agenda=AGENDA_NOTE,
        problem="""
Sources: docs/faqs/api-sec.md Q4 for shadow, zombie and orphan definitions. Q2 and Q7 for WAF and perimeter tools missing encrypted east-west traffic.
The same FAQ says 68 percent of organizations lack visibility into shadow APIs, with no source. It is left off the slide.
Four states: docs/use-cases/api-security.md. Connectors with guides: AWS API Gateway, Kubernetes proxy, Istio, NGINX Ingress, Kong, F5 BIG-IP (docs/integrations). Logs reach SaaS in 30 seconds to 1 minute (docs/integrations/api-istio.md).
Note: the zombie definition differs between docs/use-cases/api-security.md and the FAQ. Use the FAQ wording, deprecated versions that still take live calls.
""",
        overview="""
Inventory, Shadow, Zombie, Orphan, Active, collections and rate limiting (docs/use-cases/api-security.md).
Spec generation from traffic (docs/getting-started/3.4-release.md).
API Scan collector under Settings, Collectors, Web Application DAST Scan (docs/how-to/api-security-onboarding.md).
Rate limiting scopes per user or IP per endpoint, per user or IP global, and global service, with Block or Alert. In v3.5 the policies are YAML, with no UI builder yet (docs/getting-started/3.5-release.md).
Do not claim eBPF API capture. The API Security eBPF Collector is listed as in progress (3.5-release.md).
""",
        detail="""
Risk scoring by auth type, sensitive data, exposure, category and OWASP patterns (docs/faqs/api-sec.md Q10).
The UI Contribution to Risk panel lists data sensitivity, presence of sensitive data, recent discovery and public accessibility (references/PRODUCT UI/API security/4.png).
Spec files JSON, YAML or YML up to 3 MB (docs/how-to/api-security-onboarding.md).
Do not use API security/5.png or 6.png. 5.png shows a competitor's demo domain. 6.png shows a full bearer token.
""",
        tech="""
AWS API Gateway: base stack creates the IAM role. A standard stack per stage creates a CloudWatch Log Group and a Lambda that forwards logs (docs/integrations/api-aws.md).
Kubernetes proxy: SentryFlow in the sentryflow namespace exports API events over gRPC (docs/integrations/api-k8s.md).
Istio: WasmPlugins for sidecar and gateway plus an EnvoyFilter (docs/integrations/api-istio.md).
Kong: sentryflow-log Lua plugin posts events to SentryFlow (docs/integrations/kong.md).
F5 BIG-IP: TCL iRule streams over HSL to a sentryflow pool, bodies capped at 10,000 bytes (docs/integrations/f5.md).
NGINX Ingress doc is pulled from the SentryFlow repo at build time (docs/integrations/api-nginx.md).
""",
        deploy="""
Kubernetes proxy needs Kubernetes 1.28 and kubectl 1.28 or later (docs/integrations/api-k8s.md).
Istio: Helm chart with the istio receiver enabled. The cluster must already be onboarded (docs/integrations/api-istio.md).
Kong: Helm 3, AccuKnox agents, chart v0.1.8 or later (docs/integrations/kong.md). F5: node, pool, iRule, virtual server, then Helm with the f5BigIp receiver (docs/integrations/f5.md).
No code change: docs/faqs/api-sec.md Q2 and Q7. Endpoint dedupe across integrations: Q11.
The discovery-engine config key differs between the Istio and Kong docs. Check before a POC.
""",
        usecases="""
Sources: docs/use-cases/api-security.md (inventory, spec drift, rate limiting), references/technical-reference/decks/accuknox-dast-deck-2026-06.pptx slide 15 (sensitive data exposure), docs/getting-started/3.4-release.md (spec from traffic), docs/how-to/api-security-onboarding.md (API Scan collector).
""",
        poc="""
Path 1, spec scan: API Specification, Upload, Scan, New Scan, wait for Complete, open Findings. The doc image shows Shadow APIs rated Critical and Orphan APIs rated Low (docs/how-to/images/api-sec-onboarding/08-api-security-findings.png).
Path 2, collector: the Findings column shows 154 in the doc example (14-collectors-findings-column.png, 15-collector-findings.png).
Prerequisite: a label. A traffic connector is optional (docs/how-to/api-security-onboarding.md).
SaaS POC 1 to 2 weeks (docs/faqs/deployment.md Q7). Logs reach SaaS in 30 seconds to 1 minute (docs/integrations/api-istio.md).
""",
        journey="""
1 Inventory (3.png). 2 Endpoint detail (4.png). 3 Collections (7.png). 4 Spec upload, 5 New scan, 6 Findings from docs/how-to/images/api-sec-onboarding.""" + JOURNEY_NOTE_TAIL,
        diffs="""
Sources: docs/faqs/api-sec.md. No code changes (Q2, Q7). Billing per unique endpoint, deduplicated (Q11). KubeArmor enforcement linked to KIEM and RBAC (Q14). PCI DSS 4.0.1, HIPAA, GDPR and DORA mapping (Q1).
Single-node install of the full control plane (docs/getting-started/3.3-release.md). On-prem and air-gapped (accuknox-dast-deck-2026-06.pptx slide 13).
""",
        ranking="""
Invicti rows: references/competitive/battlecards/accuknox-vs-invicti-appsec.xlsx.
Prisma Cloud rows: references/competitive/battlecards/prisma-enterprise/Accuknox-vs-Prisma-Enterprise-Comparison.md.
Not compared means the source file has no row for that vendor. There is no sourced comparison against Salt, Traceable, Noname, Akamai or 42Crunch.
""",
        pricing="""
Units: API Security 50 endpoints per unit (Pricing and Sizing sheet, Step 1). Billing by unique endpoint, not traffic. Endpoints seen in NGINX and Istio count once (docs/faqs/api-sec.md Q11).
docs/faqs/pricing.md says Bundle of per 1000 APIs, which conflicts with 50 per unit. The sheet is the newer source.
How path parameters are normalized into endpoints is not documented.
Example: 5,000 endpoints, 100 units, Tier 2, 34 dollars, 3,400 dollars a month, 40,800 a year.
""" + PRICE_NOTE),
)

ALL = [CONTAINER, CSPM, DSPM, API]


# =========================================================================
# Links. Help docs and platform pages only, each checked for HTTP 200 on 2026-10-03.
# Blogs and videos wait for approval from Atharva before they go in.
H = "https://help.accuknox.com/"
W = "https://accuknox.com/"
RED = r"D:\AccuKnox\doc-ppt-template\work\veracode\redacted"

CONTAINER["links"] = {
    "agenda": [W + "platform/container-security", H + "use-cases/cwpp/"],
    "problem": [W + "platform/runtime-security", H + "faqs/runtime-security/"],
    "overview": [W + "platform/container-security", W + "platform/cwpp", W + "platform/kspm"],
    "detail": [H + "use-cases/zero-trust/", H + "use-cases/cwpp/"],
    "tech": [H + "support-matrix/cicd-support-matrix/", H + "support-matrix/registry/", H + "support-matrix/iac/"],
    "deploy": [H + "how-to/cluster-onboarding/", H + "getting-started/deployment-models/"],
    "usecases": [H + "use-cases/image-scan/", H + "use-cases/iac-scan/", H + "use-cases/admission-controller-knoxguard/"],
    "poc": [H + "use-cases/hardening/", H + "use-cases/container-scan/"],
    "journey": [H + "how-to/cluster-onboarding/", W + "platform/kubernetes-security"],
    "diffs": [W + "differentiators", W + "platform/runtime-security"],
    "ranking": [W + "platform/cwpp", W + "differentiators"],
    "pricing": [H + "faqs/pricing/"],
}
CSPM["links"] = {
    "agenda": [W + "platform/cspm", H + "use-cases/cspm/"],
    "problem": [W + "platform/cspm", H + "use-cases/cloud-misconfigurations/"],
    "overview": [W + "platform/cspm", W + "platform/cdr", H + "use-cases/asset-inventory/"],
    "detail": [W + "platform/compliance", H + "use-cases/compliance/", H + "support-matrix/compliance-matrix/"],
    "tech": [H + "use-cases/cdr/", H + "use-cases/cspm/"],
    "deploy": [H + "how-to/aws-onboarding/", H + "how-to/cspm-permissions-overview/"],
    "usecases": [H + "use-cases/asset-inventory/", H + "use-cases/cloud-misconfigurations/", H + "use-cases/cdr/"],
    "poc": [H + "faqs/cspm/", H + "how-to/aws-onboarding/"],
    "journey": [W + "platform/cspm", H + "use-cases/compliance/"],
    "diffs": [W + "differentiators", W + "platform/multi-cloud-security"],
    "ranking": [W + "platform/cspm", W + "differentiators"],
    "pricing": [H + "resources/asset-billable-check/", H + "faqs/pricing/"],
}
DSPM["links"] = {k: v for k, v in {
    "agenda": [W + "platform/dspm", H + "getting-started/dspm-overview/"],
    "problem": [W + "platform/dspm"],
    "overview": [W + "platform/dspm", H + "getting-started/dspm-overview/"],
    "detail": [H + "getting-started/dspm-overview/"],
    "tech": [H + "getting-started/dspm-overview/"],
    "deploy": [H + "getting-started/dspm-onboarding/", H + "getting-started/deployment-models/"],
    "usecases": [W + "platform/dspm", H + "getting-started/dspm-overview/"],
    "poc": [H + "getting-started/dspm-onboarding/"],
    "journey": [H + "getting-started/dspm-onboarding/"],
    "diffs": [W + "differentiators", W + "platform/dspm"],
    "ranking": [H + "getting-started/dspm-overview/"],
    "pricing": [H + "faqs/pricing/"],
}.items()}
API["links"] = {
    "agenda": [W + "platform/api-security", H + "use-cases/api-security/"],
    "problem": [W + "platform/api-security", H + "faqs/api-sec/"],
    "overview": [W + "platform/api-security", H + "use-cases/api-security/"],
    "detail": [H + "use-cases/api-security/"],
    "tech": [H + "integrations/api-overview/"],
    "deploy": [H + "integrations/api-overview/", H + "getting-started/deployment-models/"],
    "usecases": [H + "use-cases/api-security/", H + "how-to/api-security-onboarding/"],
    "poc": [H + "how-to/api-security-onboarding/"],
    "journey": [H + "how-to/api-security-onboarding/", W + "platform/api-security"],
    "diffs": [W + "differentiators", W + "platform/api-security"],
    "ranking": [W + "platform/api-security"],
    "pricing": [H + "faqs/api-sec/", H + "faqs/pricing/"],
}

# Blurred screenshots go back in. Sensitive values are blurred, never shown.
DSPM["journey"]["steps"][0] = (os.path.join(RED, "dspm_onboarding_2.png"), "Connect the account", "Data Security sources per account")
DSPM["journey"]["steps"][1] = (os.path.join(RED, "dspm_onboarding_3.png"), "Scope the stores", "S3 by tag, name, public buckets")
DSPM["notes"]["journey"] += ("\nScreens 1 and 2 come from references/PRODUCT UI/DSPM (Data Security)/onboarding/2.png and 3.png."
                            " The AWS access key ID is blurred. Screens 3 to 6 come from docs/getting-started/images/dspm/preview.")
API["journey"]["steps"][1] = (os.path.join(RED, "api_5.png"), "Inspect a call", "Request and response per endpoint")
API["journey"]["steps"][2] = (os.path.join(RED, "api_6.png"), "Read the metadata", "Headers and auth per call")
API["notes"]["journey"] += ("\nScreens 2 and 3 come from references/PRODUCT UI/API security/5.png and 6.png. The demo target domain,"
                           " session token, bearer token, client IPs, staging hostname and tenant IDs are blurred.")
