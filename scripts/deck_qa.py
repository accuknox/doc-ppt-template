# -*- coding: utf-8 -*-
"""
Visual and readability gate for a built deck. Run it before you render.

  py -3.11 scripts/deck_qa.py output/<deck>.pptx
  py -3.11 scripts/deck_qa.py output/<deck>.pptx --gslides   # deck goes to Google Slides

FAIL (exit 1):
  - text under 9 pt anywhere
  - a content slide with no speaker notes
  - a shape that runs off the slide
  - an em dash, en dash or semicolon outside a code font
  - a raw newline inside a text run (breaks the PDF export)
  - with --gslides: Segoe MDL2 icon glyphs or Consolas, which Google Slides cannot draw

WARN:
  - body text under 10.5 pt
  - a content slide with no picture at all (no icon, logo or diagram): text only
  - more than 70 words on one slide: move the detail into the notes

The cover and closing layouts are skipped.
"""
import sys
from pptx import Presentation
from pptx.util import Emu

CODE_FONTS = {"Consolas", "JetBrains Mono", "Courier New", "Source Code Pro", "Roboto Mono"}
SKIP_LAYOUTS = {"AccuKnox Intro Title", "AccuKnox Section Title"}


def walk(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:  # group
            yield from walk(sh.shapes)


def main(path, gslides=False):
    prs = Presentation(path)
    W, H = prs.slide_width, prs.slide_height
    fails, warns = [], []
    for n, slide in enumerate(prs.slides, 1):
        if slide.slide_layout.name in SKIP_LAYOUTS:
            continue
        hidden = slide._element.get("show") == "0"
        tag = f"slide {n}" + (" (hidden)" if hidden else "")
        pics, words = 0, 0
        for sh in walk(slide.shapes):
            if sh.shape_type == 13:
                pics += 1
            if sh.left is not None and sh.width is not None and not sh.is_placeholder:
                if sh.left < -Emu(9144) or sh.top < -Emu(9144) or \
                   sh.left + sh.width > W + Emu(9144) or sh.top + sh.height > H + Emu(9144):
                    fails.append(f"{tag}: shape '{sh.name}' runs off the slide")
            frames = []
            if sh.has_text_frame:
                frames.append(sh.text_frame)
            if getattr(sh, "has_table", False) and sh.has_table:
                frames += [c.text_frame for r in sh.table.rows for c in r.cells]
            for tf in frames:
                for p in tf.paragraphs:
                    for r in p.runs:
                        t = r.text
                        if not t.strip():
                            continue
                        font = r.font.name or ""
                        size = r.font.size.pt if r.font.size else None
                        is_code = font in CODE_FONTS
                        if not is_code:
                            words += len(t.split())
                        if "\n" in t:
                            fails.append(f"{tag}: raw newline in a run: {t[:40]!r}")
                        if not is_code and any(ch in t for ch in "—–;"):
                            fails.append(f"{tag}: dash or semicolon in prose: {t[:50]!r}")
                        if size is not None and size < 9:
                            fails.append(f"{tag}: {size:g} pt text: {t[:40]!r}")
                        elif size is not None and size < 10.5 and not is_code and len(t) > 30:
                            warns.append(f"{tag}: {size:g} pt body text: {t[:40]!r}")
                        if gslides and font == "Segoe MDL2 Assets":
                            fails.append(f"{tag}: Segoe MDL2 glyph, blank in Google Slides. Use icon_img()")
                        if gslides and font == "Consolas":
                            fails.append(f"{tag}: Consolas, not in Google Slides. Call google_safe()")
        has_notes = slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip()
        if not has_notes:
            fails.append(f"{tag}: no speaker notes. Put the fine print and sources there")
        if pics == 0:
            warns.append(f"{tag}: text only, no icon or diagram")
        if words > 70:
            warns.append(f"{tag}: {words} words on the slide, move detail to the notes")
    for f in dict.fromkeys(fails):
        print("FAIL", f)
    for w in dict.fromkeys(warns):
        print("WARN", w)
    print(f"\n{len(prs.slides)} slides, {len(set(fails))} fail, {len(set(warns))} warn")
    return 1 if fails else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__); sys.exit(2)
    sys.exit(main(args[0], gslides="--gslides" in sys.argv))
