# -*- coding: utf-8 -*-
"""
AccuKnox Secrets Manager, architecture and application integration deck for the
Sampath Bank evaluation (session of 5 October). Version 2, visual pass.

Every product fact comes from one of four sources:
  1. The Helm chart accuknoxsecretmanager-v2.tar (chart 0.28.3, app v2.5.4).
  2. help.accuknox.com/secrets-manager/ pages and the Secrets Manager FAQ.
  3. Notes from the earlier Sampath session (patterns, auth methods, engines).
  4. OpenBao docs (openbao.org/docs): HA concepts, operator raft, CSI provider,
     PKCS#11 and Transit seals. Used to explain how the Vault-compatible core works.
Anything those sources do not settle is drawn as a TO FILL or TO CONFIRM panel.
Fine print lives in the speaker notes of each slide.

Diagrams and icon PNGs come from scripts/sampath_svg.py. Run that first.

Build:   py -3.11 scripts/sampath_svg.py && py -3.11 scripts/build_sampath_secrets_manager.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_Sampath_Secrets_Manager.pptx -Out output/render/sampath
"""
import os, shutil, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _akdeck
from _akdeck import *          # noqa: F401,F403

google_safe()   # JetBrains Mono for code, survives the Slides conversion

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "PPT Template.pptx")
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_Sampath_Secrets_Manager.pptx")
DIAG = os.path.join(HERE, "..", "work", "sampath", "diagrams")
PINK = RGBColor(0xFF, 0x8A, 0x9A)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_STD = prs.slide_layouts[4]
xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try: prs.part.drop_rel(sid.get(qn('r:id')))
    except Exception: pass
    xml_slides.remove(sid)


# =================================================================== helpers
# Visual helpers come from _akdeck (icon_img, icon_tile, icon_card, callout,
# todo_panel, diagram, label, notes, hide_slide). Only deck-specific glue lives here.
_SUFFIX = {"-w": "#FFFFFF", "-g": "#0B7A42", "-r": "#C80019"}


def std(title, kicker, notes_text):
    s = prs.slides.add_slide(L_STD); set_title(s, title); blank_footer(s)
    eyebrow(s, kicker, y=0.84, w=8.6, size=11)
    notes(s, notes_text)
    return s


def ic(slide, name, x, y, s):
    """Icon by name, with an optional color suffix: key-w (white), key-g (green), key-r (red)."""
    col = None
    for suf, c in _SUFFIX.items():
        if name.endswith(suf):
            name, col = name[:-len(suf)], c
    icon_img(slide, name, x, y, s, color=col)


def ic_tile(slide, name, x, y, s, bg=PRIMARY):
    icon_tile(slide, name, x, y, s, bg=bg)


def dg(slide, name, x, y, w):
    return diagram(slide, os.path.join(DIAG, name + ".png"), x, y, w)


# =================================================================== 1. cover
cover_slide(prs, "AccuKnox Secrets Manager\nArchitecture and Application Integration",
            subtitle="Sampath Bank architecture session, 5 October", tsize=23)


# =================================================================== 2. TOC
s = std("What We Cover Today", "Agenda", """
Agenda for the session. Six parts.
Part 1 answers the architecture questions from the last session.
Part 2 answers the key question from the application teams: how much work will I have to do?
Part 3 is the live demo: an app on Kubernetes reads a database password that rotates.
Part 4 covers HA inside one data center, and backup and DR across DC1, DC2 and test.
Part 5 covers the air-gapped install and Day 2 operations.
Part 6 covers reference deployments and next steps.
Slide 3 is hidden. It maps each question from the last session to an RFP clause. Unhide it if the bank asks for the mapping.
""")
toc = [("topology-star-3", "Architecture", "What runs where", "Slides 4 to 6"),
       ("code", "Connect Your Apps", "Four patterns, code samples", "Slides 7 to 11"),
       ("refresh", "Live Use Case", "Password rotation demo", "Slide 12"),
       ("server-2", "HA and DR", "Failures, backups, DC1, DC2", "Slides 13 and 14"),
       ("wifi-off", "Air-Gapped and Day 2", "No internet, daily operations", "Slides 15 and 16"),
       ("rocket", "Proof and Next Steps", "References and the POC", "Slides 17 and 18")]
for i, (icn, h, sub, rng) in enumerate(toc):
    x = 0.40 + (i % 3) * 3.1
    y = 1.22 + (i // 3) * 2.0
    box(s, x, y, 2.96, 1.82, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    ic_tile(s, icn, x + 0.18, y + 0.2, 0.74)
    box(s, x + 1.9, y + 0.16, 0.9, 0.6, text=f"0{i+1}", size=28, color=LAV, bold=True, align=PP_ALIGN.RIGHT)
    box(s, x + 0.18, y + 1.0, 2.7, 0.36, text=h, size=16, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.18, y + 1.34, 2.7, 0.26, text=sub, size=10.5, color=MUTE)
    box(s, x + 0.18, y + 1.56, 2.7, 0.24, text=rng, size=9.5, color=PRIMARY, bold=True)


# =================================================================== 3. asks (hidden)
s = std("Five Questions This Session Answers", "Your asks, mapped to the RFP", """
HIDDEN SLIDE. Unhide if the bank wants the RFP mapping on screen.
Sampath Bank does not run a secrets manager today, so this is a new on-premises build.
The target host is the bank's own Tanzu Kubernetes platform, the option RFP 4.19.1 prefers.
Mapping: deploy and where (4.19.1, 4.19.3) on slides 4 and 6. How an app gets a secret (4.1.4, 4.6.1, 4.6.3) on slides 4 and 5.
Developer effort (4.5.2, 4.5.3) on slides 7 to 11. Node or site failure (4.12.1 to 4.12.5, 4.13.3) on slides 13 and 14.
No internet access (4.19.4) on slide 15.
""")
rows = [["You asked", "RFP clause", "Answered on"],
        ["What do we deploy, and where does it run?", "4.19.1, 4.19.3", "Slides 4 and 6"],
        ["How does an application get a secret?", "4.1.4, 4.6.1, 4.6.3", "Slides 4 and 5"],
        ["How much work will my developers do?", "4.5.2, 4.5.3", "Slides 7 to 11"],
        ["What happens when a node or a data center fails?", "4.12.1 to 4.12.5", "Slides 13 and 14"],
        ["Can it run with no internet access?", "4.19.4", "Slide 15"]]
table(s, CX, 1.3, CW, 3.4, rows, colw=[4.9, 2.2, 2.1], hsize=12, bsize=12)
hide_slide(s)


# =================================================================== 4. architecture
s = std("One Cluster Serves Every Application in the Bank", "Architecture at a glance", """
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
""")
dg(s, "architecture", 0.40, 1.14, 9.2)


# =================================================================== 5. flow
s = std("Every Secret Request Follows the Same Four Steps", "How an app gets a secret", """
The same four steps apply to every pattern: SDK, file, env var or CSI.
Step 1, authenticate. Pods use their Kubernetes service account. VM apps use AppRole or a TLS certificate. People use Entra ID (OIDC) or LDAP.
Step 2, get a token. The token is short-lived and carries one or more ACL policies. A policy names the exact paths an identity can read, for example secret/data/payments/db.
Step 3, read. The app reads only the paths its policy allows. Anything else returns permission denied. Traffic uses TLS.
Step 4, audit. Every request, allowed or denied, goes to the audit log. Turn on audit storage in the chart and forward it to the SIEM.
Revoking a token, or editing the policy, cuts access at once. Revocation lives under Access, Tokens in the UI.
A token that exists before a policy change does not pick up the new policy. The person or app must log in again (Sharing Secrets guide).
RFP links: 4.6.1 (authenticate every entity), 4.6.2 (non-human identities), 4.6.3 (encrypted channel), 4.15.1 (audit logging).
""")
y = dg(s, "flow", 0.40, 1.2, 9.2)
ids = [("kubernetes-original", "Pods", "Kubernetes service account"),
       ("server", "VM apps and jobs", "AppRole or TLS certificate"),
       ("azure-original", "People", "Entra ID (OIDC) or LDAP")]
for i, (icn, h, sub) in enumerate(ids):
    x = 0.40 + i * 3.1
    box(s, x, y + 0.22, 2.96, 0.78, fill=WHITE, line=GREY_BD, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    ic(s, icn, x + 0.14, y + 0.33, 0.56)
    box(s, x + 0.82, y + 0.27, 2.1, 0.34, text=h, size=13, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.82, y + 0.6, 2.1, 0.32, text=sub, size=11, color=MUTE, ml=0)


# =================================================================== 6. components
s = std("One Helm Chart Deploys Nine Building Blocks", "Components to deploy", """
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
""")
comps = [("server-2", "Server", "Serves the UI and API", "Required", GREEN_LT, GREEN_DK),
         ("database", "Raft storage", "Encrypted disk per node, no DB", "Required", GREEN_LT, GREEN_DK),
         ("arrows-exchange", "Services", "Send traffic to the leader", "Required", GREEN_LT, GREEN_DK),
         ("webhook", "Agent Injector", "Puts secrets in pods as files", "K8s apps", LAV, NAVY),
         ("box", "CSI provider", "Mounts secrets as a volume", "Optional", GREY_BG, MUTE),
         ("history", "Snapshot agent", "Backs up every 15 minutes", "Recommended", LAV, NAVY),
         ("eye", "Audit storage", "Keeps the audit log on its own disk", "Recommended", LAV, NAVY),
         ("chart-line", "Monitoring", "Feeds Prometheus and Grafana", "Optional", GREY_BG, MUTE),
         ("shield-lock", "Guard rails", "Ingress, NetworkPolicy, PDB", "Optional", GREY_BG, MUTE)]
for i, (icn, h, b, tag, tf, tc) in enumerate(comps):
    x = 0.40 + (i % 3) * 3.1
    y = 1.2 + (i // 3) * 1.38
    icon_card(s, x, y, 2.96, 1.24, icn, h, b, tag=tag, tag_fill=tf, tag_color=tc)


# =================================================================== 7. patterns
s = std("Four Ways to Deliver a Secret, Three Need No Code Change", "Secret interaction methods", """
Pick the pattern per application. One bank can run all four at the same time.
1. SDK or REST API. The app calls Secrets Manager at start or on demand. The secret stays in memory and never touches disk. It needs a small code change. This was presented as the preferred and most secure option. Fits Java, .NET, Python, Node.js on VMs or Kubernetes.
2. File injection. The Agent Injector adds an agent sidecar. The agent writes the secret to a file in the pod, such as /vault/secrets/db, on an in-memory volume. No code change if the app reads a config file. Best for Tanzu apps.
3. Environment variable. The sidecar writes an export file. The container start command loads it into the environment. The app code is unchanged, only the start command changes. RFP 4.4.3 asks to avoid env vars where avoidable, so prefer files.
4. CSI volume or Kubernetes Secret. The CSI provider mounts the secret as a volume through the Secrets Store CSI Driver, and can sync it to a native Kubernetes Secret. Apps that already read Kubernetes Secrets need no change.
OpenBao CSI docs: the provider authenticates as the pod's service account. Secrets are read during ContainerCreation, so the pod waits until the volume is ready. Syncing to Kubernetes Secrets lets apps use them as env vars. TLS and mTLS are supported.
Sources: patterns as presented in the earlier session. Injector and CSI objects: Helm chart 0.28.3. CSI behavior: openbao.org/docs/platform/k8s/csi.
""")
y = dg(s, "patterns", 0.40, 1.16, 9.2)
callout(s, 0.40, y + 0.08, 9.2, 0.42, "checkbox",
        "Prefer files over env vars. RFP 4.4.3 asks to keep secrets out of env vars where possible.", size=12)


# =================================================================== 8. effort
s = std("Any Language Works, Most Apps Change About Five Lines", "Effort for application teams", """
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
""")
langs = [("java-original", "Java"), ("dotnetcore-original", ".NET"), ("python-original", "Python"),
         ("nodejs-original", "Node.js"), ("php-original", "PHP"), ("bash-original", "Shell"),
         ("powershell-original", "PowerShell")]
box(s, 0.40, 1.16, 9.2, 1.16, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
for i, (icn, lab) in enumerate(langs):
    x = 0.62 + i * 0.9
    ic(s, icn, x + 0.08, 1.26, 0.56)
    box(s, x - 0.14, 1.84, 1.0, 0.3, text=lab, size=10, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
box(s, 6.95, 1.24, 2.55, 1.0, text="Any language that can call HTTPS can use the REST API.",
    size=12, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
plat = [(["kubernetes-original", "si-vmware"], "Tanzu Kubernetes apps", "No code change", GREEN_LT, GREEN_DK, "Add 3 pod annotations"),
        (["java-original", "tomcat-original"], "Java on WebSphere, WebLogic, Tomcat", "About 5 lines", LAV, PURPLE, "AppRole and a policy"),
        (["dotnetcore-original", "windows11-original"], ".NET on IIS and Windows", "About 5 lines", LAV, PURPLE, "AppRole and a policy"),
        (["linux-original", "bash-original"], "AIX, Linux batch jobs, scripts", "One API call", LAV, PURPLE, "AppRole or TLS cert")]
label(s, 0.40, 2.44, 3.8, "PLATFORM", size=9.5, color=PRIMARY)
label(s, 4.62, 2.44, 1.8, "DEVELOPER WORK", size=9.5, color=PRIMARY)
label(s, 6.72, 2.44, 2.9, "PLATFORM TEAM, ONCE", size=9.5, color=PRIMARY)
for i, (lgs, name, dev, tf, tc, ops) in enumerate(plat):
    y = 2.72 + i * 0.5
    box(s, 0.40, y, 9.2, 0.44, fill=WHITE, line=GREY_BD, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
    for j, lg in enumerate(lgs):
        ic(s, lg, 0.5 + j * 0.38, y + 0.05, 0.34)
    box(s, 1.3, y, 3.3, 0.44, text=name, size=12, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    pill(s, 4.62, y + 0.07, 1.7, 0.3, dev, fill=tf, tcolor=tc, size=10.5)
    box(s, 6.72, y, 2.85, 0.44, text=ops, size=11.5, color=MUTE, anchor=MSO_ANCHOR.MIDDLE, ml=0)
todo_panel(s, 0.40, 4.78, 4.5, 0.6, "TO CONFIRM", "App Connect, WSO2, agent on AIX and Windows", size=10.5)
callout(s, 5.08, 4.78, 4.52, 0.6, "users", "AccuKnox professional services can make the code change.", size=11)


# =================================================================== 9. k8s no code
s = std("Kubernetes Apps Get Secrets With Zero Code Change", "Pattern 2, file injection on Tanzu", """
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
""")
dg(s, "injector", 0.40, 1.18, 4.3)
callout(s, 0.40, 4.66, 4.3, 0.74, "kubernetes-original", "Same setup on any Kubernetes 1.30+, OpenShift included.", size=11.5)
code_block(s, 4.95, 1.18, 4.65, 1.1, [
    "# deployment.yaml, today", "env:", "  - name: DB_PASSWORD",
    ("    value: \"P@ssw0rd123\"  # in Git", True)], size=10, title="BEFORE", accent=PINK)
code_block(s, 4.95, 2.38, 4.65, 2.48, [
    "metadata:", "  annotations:",
    ("    vault.hashicorp.com/agent-inject: \"true\"", True),
    ("    vault.hashicorp.com/role: \"payments-app\"", True),
    ("    vault.hashicorp.com/agent-inject-secret-db:", True),
    ("      \"secret/data/payments/db\"", True),
    "spec:", "  serviceAccountName: payments-app"], size=9.6, title="AFTER")
callout(s, 4.95, 4.96, 4.65, 0.44, "checkbox", "Only the manifest changes.", size=12,
        fill=GREEN_LT, color=GREEN_DK, icolor="#0B7A42")


# =================================================================== 10/11. code
def code_slide(title, kicker, left, right, notes):
    s = std(title, kicker, notes)
    for col, (logo_, lang, before, after, tip) in enumerate((left, right)):
        x = 0.40 + col * 4.72
        ic(s, logo_, x, 1.14, 0.48)
        box(s, x + 0.58, 1.14, 3.8, 0.48, text=lang, size=17, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
        code_block(s, x, 1.7, 4.48, 0.98, before, size=9.6, title="BEFORE", accent=PINK)
        code_block(s, x, 2.76, 4.48, 2.06, after, size=9.6, title="AFTER")
        callout(s, x, 4.9, 4.48, 0.5, "bolt", tip, size=10.5)
    return s


code_slide("Java and .NET Apps Change About Five Lines", "Pattern 1, SDK on the app servers",
    ("java-original", "Java",
     ["Properties p = load(\"app.properties\");",
      ("String pwd = p.getProperty(\"db.password\");", True)],
     ["VaultConfig cfg = new VaultConfig()",
      "    .address(addr).engineVersion(2).build();",
      ("String token = Vault.create(cfg).auth()", True),
      ("    .loginByAppRole(roleId, secretId)", True),
      ("    .getAuthClientToken();", True),
      "Vault vault = Vault.create(cfg.token(token));",
      ("String pwd = vault.logical()", True),
      ("    .read(\"secret/payments/db\")", True),
      ("    .getData().get(\"password\");", True)],
     "Spring Boot apps: Spring Cloud Vault, config only."),
    ("dotnetcore-original", ".NET",
     [("var pwd = ConfigurationManager", True),
      ("    .AppSettings[\"DbPassword\"];", True), "// plaintext in web.config"],
     ["var auth = new AppRoleAuthMethodInfo(",
      "    roleId, secretId);",
      "var client = new VaultClient(",
      "    new VaultClientSettings(addr, auth));",
      ("Secret<SecretData> s = await client.V1", True),
      ("    .Secrets.KeyValue.V2.ReadSecretAsync(", True),
      ("    path: \"payments/db\", mountPoint: \"secret\");", True),
      "var pwd = s.Data.Data[\"password\"].ToString();"],
     "Same call for IIS sites, Windows services, jobs."),
    """
Both samples log in with AppRole, then read one KV v2 path. On Kubernetes, the Kubernetes auth method replaces AppRole.
Java library: io.github.jopenlibs:vault-java-driver. Before: the password sits in plaintext in app.properties.
Spring Boot apps can use Spring Cloud Vault, which fills the existing properties through configuration only, with no code change.
.NET library: VaultSharp. Before: the password sits in web.config. The same call works for IIS sites, Windows services and console jobs.
Open-source Vault clients work because Secrets Manager is Vault API compatible (Secrets Manager FAQ). AccuKnox validates each sample against v2.5.4 during the POC.
The platform team delivers the role ID with the app and the secret ID at deploy time.
""")

code_slide("Python and Node.js Apps Change About Five Lines", "Pattern 1, SDK for services and scripts",
    ("python-original", "Python",
     [("DB_PASSWORD = \"P@ssw0rd123\"", True), "# hardcoded in settings.py, in Git"],
     ["import hvac, os",
      "client = hvac.Client(url=os.environ[\"VAULT_ADDR\"])",
      ("client.auth.approle.login(", True),
      ("    role_id=ROLE_ID, secret_id=SECRET_ID)", True),
      ("s = client.secrets.kv.v2.read_secret_version(", True),
      ("    path=\"payments/db\", mount_point=\"secret\")", True),
      "db_password = s[\"data\"][\"data\"][\"password\"]"],
     "Role ID ships with the app, secret ID at deploy."),
    ("nodejs-original", "Node.js",
     [("const dbPassword = \"P@ssw0rd123\";", True), "// hardcoded in config.js, in Git"],
     ["const vault = require(\"node-vault\")({",
      "  endpoint: process.env.VAULT_ADDR });",
      ("const login = await vault.approleLogin({", True),
      ("  role_id: roleId, secret_id: secretId });", True),
      "vault.token = login.auth.client_token;",
      ("const { data } = await vault.read(", True),
      ("  \"secret/data/payments/db\");", True),
      "const dbPassword = data.data.password;"],
     "Keep it in memory. Never write it to a log."),
    """
Same flow as Java and .NET: log in with AppRole, read one path, keep the value in memory.
Python library: hvac. Node.js library: node-vault.
The platform team delivers the role ID with the app and the secret ID at deploy time.
Read the secret at start, keep it in memory, and never write it to a log.
PHP, shell and PowerShell use the same REST API. A raw call is a GET to /v1/secret/data/payments/db with the token in the X-Vault-Token header.
Open-source Vault clients work because Secrets Manager is Vault API compatible. AccuKnox validates each sample against v2.5.4 during the POC.
""")


# =================================================================== 12. rotation
s = std("The DB Password Rotates, the App Keeps Running", "Use case for the live demo", """
This is the scenario for the live demo. An app on Kubernetes connects to a database. Secrets Manager changes the password on a schedule.
Flow: the database secrets engine holds the admin connection. It issues a new password with a lease, or rotates a static password on a schedule. The agent rewrites the file, or the SDK app asks again. New connections use the new password.
With a code change (SDK): the app reads the lease time with the password. Before the lease ends, it asks for a new one and refreshes its connection pool.
Without a code change (file): the agent sidecar rewrites /vault/secrets/db. The app re-reads the file when a connection fails or on a reload signal.
The app must open new connections with the current value. Be clear about this in the room. It is the one real piece of app behavior rotation needs.
Shown in the demo: Oracle, MySQL and PostgreSQL credentials. The old password stays valid until its lease ends, so live connections finish.
TO CONFIRM by the deployment team: rotation support for DB2 and MongoDB, and the demo database and lease times used in the live demo.
Source: database engine and supported databases from the earlier product demo.
""")
y = dg(s, "rotation", 0.40, 1.16, 9.2)
for i, (icn, h, b, col, fill) in enumerate([
        ("code", "With a code change (SDK)", "The app renews before the lease ends.", PURPLE, LAV),
        ("file-text-g", "Without a code change (file)", "The agent rewrites the file. The app reloads.", GREEN_DK, GREEN_LT)]):
    x = 0.40 + i * 4.7
    box(s, x, y + 0.14, 4.5, 0.86, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.14)
    ic(s, icn, x + 0.16, y + 0.3, 0.52)
    box(s, x + 0.82, y + 0.18, 3.6, 0.36, text=h, size=13.5, color=col, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.82, y + 0.54, 3.6, 0.4, text=b, size=11.5, color=INK, ml=0)
todo_panel(s, 0.40, y + 1.12, 9.2, 0.58, "TO CONFIRM", "Rotation for DB2 and MongoDB. Demo database and lease times.", size=11)


# =================================================================== 13. HA
s = std("Three Nodes Keep Serving Secrets When One Fails", "High availability inside one data center", """
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
""")
dg(s, "ha", 0.40, 1.16, 4.4)
facts = [("key", "One leader writes", "Standbys forward requests to it"),
         ("users", "A majority keeps it alive", "3 nodes survive 1 failure"),
         ("refresh", "Election is automatic", "A standby takes over"),
         ("file-text", "Running pods keep files", "Short outages do not break them"),
         ("lock", "Restarted nodes start sealed", "Unseal with 3 of 5 keys")]
for i, (icn, h, sub) in enumerate(facts):
    y = 1.16 + i * 0.64
    ic_tile(s, icn, 5.05, y, 0.5)
    box(s, 5.68, y - 0.04, 3.9, 0.32, text=h, size=13, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, 5.68, y + 0.26, 3.9, 0.3, text=sub, size=11, color=MUTE, ml=0)
todo_panel(s, 5.05, 4.42, 4.55, 0.98, "TO FILL", "Node count and sizing per DC. Auto-unseal choice: HSM or key holders.", size=10.5)


# =================================================================== 14. DR
s = std("Snapshots Every 15 Minutes Back Up the Cluster", "Backup, restore and disaster recovery", """
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
""")
y = dg(s, "dr", 0.70, 1.14, 8.6)
for i, (n_, l_) in enumerate([("15 min", "Worst-case data loss on restore"), ("14 days", "Snapshots kept in the bucket"), ("3 of 5", "Unseal keys needed to restore")]):
    stat(s, 0.40 + i * 3.1, y + 0.1, 2.96, n_, l_, nsize=20, lsize=10.5, h=0.72)
y += 0.86
todo_panel(s, 0.40, y + 0.04, 9.2, 0.56, "TO FILL BY DEPLOYMENT TEAM",
     "DC1 to DC2 design, RTO and RPO, failover and failback runbook, DR test schedule.", size=11)


# =================================================================== 15. air-gapped
s = std("Installs and Runs With No Internet Access", "Air-gapped deployment", """
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
""")
y = dg(s, "airgap", 0.40, 1.14, 9.2)
label(s, 0.40, y + 0.1, 4, "FIVE IMAGES TO MIRROR", size=10, color=PRIMARY)
imgs = [("server-2", "Server"), ("webhook", "Agent Injector"), ("user", "Agent sidecar"),
        ("box", "CSI provider"), ("history", "Snapshot agent")]
for i, (icn, lab) in enumerate(imgs):
    x = 0.40 + i * 1.86
    box(s, x, y + 0.38, 1.74, 0.5, fill=WHITE, line=GREY_BD, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
    ic(s, icn, x + 0.1, y + 0.45, 0.36)
    box(s, x + 0.5, y + 0.38, 1.22, 0.5, text=lab, size=11, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
callout(s, 0.40, y + 1.0, 4.5, 0.56, "users", "LDAP works offline. Entra ID needs a path to Entra.", size=11)
todo_panel(s, 5.1, y + 1.0, 4.5, 0.56, "TO CONFIRM", "On-prem auto-unseal: HSM or Transit seal", size=10.5)


# =================================================================== 16. day 2
s = std("Day 2 Operations Fit Into Six Routine Jobs", "Running it after go-live", """
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
""")
jobs = [("lock-open", "Unseal after restart", "3 of 5 key holders"),
        ("history", "Check backups", "14 days in the bucket"),
        ("heartbeat", "Watch health", "Dashboard ships in the chart"),
        ("eye", "Ship the audit log", "Forward it to the SIEM"),
        ("upload", "Upgrade one pod at a time", "Standbys first, then leader"),
        ("shield-lock", "Keep access tight", "Retire the root token early")]
for i, (icn, h, b) in enumerate(jobs):
    x = 0.40 + (i % 3) * 3.1
    y = 1.2 + (i // 3) * 1.5
    icon_card(s, x, y, 2.96, 1.34, icn, h, b, hsize=13.5, bsize=12)
todo_panel(s, 0.40, 4.32, 9.2, 0.62, "TO FILL", "SIEM forwarding method, restore test schedule, upgrade and patch window.", size=11)


# =================================================================== 17. reference deployments
s = std("Where Teams Already Run This Pattern", "Use cases from previous deployments", """
TO FILL by the deployment team. The partner asked for real deployment experience.
Add two or three anonymized deployments. Keep to facts you can defend in the room.
For each one: industry and size, platforms (Kubernetes, VMs or both), the integration pattern used (SDK, file, env var, CSI), the HA and DR setup, and one result with a number.
""")
fields = [("building-bank", "Industry and size"), ("server", "Platforms"), ("code", "Pattern used"),
          ("heartbeat", "HA and DR setup"), ("chart-line", "Result, one number")]
for i in range(3):
    x = 0.40 + i * 3.1
    b = box(s, x, 1.2, 2.96, 4.1, fill=RED_LT, line=RED, line_w=1.25, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    b.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    box(s, x + 0.16, 1.3, 2.7, 0.4, text=f"DEPLOYMENT {i+1}, TO FILL", size=12.5, color=RED, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    for j, (icn, lab) in enumerate(fields):
        y = 1.86 + j * 0.66
        ic(s, icn + "-r", x + 0.18, y, 0.4)
        box(s, x + 0.7, y, 2.2, 0.4, text=lab, size=12, color=INK, anchor=MSO_ANCHOR.MIDDLE, ml=0)


# =================================================================== 18. next steps
s = std("A Live Demo Today, Then a POC on One Bank App", "Next steps", """
What we do:
Today: live demo on Kubernetes. An app reads a database password that rotates. It shows both ways: the SDK app and the file-injected app with no code change.
This week: HLD, plus the HA and DR design for DC1, DC2 and test.
On request: professional services review the chosen app and make the code change.
What we need from the bank: one representative application for the POC, and the site, HA and DR requirements for DC1 and DC2.
POC prerequisites (Deployment Guide): Kubernetes 1.30 or later (Tanzu fits), Helm 3 and kubectl, a default StorageClass with 10Gi per node, a minimum of 1 vCPU and 512Mi on a single node, and an internal registry with the five images mirrored. HA sizing: to fill by the deployment team.
The ask: name the POC application before the evaluation closes on Tuesday.
""")
tl = [("player-play", "Today", "Live demo: rotation, SDK and file"),
      ("clipboard-list", "This week", "HLD, HA and DR design"),
      ("rocket", "POC", "One bank app, end to end")]
for i, (icn, h, b) in enumerate(tl):
    x = 0.40 + i * 3.1
    ic_tile(s, icn, x, 1.2, 0.62)
    box(s, x + 0.74, 1.16, 2.0, 0.36, text=h, size=15, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.74, 1.5, 2.0, 0.5, text=b, size=11.5, color=MUTE, ml=0)
    if i < 2:
        box(s, x + 2.76, 1.3, 0.3, 0.4, text="→", size=20, color=PRIMARY, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, 0.40, 2.12, 9.2, 0.02, fill=GREY_BD)
label(s, 0.40, 2.28, 4.5, "POC PREREQUISITES", size=10, color=PRIMARY)
pre = [("kubernetes-original", "Kubernetes 1.30+, Tanzu fits", NAVY), ("helm-original", "Helm 3 and kubectl", NAVY),
       ("database", "Default StorageClass, 10Gi per node", NAVY), ("cpu", "1 vCPU, 512Mi minimum", NAVY),
       ("stack-2", "Internal registry, 5 images", NAVY), ("alert-triangle-r", "HA sizing: to fill", RED)]
for i, (icn, lab, col) in enumerate(pre):
    x = 0.40 + (i % 2) * 2.3
    y = 2.66 + (i // 2) * 0.86
    ic(s, icn, x, y, 0.5)
    box(s, x + 0.58, y - 0.06, 1.7, 0.62, text=lab, size=12, color=col, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
label(s, 5.1, 2.28, 4.5, "WHAT WE NEED FROM THE BANK", size=10, color=PRIMARY)
for i, (icn, lab) in enumerate([("code", "One representative app for the POC"),
                                ("building-bank", "Site, HA and DR needs for DC1 and DC2")]):
    y = 2.66 + i * 0.86
    ic(s, icn, 5.1, y, 0.5)
    box(s, 5.7, y - 0.06, 3.9, 0.62, text=lab, size=13, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
box(s, 5.1, 4.36, 4.5, 0.98, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12,
    text="The ask: name the POC app before the evaluation closes on Tuesday.",
    size=13, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0.72, mr=0.2)
ic(s, "checkbox-w", 5.24, 4.63, 0.44)


# =================================================================== close
closing_slide(prs)
prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
