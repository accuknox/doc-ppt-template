---
name: accuknox-visual-deck
description: Make any AccuKnox deck visual, icon-heavy and easy to read, on the light branded template. Use this skill for every deck, slide, presentation, pitch, customer briefing, architecture walkthrough, RFP response deck, POC plan or Google Slides deck built from PPT Template.pptx, and whenever the user says a deck is "too much text", "text text text", "make it visual", "add icons", "add diagrams", "make it readable" or "make it look like the Sampath deck". Covers icons, SVG diagrams, font sizes, speaker notes, the agenda slide, red placeholder panels, the QA gate and the Google Slides upload.
---

# Visual AccuKnox Decks

A deck reads as pictures first and words second. Every content slide carries a
diagram, an icon grid or a row of logos, and the fine print lives in the speaker
notes. This is the method behind the Sampath Bank Secrets Manager deck, which a
reviewer called the standard for every deck after it.

The worked example is two scripts. Read them before your first slide:

- `scripts/sampath_svg.py` builds eight diagrams from the SVG kit.
- `scripts/build_sampath_secrets_manager.py` builds the 19-slide deck.

## Six Files Supply the Icons, Diagrams and Gate

| File | Job |
|---|---|
| `assets/icons/brand/` | Real logos: Devicon (MIT) in full color, Simple Icons (CC0) as `si-*` |
| `assets/icons/ui/` | Tabler outline glyphs (MIT), recolored to any brand color |
| `scripts/fetch_icons.py` | Pull a missing icon by name. `--list` shows what is here |
| `scripts/_aksvg.py` | SVG kit: `ui`, `logo`, `text`, `rect`, `pill`, `chip`, `card`, `arrow`, `curve`, `cyl`, `badge`, `boundary`, `render`, `icon_png`, `contact_sheet` |
| `scripts/_akdeck.py` | Slide helpers: `icon_img`, `icon_tile`, `icon_card`, `logo_row`, `callout`, `todo_panel`, `diagram`, `label`, `notes`, `hide_slide`, `google_safe` |
| `scripts/deck_qa.py` | The gate: font floor, notes, off-slide shapes, punctuation, text-only slides |

Rendering uses headless Microsoft Edge, so no SVG library is needed.

## Ten Rules Keep a Deck Visual and Readable

1. **Give every item an icon.** Each list item, component, step, job and fact gets a glyph from `assets/icons/ui`. A bullet list with no icons is a draft.
2. **Show real logos for named tech.** Java, .NET, Python, Node.js, PHP, Kubernetes, VMware, Oracle, PostgreSQL, Entra ID and every other named product gets its real logo. Fetch it if it is missing.
3. **Draw one diagram per concept.** Architecture, request flows, HA, DR, pipelines and boundaries get an SVG from `_aksvg`. A table of components becomes an icon grid. A sequence becomes numbered icon steps with arrows.
4. **Iterate each diagram two or three times.** Render it, open the PNG and look for text that overflows a box, labels on top of arrows, and dead space. Fix them, then render again. The first render is never the one that ships.
5. **Keep type big.** Body text 11 pt or more, headings 13 to 17 pt, labels 9.5 pt or more, code 9.5 pt or more. Nothing goes under 9 pt, and the gate fails it. In a diagram, keep text at 17 px or more on a 1280 px canvas placed 9.2 in wide.
6. **Keep 70 words or fewer on a slide.** Move the rest into the speaker notes with `notes()`. That covers exact values, image tags, file paths, sources, RFP clauses and the talk track.
7. **Never lose data.** When a pass cuts text from a slide, the same facts go into that slide's notes. A reviewer must be able to rebuild the old slide from the notes.
8. **Put the agenda second.** Slide 1 is the template cover. Slide 2 is the agenda: six or fewer icon tiles, each with a number and its slide range. Backup material goes on hidden slides via `hide_slide()`, never deleted.
9. **Mark unknowns in red.** A fact with no opened source gets a `todo_panel()` that names who fills it. Never guess a value to make a slide look finished.
10. **Close each slide on one sentence.** A `callout()` strip carries the takeaway in plain words, with an icon.

## Ten Layouts Replace Text Slides

| Content | Layout | Helpers |
|---|---|---|
| Agenda | 3 x 2 icon tiles, big number, slide range | `icon_tile`, `box` |
| Architecture | Full-width SVG, 9.2 in | `_aksvg` plus `diagram` |
| Components or jobs | 3 x 3 or 3 x 2 grid of icon cards, status pill | `icon_card` |
| Request flow or process | Numbered icon steps with arrows, SVG | `_aksvg.badge`, `arrow` |
| Options compared | 4 columns, mini diagram each, "code change" pill | SVG plus `callout` |
| Effort per platform | Logo row, then rows of logos, name, effort pill | `logo_row`, `pill` |
| Code before and after | Two dark panels, language logo in the header | `code_block`, `icon_img` |
| HA or DR | SVG on the left, 5 icon facts on the right | `diagram`, `icon_tile` |
| Numbers that matter | Stat row of 3 | `stat` |
| Next steps | Icon timeline, icon checklist, navy ask box | `icon_tile`, `box` |

## The Build Loop Ends at Zero Gate Failures

```bash
py -3.11 scripts/<deck>_svg.py
```

```bash
py -3.11 scripts/build_<deck>.py
```

```bash
py -3.11 scripts/deck_qa.py output/<deck>.pptx --gslides
```

```bash
powershell -File scripts/render.ps1 -Pptx "<abs path>.pptx" -Out "<abs path to render dir>"
```

Pass absolute paths to `render.ps1`, because a relative `-Out` fails. Then tile
the PNGs with `_aksvg.contact_sheet()` and read every slide. Check for wrapped
titles, text that crosses a panel, and empty bands at the bottom of a slide. Fix
them and loop. `deck_qa.py` must end with 0 fail.

## Google Slides Needs Two Font and Icon Swaps

1. Call `google_safe()` at the top of the build. Code then uses JetBrains Mono, a Google Font.
2. Use `icon_img()` for every icon. The older `icon()` draws Segoe MDL2 glyphs, which show as empty boxes in Slides.
3. First upload, converted to Slides:

```bash
gws drive files create --json '{"name":"<title>","mimeType":"application/vnd.google-apps.presentation"}' --upload output/<deck>.pptx --params '{"fields":"id,webViewLink"}'
```

4. Later builds replace the content behind the same link:

```bash
gws drive files update --params '{"fileId":"<id>","fields":"id,webViewLink"}' --upload output/<deck>.pptx
```

5. Export the Slides file to PDF with `gws drive files export` and look at it. Hidden slides keep their flag, and the notes carry over.

## Every Label Follows the Writing Rules

The writing rules in `CLAUDE.md` still apply to every word, including diagram
labels. Titles state a claim, such as "Three Nodes Keep Serving Secrets When One
Fails". A topic label such as "High Availability" fails. Run the slop scorer on
the slide text and the notes together:

```bash
python "D:\Atharva\NOTES\SCRIPTS\slop\score.py" "output/<deck>_text.md"
```
