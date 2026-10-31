# -*- coding: utf-8 -*-
"""
Diagrams for the AccuKnox Agentic Identity Security deck.
Run before scripts/build_agentic_identity.py.

  py -3.11 scripts/agentic_identity_svg.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _aksvg import *  # noqa

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "agentic_identity", "diagrams")
ORANGE = "#E8A33D"


def node(x, y, w, h, icon, head, sub=None, accent=PRIMARY, fill=WHITE, hsize=22, ssize=18, brand=False):
    out = [rect(x, y, w, h, fill=fill, stroke=accent, sw=2.5, r=14)]
    out.append(logo(icon, x + 16, y + (h - 44) / 2 if not sub else y + 16, 44) if brand
               else ui(icon, x + 16, (y + (h - 44) / 2) if not sub else y + 16, 44, accent))
    if sub:
        out.append(text(x + 72, y + 44, head, hsize, NAVY, 700))
        out.append(text(x + 18, y + 90, sub, ssize, MUTE, 500))
    else:
        out.append(text(x + 72, y + h / 2 + hsize * 0.36, head, hsize, NAVY, 700))
    return "".join(out)


# ------------------------------------------------------------------ 1. hidden boundary
def d_boundary():
    b = []
    xs = [20, 330, 700, 1010]
    labs = [("user", "Human", "Identity"), ("robot", "Agent", "Identity"),
            ("key", "Workload", "Credentials"), ("plug-connected", "MCP", "Tools")]
    for x, (ic, a, c) in zip(xs, labs):
        b.append(rect(x, 30, 250, 120, stroke=NAVY, sw=3))
        b.append(ui(ic, x + 18, 62, 52, PRIMARY))
        b.append(text(x + 84, 82, a, 26, NAVY, 700))
        b.append(text(x + 84, 116, c, 26, NAVY, 700))
    b.append(arrow(272, 90, 326, 90, NAVY, 3))
    b.append(arrow(962, 90, 1006, 90, NAVY, 3))
    b.append(f'<line x1="582" y1="90" x2="696" y2="90" stroke="{ORANGE}" stroke-width="4" stroke-dasharray="12 8"/>')
    b.append(ui("alert-triangle", 615, 20, 50, ORANGE))
    b.append(text(640, 130, "the gap", 19, ORANGE, 700, "middle"))
    b.append(arrow(640, 150, 640, 222, NAVY, 3))
    b.append(rect(80, 228, 1120, 150, fill=LAV, stroke=PRIMARY, sw=3, r=16))
    b.append(text(640, 290, "Never let an agent's claim to act for User A", 34, NAVY, 700, "middle"))
    b.append(text(640, 336, "become the authorization decision.", 34, NAVY, 700, "middle"))
    b.append(text(640, 425, "Verify the identity-to-agent mapping before every sensitive action.", 22, MUTE, 500, "middle"))
    return render("boundary", 1280, 450, "".join(b), OUT)


# ------------------------------------------------------------------ 2. mapping layer
def d_mapping():
    b = []
    # identity sources
    b.append(text(20, 30, "IDENTITY SOURCES", 19, MUTE, 700))
    srcs = [("user", "Human identity", "Employee, customer", PRIMARY),
            ("robot", "Agent identity", "AI agent, sub-agent", SECOND),
            ("settings", "Service account", "App or workload", GREEN_DK),
            ("users", "Delegated identity", "On behalf of, temporary", ORANGE)]
    for i, (ic, h, s, c) in enumerate(srcs):
        y = 48 + i * 112
        b.append(rect(20, y, 330, 96, stroke=c, sw=2.5))
        b.append(ui(ic, 36, y + 24, 46, c))
        b.append(text(96, y + 42, h, 22, NAVY, 700))
        b.append(text(96, y + 72, s, 18, MUTE, 500))
        b.append(arrow(352, y + 48, 452, 268, c, 2.5))
    # center
    b.append(rect(458, 150, 370, 240, fill=NAVY, stroke=NAVY, r=18))
    b.append(ui("fingerprint", 618, 166, 50, WHITE))
    b.append(text(643, 252, "Identity-to-Agent", 27, WHITE, 700, "middle"))
    b.append(text(643, 284, "Mapping Layer", 27, WHITE, 700, "middle"))
    for i, p in enumerate(["Identity binding", "Delegation", "Policy context", "Audit trail"]):
        px = 476 + (i % 2) * 172
        py = 306 + (i // 2) * 40
        b.append(pill(px, py, 162, 32, p, fill="#2A3A8C", color=WHITE, size=17))
    # attack surfaces on top
    b.append(rect(458, 18, 370, 106, fill=RED_LT, stroke=RED, sw=2))
    b.append(ui("alert-triangle", 474, 32, 34, RED))
    b.append(text(518, 56, "Attack surfaces", 21, RED, 700))
    b.append(text(474, 88, ["Identity confusion, privilege inheritance,", "delegation abuse, stale authorization"], 17, INK, 500))
    b.append(arrow(643, 124, 643, 146, RED, 2.5))
    # bottom delegation
    b.append(rect(458, 418, 370, 74, fill=WHITE, stroke=PRIMARY, sw=2))
    b.append(ui("key", 472, 436, 38, PRIMARY))
    b.append(text(520, 448, "Delegation and credentials", 20, NAVY, 700))
    b.append(text(520, 476, "Short-lived, scoped, never implicit", 17, MUTE, 500))
    b.append(arrow(643, 416, 643, 394, PRIMARY, 2.5))
    # right side
    b.append(arrow(830, 230, 900, 120, PURPLE, 2.5))
    b.append(rect(904, 40, 356, 160, stroke=PURPLE, sw=2.5))
    b.append(ui("scale", 920, 56, 42, PURPLE))
    b.append(text(974, 86, "Policy engine", 23, NAVY, 700))
    b.append(text(922, 128, ["Can this identity and this agent", "act on this resource, now?"], 18, MUTE, 500))
    b.append(text(922, 186, "RBAC, ABAC, per-action checks", 17, PURPLE, 700))
    b.append(arrow(830, 310, 900, 330, GREEN_DK, 2.5))
    b.append(rect(904, 240, 356, 160, stroke=GREEN_DK, sw=2.5))
    b.append(ui("plug-connected", 920, 256, 42, GREEN_DK))
    b.append(text(974, 286, "Tools, APIs, data", 23, NAVY, 700))
    b.append(text(922, 328, ["MCP servers, SaaS, databases,", "internal services"], 18, MUTE, 500))
    b.append(text(922, 386, "Allowlists, resource ACLs", 17, GREEN_DK, 700))
    b.append(rect(904, 424, 356, 68, fill=GREEN_LT, stroke=GREEN, sw=2))
    b.append(ui("shield-check", 918, 438, 40, GREEN_DK))
    b.append(text(970, 466, "Trusted AI actions", 22, GREEN_DK, 700))
    return render("mapping", 1280, 510, "".join(b), OUT)


# ------------------------------------------------------------------ 3. blast radius
def d_blast():
    b = []
    b.append(f'<circle cx="330" cy="250" r="215" fill="{RED_LT}" stroke="{RED}" stroke-width="3"/>')
    b.append(ui("key", 300, 110, 60, RED))
    b.append(text(330, 222, "Long-lived API key", 30, RED, 700, "middle"))
    b.append(text(330, 262, "Works for months or years", 22, INK, 600, "middle"))
    b.append(text(330, 300, ["No identity context", "No trace to one actor"], 20, MUTE, 500, "middle"))
    b.append(text(330, 412, "blast radius", 19, RED, 700, "middle"))
    b.append(f'<circle cx="930" cy="250" r="62" fill="{GREEN_LT}" stroke="{GREEN}" stroke-width="3"/>')
    b.append(ui("clock-hour-4", 906, 226, 48, GREEN_DK))
    b.append(text(930, 360, "SPIFFE SVID or single-hop JWT", 26, GREEN_DK, 700, "middle"))
    b.append(text(930, 398, "Lives for minutes, rotates on its own", 21, INK, 600, "middle"))
    b.append(text(930, 432, "Issued at connect time, bound to one workload", 19, MUTE, 500, "middle"))
    b.append(arrow(570, 250, 850, 250, PRIMARY, 4))
    b.append(text(710, 232, "AccuKnox", 21, PRIMARY, 700, "middle"))
    return render("blast", 1280, 470, "".join(b), OUT)


# ------------------------------------------------------------------ 4. control plane
def d_control():
    b = []
    cx, cy = 640, 255
    b.append(rect(cx - 150, cy - 95, 300, 190, fill=NAVY, stroke=NAVY, r=20))
    b.append(ui("shield-lock", cx - 28, cy - 80, 56, WHITE))
    b.append(text(cx, cy + 10, "AccuKnox", 26, "#B8C4E8", 600, "middle"))
    b.append(text(cx, cy + 44, "AgentZ Control Plane", 28, WHITE, 700, "middle"))
    b.append(text(cx, cy + 76, "one policy for every agent", 17, "#B8C4E8", 500, "middle"))
    spokes = [
        (cx - 210, 20, "fingerprint", "Identity and attestation", "SPIFFE IDs, ModelKnox", PRIMARY, (cx, cy - 95), (cx, 118)),
        (cx - 210, 400, "users", "Delegation and policy", "OpenFGA, RFC 8693 chains", PURPLE, (cx, cy + 95), (cx, 398)),
        (20, 165, "shield-check", "Execution guardrails", "KubeArmor, Prompt Firewall", GREEN_DK, (cx - 150, cy), (440, cy)),
        (840, 165, "key", "Credential broker", "Ephemeral, scoped access", RED, (cx + 150, cy), (840, cy)),
    ]
    for x, y, ic, h, s, c, p1, p2 in spokes:
        b.append(rect(x, y, 420, 96, stroke=c, sw=2.5))
        b.append(f'<circle cx="{x+46}" cy="{y+48}" r="30" fill="{LAV}"/>')
        b.append(ui(ic, x + 24, y + 26, 44, c))
        b.append(text(x + 92, y + 42, h, 23, NAVY, 700))
        b.append(text(x + 92, y + 74, s, 19, MUTE, 500))
        b.append(arrow(p1[0], p1[1], p2[0], p2[1], c, 3, both=True))
    return render("control_plane", 1280, 510, "".join(b), OUT)


# ------------------------------------------------------------------ 5. reference architecture
def d_refarch():
    b = []
    cols = [(20, "users", "People, apps", ["Users, services,", "schedulers"], PRIMARY),
            (300, "robot", "AI agents", ["Agents, sub-agents,", "copilots"], SECOND),
            (980, "database", "Tools, data", ["MCP servers, APIs,", "SaaS, databases"], GREEN_DK)]
    cols = [(20,) + cols[0][1:], (268,) + cols[1][1:], (1030,) + cols[2][1:]]
    for x, ic, h, s, c in cols:
        b.append(rect(x, 40, 230, 170, stroke=c, sw=2.5))
        b.append(ui(ic, x + 18, 58, 46, c))
        b.append(text(x + 74, 90, h, 22, NAVY, 700))
        b.append(text(x + 18, 150, s, 19, MUTE, 500))
    b.append(arrow(252, 125, 264, 125, NAVY, 3))
    b.append(arrow(500, 125, 526, 125, NAVY, 3))
    b.append(arrow(1004, 125, 1026, 125, NAVY, 3))
    b.append(rect(530, 20, 470, 210, fill=NAVY, stroke=NAVY, r=16))
    b.append(text(765, 54, "AccuKnox Agent Identity Gateway", 20, WHITE, 700, "middle"))
    chips = ["Identity, attestation", "Credential broker", "Delegation", "Policy decision", "Prompt firewall", "MCP gateway"]
    for i, c in enumerate(chips):
        px = 548 + (i % 2) * 220
        py = 74 + (i // 2) * 48
        b.append(pill(px, py, 214, 38, c, fill="#2A3A8C", color=WHITE, size=17))
    below = [(20, "id-badge-2", "Enterprise IdP", ["Okta, Entra ID", "stays the source"], PRIMARY),
             (330, "scale", "Policy and risk", ["Task scopes, risk", "tiers, simulation"], PURPLE),
             (640, "cpu", "Runtime sensor", ["KubeArmor eBPF: process,", "file, network"], GREEN_DK),
             (950, "history", "Audit and AI-SOC", ["Tamper-evident logs", "to SIEM and SOAR"], RED)]
    for x, ic, h, s, c in below:
        b.append(rect(x, 300, 300, 150, stroke=c, sw=2.5))
        b.append(ui(ic, x + 16, 316, 42, c))
        b.append(text(x + 70, 346, h, 22, NAVY, 700))
        b.append(text(x + 18, 400, s, 18, MUTE, 500))
        b.append(f'<line x1="{x+150}" y1="298" x2="{min(max(x+150,560),970)}" y2="234" stroke="{c}" stroke-width="2.5" stroke-dasharray="7 6"/>')
    return render("refarch", 1280, 470, "".join(b), OUT)


# ------------------------------------------------------------------ 6. mesh stack
def d_mesh():
    b = []
    layers = [("4", "Enterprise identity", "Keycloak or internal OIDC plus Entra ID for the cloud domain", "id-badge-2", PRIMARY),
              ("3", "Translation and control", "MCP gateway routes auth and mints a single-hop JWT per call", "arrows-exchange", PURPLE),
              ("2", "Ambient service mesh", "Every hop authenticated with mTLS, no sidecar per pod", "topology-star-3", GREEN_DK),
              ("1", "Workload identity anchor", "SPIRE server issues the SVID every layer above trusts", "fingerprint", RED)]
    for i, (n, h, s, ic, c) in enumerate(layers):
        y = 20 + i * 118
        ind = (3 - i) * 26
        b.append(rect(20 + ind, y, 1240 - 2 * ind, 100, fill=WHITE, stroke=c, sw=3, r=16))
        b.append(badge(70 + ind, y + 50, n, r=24, fill=c, size=24))
        b.append(ui(ic, 112 + ind, y + 28, 44, c))
        b.append(text(172 + ind, y + 44, f"Layer {n}  ·  {h}", 24, NAVY, 700))
        b.append(text(172 + ind, y + 78, s, 20, MUTE, 500))
    return render("mesh", 1280, 490, "".join(b), OUT)


# ------------------------------------------------------------------ 7. five-step blueprint
def d_blueprint():
    b = []
    steps = [("Connect", "device-desktop", "Enterprise client", ["Signs in once at", "connect time"], NAVY),
             ("Invoke", "robot", "Autonomous agent", ["Tries to call", "a tool"], SECOND),
             ("Exchange", "arrows-exchange", "Token service", ["Swaps the token for", "an OBO token"], PURPLE),
             ("Authorize", "scale", "Policy check", ["Checks the actor", "chain per call"], PRIMARY),
             ("Execute", "server-2", "MCP server", ["Gets a scoped,", "audited token"], GREEN_DK)]
    b.append(rect(262, 16, 1000, 404, fill="none", stroke=GREY_BD, sw=2, r=18, dash="10 7"))
    b.append(text(282, 46, "Trust domain and security perimeter", 18, MUTE, 700))
    for i, (h, ic, t, s, c) in enumerate(steps):
        x = 20 + i * 252
        b.append(badge(x + 26, 100, i + 1, r=22, fill=c, size=22))
        b.append(text(x + 58, 109, h, 27, NAVY, 700))
        b.append(rect(x, 140, 210, 260, stroke=c, sw=2.5))
        b.append(f'<circle cx="{x+105}" cy="{210}" r="46" fill="{LAV}"/>')
        b.append(ui(ic, x + 75, 180, 60, c))
        b.append(text(x + 105, 296, t, 21, NAVY, 700, "middle"))
        b.append(text(x + 105, 334, s, 18, MUTE, 500, "middle"))
        if i < 4:
            b.append(arrow(x + 212, 270, x + 248, 270, c, 4))
    return render("blueprint", 1280, 430, "".join(b), OUT)


# ------------------------------------------------------------------ 8. OBO token exchange
def d_obo():
    b = []
    b.append(rect(20, 30, 200, 250, stroke=NAVY, sw=2.5))
    b.append(ui("user", 40, 50, 44, PRIMARY)); b.append(text(94, 80, "Developer", 20, NAVY, 700))
    b.append(ui("app-window", 40, 120, 44, PRIMARY)); b.append(text(94, 150, "MCP client", 20, NAVY, 700))
    b.append(text(40, 220, ["1. User and", "client"], 18, MUTE, 700))
    b.append(rect(290, 30, 250, 250, stroke=PRIMARY, sw=2.5))
    b.append(logo("si-microsoftazure", 306, 46, 40, PRIMARY))
    b.append(text(358, 74, "Entra ID", 22, NAVY, 700))
    b.append(text(308, 120, ["OIDC sign-in", "OAuth 2.1 and PKCE", "Scopes and claims", "Signing keys, JWKS"], 18, MUTE, 500))
    b.append(text(308, 262, "2. Identity provider", 18, MUTE, 700))
    b.append(arrow(222, 90, 286, 90, NAVY, 2.5)); b.append(text(254, 80, "1", 17, NAVY, 700, "middle"))
    b.append(arrow(286, 150, 224, 150, NAVY, 2.5)); b.append(text(254, 140, "2", 17, NAVY, 700, "middle"))
    b.append(rect(600, 16, 400, 280, fill=GREEN_LT, stroke=GREEN, sw=2.5, dash="10 6"))
    b.append(text(800, 48, "3. AccuKnox Agent Gateway", 21, GREEN_DK, 700, "middle"))
    b.append(rect(616, 66, 176, 210, stroke=PRIMARY, sw=2))
    b.append(text(704, 96, "Inbound", 20, PRIMARY, 700, "middle"))
    b.append(text(632, 130, ["Checks JWT:", "signature, issuer,", "audience, expiry,", "scope"], 17, INK, 500))
    b.append(rect(808, 66, 176, 210, stroke=GREEN_DK, sw=2))
    b.append(text(896, 96, "Outbound", 20, GREEN_DK, 700, "middle"))
    b.append(ui("arrows-exchange", 872, 112, 48, GREEN_DK))
    b.append(text(824, 196, ["Swaps it for an", "OBO token", "(RFC 8693)"], 17, INK, 500))
    b.append(arrow(542, 210, 596, 210, NAVY, 2.5)); b.append(text(569, 200, "3", 17, NAVY, 700, "middle"))
    b.append(rect(1060, 30, 200, 110, stroke=PURPLE, sw=2.5))
    b.append(ui("topology-star-3", 1076, 46, 40, PURPLE)); b.append(text(1126, 74, "Planner", 20, NAVY, 700))
    b.append(text(1078, 120, "agent broker", 18, MUTE, 600))
    b.append(rect(1060, 176, 200, 110, stroke=GREEN_DK, sw=2.5))
    b.append(ui("server-2", 1076, 192, 40, GREEN_DK)); b.append(text(1126, 220, "MCP server", 20, NAVY, 700))
    b.append(text(1078, 266, "4. Protected", 18, MUTE, 600))
    b.append(arrow(1002, 90, 1056, 90, PURPLE, 2.5)); b.append(arrow(1160, 142, 1160, 172, GREEN_DK, 2.5))
    # tokens
    b.append(rect(20, 330, 520, 130, fill=LAV, stroke=PURPLE, sw=2))
    b.append(text(40, 364, "Broker JWT, stays at the gateway", 21, PURPLE, 700))
    b.append(text(40, 400, ["Audience: planning-agent-broker", "Scope: invoke the broker. Subject: user"], 18, INK, 500))
    b.append(arrow(544, 395, 736, 395, GREEN_DK, 3)); b.append(text(640, 382, "token exchange", 17, GREEN_DK, 700, "middle"))
    b.append(rect(740, 330, 520, 130, fill=GREEN_LT, stroke=GREEN_DK, sw=2))
    b.append(text(760, 364, "Delegated JWT, sent to the MCP server", 21, GREEN_DK, 700))
    b.append(text(760, 400, ["Audience: MCPServer. Scope: invoke", "Subject: original user. Client: OBO"], 18, INK, 500))
    b.append(ui("alert-triangle", 330, 476, 34, RED))
    b.append(text(374, 502, "Never forward the broker JWT downstream.", 22, RED, 700))
    return render("obo", 1280, 520, "".join(b), OUT)


# ------------------------------------------------------------------ 9. caller chain
def d_chain():
    b = []
    parts = [("user", "Principal", "the user it acts for", PRIMARY),
             ("route", "Caller chain", "every agent it passed", PURPLE),
             ("server-2", "Target", "the MCP server or tool", GREEN_DK)]
    for i, (ic, h, s, c) in enumerate(parts):
        x = 20 + i * 330
        b.append(rect(x, 20, 270, 110, stroke=c, sw=2.5))
        b.append(ui(ic, x + 16, 36, 40, c))
        b.append(text(x + 66, 64, h, 23, NAVY, 700))
        b.append(text(x + 18, 108, s, 18, MUTE, 500))
        if i < 2:
            b.append(text(x + 300, 88, "+", 40, NAVY, 700, "middle"))
    b.append(text(1000, 88, "=", 40, NAVY, 700, "middle"))
    b.append(rect(1030, 20, 230, 110, fill=NAVY, stroke=NAVY))
    b.append(ui("scale", 1046, 36, 40, WHITE))
    b.append(text(1096, 64, "Authz", 23, WHITE, 700))
    b.append(text(1048, 108, "decision", 20, "#B8C4E8", 600))
    # example
    b.append(text(20, 186, "EXAMPLE: THE SAME USER, TWO AGENT PATHS", 18, MUTE, 700))
    rows = [("Coder agent", "GitHub MCP", "Read all repos", "Agent gets less than the user", PRIMARY),
            ("Remediation then Coder", "GitHub MCP", "Read repos, write PRs", "Scope narrows at each hop", PURPLE),
            ("Remediation then Security", "ServiceNow MCP", "Read and write tickets", "New path, new rights", GREEN_DK)]
    for i, (a, t, p, n, c) in enumerate(rows):
        y = 204 + i * 84
        b.append(rect(20, y, 1240, 72, stroke=GREY_BD, sw=1.5, r=12))
        b.append(ui("user", 36, y + 18, 36, NAVY)); b.append(text(80, y + 44, "User-1", 20, NAVY, 700))
        b.append(arrow(158, y + 36, 194, y + 36, c, 2.5))
        b.append(ui("robot", 202, y + 18, 36, c)); b.append(text(246, y + 44, a, 20, NAVY, 700))
        b.append(arrow(530, y + 36, 566, y + 36, c, 2.5))
        b.append(ui("server-2", 574, y + 18, 36, GREEN_DK)); b.append(text(618, y + 44, t, 20, NAVY, 700))
        b.append(pill(800, y + 17, 200, 38, p, fill=LAV, color=NAVY, size=17))
        b.append(text(1012, y + 44, n, 17, MUTE, 600))
    return render("chain", 1280, 460, "".join(b), OUT)


if __name__ == "__main__":
    for f in (d_boundary, d_mapping, d_blast, d_control, d_refarch, d_mesh, d_blueprint, d_obo, d_chain):
        print(f())
