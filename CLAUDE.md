# doc-ppt-template

Master AccuKnox brand templates for Word and PowerPoint, plus the build scripts that
turn a draft into a branded final file. Read [`README.md`](README.md) for the palette,
the logo rules and the Word workflow. This file holds the rules that get broken most
often, so read it before you write a build script.

## Hard rules for every deck

### 1. The cover and the closing slide already exist. Use them.

`PPT Template.pptx` ships both. Do not design your own, do not rebuild them from
shapes, and do not reach for a section layout because it looked close enough.

| Layout | Name | Use |
|---|---|---|
| `prs.slide_layouts[0]` | `AccuKnox Intro Title` | **Front cover, always.** Carries the full AccuKnox lockup with the "Secure Code to Cognition" tagline, the three badge groups (Certified & Accredited by / As Featured In / Available On) and the product screenshot collage. |
| `prs.slide_layouts[1]` | `AccuKnox Section Title` | **Back cover, always.** Carries the centered lockup, the "Certified by" badge row and www.AccuKnox.com. |
| `prs.slide_layouts[2]` | `AccuKnox Section Title Basic` | Part dividers only. The dark dotted-wave background. |
| `prs.slide_layouts[4]` | `Standard No Content` | Every content slide. Navy title band, white body. |

Build both covers through the helpers, which set the text color and sizes the
placeholders do not inherit:

```python
from _akdeck import cover_slide, closing_slide

cover_slide(prs, "Azure Cloud Security and AI Posture Report",
            scope=[("30", "Azure subscriptions"), ("11,221", "Cloud assets"),
                   ("31,439", "Active findings")])
...
closing_slide(prs)                      # SEE US IN ACTION / support@accuknox.com
```

Two failures to avoid, both reported by reviewers on real decks:

- **Never open a deck on layout 2.** The dark dotted wave is the part-divider
  background. A deck that opens on it makes slide 1 and slide 2 look like the same
  slide, and the cover stops catching the eye.
- **Never close a deck on layout 2 either.** The closing slide is layout 1.

### 2. Keep the cover light

The lockup, the badges and the screenshots already carry the brand. The words on the
cover are the title, plus at most one supporting line or a short row of scope numbers.

Do not add to a cover: a second AccuKnox logo in the corner, a category eyebrow
(`AZURE · CSPM · CNAPP`), a "prepared by AccuKnox" line, a horizontal rule, or a
footnote about the data basis. Every one of those competes with the title. Move the
data basis to the first content slide instead.

### 3. Never put a raw newline inside a run

`run.text = "Line one\nLine two"` writes the newline straight into `<a:t>`.
PowerPoint's PNG export breaks the line, and its PDF export draws a tofu box. Use
`_akdeck.runs()`, or `box()` and `para()`, which route through it and emit a real
`<a:br/>`. Check the PDF, not only the PNGs, because the PNGs hide this one.

### 4. Render and look before you call it done

```bash
py -3.11 scripts/build_<name>.py
```

```bash
powershell -File scripts/render.ps1 -Pptx output/<name>.pptx -Out output/render/<name>
```

Then open the PNGs and read them. Check the cover, the closing slide, and every panel
for text that crosses a panel border or runs off the slide. Export a PDF too, because
the PDF catches the newline bug and some font fallbacks the PNGs do not.

### 5. Colors

Use the palette in `README.md`. Do not invent hues. For severity, the brand-safe ramp
is High `RED #C80019`, Medium `SECOND #6464FF`, Low `GREEN #16A55C`, and green for a
zero-Critical count, because zero Critical is good news. Badge tints:
`RED_LT` on `RED` for Critical, `LAV` on `PURPLE` for High, `GREY_BG` on `MUTE` for
Medium, `GREEN_LT` on `GREEN_DK` for a clean result.

### 6. Writing style

The rules in `README.md` under "Writing style rules" apply to every word on every
slide, including table cells and chart labels. No em dashes, no en dashes, no
semicolons, no banned words, and no sentence over 20 words. Verify:

```bash
python "D:\Atharva\NOTES\SCRIPTS\slop\score.py" "<extracted-deck-text>.md"
```

CRIT must reach 0. The `readability-fragment` warnings on chart labels and headings
are expected and do not block.

## Reference builds

`scripts/build_indigo_azure_posture.py` is the cleanest current example. It uses the
two cover helpers, the `_akdeck` primitives, native tables with real borders, and it
passes the punctuation, banned-word and sentence-length checks.
