# Embedded video

PowerPoint plays a YouTube video inside the slide when the file carries the
Online Video XML that PowerPoint itself writes. `scripts/pptx_youtube.py`
writes that XML from python-pptx, and it survives a PowerPoint re-save.

## The Recipe Has Three Parts

1. An external relationship of type `.../2006/relationships/video` whose target
   is `https://www.youtube.com/embed/<id>?feature=oembed`, plus `&start=<n>` when
   the video should open part-way in.
2. A `p:pic` that holds the poster image, an `a:hlinkClick` with
   `action="ppaction://media"`, and an `a:videoFile r:link` to that relationship.
3. A `p:timing` block with a `p:video` node that names the picture's shape id.
   One video per slide, because the timing block assumes it.

No `p14:media` extension is needed. Verified against PowerPoint 365, build
16.0.20326, which wrote the same shape when asked to insert an online video.

```python
from pptx_youtube import add_youtube, add_poster_link

add_youtube(slide, "rMc-fV5kzvs", "assets/poster.jpg",
            Inches(4.55), Inches(1.30), Inches(4.90), Inches(2.76),
            title="Protect LLM and ML with AccuKnox AI-SPM", start=35)
```

The `Deck.video` layout calls this for you. Use `add_poster_link` when you want
a static poster that opens the browser instead.

## Two Shapes Cover Every Use

`shape="hero"` puts the claim and two facts on the left and the player on the
right. It opens a deck.

`shape="demo"` gives the player the left two thirds and a chapter list the right
third. Each chapter links to that timestamp, so a seller can jump to the moment
that answers the question in the room. Chapter labels stay under 33 characters,
and a coloured dot marks the beat: set up, in action, evidence.

## Check Playback Before a Live Room

The XML is correct, but playback depends on the room. Open the deck, press F5 on
the video slide and click the player. Three known failures:

- **No internet.** The embed needs the network. The caption under every player
  links to YouTube, and a copy of the file with `embed=False` falls back to a
  poster with a link.
- **A bot check.** Users have reported a "confirm you are not a bot" message in
  PowerPoint, which the presenter cannot clear mid-talk.
- **Error 153.** A bare embed URL with no `feature=oembed` can trigger it.

For a keynote where the video matters, ask marketing for the source MP4 and
insert it as a local media file. Everything else about the slide stays the same.

## Pick the Video by What It Shows

An overview video explains the problem in under three minutes. A demo video
walks the console. A product promo with headline text over the UI works only
when the deck can talk over it, because its own captions will fight the slide.

Check `playable_in_embed` on the video before you commit to it:

```bash
yt-dlp -j "https://www.youtube.com/watch?v=<id>" | py -3.11 -c "import json,sys; d=json.load(sys.stdin); print(d['playable_in_embed'], d['duration'], d['title'])"
```

Pull the chapter times from the captions rather than guessing:

```bash
yt-dlp --write-auto-subs --sub-langs en --sub-format vtt --skip-download -o "%(id)s" "<url>"
```

The auto-captions misspell the brand as "Acunox" and "AcuNox", so never paste
caption text onto a slide without fixing it.
