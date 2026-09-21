# Rebrand an existing deck

A rebrand in this style is a rebuild, not a restyle. You keep the argument and
the evidence, and you throw away the layout. Restyling in place fails because
the old deck's shape is the problem: 90 words on a slide stays 90 words after
you change its colors.

Budget roughly 20 minutes per surviving slide, and expect the slide count to
drop by a third.

## Read the Source Before You Touch It

```bash
py -3.11 scripts/extract_deck.py "Old Deck.pptx" work/olddeck
powershell -File scripts/render.ps1 -Pptx "Old Deck.pptx" -Out work/olddeck/render
```

That writes `inventory.md` (one row per slide: title, word count, pictures,
hazards), `content.json` (all text and notes) and `media/` (every embedded
picture over 120 KB). Then look at the rendered PNGs. Reading the text alone
hides what the slide actually shows, and looking alone hides what the notes say.

The hazard column is the one to act on first. It flags customer emails, cloud
account ids, tokens, confidentiality marks and internal-only product names.
Anything it flags either gets cropped, masked or dropped.

## Sort Every Slide Into Four Piles

Go through the inventory once and label each slide:

- **Keep the claim.** The slide says something true and useful. Rewrite the
  title as a claim, pick a layout, keep the evidence.
- **Keep the asset.** The slide is weak but owns a good screenshot, diagram or
  customer number. Harvest the asset, drop the slide.
- **Merge.** Two or three slides make one point between them. They become one
  slide with a claim and the best evidence from each.
- **Cut.** A topic label, a stock graphic, a wall of text with no fact, a
  roadmap under NDA, or anything the hazard column condemns.

Write this list out and show it to whoever owns the old deck before you build.
The argument about what to cut is cheaper before the rebuild than after.

## Map Each Survivor to a Layout

The old shape usually points straight at the new layout.

| Old slide | New layout |
|---|---|
| Bulleted feature list | `statement` with three points, or `cases` with three tagged uses |
| Four icon cards | `cases`, or `matrix` if the cards were really a table |
| A busy vendor diagram | Redraw with `lanes`, `pipeline` or a `cases` art callable |
| A full-page screenshot | `annotated`, cropped to the part that matters |
| A logo wall | `image` with a rail of three facts |
| A table of platforms | `matrix`, four rows at most |
| Customer logos and quotes | `proof`, one large number and a quote |
| A "journey" or "phases" graphic | `timeline` |
| An agenda of nouns | `agenda`, with each row naming what its section proves |

If a slide maps to nothing, it is usually a cut.

## Rewrite Every Title as a Claim

This is the step that changes how the deck reads, and it costs an hour on a
30-slide deck. Take the old title and the slide's own content, and write the
sentence the slide proves.

- "Platform overview" becomes "One Control Plane Covers Code, Cloud and Runtime"
- "Benefits" becomes "Three Numbers Decide the Pilot"
- "Architecture" becomes "Four Discovery Modes Reach Cloud, VM and On-Prem"

Then read the new titles top to bottom on their own. That sequence is the deck.
If it does not argue a case, reorder before you build a single slide.

## Harvest the Imagery, Then Clean It

Keep the real product screens and the real diagrams. Drop the stock art, the
cartoon icons and the sticky notes.

A diagram from an old deck is usually rebuilt rather than reused: the TCTS decks
redrew the architecture natively because the source had sticky notes, clip art
and an NDA mark on the deck cover. A redraw takes 30 minutes with `node`,
`arrow` and `panel`, and it comes out sharp at any zoom.

For screenshots, follow `references/imagery.md`: crop tight, mask any customer
data, and check the placed dpi. If the only copy of a screen is 480 px wide,
re-export the source slide at 2560 x 1440 through `render.ps1` and crop that
instead.

## Carry the Sources Across

Old decks state numbers with no source. Before a number survives the rebrand,
find where it came from: a live page, a case study, a help doc, a named internal
deck with its slide number. Put the short version in the footnote and the full
trail in the speaker notes.

Numbers that no source supports get one of three treatments. Ask the owner for
the source, write the gap in visible brackets so it cannot ship by accident, or
drop the claim to what the evidence supports. Never smooth it into a confident
sentence, because an invented specific is the defect a reader cannot catch.

## Build, Render and Show the Diff

Write one build script that holds every word. Then render both decks and put
them side by side, old on the left and new on the right, so the owner sees what
changed rather than reading about it.

```bash
py -3.11 build_<name>.py
powershell -File scripts/render.ps1 -Pptx output/<Name>.pptx -Out output/render/<name>
py -3.11 scripts/check_deck.py output/<Name>.pptx
powershell -File scripts/finalize.ps1
```

Report three things when you hand it back: the slides you cut and why, the
claims you changed because the source did not support the old wording, and the
hazards you found in the original. That last one is often the most valuable part
of the rebrand.
