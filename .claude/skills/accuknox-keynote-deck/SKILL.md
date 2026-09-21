---
name: accuknox-keynote-deck
description: Build or rebrand an AccuKnox PowerPoint deck in the dark keynote style, with a navy canvas, real product screenshots, native diagrams, sourced numbers and embedded YouTube videos. Use this skill whenever the user wants a deck, slides, a pitch, a partner or GTM deck, a customer briefing, a webinar deck, a product overview, a battlecard, or asks to rebrand, restyle, refresh, clean up or "make this deck look good" for AccuKnox, even when they do not name PowerPoint. Also use it when they hand over a .pptx to convert, or ask for a deck that must not look AI generated or boilerplate.
---

# AccuKnox keynote decks

This skill builds the deck style that came out of the TCTS build: a navy canvas,
white product screens as the only light source, one claim per slide, a source
footnote on every slide, and videos that play inside PowerPoint.

Decks built this way do three things the usual card-grid deck does not. They
show the product instead of describing it, they cite where each number came
from, and they read as a sequence of claims rather than a list of features.

## Seven Scripts Do the Repetitive Work

```
scripts/akslides.py      the runtime: brand tokens, primitives, 13 layouts
scripts/pptx_youtube.py  the Online Video XML that PowerPoint accepts
scripts/example_deck.py  every layout with placeholder copy, runnable
scripts/check_deck.py    the gate: punctuation, copy, geometry, image dpi
scripts/extract_deck.py  read a source deck before a rebrand
scripts/render.ps1       export every slide to PNG through PowerPoint
scripts/finalize.ps1     embed the fonts and export the PDF
```

Read `references/design-system.md` before your first slide. It holds the tokens,
the geometry and the rules that decide whether the deck looks expensive.

## Build a New Deck in Seven Steps

1. **Settle the story first.** One claim per slide, written as the slide title.
   Write the titles before anything else and read them top to bottom. If they do
   not argue a case on their own, the deck will not either.
2. **Find the evidence.** Every number, framework, integration and customer
   result needs an opened source: a live product page, a case study, a help doc
   or an internal deck you can name. Facts with no source get cut or bracketed,
   never softened into a claim.
3. **Pick a layout per slide** from `references/layouts.md`. The layout follows
   the kind of point: argument, number, picture, mechanism or evidence.
4. **Prepare the imagery** with `references/imagery.md`. Crop tight, mask
   customer data, keep 140 dpi or better at placed size.
5. **Write the build script.** One Python file holds every word and position, so
   a revision is an edit and a rerun. Copy the shape of `example_deck.py`.
6. **Render, look, fix.** Follow `references/qa.md`. Look at every slide. The
   render is the only place a collision shows up.
7. **Finalize.** `finalize.ps1` embeds Space Grotesk and writes the PDF, so the
   deck survives a machine that lacks the font.

```bash
py -3.11 scripts/example_deck.py
powershell -File scripts/render.ps1 -Pptx output/My_Deck.pptx -Out output/render/my_deck
py -3.11 scripts/check_deck.py output/My_Deck.pptx
powershell -File scripts/finalize.ps1
```

## Rebrand an Existing Deck by Rebuilding It

Read `references/rebrand.md` for the full workflow. The short version: extract
what the old deck says and owns, decide what survives, then rebuild it in this
system rather than restyling it in place.

```bash
py -3.11 scripts/extract_deck.py "Old Deck.pptx" work/olddeck
powershell -File scripts/render.ps1 -Pptx "Old Deck.pptx" -Out work/olddeck/render
```

A rebrand is mostly subtraction. A typical source slide carries 90 words and one
stock graphic. The rebuilt slide carries a claim, one real screen and a source.
Say out loud what you cut, because the owner of the old deck will ask.

## Eight Rules Decide Whether the Deck Looks Expensive

These came from slides that failed review, so they are cheap to follow and
costly to skip.

- **One idea per slide, under 40 words of body copy.** If a slide needs more,
  it is two slides.
- **Titles state a claim in AP Title Case.** "One Dashboard Ranks Every AI Asset
  by Risk" works. "AI asset inventory" does not. Break a long title yourself
  with `\n` so no single word lands alone on line two.
- **Every slide carries one real thing:** a product screen, a native diagram, a
  large number or an embedded video. A slide of text is a slide of nothing.
- **Screens bleed off the edge.** A screenshot that runs past the right or the
  bottom reads as a window into a live product. One shrunk to fit reads as a
  brochure.
- **Depth comes from alpha, never from new colors.** White at 6 to 16 percent
  over navy, plus one soft accent glow behind the screen.
- **Numbers carry their unit and their source.** The footnote names the page or
  deck. A partner seller needs to answer "where is that from" in one breath.
- **Never draw the cover or the closing slide.** They come from
  `PPT Template.pptx` layouts 0 and 1, with the lockup and the badge rows.
- **Say which layer a proof point proves.** Runtime numbers are not AI numbers.
  Claiming across that line is what a technical buyer catches first.

## This Style Refuses Nine Things

Four-card grids with icon, heading and paragraph. Eyebrow labels over titles.
Gradient fills. Stock photography of server rooms. Em dashes, en dashes and
semicolons anywhere in the copy. Body text under 8 pt. A screenshot that still
shows a customer name, an email address, a cloud account id or a token.

## Each Reference File Answers One Question

| File | Read it when |
|---|---|
| `references/design-system.md` | Before the first slide. Tokens, geometry, type. |
| `references/layouts.md` | Choosing a layout, or wiring its data. |
| `references/rebrand.md` | Converting an existing deck into this style. |
| `references/imagery.md` | Preparing screenshots, posters, logo walls, masks. |
| `references/video.md` | Embedding a YouTube video that plays in the slide. |
| `references/qa.md` | After every build. The render loop and the gates. |
| `references/gotchas.md` | When a command fails on this machine. |

The worked example that produced this style is
`scripts/build_tcts_ai_decks.py` in this repo: three eleven-slide partner decks,
every layout in use, every fact sourced.
