# doc-ppt-template

Master AccuKnox brand templates for Word documents and PowerPoint decks, plus the
build scripts used to turn any draft into an AccuKnox-branded final file. This repo
is the single source of truth for "how do I brand this doc/deck like AccuKnox."

## What's in here

| File / folder | What it is |
|---|---|
| `WORD_TEMPLATE_ACCUKNOX.docx` | Master Word template. Logo + title in the header, page numbers in the footer, brand fonts embedded, and `Title` / `Subtitle` / `Heading1-6` / `Normal` styles pre-configured. |
| `PPT Template.pptx` | Master PowerPoint template (the full brand deck: title slide, section breaks, comparison tables, stat panels, etc.). Copy this as the base for every new deck. |
| `AccuKnox_Proposal_Template_BLANK.pptx` | A de-branded copy of the master deck with placeholder text (`[ Client ]`, `[ Title ]`, ...) instead of real content. Use this as your starting point when writing a new `build.py`, so you're not editing the master file directly. |
| `build.py` | Worked example: a full python-pptx build script that turns the blank template into a real customer proposal deck. Read this before writing a new one, it shows every helper function you'll need. |
| `render.ps1` | Exports every slide of a `.pptx` to PNG via PowerPoint COM automation, for visual review. |
| `final_check.py`, `verify.py` | Scan a built `.pptx` for em/en dashes and other banned writing-style tells (see below). |
| `customer-comparisons/` | Worked example of a Word doc branded from `WORD_TEMPLATE_ACCUKNOX.docx` (an AccuKnox vs. SonarQube Cloud comparison), plus the `build.py` that generated it. |

## Brand basics

**Fonts**
- Headings and UI-style text: `Space Grotesk` (Regular, Bold, SemiBold). Embedded directly in `WORD_TEMPLATE_ACCUKNOX.docx`, no install needed when you edit that file in Word.
- Body copy in decks: `Space Grotesk` throughout, per `build.py`.

**Colors**

| Name | Hex | Use |
|---|---|---|
| Navy | `#11206D` | Primary brand color, dark UI panels, table headers |
| Navy (heading) | `#003BF6` / `#0000FF` | Word template heading colors (`Heading1-4`) |
| Purple | `#4D4DD9` | Secondary accent |
| Green | `#16A55C` (light `#0B7A42`, tint `#E7F6EE`) | "Live" / "Yes" / advantage state |
| Red | `#C80019` | Alerts, "not covered" state |
| Grey (placeholder) | `#EEF0F6` fill / `#C4CCDE` border | Screenshot placeholders, table borders |

Don't invent new brand colors. If a design need doesn't fit this palette, ask before
picking your own.

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

See `customer-comparisons/build.py` for a full worked example of this pattern.

## Branding a PowerPoint deck

1. Copy `AccuKnox_Proposal_Template_BLANK.pptx` and rename it for your project.
2. Copy `build.py` and update the three path variables at the top:
   - `SRC` — the master brand template, `PPT Template.pptx`. Leave as-is.
   - `OUT` — where your generated `.pptx` should land.
   - `BLANK` — your renamed copy of the blank template.
3. Edit slide content using `settext()`, `add_box()`, and the other helpers already
   defined in `build.py`, don't add new shapes with hardcoded fonts/colors when an
   existing placeholder or helper will do.
4. Run `py -3.11 build.py` to generate the deck.
5. Render it for visual review:
   ```
   powershell -File render.ps1 -Pptx "path\to\your.pptx" -Out "path\to\render"
   ```
6. Run the writing-style checks before calling it done:
   ```
   py -3.11 final_check.py
   py -3.11 verify.py
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

## Verification checklist

Before treating any branded output as final:

- [ ] Logo and header text render correctly on every page/slide.
- [ ] Footer page numbers present (Word).
- [ ] No placeholder text (`[ Client ]`, `Document Title`, `Subheading 1`, ...) survived.
- [ ] Colors match the palette above, no ad hoc colors introduced.
- [ ] Fonts are `Space Grotesk` throughout, no fallback fonts leaking in.
- [ ] Tables have visible borders and correctly widthed columns.
- [ ] Ran the dash/writing-style check (`verify.py` / `final_check.py` for decks; a manual read for docs).
- [ ] Rendered to PDF/PNG and actually looked at it, don't ship unseen output.
