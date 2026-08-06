"""Build the AccuKnox BSides Bangalore 2026 partner brief as a 3-page A4 PDF.

Emits branded HTML with all imagery inlined as data URIs, then prints to PDF with
headless Edge. Source material: the July 15 2026 press release, the AI-SPM buyer's
guide blog, and the two BSides speaker sessions.
"""
import base64
import mimetypes
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(REPO, "output", "bsides")
IMG = os.path.join(WORK, "img")
HTML_OUT = os.path.join(WORK, "AccuKnox_BSides_Bangalore_2026_Partner_Brief.html")
PDF_OUT = os.path.join(REPO, "output", "AccuKnox_BSides_Bangalore_2026_Partner_Brief.pdf")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

NAVY = "#11206D"
DEEP = "#0000C8"
BLUE = "#0046FF"
SEC = "#6464FF"
RED = "#C80019"
GREY_BG = "#EEF0F6"
GREY_BD = "#C4CCDE"


def uri(path):
    mt = mimetypes.guess_type(path)[0] or "application/octet-stream"
    if path.lower().endswith(".svg"):
        mt = "image/svg+xml"
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mt, base64.b64encode(f.read()).decode())


A = {
    "logo_dark": uri(os.path.join(REPO, "assets", "logos", "accuknox-logo-dark-bg.png")),
    "logo_light": uri(os.path.join(REPO, "assets", "logos", "accuknox-logo-light-bg.png")),
    "emblem": uri(os.path.join(REPO, "assets", "logos", "accuknox-emblem.png")),
    "award": uri(os.path.join(IMG, "bsides-AI-startup-award-1024x640.png")),
    "team": uri(os.path.join(IMG, "PR_BSides_Bangalore.png")),
    "rahul": uri(os.path.join(IMG, "bsides-rahul-banner.png")),
    "hero": uri(os.path.join(IMG, "AI-Security-Hero.svg")),
    "dash": uri(os.path.join(IMG, "AI-Security-form.png")),
    "emergex": uri(os.path.join(IMG, "emergex-bsides.png")),
}


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { font-family: 'Space Grotesk', 'Inter', 'Segoe UI', sans-serif;
  color: #1A1D2E; -webkit-print-color-adjust: exact; print-color-adjust: exact; }

.page { position: relative; width: 210mm; height: 297mm; overflow: hidden;
  page-break-after: always; background: #fff; }
.page:last-child { page-break-after: auto; }

/* ---------- page 1, dark ---------- */
.dark { background:
    radial-gradient(760px 420px at 78%% -8%%, rgba(100,100,255,.42), transparent 68%%),
    radial-gradient(620px 460px at -6%% 96%%, rgba(200,0,25,.24), transparent 66%%),
    linear-gradient(158deg, #0B1240 0%%, %(NAVY)s 46%%, #0A0E33 100%%);
  color: #fff; }
.grid { position: absolute; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,.05) 1px, transparent 1px);
  background-size: 26px 26px; }
.p1 { position: relative; padding: 15mm 14mm 12mm 14mm; height: 100%%; }
.p1 .logo { height: 8.6mm; }
.rule { height: 3px; width: 46mm; border-radius: 3px; margin: 7mm 0 5mm;
  background: linear-gradient(90deg, %(RED)s, %(SEC)s 55%%, transparent); }
h1 { font-size: 26pt; line-height: 1.1; font-weight: 700; letter-spacing: -.7px; }
h1 em { font-style: normal; color: #9BB4FF; }
.lede { margin-top: 5mm; font-size: 10.4pt; line-height: 1.6; color: #D6DEF8;
  max-width: 172mm; }
.lede b { color: #fff; font-weight: 600; }

.hero-wrap { position: relative; margin-top: 7mm; height: 93mm; }
.hero-shot { width: 148mm; border-radius: 6mm; display: block;
  box-shadow: 0 14px 46px rgba(0,0,0,.55); border: 1px solid rgba(255,255,255,.14); }
.float-team { position: absolute; right: 0; bottom: 0; width: 62mm;
  border-radius: 4.5mm; border: 2.4px solid rgba(255,255,255,.9); display: block;
  box-shadow: 0 12px 34px rgba(0,0,0,.6); }
.chip-emergex { position: absolute; left: 124mm; top: -5mm; width: 38mm;
  background: #0A0E33; border: 1px solid rgba(155,180,255,.4); border-radius: 3.4mm;
  padding: 4mm 5mm; box-shadow: 0 10px 28px rgba(0,0,0,.6); text-align: center; }
.chip-emergex img { width: 100%%; display: block; }
.chip-emergex span { display: block; margin-top: 2mm; font-size: 6.4pt;
  color: #9BB4FF; letter-spacing: .4px; }

.qdark { margin-top: 6mm; border-radius: 4mm; padding: 4.6mm 5.4mm;
  background: rgba(255,255,255,.06); border: 1px solid rgba(155,180,255,.26);
  border-left: 3.4px solid %(SEC)s; }
.qdark p { font-size: 9.2pt; line-height: 1.55; color: #E2E8FA; font-style: italic; }
.qdark .by { margin-top: 2.4mm; font-size: 7.8pt; font-weight: 700; color: #9BB4FF;
  font-style: normal; }

.stats { display: flex; gap: 3.4mm; margin-top: 7mm; }
.stat { flex: 1; background: rgba(255,255,255,.07); border: 1px solid rgba(155,180,255,.28);
  border-radius: 3.4mm; padding: 4mm 4mm 4.4mm; }
.stat .n { font-size: 19pt; font-weight: 700; color: #fff; line-height: 1; }
.stat .n small { font-size: 10pt; font-weight: 600; color: #9BB4FF; }
.stat .l { margin-top: 2.2mm; font-size: 7.6pt; line-height: 1.35; color: #B9C6EE;
  letter-spacing: .2px; }
.p1foot { position: absolute; left: 14mm; right: 14mm; bottom: 8mm; font-size: 7.6pt;
  color: #8FA2D8; display: flex; justify-content: space-between;
  border-top: 1px solid rgba(155,180,255,.22); padding-top: 3mm; }

/* ---------- light pages ---------- */
.p { padding: 13mm 14mm 14mm 14mm; height: 100%%; position: relative; }
.head { display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1.6px solid %(GREY_BD)s; padding-bottom: 3mm; margin-bottom: 7mm; }
.head img { height: 6.2mm; }
.head span { font-size: 7.6pt; color: #6A749A; letter-spacing: .6px; }
h2 { font-size: 18.5pt; font-weight: 700; color: %(NAVY)s; letter-spacing: -.5px;
  line-height: 1.14; }
h2 .accent { color: %(BLUE)s; }
.sub { margin-top: 3mm; font-size: 10pt; line-height: 1.6; color: #3A4064; }
.sub b { color: %(NAVY)s; }

.diagram { margin: 5.5mm auto 0; width: 162mm; border: 1.4px solid %(GREY_BD)s;
  border-radius: 4.5mm; background: #fff; padding: 3.2mm;
  box-shadow: 0 6px 20px rgba(17,32,109,.09); }
.diagram img { width: 100%%; display: block; }
.cap { margin-top: 2.2mm; font-size: 7.4pt; color: #6A749A; text-align: center; }

.items { margin-top: 5.5mm; }
.item { position: relative; padding: 0 0 0 9mm; margin-bottom: 3.6mm; }
.item:before { content: ''; position: absolute; left: 0; top: 1.2mm; width: 2.6mm;
  height: 2.6mm; border-radius: 50%%; background: %(BLUE)s;
  box-shadow: 0 0 0 2.2mm rgba(0,70,255,.12); }
.item h3 { font-size: 10.4pt; font-weight: 700; color: %(NAVY)s; margin-bottom: 1.4mm; }
.item p { font-size: 9.2pt; line-height: 1.56; color: #3A4064; }
.item p b { color: %(NAVY)s; }

.band { margin-top: 5mm; background: %(GREY_BG)s; border-left: 3.4px solid %(BLUE)s;
  border-radius: 0 3mm 3mm 0; padding: 4.4mm 5mm; font-size: 9pt; line-height: 1.55;
  color: #2B3157; }
.band b { color: %(NAVY)s; }

.shot-row { position: relative; margin-top: 6mm; height: 62mm; }
.shot { position: absolute; left: 0; top: 0; width: 118mm; border-radius: 4mm;
  border: 1.2px solid %(GREY_BD)s; box-shadow: 0 10px 30px rgba(17,32,109,.16);
  display: block; }
.shot-note { position: absolute; right: 0; top: 6mm; width: 58mm; background: %(NAVY)s;
  color: #fff; border-radius: 4mm; padding: 5mm; box-shadow: 0 10px 28px rgba(17,32,109,.3); }
.shot-note h4 { font-size: 9.6pt; font-weight: 700; margin-bottom: 2.2mm; }
.shot-note p { font-size: 8.4pt; line-height: 1.5; color: #C9D4F5; }

/* talks */
.trow { position: relative; height: 66mm; margin-top: 0; }
.banner { width: 106mm; border-radius: 4.2mm; display: block;
  box-shadow: 0 10px 30px rgba(17,32,109,.26); }
.float-dash { position: absolute; left: 98mm; top: 23mm; width: 70mm; border-radius: 3.4mm;
  border: 2.4px solid #fff; display: block; box-shadow: 0 12px 30px rgba(17,32,109,.3); }
.dashcap { position: absolute; right: 0; top: 24mm; width: 66mm; font-size: 7.4pt;
  line-height: 1.4; color: %(NAVY)s; font-weight: 600; }
.talks { display: flex; gap: 4mm; margin-top: 2mm; }
.talk { flex: 1; border: 1.4px solid %(GREY_BD)s; border-radius: 4mm; padding: 3.8mm; }
.talk .who { font-size: 9.4pt; font-weight: 700; color: %(NAVY)s; }
.talk .role { font-size: 7.6pt; color: %(BLUE)s; margin-top: .8mm; letter-spacing: .3px; }
.talk .t { margin-top: 2.6mm; font-size: 9.2pt; font-weight: 600; color: #1A1D2E;
  line-height: 1.32; }
.talk .d { margin-top: 2.2mm; font-size: 8.4pt; line-height: 1.5; color: #4A517A; }

.quote { margin-top: 5.5mm; border-radius: 4mm; padding: 5mm 5.5mm;
  background: linear-gradient(120deg, rgba(0,70,255,.07), rgba(100,100,255,.11));
  border: 1px solid rgba(0,70,255,.18); }
.quote p { font-size: 9.4pt; line-height: 1.56; color: %(NAVY)s; font-style: italic; }
.quote .by { margin-top: 2.6mm; font-size: 8pt; font-weight: 700; color: %(BLUE)s;
  font-style: normal; }

.closer { position: absolute; left: 14mm; right: 14mm; bottom: 12mm; color: #fff;
  border-radius: 5mm; padding: 5.4mm 6.2mm; background:
    radial-gradient(420px 200px at 92%% 10%%, rgba(100,100,255,.5), transparent 70%%),
    linear-gradient(120deg, %(NAVY)s, #0A0E33); }
.closer h4 { font-size: 12pt; font-weight: 700; margin-bottom: 2.8mm; }
.closer p { font-size: 9.2pt; line-height: 1.58; color: #D6DEF8; }
.closer .meta { margin-top: 4mm; padding-top: 3.2mm; font-size: 7.8pt; color: #9BB4FF;
  border-top: 1px solid rgba(155,180,255,.26); display: flex;
  justify-content: space-between; align-items: center; }
.closer .meta img { height: 5.6mm; }
.pnum { position: absolute; right: 14mm; bottom: 6mm; font-size: 7.4pt; color: #8A93B8; }
""" % {"NAVY": NAVY, "BLUE": BLUE, "SEC": SEC, "RED": RED, "GREY_BG": GREY_BG,
       "GREY_BD": GREY_BD}


PAGE1 = """
<div class="page dark"><div class="grid"></div><div class="p1">
  <img class="logo" src="%(logo_dark)s" alt="AccuKnox">
  <div class="rule"></div>
  <h1>AccuKnox wins the #1 AI Startup Award<br>at Security BSides Bangalore <em>2026</em></h1>
  <p class="lede">AccuKnox took first place in <b>EmergeX</b>, the startup competition at
    Security BSides Bangalore 2026, judged in front of practitioners and security leaders
    at the Annual Cyber Security Conference in Whitefield. <b>It is the second year in a
    row</b> that AccuKnox has topped the category. What earned it was live enforcement, a
    booth running real prompt injection and agentic AI attacks against a working instance
    while attendees watched.</p>

  <div class="hero-wrap">
    <img class="hero-shot" src="%(award)s" alt="AccuKnox wins AI Startup Award">
    <div class="chip-emergex"><img src="%(emergex)s" alt="EmergeX BSides Bangalore">
      <span>STARTUP COMPETITION</span></div>
    <img class="float-team" src="%(team)s" alt="AccuKnox team receiving the EmergeX award">
  </div>

  <div class="stats">
    <div class="stat"><div class="n">#1</div>
      <div class="l">EmergeX startup award, BSides Bangalore ACSC 2026</div></div>
    <div class="stat"><div class="n">2<small> yrs</small></div>
      <div class="l">Back to back wins, 2025 and 2026</div></div>
    <div class="stat"><div class="n">2</div>
      <div class="l">Speaker sessions on the main agenda</div></div>
    <div class="stat"><div class="n">8</div>
      <div class="l">AI security modules integrated into a single policy engine</div></div>
  </div>

  <div class="qdark">
    <p>&ldquo;The depth of the AccuKnox Agentic AI Security platform stood out even more
      than the first time around. Back to back wins at Security BSides Bangalore do not
      happen by chance. They happen when a team keeps building instead of pausing to
      celebrate the last trophy.&rdquo;</p>
    <div class="by">Sujatha Yakasiri, Founder, Security BSides Bangalore</div>
  </div>

  <div class="p1foot"><span>Security BSides Bangalore ACSC 2026, Sheraton Grand Whitefield,
    July 9 2026</span><span>Partner and customer brief</span></div>
</div></div>
""" % A


PAGE2 = """
<div class="page"><div class="p">
  <div class="head"><img src="%(logo_light)s" alt="AccuKnox">
    <span>WHAT WENT IN FRONT OF THE JUDGES</span></div>

  <h2>A working control plane, <span class="accent">running live at the booth</span></h2>
  <p class="sub">Attendees queued up to attack the platform rather than to watch a slide
    deck. Eight AI security modules run on the same policy engine AccuKnox uses for cloud
    workloads, all reachable from one console.</p>

  <div class="diagram"><img src="%(hero)s" alt="AccuKnox AI Security architecture"></div>
  <div class="cap">Eight AI security modules over AI assets, substrate, and every
    deployment model, including air-gapped and edge.</div>

  <div class="items">
    <div class="item"><h3>Enforcement lives inside the kernel</h3>
      <p>KubeArmor, the open source project AccuKnox maintains, uses <b>eBPF and LSM</b>
      to allow or block process, file, and network behavior inside the kernel. The same
      engine that guards production workloads now guards AI agents and MCP servers.</p></div>

    <div class="item"><h3>Prompt defense that holds state across turns</h3>
      <p>Classifier-only prompt firewalls have a measurable bypass problem. Published
      research records <b>100%% attack success</b> for some character injection techniques,
      and multi-turn frameworks such as HarmNet and X-Teaming land at <b>94 to 99%%</b>.
      AccuKnox tracks context across turns, inspects input and output, masks PII and PHI,
      and catches secrets before they leave the session.</p></div>

    <div class="item"><h3>Agents get an identity and a permission boundary</h3>
      <p>Identity comes from <b>SPIFFE</b>, authorization from <b>OpenFGA</b>, isolation
      from the kernel. An agent that reaches for a tool it never needed gets stopped
      rather than logged after the fact.</p></div>

    <div class="item"><h3>Red teaming runs on every model update</h3>
      <p>Automated adversarial probes for injection, jailbreak, and hallucination fire
      after each change, because a model that ships weekly cannot be signed off once a
      year. Findings map to <b>MITRE ATLAS, OWASP LLM Top 10, NIST AI RMF, and the
      EU AI Act</b>.</p></div>
  </div>

  <div class="band"><b>Deployment parity is the part regulated buyers test first.</b>
    One policy engine, one audit trail, and identical scanning across SaaS, Kubernetes,
    private cloud, and fully air-gapped installs. Coverage reaches cloud unmanaged and
    on-prem unmanaged AI too, which is where shadow AI hides. IBM priced that blind spot
    at <b>$670K</b> in extra average breach cost in 2025.</div>

  <div class="pnum">2</div>
</div></div>
""" % A


PAGE3 = """
<div class="page"><div class="p">
  <div class="head"><img src="%(logo_light)s" alt="AccuKnox">
    <span>THE TALKS AND WHY IT WON</span></div>

  <div class="trow">
    <img class="banner" src="%(rahul)s" alt="Rahul Jadhav speaker session banner">
    <img class="float-dash" src="%(dash)s" alt="AccuKnox AI security console">
  </div>

  <div class="talks">
    <div class="talk">
      <div class="who">Rahul Jadhav</div><div class="role">CTO AND CO-FOUNDER</div>
      <div class="t">The Subtle Art of AI Prompt Guardrails</div>
      <div class="d">Where guardrails hold, where they break, and what the literature
        actually shows. Attack techniques with their measured success rates, the latency
        cost of inspection, and the integration patterns that survive production.</div>
    </div>
    <div class="talk">
      <div class="who">Gaurav Mishra</div><div class="role">SENIOR PRODUCT MANAGER</div>
      <div class="t">A multi-layered defence pipeline for an enterprise LLM chat
        application</div>
      <div class="d">One real enterprise chat application, traced through the full
        defence chain, from prompt inspection to dataset controls to runtime enforcement
        on the serving infrastructure.</div>
    </div>
  </div>

  <h2 style="margin-top:3.4mm;font-size:15pt">Why <span class="accent">AccuKnox</span>
    took first place</h2>
  <div class="items" style="margin-top:4.6mm">
    <div class="item"><h3>The judges could attack it themselves</h3>
      <p>Prompt injection and agentic attacks ran against a live instance, and each block
      landed in the audit trail while the attacker watched.</p></div>
    <div class="item"><h3>The enforcement claim is auditable</h3>
      <p>KubeArmor is open source with a public codebase and an active contributor base,
      so the kernel-level enforcement story can be read rather than taken on trust.</p></div>
    <div class="item"><h3>Coverage includes the assets nobody wants to discuss</h3>
      <p>Rogue notebooks, self-hosted models on VMs, developer workstation LLMs, and MCP
      servers sit under one policy engine with the sanctioned cloud services.</p></div>
  </div>

  <div class="closer">
    <h4>What this means for you</h4>
    <p>For organizations across financial services, healthcare, telecommunications,
      manufacturing, critical infrastructure, government, and other regulated industries,
      AI security is now a standard part of every customer and compliance review. AccuKnox
      addresses these requirements with a unified platform that deploys wherever sensitive
      data must remain, enforces protection at runtime to stop threats before they become
      incidents, and generates the evidence auditors and customers expect. Recognition at
      BSides validates the platform's capabilities through independent testing by security
      practitioners in real-world environments.</p>
    <div class="meta"><span>AccuKnox &middot; Zero Trust security for AI, API,
      Application, Cloud, and Supply Chain &middot; accuknox.com</span>
      <img src="%(emblem)s" alt=""></div>
  </div>

  <div class="pnum">3</div>
</div></div>
""" % A


def main():
    doc = ("<!doctype html><meta charset='utf-8'>"
           "<title>AccuKnox at Security BSides Bangalore 2026</title>"
           "<style>%s</style>%s%s%s" % (CSS, PAGE1, PAGE2, PAGE3))
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print("html %.2f MB" % (os.path.getsize(HTML_OUT) / 1e6))

    if os.path.exists(PDF_OUT):
        os.remove(PDF_OUT)
    subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        "--print-to-pdf=" + PDF_OUT, HTML_OUT.replace("\\", "/"),
    ], check=True, timeout=300)
    print("wrote %s (%.2f MB)" % (PDF_OUT, os.path.getsize(PDF_OUT) / 1e6))


if __name__ == "__main__":
    sys.exit(main())
