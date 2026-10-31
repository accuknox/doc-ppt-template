## Slide 1

Airtel DSPM PoC Plan.

PI data discovery on Airtel Cloud, 7 to 21 October 2026.

## Slide 2

Table of Contents.

AIRTEL DSPM POC PLAN.

01.

Scope.

What is in and out.

Slide 3.

02.

Architecture.

Layout and prerequisites.

Slides 4 and 5.

03.

Onboarding.

Five steps, two screens.

Slides 6 to 8.

04.

Use Cases.

Six tests that close the PoC.

Slides 9 to 15.

05.

Timeline.

7 to 21 October.

Slide 16.

06.

Resources.

Docs, platform, micro deck.

Slide 17.

Six parts. Each tile links to its first slide.
1. Scope: which Airtel data stores the PoC covers, which need work, which sit outside. Slide 3.
2. Architecture and prerequisites: the draft layout from the scoping call and what Airtel provides. Slides 4 and 5.
3. Onboarding: five steps from token to first findings, then two console screens. Slides 6 to 8.
4. Use cases: six tests with pass conditions, then one full screen per use case. Slides 9 to 15.
5. Timeline: two weeks from Wednesday 7 October. Slide 16.
6. Resources: help pages, platform page and the micro deck. Slide 17.

## Slide 3

The PoC Scans Seven Data Store Types on Airtel's OpenStack.

SCOPE.

IN SCOPE.

VM files.

On OpenStack.

PostgreSQL.

Version 16 and later.

MySQL.

Self-managed.

MariaDB.

Self-managed.

SQL Server.

Self-managed.

MongoDB.

Document store.

Google Drive.

SaaS, read-only.

Any host.

Same DB versions.

NEEDS A CONNECTOR.

NetApp ONTAP S3
Custom connector. Ayush to confirm the build date..

OUT OF SCOPE.

Public cloud assets.

Airtel is on-prem.

SharePoint and M365 PI.

No PI scanning today.

Goal: prove PI discovery on-prem, as RBI expects for Airtel's NBFC tenants..

Airtel runs OpenStack only. OpenShift came up in earlier notes by mistake. Neither Rahul nor Ayush recall it being discussed, so it is removed.
In scope, from the scoping call:
VM file systems on OpenStack.
Structured databases: PostgreSQL 16 and later (Airtel runs 16.x, which is compatible), MySQL, MariaDB, SQL Server.
Document database: MongoDB.
SaaS: Google Drive. Support already exists.
The connector works at the database level. Any cloud or on-prem host that runs a supported database version is covered.
Needs work: NetApp ONTAP S3 buckets. Airtel wants them scanned. This needs a custom connector. Ayush said it can be built but gave no date.
Out of scope: AWS and other public cloud assets, because Airtel is on-prem. SharePoint and Office 365 PI scanning: Airtel asked, AccuKnox has no PI scanning for Microsoft 365 today. Microsoft support covers compliance use cases only.
Why this matters to Airtel: NBFC tenants need PI data discovery and protection to meet RBI guidelines.

## Slide 4

The DSPM Scanner and Control Plane Both Run Inside Airtel.

POC ARCHITECTURE, DRAFT FROM THE SCOPING CALL.

Draft from the scoping call.
Adapt Ayush's diagram and confirm the registry placement before sending..

Draft layout from the scoping call. Not a finalized deployment design. Adapt Ayush's existing diagram, shared on Slack, before sending.
Boundary: Airtel on-prem, private cloud.
Inside OpenStack: VM file systems, the supported databases (PostgreSQL 16+, MySQL, MariaDB, SQL Server, MongoDB), and NetApp ONTAP S3 buckets.
NetApp ONTAP S3 needs a custom connector. Its readiness is not confirmed.
The AccuKnox DSPM scanner runs as a VM for this PoC. VM is the chosen path. Kubernetes is the other option. A third option is deferred to a later phase.
From the help docs: the scanner has read-only access, no inbound connections, and sends one findings file per data store.
AccuKnox control plane: in Airtel's environment, as Rahul requested. It holds the AccuKnox console.
Network: outbound HTTPS on port 443 from the scanner to the AccuKnox console.
Container registry: it appears in Ayush's existing diagram. The call did not settle where it sits in the VM-only version, so its placement needs confirmation.
Google Drive is SaaS, so the scanner reaches it through the Drive API with the read-only Drive scope.

## Slide 5

Airtel Provides 2 Nodes With 16 vCPU and 64 GB RAM Each.

PREREQUISITES DISCUSSED ON THE SCOPING CALL.

2 nodes.

On-prem compute.

16 vCPU.

Per node.

64 GB RAM.

Per node.

Port 443.

Outbound to the console.

Deployment mode needs confirmation
Rahul gave this spec as a 2-node Kubernetes cluster. Ayush set VM only for the PoC. Confirm before sending..

ALSO NEEDED, FROM THE ONBOARDING GUIDE.

Scanner VM.

Linux, Docker or Podman.

DB logins.

Read-only, one per DB.

Drive access.

Read-only account.

Console token.

Token and one label.

Ready these by Wednesday 7 October. Deployment then takes 2 days..

Discussed on the scoping call.
On-prem compute: Rahul specified 2 nodes, each with 16 vCPUs and 64 GB RAM. He described it as an on-prem Kubernetes cluster prerequisite.
Network: outbound access on port 443 to the AccuKnox console.
Deployment mode needs confirmation. Ayush later said the PoC uses VM deployment only. The team did not reconcile that with the 2-node Kubernetes prerequisite. Do not present the cluster spec as the confirmed VM requirement until this is clarified.
Also needed, from the onboarding guide (help.accuknox.com/getting-started/dspm-onboarding/):
Scanner VM: Linux with Docker or Podman, about 20 GB free disk. 4 vCPU and 8 GB RAM scan one data store at a time. 8 vCPU and 32 GB RAM scan four in parallel.
Database ports open from the scanner to the data subnets. No inbound connections.
A read-only login per database, for example pg_read_all_data on PostgreSQL or db_datareader on SQL Server, and a read-only MongoDB user.
Google Drive: a GCP service account with domain-wide delegation and the single read-only Drive scope.
Console: an artifact token and one label per scanner instance.

## Slide 6

Five Steps Take a Data Store From Zero to First Findings.

ONBOARDING.

STEP 1.

Token and label.

Create an artifact token and one label per scanner.

→.

STEP 2.

Scanner VM.

Linux VM on OpenStack, no inbound rules.

→.

STEP 3.

Read-only grants.

One read-only login per data store.

→.

STEP 4.

Configure.

Console URL, token, India country pack.

→.

STEP 5.

First scan.

Run the installer, watch the first upload.

The next two slides show the console screens at full size..

Step 1, token and label. In the AccuKnox console go to Settings, Tokens and create an artifact token. Create one label per scanner instance.
Step 2, scanner VM. Create a Linux VM in a private subnet on OpenStack. Allow no inbound rules. Install Docker, then pull the scanner image.
Step 3, read-only grants. Apply the grant for each data store. Every grant is read-only.
Step 4, configure. Copy the deployment kit to the VM. Set the console URL, the artifact token and the country packs (IN for Aadhaar, PAN and GST) in the shared settings file. Add one instance file per data store.
Step 5, install and first scan. Run the installer once. It creates a nightly timer per instance. Start one instance by hand and follow its log until the upload succeeds. Findings appear in the console within minutes.
The next two slides show the console screens. Ayush is sending the Airtel OpenStack versions.
Source: Onboard the DSPM Scanner.

## Slide 7

Onboarding Starts in Cloud Accounts With Onboard Account.

ONBOARDING SCREEN 1 OF 2.

Settings, then Cloud Accounts.

Click Onboard Account.

Pick the cloud type.

Airtel's OpenStack shows as a connected account..

Console path: Settings, Cloud Accounts, Onboard Account, Select Cloud Type.
The list shows each onboarded account with its configured scans, such as CSPM and DSPM, and its connection status.
This screen is from the current build. Its Private Cloud tile names Red Hat OpenShift and Nutanix. Airtel runs OpenStack only, so Ayush is sending the OpenStack version of this screen.
Source: image (4).png, shared for this deck.

## Slide 8

Each Data Source Gets a Read-Only Connection and a Scanner.

ONBOARDING SCREEN 2 OF 2.

WHAT TO CHECK.

Add each data source.

Create the access token.

Deploy the DSPM engine.

PASS WHEN
The engine reports its first scan to the console..

Step 4 of 4 in the onboarding wizard: Data Sources.
Top: add data sources. Each source has its own connection settings.
Bottom: deploy the DSPM engine. Create an access token, download the deployment scripts, run the script, then add the engine instance IDs so AccuKnox can tell whether the engine runs.
This screen shows the AWS flow. On Airtel, the engine is the scanner VM on OpenStack. Ayush is sending the OpenStack screens.
Source: image (3).png, shared for this deck.

## Slide 9

Six Use Cases Decide Whether the PoC Passes.

USE CASES AND SUCCESS CRITERIA.

01.

Find every data store.

Each store shows as an asset.

Screen on slide 10.

02.

Find Indian PI.

Seeded Aadhaar, PAN found.

Screen on slide 11.

03.

Prove each finding.

Path and data type shown.

Screen on slide 12.

04.

See risk on one view.

Alerts by severity, top assets.

Screen on slide 13.

05.

Map to regulation.

DPDP filter lists the assets.

Screen on slide 14.

06.

Fix and close.

One Critical finding ticketed.

Screen on slide 15.

Each use case is a success criterion. The PoC passes when all six pass. Each tile links to its full-size screen.
1. Find every data store. Each in-scope store appears as an asset, with total risks, sensitive records by data type, tags, file types and security configuration.
2. Find Indian PI. The India country pack covers Aadhaar, PAN and GST, each checked with its public check-digit algorithm. Seed test records in PostgreSQL, MySQL, MongoDB and a VM file system before execution starts.
3. Prove each finding. The evidence tab lists each file behind the finding, its type, path and the data types found. The console masks each value to its last four characters.
4. See risk on one view. Data alerts by severity, findings trends, the top 10 data findings, top assets and accounts with findings, and open tickets.
5. Map to regulation. Filter findings by India DPDP Act 2023 and SPDI Rules 2011 (17 data classes). Airtel shares its RBI guidelines so AccuKnox can map them too. The scanner shows where regulated data sits. It does not assess the controls around it.
6. Fix and close. Create Ticket raises a ticket. Severity sets the SLA, 10 days for a Critical finding. After the data is masked, moved or deleted, Last detected stops advancing.
Source: DSPM overview, Product Tour and Compliance Mapping. Onboarding guide, Review Findings.

## Slide 10

Use Case 1 Shows Every Data Store as an Asset With Its Risk.

USE CASE 1 OF 6.

WHAT TO CHECK.

Total risks and sensitive records.

Sensitive data by type, such as Aadhaar.

Security configuration.

PASS WHEN
Every in-scope Airtel store shows as an asset..

Asset overview. Total risks, sensitive records by data type, tags, file types, and security configuration such as encryption and public access. Source: DSPM overview, Product Tour, Assets tab.
Help page: https://help.accuknox.com/getting-started/dspm-overview/#product-tour

## Slide 11

Use Case 2 Finds Indian PI File by File.

USE CASE 2 OF 6.

WHAT TO CHECK.

Each file behind the asset.

File type and path.

Data types found per file.

PASS WHEN
Seeded Aadhaar and PAN show up in each store type..

Asset evidence. The India country pack covers Aadhaar, PAN and GST, each checked with its public check-digit algorithm. Seed test records in PostgreSQL, MySQL, MongoDB and a VM file system before execution starts. Source: DSPM overview, What the Scanner Detects.
Help page: https://help.accuknox.com/getting-started/dspm-overview/#what-the-scanner-detects

## Slide 12

Use Case 3 Proves Each Finding With Its Evidence.

USE CASE 3 OF 6.

WHAT TO CHECK.

Severity, status, occurrence.

Evidence files and data types.

Create Ticket and Ask AI.

PASS WHEN
Each finding shows where the data sits..

Finding evidence. Each file behind the finding, with its type and path, and the sensitive data types found in it. The Data Matches tab shows values masked to their last four characters. Source: DSPM overview, Product Tour, Evidence tab, and Data Privacy.
Help page: https://help.accuknox.com/getting-started/dspm-overview/#data-privacy

## Slide 13

Use Case 4 Puts Data Risk on One Dashboard.

USE CASE 4 OF 6.

WHAT TO CHECK.

Data alerts by severity.

Findings trend over time.

Top 10 data findings.

PASS WHEN
Airtel's stores show on the risk view..

Risk overview. Data alerts by severity, findings trends over time, the top 10 data findings, the assets and accounts with the most findings, open tickets, and data distribution by store type. Source: DSPM overview, Product Tour, Risk tab.
Help page: https://help.accuknox.com/getting-started/dspm-overview/#product-tour

## Slide 14

Use Case 5 Maps Each Finding to Its Regulation.

USE CASE 5 OF 6.

WHAT TO CHECK.

Issue description and risk.

Compliance frameworks.

Recommendation to fix.

PASS WHEN
Findings filter by India DPDP Act 2023..

Finding overview with compliance frameworks and the recommendation. 282 of the 283 data classes carry the regulation clauses they fall under. India DPDP Act 2023 and SPDI Rules 2011 cover 17 data classes. Airtel shares its RBI guidelines so AccuKnox can map them too. The scanner shows where regulated data sits. It does not assess the controls around it. Source: DSPM overview, Compliance Mapping.
Help page: https://help.accuknox.com/getting-started/dspm-overview/#compliance-mapping

## Slide 15

Use Case 6 Turns a Finding Into a Ticket With an SLA.

USE CASE 6 OF 6.

WHAT TO CHECK.

Age, severity, SLA.

Create Ticket, Ask AI.

Status and location.

PASS WHEN
One Critical finding is ticketed and closed..

Finding detail. Callout 1: age, severity, SLA and sensitivity. The SLA is 10 days for a Critical finding. Callout 2: six tabs. Callout 3: Create Ticket and Ask AI. Callout 4: Status and Ignored. Callout 5: Location. After the data is masked, moved or deleted, Last detected stops advancing. Source: Onboard the DSPM Scanner, Review Findings.
Help page: https://help.accuknox.com/getting-started/dspm-onboarding/#review-findings

## Slide 16

Two Weeks Run From 7 October to Readout on 21 October.

TIMELINE.

Dates are a proposal. Airtel confirms them at kickoff on 7 October..

Proposed plan. Working days only, weekends skipped.
Wednesday 7 and Thursday 8 October: on-prem deployment of the control plane and the scanner VM. Two days, per Rahul.
Friday 9 and Monday 12 October: onboarding. Read-only grants, scanner configuration, first scan per data store. First findings land in the console.
Tuesday 13 to Monday 19 October: use case execution. The six use cases on slide 9, with a daily check-in.
Tuesday 20 and Wednesday 21 October: executive report, readout and closure. Go or no go on 21 October.
Dependencies: the VMs, the outbound 443 rule and the read-only logins on slide 5 must be ready on 7 October. NetApp ONTAP S3 joins only if the custom connector lands inside the window.
Airtel has not committed to these dates yet. Confirm at kickoff.

## Slide 17

Six Links Answer Most Questions During the PoC.

RESOURCES.

DSPM overview.

Coverage, detectors, privacy.

Onboarding guide.

Prerequisites to first scan.

DSPM platform page.

accuknox.com/platform/dspm.

DSPM micro deck.

Airtel needs mapped to AccuKnox.

On-prem console.

Nothing leaves your boundary.

Create tokens.

The scanner's artifact token.

Questions during the PoC go to support@accuknox.com..

Every link opens the live page.
DSPM overview: what the scanner covers, supported data stores, the 283 data classes, compliance mapping and data privacy.
Onboard the DSPM scanner: prerequisites, read-only grants per data store, install, first scan and how to review findings.
DSPM platform page on accuknox.com.
AccuKnox DSPM micro deck: the short product deck, with the Airtel requirements mapped to AccuKnox.
Run the console on-premises: the section of the overview that explains the on-prem and air-gapped console.
Create tokens: how to create the artifact token the scanner uses.

## Slide 18

SEE US IN ACTION.

support@accuknox.com.