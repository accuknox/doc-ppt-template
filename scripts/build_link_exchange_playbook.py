# -*- coding: utf-8 -*-
"""
Link Exchange and Guest Posts. A deck we can send to the people who ask.

Five content slides in two parts. Slides 2 and 3 are our own rules, written so a
partner can read them. Slides 4 to 6 tell the other side what to send us. The
source is the "[Kavitha] Link Exchange and Guest Posts" section of the 2026 Daily
Marketing Tasks doc, prepared 17 August 2026.

Everything internal stays out, because the whole file gets shared. No Tier 1 / 2 / 3
triage, no inbound thread counts, no mailbox names, no tracker columns and no
escalation threshold.

Two build rules this deck follows, both learned from Google Slides imports:
  - Icons are rasterised PNGs, never live Segoe MDL2 text. See glyph_png below.
  - Body copy is INK, not MUTE or GREY_TX, and no body text sits under 11pt.

Build:   py -3.11 scripts/build_link_exchange_playbook.py
Render:  powershell -File scripts/render.ps1 -Pptx output/AccuKnox_Link_Exchange_Playbook.pptx -Out output/render/linkex
"""
import os, shutil, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _akdeck import *          # noqa: F401,F403  brand palette + shape helpers

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "PPT Template.pptx")
OUT  = os.path.join(HERE, "..", "output", "AccuKnox_Link_Exchange_Playbook.pptx")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(SRC, OUT)
prs = Presentation(OUT)
L_STD = prs.slide_layouts[4]
xml_slides = prs.slides._sldIdLst
for sid in list(xml_slides):
    try: prs.part.drop_rel(sid.get(qn('r:id')))
    except Exception: pass
    xml_slides.remove(sid)


# ======================================================= portable icon glyphs
# Segoe MDL2 Assets ships only with Windows, and its icons sit in the Unicode
# private-use area. Google Slides has no fallback for a private-use codepoint,
# so a live glyph imports as a tofu box while the local PNG render still looks
# right. Rasterise each glyph once and place a picture instead. Cached under
# output/assets/glyphs, so a rebuild costs nothing.
GLYPHS   = os.path.join(HERE, "..", "output", "assets", "glyphs")
MDL2_TTF = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "segmdl2.ttf")
os.makedirs(GLYPHS, exist_ok=True)
_GCACHE = {}


def _rgb(c):
    h = str(c)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def glyph_png(glyph, color, px=320):
    """Return (path, aspect) for one MDL2 glyph drawn in `color` on transparency."""
    cp = ord(glyph)
    key = (cp, str(color))
    if key in _GCACHE:
        return _GCACHE[key]
    path = os.path.join(GLYPHS, "mdl2-%04X-%s.png" % (cp, str(color)))
    if not os.path.exists(path):
        from PIL import Image, ImageDraw, ImageFont
        f = ImageFont.truetype(MDL2_TTF, int(px * 0.78))
        im = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.text((px * 0.11, px * 0.11), glyph, font=f, fill=_rgb(color) + (255,))
        im = im.crop(im.getbbox())
        im.save(path)
    from PIL import Image as _I
    w, h = _I.open(path).size
    _GCACHE[key] = (path, w / float(h))
    return _GCACHE[key]


def glyph_pic(s, cx, cy, height, glyph, color, max_w=None):
    """Centre a glyph picture on (cx, cy) at the given height, in inches."""
    path, ar = glyph_png(glyph, color)
    w = height * ar
    if max_w and w > max_w:            # the wide glyphs must not touch the chip edge
        height *= max_w / w
        w = max_w
    return s.shapes.add_picture(path, Inches(cx - w / 2), Inches(cy - height / 2),
                                Inches(w), Inches(height))


def icon(s, x, y, size, glyph, color=WHITE, bg=PRIMARY, radius=0.26, fsz=None):
    """Same call shape as _akdeck.icon, but the glyph is a picture, not text."""
    sp = box(s, x, y, size, size, fill=bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
             radius=radius, wrap=False, ml=0, mr=0, mt=0, mb=0)
    glyph_pic(s, x + size / 2, y + size / 2, (fsz or size * 42) / 72.0 * 1.06,
              glyph, color, max_w=size * 0.66)
    return sp


import _akdeck                        # noqa: E402  patch the helpers that draw icons
_akdeck.icon = icon
_akdeck.IC['edit'] = 0xE70F           # pencil, for the two guest-post cards


# =================================================================== scaffold
# One type scale for the whole deck. Nothing readable falls below 11pt, and body
# copy is INK rather than MUTE, so the contrast holds on a projector.
T_LEDE, T_HEAD, T_BODY, T_SMALL = 13.0, 14.5, 12.0, 11.0

BLUE_TAG  = (PRIMARY, LAV)            # part 1, our rules
GREEN_TAG = (GREEN_DK, GREEN_LT)      # part 2, what we need from you


def std(title, part, lede=None, tag=BLUE_TAG, source=None):
    s = prs.slides.add_slide(L_STD); set_title(s, title); blank_footer(s)
    fg, bg = tag
    w = 0.115 * len(part) + 0.44
    box(s, CX, 0.80, w, 0.34, text=part.upper(), size=10.5, color=fg, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=bg, wrap=False,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5, ml=0, mr=0)
    if lede:
        box(s, CX, 1.18, CW, 0.34, text=lede, size=T_LEDE, color=INK,
            anchor=MSO_ANCHOR.MIDDLE, ml=0)
    if source:
        box(s, CX, 5.16, CW, 0.30, text=source, size=9.5, color=INK,
            anchor=MSO_ANCHOR.MIDDLE, ml=0)
    return s


def panel(s, x, y, w, h, head=None, accent=None, hcolor=NAVY):
    box(s, x, y, w, h, fill=WHITE, line=GREY_BD, line_w=1.25,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
    if accent is not None:
        box(s, x, y, w, 0.10, fill=accent, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    if head:
        box(s, x + 0.24, y + 0.16, w - 0.48, 0.32, text=head, size=T_HEAD,
            color=hcolor, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
        return y + 0.58
    return y + 0.18


def mark_list(s, x, y, w, items, glyph, color, gap=0.62, size=T_BODY):
    """A list with a rasterised tick or cross in front of every line."""
    for i, it in enumerate(items):
        yy = y + i * gap
        glyph_pic(s, x + 0.13, yy + 0.19, 0.19, glyph, color)
        box(s, x + 0.36, yy, w - 0.36, 0.38, text=it, size=size, color=INK,
            anchor=MSO_ANCHOR.MIDDLE, ml=0, mt=0, mb=0)


# =================================================================== 1. COVER
# Layout 0 carries the lockup, the badges and the product collage. Words only.
cover_slide(prs, "Link Exchange and Guest Posts",
            subtitle="How we trade links, and what we need from you", ssize=13)


# ============================================== 2. HOW WE WORK, THE THREE WAYS
s = std("Three ways we work with you", "Part 1 · How we work",
        "Every request we get is one of these three. Pick the one that fits you.")

WAYS = [
    # Only the paragraph break is hard. A newline inside a sentence fights the
    # box wrap and drops one orphan word onto a line of its own.
    ('swap', PRIMARY, "Link exchange",
     "We link to you and you link to us.\n\n"
     "Free in both directions. Your site must clear DR50 and cover "
     "cloud security, DevOps, AI or QA."),
    ('briefcase', PURPLE, "Paid listicle slot",
     "You want your product named in one of our comparison posts.\n\n"
     "We quote you a rate. You can pay it, or give us a dofollow link instead."),
    ('edit', GREEN_DK, "Guest post",
     "You write an article for the AccuKnox blog.\n\n"
     "No money moves either way. We edit it and we schedule it."),
]
cw = (CW - 2 * 0.19) / 3
for i, (ic, accent, head, body) in enumerate(WAYS):
    x = CX + i * (cw + 0.19)
    box(s, x, 1.66, cw, 3.28, fill=WHITE, line=GREY_BD, line_w=1.25,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, 1.66, cw, 0.10, fill=accent, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    icon(s, x + 0.24, 1.92, 0.62, G(ic), bg=accent, radius=0.24)
    box(s, x + 0.24, 2.66, cw - 0.44, 0.34, text=head, size=15.5, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.24, 3.04, cw - 0.44, 1.80, text=body, size=T_BODY, color=INK,
        anchor=MSO_ANCHOR.TOP, ml=0, mt=0)


# ================================================================ 3. OUR RULES
s = std("What we accept and what we refuse", "Part 1 · How we work",
        "Four rules on each side. One failure on the right closes the request.")

y0 = panel(s, CX, 1.60, 4.48, 3.32, head="We say yes when", accent=GREEN, hcolor=GREEN_DK)
mark_list(s, CX + 0.20, y0 + 0.14, 4.16, [
    "Your domain rating is 50 or higher.",
    "Your site covers cloud security,\nDevOps, AI or QA.",
    "You write from your company domain.",
    "Both links are dofollow and sit in\nreal body copy.",
], G('check'), GREEN_DK, gap=0.64)

y1 = panel(s, 5.12, 1.60, 4.48, 3.32, head="We say no when", accent=RED, hcolor=RED)
mark_list(s, 5.32, y1 + 0.14, 4.16, [
    "The mail comes from a free Gmail\naccount with no domain named.",
    "The domain does not belong to the\nbrand it claims.",
    "The site is a link farm or a private\nblog network.",
    "The site covers casinos, CBD, adult\nor any off topic subject.",
], G('cancel'), RED, gap=0.64)


# ======================================================= 4. WHAT WE NEED, LIST
s = std("Send us these five things", "Part 2 · What we need from you",
        "Put all five in your first email. Most requests then close in one round.",
        tag=GREEN_TAG)

ASK = [
    ("Your domain, and its domain rating",     "For example: example.com, DR62 on Ahrefs."),
    ("The page on your site that will link out", "Give the exact URL, not the home page."),
    ("The AccuKnox page you want a link to",   "For example: accuknox.com/platform/cnapp."),
    ("The anchor text you propose",            "Two to four words that match the page."),
    ("The date your link goes live",           "We publish ours on the same day."),
]
for i, (head, sub) in enumerate(ASK):
    y = 1.66 + i * 0.68
    box(s, CX, y, CW, 0.60, fill=GREY_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, CX + 0.14, y + 0.09, 0.42, 0.42, text=str(i + 1), size=15, color=WHITE,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=PRIMARY,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.22, wrap=False,
        ml=0, mr=0, mt=0, mb=0)
    box(s, CX + 0.70, y + 0.06, 4.90, 0.48, text=head, size=T_HEAD, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, 5.72, y + 0.06, 3.74, 0.48, text=sub, size=T_SMALL, color=INK,
        anchor=MSO_ANCHOR.MIDDLE, ml=0)


# ================================================== 5. GUEST POST, THREE STEPS
s = std("Writing a guest post for us", "Part 2 · What we need from you",
        "Three steps, and three terms we agree before you write a word.",
        tag=GREEN_TAG)

GP = [
    ('bulb',  "1. Pitch the topic",
     "Send two or three sentences. We check it against our calendar."),
    ('edit',  "2. Send the draft",
     "We send you our style guide the day we approve your topic."),
    ('check', "3. We edit and publish",
     "We check the technical accuracy, then we schedule the post."),
]
cw = 2.80
for i, (ic, head, body) in enumerate(GP):
    x = CX + i * (cw + 0.40)
    box(s, x, 1.66, cw, 1.94, fill=WHITE, line=GREY_BD, line_w=1.25,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    icon(s, x + 0.22, 1.86, 0.52, G(ic), bg=PRIMARY, radius=0.24)
    box(s, x + 0.84, 1.86, cw - 1.04, 0.52, text=head, size=T_HEAD, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.22, 2.50, cw - 0.42, 1.00, text=body, size=T_BODY, color=INK,
        anchor=MSO_ANCHOR.TOP, ml=0, mt=0)
    if i < 2:
        glyph_pic(s, x + cw + 0.20, 2.63, 0.24, G('right'), PRIMARY)

box(s, CX, 3.82, CW, 0.32, text="THE TERMS, AGREED UP FRONT", size=10.5,
    color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
TERMS = [
    ("No payment either way",   "We pay no writer, and you pay us nothing."),
    ("Original writing only",   "It must be unpublished, including on your own blog."),
    ("We hold editorial control", "We edit for accuracy, clarity and house style."),
]
tw = (CW - 2 * 0.16) / 3
for i, (head, sub) in enumerate(TERMS):
    x = CX + i * (tw + 0.16)
    box(s, x, 4.18, tw, 0.92, fill=LAV, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(s, x + 0.18, 4.24, tw - 0.36, 0.30, text=head, size=T_SMALL + 0.5, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.18, 4.52, tw - 0.36, 0.52, text=sub, size=T_SMALL, color=INK,
        anchor=MSO_ANCHOR.TOP, ml=0, mt=0)


# ================================================================= 6. WHAT NEXT
s = std("What happens after you write to us", "Part 2 · What we need from you",
        "We read new requests once a week, so expect our answer within seven days.",
        tag=GREEN_TAG)

FLOW = [
    ('mail',   "You send the five items",  "One email to the address below."),
    ('search', "We check your site",       "Domain rating, subject and link type."),
    ('swap',   "We agree it in writing",   "Both URLs, both anchors, one live date."),
    ('link',   "Both links go live",       "We re-check both of them after 30 days."),
]
fw = (CW - 3 * 0.12) / 4
for i, (ic, head, body) in enumerate(FLOW):
    x = CX + i * (fw + 0.12)
    box(s, x, 1.66, fw, 1.96, fill=WHITE, line=GREY_BD, line_w=1.25,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    box(s, x, 1.66, fw, 0.10, fill=PRIMARY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    icon(s, x + (fw - 0.56) / 2, 1.90, 0.56, G(ic), bg=PRIMARY, radius=0.24)
    box(s, x + 0.14, 2.56, fw - 0.28, 0.52, text=head, size=T_SMALL + 1.0, color=NAVY,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0)
    box(s, x + 0.14, 3.06, fw - 0.28, 0.50, text=body, size=T_SMALL, color=INK,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, ml=0, mt=0)

box(s, CX, 3.86, CW, 1.20, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
box(s, CX + 0.34, 4.02, 5.40, 0.36, text="Write to one address", size=T_HEAD,
    color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, ml=0)
box(s, CX + 0.34, 4.38, 5.40, 0.56,
    text="Put \"Link exchange\" or \"Guest post\" in the subject line, so it\nreaches the right person on the first day.",
    size=T_SMALL, color=WHITE, anchor=MSO_ANCHOR.TOP, ml=0, mt=0)
box(s, 6.10, 4.14, 3.34, 0.64, text="info@accuknox.com", size=17, color=WHITE,
    bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0, mr=0)


# =================================================================== 7. CLOSING
# Layout 1 carries the lockup, the "Certified by" row and www.AccuKnox.com.
closing_slide(prs, headline="LET'S TRADE LINKS", contact="info@accuknox.com")

prs.save(OUT)
print("saved:", os.path.abspath(OUT), "slides:", len(prs.slides._sldIdLst))
