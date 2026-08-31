"""Shared palette, typography and timing for the RPM animations.

Dark Meta house style: pure black ground, Optimistic type, Meta blue as the
single loud accent.  Colours are sampled from
``project_background/sample_meta_images/``.

The *semantics* still come from Figure 1 of the paper — executed / failed /
unexecuted / selected are four visually distinct node states — they are just
re-voiced for a black background.
"""

from manim import *  # noqa: F401,F403

# --------------------------------------------------------------------------
# ground + type colours
# --------------------------------------------------------------------------
BG = "#000000"

INK = "#FFFFFF"          # primary text, tree edges
INK_SOFT = "#A7B3BF"     # secondary text
INK_FAINT = "#67788A"    # tertiary text, faint arrows
RULE = "#32383E"         # hairlines, dividers

# --------------------------------------------------------------------------
# Meta accents (sampled)
# --------------------------------------------------------------------------
BLUE = "#0064E0"         # primary
BLUE_LIGHT = "#47A5FA"   # secondary
BLUE_DEEP = "#003270"
PEACH = "#FABE82"        # the sample decks' callout accent

# --------------------------------------------------------------------------
# surfaces
# --------------------------------------------------------------------------
SURFACE = "#0E1114"      # panel fill (agent box, GPU box, RPM box)
SURFACE_2 = "#171C21"    # inset fill (chip die, cards)
SURFACE_BLUE = "#08182B"  # sandbox tint
TRACK = "#22272C"        # progress-bar groove
PANEL_FILL = SURFACE
PANEL_STROKE = "#3A424A"

# --------------------------------------------------------------------------
# node states (Figure 1 semantics, dark-mode voicing)
# --------------------------------------------------------------------------
GOOD_FILL = "#0D2A20"    # executed solution, has a validation score
GOOD_STROKE = "#3ED598"

FAIL_FILL = "#2C1418"    # executed, buggy / failed
FAIL_STROKE = "#FA8282"

CAND_FILL = "#14181C"    # generated but NOT executed
CAND_STROKE = "#67788A"
CAND_TEXT = "#A7B3BF"

SEL_FILL = BLUE          # the candidate the RPM picked
SEL_STROKE = BLUE_LIGHT
SEL_ACCENT = BLUE_LIGHT  # blue flow arrows

GLOW_FILL = "#2A2214"    # "node under selection" halo
GLOW_STROKE = PEACH

COST = PEACH             # expense / GPU time callouts
COST_RED = COST          # backwards-compatible alias

# --------------------------------------------------------------------------
# typography — Optimistic is Meta's brand face (installed in /Library/Fonts).
# Light / Medium / SemiBold / Bold all resolve inside the base family.
# --------------------------------------------------------------------------
FONT = "Optimistic"

FS_HERO = 46        # closing takeaway
FS_TITLE = 34       # beat captions
FS_BODY = 26
FS_SMALL = 22
FS_TINY = 18
FS_SCORE = 27       # score inside a tree node
FS_LETTER = 23      # letter inside a candidate node

# --------------------------------------------------------------------------
# geometry
# --------------------------------------------------------------------------
NODE_R = 0.46           # executed tree node radius
CAND_R = 0.30           # unexecuted candidate radius
EDGE_W = 6.0            # tree edge stroke width
EDGE_W_FAINT = 3.0

# --------------------------------------------------------------------------
# timing
# --------------------------------------------------------------------------
T_SNAP = 0.22           # "cheap" beats: generation, ranking
T_QUICK = 0.45
T_BEAT = 0.8
T_EXEC = 2.0            # "expensive" beats: GPU execution
HOLD = 0.7


def txt(s, size=FS_BODY, color=INK, weight=NORMAL, font=FONT, **kw):
    """Project-standard text mobject, using Optimistic unless overridden."""
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def title(s, size=FS_TITLE, color=INK, **kw):
    return txt(s, size=size, color=color, weight=MEDIUM, **kw)
