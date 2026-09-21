# Design system

The whole look comes from four decisions: a navy canvas, white screens as the
light, a closed palette, and one claim per slide. Everything below serves those.

## Three References Set the Direction

Naming references beats naming adjectives, because "modern" and "clean" produce
generic output while a reference plus one sentence produces the thing you meant.

| Reference | What this deck takes from it |
|---|---|
| [Refero](https://refero.design) | Real app UI shown one component at a time, cropped tight. Never a full-page screenshot shrunk to fit. |
| [Dark Mode Design](https://www.darkmodedesign.com) | The navy canvas, so a white product screen becomes the light source on the slide. |
| [Awwwards](https://www.awwwards.com) | Type-led claims, oversized numerals, and most of the slide left empty. |

## The Palette Stays Closed

```python
NAVY    = 11206D   # the canvas, every content slide
NAVY_DK = 0A144A   # panels that must sit behind, video wells
PRIMARY = 0046FF   # accent one
SECOND  = 6464FF   # accent two
PURPLE  = 4D4DD9
RED     = C80019   # block, risk, the "before" column
GREEN   = 16A55C   # allow, pass, the "after" column
WHITE   = FFFFFF
SOFT    = B8C4E8   # secondary text on navy
```

Give each deck in a set its own accent, so a seller can tell three decks apart
at a glance: AISPM took `PRIMARY`, the Prompt Firewall took `RED`, and Agentic
took `SECOND`.

Depth comes from alpha, not from new colors. White at 6 percent is a card, 10 to
16 percent is a raised card, and a hairline runs at 16 to 30 percent. One soft
accent glow sits behind the main screen at 32 to 40 percent with a 60 to 80 pt
soft edge. Without that glow the screens read as pasted rectangles.

## The Geometry Is Fixed

```
slide          10.0 x 5.625 in (16:9)
side margin    0.55 in, and nothing important crosses it
title row      y 0.40, height 1.1, 22 pt Space Grotesk Medium
body starts    y 1.45
footnote       y 5.34, 8 pt, the source line
logo           top right, 1.2 in wide, y 0.46
```

A screenshot on the right starts at x 3.30 and runs to x 10.25, which is past
the slide edge on purpose. PowerPoint clips it, and the clipped edge is what
makes the slide feel like a window rather than a page.

## The Type Scale Has Six Steps

| Step | Size | Font | Use |
|---|---|---|---|
| Display | 80 pt | Medium | The one number on a proof slide |
| Section | 34 pt | Medium | A part divider |
| Title | 22 pt | Medium | Every content slide |
| Lead | 32 pt | Medium | A supporting number |
| Body | 11 to 12 pt | SemiBold for heads, Regular for prose | Rail heads, node labels |
| Caption | 7 to 9.5 pt | Regular, or SemiBold with 1.2 pt tracking for labels | Subs, chips, footnotes |

Space Grotesk carries all of it. Medium and SemiBold are separate installed
families on this machine, so `"Space Grotesk Medium"` is a real typeface name
rather than a weight flag. `finalize.ps1` embeds them, which is what keeps the
deck intact on a machine that never installed the font.

## Every Slide Answers One Question

Write the titles first, read them top to bottom, and check that they argue a
case without the bodies. A title states a claim in AP Title Case with a risk, a
control, a number or an outcome in it.

- Strong: "IDT Put Kernel Enforcement on 30,000 Devices in One Week"
- Weak: "Customer success" or "Runtime security overview"

Break a long title yourself with `\n` at a phrase boundary. PowerPoint will not
balance the line for you, and one orphaned word on line two is the fastest way
to look unfinished.

## Body Copy Stays Under Forty Words

Sentences run to 20 words or fewer. Prose beats bullets for two items, and a row
of three parallel items beats prose. No em dashes, no en dashes, no semicolons,
and none of the banned words the repo scorer blocks.

Each slide carries at most one honest limit, stated plainly. A named limitation
is the most credible line on a technical slide, and it is the first thing a
polish pass deletes.

## Speaker Notes Carry the Sources

The visible footnote names where a fact came from in one line. The speaker note
carries the full trail: the deck and slide number, the page URL, the tenant a
screenshot came from, and any caveat the presenter should know but not show.
That split keeps the slide clean and the seller safe.
