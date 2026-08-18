"""Rebrand the two Defence Forces briefing decks into AccuKnox house style.

The source decks arrive in a generic navy/gold government palette with
Calibri + Cambria and no logo anywhere. This script keeps every layout,
shape position, and image exactly where it is, and swaps three things:

1. Colors  -> the AccuKnox palette from README.md
2. Fonts   -> Space Grotesk (primary brand face)
3. Logo    -> footer lockup on every slide, plus a large lockup on the cover

It also rewrites em/en dashes, which the repo writing rules ban.

Run:  py -3.11 scripts/brand_defence_decks.py [--dry-run]
"""

import copy
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Pt

REPO = Path(__file__).resolve().parent.parent
LOGO_LIGHT = REPO / "assets" / "logos" / "accuknox-logo-light-bg.png"
LOGO_DARK = REPO / "assets" / "logos" / "accuknox-logo-dark-bg.png"
LOGO_RATIO = 2763 / 653  # width / height of the horizontal lockup

DOWNLOADS = Path.home() / "Downloads"
OUTDIR = REPO / "output"

DECKS = [
    (DOWNLOADS / "AccuKnox_ASPM_Defence_Briefing.pptx",
     OUTDIR / "AccuKnox_ASPM_Defence_Briefing_Branded.pptx"),
    (DOWNLOADS / "AccuKnox_AI_Security_Defence_Blended.pptx",
     OUTDIR / "AccuKnox_AI_Security_Defence_Briefing_Branded.pptx"),
    (DOWNLOADS / "AccuKnox_CNAPP_Executive_Briefing_v2 (1).pptx",
     OUTDIR / "AccuKnox_CNAPP_Executive_Briefing_Branded.pptx"),
]

# ---------------------------------------------------------------- colors

# Source hex -> AccuKnox hex. Applied to shape fills, lines, and text.
COLOR_MAP = {
    # navy family (backgrounds, dark panels, table headers)
    "0B1F3A": "070E36",   # deepest navy, full-bleed slide backgrounds
    "0E2544": "0C1750",
    "112A4C": "11206D",
    "1B3A63": "11206D",   # main dark panel
    "1E3E68": "1B2E8C",   # panel hairline
    # accent blues
    "1F4E79": "0046FF",
    "2E5FA3": "0046FF",
    "5B8DEF": "6464FF",
    # gold -> brand blue (see pick_accent for the on-dark variant)
    "C9A227": "0046FF",
    # status colors
    "8C1C1C": "C80019",
    "1F5D3A": "0B7A42",
    "4B2E83": "4D4DD9",
    "FCEDED": "FCE9EB",
    "EAF5EC": "E7F6EE",
    # neutrals
    "F4F6F9": "F4F6FB",
    "EAEFF6": "EEF0F6",
    "DCE3EE": "D3D9EC",
    # text on dark
    "CADCFC": "C7D2FF",
    "AEC1DE": "AFB9F0",
    "8FA3C4": "8E97D6",
    # body text stays neutral; headings pick up brand navy
    "16202B": "16202B",
    "5B6675": "5B6675",
}

GOLD = "C9A227"
ACCENT_ON_DARK = "6464FF"   # secondary blue reads on #11206D / #070E36
ACCENT_ON_LIGHT = "0046FF"  # primary blue reads on white / #F4F6FB

# Source darks plus their remapped equivalents: shapes are recolored in
# z-order, so a panel may already carry its AccuKnox hex by the time the text
# sitting on top of it asks what background it is on.
DARK_FILLS = {
    "0B1F3A", "0E2544", "112A4C", "1B3A63", "8C1C1C", "1F5D3A", "4B2E83",
    "070E36", "0C1750", "11206D", "C80019", "0B7A42", "4D4DD9",
}

# Brand colors are picked for white paper. On a navy panel the darker ones drop
# below a readable contrast ratio, so text (never fills) swaps to a tint.
ON_DARK_TEXT = {
    "0046FF": "6464FF",
    "11206D": "C7D2FF",
    "0C1750": "FFFFFF",
    "070E36": "FFFFFF",
    "16202B": "FFFFFF",
    "5B6675": "AFB9F0",
    "C80019": "FF5C6E",   # tint of brand red
    "0B7A42": "4FD18B",   # tint of brand green
    "4D4DD9": "9A9AF0",
    "6464FF": "6464FF",   # already the on-dark accent, leave alone
}

FONT_MAP = {"Calibri": "Space Grotesk", "Cambria": "Space Grotesk"}
# Space Grotesk sets wider than Calibri, so pull sizes back a touch to keep
# every existing text box from overflowing its shape.
SIZE_SCALE = 0.93

# ------------------------------------------------------------- dash fixes

# Hand-written replacements where a mechanical rule would read badly.
DASH_OVERRIDES = {
    "CONFIDENTIAL — EXECUTIVE BRIEFING": "CONFIDENTIAL  ·  EXECUTIVE BRIEFING",
    "Six Scanners, Six Reports — Until Now": "Six Scanners Produce Six Reports",
    "Raw CVSS doesn't say what to fix first — teams chase the longest list, not the most dangerous one":
        "Raw CVSS doesn't say what to fix first, so teams chase the longest list rather than the most dangerous one",
    "Most estates run separate tools for code scanning, dependencies, secrets, infrastructure-as-code, containers, and running applications — each producing its own report, its own severity scale, and its own blind spots.":
        "Most estates run separate tools for code scanning, dependencies, secrets, infrastructure-as-code, containers, and running applications, each producing its own report, its own severity scale, and its own blind spots.",
    "Six distinct engines, correlated into a single dashboard, prioritized by combining CVSS severity with EPSS-based exploitability — so remediation effort goes to what is both exploitable and remediable within SLA.":
        "Six distinct engines, correlated into a single dashboard, prioritized by combining CVSS severity with EPSS-based exploitability, so remediation effort goes to what is both exploitable and remediable within SLA.",
    "Full scan history retained — on demand, on schedule, or scripted":
        "Full scan history retained. Run on demand, on schedule, or scripted.",
    "Findings stay local — nothing uploads unless you opt into the platform":
        "Findings stay local. Nothing uploads unless you opt into the platform.",
    "Continuously detects known, unknown, and shadow APIs across Kubernetes, containers, and microservices — from live traffic, not a static contract you maintained by hand.":
        "Continuously detects known, unknown, and shadow APIs across Kubernetes, containers, and microservices, reading live traffic rather than a static contract you maintained by hand.",
    "Analyses traffic behaviour, usage patterns, and anomalies mapped to users, services, and namespaces — visibility into internal east-west flows a WAF never sees.":
        "Analyses traffic behaviour, usage patterns, and anomalies mapped to users, services, and namespaces, giving visibility into internal east-west flows a WAF never sees.",
    "Applies least-privilege access policies via eBPF and service mesh sidecars — no code changes, no refactoring. Blocks unauthorised access and abnormal behaviour with KubeArmor.":
        "Applies least-privilege access policies via eBPF and service mesh sidecars, with no code changes and no refactoring. Blocks unauthorised access and abnormal behaviour with KubeArmor.",
    "API findings correlate with cloud runtime and compliance signals inside the same ASPM dashboard as SAST, DAST, and SCA — shrinking triage time instead of adding a seventh siloed tool.":
        "API findings correlate with cloud runtime and compliance signals inside the same ASPM dashboard as SAST, DAST, and SCA, which shrinks triage time instead of adding a seventh siloed tool.",
    "Severity ratings and CVSS scores linked to the exact affected component — triage starts from the component, not a flat list":
        "Severity ratings and CVSS scores linked to the exact affected component, so triage starts from the component rather than a flat list",
    "Every finding can be exported as a report or raw data, filtered by application, severity, or module — so output stays in the language a development or AppSec team already works in.":
        "Every finding can be exported as a report or raw data, filtered by application, severity, or module, so output stays in the language a development or AppSec team already works in.",
    "The phases are additive. Nothing from an earlier phase is removed as later phases turn on — gating in Phase 3 simply hardens coverage that already works from Phase 1.":
        "The phases are additive. Nothing from an earlier phase is removed as later phases turn on. Gating in Phase 3 simply hardens coverage that already works from Phase 1.",
    "The Defense Forces is adopting AI across mission-critical functions. That adoption creates an attack surface conventional cyber tooling cannot see — models, agents, datasets, and GPU compute need their own discovery, testing, runtime protection, and governance, inside a boundary that never touches the open internet.":
        "The Defense Forces is adopting AI across mission-critical functions. That adoption creates an attack surface conventional cyber tooling cannot see. Models, agents, datasets, and GPU compute need their own discovery, testing, runtime protection, and governance, inside a boundary that never touches the open internet.",
    "Enterprise reality: identity + least privilege + runtime protection is the call of the hour — treat AI agents like privileged identities.":
        "Enterprise reality: identity, least privilege, and runtime protection are the call of the hour. Treat AI agents like privileged identities.",
    "A model pulled from a public repo is executable code — pickle payloads, deserialization exploits, embedded backdoors.":
        "A model pulled from a public repo is executable code: pickle payloads, deserialization exploits, embedded backdoors.",
    "Prevention reduces risk but never removes it — novel attacks and shadow AI on operator endpoints still occur.":
        "Prevention reduces risk but never removes it. Novel attacks and shadow AI on operator endpoints still occur.",
    "A jailbreak unfolds slowly across 5–15 messages — most firewalls only inspect one message at a time and miss the pattern entirely.":
        "A jailbreak unfolds slowly across 5 to 15 messages. Most firewalls inspect one message at a time and miss the pattern entirely.",
    "A jailbreak found against your internal chatbot in Stage II testing doesn't sit in a report — it becomes a live Prompt Firewall rule the same day, and the agent that tried to misuse a tool gets sandboxed at the kernel before the next test cycle.":
        "A jailbreak found against your internal chatbot in Stage II testing doesn't sit in a report. It becomes a live Prompt Firewall rule the same day, and the agent that tried to misuse a tool gets sandboxed at the kernel before the next test cycle.",
    "Inline prompt firewall, response filtering, and kernel-level agent sandboxing through KubeArmor and KnoxClaw — blocking injection and unsafe agent actions at runtime.":
        "Inline prompt firewall, response filtering, and kernel-level agent sandboxing through KubeArmor and KnoxClaw, blocking injection and unsafe agent actions at runtime.",
    "KubeArmor enforces least privilege at the kernel via eBPF/LSM. KnoxClaw constrains what an agent can execute, read, and reach — blocking drift, not just logging it.":
        "KubeArmor enforces least privilege at the kernel via eBPF/LSM. KnoxClaw constrains what an agent can execute, read, and reach, blocking drift rather than just logging it.",
    "Each finding carries the exact prompt, model output, goal attempted, and detector verdict — mapped to the compliance framework it exercises.":
        "Each finding carries the exact prompt, model output, goal attempted, and detector verdict, mapped to the compliance framework it exercises.",
    "Agentic AI Security sandboxes every connected agent at runtime with eBPF and LSM — no code changes needed.":
        "Agentic AI Security sandboxes every connected agent at runtime with eBPF and LSM. No code changes needed.",
    "Every prompt firewall request and response is recorded with full conversation history, per-policy risk scores, and a block/monitor/pass status — a continuous, immutable record inside the boundary for investigation, forensics, and audit.":
        "Every prompt firewall request and response is recorded with full conversation history, per-policy risk scores, and a block/monitor/pass status, a continuous immutable record inside the boundary for investigation, forensics, and audit.",
    "SAST — Static Code Analysis": "SAST: Static Code Analysis",
    "DAST — Runtime Application Testing": "DAST: Runtime Application Testing",
    "Defending the AI Attack Surface — Discover & Test":
        "Defending the AI Attack Surface: Discover & Test",
    "Defending the AI Attack Surface — Protect & Govern":
        "Defending the AI Attack Surface: Protect & Govern",
    "Zero Trust AI Security — Build to Runtime":
        "Zero Trust AI Security from Build to Runtime",
    "Application Security Posture Management — SAST, DAST, SCA, API Security & Supply Chain":
        "Application Security Posture Management: SAST, DAST, SCA, API Security & Supply Chain",
    "Committed credentials — API keys, access tokens, passwords, certificates — across the full git history":
        "Committed credentials (API keys, access tokens, passwords, certificates) across the full git history",
    "Identify coverage gaps — code, dependencies, IaC, secrets, or container images — so first scans target the highest-value surface":
        "Identify coverage gaps in code, dependencies, IaC, secrets, or container images, so first scans target the highest-value surface",
    "Indirect prompt injection — arriving inside a document, tool description, or memory entry — now succeeds with fewer attempts. A policy document doesn't prove a model is safe.":
        "Indirect prompt injection, arriving inside a document, tool description, or memory entry, now succeeds with fewer attempts. A policy document doesn't prove a model is safe.",
    "60–80% of API calls in modern environments are east-west — service-to-service, never touching a perimeter":
        "60 to 80% of API calls in modern environments are east-west: service-to-service, never touching a perimeter",
    "60–80% of API calls in modern environments are east-west, service-to-service traffic that never passes through a perimeter gateway or WAF":
        "60 to 80% of API calls in modern environments are east-west, service-to-service traffic that never passes through a perimeter gateway or WAF",
    "Severity — how bad the vulnerability could be if exploited. The industry-standard scoring most scanners stop at.":
        "Severity: how bad the vulnerability could be if exploited. The industry-standard scoring most scanners stop at.",
    "Exploit Prediction Scoring System — the probability a vulnerability will actually be exploited in the wild in the next 30 days.":
        "Exploit Prediction Scoring System: the probability a vulnerability will actually be exploited in the wild in the next 30 days.",
    "Inference-time risk — exploitation via adversarial prompts":
        "Inference-time risk: exploitation via adversarial prompts",
    "Discovery & Posture — inventory every AI asset, map blast radius":
        "Discovery & Posture: inventory every AI asset, map blast radius",
    "Red Teaming & Runtime Protection — prompt firewall, agent sandbox, AI-BOM":
        "Red Teaming & Runtime Protection: prompt firewall, agent sandbox, AI-BOM",
    "Shadow AI, DevSecOps & Governance — endpoint, pipeline gates, evidence":
        "Shadow AI, DevSecOps & Governance: endpoint, pipeline gates, evidence",
    "Detect misconfigurations — AI-SPM posture baseline":
        "Detect misconfigurations, the AI-SPM posture baseline",
    "AI-BOM in the build pipeline — DevSecOps AI gates":
        "AI-BOM in the build pipeline, as DevSecOps AI gates",
    "Automated red teaming — 1,500+ adversarial probes across prompt injection, jailbreak, hallucination, toxicity, and unsafe code, plus static scanning of model artifacts.":
        "Automated red teaming: 1,500+ adversarial probes across prompt injection, jailbreak, hallucination, toxicity, and unsafe code, plus static scanning of model artifacts.",
    "Multi-engine scans — SAST, SCA, secrets, IaC, ML-static, container/SBOM":
        "Multi-engine scans: SAST, SCA, secrets, IaC, ML-static, container/SBOM",
    "SQL injection, XSS, insecure deserialization, command injection, path traversal, broken auth, hardcoded crypto — mapped to CWE and OWASP Top 10":
        "SQL injection, XSS, insecure deserialization, command injection, path traversal, broken auth, hardcoded crypto, all mapped to CWE and OWASP Top 10",
    "Runtime web-application issues that only appear once the app is live — XSS, SQLi, CORS misconfiguration, missing security headers":
        "Runtime web-application issues that only appear once the app is live: XSS, SQLi, CORS misconfiguration, missing security headers",
    "XSS, SQL injection, CORS misconfiguration, file inclusion, missing security headers — issues that only appear once the app is live.":
        "XSS, SQL injection, CORS misconfiguration, file inclusion, missing security headers, all of which only appear once the app is live.",
    "A single CLI binary and console drive every scan type — from the first line of code to the running container":
        "A single CLI binary and console drive every scan type, from the first line of code to the running container",
    "Two developer-facing ways to run every scan — the command line, and the editor itself":
        "Two developer-facing ways to run every scan: the command line, and the editor itself",
    "VS Code, Cursor, and IntelliJ — findings before commit":
        "VS Code, Cursor, and IntelliJ. Findings before commit.",
    "Not just another scan output — a complete, versioned inventory in the CycloneDX standard":
        "A complete, versioned inventory in the CycloneDX standard",
    "On-premises model servers — vLLM, NVIDIA Triton, Hugging Face":
        "On-premises model servers: vLLM, NVIDIA Triton, Hugging Face",
    "Built on KubeArmor — CNCF project, 2M+ downloads":
        "Built on KubeArmor, a CNCF project with 2M+ downloads",
    "Discover, test, protect, govern — from one console":
        "Discover, test, protect, and govern from one console",
    "Contract from NSF / SRI / US Army — Under Secretary of Defense for 5G security R&D.":
        "Contract from NSF / SRI / US Army, Under Secretary of Defense, for 5G security R&D.",
    "Contract for Zero Trust Space Satellite Security — the same kernel-level engine, extended to space-edge computing.":
        "Contract for Zero Trust Space Satellite Security. The same kernel-level engine, extended to space-edge computing.",
    "Confirm engagement parameters — Defense Forces & AccuKnox SE":
        "Confirm engagement parameters with the Defense Forces & AccuKnox SE",
    "Stage I begins — discovery and posture baseline":
        "Stage I begins with the discovery and posture baseline",
    "Stateful Prompt Firewall + Agentic AI Security — this is not hypothetical":
        "Stateful Prompt Firewall + Agentic AI Security. This is not hypothetical.",
    "Models running on VMs, and chatbots serving internal users — both are live attack surface today":
        "Models running on VMs, and chatbots serving internal users. Both are live attack surface today.",
    "Models on VMs and internal chatbots are running today — governed or not":
        "Models on VMs and internal chatbots are running today, governed or not",
    "A weakness discovered in testing becomes an enforced runtime policy — no separate tool, no manual handoff":
        "A weakness discovered in testing becomes an enforced runtime policy. No separate tool, no manual handoff.",
    "24 weeks — a go / no-go gate at the end of each stage":
        "24 weeks, with a go / no-go gate at the end of each stage",
    "Asset discovery, risk scoring, and shadow AI surfacing — including models running on VMs":
        "Asset discovery, risk scoring, and shadow AI surfacing, including models running on VMs",
    "No live inventory — teams can't answer “which VMs run which models?”":
        "No live inventory. Teams can't answer “which VMs run which models?”",
    "Effort tracks what's exploitable and remediable within SLA — not the longest list":
        "Effort tracks what's exploitable and remediable within SLA, never the longest list",
    "SAST, SCA, Secret, IaC, Container/SBOM, and DAST feed a single ASPM dashboard — one connected picture, not six separate reports":
        "SAST, SCA, Secret, IaC, Container/SBOM, and DAST feed a single ASPM dashboard. One connected picture, six engines.",
    "Runtime enforcement built on CNCF project KubeArmor, using eBPF and LSM — auditable, not a closed black box":
        "Runtime enforcement built on CNCF project KubeArmor, using eBPF and LSM. Auditable, never a closed black box.",
    "The same scans run in the IDE as code is written, on the CLI on demand, and as native CI/CD steps — no engine or format changes":
        "The same scans run in the IDE as code is written, on the CLI on demand, and as native CI/CD steps, with no engine or format changes",
    # ---- CNAPP executive briefing
    "Code, APIs, and AI — from One Platform": "Code, APIs, and AI from One Platform",
    "Operates on-prem with no reliable internet path — most security tools assume cloud connectivity.":
        "Operates on-prem with no reliable internet path, while most security tools assume cloud connectivity.",
    " before the syscall completes — hostile execution is blocked inline, not detected after the fact.":
        " before the syscall completes, so hostile execution is blocked inline rather than detected after the fact.",
    "No mandatory telemetry egress — all data stays inside your perimeter":
        "No mandatory telemetry egress. All data stays inside your perimeter.",
    "AccuKnox India Pvt Ltd — indigenous support mapped to STQC IC3S, CERT-In, MeghRaj, DPDP":
        "AccuKnox India Pvt Ltd provides indigenous support mapped to STQC IC3S, CERT-In, MeghRaj, DPDP",
    "From the compute layer up through Kubernetes, code, APIs, and AI — wrapped in cloud posture, identity, and compliance":
        "From the compute layer up through Kubernetes, code, APIs, and AI, wrapped in cloud posture, identity, and compliance",
    "Layerwise Enforcement — Compute to Code": "Layerwise Enforcement: Compute to Code",
    "Layerwise Enforcement — API to Identity": "Layerwise Enforcement: API to Identity",
    "On VMs and bare metal, KubeArmor observes syscalls through eBPF and enforces through an LSM hook — BPF-LSM on kernel 5.7+, with AppArmor or SELinux fallback. It allowlists process execution, makes sensitive files (keys, audit logs) immutable, and restricts egress to approved destinations. An unapproved process, file write, or connection returns Permission denied before the syscall completes.":
        "On VMs and bare metal, KubeArmor observes syscalls through eBPF and enforces through an LSM hook, using BPF-LSM on kernel 5.7+ with AppArmor or SELinux fallback. It allowlists process execution, makes sensitive files (keys, audit logs) immutable, and restricts egress to approved destinations. An unapproved process, file write, or connection returns Permission denied before the syscall completes.",
    "AccuKnox discovers every endpoint — including shadow and deprecated ones — and enforces against the OWASP API Top 10. It flags and closes missing or broken authorization and blocks excessive data exposure, each tied to the workload and identity behind the endpoint.":
        "AccuKnox discovers every endpoint, including shadow and deprecated ones, and enforces against the OWASP API Top 10. It flags and closes missing or broken authorization and blocks excessive data exposure, each tied to the workload and identity behind the endpoint.",
    "No single control has to be perfect — every layer of the estate has an independent stop":
        "No single control has to be perfect. Every layer of the estate has an independent stop.",
    "Platform Modules — Cloud, Workload & Kubernetes":
        "Platform Modules: Cloud, Workload & Kubernetes",
    "Platform Modules — Application, API & AI Security":
        "Platform Modules: Application, API & AI Security",
    "Continuously scans cloud and sovereign private cloud for misconfiguration, drift, network exposure, and IAM risk against 33+ frameworks. Surfaces issues like a public bucket or an over-wide security group, mapped to the control it violates — results from proven scanners normalized into one dashboard.":
        "Continuously scans cloud and sovereign private cloud for misconfiguration, drift, network exposure, and IAM risk against 33+ frameworks. Surfaces issues like a public bucket or an over-wide security group, mapped to the control it violates, with results from proven scanners normalized into one dashboard.",
    "Finds unused roles, excessive permissions, and shadow privileges across Kubernetes RBAC and cloud IAM, and cuts them to least privilege — so a compromised identity cannot reach beyond its task.":
        "Finds unused roles, excessive permissions, and shadow privileges across Kubernetes RBAC and cloud IAM, and cuts them to least privilege, so a compromised identity cannot reach beyond its task.",
    "Discovers every endpoint, including shadow and deprecated APIs, and flags OWASP API Top 10 risks — broken authorization, excessive data exposure — each tied to the workload and identity behind it.":
        "Discovers every endpoint, including shadow and deprecated APIs, and flags OWASP API Top 10 risks such as broken authorization and excessive data exposure, each tied to the workload and identity behind it.",
    "Discovers every AI asset — models on VMs, MLOps pipelines, agents, and local endpoints (Ollama, vLLM, MCP servers)":
        "Discovers every AI asset: models on VMs, MLOps pipelines, agents, and local endpoints (Ollama, vLLM, MCP servers)",
    "eBPF observes; a Linux Security Module hook decides — before the syscall completes":
        "eBPF observes. A Linux Security Module hook decides before the syscall completes.",
    "CSPM — posture management": "CSPM: posture management",
    "CWPP — workload protection": "CWPP: workload protection",
    "KSPM — Kubernetes posture": "KSPM: Kubernetes posture",
    "KIEM — identity & entitlements": "KIEM: identity & entitlements",
    "CDR — cloud detection & response": "CDR: cloud detection & response",
    "A real, documented attack pattern — and the exact control that stops it":
        "A real, documented attack pattern, and the exact control that stops it",
    "MITRE ATT&CK T1496 — Resource Hijacking": "MITRE ATT&CK T1496: Resource Hijacking",
    "This is a documented pattern across XMRig, Kinsing, Dero, and TNTBotinger campaigns — enforced identically on Kubernetes and on VMs / bare metal via systemd.":
        "This is a documented pattern across XMRig, Kinsing, Dero, and TNTBotinger campaigns, enforced identically on Kubernetes and on VMs / bare metal via systemd.",
    "One hostile binary on a VM, traced step by step — with and without AccuKnox":
        "One hostile binary on a VM, traced step by step, with and without AccuKnox",
    "The control plane runs inside your boundary — no outbound internet dependency, ever":
        "The control plane runs inside your boundary. No outbound internet dependency, ever.",
    "Continuous, framework-mapped evidence — with automated ticketing end to end":
        "Continuous, framework-mapped evidence, with automated ticketing end to end",
    "Ticketing: Jira, ServiceNow, ServiceDesk Plus, FreshService, ConnectWise — with Slack, Teams, email, and PagerDuty notifications, and full two-way sync":
        "Ticketing: Jira, ServiceNow, ServiceDesk Plus, FreshService, ConnectWise, plus Slack, Teams, email, and PagerDuty notifications with full two-way sync",
    "33+ frameworks pre-mapped — one enforced control satisfies its equivalent across every framework":
        "33+ frameworks pre-mapped. One enforced control satisfies its equivalent across every framework.",
    "Prudent — a 200+ cloud account customer — cut audit prep from 60 hours to under 5 hours per quarter with continuous evidence (about 92%).":
        "Prudent, a 200+ cloud account customer, cut audit prep from 60 hours to under 5 hours per quarter with continuous evidence (about 92%).",
    "Full offline deployment with a controlled update channel — data never leaves your boundary.":
        "Full offline deployment with a controlled update channel. Data never leaves your boundary.",
    "KubeArmor and ModelArmor are CNCF open source — no black box in a classified environment.":
        "KubeArmor and ModelArmor are CNCF open source. No black box in a classified environment.",
    "24 weeks — each phase produces a concrete outcome command can verify":
        "24 weeks. Each phase produces a concrete outcome command can verify.",
    "Baseline posture against ISO 27001 & CIS — first evidence pack":
        "Baseline posture against ISO 27001 & CIS, plus a first evidence pack",
    "A priority mission network — visibility and enforcement delivered in weeks, not months.":
        "A priority mission network, with visibility and enforcement delivered in weeks, not months.",
}

DASH_RE = re.compile(r"\s+[—]\s+")


def fix_dashes(text: str) -> str:
    if "—" not in text and "–" not in text:
        return text
    if text in DASH_OVERRIDES:
        return DASH_OVERRIDES[text]
    stripped = text.strip()
    if stripped in DASH_OVERRIDES:
        return text.replace(stripped, DASH_OVERRIDES[stripped])
    out = text
    # numeric / date ranges
    out = re.sub(r"(?<=\d)\s*–\s*(?=\d)", " to ", out)
    out = out.replace("–", ", ")
    # remaining em dashes: comma if the leading clause has none, else a period
    def sub(m):
        head = out[: m.start()]
        return ". " if "," in head.split(".")[-1] else ", "
    while "—" in out:
        m = DASH_RE.search(out) or re.search(r"—", out)
        head, tail = out[: m.start()], out[m.end():]
        joiner = ". " if "," in head.split(". ")[-1] else ", "
        if joiner == ". " and tail:
            tail = tail[0].upper() + tail[1:]
        out = head + joiner + tail
    return out


# ------------------------------------------------------------- helpers

def hexof(color) -> str | None:
    try:
        if color and color.type is not None and str(color.type).startswith("RGB"):
            return str(color.rgb).upper()
    except Exception:
        pass
    return None


def is_dark(hexstr: str) -> bool:
    r, g, b = (int(hexstr[i:i + 2], 16) for i in (0, 2, 4))
    return (0.299 * r + 0.587 * g + 0.114 * b) < 128


def shape_fill_hex(shape) -> str | None:
    try:
        if shape.fill.type == 1:
            return str(shape.fill.fore_color.rgb).upper()
    except Exception:
        pass
    return None


def bbox(shape):
    if None in (shape.left, shape.top, shape.width, shape.height):
        return None
    return (shape.left, shape.top, shape.left + shape.width, shape.top + shape.height)


def on_dark_background(slide, shape) -> bool:
    """True when this shape sits on the slide's dark background or inside a
    dark panel drawn earlier in z-order."""
    box = bbox(shape)
    if box is None:
        return False
    for other in slide.shapes:
        if other is shape:
            break
        obox = bbox(other)
        fill = shape_fill_hex(other)
        if obox is None or fill is None:
            continue
        if fill in DARK_FILLS and (
            obox[0] <= box[0] and obox[1] <= box[1]
            and obox[2] >= box[2] and obox[3] >= box[3]
        ):
            return True
    bg = None
    try:
        if slide.background.fill.type == 1:
            bg = str(slide.background.fill.fore_color.rgb).upper()
    except Exception:
        pass
    return bool(bg and bg in DARK_FILLS)


def remap(hexstr: str) -> str:
    return COLOR_MAP.get(hexstr, hexstr)


def recolor_slide_background(slide):
    try:
        if slide.background.fill.type == 1:
            cur = str(slide.background.fill.fore_color.rgb).upper()
            slide.background.fill.fore_color.rgb = RGBColor.from_string(remap(cur))
    except Exception:
        pass


def restyle_shape(slide, shape, changes):
    dark_bg = on_dark_background(slide, shape)

    # fill
    try:
        if shape.fill.type == 1:
            cur = str(shape.fill.fore_color.rgb).upper()
            new = ACCENT_ON_DARK if (cur == GOLD and dark_bg) else remap(cur)
            if new != cur:
                shape.fill.fore_color.rgb = RGBColor.from_string(new)
    except Exception:
        pass

    # outline
    try:
        if shape.line.fill.type == 1:
            cur = str(shape.line.color.rgb).upper()
            new = ACCENT_ON_DARK if (cur == GOLD and dark_bg) else remap(cur)
            if new != cur:
                shape.line.color.rgb = RGBColor.from_string(new)
    except Exception:
        pass

    if shape.has_table:
        for row in shape.table.rows:
            for cell in row.cells:
                restyle_textframe(cell.text_frame, dark_bg, changes)
        return

    if shape.has_text_frame:
        restyle_textframe(shape.text_frame, dark_bg, changes)


def restyle_textframe(tf, dark_bg, changes):
    for para in tf.paragraphs:
        for run in para.runs:
            new_text = fix_dashes(run.text)
            if new_text != run.text:
                changes.append((run.text, new_text))
                run.text = new_text
            f = run.font
            if f.name in FONT_MAP:
                f.name = FONT_MAP[f.name]
            if f.size is not None:
                f.size = Pt(round(f.size.pt * SIZE_SCALE, 1))
            cur = hexof(f.color)
            if cur:
                new = ACCENT_ON_DARK if (cur == GOLD and dark_bg) else remap(cur)
                if dark_bg and is_dark(new):
                    new = ON_DARK_TEXT.get(new, "FFFFFF")
                if new != cur:
                    f.color.rgb = RGBColor.from_string(new)


def add_logo(slide, path, left, top, height):
    pic = slide.shapes.add_picture(str(path), left, top,
                                   height=height,
                                   width=Emu(int(height * LOGO_RATIO)))
    return pic


def brand_footer(slide, dark_bg):
    """Swap the 'AccuKnox  |  X' footer text for the real lockup."""
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        txt = shape.text_frame.text.strip()
        if not txt.startswith("AccuKnox  |  "):
            continue
        tail = txt.split("|", 1)[1].strip()
        para = shape.text_frame.paragraphs[0]
        for run in para.runs[1:]:
            run._r.getparent().remove(run._r)
        para.runs[0].text = tail
        shape.left = Inches(1.72)
        shape.width = Inches(4.0)
        logo = LOGO_DARK if dark_bg else LOGO_LIGHT
        add_logo(slide, logo, Inches(0.5), Inches(7.22), Inches(0.21))
        return True
    return False


# Spots where the source deck already overflowed its own card. Keyed by
# (slide index, shape name) -> {top, height} in inches.
LAYOUT_FIXES = {
    "AccuKnox_ASPM_Defence_Briefing": {
        # CVSS / EPSS card: the EPSS paragraph ran past the card border
        (7, "Text 3"): {"top": 1.85, "height": 0.45},
        (7, "Text 4"): {"top": 2.32, "height": 0.95},
        (7, "Text 5"): {"top": 3.35, "height": 0.45},
        (7, "Text 6"): {"top": 3.85, "height": 0.9},
    },
}


# Cover eyebrows that just repeat the wordmark once the logo is placed.
DROP_SHAPES = {
    "AccuKnox_CNAPP_Executive_Briefing_v2 (1)": {(0, "Text 6")},
}


def drop_redundant_shapes(stem, idx, slide):
    targets = DROP_SHAPES.get(stem, set())
    for shape in list(slide.shapes):
        if (idx, shape.name) in targets:
            shape._element.getparent().remove(shape._element)


def apply_layout_fixes(stem, idx, slide):
    fixes = LAYOUT_FIXES.get(stem, {})
    for shape in slide.shapes:
        fix = fixes.get((idx, shape.name))
        if not fix:
            continue
        if "top" in fix:
            shape.top = Inches(fix["top"])
        if "height" in fix:
            shape.height = Inches(fix["height"])


def brand(src: Path, dst: Path, dry_run: bool):
    prs = Presentation(str(src))
    changes = []
    for idx, slide in enumerate(prs.slides):
        dark_bg = False
        try:
            dark_bg = str(slide.background.fill.fore_color.rgb).upper() in DARK_FILLS
        except Exception:
            pass
        for shape in list(slide.shapes):
            restyle_shape(slide, shape, changes)
        recolor_slide_background(slide)
        apply_layout_fixes(src.stem, idx, slide)
        drop_redundant_shapes(src.stem, idx, slide)
        brand_footer(slide, dark_bg)
        if idx == 0:
            add_logo(slide, LOGO_DARK, Inches(0.68), Inches(0.5), Inches(0.5))
    if dry_run:
        print(f"--- {src.name}: {len(changes)} text rewrites")
        for old, new in changes:
            print(f"  - {old}\n  + {new}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(dst))
    print(f"wrote {dst}")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    for src, dst in DECKS:
        brand(src, dst, dry)
