# -*- coding: utf-8 -*-
"""extract_deck.py: read a source deck so you can rebrand it.

A rebrand starts by seeing what the old deck actually says and owns. This writes
three things beside each other:

    <out>/inventory.md    one row per slide: title, word count, pictures, hazards
    <out>/content.json    the full text of every slide, plus the speaker notes
    <out>/media/          every embedded picture over a size threshold, named
                          s<NN>-<i>.png, so you can reuse the good ones

Run it, then render the source deck to PNG and look at both together:

    py -3.11 extract_deck.py "Old Deck.pptx" out/olddeck
    powershell -File render.ps1 -Pptx "Old Deck.pptx" -Out out/olddeck/render

The hazard column is the part that saves you. It flags the text that must never
reach a partner deck: a customer name, an email address, a cloud account id, a
token, an NDA mark or an internal-only product name.
"""
import json
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

HAZARDS = [
    (r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "email address"),
    (r"\b\d{12}\b", "cloud account id"),
    (r"\bey[A-Za-z0-9_-]{10,}\b", "token"),
    (r"(?i)\bconfidential\b|\bNDA\b|limited distribution", "confidentiality mark"),
    (r"(?i)\bmodelarmor\b|\bmodelknox\b", "internal product name"),
    (r"(?i)\bgarak\b|\bllmguard\b|\bmodelscan\b|\bpresidio\b|\bprowler\b|\bsteampipe\b",
     "open-source engine name"),
    (r"(?i)\bapi[_ -]?key\b|\bsecret[_ -]?key\b", "credential label"),
]


def texts(slide):
    out = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                t = "".join(r.text for r in p.runs).strip()
                if t:
                    out.append(t)
        if sh.has_table:
            for row in sh.table.rows:
                out.append(" | ".join(c.text.strip() for c in row.cells))
    return out


def pictures(slide):
    return [sh for sh in slide.shapes if sh.shape_type == 13]


def main(src, outdir, min_kb=120):
    src, outdir = Path(src), Path(outdir)
    media = outdir / "media"
    media.mkdir(parents=True, exist_ok=True)
    prs = Presentation(str(src))
    rows, payload = [], []

    for n, slide in enumerate(prs.slides, 1):
        body = texts(slide)
        title = body[0] if body else ""
        words = sum(len(t.split()) for t in body)
        notes = ""
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()
        found = []
        for pattern, label in HAZARDS:
            for t in body + [notes]:
                if re.search(pattern, t):
                    found.append(label)
                    break
        kept = []
        for i, pic in enumerate(pictures(slide), 1):
            blob = pic.image.blob
            if len(blob) < min_kb * 1024:
                continue
            ext = pic.image.ext or "png"
            name = f"s{n:02d}-{i}.{ext}"
            (media / name).write_bytes(blob)
            kept.append({"file": f"media/{name}",
                         "kb": round(len(blob) / 1024),
                         "w_in": round((pic.width or 0) / 914400, 2)})
        rows.append((n, title[:70], words, len(pictures(slide)), len(kept),
                     ", ".join(sorted(set(found))) or ""))
        payload.append({"slide": n, "title": title, "text": body, "notes": notes,
                        "media": kept, "hazards": sorted(set(found))})

    (outdir / "content.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                         encoding="utf-8")
    lines = [f"# {src.name}", "",
             f"{len(payload)} slides. Media over {min_kb} KB is extracted to `media/`.", "",
             "| # | Title | Words | Pics | Kept | Hazards |", "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |")
    heavy = [r for r in rows if r[2] > 60]
    lines += ["", f"Slides over 60 words: {len(heavy)}. Those are the ones to split or cut.",
              f"Slides carrying a hazard: {sum(1 for r in rows if r[5])}."]
    (outdir / "inventory.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(payload)} slides -> {outdir}")
    print(f"  media kept: {sum(r[4] for r in rows)}")
    print(f"  hazards on: {[r[0] for r in rows if r[5]]}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 120)
