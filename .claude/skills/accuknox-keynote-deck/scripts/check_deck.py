# -*- coding: utf-8 -*-
"""check_deck.py: the gate that catches what a rendered PNG hides.

Every finding here comes from a defect that reached a real slide during the
TCTS build. Run it after each build, before you render:

    py -3.11 check_deck.py output/My_Deck.pptx

It reports four classes of problem:

  PUNCTUATION  an em dash, en dash, double hyphen or semicolon in slide text
  COPY         a sentence over 20 words, a banned word, a lower-case heading
  GEOMETRY     a shape that crosses the slide edge or the side margin
  IMAGE        a picture placed at under 140 effective dpi, so it looks soft

Exit code is 1 when a blocking finding exists, so a build script can gate on it.
Geometry findings for pictures are advisory, because a screen that runs off the
right edge on purpose is part of the style.
"""
import re
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.util import Emu

EMU_IN = 914400.0
SW, SH = 10.0, 5.625
MARGIN = 0.55

BANNED_WORDS = ["delve", "leverage", "robust", "seamless", "ensure", "comprehensive",
                "elevate", "empower", "streamline", "utilize", "groundbreaking",
                "testament", "cutting-edge", "game-changer", "state-of-the-art"]
# A title is a claim, so it starts on a capital. These words stay lower case inside it.
LOWER_OK = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "as", "at",
            "by", "in", "of", "off", "on", "per", "to", "up", "via", "vs"}


def slide_text(slide):
    out = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                t = "".join(r.text for r in p.runs).strip()
                if t:
                    out.append((sh, t))
        if sh.has_table:
            for row in sh.table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        out.append((sh, cell.text.strip()))
    return out


def check(path):
    prs = Presentation(str(path))
    findings = []

    def add(level, n, kind, msg):
        findings.append((level, n, kind, msg))

    for n, slide in enumerate(prs.slides, 1):
        texts = slide_text(slide)
        for sh, t in texts:
            for ch, name in (("—", "em dash"), ("–", "en dash"), (";", "semicolon")):
                if ch in t:
                    add("BLOCK", n, "PUNCTUATION", f"{name} in {t[:60]!r}")
            if "--" in t:
                add("BLOCK", n, "PUNCTUATION", f"double hyphen in {t[:60]!r}")
            for w in BANNED_WORDS:
                if re.search(rf"\b{w}\b", t, re.I):
                    add("BLOCK", n, "COPY", f"banned word {w!r} in {t[:60]!r}")
            for sentence in re.split(r"(?<=[.?!])\s+", t):
                words = sentence.split()
                # A chip row or a credentials strip is a list, not a sentence.
                if len(words) > 20 and "·" not in sentence:
                    add("WARN", n, "COPY", f"{len(words)}-word sentence: {sentence[:70]!r}")

        # the first sizeable text shape on the slide is the title
        titles = [(sh, t) for sh, t in texts
                  if sh.has_text_frame and sh.top is not None and sh.top < Emu(int(0.9 * EMU_IN))]
        for sh, t in titles[:1]:
            words = [w for w in re.split(r"[\s\n]+", t) if w]
            for w in words[1:]:
                bare = re.sub(r"[^A-Za-z-]", "", w)
                if bare and bare.islower() and bare.lower() not in LOWER_OK:
                    add("WARN", n, "COPY", f"title word {w!r} is lower case: {t[:60]!r}")
                    break

        for sh in slide.shapes:
            if sh.left is None or sh.width is None:
                continue
            x, y = sh.left / EMU_IN, sh.top / EMU_IN
            w, h = sh.width / EMU_IN, sh.height / EMU_IN
            is_pic = sh.shape_type == 13
            if y < -0.01 or y + h > SH + 0.01:
                add("WARN" if is_pic else "BLOCK", n, "GEOMETRY",
                    f"{sh.shape_type} runs past the top or bottom: y={y:.2f} h={h:.2f}")
            if x < -0.01 or x + w > SW + 0.01:
                add("WARN" if is_pic else "BLOCK", n, "GEOMETRY",
                    f"{sh.shape_type} runs past the left or right: x={x:.2f} w={w:.2f}")
            elif not is_pic and (x < MARGIN - 0.2 or x + w > SW - MARGIN + 0.3):
                add("WARN", n, "GEOMETRY", f"{sh.shape_type} crosses the side margin: x={x:.2f}")
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.font.size and r.font.size.pt < 7:
                            add("WARN", n, "COPY", f"{r.font.size.pt} pt text: {r.text[:40]!r}")

            if is_pic:
                try:
                    im = Image.open(sh.image.blob and __import__("io").BytesIO(sh.image.blob))
                    dpi = im.width / max(w, 0.01)
                    if dpi < 140:
                        add("WARN", n, "IMAGE", f"{dpi:.0f} dpi at {w:.2f} in wide, looks soft")
                except Exception:
                    pass

    blocking = [f for f in findings if f[0] == "BLOCK"]
    for level, n, kind, msg in findings:
        print(f"{level:5s} slide {n:>2}  {kind:<11s} {msg}")
    print(f"\n{len(prs.slides.__iter__.__self__._sldIdLst)} slides, "
          f"{len(blocking)} blocking, {len(findings) - len(blocking)} advisory")
    return 1 if blocking else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(max(check(Path(a)) for a in sys.argv[1:]))
