# -*- coding: utf-8 -*-
"""
Diagrams for the Airtel DSPM PoC plan deck: the on-prem architecture and the
two-week timeline. Run before build_airtel_dspm_poc.py.

Sources: help.accuknox.com DSPM overview and onboarding pages, and the Airtel
PoC scoping call notes (OpenStack only, VM deployment, NetApp ONTAP connector TBC).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _aksvg import *  # noqa: F401,F403

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "airtel_dspm", "diagrams")


def architecture():
    """Draft layout agreed on the scoping call. Adapt Ayush's existing diagram before sending."""
    b = []
    # Airtel boundary
    b.append(rect(16, 44, 1248, 420, fill="#F7F8FC", stroke=NAVY, sw=2.5, r=18, dash="12 8"))
    b.append(ui("building", 34, 56, 32, NAVY))
    b.append(text(76, 80, "Airtel on-prem, private cloud", 23, NAVY, 700))

    # OpenStack box
    ox, oy, ow, oh = 36, 100, 760, 344
    b.append(rect(ox, oy, ow, oh, fill=WHITE, stroke=RED, sw=2, r=16))
    b.append(logo("si-openstack", ox + 18, oy + 14, 30, tint=RED))
    b.append(text(ox + 58, oy + 38, "OpenStack", 22, RED, 700))

    stores = [("si-openstack", "VM file systems", False), ("postgresql-original", "PostgreSQL 16+", False),
              ("mysql-original", "MySQL", False), ("mariadb-original", "MariaDB", False),
              ("microsoftsqlserver-original", "SQL Server", False), ("mongodb-original", "MongoDB", False),
              ("si-netapp", "NetApp ONTAP S3 *", True)]
    ys = []
    for i, (lg, name, todo) in enumerate(stores):
        y = oy + 58 + i * 40
        ys.append(y + 17)
        if todo:
            b.append(rect(ox + 20, y, 290, 34, fill=RED_LT, stroke=RED, sw=2, r=9, dash="6 5"))
            b.append(logo(lg, ox + 28, y + 4, 26, tint=RED))
            b.append(text(ox + 64, y + 24, name, 18, RED, 700))
        else:
            b.append(rect(ox + 20, y, 290, 34, fill=GREY_BG, stroke=GREY_BD, sw=1.5, r=9))
            b.append(logo(lg, ox + 28, y + 4, 26, tint=RED if lg == "si-openstack" else NAVY))
            b.append(text(ox + 64, y + 24, name, 18, NAVY, 600))

    # scanner
    sx, sy, sw_, sh = 440, 150, 334, 230
    b.append(rect(sx, sy, sw_, sh, fill=WHITE, stroke=PRIMARY, sw=3, r=16))
    b.append(f'<circle cx="{sx+44}" cy="{sy+44}" r="28" fill="{LAV}"/>')
    b.append(ui("scan", sx + 24, sy + 24, 40, PRIMARY))
    b.append(text(sx + 86, sy + 40, "AccuKnox DSPM", 22, NAVY, 700))
    b.append(text(sx + 86, sy + 66, "scanner", 22, NAVY, 700))
    b.append(pill(sx + 20, sy + 88, 300, 34, "VM deployment for this PoC", fill=PRIMARY, color=WHITE, size=17))
    for i, ln in enumerate(["Reads the data stores", "Read-only access", "No inbound ports"]):
        b.append(ui("check", sx + 22, sy + 138 + i * 28, 20, GREEN))
        b.append(text(sx + 50, sy + 154 + i * 28, ln, 18, INK, 500))
    for y in ys:
        col = RED if y == ys[-1] else PRIMARY
        b.append(arrow(sx - 2, sy + sh / 2, ox + 314, y, color=col, sw=2, dash="6 5" if col == RED else None))
    b.append(text(390, oy + 40, "read-only", 17, PRIMARY, 700, anchor="middle"))

    # control plane in Airtel's environment
    cx, cy, cw, ch = 900, 100, 344, 220
    b.append(rect(cx, cy, cw, ch, fill=NAVY, stroke=NAVY, r=18))
    b.append(text(cx + 22, cy + 38, "AccuKnox control plane", 22, WHITE, 700))
    b.append(text(cx + 22, cy + 64, "In Airtel's environment", 17, "#B8C4E8", 500))
    b.append(rect(cx + 18, cy + 84, cw - 36, 78, fill=WHITE, stroke=WHITE, r=12))
    b.append(ui("chart-bar", cx + 32, cy + 102, 40, PRIMARY))
    b.append(text(cx + 86, cy + 118, "AccuKnox console", 21, NAVY, 700))
    b.append(text(cx + 86, cy + 144, "Findings and reports", 17, MUTE, 500))
    b.append(ui("users-group", cx + 22, cy + 176, 28, "#FFFFFF"))
    b.append(text(cx + 60, cy + 197, "Airtel security team", 18, WHITE, 600))

    b.append(arrow(sx + sw_ + 2, 230, cx - 4, 222, color=GREEN, sw=3.5))
    b.append(text(848, 206, "Outbound", 17, GREEN_DK, 700, anchor="middle"))
    b.append(text(848, 262, "HTTPS 443", 17, GREEN_DK, 700, anchor="middle"))

    # registry, placement unconfirmed
    b.append(rect(cx, 344, cw, 96, fill=WHITE, stroke=MUTE, sw=2, r=14, dash="7 6"))
    b.append(ui("package", cx + 20, 366, 40, MUTE))
    b.append(text(cx + 74, 384, "Container registry", 21, NAVY, 700))
    b.append(text(cx + 74, 412, "Placement to confirm", 17, RED, 700))

    # Google Drive outside
    b.append(arrow(sx + sw_ / 2, sy + sh + 2, sx + sw_ / 2, 484, color=PRIMARY, sw=2.5, dash="6 5"))
    b.append(text(sx + sw_ / 2 - 12, 482, "Drive API", 17, PRIMARY, 600, anchor="end"))
    b.append(rect(sx + 50, 488, 240, 42, fill=WHITE, stroke=GREY_BD, sw=1.5, r=10))
    b.append(logo("si-googledrive", sx + 60, 494, 30, tint=PRIMARY))
    b.append(text(sx + 100, 516, "Google Drive (SaaS)", 18, NAVY, 600))
    b.append(text(36, 504, "* NetApp ONTAP S3 needs a custom connector.", 17, RED, 600))
    b.append(text(36, 527, "  Readiness not confirmed.", 17, RED, 600))
    return render("architecture", 1280, 540, "".join(b), OUT)


def timeline():
    days = [("Wed", "7"), ("Thu", "8"), ("Fri", "9"), ("Mon", "12"), ("Tue", "13"),
            ("Wed", "14"), ("Thu", "15"), ("Fri", "16"), ("Mon", "19"), ("Tue", "20"), ("Wed", "21")]
    L, R = 330, 1262
    dw = (R - L) / len(days)
    b = []
    b.append(rect(L, 8, dw * 5 - 4, 34, fill=NAVY, stroke=NAVY, r=8))
    b.append(text(L + (dw * 5 - 4) / 2, 32, "WEEK 1", 17, WHITE, 700, anchor="middle"))
    b.append(rect(L + dw * 5 + 4, 8, dw * 6 - 4, 34, fill=PRIMARY, stroke=PRIMARY, r=8))
    b.append(text(L + dw * 5 + 4 + (dw * 6 - 4) / 2, 32, "WEEK 2", 17, WHITE, 700, anchor="middle"))
    for i, (d, n) in enumerate(days):
        x = L + i * dw
        b.append(rect(x + 3, 50, dw - 6, 52, fill=GREY_BG, stroke="none", r=8))
        b.append(text(x + dw / 2, 72, d, 17, MUTE, 600, anchor="middle"))
        b.append(text(x + dw / 2, 95, n + " Oct", 18, NAVY, 700, anchor="middle"))
        b.append(f'<line x1="{x}" y1="108" x2="{x}" y2="398" stroke="{GREY_BG}" stroke-width="2"/>')
    for wk in (3, 8):   # weekend gaps before Mon 12 and Mon 19
        x = L + wk * dw
        b.append(f'<line x1="{x}" y1="50" x2="{x}" y2="398" stroke="{GREY_BD}" stroke-width="2" stroke-dasharray="5 5"/>')
    rows = [("server-cog", "On-prem deployment", "Control plane, scanner VM", 0, 2, NAVY, "2 days"),
            ("plug-connected", "Onboarding", "Read-only grants, first scan", 2, 4, PRIMARY, "First findings"),
            ("target", "Use case execution", "Run the six use cases", 4, 9, SECOND, "Six use cases, daily check-ins"),
            ("report-analytics", "Executive report", "Evidence, readout, closure", 9, 11, GREEN, "Readout 21 Oct")]
    for i, (ic, h, s, a, z, col, lab) in enumerate(rows):
        y = 118 + i * 72
        b.append(f'<circle cx="34" cy="{y+28}" r="24" fill="{LAV}"/>')
        b.append(ui(ic, 16, y + 10, 36, col if col != SECOND else PURPLE))
        b.append(text(70, y + 24, h, 21, NAVY, 700))
        b.append(text(70, y + 49, s, 17, MUTE, 500))
        x1, x2 = L + a * dw + 4, L + z * dw - 4
        b.append(rect(x1, y + 6, x2 - x1, 46, fill=col, stroke=col, r=12))
        b.append(text((x1 + x2) / 2, y + 36, lab, 18, WHITE, 700, anchor="middle"))
    # milestones
    for xi, lab in ((0, "Kickoff"), (4, "Data stores live"), (11, "Go or no go")):
        x = L + xi * dw - (6 if xi == 11 else 0)
        b.append(f'<path d="M{x},{410} l10,10 l-10,10 l-10,-10 z" fill="{RED}"/>')
        b.append(text(x + (-16 if xi == 11 else 16), 427, lab, 17, RED, 700, anchor="end" if xi == 11 else "start"))
    return render("timeline", 1280, 440, "".join(b), OUT)


if __name__ == "__main__":
    for f in (architecture, timeline):
        print(f())
