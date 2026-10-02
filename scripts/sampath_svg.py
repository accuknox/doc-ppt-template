# -*- coding: utf-8 -*-
"""
SVG diagrams for the Sampath Bank Secrets Manager deck. The worked example for
the shared kit in scripts/_aksvg.py: each d_*() builds one diagram from kit
primitives and real icons, and renders it to work/sampath/diagrams/<name>.png.

Canvas width 1280 px maps to the 9.2 in content width, so 1 px = 0.52 pt.

Run:  py -3.11 scripts/sampath_svg.py            all diagrams
      py -3.11 scripts/sampath_svg.py ha dr      some of them
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _aksvg import *          # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, "..", "work", "sampath", "diagrams")
_render = render


def render(name, w, h, body, bg=WHITE):
    return _render(name, w, h, body, OUTD, bg=bg)


# ================================================================== diagrams
def d_architecture():
    W, H = 1280, 590
    b = []
    b.append(text(0, 26, "YOUR APPLICATIONS", 19, PRIMARY, 700))
    b.append(text(345, 26, "SECRETS MANAGER ON THE BANK'S TANZU CLUSTER", 19, PRIMARY, 700))
    b.append(text(1018, 26, "BANK SYSTEMS", 19, PRIMARY, 700))
    apps = [(44, "Kubernetes pods", "Secret arrives as a file", ["kubernetes-original", "helm-original", "docker-original"], GREEN),
            (218, "App servers on VMs", "SDK or REST API call", ["java-original", "dotnetcore-original", "tomcat-original", "windows11-original"], PRIMARY),
            (392, "Jobs and pipelines", "CLI or REST API call", ["bash-original", "powershell-original", "linux-original", "argocd-original"], PRIMARY)]
    for y, h1, h2, logos, acc in apps:
        b.append(rect(0, y, 290, 156, fill=WHITE, stroke=GREY_BD))
        b.append(rect(0, y, 8, 156, fill=acc, stroke="none", r=4))
        b.append(text(22, y + 36, h1, 24, NAVY, 700))
        for i, lg in enumerate(logos):
            b.append(logo(lg, 22 + i * 62, y + 54, 46))
        b.append(text(22, y + 136, h2, 19, MUTE, 500))
        b.append(arrow(296, y + 78, 338, y + 78, acc, 4))
    b.append(ui("lock", 0, 560, 24, MUTE))
    b.append(text(32, 580, "Every call travels over TLS", 18, MUTE, 600, italic=True))
    # cluster
    b.append(rect(345, 44, 640, 504, fill=GREY_BG, stroke=GREY_BD, r=18))
    b.append(rect(362, 58, 606, 98, fill=NAVY, stroke="none", r=12))
    b.append(ui("fingerprint", 376, 68, 30, WHITE))
    b.append(text(414, 92, "Auth methods: who is asking?", 21, WHITE, 700))
    xx = 376
    for a in ["K8s service account", "AppRole", "Entra ID (OIDC)", "LDAP", "JWT", "TLS cert"]:
        wdt = 16 + len(a) * 7.6
        b.append(pill(xx, 112, wdt, 30, a, fill="#24358A", color=WHITE, size=14, weight=500))
        xx += wdt + 5
    for i, (n, role, col) in enumerate([("node-0", "Active", PRIMARY), ("node-1", "Standby", SECOND), ("node-2", "Standby", SECOND)]):
        x = 362 + i * 206
        b.append(rect(x, 170, 194, 92, fill=WHITE, stroke=col, sw=3))
        b.append(ui("server-2", x + 12, 182, 36, col))
        b.append(text(x + 56, 206, n, 22, NAVY, 700))
        b.append(pill(x + 56, 218, 100 if role == "Active" else 110, 28, role, fill=col, color=WHITE, size=16))
        b.append(cyl(x + 37, 274, 120, 50, "Raft 10Gi"))
    b.append(arrow(558, 300, 596, 300, SECOND, 2.5, "6 5", both=True))
    b.append(arrow(764, 300, 802, 300, SECOND, 2.5, "6 5", both=True))
    b.append(text(665, 342, "data replicates between all three nodes", 15, SECOND, 600, "middle", italic=True))
    b.append(text(362, 372, "Secret engines", 20, NAVY, 700))
    b.append(text(520, 372, "policy decides which paths each identity reads", 16, MUTE, 500, italic=True))
    xx = 362
    for ic, lb in [("key", "KV v2"), ("database", "Database"), ("certificate", "PKI"), ("lock", "Transit"), ("terminal-2", "SSH"), ("clock", "TOTP")]:
        wdt = 48 + len(lb) * 8.4
        b.append(chip(xx, 382, wdt, 38, ic, lb, size=15))
        xx += wdt + 7
    b.append(chip(362, 432, 298, 48, "webhook", "Agent Injector", size=19))
    b.append(chip(670, 432, 298, 48, "box", "CSI provider", size=19))
    b.append(rect(362, 492, 606, 40, fill=GREEN_LT, stroke="none", r=20))
    b.append(ui("shield-check", 376, 498, 28, GREEN_DK))
    b.append(text(412, 519, "KubeArmor runtime hardening on every pod", 19, GREEN_DK, 700))
    sysrows = [(44, "Identity", ["Entra ID or LDAP"], "brand", "azure-original"),
               (170, "Snapshots", ["S3-compatible", "bucket, on-prem"], "ui", "bucket"),
               (296, "SIEM", ["Receives the", "audit log"], "ui", "eye"),
               (422, "Monitoring", ["Prometheus", "and Grafana"], "brand", "prometheus-original")]
    for y, h1, h2, kind, ic in sysrows:
        b.append(rect(1018, y, 262, 112, fill=WHITE, stroke=GREY_BD))
        b.append(logo(ic, 1032, y + 16, 46) if kind == "brand" else ui(ic, 1032, y + 16, 46, PRIMARY))
        if ic == "prometheus-original":
            b.append(logo("grafana-original", 1036, y + 66, 38))
        b.append(text(1092, y + 42, h1, 23, NAVY, 700))
        b.append(text(1092, y + 70, h2, 17, MUTE, 500))
        b.append(arrow(988, y + 56, 1012, y + 56, SECOND, 3))
    return render("architecture", W, H, "".join(b))


def d_flow():
    W, H = 1280, 360
    b = []
    steps = [("user", "Application", "Starts with its own identity", NAVY),
             ("fingerprint", "1. Authenticate", "Service account, AppRole, cert", PRIMARY),
             ("id-badge-2", "2. Get a token", "Short-lived, tied to one policy", PRIMARY),
             ("key", "3. Read the secret", "Only allowed paths, over TLS", PRIMARY),
             ("eye", "4. Audit", "Allowed and denied calls logged", GREEN_DK)]
    for i, (ic, h1, h2, col) in enumerate(steps):
        x = i * 260
        b.append(rect(x, 40, 228, 250, fill=WHITE, stroke=col if i else GREY_BD, sw=3))
        b.append(f'<circle cx="{x+114}" cy="110" r="50" fill="{LAV if col != GREEN_DK else GREEN_LT}"/>')
        b.append(ui(ic, x + 84, 80, 60, col))
        b.append(text(x + 114, 200, h1, 25, NAVY, 700, "middle"))
        lines = h2.split(", ") if len(h2) > 22 else [h2]
        words = h2.split(" "); l1, l2 = "", ""
        for wd in words:
            if len(l1) + len(wd) < 18 and not l2: l1 += wd + " "
            else: l2 += wd + " "
        b.append(text(x + 114, 236, [l1.strip(), l2.strip()], 19, MUTE, 500, "middle"))
        if i < 4:
            b.append(arrow(x + 232, 165, x + 256, 165, PRIMARY, 4))
    b.append(rect(0, 314, 1280, 44, fill=LAV, stroke="none", r=22))
    b.append(text(640, 343, "The app never holds a long-lived password. A revoked token stops access at once.", 21, NAVY, 600, "middle"))
    return render("flow", W, H, "".join(b))


def d_patterns():
    W, H = 1280, 520
    b = []
    cols = [("1  SDK or REST API", "Small code change", PURPLE, LAV),
            ("2  File injection", "No code change", GREEN_DK, GREEN_LT),
            ("3  Environment variable", "Start command only", GREEN_DK, GREEN_LT),
            ("4  CSI volume", "No code change", GREEN_DK, GREEN_LT)]
    for i, (h1, tag, tc, tf) in enumerate(cols):
        x = i * 324
        b.append(rect(x, 0, 304, 520, fill=WHITE, stroke=GREY_BD))
        b.append(rect(x, 0, 304, 10, fill=PRIMARY if i == 0 else GREEN, stroke="none", r=5))
        b.append(text(x + 18, 48, h1, 23, NAVY, 700))
        b.append(pill(x + 18, 64, 200, 34, tag, fill=tf, color=tc, size=17))
        # mini diagram area
        b.append(rect(x + 18, 116, 268, 230, fill=GREY_BG, stroke="none", r=12))
        sm = (x + 152, 150)  # secrets manager position
        b.append(ui("lock", x + 126, 128, 52, NAVY))
        b.append(text(x + 152, 200, "Secrets Manager", 16, NAVY, 700, "middle"))
        if i == 0:
            b.append(rect(x + 62, 262, 180, 70, fill=WHITE, stroke=PURPLE, sw=2.5, r=10))
            b.append(ui("code", x + 74, 276, 40, PURPLE))
            b.append(text(x + 122, 292, "App code", 18, NAVY, 700))
            b.append(text(x + 122, 316, "calls the API", 15, MUTE, 500))
            b.append(arrow(x + 152, 260, x + 152, 210, PURPLE, 3, both=True))
        else:
            b.append(rect(x + 34, 236, 236, 102, fill=WHITE, stroke=GREEN, sw=2.5, r=10, dash="7 5"))
            b.append(text(x + 46, 256, "Pod", 15, GREEN_DK, 700))
            if i == 1:
                b.append(rect(x + 46, 266, 92, 62, fill=LAV, stroke="none", r=8))
                b.append(text(x + 92, 292, "Agent", 16, NAVY, 700, "middle"))
                b.append(text(x + 92, 314, "sidecar", 14, MUTE, 500, "middle"))
                b.append(ui("file-text", x + 150, 268, 30, GREEN_DK))
                b.append(rect(x + 186, 266, 74, 62, fill=WHITE, stroke=GREY_BD, r=8))
                b.append(text(x + 223, 302, "App", 17, NAVY, 700, "middle"))
                b.append(arrow(x + 92, 262, x + 120, 212, GREEN, 3))
            elif i == 2:
                b.append(rect(x + 46, 266, 92, 62, fill=LAV, stroke="none", r=8))
                b.append(text(x + 92, 292, "Agent", 16, NAVY, 700, "middle"))
                b.append(text(x + 92, 314, "sidecar", 14, MUTE, 500, "middle"))
                b.append(text(x + 165, 304, "$ENV", 15, GREEN_DK, 700, "middle"))
                b.append(rect(x + 196, 266, 64, 62, fill=WHITE, stroke=GREY_BD, r=8))
                b.append(text(x + 228, 302, "App", 17, NAVY, 700, "middle"))
                b.append(arrow(x + 92, 262, x + 120, 212, GREEN, 3))
            else:
                b.append(rect(x + 46, 266, 92, 62, fill=LAV, stroke="none", r=8))
                b.append(text(x + 92, 292, "CSI", 16, NAVY, 700, "middle"))
                b.append(text(x + 92, 314, "volume", 14, MUTE, 500, "middle"))
                b.append(logo("kubernetes-original", x + 148, 280, 30))
                b.append(rect(x + 186, 266, 74, 62, fill=WHITE, stroke=GREY_BD, r=8))
                b.append(text(x + 223, 302, "App", 17, NAVY, 700, "middle"))
                b.append(arrow(x + 92, 262, x + 120, 212, GREEN, 3))
        desc = [["The app asks at run", "time. The secret lives", "only in memory."],
                ["A sidecar writes the", "secret to a file the", "app already reads."],
                ["The start command", "loads the file into", "env vars."],
                ["The pod mounts the", "secret as a volume or", "a Kubernetes Secret."]][i]
        b.append(text(x + 18, 384, desc, 19, INK, 500))
        best = ["Most secure", "Best for Tanzu apps", "Use files if you can", "Apps on K8s Secrets"][i]
        b.append(ui("check" if False else "checkbox", x + 18, 472, 26, tc))
        b.append(text(x + 52, 492, best, 19, tc, 700))
    return render("patterns", W, H, "".join(b))


def d_injector():
    W, H = 640, 500
    b = []
    b.append(rect(0, 0, 640, 500, fill=GREY_BG, stroke="none", r=18))
    b.append(text(20, 36, "INSIDE THE POD AT START", 18, PRIMARY, 700))
    # secrets manager
    b.append(rect(420, 60, 200, 92, fill=NAVY, stroke="none", r=12))
    b.append(ui("lock", 434, 76, 40, WHITE))
    b.append(text(482, 100, "Secrets", 20, WHITE, 700))
    b.append(text(482, 124, "Manager", 20, WHITE, 700))
    # webhook
    b.append(rect(20, 60, 260, 92, fill=WHITE, stroke=PRIMARY, sw=2.5, r=12))
    b.append(ui("webhook", 34, 78, 40, PRIMARY))
    b.append(text(84, 100, "Agent Injector", 20, NAVY, 700))
    b.append(text(84, 126, "reads the annotations", 16, MUTE, 500))
    b.append(badge(270, 62, 1))
    # pod
    b.append(rect(20, 186, 600, 290, fill=WHITE, stroke=GREEN, sw=3, r=14, dash="9 6"))
    b.append(logo("kubernetes-original", 372, 452, 22))
    b.append(text(400, 469, "Pod: payments-app", 17, GREEN_DK, 700))
    b.append(arrow(150, 152, 150, 244, PRIMARY, 3))
    b.append(text(160, 176, "adds the agent", 15, PRIMARY, 600))
    b.append(rect(40, 248, 220, 100, fill=LAV, stroke="none", r=12))
    b.append(ui("user", 54, 262, 34, NAVY))
    b.append(text(98, 284, "Agent sidecar", 19, NAVY, 700))
    b.append(text(54, 330, "logs in with the pod's SA", 15, MUTE, 500))
    b.append(badge(252, 252, 2))
    b.append(arrow(260, 268, 470, 156, PURPLE, 3, both=True))
    b.append(text(432, 216, "TLS", 16, PURPLE, 700))
    # memory volume
    b.append(rect(40, 366, 220, 92, fill=WHITE, stroke=GREY_BD, r=12))
    b.append(ui("file-text", 54, 382, 36, GREEN_DK))
    b.append(text(98, 404, "/vault/secrets/db", 16, NAVY, 700))
    b.append(text(98, 428, "in-memory volume", 15, MUTE, 500))
    b.append(badge(252, 370, 3))
    b.append(arrow(150, 348, 150, 364, GREEN, 3))
    # app
    b.append(rect(340, 292, 260, 146, fill=WHITE, stroke=NAVY, sw=2.5, r=12))
    b.append(ui("code", 356, 316, 38, NAVY))
    b.append(text(404, 342, "App container", 20, NAVY, 700))
    b.append(text(356, 386, "Reads the file it", 17, MUTE, 500))
    b.append(text(356, 410, "already reads today", 17, MUTE, 500))
    b.append(badge(590, 304, 4))
    b.append(arrow(262, 412, 336, 400, GREEN, 3))
    return render("injector", W, H, "".join(b))


def d_rotation():
    W, H = 1280, 300
    b = []
    steps = [("database", "DB engine", ["Holds the admin", "connection to the DB"], "db"),
             ("refresh", "Rotate", ["New password on a", "lease or a schedule"], None),
             ("file-text", "Deliver", ["Agent rewrites the file,", "or the SDK asks again"], None),
             ("code", "Application", ["New connections use", "the new password"], None)]
    for i, (ic, h1, sub, extra) in enumerate(steps):
        x = i * 322
        b.append(rect(x, 10, 290, 200, fill=WHITE, stroke=PRIMARY if i else NAVY, sw=3))
        b.append(f'<circle cx="{x+56}" cy="68" r="40" fill="{LAV}"/>')
        b.append(ui(ic, x + 32, 44, 48, PRIMARY))
        b.append(text(x + 110, 64, h1, 24, NAVY, 700))
        b.append(badge(x + 270, 30, i + 1, r=15, size=17))
        b.append(text(x + 18, 146, sub, 19, MUTE, 500))
        if i < 3:
            b.append(arrow(x + 294, 110, x + 318, 110, PRIMARY, 4))
    b.append(text(0, 262, "Shown in the demo", 20, NAVY, 700))
    for i, lg in enumerate(["oracle-original", "postgresql-original", "mysql-original"]):
        b.append(logo(lg, 196 + i * 64, 228, 52))
    b.append(text(420, 262, "Old password stays valid until its lease ends, so live connections finish.", 20, MUTE, 500))
    return render("rotation", W, H, "".join(b))


def d_ha():
    W, H = 640, 520
    b = []
    b.append(rect(0, 0, 640, 520, fill=GREY_BG, stroke="none", r=18))
    b.append(rect(180, 20, 280, 70, fill=WHITE, stroke=GREY_BD, r=12))
    b.append(ui("route", 194, 34, 40, NAVY))
    b.append(text(244, 54, "Load balancer", 20, NAVY, 700))
    b.append(text(244, 78, "Ingress or Route", 16, MUTE, 500))
    b.append(arrow(320, 90, 320, 124, PRIMARY, 4))
    b.append(rect(180, 128, 280, 64, fill=WHITE, stroke=PRIMARY, sw=2.5, r=12))
    b.append(ui("arrows-exchange", 194, 140, 40, PRIMARY))
    b.append(text(244, 168, "Active service", 20, NAVY, 700))
    b.append(arrow(260, 192, 110, 238, PRIMARY, 4))
    for i, (n, r, col) in enumerate([("node-0", "Leader", PRIMARY), ("node-1", "Standby", SECOND), ("node-2", "Standby", SECOND)]):
        x = 20 + i * 210
        b.append(rect(x, 242, 180, 120, fill=WHITE, stroke=col, sw=3))
        b.append(ui("server-2", x + 12, 256, 38, col))
        b.append(text(x + 58, 282, n, 21, NAVY, 700))
        b.append(pill(x + 58, 294, 104, 28, r, fill=col, color=WHITE, size=16))
        b.append(text(x + 14, 350, "own host", 15, MUTE, 500))
        b.append(cyl(x + 30, 380, 120, 52, "Raft disk"))
    b.append(arrow(200, 300, 230, 300, SECOND, 2.5, "6 5", both=True))
    b.append(arrow(410, 300, 440, 300, SECOND, 2.5, "6 5", both=True))
    b.append(text(320, 470, "Dashed: Raft replication, mutual TLS, port 8201", 17, MUTE, 500, "middle", italic=True))
    b.append(text(320, 500, "Standbys forward requests to the leader", 17, MUTE, 500, "middle", italic=True))
    return render("ha", W, H, "".join(b))


def d_dr():
    W, H = 1280, 420
    b = []
    # DC1
    for j, (lab, x) in enumerate([("DC1 production", 0), ("DC2 production", 495)]):
        b.append(rect(x, 0, 400, 250, fill=GREY_BG, stroke=GREY_BD, r=16))
        b.append(ui("building-bank", x + 16, 14, 40, NAVY))
        b.append(text(x + 66, 44, lab, 24, NAVY, 700))
        for i in range(3):
            nx = x + 18 + i * 124
            b.append(rect(nx, 70, 112, 84, fill=WHITE, stroke=PRIMARY if i == 0 else SECOND, sw=2.5))
            b.append(ui("server-2", nx + 38, 80, 36, PRIMARY if i == 0 else SECOND))
            b.append(text(nx + 56, 142, "node-%d" % i, 16, NAVY, 700, "middle"))
        b.append(rect(x + 18, 172, 364, 60, fill=WHITE, stroke=GREY_BD, r=10))
        b.append(ui("history", x + 32, 182, 38, PRIMARY))
        b.append(text(x + 80, 200, "Snapshot agent", 19, NAVY, 700))
        b.append(text(x + 80, 222, "every 15 min, kept 14 days", 15, MUTE, 500))
    # link between DCs
    b.append(arrow(408, 100, 486, 100, RED, 3, "7 5", both=True))
    b.append(rect(406, 120, 82, 32, fill=RED_LT, stroke=RED, sw=1.5, r=8, dash="5 4"))
    b.append(text(447, 142, "to fill", 16, RED, 700, "middle"))
    # bucket
    b.append(rect(955, 0, 325, 250, fill=WHITE, stroke=GREY_BD, r=16))
    b.append(ui("bucket", 972, 20, 56, PRIMARY))
    b.append(text(1038, 46, "Snapshot bucket", 23, NAVY, 700))
    b.append(text(1038, 72, "S3-compatible, on-prem", 16, MUTE, 500))
    b.append(text(974, 128, ["Holds encrypted", "Raft snapshots.", "A restore needs the", "unseal keys too."], 18, INK, 500))
    b.append(curve("M390,232 C560,300 820,300 950,200", PRIMARY, 3))
    b.append(curve("M884,202 L950,202", PRIMARY, 3))
    b.append(text(640, 296, "Snapshots upload", 17, PRIMARY, 600, "middle"))
    # test
    b.append(rect(0, 300, 420, 110, fill=WHITE, stroke=GREY_BD, r=16))
    b.append(ui("zoom-check", 18, 322, 44, MUTE))
    b.append(text(74, 344, "Test environment", 22, NAVY, 700))
    b.append(text(74, 372, "Separate install, its own keys", 17, MUTE, 500))
    b.append(rect(495, 320, 785, 90, fill=LAV, stroke="none", r=14))
    b.append(ui("refresh", 513, 340, 46, PRIMARY))
    b.append(text(573, 358, "Restore path, confirmed in the chart", 21, NAVY, 700))
    b.append(text(573, 388, "Load the latest snapshot into a cluster, then unseal it.", 18, MUTE, 500))
    return render("dr", W, H, "".join(b))


def d_airgap():
    W, H = 1280, 300
    b = []
    zones = [(0, 300, "Connected host", "Outside the bank", "download", MUTE),
             (360, 300, "Transfer", "Approved media", "package", PURPLE),
             (720, 260, "Bank registry", "registry.bank.local", "stack-2", PRIMARY),
             (1020, 260, "Tanzu cluster", "helm upgrade --install", "kubernetes-original", GREEN_DK)]
    for i, (x, w, h1, h2, ic, col) in enumerate(zones):
        b.append(rect(x, 30, w, 170, fill=WHITE, stroke=col, sw=3))
        if ic.endswith("original"):
            b.append(logo(ic, x + w / 2 - 32, 46, 64))
        else:
            b.append(ui(ic, x + w / 2 - 32, 46, 64, col))
        b.append(text(x + w / 2, 146, h1, 24, NAVY, 700, "middle"))
        b.append(text(x + w / 2, 176, h2, 17, MUTE, 500, "middle"))
        b.append(badge(x + 24, 30, i + 1, r=17, fill=col))
        if i < 3:
            nx = zones[i + 1][0]
            b.append(arrow(x + w + 4, 115, nx - 6, 115, col, 4))
    # air gap boundary
    b.append(f'<line x1="690" y1="0" x2="690" y2="230" stroke="{RED}" stroke-width="3" stroke-dasharray="10 7"/>')
    b.append(ui("wifi-off", 672, 232, 36, RED))
    b.append(text(720, 258, "Air gap: nothing inside calls the internet", 19, RED, 700))
    b.append(text(0, 258, "Pull 5 images and the chart tar once", 19, MUTE, 600))
    b.append(text(0, 288, "Unseal with bank key holders, 3 of 5 Shamir keys", 19, MUTE, 600))
    return render("airgap", W, H, "".join(b))


if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    fns = {"architecture": d_architecture, "flow": d_flow, "patterns": d_patterns,
           "injector": d_injector, "rotation": d_rotation, "ha": d_ha, "dr": d_dr, "airgap": d_airgap}
    for k, f in fns.items():
        if "all" in which or k in which:
            print(k, f())
