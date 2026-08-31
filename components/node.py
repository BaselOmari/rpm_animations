"""Solution nodes.

A node is one solution in the agent's search tree (paper §2.2).  Four states,
matching Figure 1:

    good       executed, has a validation score      green
    failed     executed, buggy / no usable score     red
    candidate  generated but NOT yet executed        grey, near-black fill
    selected   the candidate the RPM picked          Meta blue
"""

from manim import *

from .theme import (
    txt,
    CAND_FILL,
    CAND_R,
    CAND_STROKE,
    CAND_TEXT,
    FAIL_FILL,
    FAIL_STROKE,

    FS_LETTER,
    FS_SCORE,
    GLOW_FILL,
    GLOW_STROKE,
    GOOD_FILL,
    GOOD_STROKE,
    INK,
    NODE_R,
    SEL_FILL,
    SEL_STROKE,
)

STYLES = {
    "good": dict(fill=GOOD_FILL, stroke=GOOD_STROKE, text=INK, width=5.0),
    "failed": dict(fill=FAIL_FILL, stroke=FAIL_STROKE, text=INK, width=5.0),
    "candidate": dict(fill=CAND_FILL, stroke=CAND_STROKE, text=CAND_TEXT, width=3.6),
    "selected": dict(fill=SEL_FILL, stroke=SEL_STROKE, text=INK, width=4.2),
}


class SolutionNode(VGroup):
    """A single circular node.  ``label`` is a score ("0.60") or letter ("C")."""

    def __init__(self, label="", kind="good", radius=None, font_size=None, **kw):
        super().__init__(**kw)
        if radius is None:
            radius = NODE_R if kind in ("good", "failed") else CAND_R
        if font_size is None:
            font_size = FS_SCORE if kind in ("good", "failed") else FS_LETTER

        st = STYLES[kind]
        self.kind = kind
        self.label_text = label
        self.base_radius = radius

        self.circle = Circle(
            radius=radius,
            fill_color=st["fill"],
            fill_opacity=1.0,
            stroke_color=st["stroke"],
            stroke_width=st["width"],
        )
        if label:
            self.label = txt(label, size=font_size, color=st["text"])
        else:
            # Failed nodes carry no score.  Keep a degenerate placeholder so the
            # submobject count stays stable and Transform() can morph cleanly.
            self.label = Dot(radius=0.001, fill_opacity=0, stroke_opacity=0)
        self.label.move_to(self.circle.get_center())
        self.add(self.circle, self.label)

    # -- geometry -----------------------------------------------------------
    @property
    def radius(self):
        """Current on-screen radius (survives group scaling)."""
        return self.circle.width / 2

    # -- restyling ----------------------------------------------------------
    def ghost(self, kind=None, label=None, radius=None):
        """A copy of this node in a new state, parked at the same centre."""
        kind = self.kind if kind is None else kind
        label = self.label_text if label is None else label
        radius = self.radius if radius is None else radius
        scale = radius / (NODE_R if kind in ("good", "failed") else CAND_R)
        fs = (FS_SCORE if kind in ("good", "failed") else FS_LETTER) * scale
        g = SolutionNode(label, kind, radius=radius, font_size=fs)
        g.move_to(self.get_center())
        return g

    def morph(self, kind=None, label=None, radius=None, **anim_kw):
        """Animation that turns this node into another state, in place."""
        g = self.ghost(kind, label, radius)
        self.kind = g.kind
        self.label_text = g.label_text
        return Transform(self, g, **anim_kw)

    def dim(self, opacity=0.22):
        return self.animate.set_opacity(opacity)


# ---------------------------------------------------------------------------
# factory helpers (the names the brief asked for)
# ---------------------------------------------------------------------------
def make_tree_node(score, status="good", **kw):
    return SolutionNode(f"{score}" if score != "" else "", status, **kw)


def make_failed_node(**kw):
    return SolutionNode("", "failed", **kw)


def make_candidate(label, **kw):
    return SolutionNode(label, "candidate", **kw)


def make_selected(label, **kw):
    """The blue 'RPM picked this one' node."""
    return SolutionNode(label, "selected", **kw)


def glow_halo(node, pad=0.26):
    """The warm 'currently selected parent' plate from Figure 1."""
    side = 2 * node.radius + 2 * pad
    return RoundedRectangle(
        width=side,
        height=side,
        corner_radius=0.16,
        fill_color=GLOW_FILL,
        fill_opacity=1.0,
        stroke_color=GLOW_STROKE,
        stroke_width=2,
    ).move_to(node.get_center())
