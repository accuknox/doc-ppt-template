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
cover_slide(prs, "AccuKnox Secrets Manager\nArchitecture and Application Integration", tsize=23)


# =================================================================== 2. TOC
s = std("Table of Contents", "Agenda", """
Agenda for the session. Six parts.
Part 1 answers the architecture questions from the last session.
Part 2 shows the two agreed ways to connect an app: the direct SDK first, then the External Secrets Operator. It closes on the security tradeoff between them.
Part 3 shows dynamic database credentials.
Part 4 covers HA inside one data center, and backup and DR across DC1, DC2 and test.
Part 5 covers the air-gapped install and Day 2 operations.
Part 6 is the WordPress and MySQL demo in five steps, then next steps. A two-minute video of the demo sits on a hidden slide after step 5.
Backup slides after the closing slide are hidden: SDK samples in Java, .NET, Python and Node.js, and the reference deployments placeholder.
""")
_t = s.shapes.title.text_frame
_t.clear()
_p = _t.paragraphs[0]
_r = _p.add_run(); _r.text = "Table of Contents"; _r.font.size = Pt(14.67); _r.font.name = FONT
_p._p.append(_p._p.makeelement(qn("a:br"), {}))
_r = _p.add_run(); _r.text = "AccuKnox Secrets Manager Architecture and Application Integration"; _r.font.name = FONT; _r.font.size = Pt(20)
toc = [("topology-star-3", "Architecture", "What runs where", "Slides 3 to 5"),
       ("code", "Connect Your Apps", "SDK first, then External Secrets", "Slides 6 to 10"),
       ("refresh", "Dynamic Secrets", "Temporary database users", "Slide 11"),
       ("server-2", "HA and DR", "Failures, backups, DC1, DC2", "Slides 12 and 13"),
       ("wifi-off", "Air-Gapped and Day 2", "No internet, daily operations", "Slides 14 and 15"),
       ("player-play", "Demo and Next Steps", "WordPress and MySQL demo", "Slides 16 to 21")]
for i, (icn, h, sub, rng) in enumerate(toc):
    x = 0.40 + (i % 3) * 3.1
    y = 1.22 + (i // 3) * 2.0
    box(s, x, y, 2.96, 1.82, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    ic_tile(s, icn, x + 0.18, y + 0.2, 0.74)
    box(s, x + 1.9, y + 0.16, 0.9, 0.6, text=f"0{i+1}", size=28, color=LAV, bold=True, align=PP_ALIGN.RIGHT)
    box(s, x + 0.18, y + 1.0, 2.7, 0.36, text=h, size=16, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.18, y + 1.34, 2.7, 0.26, text=sub, size=10.5, color=MUTE)
    box(s, x + 0.18, y + 1.56, 2.7, 0.24, text=rng, size=9.5, color=PRIMARY, bold=True)


# =================================================================== 4. architecture
s = std("One Cluster Serves Every Application in the Bank", "Architecture at a glance", """
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
""")
dg(s, "architecture", 0.40, 1.14, 9.2)


# =================================================================== 5. flow
s = std("Every Secret Request Follows the Same Four Steps", "How an app gets a secret", """
The same four steps apply to both methods. With the SDK the app runs them itself. With External Secrets the operator runs them on the app's behalf.
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
s = std("Nine Building Blocks Make Up the Deployment", "Components to deploy", """
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
""")
comps = [("server-2", "Server", "Serves the UI and API", "Required", GREEN_LT, GREEN_DK),
         ("database", "Raft storage", "Encrypted disk per node, no DB", "Required", GREEN_LT, GREEN_DK),
         ("arrows-exchange", "Services", "Send traffic to the leader", "Required", GREEN_LT, GREEN_DK),
         ("refresh", "External Secrets", "Syncs secrets into K8s secrets", "K8s apps", LAV, NAVY),
         ("link", "ClusterSecretStore", "Links the cluster to AccuKnox", "K8s apps", LAV, NAVY),
         ("history", "Snapshot agent", "Backs up every 15 minutes", "Recommended", LAV, NAVY),
         ("eye", "Audit storage", "Keeps the audit log on its own disk", "Recommended", LAV, NAVY),
         ("chart-line", "Monitoring", "Feeds Prometheus and Grafana", "Optional", GREY_BG, MUTE),
         ("shield-lock", "Guard rails", "Ingress, NetworkPolicy, PDB", "Optional", GREY_BG, MUTE)]
for i, (icn, h, b, tag, tf, tc) in enumerate(comps):
    x = 0.40 + (i % 3) * 3.1
    y = 1.2 + (i // 3) * 1.38
    icon_card(s, x, y, 2.96, 1.24, icn, h, b, tag=tag, tag_fill=tf, tag_color=tc)


# =================================================================== 6. two methods
import os as _os
from PIL import Image as _PI
_AS = _os.path.join(HERE, "..", "work", "sampath", "assets")
_DM = _os.path.join(HERE, "..", "work", "sampath", "demo")


def _crop(src, box_, out):
    p = _os.path.join(_AS, out)
    _PI.open(_os.path.join(_AS, src)).crop(box_).save(p)
    return p


SS_SDK = _os.path.join(_AS, "ss_sdk.png")
SDK_AFTER = _crop("ss_sdk.png", (540, 30, 982, 400), "sdk_after.png")
K8S_AFTER = _crop("ss_k8s_secret.png", (555, 55, 987, 420), "k8s_after.png")
ENV_AFTER = _crop("ss_env_var.png", (540, 40, 954, 405), "env_after.png")
ESO_ARCH = _os.path.join(_AS, "ss_eso_arch.png")
CSS = _os.path.join(_AS, "ss_clusterstore.png")


def D(name):
    return _os.path.join(_DM, name + ".png")


def shot(slide, path, x, y, w, h, caption=None):
    """A screenshot, fitted into the box with a thin frame and an optional caption under it."""
    return image_fit(slide, path, x, y, w, h, caption=caption, frame=GREY_BD, capsize=10, capcolor=NAVY)


def fact(slide, icn, head, sub, x, y, w, col=None):
    ic_tile(slide, icn, x, y, 0.46, bg=col or PRIMARY)
    box(slide, x + 0.58, y - 0.05, w - 0.6, 0.3, text=head, size=12.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(slide, x + 0.58, y + 0.23, w - 0.6, 0.3, text=sub, size=10.5, color=MUTE, ml=0)


def step_no(slide, x, y, n, fill=PRIMARY, d=0.34):
    box(slide, x, y, d, d, text=str(n), size=12, color=WHITE, bold=True, align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE, fill=fill, shape=MSO_SHAPE.OVAL, ml=0, mr=0, mt=0, mb=0, wrap=False)


s = std("Two Ways to Connect an App, SDK First", "Integration methods", """
The session covers two methods, agreed in the internal review. The agent sidecar approach and the file, env var and CSI injection options from the earlier deck are out of scope and removed.
Method 1, the direct SDK or REST API. The app calls Secrets Manager itself at run time. The secret stays in app memory. No Kubernetes secret or environment variable holds it, so nothing sits in the namespace for someone else to read. It needs a small code change. This is the simplest and most secure option.
Method 2, the External Secrets Operator. The open-source operator syncs a value from Secrets Manager into a Kubernetes secret. The app keeps reading its existing secret location, so the app code does not change. The demo refreshes every 10 seconds.
Images: the before and after diagrams from the internal review. Left, the app calls AccuKnox directly. Right, External Secrets fills the mysql Kubernetes secret.
""")
for i, (icn, head, tag, tf, tc, img, rows) in enumerate([
        ("code", "1  Direct SDK or REST API", "Small code change", LAV, PURPLE, SDK_AFTER,
         [("key", "App asks AccuKnox at run time"), ("lock", "Secret stays in app memory"),
          ("shield-check", "No K8s secret or env var to read")]),
        ("refresh", "2  External Secrets Operator", "No app code change", GREEN_LT, GREEN_DK, K8S_AFTER,
         [("refresh", "Operator syncs into a K8s secret"), ("file-text", "App reads it as it does today"),
          ("clock", "Demo refresh: every 10 seconds")])]):
    x = 0.40 + i * 4.7
    box(s, x, 1.16, 4.5, 4.22, fill=WHITE, line=PRIMARY if i == 0 else GREY_BD, line_w=1.5 if i == 0 else 1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
    ic_tile(s, icn, x + 0.16, 1.3, 0.5)
    box(s, x + 0.76, 1.28, 3.6, 0.32, text=head, size=14.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    pill(s, x + 0.76, 1.6, 1.7, 0.24, tag, fill=tf, tcolor=tc, size=9.5)
    if i == 0:
        pill(s, x + 2.54, 1.6, 1.2, 0.24, "Recommended", fill=PRIMARY, tcolor=WHITE, size=9.5)
    shot(s, img, x + 0.16, 1.98, 4.18, 1.86)
    for j, (ri, rt) in enumerate(rows):
        y = 3.98 + j * 0.44
        ic(s, ri + ("-g" if i == 1 else ""), x + 0.2, y, 0.32)
        box(s, x + 0.62, y - 0.04, 3.7, 0.4, text=rt, size=12, color=INK, anchor=MSO_ANCHOR.MIDDLE, ml=0)


# =================================================================== 7. SDK
s = std("The SDK Reads the Secret Straight From AccuKnox", "Method 1, direct SDK integration", """
The app calls Secrets Manager directly. It does not store the secret in a Kubernetes secret or an environment variable along the way.
Python example with the hvac client, which works because Secrets Manager is Vault API compatible:
1. Read the address from VAULT_ADDR.
2. Log in with the pod's service account token, read from /var/run/secrets/kubernetes.io/serviceaccount/token (TOKEN_PATH on the slide). The auth mount path k8s-demo-cluster and the role demo-access come from the demo setup on the ClusterSecretStore slide.
3. Read demo/mysql from the KV version 2 engine mounted at secret, and keep the password in memory.
Any language that can make an HTTPS call can do the same through the REST API. Java, .NET and Node.js samples sit on hidden backup slides after the closing slide.
The deeper SDK walkthrough is not planned for the session. The method is short enough to explain from this slide.
AccuKnox professional services can review an app's code and make the change.
Image: the before and after diagram from the internal review. Before, WordPress carries a hardcoded secret. After, WordPress calls AccuKnox Secrets Manager directly.
""")
shot(s, SS_SDK, 0.40, 1.2, 4.7, 1.98)
box(s, 0.40, 3.2, 2.35, 0.26, text="Before: hardcoded secret", size=10.5, color=RED, bold=True, align=PP_ALIGN.CENTER)
box(s, 2.75, 3.2, 2.35, 0.26, text="After: a direct call", size=10.5, color=GREEN_DK, bold=True, align=PP_ALIGN.CENTER)
for j, (icn, head, sub) in enumerate([("fingerprint", "The pod logs in", "With its own service account"),
                                     ("id-badge-2", "AccuKnox checks the role", "demo-access reads only demo/mysql"),
                                     ("lock", "The app keeps it in memory", "No copy lands in the namespace")]):
    fact(s, icn, head, sub, 0.48, 3.62 + j * 0.6, 4.6)
ic(s, "python-original", 5.32, 1.18, 0.42)
box(s, 5.82, 1.18, 3.7, 0.42, text="Python", size=15, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
code_block(s, 5.32, 1.66, 4.28, 3.0, [
    "import hvac, os",
    "ADDR = os.environ[\"VAULT_ADDR\"]",
    "client = hvac.Client(url=ADDR)",
    "# log in as the pod's service account",
    "jwt = open(TOKEN_PATH).read()",
    ("client.auth.kubernetes.login(", True),
    ("    role=\"demo-access\", jwt=jwt,", True),
    ("    mount_point=\"k8s-demo-cluster\")", True),
    "# read the password into memory",
    ("s = client.secrets.kv.v2.read_secret_version(", True),
    ("    path=\"demo/mysql\", mount_point=\"secret\")", True),
    "db_password = s[\"data\"][\"data\"][\"password\"]"], size=9.4, title="WORDPRESS-STYLE APP, DIRECT CALL")
callout(s, 5.32, 4.76, 4.28, 0.6, "shield-check", "Any language with HTTPS can do the same.", size=11.5)


# =================================================================== 8. External Secrets
s = std("External Secrets Syncs AccuKnox Into a Kubernetes Secret", "Method 2, External Secrets Operator", """
Secrets Manager stays an external control plane. The External Secrets Operator, an open-source operator, runs in the application cluster and handles the sync.
Demo setup: one cluster, one namespace (wordpress-mysql in the diagram), two deployments, WordPress and MySQL.
1. The password lives in Secrets Manager at demo/mysql, key password.
2. An ExternalSecret object asks for it. refreshInterval is 10s. secretStoreRef points at the ClusterSecretStore named vault-backend-demo. remoteRef key is demo/mysql, property password.
3. The operator creates and updates the Kubernetes secret mysql-pass, key password.
4. WordPress reads WORDPRESS_DB_PASSWORD through secretKeyRef, name mysql-pass, key password. The WordPress code does not change.
Say it precisely: the sync updates the Kubernetes secret. A running app reads the new value only when it restarts. It does not hot-reload. The demo shows the restart step.
The app's own logic can also write new values to Secrets Manager. The demo changes them by hand.
Image: the External Secrets architecture diagram from the internal review.
""")
shot(s, ESO_ARCH, 0.40, 1.18, 4.1, 3.4)
for j, (icn, head, sub) in enumerate([("lock", "Password in AccuKnox", "Path demo/mysql, key password"),
                                     ("refresh", "ExternalSecret polls it", "Every 10 s, through a ClusterSecretStore"),
                                     ("file-text", "K8s secret mysql-pass", "Created and kept in sync by the operator"),
                                     ("code", "WordPress reads it", "secretKeyRef to mysql-pass, key password")]):
    y = 1.22 + j * 0.84
    step_no(s, 4.78, y + 0.06, j + 1)
    fact(s, icn, head, sub, 5.24, y, 4.36)
    if j < 3:
        box(s, 4.87, y + 0.46, 0.16, 0.34, text="↓", size=12, color=PRIMARY, bold=True, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0, mt=0, mb=0)
callout(s, 0.40, 4.74, 9.2, 0.6, "alert-triangle", "The sync updates the K8s secret. A running app picks it up when it restarts.", size=12, icolor="#C80019")


# =================================================================== 9. ClusterSecretStore
s = std("A ClusterSecretStore Links the Cluster to AccuKnox", "Method 2, connection and access", """
The ClusterSecretStore is the link between the External Secrets Operator and Secrets Manager. Values from the demo, as the k9s describe screenshot shows:
Provider Vault-compatible. Server: the AccuKnox Secrets Manager URL. Path: secret. Version: v2.
Auth: Kubernetes, mount path k8s-demo-cluster, role demo-access, service account external-secrets in namespace external-secrets. The cluster's OIDC setup binds that service account.
Status: store validated, Ready.
The role demo-access maps to a policy that grants read access to demo/mysql only. A policy names the paths, and it can also name the namespace and the bound service accounts. See Sharing Secrets Within an Organization in the Secrets Manager docs for users, policies and scoping.
Capabilities shows ReadWrite. That is the default label. It does not grant write access. The role's policy decides access.
ClusterSecretStore is cluster-wide and uses one role. When a second app needs a different role or a narrower scope, use a namespace-scoped SecretStore for that app instead.
""")
shot(s, CSS, 0.40, 1.18, 4.25, 4.0)
for j, (icn, head, sub) in enumerate([("world", "Server", "The AccuKnox Secrets Manager URL"),
                                     ("fingerprint", "Auth", "Kubernetes, mount k8s-demo-cluster"),
                                     ("id-badge-2", "Role", "demo-access reads only demo/mysql"),
                                     ("user", "Service account", "external-secrets"),
                                     ("key", "Secret engine", "KV version 2 at path secret")]):
    fact(s, icn, head, sub, 4.92, 1.2 + j * 0.62, 4.68)
callout(s, 4.92, 4.36, 4.68, 0.82, "users", "Another app needs a different role? Give it a namespace-scoped SecretStore.", size=11.5)


# =================================================================== 10. tradeoff
s = std("Easier Setup Leaves a Copy of the Secret in the Namespace", "The tradeoff between the methods", """
External Secrets is the easier path. The app keeps reading its existing secret location with no code change.
The cost: the value also sits in a Kubernetes secret, or in an environment variable. Anyone with access to that namespace or workload can read it there.
The direct SDK call leaves no such copy. The secret exists only in the app's memory, so a compromised namespace exposes nothing extra.
Variant shown in the middle and right columns: External Secrets can feed a Kubernetes secret, or an environment variable that the app reads. Both carry the same risk.
Images: the before and after diagrams from the internal review, after side only.
""")
cols = [(SDK_AFTER, "Direct SDK", [("Code change", "Small", True), ("Secret sits in", "App memory only", True),
                                  ("Who else can read it", "Only the app", True)]),
        (K8S_AFTER, "External Secrets, K8s secret", [("Code change", "None", True), ("Secret sits in", "A Kubernetes secret", False),
                                                     ("Who else can read it", "Anyone with namespace access", False)]),
        (ENV_AFTER, "External Secrets, env var", [("Code change", "None", True), ("Secret sits in", "An env var in the workload", False),
                                                  ("Who else can read it", "Anyone with workload access", False)])]
for i, (img, head, rows) in enumerate(cols):
    x = 0.40 + i * 3.1
    box(s, x, 1.16, 2.96, 3.6, fill=WHITE, line=GREY_BD, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    shot(s, img, x + 0.12, 1.26, 2.72, 1.18)
    box(s, x + 0.12, 2.5, 2.72, 0.32, text=head, size=12.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    for j, (lab, val, good) in enumerate(rows):
        y = 2.88 + j * 0.62
        box(s, x + 0.12, y, 2.7, 0.22, text=lab.upper(), size=8.5 + 0.5, color=PRIMARY, bold=True, ml=0)
        ic(s, ("circle-check-g" if good else "alert-triangle-r"), x + 0.12, y + 0.24, 0.28)
        box(s, x + 0.46, y + 0.2, 2.4, 0.34, text=val, size=11.5, color=GREEN_DK if good else RED, bold=True,
            anchor=MSO_ANCHOR.MIDDLE, ml=0)
callout(s, 0.40, 4.86, 9.2, 0.5, "scale", "Pick per app: External Secrets for speed, the SDK where the secret must stay out of the namespace.", size=11.5)


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


_bk1 = code_slide("Java and .NET Apps Change About Five Lines", "Pattern 1, SDK on the app servers",
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

_bk2 = code_slide("Python and Node.js Apps Change About Five Lines", "Pattern 1, SDK for services and scripts",
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


hide_slide(_bk1)
hide_slide(_bk2)
for _b in (_bk1, _bk2):
    _n = _b.notes_slide.notes_text_frame
    _n.text = "HIDDEN BACKUP. Show only if the bank asks for SDK samples beyond Python. " + _n.text


# =================================================================== 12. dynamic secrets
s = std("Each Request Gets Its Own Temporary Database User", "Use case for the live demo", """
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
""")
dg(s, "dynamic", 0.40, 1.16, 9.2)
todo_panel(s, 0.40, 4.44, 9.2, 0.58, "TO CONFIRM", "Rotation for DB2 and MongoDB. Demo database and lease times.", size=11)


# =================================================================== 13. HA
s = std("Three Nodes Keep Serving Secrets When One Fails", "High availability inside one data center", """
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
""")
dg(s, "ha", 0.40, 1.16, 4.4)
facts = [("key", "One leader writes", "Standbys forward requests to it"),
         ("users", "A majority keeps it alive", "3 nodes survive 1 failure"),
         ("refresh", "Election is automatic", "A standby takes over"),
         ("file-text", "Running apps keep their secret", "Short outages do not break them"),
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
""")
y = dg(s, "airgap", 0.40, 1.14, 9.2)
label(s, 0.40, y + 0.1, 4, "IMAGES TO MIRROR", size=10, color=PRIMARY)
imgs = [("server-2", "Secrets Manager server"), ("history", "Snapshot agent"), ("refresh", "External Secrets Operator")]
for i, (icn, lab) in enumerate(imgs):
    x = 0.40 + i * 3.1
    box(s, x, y + 0.38, 2.96, 0.5, fill=WHITE, line=GREY_BD, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
    ic(s, icn, x + 0.12, y + 0.45, 0.36)
    box(s, x + 0.56, y + 0.38, 2.36, 0.5, text=lab, size=11.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
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
For each one: industry and size, platforms (Kubernetes, VMs or both), the integration method used (direct SDK or External Secrets), the HA and DR setup, and one result with a number.
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
hide_slide(s)


# =================================================================== 18. next steps
s = std("A Live Demo Today, Then a POC on One Bank App", "Next steps", """
What we do:
Today: live demo on Kubernetes. WordPress reads its MySQL password from a Kubernetes secret that External Secrets keeps in sync with Secrets Manager. The app code does not change.
This week: HLD, plus the HA and DR design for DC1, DC2 and test.
On request: professional services review the chosen app and make the code change.
What we need from the bank: one representative application for the POC, and the site, HA and DR requirements for DC1 and DC2.
POC prerequisites (Deployment Guide): Kubernetes 1.30 or later (Tanzu fits), Helm 3 and kubectl, a default StorageClass with 10Gi per node, a minimum of 1 vCPU and 512Mi on a single node, and an internal registry with the images mirrored. HA sizing: to fill by the deployment team.
""")
tl = [("player-play", "Today", "Live demo: External Secrets sync"),
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
       ("stack-2", "Internal registry, mirrored images", NAVY), ("alert-triangle-r", "HA sizing: to fill", RED)]
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


# =================================================================== demo, 5 steps
def demo(n, title, notes_text):
    return std(title, f"Live demo, step {n} of 5", notes_text)


s = demo(1, "Step 1: The Password and the Sync Rule", """
The demo starts from a clean cluster. The resources from the earlier run are deleted first.
Left: the password sits in Secrets Manager under the KV engine secret, path demo/mysql, key password.
Right: the ExternalSecret YAML. refreshInterval 10s. secretStoreRef kind ClusterSecretStore, name vault-backend-demo. target name mysql-pass. data secretKey password, remoteRef key demo/mysql, property password.
Screens: frames from the recorded demo, with the presenter's webcam, the dock and the browser bar cropped out.
""")
for i, (img, head, rows) in enumerate([
        (D("smui"), "IN ACCUKNOX SECRETS MANAGER", [("key", "Path demo/mysql"), ("lock", "Key password")]),
        (D("yaml"), "THE EXTERNALSECRET OBJECT", [("clock", "Refresh every 10 s"), ("link", "Store: ClusterSecretStore"),
                                                 ("file-text", "Writes K8s secret mysql-pass")])]):
    x = 0.40 + i * 4.7
    label(s, x, 1.16, 4.5, head, size=10.5)
    shot(s, img, x, 1.46, 4.5, 2.3)
    for j, (icn, t) in enumerate(rows):
        y = 3.92 + j * 0.44
        ic(s, icn, x + 0.04, y, 0.32)
        box(s, x + 0.46, y - 0.04, 4.0, 0.4, text=t, size=12, color=INK, anchor=MSO_ANCHOR.MIDDLE, ml=0)

s = demo(2, "Step 2: Kubernetes Gets the Password Within 10 Seconds", """
1. kubectl apply on the ExternalSecret file creates the Kubernetes secret mysql-pass right away. k9s shows its decoded value.
2. A new value is saved in Secrets Manager with Create new version.
3. About 10 seconds later, mysql-pass holds the new value. Nobody touched Kubernetes.
At this point WordPress and MySQL are not deployed yet. This step shows the sync on its own.
""")
def grid4(slide, cells, last=None):
    """Four cells, 2 x 2. Each cell: number, caption, screenshot. `last` replaces cell 4 with a callout."""
    for i, (img, cap, fill) in enumerate(cells):
        x = 0.40 + (i % 2) * 4.7
        y = 1.14 + (i // 2) * 2.12
        step_no(slide, x, y + 0.02, i + 1, fill=fill)
        box(slide, x + 0.44, y, 4.0, 0.38, text=cap, size=12, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
        shot(slide, img, x, y + 0.44, 4.5, 1.58)
    if last:
        box(slide, 5.1, 3.26, 4.5, 2.1, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08,
            text=last, size=15, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=1.0, mr=0.3)
        ic(slide, "refresh", 5.34, 4.02, 0.56)


grid4(s, [(D("val1"), "kubectl apply creates mysql-pass", PRIMARY),
          (D("smnew"), "A new value is saved in AccuKnox", PRIMARY),
          (D("val2"), "About 10 s later, mysql-pass holds it", GREEN)],
      last="The operator keeps mysql-pass equal to the value in AccuKnox.")

s = demo(3, "Step 3: WordPress Reads mysql-pass With No Code Change", """
The MySQL and WordPress deployments are applied unchanged from the standard Kubernetes example.
Left: the WordPress deployment. WORDPRESS_DB_PASSWORD comes from valueFrom, secretKeyRef, name mysql-pass, key password.
Right: WordPress loads, so it reached MySQL with the synced password. The page shown is the WordPress install screen.
""")
label(s, 0.40, 1.16, 5.4, "THE WORDPRESS DEPLOYMENT", size=10.5)
shot(s, D("code"), 0.40, 1.46, 5.4, 2.8)
label(s, 6.1, 1.16, 3.5, "WORDPRESS LOADS", size=10.5)
shot(s, D("wps"), 6.1, 1.46, 3.5, 2.8)
fact(s, "file-text", "secretKeyRef points at mysql-pass", "The app reads the K8s secret it always read", 0.48, 4.48, 5.3)
fact(s, "circle-check", "Connected to MySQL", "The password came from AccuKnox", 6.18, 4.48, 3.4, col=GREEN)

s = demo(4, "Step 4: Changing the MySQL Password Breaks the Connection", """
The MySQL password is changed by hand inside the MySQL pod: ALTER USER for the wordpress user, then FLUSH PRIVILEGES.
The database now expects a password that the Kubernetes secret does not hold yet.
WordPress shows Error establishing a database connection.
""")
label(s, 0.40, 1.16, 4.5, "MYSQL PASSWORD CHANGED BY HAND", size=10.5)
shot(s, D("mysql"), 0.40, 1.46, 4.5, 2.5)
box(s, 4.92, 2.5, 0.16, 0.4, text="→", size=18, color=RED, bold=True, align=PP_ALIGN.CENTER,
    anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0, mt=0, mb=0)
label(s, 5.1, 1.16, 4.5, "WORDPRESS LOSES THE DATABASE", size=10.5, color=RED)
shot(s, D("err"), 5.1, 1.46, 4.5, 2.5)
callout(s, 0.40, 4.3, 9.2, 0.7, "alert-triangle", "The database and the Kubernetes secret no longer match, so WordPress cannot connect.",
        size=12, fill=RED_LT, color=RED, icolor="#C80019")

s = demo(5, "Step 5: A New Version and a Restart Restore the Connection", """
1. The new password is saved in Secrets Manager as a new version of demo/mysql.
2. The operator syncs it to mysql-pass within the refresh interval.
3. The WordPress pod is deleted, and Kubernetes starts a new one.
4. On startup the new pod reads the updated mysql-pass, and WordPress connects again.
Say it precisely: the sync alone did not fix the running app. The restart did, because the app reads the secret when it starts.
""")
for i, (img, cap) in enumerate([(D("smnew2"), "New version in AccuKnox"), (D("poddel"), "Restart the WordPress pod"),
                                 (D("val3"), "mysql-pass holds the new value"), (D("wp2s"), "WordPress connects again")]):
    x = 0.40 + (i % 2) * 4.7
    y = 1.12 + (i // 2) * 1.82
    step_no(s, x, y + 0.02, i + 1, fill=GREEN if i == 3 else PRIMARY)
    box(s, x + 0.44, y, 4.0, 0.36, text=cap, size=12, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    shot(s, img, x, y + 0.4, 4.5, 1.36)
callout(s, 0.40, 4.8, 9.2, 0.54, "refresh", "The sync alone did not fix the running app. The restart did.", size=12.5)

s = std("Watch the Two-Minute Demo", "Live demo, recorded", """
HIDDEN until the video is approved.
The edited recording: 2 minutes 0 seconds, 1600 x 900, AI voiceover. Faces and personal browser tabs are cropped out.
Local file: D:\\AccuKnox\\help\\references\\video-edits\\sm-eso-wordpress\\output\\sm-eso-wordpress.mp4
To embed: upload the MP4 to Drive, then Insert, Video, Google Drive in Google Slides, and place it over the poster frame.
""")
shot(s, D("poster"), 1.2, 1.2, 7.6, 4.0)
box(s, 4.55, 2.75, 0.9, 0.9, fill=PRIMARY, shape=MSO_SHAPE.OVAL)
ic(s, "player-play-w", 4.75, 2.95, 0.5)
hide_slide(s)


# =================================================================== close
closing_slide(prs)
# Final order: the agreed flow, then hidden backups after the closing slide.
ORDER = ["", "Table of Contents", "One Cluster Serves", "Every Secret Request", "Nine Building Blocks",
         "Two Ways to Connect", "The SDK Reads", "External Secrets Syncs", "A ClusterSecretStore", "Easier Setup Leaves",
         "Each Request Gets", "Three Nodes Keep", "Snapshots Every 15", "Installs and Runs", "Day 2 Operations",
         "Step 1:", "Step 2:", "Step 3:", "Step 4:", "Step 5:", "Watch the Two-Minute", "A Live Demo Today",
         "SEE US IN ACTION", "Java and .NET", "Python and Node.js", "Where Teams Already"]


def _title(sl):
    for sh in sl.placeholders:
        if sh.placeholder_format.idx == 0 and sh.text_frame.text.strip():
            return sh.text_frame.text.strip()
    return ""


_lst = prs.slides._sldIdLst
_ids = list(_lst)
_by = {}
for _sid, _sl in zip(_ids, prs.slides):
    _t = _title(_sl)
    _k = next((k for k in ORDER[1:] if _t.startswith(k)), "" if _sl.slide_layout.name == "AccuKnox Intro Title" else None)
    assert _k is not None, _t
    _by[_k] = _sid
for _sid in _ids:
    _lst.remove(_sid)
for _k in ORDER:
    _lst.append(_by[_k])
prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
