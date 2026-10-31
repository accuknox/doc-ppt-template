## Slide 1

AccuKnox Secrets ManagerArchitecture and Application Integration



## Slide 2

Table of ContentsAccuKnox Secrets Manager Architecture and Application Integration

AGENDA

01

Architecture

What runs where

Slides 3 to 5

02

Connect Your Apps

SDK first, then External Secrets

Slides 6 to 10

03

Dynamic Secrets

Temporary database users

Slide 11

04

HA and DR

Failures, backups, DC1, DC2

Slides 12 and 13

05

Air-Gapped and Day 2

No internet, daily operations

Slides 14 and 15

06

Demo and Next Steps

WordPress and MySQL demo

Slides 16 to 21

Agenda for the session. Six parts.
Part 1 answers the architecture questions from the last session.
Part 2 shows the two agreed ways to connect an app: the direct SDK first, then the External Secrets Operator. It closes on the security tradeoff between them.
Part 3 shows dynamic database credentials.
Part 4 covers HA inside one data center, and backup and DR across DC1, DC2 and test.
Part 5 covers the air-gapped install and Day 2 operations.
Part 6 is the WordPress and MySQL demo in five steps, then next steps. A two-minute video of the demo sits on a hidden slide after step 5.
Backup slides after the closing slide are hidden: SDK samples in Java, .NET, Python and Node.js, and the reference deployments placeholder.

## Slide 3

One Cluster Serves Every Application in the Bank

ARCHITECTURE AT A GLANCE

Walk the diagram left to right.
LEFT, applications. Kubernetes and Tanzu pods get secrets through the External Secrets Operator, which syncs them into a Kubernetes secret, or call the SDK directly. App servers on VMs (WebSphere, WebLogic, Tomcat, .NET on IIS, AIX) call the SDK or the REST API. Jobs, scripts and CI/CD pipelines call the CLI or the REST API. Every call goes over TLS.
MIDDLE, the Secrets Manager cluster in namespace accuknox on the bank's Tanzu cluster.
Auth methods (from the FAQ and the earlier demo): Kubernetes service account, AppRole, OIDC with Entra ID, LDAP, JWT, TLS certificates, tokens, userpass, Okta.
Three server pods in HA mode: one active, two standby. Each has its own Raft integrated storage disk, 10Gi by default. Data replicates between the three nodes. There is no external database to run. Data is encrypted before it reaches disk.
Secret engines: KV v1 and v2, Database (Oracle, MySQL, PostgreSQL shown in the demo), PKI, Transit (encryption as a service), SSH, TOTP, Kubernetes, LDAP.
Apps connect in one of two ways: the REST API or an SDK, or the External Secrets sync into a Kubernetes secret. The agent sidecar approach is out of scope for this design.
AccuKnox CWPP with KubeArmor hardens every Secrets Manager pod at runtime: env var protection, secret and volume-mount protection, limits on lateral movement. The Secrets Manager overview page says AccuKnox CWPP hardens every instance.
RIGHT, bank systems: the identity provider (Entra ID or LDAP), an S3-compatible on-prem bucket for snapshots, the SIEM for the audit log, and Prometheus and Grafana for health.
Source: accuknoxsecretmanager Helm chart 0.28.3 (app v2.5.4), values.yaml and templates. Auth methods and engines: Secrets Manager FAQ and the earlier product demo.

## Slide 4

Every Secret Request Follows the Same Four Steps

HOW AN APP GETS A SECRET

Pods

Kubernetes service account

VM apps and jobs

AppRole or TLS certificate

People

Entra ID (OIDC) or LDAP

The same four steps apply to both methods. With the SDK the app runs them itself. With External Secrets the operator runs them on the app's behalf.
Step 1, authenticate. Pods use their Kubernetes service account. VM apps use AppRole or a TLS certificate. People use Entra ID (OIDC) or LDAP.
Step 2, get a token. The token is short-lived and carries one or more ACL policies. A policy names the exact paths an identity can read, for example secret/data/payments/db.
Step 3, read. The app reads only the paths its policy allows. Anything else returns permission denied. Traffic uses TLS.
Step 4, audit. Every request, allowed or denied, goes to the audit log. Turn on audit storage in the chart and forward it to the SIEM.
Revoking a token, or editing the policy, cuts access at once. Revocation lives under Access, Tokens in the UI.
A token that exists before a policy change does not pick up the new policy. The person or app must log in again (Sharing Secrets guide).
RFP links: 4.6.1 (authenticate every entity), 4.6.2 (non-human identities), 4.6.3 (encrypted channel), 4.15.1 (audit logging).

## Slide 5

Nine Building Blocks Make Up the Deployment

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

External Secrets

Syncs secrets into K8s secrets

K8s apps

ClusterSecretStore

Links the cluster to AccuKnox

K8s apps

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
External Secrets Operator: the open-source operator, installed in the application cluster. It reads from Secrets Manager and writes Kubernetes secrets. In the demo it runs in namespace external-secrets with service account external-secrets.
ClusterSecretStore: the cluster-wide object that links the operator to Secrets Manager: server URL, Kubernetes auth mount, role and KV path. A namespace-scoped SecretStore does the same for one namespace and one role.
The chart also ships an Agent Injector and a CSI provider. This design does not use them. Set injector.enabled=false at install. The CSI provider is already off by default (csi.enabled).
Snapshot agent: CronJob, off by default. Schedule */15 * * * *. Sends to an S3-compatible bucket, expires files after 14 days. Logs in with Kubernetes auth, role snapshot. Image snapshot-agent 0.3.0.
Audit storage: separate PVC, 10Gi default, off by default, mounted at /accuknoxsecretmanager/audit.
Monitoring: ServiceMonitor, PrometheusRules and a Grafana dashboard ship in the chart, all off by default.
Guard rails: Ingress, OpenShift Route or Gateway API routes. NetworkPolicy allows ports 8200 and 8201. PodDisruptionBudget protects quorum.
OpenShift has its own values file, values.openshift.yaml.
Source: accuknoxsecretmanager Helm chart 0.28.3, app v2.5.4.

## Slide 6

Two Ways to Connect an App, SDK First

INTEGRATION METHODS

1  Direct SDK or REST API

Small code change

Recommended

App asks AccuKnox at run time

Secret stays in app memory

No K8s secret or env var to read

2  External Secrets Operator

No app code change

Operator syncs into a K8s secret

App reads it as it does today

Demo refresh: every 10 seconds

The session covers two methods, agreed in the internal review. The agent sidecar approach and the file, env var and CSI injection options from the earlier deck are out of scope and removed.
Method 1, the direct SDK or REST API. The app calls Secrets Manager itself at run time. The secret stays in app memory. No Kubernetes secret or environment variable holds it, so nothing sits in the namespace for someone else to read. It needs a small code change. This is the simplest and most secure option.
Method 2, the External Secrets Operator. The open-source operator syncs a value from Secrets Manager into a Kubernetes secret. The app keeps reading its existing secret location, so the app code does not change. The demo refreshes every 10 seconds.
Images: the before and after diagrams from the internal review. Left, the app calls AccuKnox directly. Right, External Secrets fills the mysql Kubernetes secret.

## Slide 7

The SDK Reads the Secret Straight From AccuKnox

METHOD 1, DIRECT SDK INTEGRATION

Before: hardcoded secret

After: a direct call

The pod logs in

With its own service account

AccuKnox checks the role

demo-access reads only demo/mysql

The app keeps it in memory

No copy lands in the namespace

Python

WORDPRESS-STYLE APP, DIRECT CALL

Any language with HTTPS can do the same.

The app calls Secrets Manager directly. It does not store the secret in a Kubernetes secret or an environment variable along the way.
Python example with the hvac client, which works because Secrets Manager is Vault API compatible:
1. Read the address from VAULT_ADDR.
2. Log in with the pod's service account token, read from /var/run/secrets/kubernetes.io/serviceaccount/token (TOKEN_PATH on the slide). The auth mount path k8s-demo-cluster and the role demo-access come from the demo setup on the ClusterSecretStore slide.
3. Read demo/mysql from the KV version 2 engine mounted at secret, and keep the password in memory.
Any language that can make an HTTPS call can do the same through the REST API. Java, .NET and Node.js samples sit on hidden backup slides after the closing slide.
The deeper SDK walkthrough is not planned for the session. The method is short enough to explain from this slide.
AccuKnox professional services can review an app's code and make the change.
Image: the before and after diagram from the internal review. Before, WordPress carries a hardcoded secret. After, WordPress calls AccuKnox Secrets Manager directly.

## Slide 8

External Secrets Syncs AccuKnox Into a Kubernetes Secret

METHOD 2, EXTERNAL SECRETS OPERATOR

1

Password in AccuKnox

Path demo/mysql, key password

↓

2

ExternalSecret polls it

Every 10 s, through a ClusterSecretStore

↓

3

K8s secret mysql-pass

Created and kept in sync by the operator

↓

4

WordPress reads it

secretKeyRef to mysql-pass, key password

The sync updates the K8s secret. A running app picks it up when it restarts.

Secrets Manager stays an external control plane. The External Secrets Operator, an open-source operator, runs in the application cluster and handles the sync.
Demo setup: one cluster, one namespace (wordpress-mysql in the diagram), two deployments, WordPress and MySQL.
1. The password lives in Secrets Manager at demo/mysql, key password.
2. An ExternalSecret object asks for it. refreshInterval is 10s. secretStoreRef points at the ClusterSecretStore named vault-backend-demo. remoteRef key is demo/mysql, property password.
3. The operator creates and updates the Kubernetes secret mysql-pass, key password.
4. WordPress reads WORDPRESS_DB_PASSWORD through secretKeyRef, name mysql-pass, key password. The WordPress code does not change.
Say it precisely: the sync updates the Kubernetes secret. A running app reads the new value only when it restarts. It does not hot-reload. The demo shows the restart step.
The app's own logic can also write new values to Secrets Manager. The demo changes them by hand.
Image: the External Secrets architecture diagram from the internal review.

## Slide 9

A ClusterSecretStore Links the Cluster to AccuKnox

METHOD 2, CONNECTION AND ACCESS

Server

The AccuKnox Secrets Manager URL

Auth

Kubernetes, mount k8s-demo-cluster

Role

demo-access reads only demo/mysql

Service account

external-secrets

Secret engine

KV version 2 at path secret

Another app needs a different role? Give it a namespace-scoped SecretStore.

The ClusterSecretStore is the link between the External Secrets Operator and Secrets Manager. Values from the demo, as the k9s describe screenshot shows:
Provider Vault-compatible. Server: the AccuKnox Secrets Manager URL. Path: secret. Version: v2.
Auth: Kubernetes, mount path k8s-demo-cluster, role demo-access, service account external-secrets in namespace external-secrets. The cluster's OIDC setup binds that service account.
Status: store validated, Ready.
The role demo-access maps to a policy that grants read access to demo/mysql only. A policy names the paths, and it can also name the namespace and the bound service accounts. See Sharing Secrets Within an Organization in the Secrets Manager docs for users, policies and scoping.
Capabilities shows ReadWrite. That is the default label. It does not grant write access. The role's policy decides access.
ClusterSecretStore is cluster-wide and uses one role. When a second app needs a different role or a narrower scope, use a namespace-scoped SecretStore for that app instead.

## Slide 10

Easier Setup Leaves a Copy of the Secret in the Namespace

THE TRADEOFF BETWEEN THE METHODS

Direct SDK

CODE CHANGE

Small

SECRET SITS IN

App memory only

WHO ELSE CAN READ IT

Only the app

External Secrets, K8s secret

CODE CHANGE

None

SECRET SITS IN

A Kubernetes secret

WHO ELSE CAN READ IT

Anyone with namespace access

External Secrets, env var

CODE CHANGE

None

SECRET SITS IN

An env var in the workload

WHO ELSE CAN READ IT

Anyone with workload access

Pick per app: External Secrets for speed, the SDK where the secret must stay out of the namespace.

External Secrets is the easier path. The app keeps reading its existing secret location with no code change.
The cost: the value also sits in a Kubernetes secret, or in an environment variable. Anyone with access to that namespace or workload can read it there.
The direct SDK call leaves no such copy. The secret exists only in the app's memory, so a compromised namespace exposes nothing extra.
Variant shown in the middle and right columns: External Secrets can feed a Kubernetes secret, or an environment variable that the app reads. Both carry the same risk.
Images: the before and after diagrams from the internal review, after side only.

## Slide 11

Each Request Gets Its Own Temporary Database User

USE CASE FOR THE LIVE DEMO

TO CONFIRM
Rotation for DB2 and MongoDB. Demo database and lease times.

This is the scenario for the live demo. It shows dynamic, temporary database credentials. It does not show one permanent app password changed in place.
Three components: the application, Secrets Manager, and the database.
1. Application to Secrets Manager: the app requests database credentials.
2. Secrets Manager to the database: using its admin access, Secrets Manager creates a temporary database user and password.
3. Secrets Manager to the application: it returns those temporary credentials.
4. Application to the database: the app opens a connection with them.
5. Next new connection: the app requests fresh credentials when it needs them.
An already established connection is not cut just because its credentials later expire. The credentials are valid for a set time, for example 1 or 2 hours.
Each request creates a new temporary user. Secrets Manager does not just update one existing password.
Shown in the earlier demo: Oracle, MySQL and PostgreSQL credentials.
TO CONFIRM by the deployment team: support for DB2 and MongoDB, and the demo database and lease times used in the live demo.
Source: the earlier product demo, and the internal review of this slide before the session.

## Slide 12

Three Nodes Keep Serving Secrets When One Fails

HIGH AVAILABILITY INSIDE ONE DATA CENTER

One leader writes

Standbys forward requests to it

A majority keeps it alive

3 nodes survive 1 failure

Election is automatic

A standby takes over

Running apps keep their secret

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
Running apps keep their secret. A Kubernetes secret synced by External Secrets stays in place during a short outage, and the next sync catches up. An SDK app that already read its secret keeps it in memory. New logins wait for the server.
A restarted node starts sealed. It rejoins after unsealing with 3 of 5 keys (Deployment Guide).
Spread pods over separate hosts with pod anti-affinity. The server affinity in values.yaml is empty by default, so set it.
Honest limit from the OpenBao docs: HA protects against outages but does not add throughput, because the storage is the bottleneck. Non-voter nodes can add read capacity (bao operator raft join -non-voter).
TO FILL by the deployment team: node count and sizing per data center. The on-prem auto-unseal choice. OpenBao supports an HSM over PKCS#11 and a Transit seal. Confirm which ones the AccuKnox build supports, or plan manual key holders.
Sources: Helm chart 0.28.3, Deployment Guide, openbao.org/docs/concepts/ha, openbao.org/docs/commands/operator/raft.

## Slide 13

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

## Slide 14

Installs and Runs With No Internet Access

AIR-GAPPED DEPLOYMENT

IMAGES TO MIRROR

Secrets Manager server

Snapshot agent

External Secrets Operator

LDAP works offline. Entra ID needs a path to Entra.

TO CONFIRM
On-prem auto-unseal: HSM or Transit seal

Five steps:
1. Receive one tar file. The Helm chart ships as a file, so no Helm repository is needed.
2. Mirror the images. Pull them on a connected host, then push them to the bank registry.
3. Point the chart inside. A values file sets the internal registry and the pull secret (global.imagePullSecrets).
4. Install with helm upgrade --install, the same as any cluster.
5. Unseal with bank key holders. Shamir keys, 3 of 5. No cloud KMS is involved.
Images to mirror:
Server, from the chart: harbor.do.accuknox.com/secrets-manager/ak-secrets-mgr:v2.5.4-amd64
Snapshot agent, from the chart: ghcr.io/accuknoxsecretmanager/accuknoxsecretmanager-snapshot-agent:0.3.0
External Secrets Operator: the images its own Helm chart names. TO CONFIRM: the version the deployment team pins.
This design does not use the Agent Injector, the agent sidecar or the CSI provider, so their images need no mirroring. Install with injector.enabled=false.
Sample values file:
global: imagePullSecrets [ name bank-registry ]. server.image.registry set to registry.bank.local.
LDAP sign-in works fully offline. Entra ID over OIDC needs a network path to Entra.
Auto-unseal options in OpenBao that stay on-prem: an HSM over PKCS#11 (key material created in the HSM first) and a Transit seal from another cluster. The chart values only show a Google Cloud KMS example, which needs internet. Confirm what the AccuKnox build supports.
Sources: Helm chart 0.28.3. Air-gapped support: Secrets Manager overview and FAQ. Seals: openbao.org/docs/configuration/seal/pkcs11 and /transit.

## Slide 15

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

## Slide 16

Step 1: The Password and the Sync Rule

LIVE DEMO, STEP 1 OF 5

IN ACCUKNOX SECRETS MANAGER

Path demo/mysql

Key password

THE EXTERNALSECRET OBJECT

Refresh every 10 s

Store: ClusterSecretStore

Writes K8s secret mysql-pass

The demo starts from a clean cluster. The resources from the earlier run are deleted first.
Left: the password sits in Secrets Manager under the KV engine secret, path demo/mysql, key password.
Right: the ExternalSecret YAML. refreshInterval 10s. secretStoreRef kind ClusterSecretStore, name vault-backend-demo. target name mysql-pass. data secretKey password, remoteRef key demo/mysql, property password.
Screens: frames from the recorded demo, with the presenter's webcam, the dock and the browser bar cropped out.

## Slide 17

Step 2: Kubernetes Gets the Password Within 10 Seconds

LIVE DEMO, STEP 2 OF 5

1

kubectl apply creates mysql-pass

2

A new value is saved in AccuKnox

3

About 10 s later, mysql-pass holds it

The operator keeps mysql-pass equal to the value in AccuKnox.

1. kubectl apply on the ExternalSecret file creates the Kubernetes secret mysql-pass right away. k9s shows its decoded value.
2. A new value is saved in Secrets Manager with Create new version.
3. About 10 seconds later, mysql-pass holds the new value. Nobody touched Kubernetes.
At this point WordPress and MySQL are not deployed yet. This step shows the sync on its own.

## Slide 18

Step 3: WordPress Reads mysql-pass With No Code Change

LIVE DEMO, STEP 3 OF 5

THE WORDPRESS DEPLOYMENT

WORDPRESS LOADS

secretKeyRef points at mysql-pass

The app reads the K8s secret it always read

Connected to MySQL

The password came from AccuKnox

The MySQL and WordPress deployments are applied unchanged from the standard Kubernetes example.
Left: the WordPress deployment. WORDPRESS_DB_PASSWORD comes from valueFrom, secretKeyRef, name mysql-pass, key password.
Right: WordPress loads, so it reached MySQL with the synced password. The page shown is the WordPress install screen.

## Slide 19

Step 4: Changing the MySQL Password Breaks the Connection

LIVE DEMO, STEP 4 OF 5

MYSQL PASSWORD CHANGED BY HAND

→

WORDPRESS LOSES THE DATABASE

The database and the Kubernetes secret no longer match, so WordPress cannot connect.

The MySQL password is changed by hand inside the MySQL pod: ALTER USER for the wordpress user, then FLUSH PRIVILEGES.
The database now expects a password that the Kubernetes secret does not hold yet.
WordPress shows Error establishing a database connection.

## Slide 20

Step 5: A New Version and a Restart Restore the Connection

LIVE DEMO, STEP 5 OF 5

1

New version in AccuKnox

2

Restart the WordPress pod

3

mysql-pass holds the new value

4

WordPress connects again

The sync alone did not fix the running app. The restart did.

1. The new password is saved in Secrets Manager as a new version of demo/mysql.
2. The operator syncs it to mysql-pass within the refresh interval.
3. The WordPress pod is deleted, and Kubernetes starts a new one.
4. On startup the new pod reads the updated mysql-pass, and WordPress connects again.
Say it precisely: the sync alone did not fix the running app. The restart did, because the app reads the secret when it starts.

## Slide 21

Watch the Two-Minute Demo

LIVE DEMO, RECORDED

HIDDEN until the video is approved.
The edited recording: 2 minutes 0 seconds, 1600 x 900, AI voiceover, no faces, no personal browser tabs.
Local file: D:\AccuKnox\help\references\video-edits\sm-eso-wordpress\output\sm-eso-wordpress.mp4
To embed: upload the MP4 to Drive, then Insert, Video, Google Drive in Google Slides, and place it over the poster frame.

## Slide 22

A Live Demo Today, Then a POC on One Bank App

NEXT STEPS

Today

Live demo: External Secrets sync

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

Internal registry, mirrored images

HA sizing: to fill

WHAT WE NEED FROM THE BANK

One representative app for the POC

Site, HA and DR needs for DC1 and DC2

What we do:
Today: live demo on Kubernetes. WordPress reads its MySQL password from a Kubernetes secret that External Secrets keeps in sync with Secrets Manager. The app code does not change.
This week: HLD, plus the HA and DR design for DC1, DC2 and test.
On request: professional services review the chosen app and make the code change.
What we need from the bank: one representative application for the POC, and the site, HA and DR requirements for DC1 and DC2.
POC prerequisites (Deployment Guide): Kubernetes 1.30 or later (Tanzu fits), Helm 3 and kubectl, a default StorageClass with 10Gi per node, a minimum of 1 vCPU and 512Mi on a single node, and an internal registry with the images mirrored. HA sizing: to fill by the deployment team.

## Slide 23

SEE US IN ACTION

support@accuknox.com



## Slide 24

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

HIDDEN BACKUP. Show only if the bank asks for SDK samples beyond Python. Both samples log in with AppRole, then read one KV v2 path. On Kubernetes, the Kubernetes auth method replaces AppRole.
Java library: io.github.jopenlibs:vault-java-driver. Before: the password sits in plaintext in app.properties.
Spring Boot apps can use Spring Cloud Vault, which fills the existing properties through configuration only, with no code change.
.NET library: VaultSharp. Before: the password sits in web.config. The same call works for IIS sites, Windows services and console jobs.
Open-source Vault clients work because Secrets Manager is Vault API compatible (Secrets Manager FAQ). AccuKnox validates each sample against v2.5.4 during the POC.
The platform team delivers the role ID with the app and the secret ID at deploy time.

## Slide 25

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

HIDDEN BACKUP. Show only if the bank asks for SDK samples beyond Python. Same flow as Java and .NET: log in with AppRole, read one path, keep the value in memory.
Python library: hvac. Node.js library: node-vault.
The platform team delivers the role ID with the app and the secret ID at deploy time.
Read the secret at start, keep it in memory, and never write it to a log.
PHP, shell and PowerShell use the same REST API. A raw call is a GET to /v1/secret/data/payments/db with the token in the X-Vault-Token header.
Open-source Vault clients work because Secrets Manager is Vault API compatible. AccuKnox validates each sample against v2.5.4 during the POC.

## Slide 26

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
For each one: industry and size, platforms (Kubernetes, VMs or both), the integration method used (direct SDK or External Secrets), the HA and DR setup, and one result with a number.