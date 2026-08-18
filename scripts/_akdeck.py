# -*- coding: utf-8 -*-
"""
Shared AccuKnox deck helpers, factored out of build_srilanka_banking.py so more than
one build script can use the same brand primitives.

Palette and fonts follow the repo README and assets/accuknox-brand-guidelines.pdf.
Icons come from the Segoe MDL2 Assets font, which PowerPoint COM renders reliably.
"""
import os
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image as PILImage

# ---- palette ------------------------------------------------------
NAVY     = RGBColor(0x11, 0x20, 0x6D)
NAVY_DK  = RGBColor(0x0A, 0x14, 0x4A)
BLACK    = RGBColor(0x00, 0x00, 0x00)
PRIMARY  = RGBColor(0x00, 0x46, 0xFF)
SECOND   = RGBColor(0x64, 0x64, 0xFF)
PURPLE   = RGBColor(0x4D, 0x4D, 0xD9)
RED      = RGBColor(0xC8, 0x00, 0x19)
RED_LT   = RGBColor(0xFB, 0xEC, 0xEE)
GREEN    = RGBColor(0x16, 0xA5, 0x5C)
GREEN_DK = RGBColor(0x0B, 0x7A, 0x42)
GREEN_LT = RGBColor(0xE7, 0xF6, 0xEE)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
INK      = RGBColor(0x1B, 0x22, 0x3B)
MUTE     = RGBColor(0x5A, 0x63, 0x7D)
GREY_BD  = RGBColor(0xC4, 0xCC, 0xDE)
GREY_BG  = RGBColor(0xEE, 0xF0, 0xF6)
LAV      = RGBColor(0xEC, 0xEC, 0xFB)
GREY_TX  = RGBColor(0x8A, 0x93, 0xA8)
NAVY_TXT = RGBColor(0xB8, 0xC4, 0xE8)
FONT     = "Space Grotesk"
MONO     = "Consolas"
ICF      = "Segoe MDL2 Assets"

IC = {
 'lock':0xE72E,'shield':0xE83D,'cloud':0xE753,'globe':0xE774,'pulse':0xE9D9,
 'doc':0xE8A5,'person':0xE7EE,'gear':0xE713,'gears':0xE9F5,'key':0xE8D7,
 'finger':0xE928,'bolt':0xE945,'warn':0xE7BA,'copy':0xE8C8,'check':0xE930,
 'flag':0xE7C1,'pie':0xEB05,'bulb':0xEB50,'server':0xE968,'devices':0xE977,
 'chip':0xE964,'swap':0xE8AB,'search':0xE721,'wrench':0xE90F,'clock':0xE81C,
 'star':0xE734,'books':0xE8F1,'wifi':0xEC3F,'cert':0xEB95,'eye':0xE890,
 'briefcase':0xE821,'list':0xE71D,'rocket':0xE7A7,'block':0xF140,'cancel':0xE711,
 'net':0xE968,'route':0xE7C0,'sitemap':0xF0E2,'link':0xE71B,'code':0xE943,
 'people':0xE716,'mail':0xE715,'chart':0xE9D2,'db':0xE81E,'firewall':0xE83D,
 'up':0xE74A,'down':0xE74B,'right':0xE72A,'terminal':0xE756,'bug':0xEBE8,
}
def G(name): return chr(IC[name])

# ---- geometry -----------------------------------------------------
CX, CW = 0.40, 9.20
RCOLX  = 4.98


# ===================================================================
def runs(p, text, font=None, size=12, bold=False, italic=False, color=None):
    """Write `text` into paragraph `p`, turning every newline into a real
    <a:br/> element.

    Do not put a raw newline inside <a:t>. python-pptx passes it straight
    through, PowerPoint's PNG export happens to break the line, and its PDF
    export draws a tofu box instead. Every helper below routes text through
    here so no build script has to remember this.
    """
    font = font or FONT
    color = INK if color is None else color
    for i, part in enumerate(text.split("\n")):
        if i:
            p._p.append(p._p.makeelement(qn("a:br"), {}))
        r = p.add_run()
        r.text = part
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return p


def set_title(slide, text, color=None):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0:
            ph.text_frame.paragraphs[0].text = text
            for r in ph.text_frame.paragraphs[0].runs:
                r.font.name = FONT
                if color is not None:
                    r.font.color.rgb = color
            return ph


def blank_footer(slide):
    """Clear the date and footer placeholders. Keeps the deck free of the
    'CLASSIFICATION: CONFIDENTIAL' style artifacts the source deck carried."""
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx in (10, 11):
            ph.text_frame.paragraphs[0].text = ""


def box(slide, x, y, w, h, text="", size=12, color=INK, bold=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, fill=None, line=None,
        line_w=0.75, shape=MSO_SHAPE.RECTANGLE, radius=None, italic=False,
        wrap=True, ml=0.08, mr=0.08, mt=0.04, mb=0.04, font=FONT, spacing=None):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    if radius is not None:
        try: sp.adjustments[0] = radius
        except Exception: pass
    tf = sp.text_frame; tf.word_wrap = wrap
    tf.margin_left=Inches(ml); tf.margin_right=Inches(mr)
    tf.margin_top=Inches(mt); tf.margin_bottom=Inches(mb)
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align
    if spacing is not None:
        p.line_spacing = spacing
    if text:
        runs(p, text, font=font, size=size, bold=bold, italic=italic, color=color)
    return sp


def para(shape, text, size=12, color=INK, bold=False, align=PP_ALIGN.LEFT,
         italic=False, space_before=0, space_after=4, first=False, font=FONT):
    tf = shape.text_frame
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align; p.space_before = Pt(space_before); p.space_after = Pt(space_after)
    runs(p, text, font=font, size=size, bold=bold, italic=italic, color=color)
    return p


def icon(slide, x, y, size, glyph, color=WHITE, bg=PRIMARY, radius=0.26, fsz=None):
    sp = box(slide, x, y, size, size, fill=bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
             radius=radius, anchor=MSO_ANCHOR.MIDDLE, wrap=False, ml=0, mr=0, mt=0, mb=0)
    p = sp.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = glyph
    r.font.name = ICF; r.font.size = Pt(fsz or size*42); r.font.color.rgb = color
    return sp


def image_fit(slide, path, x, y, w, h, caption=None, frame=GREY_BD, panel=None,
              capcolor=None, capsize=8.5):
    im = PILImage.open(path); ar = im.size[0]/im.size[1]
    if w/h > ar: dh=h; dw=h*ar
    else:        dw=w; dh=w/ar
    dx=x+(w-dw)/2; dy=y+(h-dh)/2
    if panel is not None:
        box(slide, x, y, w, h, fill=panel, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
    pic = slide.shapes.add_picture(path, Inches(dx), Inches(dy), Inches(dw), Inches(dh))
    if frame is not None:
        pic.line.color.rgb=frame; pic.line.width=Pt(1.0)
    pic.shadow.inherit = False
    if caption:
        box(slide, x, y+h+0.02, w, 0.26, text=caption, size=capsize, color=capcolor or MUTE,
            italic=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return pic


def card(slide, x, y, w, h, heading, body, accent=PRIMARY, hsize=12.5, bsize=10.2,
         ic=None, fill=WHITE, hcolor=NAVY, bcolor=MUTE):
    box(slide, x, y, w, h, fill=fill, line=GREY_BD, line_w=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    box(slide, x, y, w, 0.09, fill=accent, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    if ic:
        icon(slide, x+0.16, y+0.2, 0.42, G(ic), bg=accent)
        box(slide, x+0.66, y+0.16, w-0.8, 0.52, text=heading, size=hsize, color=hcolor,
            bold=True, anchor=MSO_ANCHOR.MIDDLE)
        box(slide, x+0.18, y+0.76, w-0.36, h-0.86, text=body, size=bsize, color=bcolor,
            anchor=MSO_ANCHOR.TOP)
    else:
        box(slide, x+0.16, y+0.18, w-0.32, 0.4, text=heading, size=hsize, color=hcolor, bold=True)
        box(slide, x+0.16, y+0.6, w-0.32, h-0.72, text=body, size=bsize, color=bcolor)


def stat(slide, x, y, w, number, label, color=PRIMARY, nsize=25, lsize=9.5, h=1.15,
         source=None, ssize=7.2):
    b = box(slide, x, y, w, h, fill=WHITE, line=GREY_BD, line_w=1.0,
            shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.09, anchor=MSO_ANCHOR.MIDDLE)
    para(b, number, size=nsize, color=color, bold=True, align=PP_ALIGN.CENTER, first=True, space_after=1)
    para(b, label, size=lsize, color=MUTE, align=PP_ALIGN.CENTER, space_after=0)
    if source:
        para(b, source, size=ssize, color=GREY_TX, align=PP_ALIGN.CENTER, space_before=2, space_after=0)
    return b


def pill(slide, x, y, w, h, text, fill=PRIMARY, tcolor=WHITE, size=10, bold=True):
    return box(slide, x, y, w, h, text=text, size=size, color=tcolor, bold=bold,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=fill,
               shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5, wrap=False)


def eyebrow(slide, text, x=CX, y=0.88, color=PRIMARY, w=7.6, size=10.5):
    return box(slide, x, y, w, 0.26, text=text.upper(), size=size, color=color,
               bold=True, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)


def footer_note(slide, text, color=MUTE, y=5.18, size=8.5):
    return box(slide, CX, y, CW, 0.28, text=text, size=size, color=color,
               italic=True, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)


def list_row(slide, x, y, w, glyph, head, sub, accent=PRIMARY, h=0.66, hsize=11.5,
             ssize=9.3, isz=0.4):
    icon(slide, x, y+0.02, isz, glyph, bg=accent)
    box(slide, x+isz+0.14, y-0.04, w-isz-0.14, 0.3, text=head, size=hsize, color=NAVY,
        bold=True, anchor=MSO_ANCHOR.BOTTOM, mb=0)
    box(slide, x+isz+0.14, y+0.26, w-isz-0.14, h-0.24, text=sub, size=ssize, color=MUTE,
        anchor=MSO_ANCHOR.TOP, mt=0)


def bullets(slide, x, y, w, h, items, size=11, color=INK, marker="▸", mcolor=None,
            gap=5, bold_lead=True):
    mcolor = mcolor or PRIMARY
    sp = box(slide, x, y, w, h, wrap=True, anchor=MSO_ANCHOR.TOP, ml=0.02, mr=0.04, mt=0.02)
    tf = sp.text_frame
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        if marker:
            rm=p.add_run(); rm.text=marker+"  "; rm.font.name=FONT; rm.font.size=Pt(size)
            rm.font.bold=True; rm.font.color.rgb=mcolor
        if isinstance(it, tuple):
            r1=p.add_run(); r1.text=it[0]; r1.font.name=FONT; r1.font.size=Pt(size)
            r1.font.bold=bold_lead; r1.font.color.rgb=color
            r2=p.add_run(); r2.text=it[1]; r2.font.name=FONT; r2.font.size=Pt(size); r2.font.color.rgb=color
        else:
            r=p.add_run(); r.text=it; r.font.name=FONT; r.font.size=Pt(size); r.font.color.rgb=color
    return sp


def table(slide, x, y, w, h, rows, colw=None, hsize=9.5, bsize=8.6, head_fill=NAVY,
          firstcol_fill=LAV, bold_firstcol=True, aligns=None):
    """rows[0] is the header row."""
    t = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y),
                              Inches(w), Inches(h)).table
    t.first_row = False; t.horz_banding = False
    if colw:
        for i, cw in enumerate(colw):
            t.columns[i].width = Inches(cw)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            c = t.cell(ri, ci)
            c.margin_left=Inches(0.08); c.margin_right=Inches(0.06)
            c.margin_top=Inches(0.03); c.margin_bottom=Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.fill.solid()
            if ri == 0:              c.fill.fore_color.rgb = head_fill
            elif ci == 0 and firstcol_fill is not None: c.fill.fore_color.rgb = firstcol_fill
            else:                    c.fill.fore_color.rgb = WHITE
            p = c.text_frame.paragraphs[0]
            if aligns: p.alignment = aligns[ci]
            r = p.add_run(); r.text = val; r.font.name = FONT
            r.font.size = Pt(hsize if ri == 0 else bsize)
            r.font.bold = (ri == 0 or (ci == 0 and bold_firstcol))
            r.font.color.rgb = WHITE if ri == 0 else NAVY
    return t


def code_block(slide, x, y, w, h, lines, size=8.6, fill=NAVY_DK, color=None,
               accent=SECOND, title=None):
    """A dark monospace panel. `lines` is a list of str, or (str, is_accent) tuples."""
    box(slide, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    ty = y
    if title:
        box(slide, x+0.14, y+0.06, w-0.28, 0.24, text=title, size=8, color=SECOND,
            bold=True, anchor=MSO_ANCHOR.MIDDLE)
        ty = y + 0.28
    sp = box(slide, x+0.14, ty+0.04, w-0.28, h-(ty-y)-0.1, anchor=MSO_ANCHOR.TOP,
             ml=0, mr=0, mt=0, mb=0)
    tf = sp.text_frame
    for i, ln in enumerate(lines):
        txt, acc = (ln, False) if isinstance(ln, str) else ln
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(1.5)
        r = p.add_run(); r.text = txt
        r.font.name = MONO; r.font.size = Pt(size)
        r.font.color.rgb = accent if acc else (color or NAVY_TXT)
        r.font.bold = acc
    return sp


def arrow(slide, x, y, w=0.26, h=0.26, color=PRIMARY, size=13):
    return box(slide, x, y, w, h, text="→", size=size, color=color, bold=True,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False,
               ml=0, mr=0, mt=0, mb=0)


# ===================================================================
# THE ONLY APPROVED COVER AND CLOSING SLIDES
# ===================================================================
# `PPT Template.pptx` already ships both of them as master layouts, complete
# with artwork that no script should try to redraw:
#
#   Layout 0, "AccuKnox Intro Title"   -> the FRONT cover. Carries the full
#       AccuKnox lockup with the "Secure Code to Cognition" tagline, the three
#       badge groups (Certified & Accredited by / As Featured In / Available
#       On) and the product screenshot collage on the right.
#   Layout 1, "AccuKnox Section Title" -> the BACK cover. Carries the centered
#       lockup, the "Certified by" badge row and www.AccuKnox.com.
#
# Only the words change. Never rebuild either one on a section layout, and
# never open or close a deck on the dark dotted-wave layout: that one is for
# part dividers, so a deck that uses it for the cover makes slide 1 and slide 2
# look identical.


def _ph(slide, idx):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == idx:
            return ph
    return None


def _drop_ph(slide, idx):
    ph = _ph(slide, idx)
    if ph is not None:
        ph._element.getparent().remove(ph._element)


def _move_ph(ph, top, height):
    """Reposition a placeholder vertically without losing its inherited x and
    width. Setting only `top` writes an <a:off>/<a:ext> whose other values
    default to 0, which collapses the box to a one-character column."""
    left, width = ph.left, ph.width
    ph.left, ph.width = left, width
    ph.top, ph.height = Inches(top), Inches(height)
    return left / 914400.0, width / 914400.0


def _fill_ph(ph, text, size, color, bold, align=PP_ALIGN.CENTER, spacing=None):
    tf = ph.text_frame
    tf.word_wrap = True
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = align
    if spacing is not None:
        p.line_spacing = spacing
    runs(p, text, size=size, bold=bold, color=color)
    return ph


def cover_slide(prs, title, scope=None, subtitle=None, tsize=25, ssize=11,
                y=1.86, h=1.20):
    """The AccuKnox front cover, on layout 0.

    Keep it light. The lockup, badges and screenshots already carry the brand,
    so the words are the title and, at most, one supporting line.

    title     the deck title, one or two lines
    scope     optional list of (number, label) drawn as a compact row under the
              title, for the two or three numbers that frame the deck
    subtitle  optional single line, used only when `scope` is not given
    """
    s = prs.slides.add_slide(prs.slide_layouts[0])
    blank_footer(s)
    ph = _ph(s, 0)
    tx, tw = _move_ph(ph, y, h)
    _fill_ph(ph, title, tsize, WHITE, True, spacing=1.0)
    if scope:
        _drop_ph(s, 1)
        cw = tw / len(scope)
        sy = y + h + 0.04
        for i, (num, lab) in enumerate(scope):
            cx = tx + i * cw
            box(s, cx, sy, cw, 0.34, text=num, size=17, color=WHITE, bold=True,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False,
                ml=0, mr=0)
            box(s, cx, sy + 0.32, cw, 0.24, text=lab, size=7.6, color=NAVY_TXT,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, ml=0, mr=0)
    elif subtitle:
        sub = _ph(s, 1)
        _move_ph(sub, y + h + 0.06, 0.44)
        _fill_ph(sub, subtitle, ssize, NAVY_TXT, False)
    else:
        _drop_ph(s, 1)
    return s


def closing_slide(prs, headline="SEE US IN ACTION",
                  contact="support@accuknox.com", tsize=22, csize=13):
    """The AccuKnox back cover, on layout 1. Change the words, nothing else."""
    s = prs.slides.add_slide(prs.slide_layouts[1])
    blank_footer(s)
    ph = _ph(s, 0)
    _move_ph(ph, 2.02, 0.62)
    _fill_ph(ph, headline, tsize, WHITE, True)
    sub = _ph(s, 1)
    if contact:
        _move_ph(sub, 2.66, 0.44)
        _fill_ph(sub, contact, csize, NAVY_TXT, False)
    else:
        _drop_ph(s, 1)
    return s
