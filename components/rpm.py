"""The Research Preference Model itself.

Figure 1 draws the RPM as a plain white box in the flow.  We keep that, and add
the internals the paper describes: pairwise comparisons in a tournament knockout
structure (§3.3), rather than absolute score prediction (§3).
"""

from manim import *

from .theme import (
    FAIL_STROKE,
    FS_BODY,
    FS_SMALL,
    FS_TINY,
    INK,
    INK_FAINT,
    INK_SOFT,
    PANEL_STROKE,
    SEL_ACCENT,
    SEL_FILL,
    SEL_STROKE,
    SURFACE,
    txt,
)


class RPMBox(VGroup):
    """The ``RPM`` box from Figure 1, optionally subtitled."""

    def __init__(self, label="RPM", subtitle=None, width=2.4, height=1.45,
                 label_size=FS_BODY, **kw):
        super().__init__(**kw)
        self.panel = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            fill_color=SURFACE, fill_opacity=1,
            stroke_color=PANEL_STROKE, stroke_width=3.2,
        )
        self.label = txt(label, size=label_size, color=INK, weight=MEDIUM)
        parts = [self.label]
        if subtitle:
            self.subtitle = txt(subtitle, size=FS_TINY, color=INK_SOFT)
            parts.append(self.subtitle)
        body = VGroup(*parts).arrange(DOWN, buff=0.10).move_to(self.panel.get_center())
        self.add(self.panel, body)

    def pulse(self, run_time=0.5, amount=1.05):
        # NB: animate ``self``, not ``self.panel``.  Manim hoists any animated
        # submobject to the top of the scene's draw order, which would leave the
        # panel painted over its own label for the rest of the video.
        return Succession(
            self.animate(run_time=run_time / 2).scale(amount),
            self.animate(run_time=run_time / 2).scale(1 / amount),
        )

    def thinking(self, n=3):
        """Three dots under the label, for 'it is reasoning'."""
        dots = VGroup(
            *[Dot(radius=0.055, color=SEL_ACCENT) for _ in range(n)]
        ).arrange(RIGHT, buff=0.13)
        dots.next_to(self.panel, DOWN, buff=0.16)
        return dots


def make_rpm_box(**kw):
    return RPMBox(**kw)


def flow_arrow(a, b, color=INK, stroke=4.0, tip=0.22, gap=0.13):
    """Straight arrow from the rim of ``a`` to the rim of ``b``."""
    d = normalize(b.get_center() - a.get_center())
    return Arrow(
        a.get_boundary_point(d) + d * gap,
        b.get_boundary_point(-d) - d * gap,
        buff=0,
        color=color,
        stroke_width=stroke,
        tip_length=tip,
        max_tip_length_to_length_ratio=0.35,
        max_stroke_width_to_length_ratio=999,
    )


def curved_arrow(start, end, bow=0.85, color=INK_SOFT, stroke=3.0,
                 tip_length=0.17, tip_width=0.15):
    """Left-to-right S-curve with an arrowhead.

    ``CubicBezier`` is not tipable in Manim CE, so the head is placed by hand.
    """
    p1 = start + RIGHT * bow
    p2 = end + LEFT * bow
    d = normalize(end - p2)
    curve = CubicBezier(
        start, p1, p2, end - d * tip_length * 0.8,
        stroke_color=color, stroke_width=stroke, fill_opacity=0,
    )
    tip = ArrowTriangleFilledTip(
        color=color, length=tip_length, width=tip_width,
        start_angle=angle_of_vector(d),
    )
    tip.shift(end - tip.tip_point)
    return VGroup(curve, tip)


def fan_arrows(source, targets, color=INK_FAINT, stroke=2.6, spread=0.55, bow=0.8):
    """One source -> many targets.  The agent spraying out candidates."""
    arrows = VGroup()
    n = len(targets)
    right = source.get_right()
    for i, t in enumerate(targets):
        frac = 0.0 if n == 1 else (i / (n - 1) - 0.5)
        start = right + RIGHT * 0.10 + UP * frac * source.height * spread
        end = t.get_left() + LEFT * 0.10
        arrows.add(curved_arrow(start, end, bow=bow, color=color, stroke=stroke,
                                tip_length=0.15, tip_width=0.13))
    return arrows


def funnel_arrows(sources, target, color=INK_SOFT, stroke=3.0, spread=0.74, bow=0.8):
    """The A/B/C/D/E -> [RPM] funnel: curves converging on the box's left edge."""
    arrows = VGroup()
    n = len(sources)
    left = target.get_left()
    for i, s in enumerate(sources):
        frac = 0.0 if n == 1 else (i / (n - 1) - 0.5)
        end = left + LEFT * 0.10 + UP * frac * target.height * spread
        start = s.get_right() + RIGHT * 0.08
        arrows.add(curved_arrow(start, end, bow=bow, color=color, stroke=stroke))
    return arrows


class MatchUp(VGroup):
    """One pairwise comparison: ``A vs B  ->  B``."""

    def __init__(self, left, right, winner, size=FS_SMALL, **kw):
        super().__init__(**kw)
        self.left = txt(left, size=size, color=INK, weight=MEDIUM)
        self.vs = txt("vs", size=size - 4, color=INK_SOFT)
        self.right = txt(right, size=size, color=INK, weight=MEDIUM)
        self.arrow = txt("→", size=size, color=INK_SOFT)
        self.winner = txt(winner, size=size, color=SEL_ACCENT, weight=BOLD)
        VGroup(self.left, self.vs, self.right, self.arrow, self.winner).arrange(
            RIGHT, buff=0.20
        )
        self.add(self.left, self.vs, self.right, self.arrow, self.winner)


def tournament_ladder(matches, buff=0.34):
    """Stack of MatchUp rows, e.g. [("A","B","B"), ("B","C","C"), ...]."""
    return VGroup(*[MatchUp(*m) for m in matches]).arrange(
        DOWN, buff=buff, aligned_edge=LEFT
    )


def crossed_out(mobject, color=FAIL_STROKE, stroke=5):
    """A single strike through a mobject — 'not what the RPM does'."""
    return Line(
        mobject.get_left() + LEFT * 0.12,
        mobject.get_right() + RIGHT * 0.12,
        stroke_width=stroke,
        color=color,
    )
