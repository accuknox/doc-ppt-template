# Gotchas

Every line here cost time once. None of them is obvious from an error message.

## Python and PowerShell

- **Use `py -3.11`.** python-pptx, lxml and Pillow live there. The default
  `python` is 3.10 and lacks them. Playwright is the opposite case: it is
  installed on `python` 3.10, not on 3.11.
- **Never name a script `inspect.py`.** It shadows the standard library module
  and breaks the lxml import with a confusing traceback.
- **Do not put a raw newline inside a run.** `run.text = "a\nb"` writes the
  newline into `<a:t>`. The PNG export hides it and the PDF draws a tofu box.
  The runtime's `runs()` emits a real `<a:br/>`, so route everything through it.
- **A PowerShell path in bash needs forward slashes.** `"...\\$n"` escapes the
  dollar sign, so a loop writes every render into one folder called `tcts$n`.
  Write `"D:/Atharva/.../$n"` instead.
- **A heredoc with tricky quoting fails oddly.** For anything beyond a few
  lines, write the script to the scratchpad with the Write tool and run the
  file. Long inline heredocs have failed here with unterminated-string errors.

## PowerPoint COM

- **One render at a time.** `render.ps1` calls `Quit()` at the end, which kills
  any other PowerPoint automation session in flight. Never run two renders, or a
  render and a finalize, at once.
- **Font embedding happens on re-save.** `finalize.ps1` opens each file and calls
  `SaveAs(path, 24, -1)`, where `-1` is `msoTrue` for `EmbedTrueTypeFonts`.
  After it runs, `ppt/fonts/` holds seven font files.
- **The embed survives.** A PowerPoint re-save keeps the Online Video XML
  written by python-pptx, checked on every TCTS deck.
- **Export a PDF every time.** `SaveAs(path, 32)` writes it, and the PDF is
  where a newline bug or a font fallback shows up.

## Images and Video

- **The first `ffmpeg` on PATH is ImageMagick's 4.2.3.** Call
  `C:\ProgramData\chocolatey\bin\ffmpeg.exe` by its full path, and the same for
  `ffprobe.exe`.
- **`yt-dlp` flat mode returns no upload date.** Fetch full metadata with
  `-j` for the handful of videos you actually care about.
- **Auto-captions misspell the brand.** They render "Acunox", "AcuNox" and
  "Acox". Fix any caption text before it reaches a slide.
- **`--sub-langs "en.*"` can write nothing while exiting 0.** Use `en`.

## The Browser Pane

- **Screenshots time out.** The pane's screenshot call fails with a render
  timeout on this machine. Use a Playwright script on `python` 3.10 for the one
  visual check, or read geometry with `javascript_tool`.

## Source Material

- **The macro deck cover carries an NDA mark.** Take facts from it, redraw the
  pictures, and put no slide image from it into a partner deck.
- **Case study pages carry a template stat block.** "37+ integrations, 89% fewer
  false positives, 91% reduced remediation" appears on every page and belongs to
  no customer. Never attribute it to the named one.
- **accuknox.com serves a markdown twin.** Append `.md` to a path for clean
  text. Not every page has one, and a 404 on `.md` does not mean the page is
  missing.
- **Public numbers conflict.** Framework counts, probe counts and policy counts
  differ between the site, the decks and the docs. Pick the figure on the live
  product page, cite it, and keep the same figure across the deck.
