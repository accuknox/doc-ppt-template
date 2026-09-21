# QA

A deck is not done when the script runs. It is done when you have looked at
every rendered slide and found nothing new to fix.

## Run Four Commands in This Order

```bash
py -3.11 build_<name>.py
py -3.11 scripts/check_deck.py output/<Name>.pptx
powershell -File scripts/render.ps1 -Pptx output/<Name>.pptx -Out output/render/<name>
powershell -File scripts/finalize.ps1
```

`check_deck.py` catches what a render hides: an em dash inside a table cell, a
23-word sentence, a shape that crosses the margin, a picture placed at 90 dpi.
It exits 1 on a blocking finding, so a build script can gate on it.

`render.ps1` exports every slide to PNG through PowerPoint COM, which renders
the real fonts. Tile the PNGs four to a sheet and look at them. Every layout
collision in the TCTS build showed up here and nowhere else.

`finalize.ps1` re-saves each deck with the fonts embedded and exports a PDF.
Export the PDF even when nobody asked for one, because a raw newline inside a
run renders fine as PNG and draws a tofu box in the PDF.

## Look for These Twelve Things

Walk each rendered slide with this list. It is short because each item came from
a real defect.

1. A title with one orphaned word on line two.
2. A title that collides with the body under it.
3. A two-line label that runs into the text below it.
4. A pin sitting on top of the label it points at.
5. An inset covering rail text on the left.
6. A footnote wrapping to two lines and falling off the slide.
7. A chip row running past the right margin.
8. A number whose unit or source is missing.
9. Body copy over 40 words, or a sentence over 20 words.
10. A screenshot still showing a tenant name, an email or an account id.
11. A screen placed soft, under about 140 dpi at its placed size.
12. Two consecutive slides with the same layout.

## Run the Writing Gate on the Extracted Text

Pull every word out of the built deck and score it with the shared scorer, which
is the same gate the repo uses for prose:

```bash
py -3.11 scripts/deck_text.py output/<Name>.pptx > work/deck-text.md
python "D:\Atharva\NOTES\SCRIPTS\slop\score.py" work/deck-text.md
```

CRIT must reach 0. Two findings are expected and safe to ignore: the extractor's
own `## Slide n` headings read as topic labels, and chip rows read as verbless
fragments because they are lists.

When the scorer flags a banned word inside a customer quote, do not edit the
quote. Trim it at a clause boundary and mark the cut, or drop the quote.

## Check the Deck File Itself

```python
import zipfile, re
z = zipfile.ZipFile("output/Deck.pptx")
print(len([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]))
print(len([n for n in z.namelist() if n.startswith("ppt/fonts/")]))   # 7 after finalize
```

Confirm the slide count, the embedded fonts, and that each video slide still
carries its `youtube.com/embed/` relationship after the PowerPoint re-save.

## Hazards That Must Never Ship

- A screenshot with a customer name, a real email, a cloud account id, a token
  or a tenant switcher showing a real tenant.
- A slide image lifted from a deck whose cover carries an NDA or "limited
  distribution" mark. Take the facts, redraw the picture.
- An internal-only product name in a visible label.
- An open-source engine name that the product masks.
- A competitor named anywhere except a sourced comparison.
- A number attributed to a customer when it belongs to a platform-wide template
  block, which is a trap on case study pages.
- A capability marked Beta or Coming Soon presented as shipped.

## Look Once, Then Stop

Three passes is usually enough: build, fix what the render shows, fix what the
gate shows. A fourth pass tends to trade one small imperfection for another,
and the deck is already better than the room needs.
