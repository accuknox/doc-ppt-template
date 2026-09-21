"""Build two AccuKnox AI security comparison briefs as branded A4 PDFs.

  AccuKnox vs. TrendAI Security
  AccuKnox vs. Harmonic Security (AI Security)

Each brief runs three pages at most: a summary with the scorecard, then the
capability matrix, then the closing argument. Every cell carries a status, one
line of evidence and a link to the vendor's own published page. The scorecard is
counted from the rows, so the two can never disagree.

Research lives in the HelpDocs repo:
  references/comparisons-builder/harmonic/evidence-log.md
  references/comparisons-builder/trendai/evidence-log.md

Flat colors only, no gradients. Emits HTML with the logos inlined, then prints
to PDF with headless Edge.
"""
import base64
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(REPO, "output", "comparisons")
OUT = os.path.join(REPO, "output")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

NAVY = "#11206D"
BLUE = "#0046FF"
SEC = "#6464FF"
RED = "#C80019"
GREEN = "#16A55C"
MUTE = "#6A749A"
INK = "#1A1D2E"
GREY_BG = "#EEF0F6"
GREY_BD = "#C4CCDE"
TINT = "#F7F9FF"


def uri(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


LOGO_DARK = uri(os.path.join(REPO, "assets", "logos", "accuknox-logo-dark-bg.png"))

READ_ON = "11 September 2026"

# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------
H = "https://help.accuknox.com/"
AK = {
    "arch": ("help.accuknox.com · AI security architecture", H + "getting-started/ai-security-arch/"),
    "rt": ("help.accuknox.com · Runtime security architecture", H + "getting-started/runtime-sec-arch/"),
    "shadow": ("help.accuknox.com · Shadow AI discovery", H + "use-cases/shadow-ai-discovery/"),
    "aidr": ("help.accuknox.com · AI-DR", H + "use-cases/aidr/"),
    "intmx": ("help.accuknox.com · Integration support matrix", H + "integrations/support-matrix/"),
    "agentz": ("help.accuknox.com · AgentZ", H + "agentz/"),
    "mlscan": ("help.accuknox.com · ML model static scans", H + "how-to/ml-static-scan/"),
    "cicd": ("help.accuknox.com · Model scan in CI/CD", H + "how-to/model-scan-cicd/"),
    "redteam": ("help.accuknox.com · AI red teaming", H + "use-cases/red-teaming/"),
    "uc": ("help.accuknox.com · AI security use cases", H + "use-cases/aiml-usecases/"),
    "pf": ("help.accuknox.com · Prompt Firewall", H + "use-cases/prompt-firewall-overview/"),
    "aiint": ("help.accuknox.com · AI integrations", H + "integrations/ai-overview/"),
    "onprem": ("help.accuknox.com · SaaS vs on-prem", H + "how-to/aiml-saas-vs-onprem/"),
    "v36": ("help.accuknox.com · v3.6 release notes", H + "getting-started/3.6-release/"),
    "oss": ("help.accuknox.com · Open source", H + "getting-started/open-source/"),
    "faq": ("help.accuknox.com · General FAQ", H + "faqs/general/"),
}

HS = "https://www.harmonic.security/"
HD = "https://docs.harmonicsecurity.app/"
HM = {
    "diff": ("harmonic.security · How Harmonic is different", HS + "the-harmonic-difference"),
    "endpoint": ("harmonic.security · Endpoint AI security", HS + "solutions/endpoint-ai-security"),
    "pricing": ("harmonic.security · Pricing and packages", HS + "pricing"),
    "command": ("harmonic.security · Harmonic Command", HS + "products/command"),
    "explore": ("harmonic.security · Harmonic Explore", HS + "products/explore"),
    "riskrubric": ("harmonic.security · RiskRubric launch", HS + "resources/introducing-riskrubric-a-new-standard-for-evaluating-ai-model-safety"),
    "trust": ("trust.harmonic.security · Trust center", "https://trust.harmonic.security/"),
    "rn0610": ("Harmonic docs · Release note, 10 June 2026", HD + "release-notes/2026/june-10-2026"),
    "rn0813": ("Harmonic docs · Release note, 13 August 2026", HD + "release-notes/2026/august-13-2026"),
    "webhook": ("Harmonic docs · Configure a webhook", HD + "portal-guides/integration-guides/configure-a-webhook"),
    "mcpacl": ("Harmonic docs · MCP access controls", HD + "portal-guides/managing-your-organization/configure-mcp-server-access-controls"),
    "mcp": ("Harmonic docs · MCP Gateway", HD + "mcp-gateway"),
    "risk": ("Harmonic docs · Risk scoring framework", HD + "portal-guides/applications/application-risk-scoring-framework"),
    "agent": ("Harmonic docs · Protect Agent", HD + "protect-agent"),
}

TS = "https://www.trendaisecurity.com/en/"
TD = "https://docs.trendmicro.com/en-us/documentation/article/"
TR = {
    "aispm": ("docs.trendmicro.com · AI-SPM", TD + "trend-vision-one-__ai-spm-2"),
    "aias": ("docs.trendmicro.com · AI Application Security", TD + "trend-vision-one-ai-scanner-ai-guard"),
    "guard": ("docs.trendmicro.com · Integrate AI Guard", TD + "trend-vision-one-integrate-ai-guard"),
    "tmas": ("docs.trendmicro.com · Artifact Scanner with AI Scanner", TD + "trend-vision-one-tmas-ai-scanner"),
    "cs": ("trendaisecurity.com · Cloud security", TS + "platform/cloud-security"),
    "ai": ("trendaisecurity.com · AI security", TS + "platform/proactive-ai-security"),
    "ident": ("trendaisecurity.com · Identity security", TS + "platform/identity-security"),
    "deploy": ("trendaisecurity.com · Deployment options", TS + "platform/deployment-options"),
    "platform": ("trendaisecurity.com · Platform", TS + "platform"),
    "ka": ("success.trendmicro.com · Container Security policies", "https://success.trendmicro.com/en-US/solution/KA-0016974"),
    "openshell": ("newsroom.trendmicro.com · 16 March 2026 release", "https://newsroom.trendmicro.com/2026-03-16-TrendAI-TM-to-Secure-Enterprise-Adoption-of-Agentic-AI-with-NVIDIA"),
}

# --------------------------------------------------------------------------
# briefs. A row is (parameter, accuknox cell, competitor cell).
# A cell is (state, evidence, [source keys]). States: y, p, n, r.
# --------------------------------------------------------------------------
HARMONIC = {
    "file": "AccuKnox_vs_Harmonic_Security_AI_Security",
    "title": "AccuKnox vs. Harmonic Security",
    "qual": "(AI Security)",
    "vendor": "Harmonic Security",
    "short": "Harmonic",
    "src": HM,
    "summary": [
        "AccuKnox covers 12 of 17 capability rows across the eight AI security modules, and Harmonic Security covers 4.",
        "The AccuKnox lead comes from the AI your teams build and run: models, endpoints, agents and cloud AI services.",
        "Harmonic leads on employee AI use, and its own site says it does not red team homegrown models.",
    ],
    "scope": ("Harmonic places itself in workforce AI governance. This brief scores "
              "both vendors on the eight AccuKnox AI security modules, then adds four "
              "workforce rows where Harmonic leads.", ["diff"]),
    "split": 17,
    "groups": [
        ("AI Security Posture Management (AI-SPM)", "Deploy", [
            ("Cloud AI asset inventory",
             ("y", "An agentless cloud SDK inventories Bedrock, AgentCore, Azure AI Foundry, Copilot Studio and Vertex AI.", ["arch"]),
             ("n", "Publishes no cloud-account connector. The endpoint agent sees device connections to Bedrock and Azure AI Foundry.", ["endpoint"])),
            ("Self-hosted AI on servers and clusters",
             ("y", "A VM scanner and an in-cluster Kubernetes scanner find inference engines, SDKs and MCP servers by package.", ["shadow"]),
             ("p", "The endpoint agent finds locally hosted models such as Ollama on employee devices. No server scanner is documented.", ["endpoint"])),
        ]),
        ("AI Detect and Respond (AI-DR)", "Run", [
            ("Detection from cloud AI service events",
             ("y", "Reads CloudTrail and Event Hub, and flags events such as a Bedrock customization job.", ["aidr"]),
             ("p", "Ingests Claude activity through the Anthropic Compliance API. Publishes no CloudTrail or Event Hub connector.", ["rn0610"])),
            ("Alert routing to SIEM and ticketing",
             ("y", "Sends findings to Splunk, Sentinel and QRadar, and opens Jira or ServiceNow tickets.", ["intmx"]),
             ("y", "Webhooks send new alerts and intervention actions to a SIEM or a ticketing tool.", ["webhook"])),
        ]),
        ("Agentic AI Security", "Run", [
            ("Runtime sandbox for agent workloads",
             ("y", "KubeArmor limits process, file, network and domain access for agents and MCP servers at the kernel.", ["arch", "rt"]),
             ("n", "Publishes no workload runtime control. Its site says it does not secure agents that customers build.", ["diff"])),
            ("MCP server and tool access control",
             ("y", "The AgentZ sandbox starts at default deny, with per-tool toggles for each MCP server.", ["agentz"]),
             ("y", "The MCP Gateway allows or blocks servers, tools, prompts and resources per employee group.", ["mcpacl"])),
            ("Sensitive data inside tool calls",
             ("p", "The sandbox limits what an agent may execute, read and open. The docs show no tool-call content check.", ["arch"]),
             ("y", "The MCP Gateway detects PII, secrets and credentials in tool invocations in real time.", ["mcp"])),
        ]),
        ("AI Model and Dataset Security", "Build", [
            ("Static scan of model files",
             ("y", "Scans Pickle, HDF5, SavedModel, checkpoints and ONNX from GitHub and Hugging Face.", ["mlscan"]),
             ("n", "Publishes no model-file scanner. Its site places model security in a separate market.", ["diff"])),
            ("Model scan gate in CI/CD",
             ("p", "A /scan pull-request comment runs a GitHub Action. Support supplies the action name.", ["cicd"]),
             ("n", "Publishes no CI/CD integration for models. Its tiers list browser, desktop and agent coverage.", ["pricing"])),
        ]),
        ("AI Red Teaming and Pen Testing", "Build", [
            ("Adversarial testing of LLM endpoints",
             ("y", "Runs prompt injection, hallucination and code safety probes against any OpenAI-compatible endpoint.", ["redteam"]),
             ("n", "Its site states that Harmonic does not red team homegrown models.", ["diff"])),
            ("Risk signal on public models",
             ("y", "Static scans pull public models from Hugging Face and check provenance and file safety.", ["mlscan"]),
             ("p", "Co-launched RiskRubric, a public leaderboard of public models. It does not scan a customer copy.", ["riskrubric"])),
        ]),
        ("AI Identity Security", "Govern", [
            ("Identity for AI agents",
             ("r", "The AI Identity Security module is on the roadmap and not in the console today.", ["uc"]),
             ("n", "Its site states that Harmonic does not manage agent credentials.", ["diff"])),
            ("Employee identity on AI activity",
             ("p", "The browser plugin records user identity, timestamp and domain for GenAI access.", ["shadow"]),
             ("y", "Syncs Entra ID, Okta and Google Workspace, and adds identity to every alert.", ["pricing"])),
        ]),
        ("AI Guardrails (Prompt Firewall)", "Run", [
            ("Inline guardrail for apps you build",
             ("y", "A proxy blocks, sanitizes or logs across 14 policy types, through LiteLLM, APIM, API Gateway or an SDK.", ["pf", "aiint"]),
             ("n", "Its site assigns guardrails for apps your engineers ship to a model security vendor.", ["diff"])),
            ("Prompt injection detection",
             ("y", "Prompt Injection is one of the 14 policy types, tracked across conversation turns.", ["pf"]),
             ("r", "The Command tier lists prompt injection detection and blocking as coming soon.", ["pricing"])),
        ]),
        ("AI Compliance and Governance (AI-GRC)", "Govern", [
            ("Governance module in the console",
             ("r", "The AI-GRC module is on the roadmap and not in the console today.", ["uc"]),
             ("p", "Provides audit logs, app tiering and data residency. Regulatory mapping is available on request.", ["command"])),
            ("Framework mapping on AI findings",
             ("y", "Maps AI findings to MITRE ATLAS, OWASP LLM Top 10, NIST AI RMF and AVID.", ["onprem"]),
             ("p", "Names the EU AI Act and GDPR, and supplies control mapping on request.", ["command"])),
        ]),
        ("Workforce GenAI usage", "Where Harmonic leads", [
            ("Browser coverage for employee AI use",
             ("p", "The plugin covers ChatGPT, Claude, Gemini, GitHub Copilot and Microsoft Copilot.", ["v36"]),
             ("y", "The extension covers 1,000+ web AI tools across Chrome, Edge, Firefox, Safari and more.", ["explore"])),
            ("Desktop apps, IDEs and CLI agents",
             ("n", "The browser plugin only sees browser traffic. Desktop prompts need the SDK or a gateway.", ["arch"]),
             ("y", "The Protect Agent adds controls in Claude Code, Codex, Cursor, VS Code and GitHub Copilot CLI.", ["rn0813"])),
            ("Sensitive data blocking in employee prompts",
             ("y", "A prompt that breaks policy is blocked in the page. Uploads are blocked by file type.", ["v36"]),
             ("y", "Small language models warn, nudge or block in under 200 milliseconds.", ["pricing"])),
            ("AI app risk scoring and usage intelligence",
             ("n", "No vendor risk score or use-case classification appears in the AccuKnox docs.", ["shadow"]),
             ("y", "Scores each app on four risk factors and classifies prompts into business use cases.", ["risk"])),
        ]),
    ],
    "fit_ak": [
        ("A platform team ships LLM apps and agents on Kubernetes, Bedrock or Vertex AI.",
         "Model scans, red teaming, the Prompt Firewall and the kernel sandbox cover build through run."),
        ("A regulated team must run AI security on-prem or air-gapped.",
         "AI-SPM on-prem has the same features as SaaS and supports air-gapped installs."),
    ],
    "fit_them": [
        ("A CISO must find and govern employee use of third-party AI tools.",
         "Browser, desktop and CLI coverage, with app risk scores and use-case reports."),
        ("Developers use Claude Code and Cursor with local MCP servers.",
         "The local MCP Gateway and Protect Agent run on Windows, macOS and Linux workstations."),
    ],
    "why": [
        ("Better", "AccuKnox secures the AI your teams build. Harmonic's own site puts that job outside its scope. "
                   "KubeArmor, the enforcement engine, is a CNCF Sandbox project that AccuKnox created.", ["uc", "oss"]),
        ("Faster", "AI-SPM on SaaS deploys within minutes. An on-prem install takes 30 minutes to 4 hours, "
                   "with the same features.", ["onprem"]),
        ("Cheaper", "AccuKnox puts AppSec, CloudSec and AI security in one platform. "
                    "Harmonic publishes three tiers and no list price.", ["faq", "pricing"]),
    ],
    "leads": ("Harmonic leads on employee AI use: browser and desktop coverage, CLI agents, app risk "
              "scores and content checks inside tool calls. Harmonic also holds ISO/IEC 42001:2023.",
              ["trust"]),
}

TRENDAI = {
    "file": "AccuKnox_vs_TrendAI_Security",
    "title": "AccuKnox vs. TrendAI Security",
    "qual": "",
    "vendor": "TrendAI Security",
    "short": "TrendAI",
    "src": TR,
    "summary": [
        "Both platforms cover AI posture, cloud detection, red teaming and prompt guardrails, so the split sits in runtime depth.",
        "AccuKnox blocks a single process, file or network call at the kernel, and TrendAI isolates or terminates the container.",
        "TrendAI leads on breadth, with endpoint, email, network, identity and employee AI controls in one platform.",
    ],
    "scope": ("TrendAI Vision One is a full security platform. This brief scores the "
              "eight AccuKnox AI security modules, then runtime, workforce and "
              "deployment. The last row names TrendAI coverage outside the AccuKnox "
              "platform.", ["platform"]),
    "split": 10,
    "groups": [
        ("AI Security Posture Management (AI-SPM)", "Deploy", [
            ("Cloud AI asset inventory",
             ("y", "An agentless cloud SDK inventories Bedrock, AgentCore, Azure AI Foundry, Copilot Studio and Vertex AI.", ["arch"]),
             ("y", "The AI-SPM tab lists AI services, models, workloads, data storage and entitlements per cloud account.", ["aispm"])),
            ("Self-hosted AI on servers and clusters",
             ("y", "A VM scanner and an in-cluster Kubernetes scanner find inference engines, SDKs and MCP servers by package.", ["shadow"]),
             ("p", "AI-SPM covers AI assets in connected cloud accounts. No on-prem server discovery is documented.", ["aispm"])),
        ]),
        ("AI Detect and Respond (AI-DR)", "Run", [
            ("Detection from cloud AI service events",
             ("y", "Reads CloudTrail and Event Hub, and flags events such as a Bedrock customization job.", ["aidr"]),
             ("y", "XDR for Cloud adds 700-plus detection models and AWS CloudTrail integration.", ["cs"])),
        ]),
        ("Agentic AI Security", "Run", [
            ("Runtime sandbox for agent workloads",
             ("y", "KubeArmor limits process, file, network and domain access for agents and MCP servers at the kernel.", ["arch", "rt"]),
             ("p", "Announced runtime policy for agents on the NVIDIA OpenShell runtime on 16 March 2026.", ["openshell"])),
        ]),
        ("AI Model and Dataset Security", "Build", [
            ("Static scan of model files",
             ("y", "Scans Pickle, HDF5, SavedModel, checkpoints and ONNX from GitHub and Hugging Face.", ["mlscan"]),
             ("n", "Publishes no model-file scanner. AI Scanner tests model behavior through simulated attacks.", ["tmas"])),
        ]),
        ("AI Red Teaming and Pen Testing", "Build", [
            ("Automated adversarial testing",
             ("y", "Runs prompt injection, hallucination and code safety probes against any OpenAI-compatible endpoint.", ["redteam"]),
             ("y", "AI Scanner simulates prompt injection and data exfiltration before release, hosted or self-hosted.", ["aias"])),
        ]),
        ("AI Identity Security", "Govern", [
            ("Identity for AI agents",
             ("r", "The AI Identity Security module is on the roadmap and not in the console today.", ["uc"]),
             ("y", "Identity Security discovers human, non-human and AI agent identities.", ["ident"])),
        ]),
        ("AI Guardrails (Prompt Firewall)", "Run", [
            ("Inline guardrail for apps you build",
             ("y", "A proxy blocks, sanitizes or logs across 14 policy types, tracked across conversation turns.", ["pf"]),
             ("y", "The AI Guard API scans for harmful content, sensitive data and prompt attacks, with a LiteLLM option.", ["guard"])),
        ]),
        ("AI Compliance and Governance (AI-GRC)", "Govern", [
            ("Governance module in the console",
             ("r", "The AI-GRC module is on the roadmap and not in the console today.", ["uc"]),
             ("y", "AI Risk Insights reports AI usage, policy violations and threats for governance.", ["ai"])),
            ("Framework mapping on AI findings",
             ("y", "Maps AI findings to MITRE ATLAS, OWASP LLM Top 10, NIST AI RMF and AVID.", ["onprem"]),
             ("y", "AI Scanner maps risks to the OWASP LLM Top 10 and MITRE ATLAS.", ["tmas"])),
        ]),
        ("Cloud and Kubernetes runtime", "Where AccuKnox leads", [
            ("Response on a running container",
             ("y", "KubeArmor blocks a single process, file or network action through Linux Security Modules.", ["rt"]),
             ("p", "Runtime rules log, isolate or terminate the container. Admission control blocks at deploy time.", ["ka"])),
        ]),
        ("Workforce and platform", "Where TrendAI leads", [
            ("Employee use of GenAI services",
             ("p", "The browser plugin covers five AI platforms. Desktop and terminal prompts need the SDK or a gateway.", ["v36", "arch"]),
             ("y", "AI Secure Access blocks sensitive data to AI services, finds Shadow AI and restricts uploads.", ["ai"])),
            ("Deployment models",
             ("y", "SaaS or on-prem with the same features. On-prem supports air-gapped installs.", ["onprem"]),
             ("y", "SaaS, sovereign or private cloud, and on-premises, including air-gapped.", ["deploy"])),
            ("Endpoint, email and network security",
             ("n", "Outside the AccuKnox platform, which covers AppSec, CloudSec and AI security.", ["faq"]),
             ("y", "Endpoint, email, network and identity security run on the same platform.", ["platform"])),
        ]),
    ],
    "fit_ak": [
        ("A platform team runs LLM apps and agents on Kubernetes and needs prevention, not only detection.",
         "KubeArmor blocks the call at the kernel before it executes, and the pod keeps running."),
        ("An ML team pulls open models from Hugging Face.",
         "Static scans check Pickle, HDF5, SavedModel, checkpoints and ONNX before anyone loads them."),
    ],
    "fit_them": [
        ("A CISO wants one vendor across endpoint, email, network, cloud and AI.",
         "Vision One runs all of those on one platform, with SaaS or sovereign deployment."),
        ("A security team must govern employee use of GenAI services.",
         "AI Secure Access blocks sensitive data, finds Shadow AI and restricts uploads."),
    ],
    "why": [
        ("Better", "KubeArmor enforces process, file and network policy at the kernel through eBPF and "
                   "Linux Security Modules. The workload keeps running while the single call is denied.", ["rt"]),
        ("Faster", "AI-SPM on SaaS deploys within minutes. An on-prem install takes 30 minutes to 4 hours, "
                   "with the same features.", ["onprem"]),
        ("Open", "KubeArmor is a CNCF Sandbox project that AccuKnox created and donated. "
                 "Teams can run and inspect the engine before they buy.", ["oss"]),
    ],
    "leads": ("TrendAI leads on platform breadth, on employee AI controls and on AI agent identity "
              "discovery. AccuKnox marks AI Identity Security and AI-GRC as roadmap.", ["ident"]),
}

BRIEFS = [TRENDAI, HARMONIC]

# --------------------------------------------------------------------------
LABEL = {"y": "Yes", "p": "Partial", "n": "No", "r": "Roadmap"}


def mark(state, size="3.6mm"):
    if state == "y":
        body = ('<circle cx="8" cy="8" r="8" fill="%s"/><path d="M4.3 8.2 6.8 10.7 '
                '11.8 5.4" stroke="#fff" stroke-width="2" fill="none" '
                'stroke-linecap="round" stroke-linejoin="round"/>' % GREEN)
    elif state == "n":
        body = ('<circle cx="8" cy="8" r="8" fill="%s"/><path d="M5.3 5.3 10.7 10.7 '
                'M10.7 5.3 5.3 10.7" stroke="#fff" stroke-width="2" fill="none" '
                'stroke-linecap="round"/>' % RED)
    elif state == "p":
        body = ('<circle cx="8" cy="8" r="8" fill="%s"/><path d="M4.9 8 11.1 8" '
                'stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>'
                % MUTE)
    else:
        body = ('<circle cx="8" cy="8" r="6.8" fill="#fff" stroke="%s" '
                'stroke-width="2.4"/><circle cx="8" cy="8" r="2.3" fill="%s"/>'
                % (SEC, SEC))
    return ('<svg class="mk" style="width:%s;height:%s" viewBox="0 0 16 16">%s'
            '</svg>' % (size, size, body))


def srcs(keys, table):
    return " ".join('<a href="%s">%s</a>' % (table[k][1], table[k][0]) for k in keys)


def cell(c, table):
    state, text, keys = c
    return ('<div class="ev">%s<b class="s-%s">%s.</b> %s</div><div class="sr">%s</div>'
            % (mark(state, "3.2mm"), state, LABEL[state], text, srcs(keys, table)))


def rows(b):
    out = []
    for g, stage, items in b["groups"]:
        for i, (p, ak, them) in enumerate(items):
            lab = ('<div class="mod">%s</div>' % g) if i == 0 else ""
            out.append('<tr class="%s"><td class="pm">%s<div class="pn">%s</div></td>'
                       '<td class="ak">%s</td><td class="tm">%s</td></tr>'
                       % ("g0" if i == 0 else "gn", lab, p, cell(ak, AK),
                          cell(them, b["src"])))
    return "".join(out)


def counts(b, lo, hi):
    flat = [r for _g, _s, items in b["groups"] for r in items][lo:hi]
    res = []
    for side in (1, 2):
        c = {"y": 0, "p": 0, "n": 0, "r": 0}
        for r in flat:
            c[r[side][0]] += 1
        res.append(c)
    return res, len(flat)


def scorecard(b):
    total = sum(len(i) for _g, _s, i in b["groups"])
    split = b["split"]
    parts = [("Eight AI security modules" if split != total else "All rows", 0, split)]
    if split < total:
        parts.append(("Runtime, workforce and platform" if b is TRENDAI else "Workforce GenAI usage",
                      split, total))
    body = []
    for name, lo, hi in parts:
        (a, t), n = counts(b, lo, hi)
        for vendor, c in (("AccuKnox", a), (b["vendor"], t)):
            body.append('<tr><td>%s, %d rows</td><td class="v">%s</td>%s</tr>'
                        % (name, n, vendor, "".join(
                            '<td class="n">%d</td>' % c[k] for k in "ypnr")))
    head = "".join('<th class="n">%s%s</th>' % (mark(k, "3mm"), LABEL[k]) for k in "ypnr")
    return ('<table class="score"><thead><tr><th>Scope</th><th>Vendor</th>%s</tr>'
            '</thead><tbody>%s</tbody></table>' % (head, "".join(body)))


def fits(b):
    def col(name, items):
        li = "".join('<li><b>%s</b><span>%s</span></li>' % (s, w) for s, w in items)
        return '<div class="fc"><h4>Choose %s when</h4><ul>%s</ul></div>' % (name, li)
    return '<div class="fits">%s%s</div>' % (col("AccuKnox", b["fit_ak"]),
                                             col(b["short"], b["fit_them"]))


def table_for(k):
    return AK if k in AK else None


def why(b):
    out = []
    for tag, txt, keys in b["why"]:
        links = " ".join('<a href="%s">%s</a>' % ((AK.get(k) or b["src"][k])[1],
                                                  (AK.get(k) or b["src"][k])[0]) for k in keys)
        out.append('<div class="wc"><i>%s</i><p>%s</p><div class="sr">%s</div></div>'
                   % (tag, txt, links))
    return '<div class="why">%s</div>' % "".join(out)


CSS = """
@page { size: A4; margin: 11mm 12mm 13mm;
  @bottom-right { content: "Page " counter(page) " of " counter(pages);
    font-family: 'Space Grotesk', sans-serif; font-size: 7pt; color: MUTE; } }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { font-family: 'Space Grotesk', 'Segoe UI', sans-serif; color: INK;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: BLUE; text-decoration: none; }

.band { background: NAVY; color: #fff; border-radius: 2.4mm; padding: 5.4mm 7mm 5.6mm;
  display: flex; justify-content: space-between; align-items: flex-end; }
.band img { height: 6.4mm; display: block; margin-bottom: 4.4mm; }
.band .eb { font-size: 7.4pt; letter-spacing: 2.4px; font-weight: 700; color: #A9BEFF; }
.band h1 { margin-top: 1.4mm; font-size: 22pt; line-height: 1.1; font-weight: 700;
  letter-spacing: -.6px; }
.band h1 span { color: #A9BEFF; font-weight: 500; }
.band .rd { font-size: 7.4pt; color: #CBD7FA; text-align: right; line-height: 1.5; white-space: nowrap; }

.sum { margin-top: 4mm; border-left: 3px solid BLUE; background: GREY_BG;
  border-radius: 2mm; padding: 4.2mm 5mm; }
.sum h3 { font-size: 7.4pt; letter-spacing: 1.8px; color: BLUE; font-weight: 700; }
.sum ol { margin-top: 2mm; padding-left: 4.4mm; }
.sum li { font-size: 9pt; line-height: 1.5; color: #23283F; margin-top: 1mm; }

.row2 { display: flex; gap: 5mm; margin-top: 4mm; }
.row2 > div { flex: 1; }
h2 { font-size: 11pt; font-weight: 700; color: NAVY; margin-bottom: 2.4mm; }
.scope { font-size: 8.4pt; line-height: 1.55; color: #3A4064; }
.scope .sr { margin-top: 1.6mm; }

table.score { width: 100%; border-collapse: collapse; }
table.score th { background: NAVY; color: #fff; font-size: 7.2pt; font-weight: 700;
  padding: 2.2mm 2mm; text-align: left; }
table.score th.n { text-align: center; white-space: nowrap; }
table.score th .mk { margin-right: 1mm; vertical-align: -.5mm; }
table.score td { border: 1px solid GREY_BD; font-size: 7.8pt; padding: 1.4mm 2mm; color: #23283F; }
table.score td.v { font-weight: 700; color: NAVY; }
table.score td.n { text-align: center; font-weight: 700; font-size: 9pt; }
table.score tbody tr:nth-child(4n+1) td, table.score tbody tr:nth-child(4n+2) td {
  background: TINT; }

.fits { display: flex; gap: 5mm; margin-top: 4mm; }
.fc { flex: 1; border: 1px solid GREY_BD; border-radius: 2mm; padding: 3mm 3.8mm; }
.fc h4 { font-size: 8.6pt; color: NAVY; font-weight: 700; }
.fc:first-child { border-top: 3px solid BLUE; }
.fc:last-child { border-top: 3px solid MUTE; }
.fc ul { list-style: none; margin-top: 2mm; }
.fc li { margin-top: 1.6mm; }
.fc li b { display: block; font-size: 8.2pt; color: #23283F; line-height: 1.4; }
.fc li span { display: block; font-size: 7.8pt; color: #4A5178; line-height: 1.45;
  margin-top: .6mm; }

.legend { display: flex; gap: 4mm; align-items: center; font-size: 7.2pt; color: MUTE;
  margin: 3.6mm 0 1.4mm; }
.legend .mk { margin-right: 1mm; vertical-align: -.6mm; }
.method { font-size: 7.2pt; color: MUTE; line-height: 1.5; }

table.mx { width: 100%; border-collapse: collapse; table-layout: fixed; margin-top: 2mm; }
table.mx thead { display: table-header-group; }
table.mx th { background: NAVY; color: #fff; font-size: 8pt; font-weight: 700;
  text-align: left; padding: 2.4mm 3mm; vertical-align: middle; }
table.mx th img { height: 4.2mm; display: block; }
table.mx tr { break-inside: avoid; page-break-inside: avoid; }
table.mx td { border: 1px solid GREY_BD; padding: 1.7mm 2.6mm 1.9mm; vertical-align: top; }
table.mx tr.g0 td { border-top: 1.6px solid NAVY; }
.mod { font-size: 6.4pt; font-weight: 700; color: BLUE; letter-spacing: .3px; line-height: 1.3; margin-bottom: 1mm; }
.mod i { display: block; font-style: normal; color: MUTE; letter-spacing: 1px; text-transform: uppercase; font-size: 5.8pt; margin-top: .3mm; }
.pn { font-size: 7.8pt; font-weight: 600; color: NAVY; line-height: 1.32; }
table.mx tr.grp td { background: GREY_BG; border-left: 3px solid BLUE; padding: 1.6mm 3mm; }
table.mx tr.grp span { font-size: 8pt; font-weight: 700; color: NAVY; }
table.mx tr.grp i { float: right; font-style: normal; font-size: 6.8pt; letter-spacing: 1.2px;
  text-transform: uppercase; color: MUTE; font-weight: 700; padding-top: .4mm; }
td.pm { }
td.ak { background: TINT; }
.st { display: flex; align-items: center; gap: 1.4mm; }
.ev .mk { vertical-align: -.7mm; margin-right: 1.2mm; }
.ev b { font-size: 7.5pt; margin-right: .6mm; }
.s-y { color: GREEN; } .s-n { color: RED; } .s-p { color: MUTE; } .s-r { color: SEC; }
.ev { font-size: 7.5pt; line-height: 1.4; color: #23283F; }
.sr { margin-top: .6mm; font-size: 6.3pt; line-height: 1.4; color: MUTE; }
.sr a + a:before { content: "  |  "; color: GREY_BD; }

.close { break-inside: avoid; page-break-inside: avoid; margin-top: 4mm; }
.why { display: flex; gap: 4mm; }
.wc { flex: 1; border: 1px solid GREY_BD; border-radius: 2mm; padding: 2.8mm 3.4mm; }
.wc i { display: inline-block; font-style: normal; font-size: 7.2pt; font-weight: 700;
  letter-spacing: 1px; text-transform: uppercase; color: #fff; background: BLUE;
  padding: 1.2mm 2.6mm; border-radius: 1.4mm; }
.wc:nth-child(2) i { background: SEC; } .wc:nth-child(3) i { background: GREEN; }
.wc p { margin-top: 1.8mm; font-size: 7.8pt; line-height: 1.5; color: #2B3150; }
.leads { margin-top: 3mm; border: 1px solid GREY_BD; border-left: 3px solid MUTE;
  border-radius: 2mm; padding: 3.2mm 4.2mm; }
.leads b { font-size: 7.2pt; letter-spacing: 1.4px; color: MUTE; }
.leads p { margin-top: 1.4mm; font-size: 8.2pt; line-height: 1.5; color: #2B3150; }
.cta { margin-top: 3mm; background: NAVY; color: #fff; border-radius: 2mm;
  padding: 3mm 5mm; display: flex; justify-content: space-between; align-items: center; }
.cta b { font-size: 10pt; } .cta span { font-size: 8pt; color: #CBD7FA; }
.cta img { height: 5.6mm; }
"""
for _k, _v in (("GREY_BG", GREY_BG), ("GREY_BD", GREY_BD), ("TINT", TINT),
               ("INK", INK), ("NAVY", NAVY), ("BLUE", BLUE), ("SEC", SEC),
               ("RED", RED), ("GREEN", GREEN), ("MUTE", MUTE)):
    CSS = CSS.replace(_k, _v)


def build_html(b):
    full = (b["title"] + " " + b["qual"]).strip()
    css = CSS.replace("FOOTER", full + "  \\00B7  accuknox.com")
    qual = ' <span>%s</span>' % b["qual"] if b["qual"] else ""
    legend = ('<div class="legend">%s</div>' % "".join(
        '<span>%s%s</span>' % (mark(k, "3.2mm"), t) for k, t in (
            ("y", "Yes, shipped and documented"), ("p", "Partial"),
            ("n", "No, absent from the vendor's site"), ("r", "Roadmap"))))
    scope_txt, scope_keys = b["scope"]
    lead_txt, lead_keys = b["leads"]

    def anysrc(keys):
        return " ".join('<a href="%s">%s</a>' % ((AK.get(k) or b["src"][k])[1],
                                                 (AK.get(k) or b["src"][k])[0]) for k in keys)

    html = """
<div class="band"><div>
  <img src="{logo}" alt="AccuKnox">
  <h1>{title}{qual}</h1></div>
</div>

<div class="sum"><h3>THE SHORT ANSWER</h3><ol>{summary}</ol></div>

<div class="row2">
  <div><h2>Scorecard</h2>{score}</div>
</div>
{fits}

<table class="mx"><colgroup><col style="width:21%"><col style="width:39.5%"><col style="width:39.5%"></colgroup>
<thead><tr><th>Capability</th><th><img src="{logo}" alt="AccuKnox"></th><th>{vendor}</th></tr></thead>
<tbody>{rows}</tbody></table>

<div class="close"><h2 style="margin-top:2mm">Why teams choose AccuKnox over {vendor}</h2>
  {why}
  <div class="leads"><b>WHERE {VENDOR} LEADS</b><p>{leads}</p><div class="sr">{lead_src}</div></div>
  <div class="cta"><div><b>See the AccuKnox platform in action</b><br>
    <span>accuknox.com  \u00b7  support@accuknox.com</span></div><img src="{logo}" alt=""></div>
</div>
""".format(logo=LOGO_DARK, title=b["title"], qual=qual, read=READ_ON,
           summary="".join("<li>%s</li>" % s for s in b["summary"]),
           score=scorecard(b), scope=scope_txt, scope_src=anysrc(scope_keys),
           fits=fits(b), legend=legend, vendor=b["vendor"], rows=rows(b),
           why=why(b), VENDOR=b["vendor"].upper(), leads=lead_txt,
           lead_src=anysrc(lead_keys))
    return ("<!doctype html><meta charset='utf-8'><title>%s</title><style>%s</style>%s"
            % (full, css, html))


def main():
    os.makedirs(WORK, exist_ok=True)
    only = sys.argv[1:] or [b["file"] for b in BRIEFS]
    for b in BRIEFS:
        if b["file"] not in only:
            continue
        html_path = os.path.join(WORK, b["file"] + ".html")
        pdf_path = os.path.join(OUT, b["file"] + ".pdf")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(build_html(b))
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        subprocess.run([
            EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--print-to-pdf=" + pdf_path, html_path.replace("\\", "/"),
        ], check=True, timeout=300)
        print("wrote %s (%.2f MB)" % (pdf_path, os.path.getsize(pdf_path) / 1e6))


if __name__ == "__main__":
    sys.exit(main())
