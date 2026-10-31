# -*- coding: utf-8 -*-
"""
Shared kit for the four AccuKnox product decks prepared for Veracode
(Container Security + IaC, CSPM, DSPM, API Security).

One product = one spec module in scripts/veracode_decks/<key>.py holding SPEC, a dict.
build_veracode_products.py renders the diagrams and builds one 14-slide deck per spec.

Slide order, fixed for every product:
  1 cover, 2 agenda, 3 problem, 4 solution overview, 5 solution detail,
  6 technical architecture, 7 deployment architecture, 8 use cases, 9 POC,
  10 user journey, 11 differentiators, 12 stack ranking, 13 pricing, 14 closing.
"""
import os, shutil
from pptx import Presentation
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

import _aksvg as S
import _veracode_visuals as V
from _akdeck import *  # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
UI = r"D:\AccuKnox\help\references\PRODUCT UI"
DOCS = r"D:\AccuKnox\help\docs"


# =================================================================== diagrams
def svg_arch(name, outdir, cols, cp_title, cp_rows):
    """Four-stage flow. cols = [(head, [(icon, label, brand), ...]), ...] for stages 1, 2 and 4.
    cp_rows = [(icon, line1, line2 or None), ...] for the control-plane stage."""
    W, H = 1280, 512
    b = []
    (h1, src), (h2, col), (h4, out) = cols
    b.append(S.text(10, 26, "1  " + h1, 20, S.PRIMARY, 700))
    b.append(S.text(318, 26, "2  " + h2, 20, S.PRIMARY, 700))
    b.append(S.text(628, 26, "3  " + cp_title, 20, S.PRIMARY, 700))
    b.append(S.text(1048, 26, "4  " + h4, 20, S.PRIMARY, 700))
    step = min(64, 456 // max(len(src), 1))
    for i, (ic, lab, br) in enumerate(src):
        b.append(S.chip(10, 44 + i * step, 270, min(52, step - 10), ic, lab, size=17, brand=br))
    step = min(80, 456 // max(len(col), 1))
    for i, (ic, lab, br) in enumerate(col):
        b.append(S.chip(318, 48 + i * step, 262, min(58, step - 12), ic, lab, size=17, brand=br))
    for x1, x2 in ((284, 314), (584, 624), (1004, 1044)):
        b.append(S.arrow(x1, 268, x2, 268, color=S.PRIMARY, sw=6))
    b.append(S.rect(628, 44, 372, 456, fill=S.NAVY, stroke=S.NAVY, r=18))
    n = len(cp_rows)
    rh = (436 - (n - 1) * 12) / n
    for i, (ic, l1, l2) in enumerate(cp_rows):
        y = 54 + i * (rh + 12)
        b.append(S.rect(646, y, 336, rh, fill=S.NAVY_DK, stroke=S.PURPLE, sw=1.5, r=12))
        b.append(S.ui(ic, 660, y + rh / 2 - 20, 40, "#FFFFFF"))
        if l2:
            b.append(S.text(714, y + rh / 2 - 4, [l1, l2], 18, S.WHITE, 600, lh=1.2))
        else:
            b.append(S.text(714, y + rh / 2 + 7, l1, 18, S.WHITE, 600))
    step = min(90, 456 // max(len(out), 1))
    for i, (ic, lab, br) in enumerate(out):
        b.append(S.chip(1048, 52 + i * step, 222, min(60, step - 14), ic, lab, size=18, brand=br))
    return S.render(name, W, H, "".join(b), outdir)


def svg_deploy(name, outdir, env_label, rows, cp_lines, note):
    """Customer boundary with component rows on the left, control plane on the right.
    rows = [(icon, brand, head, sub), ...]"""
    W = 1280
    n = len(rows)
    H = 70 + n * 78 + 10
    H = max(H, 380)
    b = [S.rect(8, 8, 846, H - 16, fill="#F7F8FC", stroke=S.PRIMARY, sw=2.5, r=18, dash="12 8"),
         S.ui("building", 26, 18, 30, S.PRIMARY), S.text(64, 42, env_label, 21, S.PRIMARY, 700)]
    mid = H / 2
    for i, (ic, brand, head, sub) in enumerate(rows):
        y = 62 + i * 78
        b.append(S.rect(26, y, 810, 66, fill=S.WHITE, stroke=S.GREY_BD, sw=1.5, r=12))
        b.append(S.logo(ic, 40, y + 11, 44) if brand else S.ui(ic, 40, y + 11, 44, S.PRIMARY))
        b.append(S.text(100, y + 29, head, 20, S.NAVY, 700))
        b.append(S.text(100, y + 54, sub, 17, S.MUTE, 500))
        b.append(S.arrow(838, y + 33, 924, mid - 40, color=S.PRIMARY, sw=2.5))
    top = mid - 40 - 110
    b.append(S.rect(930, top, 342, 220, fill=S.NAVY, stroke=S.NAVY, r=18))
    b.append(S.ui("server-2", 952, top + 20, 44, "#FFFFFF"))
    b.append(S.text(1008, top + 40, ["AccuKnox", "control plane"], 21, S.WHITE, 700, lh=1.15))
    for i, ln in enumerate(cp_lines):
        b.append(S.text(954, top + 118 + i * 30, ln, 18, "#B8C4E8", 500))
    b.append(S.rect(930, top + 234, 342, 82, fill=S.GREEN_LT, stroke=S.GREEN, sw=1.5, r=12))
    b.append(S.ui("shield-check", 944, top + 250, 36, S.GREEN_DK))
    b.append(S.text(990, top + 266, note, 17, S.GREEN_DK, 700, lh=1.2))
    return S.render(name, W, H, "".join(b), outdir)


# =================================================================== deck
class Deck:
    def __init__(self, spec, out):
        self.sp = spec
        self.out = out
        shutil.copy(os.path.join(ROOT, "PPT Template.pptx"), out)
        self.prs = Presentation(out)
        for sid in list(self.prs.slides._sldIdLst):
            try:
                self.prs.part.drop_rel(sid.get(qn("r:id")))
            except Exception:
                pass
            self.prs.slides._sldIdLst.remove(sid)
        self.L = self.prs.slide_layouts[4]

    # ---- primitives
    def std(self, title, kicker, key):
        s = self.prs.slides.add_slide(self.L)
        set_title(s, title)
        blank_footer(s)
        eyebrow(s, kicker, y=0.84, w=9.2, size=10.5)
        lk = self.sp.get("links", {}).get(key) or []
        txt = self.sp["notes"][key].strip()
        if lk:
            txt += "\n\nLinks on this slide:\n" + "\n".join((u[0] + ": " + u[1]) if isinstance(u, tuple) else u for u in lk)
        notes(s, txt)
        if lk:
            self.links(s, lk)
        return s

    def links(self, s, urls, y=5.3):
        V.link_pills(s, urls, y=y)

    def web(self, key):
        """A slide of graphics taken from the accuknox.com platform pages."""
        wb = self.sp[key]
        s = self.std(wb["title"], wb["kicker"], key)
        for (png, cap, x, y, w, h) in wb["items"]:
            box(s, x, y, w, h, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
            image_fit(s, png, x + 0.08, y + 0.08, w - 0.16, h - 0.16, frame=None)
            if cap:
                box(s, x, y + h + 0.02, w, 0.26, text=cap, size=9.5, color=MUTE, italic=True, ml=0)
        for (num, lab, x, y, w) in wb.get("stats", []):
            stat(s, x, y, w, num, lab, nsize=22, lsize=10, h=0.86)
        if wb.get("callout"):
            callout(s, CX, wb.get("callout_y", 4.74), CW, 0.44, wb.get("callout_icon", "route"), wb["callout"], size=11.5)
        return s

    def row(self, s, x, y, w, icn, head, sub, ts=0.46, h=0.72):
        icon_tile(s, icn, x, y + 0.04, ts)
        box(s, x + ts + 0.14, y, w - ts - 0.14, 0.3, text=head, size=12.5, color=NAVY, bold=True,
            anchor=MSO_ANCHOR.MIDDLE, ml=0)
        box(s, x + ts + 0.14, y + 0.29, w - ts - 0.14, h - 0.3, text=sub, size=10.5, color=MUTE, ml=0, mt=0)

    def card(self, s, x, y, w, h, icn, head, body, tag=None, accent=None):
        box(s, x, y, w, h, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
        icon_tile(s, icn, x + 0.14, y + 0.16, 0.52, bg=accent)
        box(s, x + 0.78, y + 0.12, w - 0.88, 0.62, text=head, size=12.5, color=NAVY, bold=True,
            anchor=MSO_ANCHOR.MIDDLE, ml=0)
        box(s, x + 0.16, y + 0.8, w - 0.3, h - 1.1 if tag else h - 0.86, text=body, size=11, color=MUTE, ml=0)
        if tag:
            pill(s, x + w - 1.32, y + h - 0.36, 1.2, 0.26, tag, fill=LAV, tcolor=NAVY, size=9.5)

    def shot(self, s, path, x, y, w, h):
        """Crop a tall screenshot from the top to the box aspect, then fit it."""
        from PIL import Image as _I
        import hashlib
        im = _I.open(path).convert("RGB")
        ar = w / h
        if im.size[0] / im.size[1] < ar:
            im = im.crop((0, 0, im.size[0], int(im.size[0] / ar)))
        if im.size[0] > 2400:
            im = im.resize((2400, int(im.size[1] * 2400 / im.size[0])))
        cache = os.path.join(ROOT, "work", "veracode", "crops")
        os.makedirs(cache, exist_ok=True)
        out = os.path.join(cache, hashlib.md5((path + str(round(ar, 3))).encode()).hexdigest()[:12] + ".png")
        im.save(out)
        return image_fit(s, out, x, y, w, h)

    # ---- slides
    def build(self):
        sp = self.sp
        P = self.prs
        cover_slide(P, sp["cover_title"], subtitle=sp["cover_sub"], tsize=24, h=1.3)

        # 2 agenda
        _a = 1 if sp.get("web_a") else 0
        _b = 1 if sp.get("web_b") else 0
        s = self.std("Agenda", f"Six parts, slides 3 to {13 + _a + _b}", "agenda")
        a = 1 if sp.get("web_a") else 0
        b = 1 if sp.get("web_b") else 0
        prob = "Slide 3" if not a else "Slides 3 and 4"
        toc = [("alert-triangle", "The Problem", "Why teams buy " + sp["short"], prob),
               ("stack-2", "Our Solution", "Functional and technical", f"Slides {4 + a} to {6 + a + b}"),
               ("sitemap", "Deployment", "What runs where", f"Slide {7 + a + b}"),
               ("target", "Use Cases and POC", "Scenarios with pass checks", f"Slides {8 + a + b} and {9 + a + b}"),
               ("device-desktop", "User Journey", "The console, step by step", f"Slide {10 + a + b}"),
               ("trophy", "Why AccuKnox", "Differentiators, ranking, pricing", f"Slides {11 + a + b} to {13 + a + b}")]
        for i, (icn, h, sub, rng) in enumerate(toc):
            x = CX + (i % 3) * 3.1
            y = 1.22 + (i // 3) * 2.0
            box(s, x, y, 2.96, 1.82, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
            icon_tile(s, icn, x + 0.18, y + 0.2, 0.74)
            box(s, x + 1.9, y + 0.16, 0.9, 0.6, text=f"0{i+1}", size=28, color=LAV, bold=True, align=PP_ALIGN.RIGHT)
            box(s, x + 0.18, y + 1.0, 2.7, 0.36, text=h, size=16, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
            box(s, x + 0.18, y + 1.34, 2.7, 0.26, text=sub, size=10.5, color=MUTE)
            box(s, x + 0.18, y + 1.56, 2.7, 0.24, text=rng, size=9.5, color=PRIMARY, bold=True)

        # 3 problem
        pr = sp["problem"]
        s = self.std("The Problem We Solve", pr["kicker"], "problem")
        diagram(s, pr["png"], CX, 1.14, CW)
        callout(s, CX, 4.8, CW, 0.44, "shield-check", pr["callout"], size=12)

        if sp.get("web_a"):
            self.web("web_a")

        # 4 solution, functional
        so = sp["overview"]
        s = self.std("Our Solution, Functional", so["kicker"], "overview")
        diagram(s, so["png"], CX, 1.1, CW)
        m = len(so["outcomes"])
        ow = (CW - (m - 1) * 0.14) / m
        for i, (num, lab) in enumerate(so["outcomes"]):
            x = CX + i * (ow + 0.14)
            box(s, x, 4.52, ow, 0.7, fill=GREEN_LT, line=GREEN, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.14)
            icon_img(s, "circle-check", x + 0.14, 4.69, 0.36, color="#16A55C")
            box(s, x + 0.58, 4.54, ow - 0.66, 0.36, text=num, size=15, color=GREEN_DK, bold=True, anchor=MSO_ANCHOR.BOTTOM, ml=0, mb=0)
            box(s, x + 0.58, 4.88, ow - 0.66, 0.3, text=lab, size=10, color=INK, ml=0, mt=0)

        if sp.get("web_b"):
            self.web("web_b")

        # 5 solution detail, bigger screenshot
        sd = sp["detail"]
        s = self.std(sd["title"], sd["kicker"], "detail")
        sh = sd.get("shot_h", 2.86)
        for i, (icn, head, sub) in enumerate(sd["rows"]):
            self.row(s, CX, 1.22 + i * 0.78, 3.75, icn, head, sub, h=0.74)
        self.shot(s, sd["shot"], 4.3, 1.18, 5.3, sh)
        if sd.get("stats"):
            m = len(sd["stats"])
            sw = (5.3 - (m - 1) * 0.12) / m
            for i, (num, lab) in enumerate(sd["stats"]):
                stat(s, 4.3 + i * (sw + 0.12), 1.18 + sh + 0.12, sw, num, lab, nsize=19, lsize=9.5, h=0.78)
        if sd.get("caption"):
            box(s, 4.3, 1.22 + sh, 5.3, 0.3, text=sd["caption"], size=9.5, color=MUTE, italic=True, ml=0)
        if sd.get("note"):
            callout(s, CX, 4.84, CW, 0.4, sd.get("note_icon", "alert-triangle"), sd["note"], size=11)

        # 6 technical architecture
        ta = sp["tech"]
        s = self.std("Our Solution, Technical Architecture", ta["kicker"], "tech")
        bottom = diagram(s, ta["png"], CX, 1.16, CW)
        if ta.get("callout") and bottom < 4.7:
            callout(s, CX, bottom + 0.1, CW, 0.46, "route", ta["callout"], size=11.5)

        # 7 deployment architecture
        de = sp["deploy"]
        s = self.std("Deployment Architecture", de["kicker"], "deploy")
        w = de.get("w", 8.6)
        bottom = diagram(s, de["png"], CX + (CW - w) / 2, 1.14, w)
        modes = [("SaaS", "AccuKnox cloud, same day"), ("Your Cloud", "Your account, no egress"),
                 ("On-Premises", "Your servers, native install"), ("Air-Gapped", "No outbound traffic")]
        y = max(bottom + 0.1, 4.46)
        label(s, CX, y, 1.6, "DEPLOYMENT MODES", size=9.5)
        for i, (h, sub) in enumerate(modes):
            x = CX + 1.62 + i * 1.9
            col = RED if h == "Air-Gapped" else PRIMARY
            box(s, x, y - 0.02, 1.82, 0.72, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
            box(s, x + 0.08, y + 0.02, 1.7, 0.28, text=h, size=11.5, color=col, bold=True, ml=0)
            box(s, x + 0.08, y + 0.3, 1.7, 0.36, text=sub, size=9.5, color=NAVY, ml=0)

        # 8 use cases
        uc = sp["usecases"]
        s = self.std("Use Cases", uc["kicker"], "usecases")
        for i, (icn, head, body, tag) in enumerate(uc["cards"]):
            x = CX + (i % 3) * 3.1
            y = 1.22 + (i // 3) * 2.0
            self.card(s, x, y, 3.0, 1.86, icn, head, body, tag=tag)

        # 9 POC
        po = sp["poc"]
        s = self.std("POC Scenarios", po["kicker"], "poc")
        k = len(po["steps"])
        stepw = (7.2) / k
        for i, (icn, d, t) in enumerate(po["steps"]):
            x = CX + i * stepw
            icon_tile(s, icn, x, 1.24, 0.46)
            box(s, x + 0.54, 1.2, stepw - 0.74, 0.26, text=d, size=10, color=PRIMARY, bold=True, ml=0)
            box(s, x + 0.54, 1.44, stepw - 0.74, 0.5, text=t, size=11, color=NAVY, bold=True, ml=0)
            if i < k - 1:
                arrow(s, x + stepw - 0.22, 1.36, 0.2, 0.26)
        for j, (txt, fill, tc) in enumerate(po["pills"]):
            pill(s, 7.75, 1.22 + j * 0.33, 1.85, 0.27, txt, fill=fill, tcolor=tc, size=10)
        n = len(po["tests"])
        cw = (CW - (n - 1) * 0.13) / n
        for i, (icn, h, test, ok) in enumerate(po["tests"]):
            x = CX + i * (cw + 0.13)
            box(s, x, 2.06, cw, 3.1, fill=WHITE, line=GREY_BD, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
            icon_tile(s, icn, x + 0.14, 2.2, 0.5)
            box(s, x + 0.74, 2.16, cw - 0.84, 0.58, text=h, size=12.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
            label(s, x + 0.14, 2.82, cw - 0.3, "TEST", size=9.5)
            box(s, x + 0.14, 3.06, cw - 0.25, 0.9, text=test, size=11, color=INK, ml=0)
            box(s, x + 0.1, 4.02, cw - 0.2, 1.04, fill=GREEN_LT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
            label(s, x + 0.2, 4.06, cw - 0.4, "PASS CHECK", size=9.5, color=GREEN_DK)
            box(s, x + 0.2, 4.3, cw - 0.38, 0.72, text=ok, size=11, color=GREEN_DK, bold=True, ml=0)

        # 10 journey, bigger screenshots with an overlay caption band
        jr = sp["journey"]
        s = self.std("User Journey, UI and UX", jr["kicker"], "journey")
        for i, (pic, h, sub) in enumerate(jr["steps"]):
            x = CX + (i % 3) * 3.1
            y = 1.12 + (i // 3) * 2.06
            self.shot(s, pic, x, y, 3.0, 1.98)
            band = box(s, x, y + 1.46, 3.0, 0.52, fill=NAVY, shape=MSO_SHAPE.RECTANGLE)
            sf = band.fill._xPr.find(qn("a:solidFill"))
            clr = sf[0]
            a = clr.makeelement(qn("a:alpha"), {"val": "88000"}); clr.append(a)
            box(s, x + 0.08, y + 1.54, 0.36, 0.36, text=str(i + 1), size=12, color=WHITE, bold=True, fill=PRIMARY,
                shape=MSO_SHAPE.OVAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0, mt=0, mb=0)
            box(s, x + 0.52, y + 1.47, 2.44, 0.27, text=h, size=12, color=WHITE, bold=True, ml=0, mb=0, anchor=MSO_ANCHOR.BOTTOM)
            box(s, x + 0.52, y + 1.73, 2.44, 0.24, text=sub, size=9.5, color=NAVY_TXT, ml=0, mt=0)

        # 11 differentiators
        di = sp["diffs"]
        s = self.std("Key Differentiators", di["kicker"], "diffs")
        m = len(di["stats"])
        sw = (CW - (m - 1) * 0.16) / m
        for i, (num, lab) in enumerate(di["stats"]):
            stat(s, CX + i * (sw + 0.16), 1.2, sw, num, lab, nsize=24, lsize=10.5, h=1.0)
        for i, (icn, h, b) in enumerate(di["cards"]):
            x = CX + (i % 3) * 3.12
            y = 2.36 + (i // 3) * 1.42
            icon_card(s, x, y, 2.96, 1.3, icn, h, b, hsize=13, bsize=11)

        # 12 stack ranking, icon scorecard
        rk = sp["ranking"]
        s = self.std("Stack Ranking", rk["kicker"], "ranking")
        score = V.scorecard(s, rk["vendors"], rk["rows"], y0=1.18)
        n = len(rk["rows"])
        tally = "   ".join(f"{v} {sc}/{n}" for v, sc in zip(rk["vendors"], score))
        callout(s, CX, 1.18 + 0.5 + 0.48 * n + 0.1, CW, 0.5, "trophy", rk["callout"] + "  Score: " + tally, size=11)

        # 13 pricing
        pc = sp["pricing"]
        s = self.std("Pricing", pc["kicker"], "pricing")
        # unit hero
        box(s, CX, 1.2, 3.0, 1.92, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
        box(s, CX + 0.18, 1.3, 2.7, 0.3, text="BILLING METRIC", size=9.5, color=NAVY_TXT, bold=True, ml=0)
        box(s, CX + 0.18, 1.56, 2.7, 0.8, text=pc["unit_big"], size=20, color=WHITE, bold=True, ml=0,
            anchor=MSO_ANCHOR.MIDDLE, spacing=0.95)
        box(s, CX + 0.18, 2.38, 2.7, 0.72, text=pc["unit_sub"], size=10, color=NAVY_TXT, ml=0)
        # tiers
        label(s, 3.55, 1.18, 3.0, "PRICE PER UNIT PER MONTH (USD)")
        tiers = [["Units", "Price"], ["10 to 50", "$40"], ["51 to 250", "$34"], ["251 to 750", "$29"],
                 ["751 to 2,500", "$25"], ["2,501 to 5,000", "$21"], ["5,001 and up", "Negotiated"]]
        table(s, 3.55, 1.46, 2.75, 2.66, tiers, colw=[1.55, 1.2], hsize=11, bsize=10.5)
        # example
        label(s, 6.5, 1.18, 3.1, "LIST PRICE EXAMPLE")
        ex = box(s, 6.5, 1.46, 3.1, 2.66, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05,
                 ml=0.16, mr=0.12, mt=0.12)
        first = True
        for (txt, big) in pc["example"]:
            para(ex, txt, size=15 if big else 10.5, color=PRIMARY if big else NAVY, bold=big, first=first,
                 space_after=5)
            first = False
        if pc.get("todo"):
            todo_panel(s, CX, 3.24, 3.0, 0.88, pc["todo"][0], pc["todo"][1], size=10)
        elif pc.get("unit_rows"):
            label(s, CX, 3.22, 3.0, "WHAT COUNTS", size=9.5)
            bullets(s, CX, 3.48, 3.0, 0.7, pc["unit_rows"], size=10.5, gap=2)
        label(s, CX, 4.4, 1.3, "SUPPORT", size=9.5)
        for i, t1 in enumerate(["Silver: included, 9x5", "Gold: +10%, 12x6", "Platinum: +25%, 24x7"]):
            pill(s, CX + 1.35 + i * 2.62, 4.4, 2.5, 0.3, t1, fill=LAV, tcolor=NAVY, size=10)
        label(s, CX, 4.78, 1.3, "DEPLOYMENT", size=9.5)
        for i, t1 in enumerate(["On-prem: $0, Platinum support", "Shared SaaS: $0", "Dedicated: $3,000/mo + 10%"]):
            pill(s, CX + 1.35 + i * 2.62, 4.78, 2.5, 0.3, t1, fill=PRIMARY, size=10)
        footer_note(s, "List prices from the AccuKnox Pricing and Sizing sheet, September 2026. Partner terms are separate.",
                    y=5.09, size=9)

        closing_slide(P)
        P.save(self.out)
        return self.out
