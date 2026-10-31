
## Slide 1

AccuKnox for VeracodeContainer, IaC, CSPM, DSPMand API Security.
Partner briefing, October 2026.

## Slide 2

Agenda.
SIX PARTS, SLIDES 3 TO 16.
01.
The Problem.
Risk after the commit.
Slide 3.
02.
Our Solution.
Four products, one platform.
Slides 4 to 7.
03.
Architecture.
Technical, deployment, modes.
Slides 8 to 10.
04.
Use Cases and POC.
Scenarios with pass checks.
Slides 11 and 12.
05.
User Journey.
The console, step by step.
Slide 13.
06.
Why AccuKnox.
Differentiators, ranking, pricing.
Slides 14 to 16.

Agenda. Six parts.
Part 1, the problem: risk that appears after the code commit.
Part 2, the four products in scope for Veracode: Container Security and IaC, CSPM, DSPM, API Security.
Part 3, architecture: how findings flow, where each component runs, and the four deployment modes.
Part 4, use cases and POC scenarios with pass checks.
Part 5, the user journey in the AccuKnox console.
Part 6, differentiators, the recommended stack ranking of the four modules, and list pricing.

## Slide 3

The Problem We Solve.
CODE FINDINGS STOP AT THE COMMIT. RISK KEEPS MOVING TO PRODUCTION..
AccuKnox tracks each finding from the first commit to live production, in one console..

Talk track. A code scanner sees the source. After the commit, the same application turns into an IaC template, a container image, a running pod, a cloud account, a data store and a live API. Each stage adds risk that a source scan does not see.
Risks shown, each from a help page:
IaC: public buckets and hardcoded secrets (docs/use-cases/iac-scan.md, docs/support-matrix/iac.md).
CI/CD: vulnerable base images, for example node:18-alpine blocked in GitHub Actions (docs/use-cases/container-scan.md).
Runtime: execution from /tmp and crypto-mining, both POC scenarios (references/technical-reference/playbooks-and-poc/accuknox-container-security-poc-cwpp-kspm.pdf).
Cloud: misconfiguration and drift (docs/use-cases/cloud-misconfigurations.md).
Data: PII and PCI data in exposed buckets (docs/getting-started/dspm-overview.md).
APIs: Shadow, Zombie and Orphan APIs and unauthenticated endpoints (docs/use-cases/api-security.md).
Callout source: accuknox.com/differentiators, "Tracks every finding from first commit to live production".

## Slide 4

Container Security and IaC.
SCAN IN THE PIPELINE, BLOCK AT RUNTIME, RANK CVES BY WHAT REALLY EXECUTES.
Inline runtime blocking.
KubeArmor stops the attack before the process runs.
Runtime Verified CVEs.
Flags CVEs that execute in production, up to 100x less noise.
Registry and CI/CD scans.
8 registries and 10 CI/CD platforms.
IaC scanning in 13 formats.
Terraform, Helm, CloudFormation and more.
Agentless KSPM.
CIS Kubernetes benchmark, KIEM, Pod Security.

Sources.
KubeArmor blocks inline with AppArmor, BPF-LSM and SELinux, before the process runs (docs/faqs/runtime-security.md). KubeArmor is a CNCF Sandbox project, 2M+ downloads (docs/faqs/general.md).
Runtime Verified flag: eBPF telemetry flags vulnerabilities that actually execute in production, CVE noise down by up to 100x (docs/getting-started/3.4-release.md).
Registries, 8: ECR, GAR, ACR, Nexus, Docker Hub, Harbor, Quay, JFrog (docs/support-matrix/registry.md).
CI/CD, 10: GitHub Actions, GitLab, Jenkins, Azure DevOps, AWS CodePipeline, Bitbucket, CircleCI, GCP Cloud Build, Harness, Bamboo (docs/support-matrix/cicd-support-matrix.md). Harness plugins are listed as Coming Soon.
IaC, 13 formats: Terraform HCL, JSON and Plan, Kubernetes YAML, Helm, Dockerfile, CloudFormation, Kustomize, Serverless Framework, Ansible, Bicep, ARM, AWS CDK (docs/support-matrix/iac.md). Finds misconfigurations, hardcoded secrets and drift.
KSPM is agentless: CIS Kubernetes benchmark, KIEM, Pod Security Admission (docs/use-cases/kspm.md).
Admission control: KnoxGuard on Kyverno restricts registries and denies privileged pods. Blocking by vulnerability threshold is in the pipeline, so do not promise it (docs/use-cases/admission-controller-knoxguard.md).
Screenshots: Container Images dashboard and IaC Findings dashboard, demo tenant data (references/PRODUCT UI/1_dashboard).

## Slide 5

Cloud Security Posture (CSPM).
AGENTLESS, READ-ONLY POSTURE AND COMPLIANCE ACROSS EVERY CLOUD ACCOUNT.
40+
Compliance frameworks.
1,500+
Policies and controls.
50+
Cloud asset types.
AWS.
Azure.
GCP.
Oracle.
Agentless onboarding.
Read-only cloud APIs. AWS uses ReadOnlyAccess and SecurityAudit.
One asset inventory.
List and hierarchy views across all clouds.
Misconfig and drift.
Checks against baselines, Monitors on critical assets.
Compliance per control.
Pass rate per control, drill-down per framework.
Tickets and fixes.
Jira, Freshservice, ConnectWise. GitOps pull requests.

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

## Slide 6

Data Security Posture (DSPM).
FIND SENSITIVE DATA WHERE IT LIVES. THE SCANNER STAYS IN YOUR REGION..
Scanner in your region.
VM, Kubernetes CronJob or Lambda. Read-only, no inbound ports.
PII, PHI, PCI and secrets.
Each finding has a confidence tier.
Values stay masked.
Last 4 characters only. Rows discarded after classification.
Mapped to regulations.
GDPR, PCI DSS, HIPAA, CCPA, DPDP, with CWE and MITRE.
283
Data classes.
62
Country packs.
282
Mapped to rules.
DATA SOURCES.
+ Salesforce,Google Drive.

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

## Slide 7

API Security.
DISCOVER EVERY LIVE ENDPOINT, THEN RANK IT BY DATA, AUTH AND EXPOSURE.
TRAFFIC SOURCES WITH SETUP GUIDES.
API Gateway.
K8s proxy.
Istio.
NGINX.
+ Kong,F5 BIG-IP.
Priced on unique endpoints, not traffic. 1 unit is 50 endpoints..
Discover every endpoint.
Method, path, bodies, sensitive data labels.
Shadow and zombie APIs.
Shadow, Zombie, Orphan, Active, against your spec.
Spec from traffic.
Generates an OpenAPI spec from live calls.
Active API tests.
Tests a live target URL for vulnerabilities.
Risk score per API.
Auth, sensitive data, exposure, category.

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

## Slide 8

Technical Architecture.
PARTNER FINDINGS ENTER BY SARIF OR API AND GET THE SAME CORRELATION AS NATIVE ONES.

Walk left to right.
1 Sources. Code scanners export SARIF. AccuKnox imports SARIF from any tool that produces it (docs/getting-started/sarif-findings.md, Universal SARIF Parser in docs/getting-started/3.4-release.md). Checkmarx and Nessus already connect by API (docs/getting-started/accuknox-arch.md).
2 Collect. CLI-based collectors cover secret scanning, SAST, container and vulnerability scanning, DAST and the Kubernetes CIS benchmark. KubeArmor is the only runtime agent. CSPM, CDR and KSPM are agentless (accuknox-control-plane-architecture-review-v3.5.txt).
3 Control plane. Triage dedupes, correlates and enriches. Prioritization uses AI risk scoring (docs/faqs/general.md Q14). Runtime Verified, CISA KEV and EPSS enrich CVEs (docs/getting-started/3.4-release.md). The rules engine raises tickets and notifications (docs/getting-started/accuknox-arch.md). Finding lifecycle: Active, Waiting for Verification, Fixed after 3 scans (docs/how-to/findings-lifecycle.md).
4 Act. Ticketing: Jira Cloud, Jira Server, ServiceNow, Freshservice, ServiceDesk Plus, ConnectWise. SIEM: Splunk, QRadar, Sentinel, CloudWatch, RSyslog, webhook. Notification: Slack, email, webhook (docs/integrations/support-matrix.md).
Integration build times from docs/getting-started/accuknox-arch.md: CLI-based 1 sprint, API-based 2 to 3 weeks, SIEM 1 sprint, ticketing (two-way) 3 to 5 sprints.

## Slide 9

Deployment Architecture.
POSTURE SCANS NEED NO AGENT. ONLY RUNTIME ENFORCEMENT RUNS ONE..
The same components install for SaaS, your cloud, on-premises and air-gapped..

Where each component runs.
Kubernetes: KubeArmor DaemonSet and the KSPM job, both installed by Helm (accuknox-control-plane-architecture-review-v3.5.txt, docs/how-to/cluster-onboarding.md).
CI/CD: image and IaC scans run as pipeline steps. SARIF files upload from the pipeline (docs/support-matrix/cicd-support-matrix.md, docs/getting-started/sarif-findings.md).
Cloud accounts: agentless, read-only. AWS role uses ReadOnlyAccess plus SecurityAudit (docs/faqs/cspm.md).
Data region: DSPM scanner as a VM or Kubernetes CronJob, read-only, no inbound ports (docs/getting-started/dspm-overview.md).
API gateways: AWS API Gateway, Istio, NGINX Ingress, Kong, F5 BIG-IP connectors (docs/integrations).
Control plane: runs on Kubernetes. Data arrives through token-authenticated APIs (docs/getting-started/accuknox-arch.md).
Runtime enforcement keeps working if the control plane goes down (docs/faqs/deployment.md Q3, docs/faqs/general.md Q16).

## Slide 10

Deployment Modes.
RUN ACCUKNOX AS SAAS, IN YOUR CLOUD, ON-PREMISES OR AIR-GAPPED.
SaaS.
Control plane.
AccuKnox cloud.
Setup.
Same day, no install.
Best for.
Fast proof of concept.
Your Cloud.
Control plane.
Your cloud account.
Data egress.
None.
Best for.
Data residency.
On-Premises.
Control plane.
Your servers.
Install.
Native, no SaaS agent.
Best for.
Banking, healthcare, telecom.
Air-Gapped.
Control plane.
Isolated network.
Outbound traffic.
None.
Best for.
Federal, defense, ITAR.
The platform, the policies and the price stay the same in all four modes..

Source: accuknox.com/differentiators, section "Your Cloud. Your data. Your AI.", read 2026-10-03.
Line from the page: Run AccuKnox as SaaS, in your cloud, on premise or air-gapped. The Platform and the policies stay the same.
SaaS: control plane in AccuKnox cloud. Setup the same day, no install. Best for a fast proof of concept. SaaS regions: US, EU, Middle East, India (docs/faqs/deployment.md Q10).
Your Cloud: control plane in your cloud account. Data egress none. Best for data residency. Managed Kubernetes: EKS, AKS, GKE (docs/getting-started/onprem-eks-aks-gke.md).
On-Premises: control plane on your servers. Native install, not a SaaS agent. Best for banking, healthcare, telecom. Single node: 8 vCPU, 32 GB, 256 GB disk (docs/getting-started/on-prem-single-node-installation.md). Multi-node: 3 nodes (docs/getting-started/on-prem-installation-guide.md).
Air-Gapped: control plane in your isolated network. Outbound traffic none. Best for federal, defense, ITAR. All modules stay available (docs/faqs/general.md Q16).
AI CoPilot (AskADA) is SaaS only (docs/getting-started/deployment-models.md).
Pricing: the sample quote says pricing is the same for on-premises and cloud deployment (Pricing and Sizing sheet, SEP 2026).

## Slide 11

Use Cases.
SIX SCENARIOS, EACH TAKEN FROM AN ACCUKNOX HELP PAGE.
Block a vulnerable image.
A GitHub Actions scan stops node:18-alpine before release.
Container.
Catch a public bucket in IaC.
The IaC scan flags a Terraform bucket set to public-read.
IaC.
Close a public S3 bucket.
CSPM finds the bucket. Remediation closes public access.
CSPM.
Find PCI data before an audit.
Scan a database replica, then filter by framework.
DSPM.
Expose shadow APIs.
Upload a spec, scan, and list Shadow and Orphan APIs.
API Security.
One view for partner findings.
Import SARIF from any tool next to native findings.
Platform.

Sources.
1 Container: GitHub Actions scan blocks the vulnerable node:18-alpine image (docs/use-cases/container-scan.md).
2 IaC: IaC scan flags a Terraform S3 bucket set to public-read (docs/use-cases/iac-scan.md).
3 CSPM: misconfigured public S3 bucket walkthrough (docs/use-cases/cloud-misconfigurations.md). Auto-remediation can close public S3 access (docs/faqs/compliance.md).
4 DSPM: point the scanner at a read replica of a production database, then filter findings by framework (docs/getting-started/dspm-onboarding.md, dspm-overview.md).
5 API: upload a spec, run a scan, get Shadow and Orphan endpoints (docs/how-to/api-security-onboarding.md, Path 1).
6 Partner findings: SARIF import from any tool, grouped and filtered by severity, tool name and file location, next to native findings (docs/getting-started/sarif-findings.md).

## Slide 12

POC Scenarios.
A FIVE-DAY SAAS POC, WITH ONE PASS CHECK PER PRODUCT.
Day 1.
Onboard.
→.
Days 2 to 3.
Scan results.
→.
Days 3 to 4.
Asset inventory.
→.
Days 4 to 5.
Findings by category.
SaaS: 1 to 2 weeks.
On-prem: 2 to 3 weeks.
Container.
TEST.
Run /tmp execution and a crypto-miner under a block policy.
PASS CHECK.
Both processes blocked.
CSPM.
TEST.
Onboard read-only, then make one S3 bucket public.
PASS CHECK.
Top 20 ranked by Day 3. Bucket reverted in 60 s.
DSPM.
TEST.
Scope S3 by tag, include public buckets.
PASS CHECK.
PII and PCI findings per bucket.
API Security.
TEST.
Upload an OpenAPI spec and connect a gateway.
PASS CHECK.
Shadow and Orphan APIs listed.

Timeline sources.
Five-day plan: Day 1 onboarding, Days 2 and 3 scan results, Days 3 and 4 asset inventory, Days 4 and 5 findings categorization (docs/faqs/general.md Q19).
Duration: SaaS POC about 1 to 2 weeks, on-prem POC about 2 to 3 weeks, longer for air-gapped (docs/faqs/deployment.md Q7). The FAQ links a POC Checklist Questionnaire.
Scenario sources.
Container: block execution from /tmp and crypto-mining, from the CWPP and KSPM POC guide (references/technical-reference/playbooks-and-poc/accuknox-container-security-poc-cwpp-kspm.pdf). Policies start in audit mode and switch to block (docs/use-cases/cwpp.md).
CSPM: top 20 misconfigurations ranked by Day 3, public S3 bucket reverted within 60 seconds, from the 2-week CSPM POC sprint (references/technical-reference/playbooks-and-poc/cspm-poc-prereq.pdf).
DSPM: scope S3 by tag or name pattern, include public buckets, triage Critical findings first (docs/getting-started/dspm-onboarding.md).
API: Path 1 in docs/how-to/api-security-onboarding.md, upload a spec and scan.
The help docs define no formal POC success criteria. The pass checks come from the POC guides above. Agree final criteria with Veracode before Day 1.

## Slide 13

User Journey in the Console.
SIX SCREENS TAKE A TEAM FROM A NEW SOURCE TO A TICKET.
1.
Add a source.
Collectors for SAST, DAST, images, clouds.
2.
See the posture.
Accounts, clusters, registries, repos.
3.
Walk the assets.
Security graph per cloud asset.
4.
Rank the findings.
Filter by severity, exploit, status.
5.
Score compliance.
Score per framework and account.
6.
Report and ticket.
Scheduled reports, Jira tickets.

Screens from references/PRODUCT UI, demo tenant data. Doc pages for each step:
1 Add a collector: SAST, DAST, host, image and cloud collectors (docs/how-to/sca.md). The picker shows SonarQube, Zap, Nessus, Trivy.
2 Dashboard: accounts, clusters, registries and repos in one view (docs/use-cases/cnapp-security-overview.md).
3 Inventory and security graph (docs/use-cases/asset-inventory.md).
4 Findings: filter by cloud, status, severity, exploit availability, then group and assign (docs/how-to/findings-lifecycle.md).
5 Compliance: average score and passed controls per framework and account (docs/use-cases/compliance.md).
6 Reports: scheduled CSPM, CWPP and ASPM reports (docs/how-to/custom-reports.md). Tickets go to Jira through the rules engine (docs/use-cases/rules-engine-ticket-creation.md).
Ask AI is available on findings (docs/getting-started/3.3-release.md). The Ask AI screenshot shows a user name, so it stays out of the deck.

## Slide 14

Key Differentiators.
PREVENTION FIRST, ONE DATA LAYER, AND ANY DEPLOYMENT.
3 to 5x
Tools replaced.
80%
Alert reduction with runtime context.
40+
Compliance frameworks out of the box.
Inline prevention.
Blocks threats before they run, at the kernel.
Code to cloud.
Tracks each finding from commit to production.
One data layer.
Add a module with no re-integration.
Runs anywhere.
Public, private, on-prem, air-gapped.
Open formats.
SARIF, syslog, CEF and webhooks.
Open source core.
KubeArmor, 2M+ downloads.

Sources.
Stats: 3 to 5x tools replaced, 80% alert reduction, 40+ frameworks (accuknox.com/differentiators). The page says runtime context cuts actionable findings by up to 80 percent.
Inline prevention: blocks threats before execution, zero trust at the kernel level through eBPF (accuknox.com/differentiators). KubeArmor uses AppArmor, BPF-LSM and SELinux (docs/faqs/runtime-security.md).
Code to cloud: every finding tracked from commit to production (accuknox.com/differentiators).
One data layer: CNAPP, API Security and AI Security share one data layer. Start with one module and expand without re-integration (accuknox.com/differentiators).
Runs anywhere: public, private, on-prem and edge from one console. Air-gapped with no telemetry and no call-home (accuknox.com/differentiators). The narrative file calls AccuKnox the only vendor that runs on all public, private and air-gapped clouds (references/source-of-truth/accuknox-summary-and-narrative.md).
Open formats: SARIF, syslog, CEF and MCP connect whole tool categories (docs/integrations/support-matrix.md).
Open source: AccuKnox created and maintains KubeArmor, 2M+ downloads, 1,000+ GitHub stars (docs/faqs/general.md).

## Slide 15

Stack Ranking for Veracode.
RECOMMENDED ORDER TO ADD THE FOUR MODULES NEXT TO CODE FINDINGS.
Rank | Module | Why in this order | Footprint | 1 unit.
1 | Container + IaC | Runs in the same pipelines as code scans | CI plugin, Helm agent | 1 node, 40 images, 30 repos.
2 | API Security | Tests the live endpoints the code becomes | Gateway connector | 50 endpoints.
3 | CSPM | Checks the cloud the code deploys into | Agentless, read-only | 10 assets.
4 | DSPM | Finds the sensitive data behind the app | Scanner in your region | [Sales to confirm].
Start with one module. Add the next one on the same data layer, with no re-integration..

This is AccuKnox's recommended order for a code-scanning partner. It is not a third-party ranking.
Order logic: start where code findings already flow (the pipeline), then the live endpoints the code becomes, then the cloud the code deploys into, then the data behind the application.
Footprint sources: CI plugins and Helm agent (docs/support-matrix/cicd-support-matrix.md, docs/how-to/cluster-onboarding.md). API gateway connectors (docs/integrations). Agentless read-only CSPM (docs/faqs/cspm.md). DSPM scanner in region (docs/getting-started/dspm-overview.md).
Unit sources: Pricing and Sizing sheet SEP 2026, Step 1 units calculator. CWPP and KSPM 1 node per unit. Container images 40 images per unit. SAST, secret scanning and IaC 30 code repos per unit. API Security 50 endpoints per unit. CSPM 10 assets per unit.
The sheet has no unit divisor for DSPM. The Cloud SKU tab counts bucket, data warehouse and PaaS DB scans per month. Sales to confirm the DSPM unit.
Website line: Start with one module and expand without re-integration (accuknox.com/differentiators).

## Slide 16

Pricing.
ONE UNIT PRICE ACROSS MODULES, WITH VOLUME TIERS.
PRICE PER UNIT PER MONTH (USD).
Tier | Units | Price.
1 | 10 to 50 | $40.
2 | 51 to 250 | $34.
3 | 251 to 750 | $29.
4 | 751 to 2,500 | $25.
5 | 2,501 to 5,000 | $21.
6 | 5,001 and up | Negotiated.
WHAT ONE UNIT COVERS.
Module | 1 unit equals.
CSPM | 10 cloud assets.
CWPP and KSPM | 1 node.
Container images | 40 images.
IaC, SAST, secrets | 30 code repos.
API Security | 50 endpoints.
DSPM unit
Not in the sheet. Sales to confirm..
SUPPORT.
Silver: included, 9x5.
Gold: +10%, 12x6.
Platinum: +25%, 24x7.
DEPLOYMENT.
On-premises: $0.
Shared SaaS: $0.
Dedicated tenant: $3,000/mo + 10%.
List prices from the AccuKnox Pricing and Sizing sheet, September 2026. Partner terms are separate..

Source: AccuKnox - Pricing and Sizing - SEP 2026.xlsx, effective August 2026.
Step 2, tiered price per unit per month in USD: Tier 1, 10 to 50 units, 40 dollars. Tier 2, 51 to 250, 34 dollars. Tier 3, 251 to 750, 29 dollars. Tier 4, 751 to 2,500, 25 dollars. Tier 5, 2,501 to 5,000, 21 dollars. Tier 6, 5,001 and up, negotiated. Tier decay 15 percent. INR prices are on the same tab.
Step 1, units: CSPM and CDR 10 assets per unit. CWPP, KSPM and KIEM 1 node per unit. Container image scanning 40 images per unit. SAST, secret scanning and IaC 30 code repos per unit. API Security 50 endpoints per unit.
Step 3, support: Silver included, 9 hours x 5 days. Gold 10 percent of subscription, 12 x 6. Platinum 25 percent, 24 x 7 with a TAM.
Step 5, deployment: On-premises 0 dollars. Shared tenant SaaS 0 dollars. Dedicated tenant 3,000 dollars a month plus 10 percent of subscription.
Professional services: 250 dollars an hour onsite, 125 offsite.
Sample quote terms: 3-year subscription, Net 30, implementation 15 to 45 days from contract.
DSPM has no unit divisor in the sheet. Sales to confirm before this slide goes to Veracode.

## Slide 17

SEE US IN ACTION.
support@accuknox.com.