"""Captions, step badges and the Figure 1 stage strip."""

from manim import *

from .theme import (
    FS_BODY,
    FS_HERO,
    FS_SMALL,
    FS_TINY,
    FS_TITLE,
    GLOW_FILL,
    GLOW_STROKE,
    INK,
    INK_FAINT,
    INK_SOFT,
    RULE,
    SEL_ACCENT,
    SURFACE,
    txt,
)

TOP_Y = 3.28
BOTTOM_Y = -3.35


def caption(text, y=BOTTOM_Y, size=FS_TITLE, color=INK):
    """One line of narration.  Used sparingly — motion carries the meaning."""
    return txt(text, size=size, color=color, weight=MEDIUM).move_to(
        np.array([0.0, y, 0.0])
    )


def two_tone(parts, y=BOTTOM_Y, size=FS_TITLE, buff=0.16):
    """caption built from (text, colour, weight?) tuples, arranged in a row."""
    grp = VGroup()
    for p in parts:
        s, c = p[0], p[1]
        w = p[2] if len(p) > 2 else MEDIUM
        grp.add(txt(s, size=size, color=c, weight=w))
    grp.arrange(RIGHT, buff=buff).move_to(np.array([0.0, y, 0.0]))
    return grp


def annotation(text, target, direction=UP, buff=0.36, size=FS_TINY, color=INK_SOFT):
    """A small label with a leader line pointing at ``target``."""
    label = txt(text, size=size, color=color)
    label.next_to(target, direction, buff=buff)
    leader = Line(
        label.get_edge_center(-direction) + (-direction) * 0.05,
        target.get_edge_center(direction) + direction * 0.05,
        stroke_width=1.8,
        color=INK_FAINT,
    )
    return VGroup(leader, label)


class StepBadge(VGroup):
    """Numbered step in the search loop, e.g. '3  Execute'."""

    def __init__(self, n, text, width=2.9, **kw):
        super().__init__(**kw)
        self.disc = Circle(
            radius=0.19, stroke_color=INK_FAINT, stroke_width=2,
            fill_color=SURFACE, fill_opacity=1,
        )
        self.num = txt(str(n), size=FS_TINY, color=INK_SOFT)
        self.num.move_to(self.disc)
        self.text = txt(text, size=FS_SMALL, color=INK_SOFT)
        VGroup(VGroup(self.disc, self.num), self.text).arrange(RIGHT, buff=0.20)
        self.add(self.disc, self.num, self.text)

    def light(self):
        return AnimationGroup(
            self.disc.animate.set_stroke(SEL_ACCENT, width=3),
            self.num.animate.set_color(SEL_ACCENT),
            self.text.animate.set_color(INK),
        )

    def unlight(self):
        return AnimationGroup(
            self.disc.animate.set_stroke(INK_FAINT, width=2),
            self.num.animate.set_color(INK_SOFT),
            self.text.animate.set_color(INK_SOFT),
        )


def step_column(steps, x=-5.1, y=0.6, buff=0.44):
    badges = VGroup(*[StepBadge(i + 1, s) for i, s in enumerate(steps)])
    badges.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    badges.move_to(np.array([x, y, 0.0]))
    return badges


FIGURE1_STAGES = [
    "Select Node\nto Mutate",
    "Generate Candidate\nMutations",
    "Select Child\nUsing RPM",
    "Evaluate Selection\nand Update Tree",
]


def stage_strip(y=2.55, size=21, xs=(-5.25, -1.75, 1.75, 5.25)):
    """The four Figure 1 panel headings in a row, with arrows between them."""
    labels = VGroup()
    for s, x in zip(FIGURE1_STAGES, xs):
        t = txt(s, size=size, color=INK, weight=MEDIUM,
                line_spacing=0.8).move_to(np.array([x, y, 0.0]))
        labels.add(t)
    arrows = VGroup()
    for a, b in zip(labels[:-1], labels[1:]):
        arrows.add(
            Arrow(
                a.get_right() + RIGHT * 0.18,
                b.get_left() + LEFT * 0.18,
                buff=0,
                color=INK,
                stroke_width=4,
                tip_length=0.18,
                max_tip_length_to_length_ratio=0.35,
                max_stroke_width_to_length_ratio=999,
            )
        )
    return labels, arrows


def repeat_arc(labels, y=3.55, label_y=3.05):
    """The 'Repeat' arc that loops the last stage back to the first."""
    start = labels[-1].get_top() + UP * 0.12
    end = labels[0].get_top() + UP * 0.12
    tip_len = 0.22
    curve = VMobject(stroke_color=INK, stroke_width=4, fill_opacity=0)
    curve.set_points_smoothly(
        [
            start,
            np.array([start[0] - 1.1, y - 0.10, 0.0]),
            np.array([0.0, y, 0.0]),
            np.array([end[0] + 1.1, y - 0.10, 0.0]),
            end + RIGHT * tip_len * 0.7,
        ]
    )
    tip = ArrowTriangleFilledTip(color=INK, length=tip_len, width=0.19,
                                 start_angle=angle_of_vector(DOWN + LEFT * 0.9))
    tip.shift(end - tip.tip_point)
    arc = VGroup(curve, tip)
    word = txt("Repeat", size=FS_SMALL, color=INK, weight=MEDIUM).move_to(
        np.array([0.0, label_y, 0.0])
    )
    return arc, word


def highlight_plate(mobject, pad=0.22, corner=0.14):
    return RoundedRectangle(
        width=mobject.width + 2 * pad,
        height=mobject.height + 2 * pad,
        corner_radius=corner,
        fill_color=GLOW_FILL,
        fill_opacity=1,
        stroke_color=GLOW_STROKE,
        stroke_width=2,
    ).move_to(mobject)


def hero(text, size=FS_HERO, color=INK, **kw):
    return txt(text, size=size, color=color, weight=MEDIUM, **kw).move_to(ORIGIN)


def pill(text, size=FS_BODY, fill=SURFACE, stroke=INK_FAINT, text_color=INK,
         pad=0.34):
    """A labelled rounded box, for the small flow charts in the closing frame."""
    label = txt(text, size=size, color=text_color, weight=MEDIUM)
    box = RoundedRectangle(
        width=label.width + 2 * pad,
        height=label.height + 2 * pad * 0.62,
        corner_radius=0.12,
        fill_color=fill,
        fill_opacity=1,
        stroke_color=stroke,
        stroke_width=2.6,
    )
    label.move_to(box)
    return VGroup(box, label)


def down_chain(texts, buff=0.44, **pill_kw):
    """Vertical [a] -> [b] -> [c] flow."""
    pills = VGroup(*[pill(t, **pill_kw) for t in texts]).arrange(DOWN, buff=buff)
    arrows = VGroup()
    for a, b in zip(pills[:-1], pills[1:]):
        arrows.add(
            Arrow(
                a.get_bottom() + DOWN * 0.04,
                b.get_top() + UP * 0.04,
                buff=0,
                color=INK,
                stroke_width=3.4,
                tip_length=0.16,
                max_tip_length_to_length_ratio=0.45,
                max_stroke_width_to_length_ratio=999,
            )
        )
    return VGroup(pills, arrows)
