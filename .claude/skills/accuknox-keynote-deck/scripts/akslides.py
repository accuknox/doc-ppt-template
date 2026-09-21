# -*- coding: utf-8 -*-
"""akslides: the AccuKnox keynote deck runtime.

One import gives you the brand tokens, the drawing primitives and thirteen slide
layouts that share one visual system: a navy canvas, white product screens as
the light source, one idea per slide.

    from akslides import Deck, T

    d = Deck("AccuKnox_Acme_Overview", accent=T.PRIMARY)
    d.cover("Runtime Security for Acme", "One agent, every cluster.")
    d.stats({"title": "Three Numbers Decide the Pilot",
             "items": [("30,000", "devices onboarded in a week", "case study", URL)]})
    d.close()
    d.save()

Every layout takes a title that states a claim, and every layout leaves room for
a source footnote. That pairing is what makes a deck read as evidence rather
than as marketing.

Run with py -3.11, which is the interpreter that carries python-pptx, lxml and
Pillow on this machine.
"""
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE  # noqa: F401  (re-exported for callers)
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

# The brand template and the logos stay in one place, so a brand refresh lands once.
BRAND_REPO = Path(__file__).resolve().parents[4]
TEMPLATE = BRAND_REPO / "PPT Template.pptx"
LOGO_DARK = BRAND_REPO / "assets" / "logos" / "accuknox-logo-dark-bg.png"
LOGO_LIGHT = BRAND_REPO / "assets" / "logos" / "accuknox-logo-light-bg.png"
OUTDIR = BRAND_REPO / "output"


class T:
    """Brand tokens. Never invent a hue: these come from the brand guidelines."""

    NAVY = RGBColor(0x11, 0x20, 0x6D)       # the canvas
    NAVY_DK = RGBColor(0x0A, 0x14, 0x4A)    # panels that must sit back
    PRIMARY = RGBColor(0x00, 0x46, 0xFF)    # accent one
    SECOND = RGBColor(0x64, 0x64, 0xFF)     # accent two
    PURPLE = RGBColor(0x4D, 0x4D, 0xD9)
    RED = RGBColor(0xC8, 0x00, 0x19)        # block, risk, "before"
    GREEN = RGBColor(0x16, 0xA5, 0x5C)      # allow, pass, "after"
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    INK = RGBColor(0x1B, 0x22, 0x3B)        # body text on white
    MUTE = RGBColor(0x5A, 0x63, 0x7D)
    SOFT = RGBColor(0xB8, 0xC4, 0xE8)       # secondary text on navy
    FONT = "Space Grotesk"
    MED = "Space Grotesk Medium"
    SEMI = "Space Grotesk SemiBold"


SW, SH = 10.0, 5.625     # slide size in inches, 16:9
M = 0.55                 # side margin. Nothing important crosses it.
TOP = 0.40               # title row
BODY = 1.45              # first row of content


# ---------------------------------------------------------------- XML helpers
def _alpha(parent, alpha):
    clr = parent.find(qn("a:solidFill")).find(qn("a:srgbClr"))
    etree.SubElement(clr, qn("a:alpha")).set("val", str(int(alpha * 1000)))


def fill(sp, rgb, alpha=None):
    """Solid fill, with an optional alpha in percent.

    Alpha is how this deck gets depth without inventing colors. White at 6 to 16
    percent over navy reads as a raised card, and the palette stays closed."""
    sp.fill.solid()
    sp.fill.fore_color.rgb = rgb
    if alpha is not None:
        _alpha(sp._element.spPr, alpha)


def stroke(sp, rgb, w=0.75, alpha=None, dash=None):
    sp.line.color.rgb = rgb
    sp.line.width = Pt(w)
    if dash is not None:
        sp.line.dash_style = dash
    if alpha is not None:
        _alpha(sp._element.spPr.find(qn("a:ln")), alpha)


def shadow(sp, blur=18, dist=6, alpha=40):
    spPr = sp._element.spPr
    eff = spPr.find(qn("a:effectLst"))
    if eff is None:
        eff = etree.SubElement(spPr, qn("a:effectLst"))
    for child in list(eff):
        eff.remove(child)
    sh = etree.SubElement(eff, qn("a:outerShdw"))
    sh.set("blurRad", str(Pt(blur)))
    sh.set("dist", str(Pt(dist)))
    sh.set("dir", "5400000")
    sh.set("algn", "t")
    sh.set("rotWithShape", "0")
    clr = etree.SubElement(sh, qn("a:srgbClr"))
    clr.set("val", "000000")
    etree.SubElement(clr, qn("a:alpha")).set("val", str(int(alpha * 1000)))


def round_pic(pic, adj=0.02):
    geom = pic._element.spPr.find(qn("a:prstGeom"))
    geom.set("prst", "roundRect")
    av = geom.find(qn("a:avLst"))
    if av is None:
        av = etree.SubElement(geom, qn("a:avLst"))
    gd = etree.SubElement(av, qn("a:gd"))
    gd.set("name", "adj")
    gd.set("fmla", f"val {int(adj * 100000)}")


def char_spacing(sp, pts):
    for p in sp.text_frame.paragraphs:
        for r in p.runs:
            r.font._rPr.set("spc", str(int(pts * 100)))


def runs(p, value, font=T.FONT, size=12, bold=False, italic=False, color=T.WHITE):
    """Write text, turning every newline into a real <a:br/>.

    A raw newline inside <a:t> survives the PNG export and then draws a tofu box
    in the PDF, so every helper here routes through this function."""
    for i, part in enumerate(str(value).split("\n")):
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


# ------------------------------------------------------------------ primitives
def box(slide, x, y, w, h, value="", size=12, color=T.WHITE, font=T.FONT, bold=False,
        italic=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, shape=MSO_SHAPE.RECTANGLE,
        radius=None, spacing=None, margin=0.0):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.background()
    sp.line.fill.background()
    sp.shadow.inherit = False
    if radius is not None:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    tf = sp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(0)
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    if spacing is not None:
        p.line_spacing = spacing
    if value != "":
        runs(p, value, font=font, size=size, bold=bold, italic=italic, color=color)
    return sp


def panel(slide, x, y, w, h, alpha=6, line_alpha=16, radius=0.06, color=T.WHITE,
          line_color=T.WHITE, dash=None):
    """A translucent card."""
    sp = box(slide, x, y, w, h, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)
    if alpha:
        fill(sp, color, alpha)
    if line_alpha:
        stroke(sp, line_color, 0.75, line_alpha, dash)
    return sp


def hline(slide, x, y, w, color=T.WHITE, alpha=22, weight=0.75):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                    Inches(x + w), Inches(y))
    stroke(ln, color, weight, alpha)
    return ln


def arrow(slide, x1, y1, x2, y2, color=T.WHITE, alpha=45, weight=1.25, dash=None, head=True):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                    Inches(x2), Inches(y2))
    stroke(ln, color, weight, alpha, dash)
    if head:
        te = etree.SubElement(ln._element.spPr.find(qn("a:ln")), qn("a:tailEnd"))
        te.set("type", "triangle")
        te.set("w", "med")
        te.set("len", "med")
    return ln


def pin(slide, cx, cy, n, color, d=0.30, size=11):
    """A numbered marker.

    Put it beside the thing it names, never on top of the label, or the pin
    hides the evidence it points at."""
    sp = box(slide, cx - d / 2, cy - d / 2, d, d, value=str(n), size=size, color=T.WHITE,
             bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shape=MSO_SHAPE.OVAL)
    fill(sp, color)
    stroke(sp, T.WHITE, 1.5)
    shadow(sp, blur=6, dist=2, alpha=45)
    return sp


def chip(slide, x, y, label, fg=T.WHITE, bg=None, bg_alpha=None, line_c=None,
         line_alpha=None, size=7.5, h=0.24, w=None, dash=None, cs=0.8):
    if w is None:
        w = len(str(label)) * (size * 0.64 + cs) / 72 + 0.22
    sp = box(slide, x, y, w, h, value=label, size=size, color=fg, font=T.SEMI,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    if bg is not None:
        fill(sp, bg, bg_alpha)
    if line_c is not None:
        stroke(sp, line_c, 0.75, line_alpha, dash)
    char_spacing(sp, cs)
    return sp


def glow(slide, x, y, w, h, color, alpha=34, soft=70):
    """A soft accent light behind a screen. Draw it before the picture."""
    sp = box(slide, x, y, w, h, shape=MSO_SHAPE.OVAL)
    fill(sp, color, alpha)
    eff = sp._element.spPr.find(qn("a:effectLst"))
    if eff is None:
        eff = etree.SubElement(sp._element.spPr, qn("a:effectLst"))
    etree.SubElement(eff, qn("a:softEdge")).set("rad", str(Pt(soft)))
    return sp


def picture(slide, path, x, y, w=None, h=None, radius=0.02, line_alpha=26,
            blur=22, dist=8, alpha=45):
    """Place an image by width or by height, keeping its aspect ratio.

    Returns (shape, width, height, px_w, px_h), so a caller can map a pixel
    coordinate in the source image to slide inches and drop a pin on it."""
    im = Image.open(path)
    if w is None:
        w = h * im.width / im.height
    h = w * im.height / im.width
    pic = slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    round_pic(pic, radius)
    stroke(pic, T.WHITE, 0.75, line_alpha)
    shadow(pic, blur=blur, dist=dist, alpha=alpha)
    return pic, w, h, im.width, im.height


def link(sp, url):
    sp.click_action.hyperlink.address = url


def lines_for(value, chars_per_line):
    """Rough line count, used to place an attribution under a quote."""
    words, count, cur = str(value).split(), 1, 0
    for wd in words:
        if cur and cur + 1 + len(wd) > chars_per_line:
            count, cur = count + 1, len(wd)
        else:
            cur = cur + (1 if cur else 0) + len(wd)
    return count


# ----------------------------------------------------------- template plumbing
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
    """Reposition a placeholder without losing its inherited x and width.

    Setting only `top` writes an offset whose other values default to zero,
    which collapses the box to a one-character column."""
    left, width = ph.left, ph.width
    ph.left, ph.width = left, width
    ph.top, ph.height = Inches(top), Inches(height)
    return left / 914400.0, width / 914400.0


def _fill_ph(ph, value, size, color, bold, align=PP_ALIGN.CENTER, spacing=None):
    tf = ph.text_frame
    tf.word_wrap = True
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = align
    if spacing is not None:
        p.line_spacing = spacing
    runs(p, value, size=size, bold=bold, color=color)
    return ph


def blank_footer(slide):
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx in (10, 11):
            ph.text_frame.paragraphs[0].text = ""


class Deck:
    """A deck in the AccuKnox keynote style.

    The cover and the closing slide come from the brand template, so nobody
    redraws the lockup or the badge rows. Everything between them sits on the
    Blank layout with a navy canvas."""

    def __init__(self, name, accent=T.PRIMARY, outdir=OUTDIR, template=TEMPLATE,
                 logo=LOGO_DARK):
        self.name = name
        self.accent = accent
        self.outdir = Path(outdir)
        self.logo = Path(logo)
        self.prs = Presentation(str(template))
        ids = self.prs.slides._sldIdLst
        for sid in list(ids):
            self.prs.part.drop_rel(sid.rId)
            ids.remove(sid)

    # -- scaffolding --------------------------------------------------------
    def _slide(self):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[7])
        blank_footer(s)
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = T.NAVY
        if self.logo.exists():
            s.shapes.add_picture(str(self.logo), Inches(SW - M - 1.2), Inches(0.46),
                                 width=Inches(1.2))
        return s

    def title(self, s, value, w=7.3, size=22, y=TOP):
        """Titles state a claim in AP Title Case.

        Break a long title yourself with \\n so no single word is orphaned on
        the second line. PowerPoint will not balance it for you."""
        return box(s, M, y, w, 1.1, value, size, T.WHITE, font=T.MED, spacing=0.95)

    def footnote(self, s, value, y=5.34):
        """Where the facts came from.

        A deck that cites its own sources survives the technical reviewer in the
        room, and the seller can answer "where does that number come from"."""
        return box(s, M, y, SW - 2 * M, 0.24, value, 8, T.SOFT) if value else None

    def notes(self, s, value):
        if value:
            s.notes_slide.notes_text_frame.text = value

    def _finish(self, s, D):
        self.footnote(s, D.get("footnote"), D.get("foot_y", 5.34))
        self.notes(s, D.get("notes"))
        return s

    def strip(self, s, items, y=4.7, label=None, w=None):
        """A row of short facts under a diagram: a timeline, a set of risks, a
        set of capabilities. Each item is (head, sub) or a plain string."""
        w = w or (SW - 2 * M)
        hline(s, M, y, w, alpha=18)
        x = M
        if label:
            c = box(s, M, y + 0.14, 1.75, 0.22, label, 7, T.WHITE, font=T.SEMI)
            char_spacing(c, 1.2)
            x = M + 1.9
        cw = (w - (x - M)) / len(items)
        for i, item in enumerate(items):
            cx = x + i * cw
            if isinstance(item, (tuple, list)):
                box(s, cx, y + 0.12, cw - 0.2, 0.24, item[0], 10, T.WHITE, font=T.SEMI)
                box(s, cx, y + 0.36, cw - 0.25, 0.4, item[1], 8.5, T.SOFT, spacing=1.05)
            else:
                box(s, cx, y + 0.12, cw - 0.2, 0.24, item, 9, T.SOFT)

    def chips(self, s, label, items, y=4.95, x=None, max_x=None):
        """A labelled row of short chips. `max_x` keeps the row clear of an
        image on the right: the row wraps down rather than sliding under it."""
        x0 = M if x is None else x
        x, limit = x0, max_x or (SW - M)
        if label:
            c = box(s, x, y + 0.04, 2.1, 0.22, label, 7, T.WHITE, font=T.SEMI)
            char_spacing(c, 1.2)
            x += min(2.2, len(label) * 0.075 + 0.5)
        for item in items:
            w = len(str(item)) * (8 * 0.64 + 0.8) / 72 + 0.22
            if x + w > limit:
                x, y = x0, y + 0.36
            c = chip(s, x, y, item, fg=T.WHITE, bg=T.WHITE, bg_alpha=12, line_c=T.WHITE,
                     line_alpha=26, size=8, h=0.28)
            x += c.width / 914400 + 0.12
        return x

    def rail(self, s, items, top=1.62, step=0.9, w=2.2, numbered=True):
        """The left column that names what the picture on the right shows."""
        for i, (head, sub) in enumerate(items):
            y = top + i * step
            if numbered:
                pin(s, M + 0.15, y + 0.14, i + 1, self.accent)
                hx = 0.98
            else:
                hline(s, M, y, w + 0.3, alpha=18)
                hline(s, M, y, 0.4, color=self.accent, alpha=None, weight=2.0)
                hx, y = M, y + 0.12
            head_lines = lines_for(head, int(w * 9.5))
            box(s, hx, y, w, 0.3 * head_lines, head, 12, T.WHITE, font=T.SEMI, spacing=1.0)
            box(s, hx, y + 0.02 + 0.27 * head_lines, w - 0.1, 0.56, sub, 9.5, T.SOFT,
                spacing=1.08)

    def node(self, s, x, y, w, h, label, sub=None, accent=None, size=11, alpha=8,
             line_color=T.WHITE, line_alpha=35):
        n = panel(s, x, y, w, h, alpha=alpha, line_alpha=None if accent else line_alpha,
                  radius=0.1, line_color=line_color)
        if accent:
            stroke(n, accent, 1.25)
        if sub:
            box(s, x + 0.14, y + 0.1, w - 0.28, 0.26, label, size, T.WHITE, font=T.SEMI)
            box(s, x + 0.14, y + 0.34, w - 0.28, h - 0.42, sub, 8.5, T.SOFT, spacing=1.05)
        else:
            box(s, x, y, w, h, label, size, T.WHITE, font=T.SEMI, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE, spacing=1.05)
        return n

    # -- layouts ------------------------------------------------------------
    def cover(self, title, subtitle=None, scope=None, tsize=25):
        """Template layout 0. Keep it light: a title plus one line, or a short
        row of scope numbers. The lockup and the badges carry the brand."""
        s = self.prs.slides.add_slide(self.prs.slide_layouts[0])
        blank_footer(s)
        ph = _ph(s, 0)
        tx, tw = _move_ph(ph, 1.86, 1.20)
        _fill_ph(ph, title, tsize, T.WHITE, True, spacing=1.0)
        if scope:
            _drop_ph(s, 1)
            cw = tw / len(scope)
            for i, (num, lab) in enumerate(scope):
                cx = tx + i * cw
                box(s, cx, 3.10, cw, 0.34, num, 17, T.WHITE, font=T.MED,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
                box(s, cx, 3.42, cw, 0.24, lab, 7.6, T.SOFT, align=PP_ALIGN.CENTER)
        elif subtitle:
            sub = _ph(s, 1)
            _move_ph(sub, 3.12, 0.44)
            _fill_ph(sub, subtitle, 11, T.SOFT, False)
        else:
            _drop_ph(s, 1)
        return s

    def close(self, headline="SEE US IN ACTION", contact="support@accuknox.com"):
        """Template layout 1. Change the words, nothing else."""
        s = self.prs.slides.add_slide(self.prs.slide_layouts[1])
        blank_footer(s)
        ph = _ph(s, 0)
        _move_ph(ph, 2.02, 0.62)
        _fill_ph(ph, headline, 22, T.WHITE, True)
        sub = _ph(s, 1)
        if contact:
            _move_ph(sub, 2.66, 0.44)
            _fill_ph(sub, contact, 13, T.SOFT, False)
        else:
            _drop_ph(s, 1)
        return s

    def section(self, D):
        """A part divider: one claim, a rule, an optional line.

        Use it sparingly, because every divider spends a slide of attention."""
        s = self._slide()
        if D.get("number"):
            c = box(s, M, 2.05, 1.0, 0.3, D["number"], 9, T.SOFT, font=T.SEMI)
            char_spacing(c, 1.4)
        box(s, M, 2.35, 7.6, 1.3, D["title"], 34, T.WHITE, font=T.MED, spacing=0.95)
        hline(s, M, 3.78, 1.4, color=self.accent, alpha=None, weight=2.5)
        if D.get("sub"):
            box(s, M, 3.95, 6.4, 0.5, D["sub"], 12, T.SOFT, spacing=1.1)
        return self._finish(s, D)

    def statement(self, D):
        """One claim and up to four supporting lines.

        Every deck needs this layout for the moment where the point is an
        argument rather than a picture."""
        s = self._slide()
        self.title(s, D["title"], w=8.0, size=28)
        y = D.get("body_y", 1.55 + 0.46 * lines_for(D["title"], 40))
        if D.get("lead"):
            box(s, M, y, 6.8, 0.9, D["lead"], 13, T.SOFT, spacing=1.15)
            y += 0.34 + 0.24 * lines_for(D["lead"], 76)
        for i, point in enumerate(D.get("points", [])):
            hline(s, M, y + i * 0.62, SW - 2 * M, alpha=16)
            box(s, M, y + i * 0.62 + 0.12, 8.6, 0.36, point, 11.5, T.WHITE, spacing=1.05)
        return self._finish(s, D)

    def agenda(self, D):
        """Numbered rows. Each row names what its section proves."""
        s = self._slide()
        self.title(s, D["title"])
        items = D["items"]
        step = min(0.72, 3.6 / max(len(items), 1))
        for i, item in enumerate(items):
            y = BODY + i * step
            head, sub = item if isinstance(item, (tuple, list)) else (item, None)
            box(s, M, y, 0.42, 0.42, f"{i + 1:02d}", 13, T.WHITE, font=T.MED,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            hline(s, M, y + 0.5, SW - 2 * M, alpha=14)
            box(s, M + 0.62, y + 0.02, 5.2, 0.3, head, 13, T.WHITE, font=T.SEMI)
            if sub:
                box(s, SW - M - 3.0, y + 0.04, 3.0, 0.3, sub, 9.5, T.SOFT)
        return self._finish(s, D)

    def stats(self, D):
        """Three or four numbers, set large.

        Each number carries its unit and its source, because a number with no
        source is decoration."""
        s = self._slide()
        self.title(s, D["title"])
        items = D["items"]
        gap = 0.3
        w = (SW - 2 * M - gap * (len(items) - 1)) / len(items)
        size = D.get("size", 54 if len(items) <= 3 else 42)
        for i, item in enumerate(items):
            x = M + i * (w + gap)
            hline(s, x, BODY + 0.5, w, alpha=22)
            hline(s, x, BODY + 0.5, 0.5, color=self.accent, alpha=None, weight=2.0)
            box(s, x, BODY + 0.66, w, 1.0, item[0], size, T.WHITE, font=T.MED, spacing=0.9)
            label_lines = lines_for(item[1], int((w - 0.15) * 15))
            box(s, x, BODY + 1.75, w - 0.15, 0.9, item[1], 11, T.SOFT, spacing=1.1)
            if len(item) > 2 and item[2]:
                l = box(s, x, BODY + 1.82 + 0.22 * label_lines, w - 0.15, 0.24, item[2],
                        7.5, T.SOFT)
                if len(item) > 3 and item[3]:
                    link(l, item[3])
        return self._finish(s, D)

    def compare(self, D):
        """Before and after, or the old stack and the new one.

        Red on the left, accent on the right, one row per claim so the eye can
        scan across rather than down."""
        s = self._slide()
        self.title(s, D["title"])
        cw = (SW - 2 * M - 0.4) / 2
        for col, (head, color) in enumerate(zip(D.get("heads", ("BEFORE", "AFTER")),
                                                (T.RED, self.accent))):
            x = M + col * (cw + 0.4)
            c = box(s, x, BODY, cw, 0.32, head, 8, T.WHITE, font=T.SEMI)
            char_spacing(c, 1.2)
            hline(s, x, BODY + 0.34, cw, color=color, alpha=None, weight=2.0)
        for r, (left, right) in enumerate(D["rows"]):
            y = BODY + 0.58 + r * D.get("row_h", 0.78)
            for col, value in enumerate((left, right)):
                x = M + col * (cw + 0.4)
                box(s, x, y, 0.3, 0.3, "✕" if col == 0 else "✓", 11,
                    T.RED if col == 0 else T.GREEN, font=T.SEMI)
                box(s, x + 0.34, y - 0.02, cw - 0.4, 0.62, value, 11, T.WHITE, spacing=1.08)
        return self._finish(s, D)

    def timeline(self, D):
        """A journey across the slide.

        Use it when the sequence is the argument: day 0, minutes, hours, day 7."""
        s = self._slide()
        self.title(s, D["title"])
        items = D["items"]
        y = D.get("y", 2.7)
        hline(s, M, y, SW - 2 * M, alpha=22)
        step = (SW - 2 * M) / len(items)
        for i, (stamp, head, sub) in enumerate(items):
            x = M + i * step
            dot = box(s, x - 0.06, y - 0.06, 0.12, 0.12, shape=MSO_SHAPE.OVAL)
            fill(dot, self.accent)
            box(s, x, y - 0.62, step - 0.25, 0.3, stamp, 13, T.WHITE, font=T.MED)
            box(s, x, y + 0.22, step - 0.25, 0.3, head, 11.5, T.WHITE, font=T.SEMI)
            box(s, x, y + 0.5, step - 0.3, 0.7, sub, 9, T.SOFT, spacing=1.08)
        return self._finish(s, D)

    def image(self, D):
        """One large image with a rail of facts beside it.

        The workhorse for a logo wall, a report page, a parity card or any
        picture that carries the argument on its own."""
        s = self._slide()
        self.title(s, D["title"], w=D.get("title_w", 7.4))
        iy = D.get("img_y", 1.55)
        if D.get("img_h") and not D.get("img_w"):
            im = Image.open(D["image"])
            iw = D["img_h"] * im.width / im.height
        else:
            iw = D.get("img_w", 6.0)
        ix = D["img_x"] if D.get("img_x") is not None else SW - M - iw
        if D.get("glow", True):
            glow(s, ix + 0.5, iy + 0.3, max(iw - 1.0, 1.0), 2.4, self.accent, alpha=32, soft=60)
        pic, w, h, pw, ph = picture(s, D["image"], ix, iy, iw, radius=D.get("radius", 0.03))
        if D.get("rail"):
            self.rail(s, D["rail"], top=D.get("rail_top", 1.6), step=D.get("rail_step", 0.86),
                      w=D.get("rail_w", 2.5), numbered=D.get("numbered", False))
        for n, px, py in D.get("pins", []):
            pin(s, ix + px / pw * w, iy + py / ph * h, n, self.accent)
        if D.get("chips"):
            limit = ix - 0.15 if iy + h > D.get("chips_y", 4.95) else SW - M
            self.chips(s, D["chips"][0], D["chips"][1], y=D.get("chips_y", 4.95), max_x=limit)
        return self._finish(s, D)

    def annotated(self, D):
        """A product screen that runs off the edge, numbered pins on the real
        widgets, and a rail that says what each pin proves.

        This is the layout that makes a deck feel like the product rather than
        like a brochure, so give it the best screenshot you have."""
        s = self._slide()
        self.title(s, D["title"], w=D.get("title_w", 7.4))
        X, Y, W = D.get("img_x", 3.30), D.get("img_y", 1.45), D.get("img_w", 6.95)
        glow(s, X + 0.6, Y + 0.5, 5.2, 3.4, self.accent, alpha=40, soft=80)
        pic, w, h, pw, ph = picture(s, D["main"], X, Y, W, radius=0.018)
        placed = []
        for spec in D.get("insets", []):
            p, iw2, ih2, ipw, iph = picture(s, spec["img"], spec["x"], spec["y"], spec["w"],
                                            radius=0.04, line_alpha=35, blur=28, dist=10, alpha=55)
            placed.append((spec["x"], spec["y"], iw2, ih2, ipw, iph))
        for n, where, px, py in D["pins"]:
            if where == "main":
                cx, cy = X + px / pw * w, Y + py / ph * h
            else:
                x0, y0, w0, h0, ipw, iph = placed[where]
                cx, cy = x0 + px / ipw * w0, y0 + py / iph * h0
            pin(s, cx, cy, n, self.accent)
        self.rail(s, D["rail"], top=D.get("rail_top", 1.62), step=D.get("rail_step", 0.9))
        return self._finish(s, D)

    def lanes(self, D):
        """A hub on the left and one labelled lane per mode or target.

        Reach for it when the buyer's question is "how does this connect to what
        I already run"."""
        s = self._slide()
        self.title(s, D["title"], w=7.4)
        cx, cw = M, D.get("hub_w", 1.75)
        top, bot = D.get("top", 1.5), D.get("bottom", 4.55)
        hub = panel(s, cx, top, cw, bot - top, alpha=10, line_alpha=None)
        stroke(hub, self.accent, 1.5)
        box(s, cx + 0.12, top + 0.12, cw - 0.24, 1.0, D["hub"], 12, T.WHITE, font=T.SEMI,
            spacing=1.05)
        if D.get("hub_sub"):
            box(s, cx + 0.12, bot - 0.75, cw - 0.24, 0.6, D["hub_sub"], 8.5, T.SOFT, spacing=1.05)
        rows = D["lanes"]
        lane_h = (bot - top - 0.18 * (len(rows) - 1)) / len(rows)
        tx = D.get("target_x", 5.35)
        for i, (mode, target, detail) in enumerate(rows):
            y = top + i * (lane_h + 0.18)
            mid = y + lane_h / 2
            arrow(s, cx + cw + 0.06, mid, tx - 0.06, mid, alpha=40)
            box(s, cx + cw + 0.22, mid - 0.24, tx - cx - cw - 0.4, 0.22, mode, 9, T.WHITE,
                font=T.SEMI)
            self.node(s, tx, y, SW - M - tx, lane_h, target, detail)
        if D.get("strip"):
            self.strip(s, D["strip"], D.get("strip_y", 4.7), D.get("strip_label"))
        return self._finish(s, D)

    def pipeline(self, D):
        """Stages in a row, with a band underneath for the engine that feeds
        them. Use it where order is the point."""
        s = self._slide()
        self.title(s, D["title"], w=7.4)
        stages = D["stages"]
        gap = 0.22
        w = (SW - 2 * M - gap * (len(stages) - 1)) / len(stages)
        y = D.get("y", 1.55)
        for i, (num, name, desc) in enumerate(stages):
            x = M + i * (w + gap)
            panel(s, x, y, w, 1.5, alpha=8, line_alpha=28, radius=0.1)
            box(s, x + 0.14, y + 0.12, w - 0.28, 0.3, num, 13, T.WHITE, font=T.MED)
            hline(s, x + 0.14, y + 0.46, 0.3, color=self.accent, alpha=None, weight=2.0)
            box(s, x + 0.14, y + 0.56, w - 0.28, 0.8, name, 12, T.WHITE, font=T.SEMI)
            box(s, x, y + 1.6, w, 0.9, desc, 8.5, T.SOFT, spacing=1.08)
            if i:
                arrow(s, x - gap + 0.02, y + 0.75, x - 0.02, y + 0.75, alpha=45)
        if D.get("band"):
            head, body, big, small = D["band"]
            by = D.get("band_y", 3.85)
            band = panel(s, M, by, SW - 2 * M, 0.92, alpha=10, line_alpha=None, radius=0.06)
            stroke(band, self.accent, 1.0)
            box(s, M + 0.22, by + 0.14, 2.4, 0.26, head, 11, T.WHITE, font=T.SEMI)
            box(s, M + 0.22, by + 0.42, 5.6, 0.42, body, 9, T.SOFT, spacing=1.05)
            if big:
                box(s, SW - M - 2.4, by + 0.2, 2.2, 0.5, big, 20, T.WHITE, font=T.MED,
                    align=PP_ALIGN.RIGHT)
                box(s, SW - M - 2.4, by + 0.62, 2.2, 0.24, small, 8.5, T.SOFT, align=PP_ALIGN.RIGHT)
        return self._finish(s, D)

    def matrix(self, D):
        """A support matrix as a native table.

        Rows beat prose when the buyer asks whether the product covers their
        stack, and a table survives being screenshotted into an email."""
        s = self._slide()
        self.title(s, D["title"], w=7.4)
        cols = D["cols"]
        scale = (SW - 2 * M) / sum(w for _, w in cols)
        y, x = D.get("y", 1.6), M
        for name, w in cols:
            c = box(s, x, y, w * scale - 0.15, 0.22, name, 7.5, T.WHITE, font=T.SEMI)
            char_spacing(c, 1.2)
            x += w * scale
        hline(s, M, y + 0.3, SW - 2 * M, color=self.accent, alpha=None, weight=1.5)
        row_h = D.get("row_h", 0.68)
        for r, row in enumerate(D["rows"]):
            ry = y + 0.42 + r * row_h
            if r % 2 == 0:
                band = box(s, M - 0.12, ry - 0.08, SW - 2 * M + 0.24, row_h - 0.06,
                           shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
                fill(band, T.WHITE, 4)
            x = M
            for c, (cell, (_, w)) in enumerate(zip(row, cols)):
                cw = w * scale - 0.2
                if c == 0:
                    box(s, x, ry, cw, row_h - 0.1, cell, 10.5, T.WHITE, font=T.SEMI, spacing=1.05)
                else:
                    box(s, x, ry + 0.02, cw, row_h - 0.1, cell, 9, T.SOFT, spacing=1.08)
                x += w * scale
            hline(s, M, ry + row_h - 0.1, SW - 2 * M, alpha=12)
        if D.get("chips"):
            cy = y + 0.46 + len(D["rows"]) * row_h
            x = M
            for label, items in D["chips"]:
                x = self.chips(s, label, items, y=cy, x=x) + 0.45
        return self._finish(s, D)

    def cases(self, D):
        """Three use cases in a row, each tagged with who it is for.

        The tag turns a capability slide into a selling slide, because the
        seller can point at the tag and name the buyer's own team."""
        s = self._slide()
        self.title(s, D["title"], w=D.get("title_w", 7.6))
        if D.get("art"):
            D["art"](s, self)          # a callable that draws the signature visual
        y = D.get("y", 3.98)
        col_w, gap = 2.78, 0.28
        for i, (head, sub, tag) in enumerate(D["items"]):
            x = M + i * (col_w + gap)
            pin(s, x + 0.15, y + 0.13, i + 1, self.accent, d=0.28)
            box(s, x + 0.42, y, col_w - 0.42, 0.28, head, 12, T.WHITE, font=T.SEMI)
            box(s, x + 0.42, y + 0.3, col_w - 0.45, 0.5, sub, 9.5, T.SOFT, spacing=1.08)
            if tag:
                chip(s, x + 0.42, y + 0.86, tag, fg=T.WHITE, bg=T.WHITE, bg_alpha=10,
                     line_c=T.WHITE, line_alpha=28, size=7)
        return self._finish(s, D)

    def proof(self, D):
        """One large number, its source, a quote, and two supporting results.

        Say which layer each number proves. A sharp buyer asks, and the slide
        that answers first keeps the room."""
        s = self._slide()
        self.title(s, D["title"], w=7.4)
        box(s, M, 1.34, 5.0, 1.2, D["big"], D.get("big_size", 80), T.WHITE, font=T.MED,
            spacing=0.9)
        box(s, M, 2.55, 4.5, 0.5, D["big_label"], 13, T.WHITE, spacing=1.1)
        if D.get("big_source"):
            src = box(s, M, 3.1, 4.5, 0.22, D["big_source"], 8.5, T.SOFT)
            if D.get("big_url"):
                link(src, D["big_url"])
        if D.get("quote"):
            qy = D.get("quote_y", 3.55)
            qlines = lines_for(D["quote"], 60)
            by = qy + qlines * 0.2 + 0.12
            bar = box(s, M, qy + 0.03, 0.04, by + 0.2 - qy)
            fill(bar, self.accent)
            box(s, M + 0.2, qy, 4.3, qlines * 0.2 + 0.05, "“" + D["quote"] + "”", 10.5,
                T.WHITE, spacing=1.12)
            box(s, M + 0.2, by, 4.3, 0.22, D["quote_by"], 8.5, T.SOFT)
        rx, rw = 5.85, SW - M - 5.85
        for i, item in enumerate(D.get("right", [])):
            yy = 1.42 + i * 1.62
            hline(s, rx, yy, rw, alpha=22)
            hline(s, rx, yy, 0.5, color=self.accent, alpha=None, weight=2.0)
            if item.get("kind", "stat") == "stat":
                box(s, rx, yy + 0.12, rw, 0.55, item["value"], 32, T.WHITE, font=T.MED)
                box(s, rx, yy + 0.7, rw, 0.55, item["label"], 9.5, T.SOFT, spacing=1.08)
            else:
                names = item["nodes"]
                nw = (rw - 0.3 * (len(names) - 1)) / len(names)
                for j, nm in enumerate(names):
                    x = rx + j * (nw + 0.3)
                    hl = j == len(names) // 2
                    n = panel(s, x, yy + 0.2, nw, 0.62, alpha=16 if hl else 8,
                              line_alpha=None if hl else 30, radius=0.12)
                    if hl:
                        stroke(n, self.accent, 1.25)
                    box(s, x + 0.04, yy + 0.2, nw - 0.08, 0.62, nm, 8.5, T.WHITE, font=T.SEMI,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1.0)
                    if j:
                        arrow(s, x - 0.28, yy + 0.51, x - 0.02, yy + 0.51, alpha=60)
                box(s, rx, yy + 0.92, rw, 0.4, item["label"], 9.5, T.SOFT, spacing=1.08)
            if item.get("source"):
                l = box(s, rx, yy + (1.22 if item.get("kind", "stat") == "stat" else 1.34),
                        rw, 0.2, item["source"], 7.5, T.SOFT)
                if item.get("url"):
                    link(l, item["url"])
        if D.get("credentials"):
            hline(s, M, 4.98, SW - 2 * M, alpha=18)
            c = box(s, M, 5.08, 2.0, 0.22, D.get("credentials_label", "TRACK RECORD"), 7,
                    T.WHITE, font=T.SEMI)
            char_spacing(c, 1.2)
            box(s, M + 1.95, 5.08, SW - 2 * M - 1.95, 0.22, D["credentials"], 7.5, T.SOFT)
        return self._finish(s, D)

    def video(self, D):
        """A slide built around an embedded video.

        Two shapes. "hero" puts the claim and two facts beside the player, which
        opens a deck. "demo" puts a chapter list beside it, so a seller can jump
        to the moment that answers the question in the room."""
        from pptx_youtube import add_poster_link, add_youtube
        s = self._slide()
        shape = D.get("shape", "hero")
        url = f"https://www.youtube.com/watch?v={D['video']}"
        if D.get("start"):
            url += f"&t={D['start']}s"
        if shape == "hero":
            box(s, M, TOP, 3.8, 1.2, D["title"], 22, T.WHITE, font=T.MED, spacing=0.95)
            box(s, M, 1.66, 3.45, 1.0, D["definition"], 11, T.SOFT, spacing=1.12)
            for i, (value, label) in enumerate(D.get("facts", [])):
                y = 2.95 + i * 1.12
                hline(s, M, y, 3.45, alpha=22)
                hline(s, M, y, 0.55, color=self.accent, alpha=None, weight=2.0)
                box(s, M, y + 0.13, 3.45, 0.42, value, 22, T.WHITE, font=T.MED)
                box(s, M, y + 0.54, 3.45, 0.42, label, 9.5, T.SOFT, spacing=1.05)
            vx, vy, vw = 4.55, 1.30, 4.90
        else:
            self.title(s, D["title"], w=7.4)
            vx, vy, vw = M, 1.45, 6.1
        vh = vw * 9 / 16
        glow(s, vx + 0.4, vy + 0.3, vw - 0.8, vh - 0.2, self.accent, alpha=38, soft=60)
        halo = panel(s, vx - 0.07, vy - 0.07, vw + 0.14, vh + 0.14, alpha=None,
                     line_alpha=22, radius=0.035)
        fill(halo, T.NAVY_DK)
        shadow(halo, blur=30, dist=10, alpha=40)
        if D.get("embed", True):
            pic = add_youtube(s, D["video"], str(D["poster"]), Inches(vx), Inches(vy),
                              Inches(vw), Inches(vh), title=D["video_title"], start=D.get("start"))
        else:
            pic = add_poster_link(s, D["video"], str(D["poster"]), Inches(vx), Inches(vy),
                                  Inches(vw), Inches(vh))
        round_pic(pic, 0.025)
        cap = box(s, vx, vy + vh + 0.2, vw, 0.24, D["video_title"], 10, T.WHITE, font=T.SEMI)
        link(cap, url)
        sub = box(s, vx, vy + vh + 0.45, vw, 0.24,
                  f"YouTube  ·  {D['duration']}  ·  {D.get('video_note', '')}", 8.5, T.SOFT)
        link(sub, url)
        if shape == "demo" and D.get("chapters"):
            self._chapters(s, D, url, vy)
        return self._finish(s, D)

    def _chapters(self, s, D, url, vy):
        cx, cw = 7.05, SW - M - 7.05
        c = box(s, cx, vy - 0.02, cw, 0.2, "CHAPTERS", 7, T.WHITE, font=T.SEMI)
        char_spacing(c, 1.4)
        top, step = vy + 0.36, 0.5
        rail = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(cx + 0.05),
                                      Inches(top + 0.08), Inches(cx + 0.05),
                                      Inches(top + 0.08 + step * (len(D["chapters"]) - 1)))
        stroke(rail, T.WHITE, 0.75, 22)
        beats = D.get("beats", {"Set up": T.WHITE, "In action": None, "Evidence": T.GREEN})
        for i, (stamp, beat, label) in enumerate(D["chapters"]):
            y = top + i * step
            dot = box(s, cx, y + 0.03, 0.1, 0.1, shape=MSO_SHAPE.OVAL)
            fill(dot, beats.get(beat) or self.accent)
            mm, ss = stamp.split(":")
            t = box(s, cx + 0.24, y - 0.04, 0.6, 0.24, stamp, 12, T.WHITE, font=T.MED)
            l = box(s, cx + 0.24, y + 0.19, cw - 0.24, 0.2, label, 8.5, T.SOFT)
            for sp in (t, l):
                link(sp, f"{url}&t={int(mm) * 60 + int(ss)}s")
        ly = top + step * len(D["chapters"]) + 0.02
        for (beat, color), off in zip(beats.items(), (0.0, 0.72, 1.56)):
            dot = box(s, cx + off, ly + 0.06, 0.09, 0.09, shape=MSO_SHAPE.OVAL)
            fill(dot, color or self.accent)
            box(s, cx + off + 0.14, ly, 0.8, 0.22, beat, 8, T.SOFT)

    # -- output -------------------------------------------------------------
    def save(self):
        self.outdir.mkdir(parents=True, exist_ok=True)
        out = self.outdir / f"{self.name}.pptx"
        self.prs.save(str(out))
        print("saved", out)
        return out
