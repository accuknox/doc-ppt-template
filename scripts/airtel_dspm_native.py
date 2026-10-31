# -*- coding: utf-8 -*-
"""
Editable versions of the Airtel DSPM architecture and timeline diagrams.
Same layout as airtel_dspm_svg.py, drawn as native PowerPoint shapes so every
box, label and arrow can be edited in Google Slides. Coordinates are SVG
pixels on a 1280 px canvas, mapped to inches at 9.2 in wide.
"""
from lxml import etree
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn
from _akdeck import box, icon_img

K = 9.2 / 1280
NAVY, PRIMARY, SECOND, PURPLE = "#11206D", "#0046FF", "#6464FF", "#4D4DD9"
RED, RED_LT, GREEN, GREEN_DK = "#C80019", "#FBECEE", "#16A55C", "#0B7A42"
INK, MUTE, GREY_BD, GREY_BG, LAV, WHITE = "#1B223B", "#5A637D", "#C4CCDE", "#EEF0F6", "#ECECFB", "#FFFFFF"


def C(h):
    return RGBColor.from_string(h.lstrip("#"))


def pt(px):
    return max(9.0, round(px * K * 72, 1))


class Canvas:
    def __init__(self, slide, ox, oy):
        self.s, self.ox, self.oy = slide, ox, oy

    def X(self, v): return self.ox + v * K
    def Y(self, v): return self.oy + v * K

    def rect(self, x, y, w, h, fill=WHITE, stroke=GREY_BD, sw=1.5, r=14, dash=False, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
        sp = box(self.s, self.X(x), self.Y(y), w * K, h * K, fill=C(fill) if fill else None,
                 line=C(stroke) if stroke else None, line_w=sw * 0.52, shape=shape,
                 radius=min(0.5, r / min(w, h)) if shape == MSO_SHAPE.ROUNDED_RECTANGLE else None)
        if dash and stroke:
            sp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        return sp

    def text(self, x, y, txt, size=18, color=INK, bold=False, anchor="start", w=None):
        """y is the SVG baseline. anchor start, middle or end, as in SVG."""
        w = w or max(40, len(txt) * size * 0.62)
        hpx = size * 1.45
        top = y - size * 1.08
        left = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
        al = {"start": PP_ALIGN.LEFT, "middle": PP_ALIGN.CENTER, "end": PP_ALIGN.RIGHT}[anchor]
        return box(self.s, self.X(left), self.Y(top), w * K, hpx * K, text=txt, size=pt(size), color=C(color),
                   bold=bold, align=al, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0, mr=0, mt=0, mb=0)

    def line(self, x1, y1, x2, y2, color=PRIMARY, sw=2.5, dash=False, head=True):
        c = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(self.X(x1)), Inches(self.Y(y1)),
                                        Inches(self.X(x2)), Inches(self.Y(y2)))
        c.line.color.rgb = C(color); c.line.width = Pt(sw * 0.6)
        if dash:
            c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        if head:
            ln = c.line._get_or_add_ln()
            ln.append(etree.SubElement(ln, qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"}))
        return c

    def icon(self, name, x, y, s, color=None):
        return icon_img(self.s, name, self.X(x), self.Y(y), s * K, color=color)


def architecture(slide, ox, oy):
    c = Canvas(slide, ox, oy)
    c.rect(16, 44, 1248, 420, fill="#F7F8FC", stroke=NAVY, sw=2.5, r=18, dash=True)
    c.icon("building", 34, 56, 32, NAVY)
    c.text(76, 80, "Airtel on-prem, private cloud", 23, NAVY, True)

    ox_, oy_, ow, oh = 36, 100, 760, 344
    c.rect(ox_, oy_, ow, oh, fill=WHITE, stroke=RED, sw=2, r=16)
    c.icon("si-openstack", ox_ + 18, oy_ + 14, 30)
    c.text(ox_ + 58, oy_ + 38, "OpenStack", 22, RED, True)
    stores = [("si-openstack", "VM file systems", False), ("postgresql-original", "PostgreSQL 16+", False),
              ("mysql-original", "MySQL", False), ("mariadb-original", "MariaDB", False),
              ("microsoftsqlserver-original", "SQL Server", False), ("mongodb-original", "MongoDB", False),
              ("si-netapp", "NetApp ONTAP S3 *", True)]
    ys = []
    for i, (lg, name, todo) in enumerate(stores):
        y = oy_ + 58 + i * 40
        ys.append(y + 17)
        c.rect(ox_ + 20, y, 290, 34, fill=RED_LT if todo else GREY_BG, stroke=RED if todo else GREY_BD,
               sw=2 if todo else 1.5, r=9, dash=todo)
        c.icon(lg, ox_ + 28, y + 4, 26)
        c.text(ox_ + 64, y + 24, name, 18, RED if todo else NAVY, True, w=240)

    sx, sy, sw_, sh = 440, 150, 334, 230
    c.rect(sx, sy, sw_, sh, fill=WHITE, stroke=PRIMARY, sw=3, r=16)
    c.rect(sx + 16, sy + 16, 56, 56, fill=LAV, stroke=None, shape=MSO_SHAPE.OVAL)
    c.icon("scan", sx + 24, sy + 24, 40, PRIMARY)
    c.text(sx + 86, sy + 40, "AccuKnox DSPM", 22, NAVY, True, w=230)
    c.text(sx + 86, sy + 66, "scanner", 22, NAVY, True, w=230)
    c.rect(sx + 20, sy + 88, 294, 34, fill=PRIMARY, stroke=None, r=17)
    c.text(sx + 167, sy + 111, "VM deployment for this PoC", 17, WHITE, True, anchor="middle", w=290)
    for i, ln in enumerate(["Reads the data stores", "Read-only access", "No inbound ports"]):
        c.icon("check", sx + 22, sy + 138 + i * 28, 20, GREEN)
        c.text(sx + 50, sy + 154 + i * 28, ln, 18, INK, w=260)
    for y in ys:
        last = y == ys[-1]
        c.line(sx - 2, sy + sh / 2, ox_ + 314, y, color=RED if last else PRIMARY, sw=2, dash=last)
    c.text(390, oy_ + 40, "read-only", 17, PRIMARY, True, anchor="middle", w=110)

    cx, cy, cw, ch = 900, 100, 344, 220
    c.rect(cx, cy, cw, ch, fill=NAVY, stroke=None, r=18)
    c.text(cx + 22, cy + 38, "AccuKnox control plane", 22, WHITE, True, w=310)
    c.text(cx + 22, cy + 64, "In Airtel's environment", 17, "#B8C4E8", w=300)
    c.rect(cx + 18, cy + 84, cw - 36, 78, fill=WHITE, stroke=None, r=12)
    c.icon("chart-bar", cx + 32, cy + 102, 40, PRIMARY)
    c.text(cx + 86, cy + 118, "AccuKnox console", 21, NAVY, True, w=230)
    c.text(cx + 86, cy + 144, "Findings and reports", 17, MUTE, w=230)
    c.icon("users-group", cx + 22, cy + 176, 28, "#FFFFFF")
    c.text(cx + 60, cy + 197, "Airtel security team", 18, WHITE, True, w=260)

    c.line(sx + sw_ + 2, 230, cx - 4, 222, color=GREEN, sw=3.5)
    c.text(848, 206, "Outbound", 17, GREEN_DK, True, anchor="middle", w=110)
    c.text(848, 262, "HTTPS 443", 17, GREEN_DK, True, anchor="middle", w=110)

    c.rect(cx, 344, cw, 96, fill=WHITE, stroke=MUTE, sw=2, r=14, dash=True)
    c.icon("package", cx + 20, 366, 40, MUTE)
    c.text(cx + 74, 384, "Container registry", 21, NAVY, True, w=250)
    c.text(cx + 74, 412, "Placement to confirm", 17, RED, True, w=250)

    c.line(sx + sw_ / 2, sy + sh + 2, sx + sw_ / 2, 484, color=PRIMARY, sw=2.5, dash=True)
    c.text(sx + sw_ / 2 - 12, 482, "Drive API", 17, PRIMARY, True, anchor="end", w=100)
    c.rect(sx + 50, 488, 240, 42, fill=WHITE, stroke=GREY_BD, sw=1.5, r=10)
    c.icon("si-googledrive", sx + 60, 494, 30)
    c.text(sx + 100, 516, "Google Drive (SaaS)", 18, NAVY, True, w=185)
    c.text(36, 504, "* NetApp ONTAP S3 needs a custom connector.", 17, RED, True, w=400)
    c.text(36, 527, "Readiness not confirmed.", 17, RED, True, w=400)
    return oy + 540 * K


def timeline(slide, ox, oy):
    c = Canvas(slide, ox, oy)
    days = [("Wed", "7"), ("Thu", "8"), ("Fri", "9"), ("Mon", "12"), ("Tue", "13"),
            ("Wed", "14"), ("Thu", "15"), ("Fri", "16"), ("Mon", "19"), ("Tue", "20"), ("Wed", "21")]
    L, R = 330, 1262
    dw = (R - L) / len(days)
    c.rect(L, 8, dw * 5 - 4, 34, fill=NAVY, stroke=None, r=8)
    c.text(L + (dw * 5 - 4) / 2, 32, "WEEK 1", 17, WHITE, True, anchor="middle", w=200)
    c.rect(L + dw * 5 + 4, 8, dw * 6 - 4, 34, fill=PRIMARY, stroke=None, r=8)
    c.text(L + dw * 5 + 4 + (dw * 6 - 4) / 2, 32, "WEEK 2", 17, WHITE, True, anchor="middle", w=200)
    for i, (d, n) in enumerate(days):
        x = L + i * dw
        c.rect(x + 3, 50, dw - 6, 52, fill=GREY_BG, stroke=None, r=8)
        c.text(x + dw / 2, 72, d, 17, MUTE, True, anchor="middle", w=dw - 6)
        c.text(x + dw / 2, 95, n + " Oct", 18, NAVY, True, anchor="middle", w=dw - 6)
        c.line(x, 108, x, 398, color=GREY_BG, sw=2, head=False)
    for wk in (3, 8):
        x = L + wk * dw
        c.line(x, 50, x, 398, color=GREY_BD, sw=2, dash=True, head=False)
    rows = [("server-cog", "On-prem deployment", "Control plane, scanner VM", 0, 2, NAVY, "2 days"),
            ("plug-connected", "Onboarding", "Read-only grants, first scan", 2, 4, PRIMARY, "First findings"),
            ("target", "Use case execution", "Run the six use cases", 4, 9, SECOND, "Six use cases, daily check-ins"),
            ("report-analytics", "Executive report", "Evidence, readout, closure", 9, 11, GREEN, "Readout 21 Oct")]
    for i, (ic, h, sub, a, z, col, lab) in enumerate(rows):
        y = 118 + i * 72
        c.rect(10, y + 4, 48, 48, fill=LAV, stroke=None, shape=MSO_SHAPE.OVAL)
        c.icon(ic, 16, y + 10, 36, PURPLE if col == SECOND else col)
        c.text(70, y + 24, h, 21, NAVY, True, w=255)
        c.text(70, y + 49, sub, 17, MUTE, w=255)
        x1, x2 = L + a * dw + 4, L + z * dw - 4
        c.rect(x1, y + 6, x2 - x1, 46, fill=col, stroke=None, r=12)
        c.text((x1 + x2) / 2, y + 36, lab, 18, WHITE, True, anchor="middle", w=x2 - x1 - 8)
    for xi, lab in ((0, "Kickoff"), (4, "Data stores live"), (11, "Go or no go")):
        x = L + xi * dw - (6 if xi == 11 else 0)
        c.rect(x - 10, 410, 20, 20, fill=RED, stroke=None, shape=MSO_SHAPE.DIAMOND)
        if xi == 11:
            c.text(x - 16, 427, lab, 17, RED, True, anchor="end", w=160)
        else:
            c.text(x + 16, 427, lab, 17, RED, True, w=180)
    return oy + 440 * K
