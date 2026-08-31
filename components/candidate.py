"""Candidate solutions.

Two representations of the same thing:

``CandidateCard``  a labeled ML-architecture card, used when we want the viewer
                   to distinguish candidate solution types at a glance.
``SolutionNode(kind="candidate")``  the compact grey circle used inside the
                   search tree (Figure 1's A / B / C).
"""

from manim import *

from .candidate_diagrams import make_candidate_diagram
from .node import make_candidate
from .theme import (
    CAND_FILL,
    CAND_STROKE,
    FS_SMALL,
    FS_TINY,
    INK,
    INK_FAINT,
    INK_SOFT,
    RULE,
    SEL_ACCENT,
    SEL_FILL,
    SEL_STROKE,
    txt,
)


DIAGRAM_SCALE = 0.86


class CandidateCard(VGroup):
    """A compact labeled candidate card with an optional architecture diagram."""

    def __init__(
        self,
        label,
        width=2.05,
        height=0.80,
        code_lines=3,
        use_diagram=True,
        **kw,
    ):
        super().__init__(**kw)
        self.label_text = label
        self.panel = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            fill_color=CAND_FILL, fill_opacity=1,
            stroke_color=CAND_STROKE, stroke_width=2.6,
        )
        self.tag = txt(label, size=FS_SMALL, color=INK, weight=MEDIUM)

        self.diagram = make_candidate_diagram(label) if use_diagram else None
        if self.diagram is not None:
            label_center = self.panel.get_left() + RIGHT * width * 0.14
            diagram_left = self.panel.get_left()[0] + width * 0.30
            diagram_right = self.panel.get_right()[0] - width * 0.075
            diagram_width = diagram_right - diagram_left
            diagram_height = height * 0.60
            self.diagram.scale(
                min(
                    diagram_width / self.diagram.width,
                    diagram_height / self.diagram.height,
                    1.0,
                ) * DIAGRAM_SCALE
            )
            diagram_center = self.panel.get_center().copy()
            diagram_center[0] = (diagram_left + diagram_right) / 2
            self.diagram.move_to(diagram_center)
            self.tag.move_to(label_center)
            self.lines = VGroup()
            self.add(self.panel, self.tag, self.diagram)
            return

        lines = VGroup()
        widths = [0.86, 0.62, 0.74, 0.5][:code_lines]
        for w in widths:
            lines.add(
                RoundedRectangle(
                    width=(width - 0.9) * w, height=0.075, corner_radius=0.037,
                    fill_color=INK_FAINT, fill_opacity=1, stroke_width=0,
                )
            )
        lines.arrange(DOWN, buff=0.085, aligned_edge=LEFT)

        body = VGroup(self.tag, lines).arrange(RIGHT, buff=0.24)
        body.move_to(self.panel.get_center())
        self.add(self.panel, body)
        self.lines = lines

    def select(self):
        """Turn blue: this is the candidate the RPM preferred."""
        return AnimationGroup(
            self.panel.animate.set_fill(SEL_FILL).set_stroke(SEL_STROKE, width=3.4),
        )


def make_candidate_card(label, **kw):
    return CandidateCard(label, **kw)


def candidate_column(labels, x, y_top, y_bottom, radius=None):
    """Grey candidate circles stacked vertically — the A/B/C/D/E rail."""
    nodes = VGroup()
    n = len(labels)
    for i, lab in enumerate(labels):
        y = y_top if n == 1 else y_top + (y_bottom - y_top) * i / (n - 1)
        node = make_candidate(lab, radius=radius) if radius else make_candidate(lab)
        node.move_to(np.array([x, y, 0.0]))
        nodes.add(node)
    return nodes


def plan_code_stack(labels, width=2.5):
    """Candidate cards stacked, for 'what the RPM actually reads'."""
    return VGroup(*[CandidateCard(l, width=width) for l in labels]).arrange(
        DOWN, buff=0.28
    )
