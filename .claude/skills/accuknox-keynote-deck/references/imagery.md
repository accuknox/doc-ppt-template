# Imagery

The screens carry this deck, so the image work decides how it lands. Budget as
much time for cropping and masking as for writing the slides.

## Four Sources, in This Order

1. **A live console capture.** The best option and the one to ask for. One
   current console, one tenant, no version drift between slides.
2. **The product UI mirror.** `D:\Atharva\AccuKnox\product-ui-assets` holds the
   Drive folder's images at full size, indexed in the blog writer skill's
   `media/INDEX.md`. These are usually 2880 px wide and clean.
3. **The help docs.** `HelpDocs/docs/**/images` has real screens, but they span
   several console versions, so a deck built from them mixes two looks.
4. **An internal deck.** Extract the embedded media rather than screenshotting
   the slide, and re-export the source slide at 2560 x 1440 when the picture you
   need is a group of shapes rather than one image.

```bash
# every embedded picture over 120 KB, named by slide
py -3.11 scripts/extract_deck.py "Source Deck.pptx" work/source
# a source slide at double resolution, when the picture is drawn shapes
powershell -File scripts/render.ps1 -Pptx "Source Deck.pptx" -Out work/source/hi
```

`render.ps1` exports at 1280 x 720. For crops, copy it and raise the numbers in
the `Export` call to 2560 x 1440, the way the TCTS build did for its logo cards.

## Crop to the Part That Argues

A full-page screenshot shrunk to fit says nothing at slide size. Crop to the one
region the pin will name, and let the crop keep the app's own edges, because the
sidebar and the top bar are what make it read as a product.

Write the crop into a prep script rather than doing it by hand, so a refresh is
a rerun:

```python
from PIL import Image
dash = Image.open(RES / "dashboard.png").convert("RGB")
dash.crop((0, 0, round(885 * 1.605), 885)).save(OUT / "a3_dashboard.png")
```

Aim for a 1.6:1 crop for a main screen on the right, because that matches the
6.95 x 4.33 in window the `annotated` layout uses.

## Mask Customer Data Before It Reaches a Slide

Blurring looks unfinished. Paint neutral skeleton bars over the text instead,
which reads as deliberate masking and keeps the layout intact:

```python
MASK = (227, 231, 240)
d.rectangle((1086, 432, 1478, 588), fill="white")        # clear the rows
for y, w in zip((442, 472, 503, 533, 564), (190, 260, 230, 250, 220)):
    d.rounded_rectangle((1090, y, 1090 + w, y + 12), radius=6, fill=MASK)
```

Mask or crop out, every time: customer names and file names that imply one, real
email addresses, cloud account ids, tenant names in the top bar, JWT prefixes and
API keys, staff names, and internal-only product names. Cropping above the app's
top bar removes the tenant switcher and the user menu in one move, which handles
most of these at once.

## Place at 140 DPI or Better

A picture placed wider than its pixels can carry looks soft on a projector.
`check_deck.py` flags anything under 140 dpi at placed size. A 1,420 px crop
across 6.95 in is 204 dpi and looks crisp. If the only copy is small, re-export
the source rather than scaling it up.

## Treatment Is the Same Every Time

```python
picture(slide, path, x, y, w, radius=0.02, line_alpha=26)   # runtime helper
```

Rounded corners at 2 to 4 percent, a white hairline at 26 percent, a soft shadow
under it, and one accent glow behind. An inset gets a stronger hairline (35
percent) and a heavier shadow so it reads as a layer above the main screen.

Main screens bleed off the right and bottom edges. Insets sit inside the canvas
and overlap the main screen by a little, which is what gives the slide depth.

## Video Posters Need a Play Button

A poster is a still from inside the video, not the YouTube thumbnail, because
marketing thumbnails carry headlines that fight the slide. Pick a frame that
shows real console, mask anything sensitive in it, and composite a play button
so a printed copy still reads as a video:

```bash
ffmpeg -ss 110 -i source.mp4 -frames:v 1 poster.png   # full path, see gotchas.md
```

`prep_posters.py` in the TCTS assets folder is a working example: it masks two
regions, pads a non-16:9 frame on black, and draws a navy play disc with a white
triangle and a soft shadow.

## Logo Walls Come From the Source, Not From the Web

When you need a platform grid, take the one the product team already drew.
Downloading vendor logos one by one produces inconsistent sizes and licence
questions, and the existing grid is already arranged and approved.
