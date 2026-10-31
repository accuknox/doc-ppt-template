# -*- coding: utf-8 -*-
"""
AccuKnox DSPM PoC plan for Airtel. Ten slides, visual system from
accuknox-visual-deck, structure from the AI Security PoC deck.

Sources:
  1. help.accuknox.com/getting-started/dspm-overview/ and dspm-onboarding/
     (local copies in D:/AccuKnox/help/docs/getting-started/).
  2. Airtel PoC scoping call notes, 5 October 2026: OpenStack only, VM deployment,
     data stores in and out of scope, control plane spec, two-week sequence.
  3. Onboarding screenshots from Downloads: image (3).png and image (4).png.
Unconfirmed facts are drawn as red TO CONFIRM panels.

Build:  py -3.11 scripts/airtel_dspm_svg.py && py -3.11 scripts/build_airtel_dspm_poc.py
"""
import os, shutil, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image as PI

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import *  # noqa: F401,F403
import airtel_dspm_native as native

google_safe()

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "PPT Template.pptx")
OUT = os.path.join(HERE, "..", "output", "AccuKnox_Airtel_DSPM_PoC.pptx")
WORK = os.path.join(HERE, "..", "work", "airtel_dspm")
DIAG = os.path.join(WORK, "diagrams")
HELP = r"D:/AccuKnox/help/docs/getting-started/images/dspm"
DL = r"C:/Users/AtharvaShah/Downloads"
os.makedirs(os.path.join(WORK, "crops"), exist_ok=True)

U_OVERVIEW = "https://help.accuknox.com/getting-started/dspm-overview/"
U_ONBOARD = "https://help.accuknox.com/getting-started/dspm-onboarding/"
U_PLATFORM = "https://accuknox.com/platform/dspm"
U_MICRO = "https://docs.google.com/presentation/d/1sqVm9cFuDlEz53xp8SEyRToRzVhiNFkhZAyHDDcdGnY/edit"
U_ONPREM = U_OVERVIEW + "#run-the-console-on-premises"
U_TOKENS = "https://help.accuknox.com/how-to/how-to-create-tokens/"

shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_STD = prs.slide_layouts[4]
lst = prs.slides._sldIdLst
for sid in list(lst):
    try: prs.part.drop_rel(sid.get(qn("r:id")))
    except Exception: pass
    lst.remove(sid)


def std(title, kicker, notes_text):
    s = prs.slides.add_slide(L_STD); set_title(s, title); blank_footer(s)
    eyebrow(s, kicker, y=0.84, w=8.6, size=11)
    notes(s, notes_text)
    return s


def crop(src, box_, name):
    p = os.path.join(WORK, "crops", name + ".png")
    im = PI.open(src)
    if box_:
        im = im.crop(box_)
    im.save(p)
    return p


def shot(slide, path, x, y, w, h):
    """Screenshot scaled to fit, centred in a light frame."""
    box(slide, x, y, w, h, fill=GREY_BG, line=GREY_BD, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
    im = PI.open(path); ar = im.size[0] / im.size[1]
    pw, ph = w - 0.08, h - 0.08
    if pw / ph > ar: dh = ph; dw = ph * ar
    else: dw = pw; dh = pw / ar
    pic = slide.shapes.add_picture(path, Inches(x + (w - dw) / 2), Inches(y + (h - dh) / 2), Inches(dw), Inches(dh))
    pic.line.color.rgb = GREY_BD; pic.line.width = Pt(0.75)
    return pic


def link(shape, url):
    for p in shape.text_frame.paragraphs:
        for r in p.runs:
            r.hyperlink.address = url


slides = {}

# ============================================================ 1. cover
cover_slide(prs, "Airtel DSPM PoC Plan", subtitle="PI data discovery on Airtel Cloud, 7 to 21 October 2026", tsize=28)

def full_shot(title, kicker, img, checks, ok, notes_text):
    """One screenshot per slide, as large as the slide allows, with what to check."""
    s = std(title, kicker, notes_text)
    iw, ih = PI.open(img).size; ar = iw / ih
    if ar > 2.2:   # wide strip: image full width, checks in a row below
        w = 9.2; h = w / ar
        shot(s, img, 0.40, 1.14, w, h + 0.08)
        y = 1.14 + h + 0.22
        cw = (9.2 - 0.3) / 3
        for i, (icn, t) in enumerate(checks):
            x = 0.40 + i * (cw + 0.15)
            box(s, x, y, cw, 0.62, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.18)
            icon_tile(s, icn, x + 0.1, y + 0.1, 0.42)
            box(s, x + 0.6, y + 0.04, cw - 0.66, 0.54, text=t, size=11, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
        callout(s, 0.40, y + 0.78, 9.2, 0.5, "circle-check", ok, size=12, fill=GREEN_LT, color=GREEN_DK, icolor="#16A55C")
        return s
    h = 4.28; w = h * ar
    if w > 6.3: w = 6.3; h = w / ar
    shot(s, img, 0.40, 1.12, w + 0.08, h + 0.08)
    rx = 0.40 + w + 0.3; rw = 9.6 - rx
    label(s, rx, 1.14, rw, "WHAT TO CHECK")
    for i, (icn, t) in enumerate(checks):
        y = 1.48 + i * 0.86
        icon_tile(s, icn, rx, y, 0.5)
        box(s, rx + 0.62, y - 0.06, rw - 0.62, 0.66, text=t, size=11.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    b_ = box(s, rx, 4.18, rw, 1.2, fill=GREEN_LT, line=GREEN, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1,
             anchor=MSO_ANCHOR.MIDDLE, ml=0.14, mr=0.12)
    para(b_, "PASS WHEN", size=10, color=GREEN_DK, bold=True, first=True, space_after=2)
    para(b_, ok, size=12, color=GREEN_DK, bold=True, space_after=0)
    return s


# ============================================================ 2. TOC
s = std("Table of Contents", "Airtel DSPM PoC plan", """
Six parts. Each tile links to its first slide.
1. Scope: which Airtel data stores the PoC covers, which need work, which sit outside. Slide 3.
2. Architecture and prerequisites: the draft layout from the scoping call and what Airtel provides. Slides 4 and 5.
3. Onboarding: five steps from token to first findings, then two console screens. Slides 6 to 8.
4. Use cases: six tests with pass conditions, then one full screen per use case. Slides 9 to 15.
5. Timeline: two weeks from Wednesday 7 October. Slide 16.
6. Resources: help pages, platform page and the micro deck. Slide 17.
""")
toc = [("list-check", "Scope", "What is in and out", "Slide 3", 3),
       ("topology-star-3", "Architecture", "Layout and prerequisites", "Slides 4 and 5", 4),
       ("plug-connected", "Onboarding", "Five steps, two screens", "Slides 6 to 8", 6),
       ("target", "Use Cases", "Six tests that close the PoC", "Slides 9 to 15", 9),
       ("calendar-stats", "Timeline", "7 to 21 October", "Slide 16", 16),
       ("book", "Resources", "Docs, platform, micro deck", "Slide 17", 17)]
toc_tiles = []
for i, (icn, h, sub, rng, tgt) in enumerate(toc):
    x = 0.40 + (i % 3) * 3.1
    y = 1.22 + (i // 3) * 2.0
    t = box(s, x, y, 2.96, 1.82, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    toc_tiles.append((t, tgt))
    icon_tile(s, icn, x + 0.18, y + 0.2, 0.74)
    box(s, x + 1.9, y + 0.16, 0.9, 0.6, text=f"0{i+1}", size=28, color=LAV, bold=True, align=PP_ALIGN.RIGHT)
    box(s, x + 0.18, y + 1.0, 2.7, 0.36, text=h, size=16, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.18, y + 1.34, 2.7, 0.26, text=sub, size=10.5, color=MUTE)
    box(s, x + 0.18, y + 1.56, 2.7, 0.24, text=rng, size=9.5, color=PRIMARY, bold=True)

# ============================================================ 3. scope
s = std("The PoC Scans Seven Data Store Types on Airtel's OpenStack", "Scope", """
Airtel runs OpenStack only. OpenShift came up in earlier notes by mistake. Neither Rahul nor Ayush recall it being discussed, so it is removed.
In scope, from the scoping call:
VM file systems on OpenStack.
Structured databases: PostgreSQL 16 and later (Airtel runs 16.x, which is compatible), MySQL, MariaDB, SQL Server.
Document database: MongoDB.
SaaS: Google Drive. Support already exists.
The connector works at the database level. Any cloud or on-prem host that runs a supported database version is covered.
Needs work: NetApp ONTAP S3 buckets. Airtel wants them scanned. This needs a custom connector. Ayush said it can be built but gave no date.
Out of scope: AWS and other public cloud assets, because Airtel is on-prem. SharePoint and Office 365 PI scanning: Airtel asked, AccuKnox has no PI scanning for Microsoft 365 today. Microsoft support covers compliance use cases only.
Why this matters to Airtel: NBFC tenants need PI data discovery and protection to meet RBI guidelines.
""")
label(s, 0.40, 1.14, 5.8, "IN SCOPE", color=GREEN_DK)
grid = [("si-openstack", "VM files", "On OpenStack"), ("postgresql-original", "PostgreSQL", "Version 16 and later"),
        ("mysql-original", "MySQL", "Self-managed"), ("mariadb-original", "MariaDB", "Self-managed"),
        ("microsoftsqlserver-original", "SQL Server", "Self-managed"), ("mongodb-original", "MongoDB", "Document store"),
        ("si-googledrive", "Google Drive", "SaaS, read-only"), ("database-search", "Any host", "Same DB versions")]
for i, (lg, h, sub) in enumerate(grid):
    x = 0.40 + (i % 4) * 1.47
    y = 1.44 + (i // 4) * 1.5
    box(s, x, y, 1.37, 1.38, fill=WHITE, line=GREY_BD, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    icon_img(s, lg, x + 0.43, y + 0.14, 0.5, color="#0046FF" if lg == "database-search" else None)
    box(s, x, y + 0.7, 1.37, 0.3, text=h, size=12, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    box(s, x, y + 0.98, 1.37, 0.28, text=sub, size=9.5, color=MUTE, align=PP_ALIGN.CENTER)
label(s, 6.4, 1.14, 3.2, "NEEDS A CONNECTOR", color=RED)
todo_panel(s, 6.4, 1.44, 3.2, 1.0, "NetApp ONTAP S3", "Custom connector. Ayush to confirm the build date.", size=10.5)
label(s, 6.4, 2.58, 3.2, "OUT OF SCOPE", color=MUTE)
for i, (lg, h, sub) in enumerate([("cloud-off", "Public cloud assets", "Airtel is on-prem"),
                                  ("si-microsoftsharepoint", "SharePoint and M365 PI", "No PI scanning today")]):
    y = 2.88 + i * 0.7
    box(s, 6.4, y, 3.2, 0.6, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    icon_img(s, lg, 6.5, y + 0.1, 0.4, color="#5A637D")
    box(s, 7.0, y + 0.02, 2.55, 0.3, text=h, size=11, color=NAVY, bold=True, anchor=MSO_ANCHOR.BOTTOM)
    box(s, 7.0, y + 0.31, 2.55, 0.26, text=sub, size=9.5, color=MUTE)
callout(s, 0.40, 4.5, 9.2, 0.6, "shield-check", "Goal: prove PI discovery on-prem, as RBI expects for Airtel's NBFC tenants.", size=12.5)

# ============================================================ 4. architecture
s = std("The DSPM Scanner and Control Plane Both Run Inside Airtel", "PoC architecture, draft from the scoping call", """
Draft layout from the scoping call. Not a finalized deployment design. Adapt Ayush's existing diagram, shared on Slack, before sending.
Boundary: Airtel on-prem, private cloud.
Inside OpenStack: VM file systems, the supported databases (PostgreSQL 16+, MySQL, MariaDB, SQL Server, MongoDB), and NetApp ONTAP S3 buckets.
NetApp ONTAP S3 needs a custom connector. Its readiness is not confirmed.
The AccuKnox DSPM scanner runs as a VM for this PoC. VM is the chosen path. Kubernetes is the other option. A third option is deferred to a later phase.
From the help docs: the scanner has read-only access, no inbound connections, and sends one findings file per data store.
AccuKnox control plane: in Airtel's environment, as Rahul requested. It holds the AccuKnox console.
Network: outbound HTTPS on port 443 from the scanner to the AccuKnox console.
Container registry: it appears in Ayush's existing diagram. The call did not settle where it sits in the VM-only version, so its placement needs confirmation.
Google Drive is SaaS, so the scanner reaches it through the Drive API with the read-only Drive scope.
""")
native.architecture(s, 0.40, 1.06)
todo_panel(s, 0.40, 4.98, 9.2, 0.52, "Draft from the scoping call.", "Adapt Ayush's diagram and confirm the registry placement before sending.", size=10.5)

# ============================================================ 5. prerequisites
s = std("Airtel Provides 2 Nodes With 16 vCPU and 64 GB RAM Each", "Prerequisites discussed on the scoping call", """
Discussed on the scoping call.
On-prem compute: Rahul specified 2 nodes, each with 16 vCPUs and 64 GB RAM. He described it as an on-prem Kubernetes cluster prerequisite.
Network: outbound access on port 443 to the AccuKnox console.
Deployment mode needs confirmation. Ayush later said the PoC uses VM deployment only. The team did not reconcile that with the 2-node Kubernetes prerequisite. Do not present the cluster spec as the confirmed VM requirement until this is clarified.
Also needed, from the onboarding guide (help.accuknox.com/getting-started/dspm-onboarding/):
Scanner VM: Linux with Docker or Podman, about 20 GB free disk. 4 vCPU and 8 GB RAM scan one data store at a time. 8 vCPU and 32 GB RAM scan four in parallel.
Database ports open from the scanner to the data subnets. No inbound connections.
A read-only login per database, for example pg_read_all_data on PostgreSQL or db_datareader on SQL Server, and a read-only MongoDB user.
Google Drive: a GCP service account with domain-wide delegation and the single read-only Drive scope.
Console: an artifact token and one label per scanner instance.
""")
stats = [("server-cog", "2 nodes", "On-prem compute"), ("cpu", "16 vCPU", "Per node"),
         ("server", "64 GB RAM", "Per node"), ("network", "Port 443", "Outbound to the console")]
for i, (icn, n, lab) in enumerate(stats):
    x = 0.40 + i * 2.33
    box(s, x, 1.42, 2.2, 1.24, fill=WHITE, line=PRIMARY, line_w=1.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    icon_tile(s, icn, x + 0.14, 1.56, 0.5)
    box(s, x + 0.72, 1.5, 1.46, 0.62, text=n, size=19, color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0, wrap=False)
    box(s, x + 0.14, 2.14, 1.98, 0.42, text=lab, size=11, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
todo_panel(s, 0.40, 2.8, 9.2, 0.78, "Deployment mode needs confirmation",
           "Rahul gave this spec as a 2-node Kubernetes cluster. Ayush set VM only for the PoC. Confirm before sending.", size=10.5)
label(s, 0.40, 3.72, 9.2, "ALSO NEEDED, FROM THE ONBOARDING GUIDE", color=MUTE)
more = [("server", "Scanner VM", "Linux, Docker or Podman"), ("database", "DB logins", "Read-only, one per DB"),
        ("si-googledrive", "Drive access", "Read-only account"), ("key", "Console token", "Token and one label")]
for i, (icn, h, sub) in enumerate(more):
    x = 0.40 + i * 2.33
    box(s, x, 4.0, 2.2, 0.82, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    icon_img(s, icn, x + 0.12, 4.18, 0.44, color=None if icn.startswith("si-") else "#11206D")
    box(s, x + 0.66, 4.04, 1.5, 0.36, text=h, size=11.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.BOTTOM, ml=0)
    box(s, x + 0.66, 4.4, 1.5, 0.38, text=sub, size=10, color=MUTE, ml=0)
callout(s, 0.40, 4.96, 9.2, 0.46, "clock", "Ready these by Wednesday 7 October. Deployment then takes 2 days.", size=12)

# ============================================================ 6. onboarding steps
s = std("Five Steps Take a Data Store From Zero to First Findings", "Onboarding", """
Step 1, token and label. In the AccuKnox console go to Settings, Tokens and create an artifact token. Create one label per scanner instance.
Step 2, scanner VM. Create a Linux VM in a private subnet on OpenStack. Allow no inbound rules. Install Docker, then pull the scanner image.
Step 3, read-only grants. Apply the grant for each data store. Every grant is read-only.
Step 4, configure. Copy the deployment kit to the VM. Set the console URL, the artifact token and the country packs (IN for Aadhaar, PAN and GST) in the shared settings file. Add one instance file per data store.
Step 5, install and first scan. Run the installer once. It creates a nightly timer per instance. Start one instance by hand and follow its log until the upload succeeds. Findings appear in the console within minutes.
The next two slides show the console screens. Ayush is sending the Airtel OpenStack versions.
Source: Onboard the DSPM Scanner.
""")
steps = [("key", "Token and label", "Create an artifact token and one label per scanner"),
         ("server", "Scanner VM", "Linux VM on OpenStack, no inbound rules"),
         ("lock-access", "Read-only grants", "One read-only login per data store"),
         ("settings", "Configure", "Console URL, token, India country pack"),
         ("player-play", "First scan", "Run the installer, watch the first upload")]
for i, (icn, h, sub) in enumerate(steps):
    x = 0.40 + i * 1.86
    last = i == 4
    box(s, x, 1.18, 1.72, 2.9, fill=GREEN_LT if last else WHITE, line=GREEN if last else GREY_BD,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    icon_tile(s, icn, x + 0.56, 1.36, 0.6, bg=GREEN if last else PRIMARY)
    box(s, x, 2.06, 1.72, 0.3, text=f"STEP {i+1}", size=10, color=GREEN_DK if last else PRIMARY, bold=True, align=PP_ALIGN.CENTER)
    box(s, x + 0.08, 2.36, 1.56, 0.5, text=h, size=13, color=NAVY, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x + 0.1, 2.9, 1.52, 1.1, text=sub, size=11, color=MUTE, align=PP_ALIGN.CENTER)
    if i < 4:
        arrow(s, x + 1.72, 2.52, w=0.14, h=0.26, size=12)
callout(s, 0.40, 4.3, 9.2, 0.56, "eye", "The next two slides show the console screens at full size.", size=12.5)

# ============================================================ 7-8. onboarding screens
img4 = crop(os.path.join(DL, "image (4).png"), (430, 40, 1390, 350), "onboard_account")
img3 = crop(os.path.join(DL, "image (3).png"), (240, 30, 1000, 770), "data_sources")
full_shot("Onboarding Starts in Cloud Accounts With Onboard Account", "Onboarding screen 1 of 2", img4,
          [("settings", "Settings, then Cloud Accounts"), ("plug-connected", "Click Onboard Account"),
           ("cloud", "Pick the cloud type")],
          "Airtel's OpenStack shows as a connected account.", """
Console path: Settings, Cloud Accounts, Onboard Account, Select Cloud Type.
The list shows each onboarded account with its configured scans, such as CSPM and DSPM, and its connection status.
This screen is from the current build. Its Private Cloud tile names Red Hat OpenShift and Nutanix. Airtel runs OpenStack only, so Ayush is sending the OpenStack version of this screen.
Source: image (4).png, shared for this deck.
""")
full_shot("Each Data Source Gets a Read-Only Connection and a Scanner", "Onboarding screen 2 of 2", img3,
          [("database", "Add each data source"), ("key", "Create the access token"),
           ("server", "Deploy the DSPM engine")],
          "The engine reports its first scan to the console.", """
Step 4 of 4 in the onboarding wizard: Data Sources.
Top: add data sources. Each source has its own connection settings.
Bottom: deploy the DSPM engine. Create an access token, download the deployment scripts, run the script, then add the engine instance IDs so AccuKnox can tell whether the engine runs.
This screen shows the AWS flow. On Airtel, the engine is the scanner VM on OpenStack. Ayush is sending the OpenStack screens.
Source: image (3).png, shared for this deck.
""")

# ============================================================ 9. use cases summary
s = std("Six Use Cases Decide Whether the PoC Passes", "Use cases and success criteria", """
Each use case is a success criterion. The PoC passes when all six pass. Each tile links to its full-size screen.
1. Find every data store. Each in-scope store appears as an asset, with total risks, sensitive records by data type, tags, file types and security configuration.
2. Find Indian PI. The India country pack covers Aadhaar, PAN and GST, each checked with its public check-digit algorithm. Seed test records in PostgreSQL, MySQL, MongoDB and a VM file system before execution starts.
3. Prove each finding. The evidence tab lists each file behind the finding, its type, path and the data types found. The console masks each value to its last four characters.
4. See risk on one view. Data alerts by severity, findings trends, the top 10 data findings, top assets and accounts with findings, and open tickets.
5. Map to regulation. Filter findings by India DPDP Act 2023 and SPDI Rules 2011 (17 data classes). Airtel shares its RBI guidelines so AccuKnox can map them too. The scanner shows where regulated data sits. It does not assess the controls around it.
6. Fix and close. Create Ticket raises a ticket. Severity sets the SLA, 10 days for a Critical finding. After the data is masked, moved or deleted, Last detected stops advancing.
Source: DSPM overview, Product Tour and Compliance Mapping. Onboarding guide, Review Findings.
""")
UCS = [("database-search", "Find every data store", "Each store shows as an asset"),
       ("id", "Find Indian PI", "Seeded Aadhaar, PAN found"),
       ("file-search", "Prove each finding", "Path and data type shown"),
       ("chart-bar", "See risk on one view", "Alerts by severity, top assets"),
       ("gavel", "Map to regulation", "DPDP filter lists the assets"),
       ("ticket", "Fix and close", "One Critical finding ticketed")]
uc_tiles = []
for i, (icn, h, ok) in enumerate(UCS):
    x = 0.40 + (i % 3) * 3.1
    y = 1.2 + (i // 3) * 1.98
    t = box(s, x, y, 2.96, 1.82, fill=WHITE, line=GREY_BD, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    uc_tiles.append((t, 10 + i))
    icon_tile(s, icn, x + 0.18, y + 0.2, 0.62)
    box(s, x + 1.9, y + 0.14, 0.9, 0.6, text=f"0{i+1}", size=26, color=LAV, bold=True, align=PP_ALIGN.RIGHT)
    box(s, x + 0.18, y + 0.9, 2.7, 0.36, text=h, size=14.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    icon_img(s, "circle-check", x + 0.18, y + 1.32, 0.26, color="#16A55C")
    box(s, x + 0.5, y + 1.28, 2.4, 0.34, text=ok, size=11, color=GREEN_DK, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.18, y + 1.56, 2.7, 0.24, text=f"Screen on slide {10 + i}", size=9.5, color=PRIMARY, bold=True)

# ============================================================ 10-15. use case screens
P = os.path.join(HELP, "preview")
UCF = [
 ("Use Case 1 Shows Every Data Store as an Asset With Its Risk", "dspm-proto-asset-overview.png", (0, 0, 1053, 1000),
  [("chart-bar", "Total risks and sensitive records"), ("id", "Sensitive data by type, such as Aadhaar"), ("lock", "Security configuration")],
  "Every in-scope Airtel store shows as an asset.", U_OVERVIEW + "#product-tour",
  "Asset overview. Total risks, sensitive records by data type, tags, file types, and security configuration such as encryption and public access. Source: DSPM overview, Product Tour, Assets tab."),
 ("Use Case 2 Finds Indian PI File by File", "dspm-proto-asset-evidence.png", (0, 0, 1420, 943),
  [("file-search", "Each file behind the asset"), ("folder", "File type and path"), ("id", "Data types found per file")],
  "Seeded Aadhaar and PAN show up in each store type.", U_OVERVIEW + "#what-the-scanner-detects",
  "Asset evidence. The India country pack covers Aadhaar, PAN and GST, each checked with its public check-digit algorithm. Seed test records in PostgreSQL, MySQL, MongoDB and a VM file system before execution starts. Source: DSPM overview, What the Scanner Detects."),
 ("Use Case 3 Proves Each Finding With Its Evidence", "dspm-proto-finding-evidence.png", (0, 0, 1420, 1049),
  [("alert-triangle", "Severity, status, occurrence"), ("file-search", "Evidence files and data types"), ("ticket", "Create Ticket and Ask AI")],
  "Each finding shows where the data sits.", U_OVERVIEW + "#data-privacy",
  "Finding evidence. Each file behind the finding, with its type and path, and the sensitive data types found in it. The Data Matches tab shows values masked to their last four characters. Source: DSPM overview, Product Tour, Evidence tab, and Data Privacy."),
 ("Use Case 4 Puts Data Risk on One Dashboard", "dspm-proto-dashboard-risk.png", (0, 0, 1060, 670),
  [("alert-triangle", "Data alerts by severity"), ("trending-up", "Findings trend over time"), ("list-numbers", "Top 10 data findings")],
  "Airtel's stores show on the risk view.", U_OVERVIEW + "#product-tour",
  "Risk overview. Data alerts by severity, findings trends over time, the top 10 data findings, the assets and accounts with the most findings, open tickets, and data distribution by store type. Source: DSPM overview, Product Tour, Risk tab."),
 ("Use Case 5 Maps Each Finding to Its Regulation", "dspm-proto-finding-overview.png", (0, 560, 1420, 1364),
  [("file-text", "Issue description and risk"), ("gavel", "Compliance frameworks"), ("sparkles", "Recommendation to fix")],
  "Findings filter by India DPDP Act 2023.", U_OVERVIEW + "#compliance-mapping",
  "Finding overview with compliance frameworks and the recommendation. 282 of the 283 data classes carry the regulation clauses they fall under. India DPDP Act 2023 and SPDI Rules 2011 cover 17 data classes. Airtel shares its RBI guidelines so AccuKnox can map them too. The scanner shows where regulated data sits. It does not assess the controls around it. Source: DSPM overview, Compliance Mapping."),
 ("Use Case 6 Turns a Finding Into a Ticket With an SLA", "dspm-finding-detail.png", (0, 0, 1792, 1180),
  [("clock", "Age, severity, SLA"), ("ticket", "Create Ticket, Ask AI"), ("map-2", "Status and location")],
  "One Critical finding is ticketed and closed.", U_ONBOARD + "#review-findings",
  "Finding detail. Callout 1: age, severity, SLA and sensitivity. The SLA is 10 days for a Critical finding. Callout 2: six tabs. Callout 3: Create Ticket and Ask AI. Callout 4: Status and Ignored. Callout 5: Location. After the data is masked, moved or deleted, Last detected stops advancing. Source: Onboard the DSPM Scanner, Review Findings."),
]
for i, (t, f, cb, checks, ok, url, nt) in enumerate(UCF):
    src = os.path.join(HELP, f) if f == "dspm-finding-detail.png" else os.path.join(P, f)
    img = crop(src, cb, f"ucfull_{i+1}")
    full_shot(t, f"Use case {i+1} of 6", img, checks, ok, nt + "\nHelp page: " + url)

# ============================================================ 8. timeline
s = std("Two Weeks Run From 7 October to Readout on 21 October", "Timeline", """
Proposed plan. Working days only, weekends skipped.
Wednesday 7 and Thursday 8 October: on-prem deployment of the control plane and the scanner VM. Two days, per Rahul.
Friday 9 and Monday 12 October: onboarding. Read-only grants, scanner configuration, first scan per data store. First findings land in the console.
Tuesday 13 to Monday 19 October: use case execution. The six use cases on slide 9, with a daily check-in.
Tuesday 20 and Wednesday 21 October: executive report, readout and closure. Go or no go on 21 October.
Dependencies: the VMs, the outbound 443 rule and the read-only logins on slide 5 must be ready on 7 October. NetApp ONTAP S3 joins only if the custom connector lands inside the window.
Airtel has not committed to these dates yet. Confirm at kickoff.
""")
native.timeline(s, 0.40, 1.16)
callout(s, 0.40, 4.72, 9.2, 0.56, "calendar-event", "Dates are a proposal. Airtel confirms them at kickoff on 7 October.", size=12.5)

# ============================================================ 9. resources
s = std("Six Links Answer Most Questions During the PoC", "Resources", """
Every link opens the live page.
DSPM overview: what the scanner covers, supported data stores, the 283 data classes, compliance mapping and data privacy.
Onboard the DSPM scanner: prerequisites, read-only grants per data store, install, first scan and how to review findings.
DSPM platform page on accuknox.com.
AccuKnox DSPM micro deck: the short product deck, with the Airtel requirements mapped to AccuKnox.
Run the console on-premises: the section of the overview that explains the on-prem and air-gapped console.
Create tokens: how to create the artifact token the scanner uses.
""")
res = [("book", "DSPM overview", "Coverage, detectors, privacy", U_OVERVIEW),
       ("list-numbers", "Onboarding guide", "Prerequisites to first scan", U_ONBOARD),
       ("world", "DSPM platform page", "accuknox.com/platform/dspm", U_PLATFORM),
       ("presentation", "DSPM micro deck", "Airtel needs mapped to AccuKnox", U_MICRO),
       ("building", "On-prem console", "Nothing leaves your boundary", U_ONPREM),
       ("key", "Create tokens", "The scanner's artifact token", U_TOKENS)]
for i, (icn, h, sub, url) in enumerate(res):
    x = 0.40 + (i % 3) * 3.1
    y = 1.2 + (i // 3) * 1.6
    box(s, x, y, 2.96, 1.42, fill=WHITE, line=GREY_BD, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    icon_tile(s, icn if icn != "presentation" else "chart-bar", x + 0.16, y + 0.18, 0.56)
    icon_img(s, "external-link", x + 2.56, y + 0.18, 0.26, color="#0046FF")
    t = box(s, x + 0.16, y + 0.82, 2.7, 0.32, text=h, size=14, color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    link(t, url)
    box(s, x + 0.16, y + 1.1, 2.7, 0.28, text=sub, size=10.5, color=MUTE)
callout(s, 0.40, 4.5, 9.2, 0.56, "message-chatbot", "Questions during the PoC go to support@accuknox.com.", size=12.5)

# ============================================================ 10. closing
closing_slide(prs)

# TOC tiles jump to their slides
all_slides = list(prs.slides)
for t, tgt in toc_tiles + uc_tiles:
    t.click_action.target_slide = all_slides[tgt - 1]

prs.save(OUT)
print(OUT, len(prs.slides))
