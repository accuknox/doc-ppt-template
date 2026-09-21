# Layouts

Thirteen layouts, each a method on `Deck` in `scripts/akslides.py`. Pick by the
kind of point the slide makes, not by how much text you have.

| The point is | Layout | Method |
|---|---|---|
| An argument | Statement, section, agenda | `statement` `section` `agenda` |
| A number | Stats, compare, timeline | `stats` `compare` `timeline` |
| A picture | Image, annotated, lanes | `image` `annotated` `lanes` |
| A mechanism | Pipeline, matrix, cases | `pipeline` `matrix` `cases` |
| Evidence | Proof, video | `proof` `video` |

Run `py -3.11 scripts/example_deck.py` to see all of them with placeholder copy,
then render that file and keep the PNGs open while you build.

## Cover and Close Come From the Template

```python
d = Deck("AccuKnox_Acme_Overview", accent=T.PRIMARY)
d.cover("AI Security Posture\nManagement for Telecom",
        "Find every model, agent and MCP server across the estate.")
d.close()                       # SEE US IN ACTION, support@accuknox.com
```

Layout 0 carries the lockup, the tagline and the badge rows. Layout 1 carries
the closing lockup and the certification badges. Never rebuild either, never
open or close on the dark dotted divider (layout 2), and keep the cover to a
title plus one line, or a short `scope=[("30", "subscriptions"), ...]` row.

## Statement, Section and Agenda Carry an Argument

```python
d.statement({"title": "A Per-Prompt Filter Misses the Attack That Builds",
             "lead": "One sentence a reader must not miss.",
             "points": ["A fact, not a topic.", "A second fact.", "A third."],
             "footnote": "Source, named."})

d.section({"number": "02", "title": "Where It Sits in Your Estate",
           "sub": "Four discovery modes."})

d.agenda({"title": "This Deck Answers Four Buyer Questions",
          "items": [("What it is", "and what it is not"),
                    ("How it connects", "four modes")]})
```

Keep `points` to three. A fourth turns the slide into a list, and a list argues
nothing.

## Stats, Compare and Timeline Carry a Number

```python
d.stats({"title": "Three Numbers Decide the Pilot",
         "items": [("30,000", "devices onboarded in one week", "IDT case study", URL),
                   ("100%", "of traffic between 5G functions seen", "DoD case study", URL),
                   ("7 days", "for an air-gapped rollout", "bank case study", URL)]})

d.compare({"title": "The Control Changes Three Things",
           "heads": ("WITHOUT", "WITH ACCUKNOX"),
           "rows": [("Assets found by hand", "A live inventory")]})

d.timeline({"title": "The First Week Has Four Milestones",
            "items": [("Day 0", "Connect", "A role, not an agent.")]})
```

Three stats read better than four. Each one takes its unit in the label and its
source underneath, because a number with no source is decoration.

## Image, Annotated and Lanes Carry a Picture

`image` puts one picture in charge, with a rail of facts beside it. Use it for a
logo wall, a deployment card, a report page or an architecture picture you did
not redraw.

```python
d.image({"title": "AccuKnox Scans the Platforms You Already Run",
         "image": "assets/platforms.png", "img_x": 3.45, "img_y": 1.55, "img_w": 6.0,
         "rail": [("Managed and on-prem", "Both sides land in one inventory.")],
         "chips": ("INCIDENTS ROUTE INTO", ["Jira", "ServiceNow", "Slack"]),
         "footnote": "Grid from the AccuKnox AI security deck, June 2026."})
```

`annotated` is the one that makes a deck feel like the product. A real console
screen runs off the right and bottom edges, numbered pins sit on real widgets,
and the rail says what each pin proves.

```python
d.annotated({"title": "One Dashboard Lists Every AI Asset\nand Ranks Its Risk",
             "main": "assets/dashboard.png",
             "insets": [{"img": "assets/shadow.png", "x": 6.62, "y": 2.92, "w": 3.1}],
             "pins": [(1, "main", 185, 232), (4, 0, 600, 357)],
             "rail": [("Every AI asset, counted", "Apps, models, datasets, compute.")]})
```

Pin coordinates are pixels in the source image, and the layout maps them to
inches. Read them off the image once, then never touch them again. A pin goes
beside the widget it names, never on top of the label, and four pins is the
ceiling.

`lanes` answers "how does this connect to what I run": a hub on the left, one
labelled lane per integration mode, an optional timeline strip underneath.

```python
d.lanes({"title": "Four Discovery Modes Reach Cloud, VM,\nOn-Prem and SaaS AI",
         "hub": "AccuKnox control plane", "hub_sub": "One tenant, one queue.",
         "lanes": [("Agentless cloud SDK", "Cloud AI platforms", "Bedrock, AI Foundry, Vertex")],
         "strip_label": "THE FIRST WEEK",
         "strip": [("Day 0", "Connect a cloud role.")]})
```

## Pipeline, Matrix and Cases Carry a Mechanism

```python
d.pipeline({"title": "Five Stages Run on Every Prompt and Every Reply",
            "stages": [("01", "Normalize", "Decode unicode tricks first.")],
            "band": ("Session context engine", "What feeds stages three to five.",
                     "< 50 ms", "p95 per request")})

d.matrix({"title": "Every AI Surface Has a Way In",
          "cols": [("SURFACE", 2.1), ("WHAT RUNS THERE", 4.2), ("HOW IT CONNECTS", 3.1)],
          "rows": [["SaaS AI apps", "Claude.ai, ChatGPT, Copilot", "Browser plugin"]],
          "chips": [("ACTIONS", ["Block", "Sanitize", "Monitor"])]})

d.cases({"title": "Care Bots, NOC Assistants and RAG Tools\nEach Need Their Own Policy",
         "art": my_signature_visual,      # a callable (slide, deck) that draws the top half
         "items": [("Subscriber care bots", "Mask numbers and IDs in replies.", "ISOC")]})
```

Five stages is the pipeline ceiling. Four rows is the matrix ceiling before the
type drops under 9 pt. The `art` callable on `cases` is where a deck earns its
keep: draw the one diagram only this product could show, using `node`, `arrow`,
`chip` and `panel` from the runtime.

## Proof and Video Carry Evidence

```python
d.proof({"title": "IDT Put Kernel Enforcement on\n30,000 Devices in One Week",
         "big": "30,000", "big_label": "devices onboarded at IDT within a week",
         "big_source": "IDT case study", "big_url": URL,
         "quote": "Choosing AccuKnox was driven by KubeArmor's use of eBPF and LSM.",
         "quote_by": "Golan Ben-Oni, CIO, IDT",
         "right": [{"kind": "stat", "value": "100%", "label": "...", "source": "..."},
                   {"kind": "flow", "nodes": ["Gateway", "Firewall", "LLM"], "label": "..."}],
         "credentials": "IDT  ·  US DoD 5G  ·  Tata Elxsi  ·  LF Nephio"})

d.video({"shape": "hero", "title": "...", "definition": "...",
         "facts": [("Agentless", "Connects through a cloud role.")],
         "video": "rMc-fV5kzvs", "start": 35, "poster": "assets/poster.jpg",
         "video_title": "Protect LLM and ML with AccuKnox AI-SPM", "duration": "2:34",
         "video_note": "Starts at 0:35, where the console screens begin."})

d.video({"shape": "demo", "title": "Watch a Policy Block a Prompt",
         "video": "l_RCQosnNJk", "poster": "assets/demo.jpg",
         "video_title": "Prompt Firewall Setup and Demo", "duration": "7:51",
         "chapters": [("0:48", "In action", "A block, a monitor, a code ban"),
                      ("3:41", "Set up", "Add an app, copy its token")]})
```

On a proof slide, say which layer each number proves. Runtime numbers are not AI
numbers, and a technical buyer catches the gap first. Chapter labels stay under
33 characters so each one holds a single line.

See `references/video.md` for the embed mechanics and the fallback.
