# doc-ppt-template

Master AccuKnox brand templates for Word and PowerPoint, plus the build scripts that
turn a draft into a branded final file. Read [`README.md`](README.md) for the palette,
the logo rules and the Word workflow. This file holds the rules that get broken most
often, so read it before you write a build script.

## Every Asset Uses Inter and Nothing Else

Every deck, Word doc, PDF, cheatsheet, ebook and diagram uses `Inter`. Never use
`Space Grotesk`, and never add a second display face. Font files for scripts live in
`assets/fonts/`.

## Every Marketing File Follows Two Leadership Rules

Leadership set these rules on 2026-10-28. They apply to every PDF, deck, Word doc, one pager and
image built from this template, by any person or tool. The help repo `CLAUDE.md` carries the
same rules.

**Name the delivered file like a person would.** Use `AccuKnox_<Asset_Type>_<Topic>.<ext>`, Title
Case words joined by underscores, for example `AccuKnox_Case_Study_Stock_Exchange.pdf`. Keep
dates, `-v1` suffixes, lowercase hyphen slugs and words such as draft, final or generated out
of a delivered name. A reader skips a file whose name shows a tool made it. Versioned names
stay in `work/` only, and older versions get deleted once a newer one ships. Set the title
metadata to the same plain name.

**Build every cover clean enough for an enterprise buyer.**

1. Put the AccuKnox logo top left. Directly below it, left aligned: a small uppercase label for
   the asset type, an H1 of 2 to 4 words, and one deck line at most. The long claim goes on
   page 2. On a deck, the template cover (layout 0) stays, and its title follows the same 2 to
   4 word limit.
2. Use flat color only: navy with white and one blue, or white with navy and one blue. Use no
   gradient anywhere on a cover, including art, rules, underlines, glows, fades and shadows.
3. Use one line-art graphic that matches the topic, in the same two colors with one stroke
   weight.
4. Give the graphic its own zone: the top right quarter, or a bottom band of at most 45 percent
   of the page height. It never sits behind, under or across text, stays inside the margins,
   and keeps 12 mm (0.5 in on a slide) of empty space from the text.

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

### 7. Make every deck visual

Text-only slides are a draft. Every deck ships icon-heavy and readable, built the
way the Sampath Bank Secrets Manager deck was. The full method is in
`.claude/skills/accuknox-visual-deck/SKILL.md`. The short version:

- Every content slide carries a picture: an SVG diagram, an icon grid or a row of
  logos. Every list item gets an icon, and every named product gets its real logo
  from `assets/icons/`. Run `scripts/fetch_icons.py` for a missing one.
- Draw each architecture, flow, HA, DR or pipeline as an SVG with `scripts/_aksvg.py`.
  Render it, look at it, and fix it two or three times before it ships.
- Body text is 11 pt or more and nothing goes under 9 pt. A slide holds 70 words
  or fewer. Fine print, sources and exact values go into the speaker notes, and a
  pass that cuts text from a slide moves those facts into the notes.
- Slide 2 is an agenda of icon tiles. Backup material goes on hidden slides.
  Unconfirmed facts get a red `todo_panel()`, never a guess.
- Run `py -3.11 scripts/deck_qa.py output/<deck>.pptx --gslides` before you render.
  It must end with 0 fail.

## The keynote skill

`.claude/skills/accuknox-keynote-deck/` carries the dark keynote system: the `akslides`
runtime with thirteen layouts, the YouTube embed recipe, the QA gate, the source-deck
extractor and the rebrand workflow. Read its `SKILL.md` before you build or rebrand a
deck in that style. `scripts/build_tcts_ai_decks.py` is the worked example it came from.

## Reference builds

`scripts/build_sampath_secrets_manager.py`, with `scripts/sampath_svg.py`, is the
reference for a visual deck: icons, SVG diagrams, notes, hidden slides and the
Google Slides upload. `scripts/build_indigo_azure_posture.py` is the cleanest
example of a table-heavy report. It uses the
two cover helpers, the `_akdeck` primitives, native tables with real borders, and it
passes the punctuation, banned-word and sentence-length checks.
