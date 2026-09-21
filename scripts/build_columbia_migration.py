# -*- coding: utf-8 -*-
"""Columbia University (CUIT) CloudDefense to AccuKnox CSPM migration proposal.

A rebuild of AccuKnox_Columbia_CSPM_Migration_Proposal.pptx in the AccuKnox
keynote style: a navy canvas, real product screens as the light source, one
claim per slide, and a source line on every slide that carries a fact.

Nothing from the source deck is dropped. Slides that carried two arguments at
once were split, and the two slides that said the same thing twice were merged,
so every fact in the original survives somewhere in this deck.

Imagery lives in assets/deck-images/columbia. Each file is a tight crop of a
screen in output/assets or output/assets/agentz, made by prep_images() below.

Run:  py -3.11 scripts/build_columbia_migration.py
"""
import sys
from pathlib import Path

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "accuknox-keynote-deck" / "scripts"))

from akslides import (BODY, M, SW, Deck, T, box, char_spacing, fill,  # noqa: E402
                      hline, panel, pin)

IMG = ROOT / "assets" / "deck-images" / "columbia"
SRC = ROOT / "output" / "assets"

# Each entry is (source screen, crop box, output name). The crop drops the empty
# rows under a table and the signed-in user name in a console sidebar.
CROPS = [
    ("compliance-dashboard.png", (0, 0, 2048, 880), "compliance.png"),
    ("policies.png", (0, 0, 2048, 680), "policies.png"),
    ("runtime-events.png", (0, 0, 2048, 930), "runtime.png"),
    ("agentz/agentz-workflow-graph.png", (0, 0, 2048, 845), "workflow.png"),
    ("agentz/trace-after.png", (0, 0, 2048, 136), "trace-after.png"),
    ("agentz/Ai-sec-Runtime-Agent-Sandboxing.png", (0, 0, 1200, 750), "sandbox.png"),
]


def prep_images():
    """Rebuild assets/deck-images/columbia from the shared screens in output/assets.

    The on-prem diagram ships with a transparent background, so it is flattened
    onto the navy canvas colour. Without that step the picture hairline draws a
    box around a mostly empty rectangle."""
    from PIL import Image

    IMG.mkdir(parents=True, exist_ok=True)
    for src, crop, name in CROPS:
        Image.open(SRC / src).convert("RGBA").crop(crop).save(IMG / name)
    arch = Image.open(SRC / "onprem-arch.png").convert("RGBA")
    navy = Image.new("RGBA", arch.size, (0x11, 0x20, 0x6D, 255))
    navy.alpha_composite(arch)
    navy.convert("RGB").save(IMG / "arch.png")
    print("prepared", len(CROPS) + 1, "images in", IMG)


# --------------------------------------------------------------- custom layout
def ownership(d, D):
    """Two owner columns, one row per task.

    The stock `compare` layout marks its left column with a red cross, which is
    the wrong reading for a split of work between two teams. This draws the same
    two columns with a neutral marker instead."""
    s = d._slide()
    d.title(s, D["title"], w=7.4)
    cw = (SW - 2 * M - 0.4) / 2
    for col, (head, count, color) in enumerate(D["heads"]):
        x = M + col * (cw + 0.4)
        c = box(s, x, BODY, cw - 0.9, 0.24, head, 8, T.WHITE, font=T.SEMI)
        char_spacing(c, 1.2)
        box(s, x + cw - 0.9, BODY - 0.06, 0.9, 0.3, count, 13, T.WHITE, font=T.MED,
            align=PP_ALIGN.RIGHT)
        hline(s, x, BODY + 0.3, cw, color=color, alpha=None, weight=2.0)
    step = D.get("step", 0.54)
    for col, items in enumerate(D["cols"]):
        x = M + col * (cw + 0.4)
        for i, task in enumerate(items):
            y = BODY + 0.5 + i * step
            dot = box(s, x + 0.04, y + 0.09, 0.09, 0.09, shape=MSO_SHAPE.OVAL)
            fill(dot, d.accent if col == 0 else T.SOFT)
            box(s, x + 0.3, y, cw - 0.35, step - 0.06, task, 9.5, T.WHITE, spacing=1.1)
    return d._finish(s, D)


def build():
    d = Deck("AccuKnox_Columbia_CSPM_Migration", accent=T.PRIMARY)

    # 1 ---------------------------------------------------------------- cover
    d.cover("CloudDefense to AccuKnox\nCSPM Migration",
            scope=[("1", "AWS config change"), ("0", "team re-onboarding"),
                   ("4-6 wks", "cutover timeline")], tsize=22)

    # 2 --------------------------------------------------------------- agenda
    d.agenda({
        "title": "This Proposal Answers Three Questions",
        "items": [
            ("How the migration runs", "One AWS change, five phases"),
            ("Why AccuKnox over Wiz", "Enforcement, not detection alone"),
            ("What AgentZ adds", "Included, with no second vendor"),
        ],
        "footnote": "Prepared for Columbia University Information Technology (CUIT).",
        "notes": "Part 1 is the plan and the ask. Part 2 is the competitive case. "
                 "Part 3 is the automation CUIT gets at no extra procurement.",
    })

    # 3 -------------------------------------------------------------- part one
    d.section({
        "number": "01",
        "title": "The Migration Plan",
        "sub": "A low-effort switch for CUIT. AccuKnox carries the work from "
               "kickoff through go-live.",
    })

    # 4 ---------------------------------------------------------------- stats
    d.stats({
        "title": "Three Numbers Define CUIT's Side of This Migration",
        "items": [
            ("1", "AWS config change CUIT makes, the AssumeRole ARN update",
             "Phase 3 of the plan"),
            ("0", "users, teams or roles CUIT has to re-onboard",
             "AccuKnox pre-populates them"),
            ("0", "new AWS IAM roles to design or send for review",
             "Existing roles carry over as is"),
        ],
        "footnote": "Decision requested: approve the on-prem model, Option A or "
                    "Option B, then set a target cutover date.",
        "notes": "Executive summary of the source proposal, slide 3. AccuKnox moves "
                 "CUIT's CSPM program from CloudDefense to AccuKnox, deployed on-prem "
                 "inside Columbia's own environment. The four named principles behind "
                 "these numbers are on the heavy-lifting slide later in Part 1.",
    })

    # 5 ------------------------------------------------- on-prem architecture
    d.image({
        "title": "Your Scan Data Never Leaves\nColumbia's Network",
        "image": str(IMG / "arch.png"),
        "img_h": 3.8, "img_x": 4.90, "img_y": 1.42, "glow": False,
        "rail_top": 1.56, "rail_step": 0.92, "rail_w": 2.6, "numbered": False,
        "rail": [
            ("Meets FERPA rules",
             "Regulated student and research data stays inside Columbia's boundary."),
            ("CUIT keeps full custody",
             "No AccuKnox account ever touches a raw finding or a credential."),
            ("Audit ready, always",
             "Every scan and access event lands in Columbia's own logs."),
            ("Zero egress",
             "No scan data or finding leaves the network, at any point."),
        ],
        "footnote": "AccuKnox on-prem deployment architecture, from the AccuKnox "
                    "product documentation.",
        "notes": "Source deck slide 4, Your Data Never Leaves Columbia. The scanner, "
                 "the findings store and the compliance controls all run inside "
                 "Columbia University premises. The diagram shows the worker "
                 "clusters, virtual machines, container registries and SIEM channels "
                 "that the on-prem deployment reaches.",
    })

    # 6 ------------------------------------------------------- the AWS change
    d.pipeline({
        "title": "One AssumeRole ARN Update Is the\nEntire AWS-Side Change",
        "stages": [
            ("01", "CUIT Security Team", "Same users, same teams, same roles as today."),
            ("02", "AccuKnox Platform", "Runs on-prem, inside Columbia's own boundary."),
            ("03", "AWS Account", "Same IAM roles, reused exactly as they are."),
        ],
        "band": ("What changes for CUIT",
                 "The AssumeRole ARN moves from CloudDefense to AccuKnox. Nothing "
                 "else in AWS changes.", "1", "AWS setting"),
        "footnote": "Access, visibility and scan behavior stay the same. Same users, "
                    "same roles, same findings.",
        "notes": "Source deck slide 5. The engine changes and the AWS account does "
                 "not. CUIT should hear that the new engine returns findings against "
                 "the same roles it already approved.",
    })

    # 7 ----------------------------------------------------- management model
    d.matrix({
        "title": "Two Management Models Reach\nthe Same Architecture",
        "cols": [("DIMENSION", 2.0), ("OPTION A: ACCUKNOX-MANAGED", 3.9),
                 ("OPTION B: CUIT-MANAGED", 3.7)],
        "rows": [
            ["Who runs day 2",
             "AccuKnox runs deployment, upgrades, monitoring and day-2 operations.",
             "Columbia's own team runs day-to-day operations on-prem."],
            ["CUIT effort",
             "Near zero. Columbia grants scoped infrastructure access.",
             "Higher. CUIT keeps control and assigns an owner."],
            ["AccuKnox role",
             "AccuKnox owns uptime.",
             "AccuKnox supplies runbooks, setup guidance and live support."],
            ["Best fit",
             "Lean teams that want the platform run for them.",
             "Hands-on teams that want the keys."],
        ],
        "chips": [("BOTH OPTIONS", ["Same on-prem architecture", "Same data residency",
                                    "Switch later with no re-onboarding"])],
        "footnote": "Columbia can start with one model and move to the other without "
                    "new IAM work.",
        "notes": "Source deck slide 6. Either way AccuKnox supports CUIT through "
                 "go-live and beyond. Both options land on the same on-prem "
                 "architecture shown on the previous slide.",
    })

    # 8 -------------------------------------------------- migration principles
    d.statement({
        "title": "AccuKnox Carries the Heavy Lifting\non Three Fronts",
        "lead": "These three principles are why AccuKnox can pre-populate access and "
                "map IAM without CUIT touching a role definition.",
        "points": [
            "AccuKnox mirrors the exact users, teams and roles from CloudDefense "
            "before cutover. CUIT recreates nothing.",
            "The AWS roles CUIT built for CloudDefense carry over as is. AccuKnox "
            "needs no new role design and no fresh security review.",
            "Configuration, mapping and validation run on AccuKnox's side. CUIT "
            "points the AssumeRole ARN at AccuKnox.",
        ],
        "footnote": "These principles remove the re-onboarding work and the new IAM "
                    "roles from Phases 1 and 2.",
        "notes": "Source deck slide 7, Migration Principles. The seller should land "
                 "the phrase zero re-onboarding and zero new IAM roles here, because "
                 "they are the two numbers on the executive summary slide.",
    })

    # 9 ------------------------------------------------------------- timeline
    d.timeline({
        "title": "Five Phases Run From Kickoff to Hypercare",
        "items": [
            ("Phase 0", "Kickoff", "Week 1. Confirm the management model."),
            ("Phase 1", "Pre-populate", "Weeks 1 to 2. AccuKnox mirrors roles and maps IAM."),
            ("Phase 2", "Review", "Week 3. CUIT reviews access. AccuKnox runs UAT."),
            ("Phase 3", "Go-live", "Week 4. CUIT updates the AssumeRole ARN."),
            ("Phase 4", "Hypercare", "Weeks 4 to 6. AccuKnox stays hands-on."),
        ],
        "footnote": "CUIT acts in Phase 3 only. Every other phase runs on AccuKnox's side.",
        "notes": "Source deck slide 8. The phased rollout keeps risk low. Phase 3 is "
                 "the only phase that needs a CUIT action.",
    })

    # 10 --------------------------------------------------- roles and ownership
    ownership(d, {
        "title": "CUIT's Five Tasks Include\nOnly One AWS Change",
        "heads": [("ACCUKNOX OWNS", "6", T.PRIMARY), ("CUIT OWNS", "5", T.SOFT)],
        "cols": [
            ["Pre-populate users, teams and roles to mirror CloudDefense.",
             "Deploy and configure AccuKnox on-prem in Columbia's environment.",
             "Map and validate existing AWS IAM roles for reuse.",
             "Migrate and validate CSPM policies and compliance benchmarks.",
             "Provide hands-on support through cutover and go-live.",
             "Own day-2 operations under the AccuKnox-managed model, Option A."],
            ["Update the AssumeRole ARN in AWS to point to AccuKnox.",
             "Confirm migrated users, teams and roles match expectations.",
             "Grant scoped infra access for Option A, or assign an owner for Option B.",
             "Validate scan results and policy behavior during UAT.",
             "Sign off on go-live readiness."],
        ],
        "footnote": "Of CUIT's five tasks, four are reviews and approvals. One is a "
                    "configuration change.",
        "notes": "Source deck slide 9, Roles and Responsibilities. The workload split "
                 "is deliberate. If CUIT pushes back on effort, this is the slide to "
                 "return to.",
    })

    # 11 ------------------------------------------------------ success criteria
    d.statement({
        "title": "CUIT Signs Off on Five Criteria\nBefore Go-Live",
        "body_y": 2.05,
        "points": [
            "All CloudDefense users, teams and roles are present and validated inside "
            "AccuKnox.",
            "The AWS AssumeRole ARN is updated and confirmed working end to end.",
            "On-prem CSPM scans return findings that match CloudDefense's last baseline.",
            "CUIT has reviewed and signed off on go-live readiness.",
            "The hypercare window closes with no open cutover issues.",
        ],
        "footnote": "AccuKnox calls the cutover complete only after CUIT signs off on "
                    "every criterion above.",
        "notes": "Source deck slide 10, Success Criteria. Read these out loud on the "
                 "call. They are the definition of done for the engagement.",
    })

    # 12 ------------------------------------------------------------ the ask
    d.agenda({
        "title": "Three Approvals Start Phase 0",
        "items": [
            ("Approve the on-prem model", "Option A or Option B"),
            ("Confirm a target cutover date", "For the AssumeRole ARN update"),
            ("Approve Phase 0 kickoff", "With CUIT infrastructure"),
        ],
        "footnote": "AccuKnox can run this migration on the timeline above once these "
                    "three items are approved.",
        "notes": "Source deck slide 10, Suggested Next Steps. Ask for the first two "
                 "on the call, because the third follows from them.",
    })

    # 13 ------------------------------------------------------------ part two
    d.section({
        "number": "02",
        "title": "Why AccuKnox Wins",
        "sub": "Built to block attacks at the kernel, rather than report them after "
               "the fact.",
    })

    # 14 ------------------------------------------------------ wiz comparison
    d.matrix({
        "title": "Wiz Reports the Risk and AccuKnox Blocks It",
        "cols": [("ATTRIBUTE", 2.1), ("WIZ", 3.9), ("ACCUKNOX", 3.6)],
        "rows": [
            ["Primary philosophy",
             "Visibility and context. Find critical risks and graph them for a team "
             "to act on.",
             "Active enforcement. A deny-by-default model that stops the attack itself."],
            ["Deployment",
             "Agentless only. API and snapshot scanning, with a gap between scans.",
             "Hybrid. Agentless posture scanning plus lightweight in-line agents for "
             "runtime."],
            ["Runtime protection",
             "Detection and alerting. Depends on external tools once the exploit is live.",
             "Kernel-level blocking with eBPF and Linux Security Modules, in real time."],
        ],
        "chips": [("BUILT ON OPEN TECHNOLOGY", ["KubeArmor, a CNCF project",
                                                "Linux Security Modules",
                                                "Kubernetes-native"])],
        "footnote": "Wiz column drawn from Wiz public product pages. [Confirm the page "
                    "URLs and access date before this goes to Columbia.]",
        "notes": "Source deck slide 12. The bracketed note in the footnote is a real "
                 "gap: the source proposal states the Wiz column with no citation. "
                 "Get the URLs from the competitive team and replace the bracket "
                 "before sending. A named competitor without a source is the line a "
                 "technical reviewer picks at first.",
    })

    # 15 ---------------------------------------------- environments comparison
    d.compare({
        "title": "Only One of These Two Runs Inside\nColumbia's Own Network",
        "heads": ("WIZ", "ACCUKNOX"),
        "rows": [
            ("Public cloud only: AWS, Azure, GCP and OCI. No on-prem and no "
             "air-gapped option.",
             "Public cloud, private cloud, on-prem and air-gapped, like Columbia's "
             "deployment."),
            ("Scans clusters for structural vulnerabilities and drift between scans.",
             "Built on the open-source KubeArmor engine. Blocks container breakouts live."),
            ("Broad CNAPP built for visibility at scale, priced and packaged for that job.",
             "A focused enforcement platform for regulated, engineering-heavy teams."),
        ],
        "footnote": "Wiz turns a finding into a ticket. AccuKnox turns it into a "
                    "block, with no human in the loop.",
        "notes": "Source deck slide 12, second half. Columbia's deployment is on-prem, "
                 "so the environments row decides this comparison on its own. Same "
                 "citation gap as the previous slide applies to the Wiz column.",
    })

    # 16 ---------------------------------------------------- prevention model
    d.pipeline({
        "title": "Observe, Enforce and Auto-Policy\nAll Run at the Kernel",
        "stages": [
            ("01", "Observe", "Learn each workload's normal process, file and network "
                              "behavior."),
            ("02", "Enforce", "Block anything outside that baseline in line, at the "
                              "kernel."),
            ("03", "Auto-Policy", "Generate hardening policy from what AccuKnox "
                                  "observed."),
        ],
        "band": ("Deny by default",
                 "Unapproved behavior never runs, so a compromised container is "
                 "blocked before it reaches research or student data.", None, None),
        "footnote": "Most CSPM and CNAPP tools report an attack once it already ran. "
                    "AccuKnox blocks it in line.",
        "notes": "Source deck slide 13. For Columbia the argument is specific: "
                 "research data and student data sit behind these workloads.",
    })

    # 17 ------------------------------------------------- runtime event stream
    d.annotated({
        "title": "Every Block Lands in the Event\nStream With Its Action",
        "main": str(IMG / "runtime.png"),
        "img_x": 3.30, "img_y": 1.45, "img_w": 6.95,
        "pins": [(1, "main", 960, 361), (2, "main", 960, 485), (3, "main", 1300, 610)],
        "rail_top": 1.62, "rail_step": 0.95,
        "rail": [
            ("A write to /etc/",
             "A config tamper attempt, caught the moment it happens."),
            ("Cryptominer blocked",
             "AccuKnox stopped the process. The row is the record."),
            ("Action on every row",
             "Process, file or network, with the policy decision beside it."),
        ],
        "footnote": "AccuKnox runtime event stream. Rows include Write to /dev/shm "
                    "folder prevented, an escape path closed in line.",
        "notes": "This slide replaces the detection-first versus prevention-first "
                 "text panels on source slide 13 with the real event stream. A "
                 "detection-first tool flags the exploit after it is active, the "
                 "alert waits in a queue for triage, and containment depends on how "
                 "fast the team responds. Each row here is already the block.",
    })

    # 18 ---------------------------------------------------------- part three
    d.section({
        "number": "03",
        "title": "AgentZ, Agentic\nSecurity Automation",
        "sub": "Included in the platform. One more reason this is a switch rather "
               "than a multi-year rebuild.",
    })

    # 19 ------------------------------------------------------ agentz sandbox
    d.image({
        "title": "AgentZ Runs Every Agent in a\nDefault-Deny Sandbox",
        "image": str(IMG / "sandbox.png"),
        "img_h": 3.45, "img_y": 1.50,
        "rail_top": 1.56, "rail_step": 0.92, "rail_w": 2.55, "numbered": False,
        "rail": [
            ("Default deny",
             "From the first run, the agent gets nothing the policy did not grant."),
            ("Domain-level egress",
             "AgentZ blocks outbound traffic at the kernel, by domain."),
            ("No standing credentials",
             "The policy on the right blocks reads of /root/.aws and similar paths."),
            ("Replayable audit trail",
             "Every tool call is recorded down to the span."),
        ],
        "footnote": "KubeArmorPolicy ai-agent-zerotrust, from the AccuKnox AI "
                    "security console.",
        "notes": "Source deck slide 15. The YAML on the right is the proof for the "
                 "third rail item: matchDirectories blocks /root/.aws recursively, "
                 "which is the path an agent would use to reach AWS credentials.",
    })

    # 20 ------------------------------------------------------- one control plane
    d.statement({
        "title": "One Control Plane Covers CSPM\nand Agent Security",
        "lead": "AgentZ runs on the same KubeArmor and eBPF engine as the CSPM "
                "platform in this proposal.",
        "points": [
            "CUIT adopts one control plane for both, instead of onboarding a separate "
            "vendor for agent security later.",
            "As Columbia's researchers and students start building AI agents, AgentZ "
            "becomes CUIT's governance layer for all of them.",
            "AgentZ is included in the platform, so this stays a switch rather than a "
            "second procurement.",
        ],
        "footnote": "AgentZ and the CSPM platform share one tenant, one policy engine "
                    "and one audit trail.",
        "notes": "Source deck slide 15, lower half. The same engine securing this "
                 "migration also runs CUIT's next AI agents.",
    })

    # 21 ------------------------------------------------------ automation loop
    d.pipeline({
        "title": "Detect, Prioritize, Act and Confirm\nRun Without a Person",
        "stages": [
            ("01", "Detect", "A scan confirms the finding."),
            ("02", "Prioritize", "AgentZ scores it by exploitability."),
            ("03", "Act", "AgentZ remediates it or opens a ticket."),
            ("04", "Confirm", "AgentZ re-tests the fix and closes the finding."),
        ],
        "band": ("Closes the Part 1 loop",
                 "Re-test and confirmation become automatic once CUIT enables AgentZ, "
                 "which is the last success criterion in Part 1.", None, None),
        "footnote": "Beyond the migration itself, AgentZ automates the work that "
                    "follows every scan.",
        "notes": "Source deck slide 16. Tie this back to the success criteria slide "
                 "in Part 1, where re-test and confirmation are manual today.",
    })

    # 22 ------------------------------------------------------------ workflows
    d.matrix({
        "title": "Four Workflows AgentZ Automates for CUIT",
        "cols": [("WORKFLOW", 3.0), ("WHAT AGENTZ DOES", 6.6)],
        "rows": [
            ["Auto-remediation playbooks",
             "Closes common misconfigurations with no person in the loop, policy-gated "
             "and logged."],
            ["Compliance evidence collection",
             "Assembles audit evidence on a schedule, ready for the next review."],
            ["Ticket and alert routing",
             "Opens a scoped ticket and routes an alert on every confirmed finding."],
            ["Scheduled re-test",
             "Re-runs validation after a fix ships and confirms the finding is closed."],
        ],
        "footnote": "Each workflow runs inside AgentZ, on the same tenant as the CSPM "
                    "platform.",
        "notes": "Source deck slide 16, the four capability cards. Manual triage "
                 "disappears from the ticket and alert row, which is the one CUIT "
                 "will feel first.",
    })

    # 23 -------------------------------------------------- finding to verdict
    d.pipeline({
        "title": "From a Raw Finding to a Verified Critical",
        "stages": [
            ("01", "ASM Findings", "Every exposed asset surfaces here."),
            ("02", "Investigate", "AgentZ finds the root cause, per finding type."),
            ("03", "Correlate", "AgentZ links related findings together."),
            ("04", "Report", "AgentZ documents the evidence."),
            ("05", "Re-Score", "AgentZ re-scores severity on that evidence."),
        ],
        "band": ("A verified verdict",
                 "A Critical from AccuKnox is already investigated and correlated "
                 "before the severity reaches CUIT.", None, None),
        "footnote": "Every finding is investigated, correlated and re-scored before a "
                    "severity reaches CUIT.",
        "notes": "Source deck slide 17. The claim to land is that a Critical from "
                 "AccuKnox is not a scanner's guess.",
    })

    # 24 --------------------------------------------- investigation principles
    d.statement({
        "title": "Three Steps Run Before a Severity\nReaches CUIT",
        "lead": "AgentZ works each finding on its own merit: what is exposed, how it "
                "is exposed, and what it reaches.",
        "points": [
            "AgentZ investigates each finding type separately, rather than applying "
            "one rule to all of them.",
            "Findings that share a root cause get linked into one story. CUIT sees "
            "one risk rather than a pile of tickets.",
            "Severity moves up or down on evidence. AgentZ marks confirmed noise as "
            "ignore and escalates real risk.",
        ],
        "footnote": "A finding that AccuKnox escalates stays escalated, because the "
                    "evidence sits behind it.",
        "notes": "Source deck slide 17, the three principle cards.",
    })

    # 25 -------------------------------------------------- live workflow proof
    d.annotated({
        "title": "A Live AgentZ Workflow Investigates\nEvery KubeArmor Alert",
        "main": str(IMG / "workflow.png"),
        "img_x": 3.30, "img_y": 1.45, "img_w": 6.95,
        "insets": [{"img": str(IMG / "trace-after.png"), "x": 3.45, "y": 4.48, "w": 6.0}],
        "pins": [(1, "main", 330, 418), (2, "main", 778, 521),
                 (3, "main", 1232, 690), (4, 0, 300, 68)],
        "rail_top": 1.6, "rail_step": 0.90,
        "rail": [
            ("Analyze the alert",
             "The workflow opens on the KubeArmor alert and finds the root cause."),
            ("Build the report",
             "AgentZ writes an HTML report from the analysis and the evidence."),
            ("Route the outcome",
             "Success and failure branches both land where a person can see them."),
            ("Replay the whole run",
             "The trace records duration, spans, tool calls and token use."),
        ],
        "footnote": "AgentZ workflow graph and run trace, from the AccuKnox AI "
                    "security console.",
        "notes": "This slide replaces the three empty screenshot placeholders on "
                 "source slide 18 with a real AgentZ workflow graph and a real run "
                 "trace. The workflow shown is kubearmor-alert-investigation. If a "
                 "severity distribution graph and a single investigation report "
                 "become available from a live environment, add them as two further "
                 "slides rather than replacing this one.",
    })

    # 26 ---------------------------------------------------------------- close
    d.close()

    return d.save()


if __name__ == "__main__":
    if "--prep" in sys.argv:
        prep_images()
    build()
