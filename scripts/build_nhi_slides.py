# -*- coding: utf-8 -*-
"""
Three slides on Non-Human Identity (NHI): workload, service and agentic identity.
Built for the "[LATEST] AccuKnox Agent Identity" Google Slides deck
(1zR9wOjCOaFjWNghenHZYjLwN93ypuln9lAXU3YN5oOg) after Nat asked for NHI collateral.

Every slide tells one story in the same order: what goes wrong (attack path, one
number, the OWASP NHI Top 10 risks), what AccuKnox does (a real product artifact and
capability rows), and the one line that sets AccuKnox apart. Each capability carries
a status pill, so a reader never mistakes a preview for a shipped feature.

Sources, opened 2026-10-26:
  help docs  use-cases/cards/Service-Account-token.md, use-cases/zero-trust.md,
             use-cases/kiem.md, secrets-manager/overview.md, secrets-manager/architecture.md,
             support-matrix/cicd-support-matrix.md, getting-started/ciem-overview.md
             (marked Coming soon), agentz/index.md, getting-started/3.5-release.md,
             use-cases/shadow-ai-discovery.md
  this deck  slides 11 to 19: SPIFFE identity and OpenFGA caller-chain authorization.
             Design material, so those rows carry a Preview pill.
  external   OWASP NHI Top 10 2025, GitGuardian State of Secrets Sprawl 2025,
             CyberArk 2025 Identity Security Landscape, SailPoint 2025 AI agent report.

Build:   py -3.11 scripts/build_nhi_slides.py
"""
import os, shutil, sys
from pptx import Presentation
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import *          # noqa: F401,F403
import _aksvg as S

google_safe()

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "PPT Template.pptx")
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_NHI_Three_Pillars.pptx")
WORK = os.path.join(HERE, "..", "work", "nhi")
DIAG = os.path.join(WORK, "diagrams")

LCOL_X, LCOL_W = CX, 4.25
RCOL_X, RCOL_W = 4.85, 4.75
STATUS = {"Shipped": (GREEN_LT, GREEN_DK), "Preview": (LAV, PURPLE),
          "Coming soon": (GREY_BG, MUTE)}


# =================================================================== diagrams
def attack_path(name, steps):
    """Three red steps left to right. steps: [(icon, [line1, line2]), ...]"""
    b, bw, gap = [], 188, 38
    for i, (ic, lines) in enumerate(steps):
        x = i * (bw + gap)
        b.append(S.rect(x, 4, bw, 150, fill=S.RED_LT if i == 2 else S.WHITE, stroke=S.RED, sw=2))
        b.append(S.badge(x + 24, 30, i + 1, r=15, fill=S.RED, size=17))
        b.append(S.ui(ic, x + bw / 2 - 20, 22, 40, S.RED))
        b.append(S.text(x + bw / 2, 100, lines, 18, S.INK, 600, anchor="middle", lh=1.2))
        if i < 2:
            b.append(S.arrow(x + bw + 3, 79, x + bw + gap - 4, 79, color=S.RED))
    return S.render(name, 640, 158, "".join(b), DIAG)


def ciem_mock():
    """CIEM identity list, redrawn from the real screen in help docs (ciem-identity-list.png)."""
    b = [S.rect(0, 2, 638, 160, fill=S.WHITE, stroke=S.GREY_BD, sw=2, r=12),
         S.text(18, 30, "Identity", 17, S.MUTE, 600), S.text(318, 30, "Risk class", 17, S.MUTE, 600),
         S.text(530, 30, "Type", 17, S.MUTE, 600),
         f'<line x1="2" y1="42" x2="636" y2="42" stroke="{S.GREY_BD}" stroke-width="1.5"/>']
    rows = [("dspm-scanner-role", "Credentials Exposure", S.RED, S.RED_LT, "machine"),
            ("pricing-poc-CURCrawler", "Data Exfiltration", S.PURPLE, S.LAV, "machine"),
            ("Iam_Full_Access", "Privilege Escalation", S.PRIMARY, S.LAV, "group")]
    for i, (n, risk, col, fill, kind) in enumerate(rows):
        y = 50 + i * 37
        b.append(S.ui("settings" if kind == "machine" else "users", 16, y + 6, 22, S.SECOND))
        b.append(S.text(46, y + 24, n, 17, S.NAVY, 600))
        b.append(S.pill(312, y + 4, 200, 28, risk, fill=fill, color=col, size=15))
        b.append(S.ui("robot" if kind == "machine" else "users", 528, y + 6, 22, S.MUTE))
        b.append(S.text(556, y + 24, kind, 17, S.INK, 500))
    return S.render("nhi_ciem_mock", 640, 164, "".join(b), DIAG)


def agentz_mock():
    """AgentZ sandbox screen, redrawn from the real screen in help docs (agentz slide-03)."""
    b = [S.rect(0, 2, 638, 160, fill=S.NAVY_DK, stroke=S.NAVY_DK, sw=2, r=12),
         S.text(18, 30, "Update sandbox", 18, S.WHITE, 700)]
    steps = ["Identity", "Packages", "MCP", "Skills", "Allowed hosts"]
    for i, st in enumerate(steps):
        cx = 64 + i * 128
        if i < 4:
            b.append(f'<line x1="{cx + 14}" y1="58" x2="{cx + 114}" y2="58" stroke="{S.SECOND}" stroke-width="2"/>')
        b.append(f'<circle cx="{cx}" cy="58" r="12" fill="{S.SECOND if i < 3 else "#2A3470"}"/>')
        b.append(S.text(cx, 92, st, 17, "#D6DBF5", 600, anchor="middle"))
    tools = [("read repo", True), ("push", False), ("delete", False)]
    for i, (tn, on) in enumerate(tools):
        x = 18 + i * 206
        b.append(S.rect(x, 110, 194, 40, fill="#151F5C", stroke="#2A3470", sw=1.5, r=8))
        b.append(S.text(x + 14, 136, tn, 17, S.WHITE, 600))
        tx = x + 140
        b.append(S.rect(tx, 120, 40, 20, fill=S.GREEN if on else "#3A4478", stroke="none", sw=0, r=10))
        b.append(f'<circle cx="{tx + (30 if on else 10)}" cy="130" r="8" fill="{S.WHITE}"/>')
    return S.render("nhi_agentz_mock", 640, 164, "".join(b), DIAG)


# =================================================================== slide parts
def tracker(s, active):
    label(s, LCOL_X, 0.86, 4.0, "NON-HUMAN IDENTITY  ·  %d OF 3" % (active + 1), size=10)
    names = ["Workload", "Service", "Agentic"]
    pw, gap = 1.02, 0.08
    x0 = CX + CW - 3 * pw - 2 * gap
    for i, n in enumerate(names):
        on = i == active
        pill(s, x0 + i * (pw + gap), 0.86, pw, 0.26, n, fill=PRIMARY if on else LAV,
             tcolor=WHITE if on else NAVY, size=10)


def problem_col(s, png, num, num_label, source, owasp):
    label(s, LCOL_X, 1.2, LCOL_W, "WHAT GOES WRONG", size=10, color=RED)
    bottom = diagram(s, png, LCOL_X, 1.48, LCOL_W)
    sy = bottom + 0.14
    box(s, LCOL_X, sy, LCOL_W, 0.92, fill=WHITE, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    box(s, LCOL_X + 0.12, sy + 0.08, 1.35, 0.76, text=num, size=28, color=RED, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    t = box(s, LCOL_X + 1.52, sy + 0.08, LCOL_W - 1.64, 0.76, text=num_label, size=11.5,
            color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    para(t, source, size=9, color=MUTE, space_before=2, space_after=0)
    oy = sy + 1.04
    label(s, LCOL_X, oy, LCOL_W, "OWASP NHI TOP 10 RISKS", size=9.5, color=MUTE)
    x = LCOL_X
    for tag in owasp:
        w = 0.16 + 0.072 * len(tag)
        pill(s, x, oy + 0.28, w, 0.27, tag, fill=RED_LT, tcolor=RED, size=9.5)
        x += w + 0.08


def answer_col(s, rows, top):
    label(s, RCOL_X, 1.2, RCOL_W, "WHAT ACCUKNOX DOES", size=10, color=PRIMARY)
    rh = (4.62 - top) / len(rows)
    for i, (ic, head, sub, status) in enumerate(rows):
        y = top + i * rh
        icon_tile(s, ic, RCOL_X, y + (rh - 0.36) / 2, 0.36,
                  bg=PURPLE if status != "Shipped" else PRIMARY)
        t = box(s, RCOL_X + 0.46, y, RCOL_W - 1.62, rh, text=head, size=11, color=NAVY,
                bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0, mt=0, mb=0)
        para(t, sub, size=10.5, color=MUTE, space_after=0)
        fill, col = STATUS[status]
        pill(s, RCOL_X + RCOL_W - 1.08, y + (rh - 0.26) / 2, 1.08, 0.26, status,
             fill=fill, tcolor=col, size=9.5)


def shot(s, path, y, h, tag=None):
    image_fit(s, path, RCOL_X, y, RCOL_W, h, frame=GREY_BD)
    if tag:
        pill(s, RCOL_X + RCOL_W - 1.3, y + 0.08, 1.2, 0.26, tag, fill=NAVY, tcolor=WHITE, size=9.5)


def new_slide(prs, title, active, notes_text):
    s = prs.slides.add_slide(prs.slide_layouts[4])
    set_title(s, title)
    blank_footer(s)
    tracker(s, active)
    notes(s, notes_text)
    return s


# =================================================================== slides
def build():
    shutil.copy(SRC, OUT)
    prs = Presentation(OUT)
    sl = prs.slides._sldIdLst
    for sid in list(sl):
        try: prs.part.drop_rel(sid.get(qn("r:id")))
        except Exception: pass
        sl.remove(sid)

    # ---------------------------------------------------------- 1. workload
    s = new_slide(prs, "A Stolen Pod Token Should Open Nothing", 0, """
Workload identity is how a pod, container, VM or function proves who it is to the Kubernetes API, the cloud and other services.

The story. Kubernetes mounts a service account token into every pod by default. Many pods never use it, so it sits there as an unused credential. An attacker who lands in one pod reads the token and calls the Kubernetes API as that workload, then moves sideways. Hildegard, BlackT and the BlackCat ransomware used this path. MITRE ATT&CK T1528, Steal Application Access Token. CIS Kubernetes Benchmark v1.27 control 5.1.6.

The number. CyberArk 2025 Identity Security Landscape, a survey of 2,600 security decision-makers: machine identities outnumber human identities 82 to 1.

OWASP NHI Top 10 2025: NHI4 Insecure Authentication, NHI8 Environment Isolation.

What AccuKnox does today.
1. KubeArmor blocks the token path. The policy on the slide is the documented one from help.accuknox.com, use case "Service Account token". The simulation returns Permission denied and raises an alert.
2. Process-level Zero Trust. Process-based network control, process-based asset access and process allowlisting. Policies move to Block once they are stable. Source: use-cases/zero-trust.md, which describes it as patented runtime Zero Trust.
3. KIEM. 15 built-in queries over Kubernetes RBAC, including service accounts not connected to any workload, excessive privileges and roles that can read secrets. Source: use-cases/kiem.md.
4. Preview. SPIFFE IDs attested by the platform (AWS IAM, Azure IAM or the Kubernetes API) and rotated automatically. This is the design in this deck, slides 11 to 13. Today AccuKnox uses SPIFFE and SPIRE to onboard its own agents to the control plane. Do not present customer workload SPIFFE issuance as shipped.

Differentiator. Identity alone says who a workload is. KubeArmor decides what it may do at the kernel, so a stolen but valid token still cannot read what the workload never reads.
""")
    problem_col(s, attack_path("nhi_workload", [
        ("bug", ["Attacker lands", "in one pod"]),
        ("key", ["Reads the service", "account token"]),
        ("server-2", ["Calls the K8s API", "as that workload"])]),
        "82:1", "machine identities for every human identity",
        "CyberArk 2025 Identity Security Landscape",
        ["NHI4 Insecure Auth", "NHI8 Env Isolation"])
    label(s, RCOL_X, 1.2, RCOL_W, "WHAT ACCUKNOX DOES", size=10, color=PRIMARY)
    code_block(s, RCOL_X, 1.48, RCOL_W, 1.22, [
        "file.matchDirectories:",
        "    - dir: /run/secrets/kubernetes.io/serviceaccount/",
        "action: Block",
        ("$ ls  ->  Permission denied, alert raised", True)],
        size=9.5, title="KubeArmorPolicy  ·  real policy from AccuKnox docs")
    answer_col(s, [
        ("shield-lock", "Token theft blocked", "KubeArmor blocks reads of the token", "Shipped"),
        ("lock-access", "Process-level Zero Trust", "Process allowlists for every workload", "Shipped"),
        ("users", "Service account hygiene", "15 KIEM queries flag risky accounts", "Shipped"),
        ("fingerprint", "Attested workload identity", "Platform-proven SPIFFE IDs that rotate", "Preview")],
        top=2.8)
    callout(s, CX, 4.72, CW, 0.44, "shield-check",
            "Identity says who a workload is. KubeArmor decides what it may do, so a valid token still hits a wall.",
            size=11.5)

    # ---------------------------------------------------------- 2. service
    s = new_slide(prs, "Find Every Machine Key Before an Attacker Does", 1, """
Service identity covers the credentials that services, scripts and pipelines use to talk to each other: service accounts, API keys, tokens, certificates and cloud IAM roles.

The story. A key gets committed to a repo or baked into a container image. Nobody rotates it, so the leaked copy keeps working. The account behind it holds a broad role, so one key opens the cloud.

The numbers. GitGuardian State of Secrets Sprawl 2025: 23.8 million secrets leaked on public GitHub repositories in 2024, and 70 percent of secrets leaked in 2022 remain active today. 35 percent of customers' private repositories contain plaintext secrets. blog.gitguardian.com/the-state-of-secrets-sprawl-2025

OWASP NHI Top 10 2025: NHI2 Secret Leakage, NHI7 Long-Lived Secrets, NHI5 Overprivileged NHI.

What AccuKnox does.
1. Secret scanning. Hardcoded keys, tokens and passwords in repos, CI/CD, container layers, IaC and serverless code. Ships on 9 CI/CD platforms (support-matrix/cicd-support-matrix.md). Version 3.7 adds a native app for GitHub, GitLab and Bitbucket with line and column for each finding.
2. AccuKnox Secrets Manager. API-compatible with HashiCorp Vault. Machine auth by Kubernetes service account, AppRole or TLS certificate. Database engine for short-lived database credentials, plus PKI, Transit, SSH and TOTP. Three-node HA on Raft, snapshots every 15 minutes, every request in the audit log. Sold standalone, no CNAPP subscription needed. Sources: secrets-manager/overview.md and architecture.md.
3. Coming soon. CIEM lists users, groups and roles across AWS, GCP, Azure and Oracle, classes each one human or machine, shows risk classes such as Privilege Escalation and Credentials Exposure, last-used dates and an access graph. The panel redraws three rows of the CIEM identity list from the current build screenshot in the help docs (ciem-identity-list.png). The help page marks CIEM as coming soon and standalone accounts only. Confirm the release status with product before any external use.

Differentiator. Point tools do one step. AccuKnox finds the leaked key, moves the live one into a vault with short-lived credentials, and maps what each machine identity can reach.
""")
    problem_col(s, attack_path("nhi_service", [
        ("file-code", ["A key lands in", "a repo or image"]),
        ("history", ["The leaked copy", "keeps working"]),
        ("cloud-lock", ["A broad role", "opens the cloud"])]),
        "70%", "of secrets leaked in 2022 still work today",
        "GitGuardian State of Secrets Sprawl 2025",
        ["NHI2 Secret Leakage", "NHI7 Long-Lived", "NHI5 Overprivileged"])
    label(s, RCOL_X, 1.2, RCOL_W, "WHAT ACCUKNOX DOES", size=10, color=PRIMARY)
    diagram(s, ciem_mock(), RCOL_X, 1.48, RCOL_W)
    pill(s, RCOL_X + RCOL_W - 1.32, 1.18, 1.32, 0.26, "CIEM preview", fill=NAVY, tcolor=WHITE, size=9.5)
    answer_col(s, [
        ("search", "Secret scanning", "Repos, CI/CD, images and IaC", "Shipped"),
        ("lock-square", "Secrets Manager", "Vault-compatible, short-lived DB creds", "Shipped"),
        ("fingerprint", "Machine identity inventory", "CIEM ranks each identity by risk", "Coming soon")],
        top=2.8)
    callout(s, CX, 4.72, CW, 0.44, "shield-check",
            "One platform finds the leaked key, vaults the live one and maps what each identity can reach.",
            size=11.5)

    # ---------------------------------------------------------- 3. agentic
    s = new_slide(prs, "AI Agents Get Scoped Access, Never a Raw Key", 2, """
Agentic identity is the identity an AI agent uses when it calls models, MCP servers and tools, often on behalf of a user and through other agents.

The story. An injected prompt in a document or tool response takes over the agent. The agent runs on a shared user or service key, so it carries far more access than the task needs. Every tool it can reach now runs with that full access.

The number. SailPoint 2025 AI agent adoption research: 23 percent of companies say agents were tricked into revealing access credentials, and 80 percent say agents took unintended actions. sailpoint.com/press-releases/sailpoint-ai-agent-adoption-report

OWASP NHI Top 10 2025: NHI9 NHI Reuse, NHI5 Overprivileged NHI, NHI3 Vulnerable Third-Party NHI (MCP servers and connectors).

What AccuKnox does today.
1. AgentZ. Credentials are scoped and injected at run time, so an injection cannot leak what the agent never sees. No standing access to any tool or credential. Source: agentz/index.md.
2. AgentZ sandbox. Each agent runs in a default-deny sandbox enforced at the kernel. The panel redraws the sandbox update screen from the help docs: Identity, Packages, MCP, Skills and Allowed hosts. The read, push and delete toggles illustrate the documented default: mutate, push and delete are denied unless allowed. Every action lands in a replayable trace.
3. Managed agent inventory. Version 3.5 lists Copilot Studio, M365 Agents, Azure AI Foundry, Bedrock AgentCore and Bedrock Agent, with each agent's IAM role and knowledge bases. Shadow AI discovery finds AI agents and MCP servers in VMs and Kubernetes. Sources: getting-started/3.5-release.md, use-cases/shadow-ai-discovery.md.
4. Preview. Caller-chain authorization. SPIFFE identity per agent and OpenFGA rules that look at the user, every upstream agent and the target tool. Example from this deck: the user can write to the repo, but the Coder agent gets read-only access. Design material, slides 8 to 19.

Differentiator. Agents never hold the key, and each tool call is checked against the task, so a hijacked agent finds nothing to steal and nothing extra to run.
""")
    problem_col(s, attack_path("nhi_agentic", [
        ("message-exclamation", ["Injected prompt", "takes the agent"]),
        ("key", ["Agent reuses", "a shared key"]),
        ("plug-connected", ["Every tool runs", "with full access"])]),
        "23%", "saw agents tricked into revealing credentials",
        "SailPoint 2025 AI agent adoption report",
        ["NHI9 NHI Reuse", "NHI5 Overprivileged", "NHI3 Third-Party"])
    label(s, RCOL_X, 1.2, RCOL_W, "WHAT ACCUKNOX DOES", size=10, color=PRIMARY)
    diagram(s, agentz_mock(), RCOL_X, 1.48, RCOL_W)
    pill(s, RCOL_X + RCOL_W - 1.02, 1.18, 1.02, 0.26, "AgentZ", fill=PRIMARY, tcolor=WHITE, size=9.5)
    answer_col(s, [
        ("key-off", "No secret in the agent", "Credentials injected per run, never stored", "Shipped"),
        ("adjustments", "Default-deny sandbox", "Per-tool MCP rules and allowed hosts", "Shipped"),
        ("robot", "Agent inventory", "Managed agents with their IAM roles", "Shipped"),
        ("hierarchy-2", "Caller-chain authorization", "Rights follow every upstream agent", "Preview")],
        top=2.8)
    callout(s, CX, 4.72, CW, 0.44, "shield-check",
            "The agent never holds the key, so a hijacked agent finds nothing to steal.",
            size=11.5)

    prs.save(OUT)
    return OUT


if __name__ == "__main__":
    print(build())
