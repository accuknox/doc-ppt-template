# -*- coding: utf-8 -*-
"""
AccuKnox SVG kit. Draw diagrams as SVG with brand tokens and real icons, then
render them to PNG for PowerPoint and Google Slides.

Why PNG at the end: python-pptx cannot place SVG, and Google Slides drops SVG
on import. So the SVG is the editable source (kept next to the PNG), and the
PNG at 2x is what the slide carries.

Icons live in assets/icons/ (see scripts/fetch_icons.py):
  ui("key", x, y, size, color)         Tabler outline glyph, any color
  logo("java-original", x, y, size)    Devicon or Simple Icons brand logo

Sizing rule. Draw on a canvas whose width maps to the space on the slide.
A 1280 px canvas placed 9.2 in wide gives 1 px = 0.52 pt, so:
  24 px heading = 12.4 pt, 19 px body = 9.9 pt, 17 px = 8.8 pt (the floor).
Never put text under 17 px on a 1280 canvas. For a half-width diagram, use a
640 px canvas placed 4.3 in wide, which keeps the same ratio.

Usage:
  from _aksvg import *
  b = [rect(0, 0, 300, 120), ui("server-2", 16, 16, 40), text(70, 46, "Server", 24, NAVY, 700)]
  png = render("my_diagram", 1280, 600, "".join(b), outdir="work/mydeck/diagrams")

  icon_png("shield-lock", PRIMARY)  -> path to a cached 288 px PNG for slides
  contact_sheet([png1, png2, ...], "sheet.png")  -> one image to review

Rendering uses headless Microsoft Edge (installed on every Windows machine here),
so no Python SVG library is needed.
"""
import base64, hashlib, os, re, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(HERE, "..", "assets", "icons")
CACHE = os.path.join(HERE, "..", "work", "_iconcache")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ---- brand tokens, same values as _akdeck.py ----------------------------
NAVY, NAVY_DK, PRIMARY, SECOND, PURPLE = "#11206D", "#0A144A", "#0046FF", "#6464FF", "#4D4DD9"
RED, RED_LT, GREEN, GREEN_DK, GREEN_LT = "#C80019", "#FBECEE", "#16A55C", "#0B7A42", "#E7F6EE"
INK, MUTE, GREY_BD, GREY_BG, LAV, WHITE = "#1B223B", "#5A637D", "#C4CCDE", "#EEF0F6", "#ECECFB", "#FFFFFF"
FONT = "Space Grotesk"
_MARK_COLORS = [PRIMARY, SECOND, RED, GREEN, GREEN_DK, MUTE, NAVY, PURPLE, GREY_BD]


# ---- icons ---------------------------------------------------------------
def _icon_path(kind, name):
    p = os.path.join(ICONS, kind, name + ".svg")
    if not os.path.exists(p):
        raise FileNotFoundError(f"{kind} icon '{name}' missing. Run: py -3.11 scripts/fetch_icons.py {kind} {name}")
    return p


def _tabler_inner(name):
    t = open(_icon_path("ui", name), encoding="utf-8").read()
    inner = t[t.index(">", t.index("<svg")) + 1: t.rindex("</svg>")]
    return re.sub(r'<path stroke="none"[^>]*/>', "", inner)


def ui(name, x, y, s, color=PRIMARY, sw=2):
    """A Tabler outline glyph, stroked in `color`."""
    return (f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
            f'{_tabler_inner(name)}</svg>')


def _brand_uri(name, tint=NAVY):
    t = open(_icon_path("brand", name), encoding="utf-8").read()
    if name.startswith("si-"):            # Simple Icons ship black, tint them
        t = t.replace("<svg ", f'<svg fill="{tint}" ', 1)
    return "data:image/svg+xml;base64," + base64.b64encode(t.encode()).decode()


def logo(name, x, y, s, tint=NAVY):
    """A full-color brand logo (Devicon), or a tinted one-color logo (si-*)."""
    return f'<image href="{_brand_uri(name, tint)}" x="{x}" y="{y}" width="{s}" height="{s}"/>'


# ---- primitives ----------------------------------------------------------
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, lines, size=22, color=INK, weight=400, anchor="start", lh=1.25, italic=False):
    """Text at baseline y. Pass a list for several lines. SVG never wraps, so
    break long lines yourself and check the render."""
    if isinstance(lines, str):
        lines = [lines]
    st = ' font-style="italic"' if italic else ""
    out = [f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{color}" '
           f'font-weight="{weight}" text-anchor="{anchor}"{st}>']
    for i, ln in enumerate(lines):
        out.append(f'<tspan x="{x}" dy="{0 if i == 0 else size * lh}">{esc(ln)}</tspan>')
    out.append("</text>")
    return "".join(out)


def rect(x, y, w, h, fill=WHITE, stroke=GREY_BD, sw=2, r=14, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def pill(x, y, w, h, label, fill=LAV, color=NAVY, size=18, weight=600, stroke="none"):
    return (rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.5, r=h / 2) +
            text(x + w / 2, y + h / 2 + size * 0.36, label, size=size, color=color, weight=weight, anchor="middle"))


def chip(x, y, w, h, icon_name, label, color=PRIMARY, fill=WHITE, size=17, brand=False, stroke=GREY_BD):
    """A small bordered box with an icon and a label. Width guide: 48 + 8.4 px per character at size 15."""
    s = h - 14
    ic = logo(icon_name, x + 8, y + 7, s) if brand else ui(icon_name, x + 8, y + 7, s, color)
    return (rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.5, r=10) + ic +
            text(x + s + 16, y + h / 2 + size * 0.36, label, size=size, color=NAVY, weight=600))


def card(x, y, w, h, icon_name, head, sub=None, accent=PRIMARY, brand=False, hsize=22, ssize=17):
    """A white card with an icon in a tinted circle, a heading and an optional sub line or list."""
    out = [rect(x, y, w, h, stroke=accent, sw=2.5),
           f'<circle cx="{x + 40}" cy="{y + 40}" r="28" fill="{LAV}"/>',
           logo(icon_name, x + 20, y + 20, 40) if brand else ui(icon_name, x + 20, y + 20, 40, accent),
           text(x + 82, y + 48, head, hsize, NAVY, 700)]
    if sub:
        out.append(text(x + 20, y + 98, sub, ssize, MUTE, 500))
    return "".join(out)


def arrow(x1, y1, x2, y2, color=PRIMARY, sw=3, dash=None, both=False):
    """A straight arrow. `color` must be one of the brand tokens, which carry markers."""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    k = color[1:]
    ms = f' marker-start="url(#s{k})"' if both else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d} marker-end="url(#e{k})"{ms}/>'


def curve(dpath, color=PRIMARY, sw=3, dash=None):
    """An arrow along any SVG path, for example 'M10,10 C200,120 400,120 600,10'."""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{dpath}" fill="none" stroke="{color}" stroke-width="{sw}"{d} marker-end="url(#e{color[1:]})"/>'


def cyl(x, y, w, h, label, fill=WHITE, stroke=GREY_BD, size=16, color=MUTE):
    """A storage cylinder: a disk, a database, a bucket of data."""
    ry = 8
    return (f'<path d="M{x},{y+ry} L{x},{y+h-ry} A{w/2},{ry} 0 0 0 {x+w},{y+h-ry} L{x+w},{y+ry}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<ellipse cx="{x+w/2}" cy="{y+ry}" rx="{w/2}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>' +
            text(x + w / 2, y + h / 2 + 10, label, size=size, color=color, weight=600, anchor="middle"))


def badge(cx, cy, n, r=17, fill=PRIMARY, size=20):
    """A numbered step circle."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>' +
            text(cx, cy + size * 0.36, str(n), size=size, color=WHITE, weight=700, anchor="middle"))


def boundary(x1, y1, x2, y2, label, color=RED, icon_name="wifi-off"):
    """A dashed line that marks a trust or network boundary, with a label."""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3" stroke-dasharray="10 7"/>' +
            ui(icon_name, x2 - 18, y2 + 2, 36, color) + text(x2 + 26, y2 + 28, label, 19, color, 700))


# ---- document and render -------------------------------------------------
def svg_doc(w, h, body, bg=WHITE):
    marks = []
    for c in _MARK_COLORS:
        k = c[1:]
        for pfx in ("e", "s"):
            marks.append(f'<marker id="{pfx}{k}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" '
                         f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{"".join(marks)}</defs>{bgr}{body}</svg>')


def render(name, w, h, body, outdir, bg=WHITE, scale=2):
    """Write <outdir>/<name>.svg and render <name>.png at `scale`x. Returns the PNG path.
    bg=None gives a transparent PNG."""
    os.makedirs(outdir, exist_ok=True)
    svg = svg_doc(w, h, body, bg)
    sp = os.path.abspath(os.path.join(outdir, name + ".svg"))
    open(sp, "w", encoding="utf-8").write(svg)
    hp = sp[:-4] + ".html"
    open(hp, "w", encoding="utf-8").write(
        '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;'
        f'background:transparent}}svg{{display:block}}</style></head><body>{svg}</body></html>')
    png = sp[:-4] + ".png"
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", f"--window-size={w},{h}",
                    "--default-background-color=00000000", f"--screenshot={png}",
                    "file:///" + hp.replace("\\", "/")], capture_output=True, timeout=90)
    Image.open(png).crop((0, 0, w * scale, h * scale)).save(png)
    os.remove(hp)
    return png


def icon_png(name, color=PRIMARY, kind=None):
    """A 288 px PNG of one icon, cached in work/_iconcache. kind is 'ui' or
    'brand', guessed from the name when omitted. Brand logos ignore `color`."""
    if kind is None:
        kind = "ui" if os.path.exists(os.path.join(ICONS, "ui", name + ".svg")) else "brand"
    key = f"{kind}-{name}-{(color or '').lstrip('#')}" if kind == "ui" else f"brand-{name}"
    out = os.path.join(CACHE, key + ".png")
    if os.path.exists(out):
        return out
    os.makedirs(CACHE, exist_ok=True)
    body = ui(name, 4, 4, 88, color) if kind == "ui" else logo(name, 2, 2, 92)
    tmp = render("_tmp_" + hashlib.md5(key.encode()).hexdigest()[:8], 96, 96, body, CACHE, bg=None, scale=3)
    os.replace(tmp, out)
    os.remove(tmp[:-4] + ".svg")
    return out


def contact_sheet(pngs, out, cols=2, width=2000, gap=16, bg="#9AA3B8"):
    """Tile slide or diagram PNGs into one image, so one look reviews many."""
    ims = [Image.open(p).convert("RGBA") for p in pngs]
    cw = (width - gap * (cols + 1)) // cols
    rows = []
    for im in ims:
        r = cw / im.size[0]
        rows.append(im.resize((cw, int(im.size[1] * r))))
    lines = [rows[i:i + cols] for i in range(0, len(rows), cols)]
    H = sum(max(i.size[1] for i in ln) for ln in lines) + gap * (len(lines) + 1)
    sheet = Image.new("RGBA", (width, H), bg)
    y = gap
    for ln in lines:
        x = gap
        for im in ln:
            sheet.alpha_composite(im, (x, y)); x += cw + gap
        y += max(i.size[1] for i in ln) + gap
    sheet.convert("RGB").save(out)
    return out
