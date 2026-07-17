# doc-ppt-template

Master AccuKnox brand templates for Word documents and PowerPoint decks, plus the
build scripts used to turn any draft into an AccuKnox-branded final file. This repo
is the single source of truth for "how do I brand this doc/deck like AccuKnox."

New to this? Start with [`How_to_Generate_AccuKnox_Branded_Docs_and_PPTs_with_Claude_Code.pdf`](How_to_Generate_AccuKnox_Branded_Docs_and_PPTs_with_Claude_Code.pdf),
a short walkthrough of the Claude Code workflow: clone this repo, attach the file
you want branded, reference the templates with `@`, and let Claude do the rest.

## What's in here

The root holds the two brand template files plus the how-to guide. Raw logo
files and the official brand guidelines live in `assets/`. Everything else,
the build, render, and verify tooling, lives in `scripts/`.

| File / folder | What it is |
|---|---|
| `WORD_TEMPLATE_ACCUKNOX.docx` | Master Word template. Logo + title in the header, page numbers in the footer, brand fonts embedded, and `Title` / `Subtitle` / `Heading1-6` / `Normal` styles pre-configured. |
| `PPT Template.pptx` | Master PowerPoint template. A brand layout showcase, one example slide per master layout (Intro Title, Section Title, Standard With Content, ...). This is the one reference PPTX, build decks by adding slides from its layouts. |
| `How_to_Generate_AccuKnox_Branded_Docs_and_PPTs_with_Claude_Code.pdf` | Short walkthrough of the Claude Code branding workflow, prerequisites, steps, an example prompt, and before/after screenshots. |
| `assets/logos/` | The 5 official logo files, see [Logos](#logos) below for which one to use where. |
| `assets/accuknox-brand-guidelines.pdf` | The official one-page brand guidelines: logo variants, clear space, color palette, typography. Source of truth if this README and the PDF ever disagree. |
| `scripts/build.py` | Historical reference build (a past, populated proposal deck edited by shape index). Read it for the helper-function patterns, it won't run successfully as-is against `PPT Template.pptx`. |
| `scripts/render.ps1` | Exports every slide of a `.pptx` to PNG via PowerPoint COM automation, for visual review. |
| `scripts/final_check.py`, `scripts/verify.py` | Scan a built `.pptx` for em/en dashes and other banned writing-style tells (see below). |

## Logos

| File | Looks like | Use it on |
|---|---|---|
| `assets/logos/accuknox-logo-light-bg.png` | Full horizontal lockup, blue wordmark | Light backgrounds, most doc/deck headers |
| `assets/logos/accuknox-logo-dark-bg.png` | Full horizontal lockup, white wordmark | Dark/navy backgrounds |
| `assets/logos/accuknox-logo-square-light-bg.png` | Stacked icon-over-wordmark, blue | Light backgrounds, square placements (title cards, app tiles) |
| `assets/logos/accuknox-logo-square-dark-bg.png` | Stacked icon-over-wordmark, white | Dark backgrounds, square placements |
| `assets/logos/accuknox-emblem.png` | Icon only, no wordmark | Favicons, social badges, thumbnails, anywhere too small for the wordmark to read |

Pick the variant by background, not by convenience, never place the light-bg (blue
wordmark) version on a dark or busy background just because it's the first one you
grabbed. Full details, clear-space rules, and the monochrome/registration-mark
variants not included here are in `assets/accuknox-brand-guidelines.pdf`.

## Brand basics

**Fonts**
- Primary: `Space Grotesk` (Regular, Medium, Semibold, Bold). Embedded directly in `WORD_TEMPLATE_ACCUKNOX.docx`, no install needed when you edit that file in Word.
- Fallback: `Inter` (Regular, Medium, Semibold, Bold), use only where Space Grotesk isn't available.

**Colors**

Core identity, per `assets/accuknox-brand-guidelines.pdf`:

| Name | Hex | Use |
|---|---|---|
| Primary Blue | `#0046FF` | Core brand color, wordmark on light backgrounds |
| Secondary Blue | `#6464FF` | Accent, the cube in the emblem |
| Red | `#C80019` | Part of the emblem gradient, accents |
| Deep Navy | `#0000C8` | Part of the emblem gradient, dark backgrounds |

Extended UI colors, empirically pulled from the templates in this repo, used for
things the one-pager doesn't cover (table shading, status text, doc headings):

| Name | Hex | Use |
|---|---|---|
| Navy (UI) | `#11206D` | Dark UI panels, table headers |
| Heading blue | `#003BF6` / `#0000FF` | Word template heading colors (`Heading1-4`) |
| Purple | `#4D4DD9` | Secondary accent |
| Green | `#16A55C` (light `#0B7A42`, tint `#E7F6EE`) | "Live" / "Yes" / advantage state |
| Grey (placeholder) | `#EEF0F6` fill / `#C4CCDE` border | Screenshot placeholders, table borders |

Don't invent new brand colors. If a design need doesn't fit either palette, ask
before picking your own.

## Branding a Word document

1. Open `WORD_TEMPLATE_ACCUKNOX.docx` with `python-docx` (`Document(TEMPLATE)`), not
   from scratch. This keeps the logo header, page-number footer, embedded fonts, and
   the `Title` / `Subtitle` / `Heading1-6` / `Normal` styles intact.
2. Clear the placeholder body paragraphs (`Document Title`, `Descriptive content
   here`, `Subheading 1/2/3`) but leave the section properties (`sectPr`) alone,
   that's what links the header/footer to the document.
3. Build your content using the existing styles, don't hardcode fonts or heading
   sizes. Use the brand colors above for any table shading or status text you add.
4. If you want the header's title text to match your document, find the run
   containing `Document Title Comes here` and replace it; the logo picture sits in
   the same header paragraph, leave it untouched.
5. Save, then render a PDF to check it before calling it done:
   ```
   soffice --headless --convert-to pdf your_file.docx
   ```
   Open the PDF pages as images and look at them. Check the logo/header on every
   page, footer page numbers, table borders, and that no placeholder text survived.

## Branding a PowerPoint deck

`PPT Template.pptx` is a layout showcase, one example slide per master layout
(Intro Title, Section Title, Standard With Content, ...). Build your deck by
copying it and adding slides from those layouts (`prs.slide_layouts`,
`slides.add_slide(layout)`), not by editing a pre-built content deck.

`scripts/build.py` is a historical reference build (a past, richer proposal
deck), it's there so you can read the helper functions (`settext()`,
`add_box()`, `img_fit()`, ...) and copy the patterns. It will not run
successfully as-is against `PPT Template.pptx`, its slide/shape indices were
recorded against a different, populated deck.

1. Copy `scripts/build.py` as a starting point and update `SRC` (the master
   template, `PPT Template.pptx`) and `OUT` (where your generated `.pptx`
   should land) at the top.
2. Re-map every `sh(slide_i, shape_i)` lookup against your own slides, don't
   assume the existing indices are correct, they were written for a
   different deck. Build content using `settext()`, `add_box()`, and the
   other helpers already defined, don't add new shapes with hardcoded
   fonts/colors when an existing placeholder or helper will do.
3. Run `py -3.11 build.py` to generate the deck.
4. Render it for visual review:
   ```
   powershell -File scripts/render.ps1 -Pptx "path\to\your.pptx" -Out "path\to\render"
   ```
5. Run the writing-style checks before calling it done:
   ```
   py -3.11 scripts/final_check.py
   py -3.11 scripts/verify.py
   ```
   (update the path variable at the top of each to point at your `.pptx`)

## Writing style rules (applies to every branded doc/deck)

Branding isn't just colors and logos, it's also voice. Never use these, they're the
top AI writing tells and make output sound generated:

1. **Em dashes** (`—` or `--`), use a comma, period, or rewrite the sentence.
2. **"Delve" / "delve into"**, say "look at", "explore", "dig into".
3. **"Leverage"**, say "use".
4. **"Ensure"**, say "make sure".
5. **"Comprehensive" / "robust" / "seamless" / "streamlined"**, cut them or be specific.
6. **"It's worth noting that" / "It is important to note"**, just say the thing.
7. **"Furthermore" / "Moreover" / "Additionally"** as sentence starters, use "Also", "And", or restructure.
8. **"Game-changer" / "cutting-edge" / "state-of-the-art" / "revolutionize"**, forbidden.
9. **Trailing summary sentences** like "This will help you achieve X" after already explaining X, cut them.
10. **Bullet-listing everything** that should just be a sentence or two of prose.

Write like a sharp human. Short sentences. Real words. No padding.

## Logo usage checklist

Before placing a logo anywhere:

- [ ] Picked the light-bg or dark-bg variant to match the actual background it
      sits on, not whichever file was open.
- [ ] Used the emblem only where the full wordmark would be illegible (favicon,
      social badge, small thumbnail), never as a stand-in for the full logo on a
      title page or header.
- [ ] Left clear space around the logo, no text or other shapes crowding it.
- [ ] Didn't stretch, skew, recolor, rotate, or add effects (drop shadows,
      outlines) to the logo.
- [ ] Didn't place it on a busy photo or pattern that hurts legibility.
- [ ] Contrast holds up, blue/white wordmark is actually readable against its
      background at the size it's placed.
- [ ] Used a file from `assets/logos/`, not a screenshot, export, or copy of the
      logo pulled from some other doc or deck.

## Verification checklist

Before treating any branded output as final:

- [ ] Logo and header text render correctly on every page/slide.
- [ ] Footer page numbers present (Word).
- [ ] No placeholder text (`[ Client ]`, `Document Title`, `Subheading 1`, ...) survived.
- [ ] Colors match the palette above, no ad hoc colors introduced.
- [ ] Fonts are `Space Grotesk` throughout, no fallback fonts leaking in.
- [ ] Tables have visible borders and correctly widthed columns.
- [ ] Ran the dash/writing-style check (`scripts/verify.py` / `scripts/final_check.py` for decks; a manual read for docs).
- [ ] Rendered to PDF/PNG and actually looked at it, don't ship unseen output.
