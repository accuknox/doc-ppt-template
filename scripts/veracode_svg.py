# -*- coding: utf-8 -*-
"""
Diagrams for the AccuKnox pitch deck to Veracode. Run before build_veracode_pitch.py.

  py -3.11 scripts/veracode_svg.py

Every label comes from help.accuknox.com pages, accuknox.com/differentiators or the
AccuKnox Pricing and Sizing sheet (SEP 2026). The build script notes cite each page.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _aksvg import *  # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "work", "veracode", "diagrams")


# ---------------------------------------------------------------- 1. problem
def problem():
    W, H = 1280, 372
    b = []
    stages = [
        ("code", "Source", "code", ["Flaws in", "your code"]),
        ("file-code", "IaC", "templates", ["Public buckets,", "hardcoded", "secrets"]),
        ("git-merge", "CI/CD", "build", ["Vulnerable", "base images", "ship"]),
        ("package", "Container", "registry", ["Images nobody", "rescans"]),
        ("container", "Kubernetes", "runtime", ["Exec from /tmp,", "crypto-mining"]),
        ("cloud", "Cloud", "accounts", ["Misconfig", "and drift"]),
        ("database", "Data", "stores", ["PII and PCI", "in open", "buckets"]),
        ("api", "Live", "APIs", ["Shadow APIs,", "no auth"]),
    ]
    x0, cw, gap = 10, 146, 12
    xs = [x0 + i * (cw + gap) for i in range(8)]
    # top brackets
    b.append(rect(xs[0], 6, cw, 44, fill=GREY_BG, stroke=GREY_BD, r=10))
    b.append(text(xs[0] + cw / 2, 35, "Code scan", 18, NAVY, 700, anchor="middle"))
    groups = [(1, 4, "Container Security + IaC"), (5, 5, "CSPM"), (6, 6, "DSPM"), (7, 7, "API Security")]
    for a, z, lab in groups:
        gx, gw = xs[a], xs[z] + cw - xs[a]
        b.append(rect(gx, 6, gw, 44, fill=PRIMARY, stroke=PRIMARY, r=10))
        b.append(text(gx + gw / 2, 35, lab, 19, WHITE, 700, anchor="middle"))
    # stage cards
    for i, (ic, l1, l2, risk) in enumerate(stages):
        x = xs[i]
        acc = MUTE if i == 0 else PRIMARY
        b.append(rect(x, 66, cw, 132, fill=WHITE, stroke=acc, sw=2.5, r=14))
        b.append(f'<circle cx="{x + cw / 2}" cy="{104}" r="27" fill="{LAV}"/>')
        b.append(ui(ic, x + cw / 2 - 18, 86, 36, acc))
        b.append(text(x + cw / 2, 158, [l1, l2], 19, NAVY, 700, anchor="middle", lh=1.15))
        if i < 7:
            b.append(arrow(x + cw + 1, 132, x + cw + gap - 1, 132, color=PRIMARY, sw=2.5))
        # risk box
        b.append(rect(x, 214, cw, 116, fill=RED_LT, stroke=RED, sw=1.5, r=12))
        b.append(ui("alert-triangle", x + cw / 2 - 13, 224, 26, RED))
        b.append(text(x + cw / 2, 274, risk, 17, RED, 700, anchor="middle", lh=1.2))
    b.append(text(xs[0], 362, "Risk found today", 17, MUTE, 600))
    b.append(text(xs[1], 362, "Risk that appears after the commit, in the build, the cloud, the data and the APIs", 17, RED, 700))
    return render("problem", W, H, "".join(b), OUT)


# ----------------------------------------------------------- 2. architecture
def architecture():
    W, H = 1280, 512
    b = []
    heads = [(10, 270, "1  Sources"), (318, 262, "2  Collect"), (628, 372, "3  AccuKnox control plane"), (1048, 222, "4  Act")]
    for x, w, h in heads:
        b.append(text(x, 26, h, 20, PRIMARY, 700))
    src = [("file-search", "Code scanners (SARIF)"), ("git-merge", "CI/CD pipelines"),
           ("package", "Container registries"), ("container", "Kubernetes and VMs"),
           ("cloud", "AWS, Azure, GCP"), ("database", "Data stores"), ("api", "API gateways")]
    for i, (ic, lab) in enumerate(src):
        b.append(chip(10, 44 + i * 64, 270, 52, ic, lab, size=17))
    col = [("upload", "SARIF and API import"), ("terminal-2", "CI plugins and CLI"),
           ("shield-lock", "KubeArmor agent"), ("cloud-lock", "Agentless, read-only"),
           ("scan", "DSPM scanner in region"), ("plug-connected", "API traffic connectors")]
    for i, (ic, lab) in enumerate(col):
        b.append(chip(318, 50 + i * 75, 262, 56, ic, lab, size=17))
    # big flow arrows
    for x1, x2 in ((284, 314), (584, 624), (1004, 1044)):
        b.append(arrow(x1, 268, x2, 268, color=PRIMARY, sw=6))
    # control plane
    b.append(rect(628, 44, 372, 456, fill=NAVY, stroke=NAVY, r=18))
    cp = [("filter", "Normalize and dedupe", None),
          ("hierarchy-2", "Correlate on one", "asset graph"),
          ("target", "Prioritize with Runtime", "Verified, KEV, EPSS"),
          ("certificate", "Map to 40+ compliance", "frameworks"),
          ("settings-automation", "Rules engine for", "tickets and alerts")]
    for i, (ic, l1, l2) in enumerate(cp):
        y = 64 + i * 86
        b.append(rect(646, y, 336, 72, fill=NAVY_DK, stroke=PURPLE, sw=1.5, r=12))
        b.append(ui(ic, 660, y + 16, 40, "#FFFFFF"))
        lines = [l1] if l2 is None else [l1, l2]
        ty = y + 44 if l2 is None else y + 31
        b.append(text(714, ty, lines, 18, WHITE, 600, lh=1.2))
    out = [("jira-original", "Jira, ServiceNow", True), ("server-bolt", "SIEM, syslog", False),
           ("slack-original", "Slack, email", True), ("report-analytics", "Reports", False),
           ("message-chatbot", "Ask AI", False)]
    for i, (ic, lab, brand) in enumerate(out):
        b.append(chip(1048, 58 + i * 90, 222, 60, ic, lab, size=18, brand=brand))
    return render("architecture", W, H, "".join(b), OUT)


# ------------------------------------------------- 3. deployment architecture
def deploy_arch():
    W, H = 1280, 468
    b = []
    b.append(rect(8, 8, 846, 452, fill="#F7F8FC", stroke=PRIMARY, sw=2.5, r=18, dash="12 8"))
    b.append(ui("building", 26, 18, 30, PRIMARY))
    b.append(text(64, 42, "Your environment", 21, PRIMARY, 700))
    rows = [("kubernetes-original", True, "Kubernetes clusters", "KubeArmor DaemonSet and KSPM job, both by Helm"),
            ("github-original", True, "CI/CD pipelines", "Image and IaC scans in the pipeline, SARIF upload"),
            ("amazonwebservices-original-wordmark", True, "Cloud accounts", "Agentless. AWS role: ReadOnlyAccess + SecurityAudit"),
            ("database", False, "Data region", "DSPM scanner as VM or CronJob. Read-only, no inbound ports"),
            ("api", False, "API gateways", "AWS API Gateway, Istio, NGINX, Kong, F5 BIG-IP")]
    for i, (ic, brand, head, sub) in enumerate(rows):
        y = 62 + i * 78
        b.append(rect(26, y, 810, 66, fill=WHITE, stroke=GREY_BD, sw=1.5, r=12))
        b.append(logo(ic, 40, y + 11, 44) if brand else ui(ic, 40, y + 11, 44, PRIMARY))
        b.append(text(100, y + 29, head, 20, NAVY, 700))
        b.append(text(100, y + 54, sub, 17, MUTE, 500))
        b.append(arrow(838, y + 33, 924, 228, color=PRIMARY, sw=2.5))
    # control plane
    b.append(rect(930, 96, 342, 266, fill=NAVY, stroke=NAVY, r=18))
    b.append(ui("server-2", 952, 116, 44, "#FFFFFF"))
    b.append(text(1008, 136, ["AccuKnox", "control plane"], 21, WHITE, 700, lh=1.15))
    for i, ln in enumerate(["Runs on Kubernetes", "SaaS, your cloud,", "on-prem or air-gapped", "Token-authenticated APIs"]):
        b.append(text(954, 214 + i * 30, ln, 18, "#B8C4E8", 500))
    b.append(rect(930, 378, 342, 82, fill=GREEN_LT, stroke=GREEN, sw=1.5, r=12))
    b.append(ui("shield-check", 944, 394, 36, GREEN_DK))
    b.append(text(990, 410, ["Runtime enforcement keeps", "working if the plane is down"], 17, GREEN_DK, 700, lh=1.2))
    return render("deploy_arch", W, H, "".join(b), OUT)


# ------------------------------------------------------- 4. deployment modes
def modes():
    W, H = 1280, 250
    b = []
    pw, gap = 296, 24
    specs = [
        ("SaaS", False, PRIMARY, "AccuKnox cloud"),
        ("Your Cloud", True, PRIMARY, "Your cloud account"),
        ("On-Premises", True, PRIMARY, "Your servers"),
        ("Air-Gapped", True, RED, "Your isolated network"),
    ]
    for i, (name, inside, col, bound) in enumerate(specs):
        x = 10 + i * (pw + gap)
        b.append(rect(x, 6, pw, 236, fill=WHITE, stroke=GREY_BD, sw=1.5, r=16))
        # customer boundary
        bw = 176 if not inside else pw - 28
        b.append(rect(x + 14, 22, bw, 204, fill="#F7F8FC", stroke=col, sw=2, r=12, dash="9 6"))
        b.append(text(x + 26, 48, bound if inside else "Your network", 17, col, 700))
        # workloads
        for j, ic in enumerate(("container", "cloud", "api")):
            b.append(rect(x + 28, 66 + j * 50, 60, 40, fill=WHITE, stroke=GREY_BD, sw=1.5, r=8))
            b.append(ui(ic, x + 44, 72 + j * 50, 28, PRIMARY))
        # control plane box
        cx = x + 210 if not inside else x + 132
        cy = 96
        b.append(rect(cx, cy, 80 if not inside else 140, 84, fill=NAVY, stroke=NAVY, r=12))
        b.append(ui("shield-lock", cx + (40 if not inside else 70) - 16, cy + 10, 32, "#FFFFFF"))
        b.append(text(cx + (40 if not inside else 70), cy + 68, "Control" if not inside else "Control plane", 17, WHITE, 700, anchor="middle"))
        if not inside:
            b.append(arrow(x + 120, 138, cx - 4, 138, color=PRIMARY, sw=3))
        else:
            b.append(arrow(x + 92, 138, cx - 4, 138, color=PRIMARY, sw=3))
        if name == "Air-Gapped":
            b.append(f'<circle cx="{x + pw - 50}" cy="{62}" r="20" fill="{RED_LT}"/>')
            b.append(ui("wifi-off", x + pw - 64, 48, 28, RED))
    return render("modes", W, H, "".join(b), OUT)


if __name__ == "__main__":
    pngs = [problem(), architecture(), deploy_arch(), modes()]
    contact_sheet(pngs, os.path.join(OUT, "_sheet.png"), cols=2)
    print("\n".join(pngs))
