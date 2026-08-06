"""Build the AccuKnox customer advisory email for CERT-In/CSIRT-Fin 261730083303
(targeted attacks against Microsoft 365 in the Indian BFSI sector) as a branded
2-page A4 PDF.

Page 1 leads with what AccuKnox produces: a CIS Microsoft 365 findings report from
the SSPM module's MS 365 integration, with the console steps and screenshot inline.
Page 2 carries the campaign detail and the close.

Source advisory is TLP: AMBER and marked not for hosting in the public domain, so
this file paraphrases the attack patterns at a level already covered by the public
references in the advisory and reproduces no IoCs.
"""
import base64
import mimetypes
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(REPO, "output", "certin-m365")
IMG = os.path.join(WORK, "img")
HTML_OUT = os.path.join(WORK, "AccuKnox_CERTIn_M365_BFSI_Advisory_Email.html")
PDF_OUT = os.path.join(REPO, "output", "AccuKnox_CERTIn_M365_BFSI_Advisory_Email.pdf")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


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
    "steps": uri(os.path.join(IMG, "sspm-m365-scan-steps.png")),
}


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { font-family: 'Space Grotesk', 'Inter', 'Segoe UI', sans-serif;
  color: #1A1D2E; -webkit-print-color-adjust: exact; print-color-adjust: exact; }

.page { position: relative; width: 210mm; height: 297mm; overflow: hidden;
  page-break-after: always; background: #fff; }
.page:last-child { page-break-after: auto; }

/* ---------- masthead ---------- */
.mast { position: relative; padding: 6.5mm 14mm 5.6mm; color: #fff; background:
    radial-gradient(560px 300px at 88% -20%, rgba(100,100,255,.45), transparent 68%),
    radial-gradient(420px 300px at -6% 130%, rgba(200,0,25,.26), transparent 66%),
    linear-gradient(150deg, #0B1240 0%, #11206D 48%, #0A0E33 100%); }
.mast .grid { position: absolute; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,.05) 1px, transparent 1px);
  background-size: 24px 24px; }
.mast .row { position: relative; display: flex; align-items: center;
  justify-content: space-between; }
.mast img.logo { height: 7mm; }
.tag { font-size: 6.8pt; letter-spacing: 1.1px; color: #9BB4FF; font-weight: 600;
  border: 1px solid rgba(155,180,255,.42); border-radius: 999px; padding: 1.4mm 3.4mm; }
.mast h1 { position: relative; margin-top: 4mm; font-size: 15.8pt; font-weight: 700;
  line-height: 1.16; letter-spacing: -.4px; max-width: 172mm; }
.mast h1 em { font-style: normal; color: #9BB4FF; }
.crit { position: relative; display: flex; gap: 2.6mm; margin-top: 3.6mm; }
.pill { font-size: 7pt; font-weight: 600; letter-spacing: .3px; border-radius: 2.4mm;
  padding: 1.6mm 3.2mm; background: rgba(255,255,255,.08);
  border: 1px solid rgba(155,180,255,.3); color: #D6DEF8; }
.pill.red { background: rgba(200,0,25,.24); border-color: rgba(255,140,150,.45);
  color: #FFD3D8; }

/* ---------- body ---------- */
.p { padding: 4.4mm 14mm 0; }
.meta { border: 1.3px solid #C4CCDE; border-radius: 3.2mm; overflow: hidden;
  margin-bottom: 3.4mm; }
.meta div { display: flex; font-size: 8.3pt; border-bottom: 1px solid #E4E8F2;
  padding: 2mm 4mm; }
.meta div:last-child { border-bottom: 0; }
.meta .k { width: 17mm; color: #6A749A; font-weight: 600; letter-spacing: .3px;
  flex-shrink: 0; }
.meta .v { color: #1A1D2E; }
.meta .subj .v { font-weight: 700; color: #11206D; }
.meta .v em { font-style: normal; color: #6A749A; }

p.b { font-size: 9.2pt; line-height: 1.56; color: #2B3157; margin-bottom: 3mm; }
p.b b { color: #11206D; }
h3.s { font-size: 10pt; font-weight: 700; color: #11206D; margin: 5mm 0 3mm; }

/* value callout, the lead */
.value { border-radius: 4mm; padding: 4.2mm 5mm; margin-bottom: 3.2mm; color: #fff;
  background: radial-gradient(360px 180px at 94% 6%, rgba(100,100,255,.55), transparent 70%),
    linear-gradient(122deg, #11206D, #0A0E33); }
.value h4 { font-size: 10.2pt; font-weight: 700; margin-bottom: 2.2mm; }
.value p { font-size: 8.9pt; line-height: 1.54; color: #D6DEF8; }
.value p b { color: #fff; font-weight: 600; }
.value p a { color: #9BB4FF; text-decoration: none; font-weight: 600; }
.value .tri { display: flex; gap: 2.6mm; margin-top: 3.4mm; }
.value .tri div { flex: 1; background: rgba(255,255,255,.08); border-radius: 2.4mm;
  border: 1px solid rgba(155,180,255,.28); padding: 2.4mm 3mm; }
.value .tri .h { font-size: 7.6pt; font-weight: 700; color: #9BB4FF;
  letter-spacing: .3px; }
.value .tri .d { font-size: 7.2pt; line-height: 1.38; color: #C9D4F5;
  margin-top: 1mm; }

ul.l { list-style: none; margin-bottom: 4mm; }
ul.l li { position: relative; padding-left: 7mm; font-size: 9pt; line-height: 1.55;
  color: #2B3157; margin-bottom: 2.4mm; }
ul.l li:before { content: ''; position: absolute; left: 0; top: 1.6mm; width: 2.2mm;
  height: 2.2mm; border-radius: 50%; background: #0046FF;
  box-shadow: 0 0 0 1.8mm rgba(0,70,255,.12); }
ul.l li b { color: #11206D; }

ol.n { list-style: none; counter-reset: n; margin-bottom: 2.4mm; }
ol.n li { counter-increment: n; position: relative; padding-left: 8.2mm;
  font-size: 8.8pt; line-height: 1.5; color: #2B3157; margin-bottom: 1.9mm; }
ol.n li:before { content: counter(n); position: absolute; left: 0; top: .2mm;
  width: 5.2mm; height: 5.2mm; border-radius: 50%; background: #11206D; color: #fff;
  font-size: 6.8pt; font-weight: 700; text-align: center; line-height: 5.2mm; }
ol.n li b { color: #11206D; }

.band { background: #EEF0F6; border-left: 3.2px solid #0046FF;
  border-radius: 0 3mm 3mm 0; padding: 3.8mm 4.8mm; font-size: 8.8pt; line-height: 1.54;
  color: #2B3157; margin-bottom: 4.2mm; }
.band b { color: #11206D; }
.band.red { background: #FFF4F5; border-left-color: #C80019; }
.band.red b { color: #A3000F; }

.shot { margin: 0 0 2mm; width: 100%; border: 1.3px solid #C4CCDE;
  border-radius: 3.4mm; padding: 1.4mm; background: #fff;
  box-shadow: 0 6px 18px rgba(17,32,109,.1); }
.shot img { width: 100%; display: block; border-radius: 2mm; }

.sign { font-size: 9pt; line-height: 1.5; color: #2B3157; margin-top: 5mm; }
.sign b { color: #11206D; }

.closer { margin-top: 6mm; color: #fff;
  border-radius: 4.4mm; padding: 5mm 5.6mm; background:
    radial-gradient(380px 190px at 93% 8%, rgba(100,100,255,.5), transparent 70%),
    linear-gradient(120deg, #11206D, #0A0E33); }
.closer h4 { font-size: 11pt; font-weight: 700; margin-bottom: 2.4mm; }
.closer p { font-size: 9pt; line-height: 1.56; color: #D6DEF8; }
.closer p b { color: #fff; font-weight: 600; }
.closer .crumb { margin-top: 3.6mm; padding-top: 3mm; font-size: 7.6pt; color: #9BB4FF;
  border-top: 1px solid rgba(155,180,255,.26); display: flex;
  justify-content: space-between; align-items: center; }
.closer .crumb img { height: 5.2mm; }

.foot { position: absolute; left: 14mm; right: 14mm; bottom: 8mm; display: flex;
  align-items: center; justify-content: space-between; border-top: 1px solid #D8DEEC;
  padding-top: 3mm; font-size: 7.2pt; color: #7A83A8; }
.foot img { height: 4.8mm; }
.pnum { font-weight: 700; color: #11206D; }
"""


PAGE1 = """
<div class="page">
  <div class="mast"><div class="grid">
    </div><div class="row">
      <img class="logo" src="%(logo_dark)s" alt="AccuKnox">
      <span class="tag">CUSTOMER SECURITY ADVISORY</span>
    </div>
    <h1>Targeted attacks on Microsoft 365 in Indian BFSI, and the
      <em>findings report AccuKnox generates for it</em></h1>
    <div class="crit">
      <span class="pill red">CERT-In / CSIRT-Fin: CRITICAL</span>
      <span class="pill">Advisory 261730083303</span>
      <span class="pill">Issued Aug 03, 2026</span>
    </div>
  </div>

  <div class="p">
    <div class="meta">
      <div class="subj"><span class="k">Subject</span><span class="v">CERT-In critical
        advisory on Microsoft 365, and your AccuKnox findings report</span></div>
      <div><span class="k">Details</span><span class="v"><em>From</em> AccuKnox Security
        Team &middot; <em>To</em> [Customer security contact] &middot;
        <em>Attached</em> Sample MS 365 findings report</span></div>
    </div>

    <p class="b">Hello [Name], on <b>August 3, 2026</b> CERT-In and CSIRT-Fin issued a
      <b>Critical</b> advisory on a campaign against Microsoft 365 in the Indian BFSI
      sector. The accounts it reached had MFA enabled, so what separates an exposed setup
      from a safe one is configuration.</p>

    <div class="value">
      <h4>AccuKnox generates the findings report for you</h4>
      <p>The <b>SSPM module, MS 365 integration</b> scans your Microsoft 365 environment
        against the <b>CIS Microsoft 365 Foundations Benchmark</b>
        (<a href="https://www.cisecurity.org/benchmark/microsoft_365">cisecurity.org/benchmark/microsoft_365</a>)
        and returns a findings report. Every control comes back pass or fail, with
        severity and the fix, so you get your gaps rather than a benchmark to read.</p>
      <div class="tri">
        <div><div class="h">Entra ID</div><div class="d">MFA coverage, legacy auth,
          device code flow</div></div>
        <div><div class="h">Exchange</div><div class="d">Mail forwarding, mailbox
          auditing</div></div>
        <div><div class="h">SharePoint</div><div class="d">External and org-wide sharing,
          audit logging</div></div>
      </div>
    </div>

    <ol class="n">
      <li>Open <b>Settings &rarr; Integrations &rarr; Collectors</b>, pick
        <b>SaaS Security Posture Management</b>.</li>
      <li>Add a collector, set Integration Type to <b>Microsoft 365</b>, then fill in the
        credential fields shown below.</li>
      <li>Label it and save. Findings land in <b>Issues</b>, the benchmark result in
        <b>Compliance</b>.</li>
    </ol>

    <div class="shot"><img src="%(steps)s" alt="Setting up the SSPM Microsoft 365
      integration in the AccuKnox console"></div>
  </div>

  <div class="foot">
    <span>AccuKnox &middot; Zero Trust security for AI, API, Application, Cloud and
      Supply Chain &middot; accuknox.com</span>
    <span class="pnum">1 / 2</span>
  </div>
</div>
""" % A


PAGE2 = """
<div class="page">
  <div class="p" style="padding-top:12mm">
    <div style="display:flex;align-items:center;justify-content:space-between;
      border-bottom:1.6px solid #C4CCDE;padding-bottom:3mm;margin-bottom:6mm">
      <img src="%(logo_light)s" alt="AccuKnox" style="height:6mm">
      <span style="font-size:7.4pt;color:#6A749A;letter-spacing:.6px">WHAT THE ADVISORY
        DESCRIBES</span>
    </div>

    <p class="b">Four access routes are described, and none of them needs your users to
      hand over a password.</p>

    <ul class="l">
      <li><b>Credential replay at scale.</b> Previously breached username and password
        lists tried against M365 sign-in endpoints through the Azure CLI ROPC flow.</li>
      <li><b>Device-code phishing.</b> The lure collects OAuth tokens instead of
        passwords. Your user approves a genuine Microsoft prompt, so the session passes
        to the attacker with MFA already satisfied.</li>
      <li><b>Session token reuse.</b> A stolen token skips sign-in entirely. Mail then
        goes out from the real account, which is what makes it hard to spot.</li>
      <li><b>Quiet reads in SharePoint.</b> Documents opened through previews, page views
        and search rather than downloads, so download-based audit trails stay quiet.</li>
    </ul>

    <div class="band red"><b>Why MFA alone does not settle this.</b> These sign-ins are
      logged as MFA satisfied, so a log review shows nothing unusual. What closes the
      path is configuration: device code flow, legacy authentication, Conditional Access
      scope, phishing-resistant MFA for admins, and SharePoint sharing and audit
      settings. All five are covered in the findings report.</div>

    <div class="band"><b>A sample report is attached.</b> It shows the output format,
      the control-by-control results and the remediation detail, so you can see what you
      get before connecting the integration.</div>

    <p class="b">If you see anything resembling this campaign, preserve the logs, contain
      first, and report to CERT-In and CSIRT-Fin at <b>incident@cert-in.org.in</b>. We can
      help with the M365 log review while you do that.</p>

    <p class="b" style="font-size:8.4pt;color:#6A749A">The advisory itself is TLP: AMBER
      and restricted, so its indicators of compromise are not reproduced here. Request
      the original through your CSIRT-Fin channel.</p>

    <div class="sign">
      Regards,<br>
      <b>[Your name]</b><br>
      AccuKnox Security Team<br>
      security@accuknox.com &middot; accuknox.com
    </div>

    <div class="closer">
    <h4>Want this report for your own environment?</h4>
    <p>Reply to this mail and we will connect the <b>SSPM MS 365 integration</b> with you,
      run the first scan, and go through the failing controls in the order that matters
      for this advisory. Existing AccuKnox customers already have the module, so there is
      nothing to buy.</p>
    <div class="crumb"><span>AccuKnox &middot; SSPM, CSPM, KSPM, AI Security and runtime
      enforcement on one policy engine</span><img src="%(emblem)s" alt=""></div>
    </div>
  </div>

  <div class="foot">
    <span>AccuKnox &middot; Zero Trust security for AI, API, Application, Cloud and
      Supply Chain &middot; accuknox.com</span>
    <img src="%(emblem)s" alt="">
    <span class="pnum">2 / 2</span>
  </div>
</div>
""" % A


def main():
    doc = ("<!doctype html><meta charset='utf-8'>"
           "<title>AccuKnox advisory email, CERT-In M365 BFSI</title>"
           "<style>%s</style>%s%s" % (CSS, PAGE1, PAGE2))
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
