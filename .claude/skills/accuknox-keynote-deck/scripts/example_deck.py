# -*- coding: utf-8 -*-
"""example_deck.py: every layout in one deck, with placeholder content.

Run it to see the system, and copy the call that matches the slide you need:

    py -3.11 example_deck.py
    powershell -File render.ps1 -Pptx ../../../../output/AccuKnox_Layout_Reference.pptx \
        -Out ../../../../output/render/layouts

The words here are deliberately generic. Real decks replace them with a claim
and a source. Where a real deck would place a product screenshot, this one draws
a grey stand-in, so the file runs with no assets.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from PIL import Image, ImageDraw  # noqa: E402

from akslides import (BODY, M, SW, T, Deck, arrow, box, chip, fill, hline,  # noqa: E402
                      panel, pin)

HERE = Path(__file__).parent
STAND_IN = HERE / "_stand_in.png"


def stand_in():
    """A grey rectangle that stands in for a product screen."""
    if STAND_IN.exists():
        return STAND_IN
    im = Image.new("RGB", (1600, 1000), "#F4F6FB")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1600, 90), fill="#FFFFFF")
    for i in range(3):
        d.rounded_rectangle((40 + i * 510, 130, 500 + i * 510, 420), 18, fill="#FFFFFF",
                            outline="#DCE3F3", width=3)
    d.rounded_rectangle((40, 460, 1560, 960), 18, fill="#FFFFFF", outline="#DCE3F3", width=3)
    for r in range(8):
        d.rounded_rectangle((80, 520 + r * 52, 700, 548 + r * 52), 10, fill="#EEF1F8")
    im.save(STAND_IN)
    return STAND_IN


def sandbox_art(s, deck):
    """A signature visual for the `cases` layout: a flow with one gated step."""
    deck.node(s, M, 1.7, 1.4, 0.62, "Trigger", "an alarm or a request")
    sx, sw = 2.35, 2.55
    sb = panel(s, sx, 1.55, sw, 1.9, alpha=5, line_alpha=None)
    from akslides import MSO_LINE_DASH_STYLE, stroke
    stroke(sb, deck.accent, 1.25, None, MSO_LINE_DASH_STYLE.DASH)
    box(s, sx + 0.16, 1.66, sw - 0.3, 0.22, "SANDBOX  ·  eBPF AND LSM", 7.5, T.WHITE, font=T.SEMI)
    deck.node(s, sx + 0.2, 1.98, sw - 0.4, 0.56, "The agent", size=11)
    for i, line in enumerate(["Allowed processes only", "No credential files"]):
        box(s, sx + 0.22, 2.68 + i * 0.3, sw - 0.4, 0.24, "✓  " + line, 9, T.WHITE)
    arrow(s, M + 1.4, 2.0, sx + 0.2, 2.26)
    for i, (name, state) in enumerate([("Tool  ·  read", "ALLOWED"), ("Tool  ·  write", "APPROVAL")]):
        y = 1.6 + i * 0.9
        gate = state != "ALLOWED"
        deck.node(s, 5.4, y, 2.3, 0.64, name, line_color=T.RED if gate else T.WHITE,
                  line_alpha=95 if gate else 40, size=10)
        chip(s, 5.56, y + 0.36, state, fg=T.WHITE, bg=T.RED if gate else T.GREEN,
             size=6.3, w=1.0 if gate else 0.74, h=0.19)
        arrow(s, sx + sw - 0.2, 2.26, 5.4, y + 0.32, alpha=45)


def build():
    d = Deck("AccuKnox_Layout_Reference", accent=T.PRIMARY)
    img = str(stand_in())

    d.cover("Every Layout in the AccuKnox Keynote System",
            "One canvas, thirteen layouts, one claim per slide.")

    d.agenda({"title": "This Reference Shows What Each Layout Is For",
              "items": [("Statement, section and agenda", "when the point is an argument"),
                        ("Stats, compare and timeline", "when the point is a number"),
                        ("Image, annotated and lanes", "when the point is a picture"),
                        ("Pipeline, matrix and cases", "when the point is a mechanism"),
                        ("Proof and video", "when the point is evidence")],
              "footnote": "Layout names match the methods on the Deck class in akslides.py."})

    d.section({"number": "01", "title": "Layouts That Carry an Argument",
               "sub": "Statement, section and agenda."})

    d.statement({"title": "A Statement Slide Lands One Claim and Backs It",
                 "lead": "Use the lead line for the sentence a reader must not miss. "
                         "Keep it under two lines.",
                 "points": ["Each supporting line states a fact, not a topic.",
                            "Three lines is the ceiling before the slide reads as a list.",
                            "The footnote carries the source, so the claim survives a challenge."],
                 "footnote": "Sources go here, named so a reader can check them."})

    d.stats({"title": "Numbers Read Better Large and Sourced",
             "items": [("30,000", "devices onboarded in one week", "case study"),
                       ("100%", "of traffic between network functions seen", "case study"),
                       ("7 days", "for an air-gapped rollout", "case study")],
             "footnote": "Give every number its unit and its source."})

    d.compare({"title": "Compare Shows the Change, Row by Row",
               "heads": ("WITHOUT THE CONTROL", "WITH THE CONTROL"),
               "rows": [("Assets discovered by hand, once a quarter",
                         "A live inventory that updates on its own"),
                        ("Findings arrive as a spreadsheet",
                         "Findings arrive in the queue the team already works"),
                        ("Evidence gathered the week before the audit",
                         "Evidence collected continuously")],
               "footnote": "Keep both columns the same length, or the slide looks biased."})

    d.timeline({"title": "A Timeline Answers How Long This Takes",
                "items": [("Day 0", "Connect", "A role, not an agent."),
                          ("Minutes", "First inventory", "Assets appear."),
                          ("Hours", "Findings", "Risk ranks itself."),
                          ("Day 7", "Rollout", "Air-gapped sites included.")],
                "footnote": "Every step needs a source or a customer that did it."})

    d.image({"title": "Image Puts One Picture in Charge",
             "image": img, "img_x": 3.45, "img_y": 1.55, "img_w": 6.0,
             "rail": [("What the picture proves", "Three facts, each one line."),
                      ("Where it came from", "The deck, page or console it is from."),
                      ("What it does not show", "The honest limit, stated.")],
             "chips": ("ROUTES INTO", ["Jira", "ServiceNow", "Slack"]),
             "footnote": "Crop the image before you place it. Never shrink to fit."})

    d.annotated({"title": "Annotated Turns a Screenshot Into an Argument",
                 "main": img,
                 "pins": [(1, "main", 300, 250), (2, "main", 900, 250), (3, "main", 1300, 700)],
                 "rail": [("Pin one names a widget", "The rail says what it proves."),
                          ("Pin two names another", "Never cover the label you point at."),
                          ("Pin three, lower right", "Four pins is the ceiling."),
                          ("The screen runs off the edge", "That is the style, on purpose.")],
                 "footnote": "Mask any customer name in the screenshot before you place it."})

    d.lanes({"title": "Lanes Answer How This Connects to My Estate",
             "hub": "Control plane", "hub_sub": "One tenant, one queue.",
             "lanes": [("Agentless cloud role", "Cloud platforms", "The managed services you run"),
                       ("Snapshot scan", "Virtual machines", "Unmanaged workloads on cloud VMs"),
                       ("Agent on the host", "On-prem servers", "Estates with no cloud API"),
                       ("Browser plugin", "SaaS apps", "What staff use in the browser")],
             "strip_label": "THE FIRST WEEK",
             "strip": [("Day 0", "Connect."), ("Minutes", "Inventory."),
                       ("Hours", "Findings."), ("Day 7", "Rollout.")],
             "footnote": "Each lane names a real integration mode, never a category."})

    d.pipeline({"title": "Pipeline Shows a Path Where Order Is the Point",
                "stages": [("01", "Normalize", "Decode the input before any check reads it."),
                           ("02", "Classify", "Fast screens run on the turn."),
                           ("03", "Contextualize", "Join the turn with session state."),
                           ("04", "Score", "Risk accumulates across the session."),
                           ("05", "Enforce", "Allow, sanitize or block, then log.")],
                "band": ("The engine underneath",
                         "A band holds the component that feeds several stages, so the row above "
                         "stays readable.", "< 50 ms", "p95 per request"),
                "footnote": "Five stages is the ceiling before the row turns into a wall."})

    d.matrix({"title": "A Matrix Answers Whether You Cover My Stack",
              "cols": [("SURFACE", 2.1), ("WHAT RUNS THERE", 4.2), ("HOW IT CONNECTS", 3.1)],
              "rows": [["First surface", "The products a buyer already runs there",
                        "The integration mode"],
                       ["Second surface", "Named platforms, never a category", "Another mode"],
                       ["Third surface", "Keep each cell under twelve words", "Another mode"],
                       ["Fourth surface", "Four rows fit, five is tight", "Another mode"]],
              "chips": [("ACTIONS", ["Block", "Sanitize", "Monitor"]),
                        ("DEPLOY", ["SaaS", "On-prem", "Air-gapped"])],
              "footnote": "Cite the page each row came from."})

    d.cases({"title": "Cases Pair a Signature Visual With Three Uses",
             "art": sandbox_art,
             "items": [("First use case", "One sentence on what the buyer gets.", "THEIR TEAM"),
                       ("Second use case", "Name the system it attaches to.", "THEIR SYSTEM"),
                       ("Third use case", "Keep all three the same shape.", "THEIR SITE")],
             "footnote": "The tag names the buyer's own team, which is what makes it sell."})

    d.proof({"title": "Proof Leads With One Number and Names Its Layer",
             "big": "85%", "big_label": "lower data leakage risk at a named customer",
             "big_source": "customer case study", "big_url": "https://accuknox.com/case-studies",
             "quote": "A short customer quote earns more than a paragraph of claims.",
             "quote_by": "Title, company",
             "right": [{"kind": "stat", "value": "40+", "label": "agents brought under one view",
                        "source": "same case study"},
                       {"kind": "flow", "nodes": ["Gateway", "The control", "Model"],
                        "label": "A small flow shows how the control sits in the path.",
                        "source": "same case study"}],
             "credentials": "Customer  ·  Programme  ·  Partner  ·  Lab  ·  Standards body",
             "footnote": "Say which layer each number proves, so nobody over-claims."})

    d.close()
    return d.save()


if __name__ == "__main__":
    build()
