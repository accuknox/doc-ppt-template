## Slide 1

AccuKnox Secrets ManagerArchitecture and Application Integration

Sampath Bank architecture session, 5 October

## Slide 2

What We Cover Today

AGENDA

01

Architecture

What runs where

Slides 4 to 6

02

Connect Your Apps

Four patterns, code samples

Slides 7 to 11

03

Live Use Case

Password rotation demo

Slide 12

04

HA and DR

Failures, backups, DC1, DC2

Slides 13 and 14

05

Air-Gapped and Day 2

No internet, daily operations

Slides 15 and 16

06

Proof and Next Steps

References and the POC

Slides 17 and 18

Agenda for the session. Six parts.
Part 1 answers the architecture questions from the last session.
Part 2 answers the key question from the application teams: how much work will I have to do?
Part 3 is the live demo: an app on Kubernetes reads a database password that rotates.
Part 4 covers HA inside one data center, and backup and DR across DC1, DC2 and test.
Part 5 covers the air-gapped install and Day 2 operations.
Part 6 covers reference deployments and next steps.
Slide 3 is hidden. It maps each question from the last session to an RFP clause. Unhide it if the bank asks for the mapping.

## Slide 3

Five Questions This Session Answers

YOUR ASKS, MAPPED TO THE RFP

HIDDEN SLIDE. Unhide if the bank wants the RFP mapping on screen.
Sampath Bank does not run a secrets manager today, so this is a new on-premises build.
The target host is the bank's own Tanzu Kubernetes platform, the option RFP 4.19.1 prefers.
Mapping: deploy and where (4.19.1, 4.19.3) on slides 4 and 6. How an app gets a secret (4.1.4, 4.6.1, 4.6.3) on slides 4 and 5.
Developer effort (4.5.2, 4.5.3) on slides 7 to 11. Node or site failure (4.12.1 to 4.12.5, 4.13.3) on slides 13 and 14.
No internet access (4.19.4) on slide 15.

## Slide 4

One Cluster Serves Every Application in the Bank

ARCHITECTURE AT A GLANCE

Walk the diagram left to right.
LEFT, applications. Kubernetes and Tanzu pods get secrets as files from the Agent Injector or the CSI provider. App servers on VMs (WebSphere, WebLogic, Tomcat, .NET on IIS, AIX) call the SDK or the REST API. Jobs, scripts and CI/CD pipelines call the CLI or the REST API. Every call goes over TLS.
MIDDLE, the Secrets Manager cluster in namespace accuknox on the bank's Tanzu cluster.
Auth methods (from the FAQ and the earlier demo): Kubernetes service account, AppRole, OIDC with Entra ID, LDAP, JWT, TLS certificates, tokens, userpass, Okta.
Three server pods in HA mode: one active, two standby. Each has its own Raft integrated storage disk, 10Gi by default. Data replicates between the three nodes. There is no external database to run. Data is encrypted before it reaches disk.
Secret engines: KV v1 and v2, Database (Oracle, MySQL, PostgreSQL shown in the demo), PKI, Transit (encryption as a service), SSH, TOTP, Kubernetes, LDAP.
The Agent Injector (a mutating webhook) and the CSI provider (a DaemonSet) deliver secrets into pods.
AccuKnox CWPP with KubeArmor hardens every Secrets Manager pod at runtime: env var protection, secret and volume-mount protection, limits on lateral movement. The Secrets Manager overview page says AccuKnox CWPP hardens every instance.
RIGHT, bank systems: the identity provider (Entra ID or LDAP), an S3-compatible on-prem bucket for snapshots, the SIEM for the audit log, and Prometheus and Grafana for health.
Source: accuknoxsecretmanager Helm chart 0.28.3 (app v2.5.4), values.yaml and templates. Auth methods and engines: Secrets Manager FAQ and the earlier product demo.

## Slide 5

Every Secret Request Follows the Same Four Steps

HOW AN APP GETS A SECRET

Pods

Kubernetes service account

VM apps and jobs

AppRole or TLS certificate

People

Entra ID (OIDC) or LDAP

The same four steps apply to every pattern: SDK, file, env var or CSI.
Step 1, authenticate. Pods use their Kubernetes service account. VM apps use AppRole or a TLS certificate. People use Entra ID (OIDC) or LDAP.
Step 2, get a token. The token is short-lived and carries one or more ACL policies. A policy names the exact paths an identity can read, for example secret/data/payments/db.
Step 3, read. The app reads only the paths its policy allows. Anything else returns permission denied. Traffic uses TLS.
Step 4, audit. Every request, allowed or denied, goes to the audit log. Turn on audit storage in the chart and forward it to the SIEM.
Revoking a token, or editing the policy, cuts access at once. Revocation lives under Access, Tokens in the UI.
A token that exists before a policy change does not pick up the new policy. The person or app must log in again (Sharing Secrets guide).
RFP links: 4.6.1 (authenticate every entity), 4.6.2 (non-human identities), 4.6.3 (encrypted channel), 4.15.1 (audit logging).

## Slide 6

One Helm Chart Deploys Nine Building Blocks

COMPONENTS TO DEPLOY

Server

Serves the UI and API

Required

Raft storage

Encrypted disk per node, no DB

Required

Services

Send traffic to the leader

Required

Agent Injector

Puts secrets in pods as files

K8s apps

CSI provider

Mounts secrets as a volume

Optional

Snapshot agent

Backs up every 15 minutes

Recommended

Audit storage

Keeps the audit log on its own disk

Recommended

Monitoring

Feeds Prometheus and Grafana

Optional

Guard rails

Ingress, NetworkPolicy, PDB

Optional

Prerequisites (Deployment Guide): Kubernetes 1.30 or later with a default StorageClass, Helm 3, kubectl. Minimum 1 vCPU and 512Mi memory on a single node, and 10Gi of persistent storage.
Details per component, from the chart:
Server: StatefulSet, 3 pods in HA mode (server.ha.enabled, replicas 3). HA is off by default and is switched on in values.yaml. UI and API on port 8200. Image harbor.do.accuknox.com/secrets-manager/ak-secrets-mgr:v2.5.4-amd64.
Raft integrated storage: one PVC per pod, 10Gi default, ReadWriteOnce, mounted at /accuknoxsecretmanager/data. No external database.
Services: active, standby and headless. Cluster traffic between pods on port 8201.
Agent Injector: Deployment plus mutating webhook. Image hashicorp/vault-k8s 1.7.2. Leader election on. Pod anti-affinity by host. Webhook failurePolicy Ignore. Auth path auth/kubernetes.
CSI provider: DaemonSet, off by default (csi.enabled). Needs the Secrets Store CSI Driver installed first. Image accuknoxsecretmanager-csi-provider 2.0.2.
Snapshot agent: CronJob, off by default. Schedule */15 * * * *. Sends to an S3-compatible bucket, expires files after 14 days. Logs in with Kubernetes auth, role snapshot. Image snapshot-agent 0.3.0.
Audit storage: separate PVC, 10Gi default, off by default, mounted at /accuknoxsecretmanager/audit.
Monitoring: ServiceMonitor, PrometheusRules and a Grafana dashboard ship in the chart, all off by default.
Guard rails: Ingress, OpenShift Route or Gateway API routes. NetworkPolicy allows ports 8200 and 8201. PodDisruptionBudget protects quorum.
OpenShift has its own values file, values.openshift.yaml.
Source: accuknoxsecretmanager Helm chart 0.28.3, app v2.5.4.

## Slide 7

Four Ways to Deliver a Secret, Three Need No Code Change

SECRET INTERACTION METHODS

Prefer files over env vars. RFP 4.4.3 asks to keep secrets out of env vars where possible.

Pick the pattern per application. One bank can run all four at the same time.
1. SDK or REST API. The app calls Secrets Manager at start or on demand. The secret stays in memory and never touches disk. It needs a small code change. This was presented as the preferred and most secure option. Fits Java, .NET, Python, Node.js on VMs or Kubernetes.
2. File injection. The Agent Injector adds an agent sidecar. The agent writes the secret to a file in the pod, such as /vault/secrets/db, on an in-memory volume. No code change if the app reads a config file. Best for Tanzu apps.
3. Environment variable. The sidecar writes an export file. The container start command loads it into the environment. The app code is unchanged, only the start command changes. RFP 4.4.3 asks to avoid env vars where avoidable, so prefer files.
4. CSI volume or Kubernetes Secret. The CSI provider mounts the secret as a volume through the Secrets Store CSI Driver, and can sync it to a native Kubernetes Secret. Apps that already read Kubernetes Secrets need no change.
OpenBao CSI docs: the provider authenticates as the pod's service account. Secrets are read during ContainerCreation, so the pod waits until the volume is ready. Syncing to Kubernetes Secrets lets apps use them as env vars. TLS and mTLS are supported.
Sources: patterns as presented in the earlier session. Injector and CSI objects: Helm chart 0.28.3. CSI behavior: openbao.org/docs/platform/k8s/csi.

## Slide 8

Any Language Works, Most Apps Change About Five Lines

EFFORT FOR APPLICATION TEAMS

Java

.NET

Python

Node.js

PHP

Shell

PowerShell

Any language that can call HTTPS can use the REST API.

PLATFORM

DEVELOPER WORK

PLATFORM TEAM, ONCE

Tanzu Kubernetes apps

No code change

Add 3 pod annotations

Java on WebSphere, WebLogic, Tomcat

About 5 lines

AppRole and a policy

.NET on IIS and Windows

About 5 lines

AppRole and a policy

AIX, Linux batch jobs, scripts

One API call

AppRole or TLS cert

TO CONFIRM
App Connect, WSO2, agent on AIX and Windows

AccuKnox professional services can make the code change.

This slide answers the question from the application teams: how much work will I have to do?
Any language that can make an HTTPS call can use the REST API: Java, .NET, Python, Node.js, PHP, shell and PowerShell.
Per platform:
Tanzu Kubernetes apps: file injection. No code change if the app reads a file. To pick up a rotation, the app reloads the file. Platform team adds 3 pod annotations and binds a role to the service account.
Java on WebSphere, WebLogic, Tomcat: SDK. Swap the property read for a client call, about 5 lines. Platform team creates an AppRole and a policy and hands over the role ID.
.NET on IIS and Windows: SDK with VaultSharp. Same change, about 5 lines. Same platform work as Java.
AIX, Linux batch jobs, scripts: REST API or CLI. Replace the hardcoded value with one API call. AppRole or TLS certificate identity per job.
TO CONFIRM by the deployment team: the integration route for IBM App Connect and WSO2, and agent support on AIX and Windows VMs, which would give a no-code option off Kubernetes.
AccuKnox professional services can review the application code and make these changes (confirmed in the earlier session).
Effort estimates assume the code samples on slides 10 and 11.

## Slide 9

Kubernetes Apps Get Secrets With Zero Code Change

PATTERN 2, FILE INJECTION ON TANZU

Same setup on any Kubernetes 1.30+, OpenShift included.

BEFORE

AFTER

Only the manifest changes.

Only the deployment manifest changes. The application binary stays the same, and the plaintext password leaves Git.
What happens when the pod starts:
1. The Agent Injector, a mutating webhook, sees the annotations and adds the agent to the pod.
2. The agent logs in with the pod's Kubernetes service account. There is no password to store.
3. The agent writes the secret to /vault/secrets/db on an in-memory volume.
4. The app reads the file it already reads today. When the secret changes, the agent rewrites the file.
A template annotation shapes the file to match the app's current config format, for example a properties file or a JSON file. The chart default template is map.
The role name payments-app is a Kubernetes auth role bound to the service account payments-app. The chart sets the auth path to auth/kubernetes.
Annotation format: the injector image in the chart is hashicorp/vault-k8s 1.7.2, so the annotations use the vault.hashicorp.com prefix.
Source: Helm chart 0.28.3, injector settings in values.yaml.

## Slide 10

Java and .NET Apps Change About Five Lines

PATTERN 1, SDK ON THE APP SERVERS

Java

BEFORE

AFTER

Spring Boot apps: Spring Cloud Vault, config only.

.NET

BEFORE

AFTER

Same call for IIS sites, Windows services, jobs.

Both samples log in with AppRole, then read one KV v2 path. On Kubernetes, the Kubernetes auth method replaces AppRole.
Java library: io.github.jopenlibs:vault-java-driver. Before: the password sits in plaintext in app.properties.
Spring Boot apps can use Spring Cloud Vault, which fills the existing properties through configuration only, with no code change.
.NET library: VaultSharp. Before: the password sits in web.config. The same call works for IIS sites, Windows services and console jobs.
Open-source Vault clients work because Secrets Manager is Vault API compatible (Secrets Manager FAQ). AccuKnox validates each sample against v2.5.4 during the POC.
The platform team delivers the role ID with the app and the secret ID at deploy time.

## Slide 11

Python and Node.js Apps Change About Five Lines

PATTERN 1, SDK FOR SERVICES AND SCRIPTS

Python

BEFORE

AFTER

Role ID ships with the app, secret ID at deploy.

Node.js

BEFORE

AFTER

Keep it in memory. Never write it to a log.

Same flow as Java and .NET: log in with AppRole, read one path, keep the value in memory.
Python library: hvac. Node.js library: node-vault.
The platform team delivers the role ID with the app and the secret ID at deploy time.
Read the secret at start, keep it in memory, and never write it to a log.
PHP, shell and PowerShell use the same REST API. A raw call is a GET to /v1/secret/data/payments/db with the token in the X-Vault-Token header.
Open-source Vault clients work because Secrets Manager is Vault API compatible. AccuKnox validates each sample against v2.5.4 during the POC.

## Slide 12

The DB Password Rotates, the App Keeps Running

USE CASE FOR THE LIVE DEMO

With a code change (SDK)

The app renews before the lease ends.

Without a code change (file)

The agent rewrites the file. The app reloads.

TO CONFIRM
Rotation for DB2 and MongoDB. Demo database and lease times.

This is the scenario for the live demo. An app on Kubernetes connects to a database. Secrets Manager changes the password on a schedule.
Flow: the database secrets engine holds the admin connection. It issues a new password with a lease, or rotates a static password on a schedule. The agent rewrites the file, or the SDK app asks again. New connections use the new password.
With a code change (SDK): the app reads the lease time with the password. Before the lease ends, it asks for a new one and refreshes its connection pool.
Without a code change (file): the agent sidecar rewrites /vault/secrets/db. The app re-reads the file when a connection fails or on a reload signal.
The app must open new connections with the current value. Be clear about this in the room. It is the one real piece of app behavior rotation needs.
Shown in the demo: Oracle, MySQL and PostgreSQL credentials. The old password stays valid until its lease ends, so live connections finish.
TO CONFIRM by the deployment team: rotation support for DB2 and MongoDB, and the demo database and lease times used in the live demo.
Source: database engine and supported databases from the earlier product demo.

## Slide 13

Three Nodes Keep Serving Secrets When One Fails

HIGH AVAILABILITY INSIDE ONE DATA CENTER

One leader writes

Standbys forward requests to it

A majority keeps it alive

3 nodes survive 1 failure

Election is automatic

A standby takes over

Running pods keep files

Short outages do not break them

Restarted nodes start sealed

Unseal with 3 of 5 keys

TO FILL
Node count and sizing per DC. Auto-unseal choice: HSM or key holders.

HA mode in the chart: server.ha.enabled with 3 replicas and Raft integrated storage. HA is off by default. The chart registers the pods with Kubernetes service registration, and creates active and standby services. A PodDisruptionBudget is on in HA mode.
How it behaves:
One leader writes. Standby nodes forward requests to the leader over mutual TLS (OpenBao HA docs: request forwarding is on by default, standbys open a mutually authenticated TLS connection to the active node on the cluster address).
A majority keeps it alive. 3 nodes survive 1 failure. 5 nodes survive 2.
Leader election is automatic. A standby takes over when the leader fails.
Running pods keep their files. Injected secrets stay in place during a short outage. New pods wait for the server to start.
A restarted node starts sealed. It rejoins after unsealing with 3 of 5 keys (Deployment Guide).
Spread pods over separate hosts with pod anti-affinity. The server affinity in values.yaml is empty by default, so set it.
Honest limit from the OpenBao docs: HA protects against outages but does not add throughput, because the storage is the bottleneck. Non-voter nodes can add read capacity (bao operator raft join -non-voter).
TO FILL by the deployment team: node count and sizing per data center. The on-prem auto-unseal choice. OpenBao supports an HSM over PKCS#11 and a Transit seal. Confirm which ones the AccuKnox build supports, or plan manual key holders.
Sources: Helm chart 0.28.3, Deployment Guide, openbao.org/docs/concepts/ha, openbao.org/docs/commands/operator/raft.

## Slide 14

Snapshots Every 15 Minutes Back Up the Cluster

BACKUP, RESTORE AND DISASTER RECOVERY

15 min
Worst-case data loss on restore

14 days
Snapshots kept in the bucket

3 of 5
Unseal keys needed to restore

TO FILL BY DEPLOYMENT TEAM
DC1 to DC2 design, RTO and RPO, failover and failback runbook, DR test schedule.

Backup, confirmed in the chart (snapshotAgent settings, all adjustable):
1. A CronJob runs. Default schedule every 15 minutes (*/15 * * * *).
2. The agent logs in with Kubernetes auth, role snapshot.
3. It takes a Raft snapshot from the active node.
4. It uploads to an S3-compatible bucket, on-prem. Files expire after 14 days.
Restore: load the snapshot into a new or standby cluster, then unseal it. Snapshot data stays encrypted, so the file alone exposes nothing. Manual commands from the OpenBao docs: operator raft snapshot save, and operator raft snapshot restore.
Three environments, as RFP 4.19.2 asks: DC1 production, DC2 production, and a separate test install.
Baseline already covered: a snapshot restore loses at most 15 minutes of secret changes.
TO FILL by the deployment team: the DC1 to DC2 design (active-active or warm standby), RTO and RPO targets, the failover and failback runbook, and the DR test schedule.
RISK: the RFP answer to 4.12.2 claims active-active across data centers. The chart and docs show one Raft cluster plus snapshot restore. Confirm the cross-DC design before anyone says active-active in the room.
Source: Helm chart 0.28.3, snapshotagent-cronjob.yaml and snapshotagent-configmap.yaml.

## Slide 15

Installs and Runs With No Internet Access

AIR-GAPPED DEPLOYMENT

FIVE IMAGES TO MIRROR

Server

Agent Injector

Agent sidecar

CSI provider

Snapshot agent

LDAP works offline. Entra ID needs a path to Entra.

TO CONFIRM
On-prem auto-unseal: HSM or Transit seal

Five steps:
1. Receive one tar file. The Helm chart ships as a file, so no Helm repository is needed.
2. Mirror the images. Pull them on a connected host, then push them to the bank registry.
3. Point the chart inside. A values file sets the internal registry and the pull secret (global.imagePullSecrets).
4. Install with helm upgrade --install, the same as any cluster.
5. Unseal with bank key holders. Shamir keys, 3 of 5. No cloud KMS is involved.
Images to mirror, as named in the chart:
Server: harbor.do.accuknox.com/secrets-manager/ak-secrets-mgr:v2.5.4-amd64
Agent Injector: docker.io/hashicorp/vault-k8s:1.7.2 (OpenShift: registry.connect.redhat.com, tag 1.7.2-ubi)
Agent sidecar: quay.io/accuknoxsecretmanager/accuknoxsecretmanager (the tag is empty in values.yaml, confirm the tag to mirror)
CSI provider, optional: quay.io/accuknoxsecretmanager/accuknoxsecretmanager-csi-provider:2.0.2
Snapshot agent, optional: ghcr.io/accuknoxsecretmanager/accuknoxsecretmanager-snapshot-agent:0.3.0
If CSI is used, the Secrets Store CSI Driver images need mirroring too.
Sample values file:
global: imagePullSecrets [ name bank-registry ]. server.image.registry, injector.image.registry and injector.agentImage.registry all set to registry.bank.local.
LDAP sign-in works fully offline. Entra ID over OIDC needs a network path to Entra.
Auto-unseal options in OpenBao that stay on-prem: an HSM over PKCS#11 (key material created in the HSM first) and a Transit seal from another cluster. The chart values only show a Google Cloud KMS example, which needs internet. Confirm what the AccuKnox build supports.
Sources: Helm chart 0.28.3. Air-gapped support: Secrets Manager overview and FAQ. Seals: openbao.org/docs/configuration/seal/pkcs11 and /transit.

## Slide 16

Day 2 Operations Fit Into Six Routine Jobs

RUNNING IT AFTER GO-LIVE

Unseal after restart

3 of 5 key holders

Check backups

14 days in the bucket

Watch health

Dashboard ships in the chart

Ship the audit log

Forward it to the SIEM

Upgrade one pod at a time

Standbys first, then leader

Keep access tight

Retire the root token early

TO FILL
SIEM forwarding method, restore test schedule, upgrade and patch window.

These are the jobs the bank's operations team owns.
Unseal after a restart: a restarted pod comes back sealed. Any 3 of the 5 key holders unseal it. The keys print once, at init, and Secrets Manager does not store the root key. Without 3 of 5 keys the data is unrecoverable.
Check backups: confirm the snapshot CronJob succeeds and the bucket holds 14 days of files.
Watch health: the chart ships a ServiceMonitor, alert rules and a Grafana dashboard for seal and HA status.
Ship the audit log: turn on audit storage and forward the log to the bank SIEM.
Upgrade one pod at a time: the StatefulSet uses the OnDelete update strategy. Replace standby pods first, then the leader.
Keep access tight: retire the root token after the first admin. Use scoped ACL policies. Revoke tokens under Access, Tokens. Rotate a shared credential by writing a new version.
Raft commands for operators (OpenBao docs): operator raft list-peers shows the cluster, remove-peer drops a dead node, snapshot save and restore handle backups.
TO FILL by the deployment team: the SIEM forwarding method, the restore test schedule, and the upgrade and patch window.
Sources: Helm chart 0.28.3, Deployment Guide, Sharing Secrets guide, openbao.org/docs/commands/operator/raft.

## Slide 17

Where Teams Already Run This Pattern

USE CASES FROM PREVIOUS DEPLOYMENTS

DEPLOYMENT 1, TO FILL

Industry and size

Platforms

Pattern used

HA and DR setup

Result, one number

DEPLOYMENT 2, TO FILL

Industry and size

Platforms

Pattern used

HA and DR setup

Result, one number

DEPLOYMENT 3, TO FILL

Industry and size

Platforms

Pattern used

HA and DR setup

Result, one number

TO FILL by the deployment team. The partner asked for real deployment experience.
Add two or three anonymized deployments. Keep to facts you can defend in the room.
For each one: industry and size, platforms (Kubernetes, VMs or both), the integration pattern used (SDK, file, env var, CSI), the HA and DR setup, and one result with a number.

## Slide 18

A Live Demo Today, Then a POC on One Bank App

NEXT STEPS

Today

Live demo: rotation, SDK and file

→

This week

HLD, HA and DR design

→

POC

One bank app, end to end

POC PREREQUISITES

Kubernetes 1.30+, Tanzu fits

Helm 3 and kubectl

Default StorageClass, 10Gi per node

1 vCPU, 512Mi minimum

Internal registry, 5 images

HA sizing: to fill

WHAT WE NEED FROM THE BANK

One representative app for the POC

Site, HA and DR needs for DC1 and DC2

The ask: name the POC app before the evaluation closes on Tuesday.

What we do:
Today: live demo on Kubernetes. An app reads a database password that rotates. It shows both ways: the SDK app and the file-injected app with no code change.
This week: HLD, plus the HA and DR design for DC1, DC2 and test.
On request: professional services review the chosen app and make the code change.
What we need from the bank: one representative application for the POC, and the site, HA and DR requirements for DC1 and DC2.
POC prerequisites (Deployment Guide): Kubernetes 1.30 or later (Tanzu fits), Helm 3 and kubectl, a default StorageClass with 10Gi per node, a minimum of 1 vCPU and 512Mi on a single node, and an internal registry with the five images mirrored. HA sizing: to fill by the deployment team.
The ask: name the POC application before the evaluation closes on Tuesday.

## Slide 19

SEE US IN ACTION

support@accuknox.com