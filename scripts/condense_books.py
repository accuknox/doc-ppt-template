"""Halve a book PDF by dropping low-value text pages, then tidy the result.

Keeps every chapter heading, every section heading it can afford, and every
image-heavy page. Protected page ranges are never touched. After selection the
script trims dangling part-sentences at the cut seams, renumbers the printed
footers, and rebuilds the contents pages so the numbers are true.
"""
import fitz, re, sys, json, math
from collections import defaultdict

# A line ending in a colon promises a list or figure that a dropped page took
# away, so a colon does not count as a finished thought here.
TERM = '.!?"\u201d\u2019)]'


# ---------------------------------------------------------------- page profile
def lines_of(page, dct=None):
    d = dct or page.get_text("dict")
    out = []
    for blk in d.get("blocks", []):
        if blk.get("type", 0) != 0:
            continue
        for ln in blk.get("lines", []):
            spans = [s for s in ln.get("spans", []) if s["text"].strip()]
            if not spans:
                continue
            txt = "".join(s["text"] for s in ln["spans"])
            out.append(dict(bbox=fitz.Rect(ln["bbox"]), text=txt, spans=spans,
                            block=blk["number"], size=max(s["size"] for s in spans),
                            origin=spans[0]["origin"]))
    return out


def profile(doc):
    rows = []
    for page in doc:
        area = page.rect.get_area()
        txt = page.get_text("text")
        img = 0.0
        for b in page.get_image_info():
            r = fitz.Rect(b["bbox"]) & page.rect
            if not r.is_empty:
                img += r.get_area()
        draw = 0.0
        for dr in page.get_drawings():
            r = fitz.Rect(dr["rect"]) & page.rect
            if not r.is_empty and r.get_area() < area * 0.9:
                draw += r.get_area()
        sizes = [ln["size"] for ln in lines_of(page)]
        rows.append(dict(words=len(txt.split()), imgcov=img / area,
                         drawcov=draw / area, maxsize=max(sizes) if sizes else 0))
    return rows


# ------------------------------------------------------------------- selection
def select_pages(doc, cfg):
    n = doc.page_count
    target = cfg["target"]
    prof = profile(doc)
    toc = doc.get_toc()

    chap_pages = sorted({p for lvl, _, p in toc if lvl == 1 and 1 <= p <= n})
    sec_pages = {p for lvl, _, p in toc if lvl == 2 and 1 <= p <= n}
    sub_pages = {p for lvl, _, p in toc if lvl == 3 and 1 <= p <= n}

    protected = set()
    for a, b in cfg.get("protect", []):
        protected |= set(range(a, b + 1))

    always = set(protected)
    always |= {1, n}                       # covers
    always |= set(cfg.get("toc_pages", []))
    always |= set(cfg.get("keep_extra", []))
    always |= {p for p in chap_pages if p not in cfg.get("drop_chapters", ())}
    always = {p for p in always if 1 <= p <= n} - set(cfg.get("force_drop", ()))

    def is_filler(p):
        r = prof[p - 1]
        return r["words"] < 15 and r["imgcov"] < 0.12 and r["drawcov"] < 0.2

    banned = set(cfg.get("force_drop", ()))
    banned |= {p for p in range(1, n + 1) if p not in always and is_filler(p)}

    def score(p):
        r = prof[p - 1]
        s = 115 * min(r["imgcov"], 0.75)
        if p in sec_pages:
            s += 46
        if p in sub_pages:
            s += 16
        s += 14 * min(r["drawcov"], 0.7)    # tables and diagrams drawn as vectors
        s -= 0.035 * r["words"]
        return s

    # bucket the remaining pages by chapter so every chapter keeps a fair share
    bounds = chap_pages + [n + 1]
    buckets = defaultdict(list)
    for p in range(1, n + 1):
        if p in always or p in banned:
            continue
        key = 0
        for i in range(len(bounds) - 1):
            if bounds[i] <= p < bounds[i + 1]:
                key = bounds[i]
                break
        buckets[key].append(p)

    budget = target - len(always)
    if budget < 0:
        raise SystemExit(f"protected pages ({len(always)}) already exceed target {target}")

    pool = sum(len(v) for v in buckets.values())
    quota, rema = {}, []
    for k, v in buckets.items():
        exact = budget * len(v) / pool
        quota[k] = int(exact)
        rema.append((exact - int(exact), k))
    for _, k in sorted(rema, reverse=True):
        if sum(quota.values()) >= budget:
            break
        quota[k] += 1

    keep = set(always)
    for k, v in buckets.items():
        ranked = sorted(v, key=lambda p: (-score(p), p))
        keep |= set(ranked[:min(quota[k], len(v))])

    # spend or refund any rounding drift globally
    rest = sorted((p for p in range(1, n + 1) if p not in keep and p not in banned),
                  key=lambda p: (-score(p), p))
    while len(keep) < target and rest:
        keep.add(rest.pop(0))
    while len(keep) > target:
        worst = min((p for p in keep if p not in always), key=score)
        keep.discard(worst)

    return sorted(keep), prof


# ------------------------------------------------------- fonts and redactions
def font_buffers(doc):
    bufs = {}
    for pno in range(doc.page_count):
        for f in doc[pno].get_fonts():
            base = f[3].split("+")[-1]
            if base in bufs:
                continue
            try:
                buf = doc.extract_font(f[0])[3]
                if buf:
                    bufs[base] = buf
            except Exception:
                pass
    return bufs


def redact(page, rects):
    rects = [r for r in rects if r and not r.is_empty]
    if not rects:
        return
    for r in rects:
        page.add_redact_annot(r, fill=None)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                          graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                          text=fitz.PDF_REDACT_TEXT_REMOVE)


def obstacles(page):
    """Images, and only those drawings that act as a box around text."""
    imgs = [fitz.Rect(b["bbox"]) for b in page.get_image_info()]
    area = page.rect.get_area()
    draws = []
    for dr in page.get_drawings():
        r = fitz.Rect(dr["rect"])
        if not r.is_empty and 400 < r.get_area() < area * 0.9:
            draws.append(r)
    return imgs, draws


def clean_seam(page, cfg, at_top, at_bottom):
    """Drop the orphan part-sentence at a seam so the page reads whole."""
    ph = page.rect.height
    top, bot = cfg["body_top"], cfg["body_bottom"]
    lines = [l for l in lines_of(page) if l["bbox"].y0 >= top and l["bbox"].y1 <= bot]
    if not lines:
        return 0
    lines.sort(key=lambda l: (l["bbox"].y0, l["bbox"].x0))
    imgs, draws = obstacles(page)
    cuts = []

    def blocked(rect):
        a = max(rect.get_area(), 1.0)
        for o in imgs:                      # a caption sitting on top of a figure
            hit = o & rect
            if not hit.is_empty and hit.get_area() >= 0.25 * a:
                return True
        for o in draws:                     # a table cell or callout around the text
            hit = o & rect
            if not hit.is_empty and hit.get_area() >= 0.55 * a and o.get_area() >= 1.4 * a:
                return True
        return False

    if at_bottom:
        # Cascade back through trailing blocks: cutting a fragment can leave the
        # heading that introduced it stranded, and that has to go as well.
        drop, cursor = [], len(lines) - 1
        for _ in range(3):
            if cursor < 0:
                break
            blk = lines[cursor]["block"]
            grp = [l for l in lines[:cursor + 1] if l["block"] == blk]
            keep_to = -1
            for i, l in enumerate(grp):
                t = plain(l["text"])
                if t and t[-1] in TERM:
                    keep_to = i
            piece = grp[keep_to + 1:]
            if not piece:
                break
            drop = piece + drop
            if keep_to >= 0:
                break                       # this block keeps a finished sentence
            cursor -= len(grp)

        def span_of(group):
            if not group:
                return None
            r = fitz.Rect(group[0]["bbox"])
            for l in group:
                r |= l["bbox"]
            return fitz.Rect(r.x0 - 1, r.y0 - 1, r.x1 + 1, min(bot, r.y1 + 2))

        last_blk = [l for l in drop if l["block"] == drop[-1]["block"]] if drop else []
        for group in (drop, last_blk):      # fall back to the smaller cut
            r = span_of(group)
            if r and r.height <= ph * 0.45 and not blocked(r):
                cuts.append(r)
                break

    if at_top:
        head = [l for l in lines if l["block"] == lines[0]["block"]]
        first = plain(head[0]["text"])
        # only an obvious continuation: starts lower-case or mid-clause
        if first and (first[0].islower() or first[0] in ",;)-"):
            start = -1
            for i, l in enumerate(head):
                t = plain(l["text"])
                if t and t[-1] in TERM:
                    start = i
                    break
            drop = head[:start + 1] if start >= 0 else head
            r = fitz.Rect(drop[0]["bbox"])
            for l in drop:
                r |= l["bbox"]
            r = fitz.Rect(r.x0 - 1, max(top, r.y0 - 2), r.x1 + 1, r.y1 + 1)
            if r.height <= ph * 0.28 and not blocked(r):
                cuts.append(r)

    if cuts:
        redact(page, cuts)
    return len(cuts)


# --------------------------------------------------------------- footer digits
def footer_span(page, cfg):
    ph = page.rect.height
    for ln in lines_of(page):
        for sp in ln["spans"]:
            t = sp["text"].strip()
            if (re.fullmatch(r"\d{1,3}", t) and sp["bbox"][1] > ph - 80
                    and cfg["num_x"][0] < sp["bbox"][0] < cfg["num_x"][1]):
                return sp
    return None


def renumber(doc, cfg, bufs):
    fname = cfg["footer_font"]
    buf = bufs.get(fname)
    done = 0
    for i in range(doc.page_count):
        page = doc[i]
        sp = footer_span(page, cfg)
        if not sp:
            continue
        new = str(i + 1)
        if new == sp["text"].strip():
            continue
        b = sp["bbox"]
        cx, size = (b[0] + b[2]) / 2, sp["size"]
        redact(page, [fitz.Rect(b[0] - 6, b[1] - 1, b[2] + 6, b[3] + 1)])
        page.insert_font(fontname="FTR", fontbuffer=buf)
        f = fitz.Font(fontbuffer=buf)
        w = f.text_length(new, fontsize=size)
        page.insert_text((cx - w / 2, sp["origin"][1]), new,
                         fontname="FTR", fontsize=size)
        done += 1
    return done


# ------------------------------------------------------------- contents pages
def plain(s):
    """Text with the invisible joiners this exporter sprinkles everywhere."""
    return re.sub(r"[​‌ ]", "", s).strip()


def norm(s):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"[​‌]", "", s).lower())


def read_contents(doc, cfg):
    """Read the printed contents list, but take page targets from the outline.

    The printed numbers and the link annotations in both sources are stale by
    several pages. The outline destinations match the real heading pages.
    """
    outline = {}
    for lvl, title, pg in doc.get_toc():
        k = norm(title)
        if k and k not in outline:
            outline[k] = pg

    entries = []
    for pno, first_y, _, _ in cfg["toc_geom"]:
        page = doc[pno - 1]
        links = [l for l in page.get_links()
                 if l.get("kind") == fitz.LINK_GOTO and l.get("page") is not None]
        rows = defaultdict(list)
        for ln in lines_of(page):
            if ln["origin"][1] < first_y - 4 or ln["bbox"].y1 > cfg["body_bottom"]:
                continue
            rows[round(ln["origin"][1], 0)].append(ln)
        for y in sorted(rows):
            group = sorted(rows[y], key=lambda l: l["bbox"].x0)
            num = [l for l in group if l["bbox"].x1 > cfg["num_x"][0]
                   and re.fullmatch(r"\d{1,3}", l["text"].strip())]
            title = [l for l in group if l not in num]
            if not num or not title:
                continue
            txt = re.sub(r"[\u200b\u200c]", "", " ".join(l["text"] for l in title))
            txt = re.sub(r"\u2026", "...", txt)
            txt = re.sub(r"\s+", " ", txt).strip()
            if not txt:
                continue
            key = norm(txt)
            target = outline.get(key)
            if target is None and len(key) >= 18:      # tolerate small text drift
                for k, v in outline.items():
                    if k[:18] == key[:18]:
                        target = v
                        break
            if target is None:
                for l in links:
                    r = fitz.Rect(l["from"])
                    if r.y0 - 2 <= y <= r.y1 + 4:
                        target = l["page"] + 1
                        break
            if target is None:
                target = int(num[0]["text"].strip()) + cfg["num_offset"]
            entries.append(dict(x0=round(min(l["bbox"].x0 for l in title), 1),
                                bold="Bold" in title[0]["spans"][0]["font"],
                                title=txt, size=title[0]["size"], target=target))
    return entries


def write_contents(doc, cfg, entries, bufs, newpage_of):
    geom = [(newpage_of[p], fy, ly, cf) for p, fy, ly, cf in cfg["toc_geom"]
            if p in newpage_of]
    lead = cfg["toc_lead"]
    for np, fy, ly, cf in geom:
        page = doc[np - 1]
        for l in page.get_links():
            if cf - 8 <= fitz.Rect(l["from"]).y0 <= ly + 8:
                page.delete_link(l)
        redact(page, [fitz.Rect(0, cf, page.rect.width, ly + 6)])

    live = [(e, newpage_of[e["target"]]) for e in entries if e["target"] in newpage_of]

    room = sum(int((ly - fy) // lead) + 1 for _, fy, ly, _ in geom)
    if len(live) > room:                       # sections thin out before chapters
        chaps = [x for x in live if x[0]["bold"] or x[0]["x0"] <= cfg["chap_x"] + 2]
        secs = [x for x in live if x not in chaps]
        slots = max(0, room - len(chaps))
        step = max(1, math.ceil(len(secs) / slots)) if slots else 0
        keep = {id(x[0]) for x in chaps + (secs[::step] if slots else [])}
        live = [x for x in live if id(x[0]) in keep]
    live = live[:room]

    reg = fitz.Font(fontbuffer=bufs[cfg["toc_font"]])
    bold = fitz.Font(fontbuffer=bufs[cfg["toc_font_bold"]])
    i = 0
    for np, fy, ly, _ in geom:
        page = doc[np - 1]
        page.insert_font(fontname="TR", fontbuffer=bufs[cfg["toc_font"]])
        page.insert_font(fontname="TB", fontbuffer=bufs[cfg["toc_font_bold"]])
        y = fy
        while i < len(live) and y <= ly + 0.5:
            e, new = live[i]
            fn, fo = ("TB", bold) if e["bold"] else ("TR", reg)
            size, title = e["size"], e["title"]
            limit = cfg["num_right"] - 16 - e["x0"]
            while fo.text_length(title, fontsize=size) > limit and len(title) > 10:
                title = title[:-2]
            if title != e["title"]:
                title = title.rstrip(" .,-") + "..."
            page.insert_text((e["x0"], y), title, fontname=fn, fontsize=size)
            num = str(new)
            w = fo.text_length(num, fontsize=size)
            page.insert_text((cfg["num_right"] - w, y), num, fontname=fn, fontsize=size)
            page.insert_link({"kind": fitz.LINK_GOTO, "page": new - 1,
                              "to": fitz.Point(0, 0),
                              "from": fitz.Rect(e["x0"], y - size,
                                                cfg["num_right"], y + size * 0.3)})
            y += lead
            i += 1
    return len(live)


# ------------------------------------------------------------------------ main
def run(cfg):
    cfg["toc_pages"] = [g[0] for g in cfg["toc_geom"]]
    cfg.setdefault("force_drop", set())
    src = fitz.open(cfg["src"])
    before = src.page_count
    keep, prof = select_pages(src, cfg)
    entries = read_contents(src, cfg)

    # The shorter book needs fewer contents pages. Give the spare ones back.
    for _ in range(3):
        live = sum(1 for e in entries if e["target"] in set(keep))
        caps = [int((g[2] - g[1]) // cfg["toc_lead"]) + 1 for g in cfg["toc_geom"]]
        need, left = 0, live
        for c in caps:
            if left <= 0:
                break
            need, left = need + 1, left - c
        surplus = cfg["toc_pages"][max(1, need):]
        if not surplus:
            break
        cfg["toc_geom"] = [g for g in cfg["toc_geom"] if g[0] not in surplus]
        cfg["toc_pages"] = [g[0] for g in cfg["toc_geom"]]
        cfg["force_drop"] = set(cfg["force_drop"]) | set(surplus)
        keep, prof = select_pages(src, cfg)

    keepset = set(keep)
    bufs = font_buffers(src)
    old_toc = src.get_toc()

    newpage_of = {old: i + 1 for i, old in enumerate(keep)}

    src.select([p - 1 for p in keep])

    seams = 0
    for i, old in enumerate(keep):
        page = src[i]
        at_top = old > 1 and (old - 1) not in keepset and old not in cfg["no_seam"]
        at_bot = old < before and (old + 1) not in keepset and old not in cfg["no_seam"]
        if at_top or at_bot:
            seams += clean_seam(page, cfg, at_top, at_bot)

    nums = renumber(src, cfg, bufs)
    toc_lines = write_contents(src, cfg, entries, bufs, newpage_of)

    new_toc = []
    for lvl, title, pg in old_toc:
        if pg in newpage_of and lvl <= 2:
            new_toc.append([lvl, re.sub(r"[\u200b]", "", title).strip(), newpage_of[pg]])
    src.set_toc(new_toc)

    src.save(cfg["out"], garbage=4, deflate=True, deflate_images=True,
             deflate_fonts=True, use_objstms=1)
    if cfg.get("keep_log"):
        json.dump(keep, open(cfg["keep_log"], "w"))
    print(f"{cfg['out']}\n  pages {before} -> {src.page_count}"
          f"  (kept {src.page_count/before:.0%})"
          f"\n  seams cleaned {seams}, footers renumbered {nums}, contents lines {toc_lines}")
    return before, src.page_count


CNAPP = dict(
    src=r"C:/Users/AtharvaShah/Downloads/[FINAL DRAFT VERSION] CNAPP_2nd Edition.pdf",
    out=r"D:/Atharva/AccuKnox/doc-ppt-template/output/AccuKnox_Zero_Trust_CNAPP_2nd_Edition_Condensed.pdf",
    target=104, protect=[], keep_extra=[3], keep_log="cnapp.keep.json",
    drop_chapters=(2, 4), no_seam={1, 2, 3, 4, 5},
    body_top=45, body_bottom=668, num_x=(250, 340), num_right=535.6, num_offset=3,
    footer_font="Garamond", toc_font="Garamond", toc_font_bold="Garamond-Bold",
    toc_geom=[(4, 124.07, 662.2, 100.0), (5, 95.27, 662.2, 60.0)], toc_lead=15.375, chap_x=55,
)

AGENTIC = dict(
    src=r"C:/Users/AtharvaShah/Downloads/combined english Agentic AI Book (1).pdf",
    out=r"D:/Atharva/AccuKnox/doc-ppt-template/output/AccuKnox_Zero_Trust_Agentic_AI_Security_Condensed.pdf",
    target=85, protect=[(135, 166)], keep_extra=[3], keep_log="agentic.keep.json",
    drop_chapters=(), no_seam={1, 2, 3, 4, 5, 6, 7},
    body_top=45, body_bottom=645, num_x=(250, 340), num_right=541.7, num_offset=3,
    footer_font="Rosarivo-Regular", toc_font="EBGaramond-Regular",
    toc_font_bold="EBGaramond-Bold", toc_lead=17.355, chap_x=26,
    toc_geom=[(5, 93.84, 640.0, 80.0), (6, 72.83, 640.0, 52.0),
              (7, 72.83, 640.0, 52.0)],
)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("cnapp", "both"):
        run(CNAPP)
    if which in ("agentic", "both"):
        run(AGENTIC)
