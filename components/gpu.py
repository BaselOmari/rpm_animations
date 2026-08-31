"""Execution hardware: the expensive half of the loop.

``GPUBox``     full-scale execution + evaluation (hours of H200 time, §2.1).
``SandboxBox`` the Agentic RPM's sandbox clone, where cheap pilot runs happen
               (§3.2).  Deliberately smaller and faster than the GPU box.
"""

from manim import *

from .theme import (
    COST,
    FS_SMALL,
    FS_TINY,
    INK,
    INK_SOFT,
    PANEL_FILL,
    PANEL_STROKE,
    RULE,
    SEL_ACCENT,
    SURFACE,
    SURFACE_2,
    SURFACE_BLUE,
    TRACK,
    txt,
)


class ProgressBar(VGroup):
    """A left-anchored fill bar.  Slow fills read as 'this costs something'."""

    def __init__(self, width=2.2, height=0.22, color=COST, **kw):
        super().__init__(**kw)
        self.track = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.05,
            fill_color=TRACK,
            fill_opacity=1,
            stroke_color=RULE,
            stroke_width=1.5,
        )
        self.bar = RoundedRectangle(
            width=height,
            height=height,
            corner_radius=0.05,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        )
        self.bar.move_to(self.track.get_left(), LEFT)
        self.add(self.track, self.bar)

    def fill_to(self, frac=1.0, **anim_kw):
        w = max(self.track.height, self.track.width * frac)
        tgt = self.bar.copy().stretch_to_fit_width(w)
        tgt.move_to(self.track.get_left(), LEFT)
        anim_kw.setdefault("rate_func", linear)
        return Transform(self.bar, tgt, **anim_kw)

    def reset(self):
        self.bar.stretch_to_fit_width(self.track.height)
        self.bar.move_to(self.track.get_left(), LEFT)
        return self


class Clock(VGroup):
    """Tiny analogue clock; spinning it sells 'wall-clock time went by'."""

    def __init__(self, radius=0.30, color=INK_SOFT, **kw):
        super().__init__(**kw)
        self.face = Circle(
            radius=radius, stroke_color=color, stroke_width=3,
            fill_color=SURFACE, fill_opacity=1,
        )
        self.hour = Line(ORIGIN, UP * radius * 0.50, stroke_width=3.5, color=color)
        self.minute = Line(ORIGIN, UP * radius * 0.80, stroke_width=2.5, color=color)
        for h in (self.hour, self.minute):
            h.move_to(self.face.get_center(), aligned_edge=DOWN)
        self.add(self.face, self.hour, self.minute)

    def spin(self, turns=2.0, **anim_kw):
        c = self.face.get_center()
        return AnimationGroup(
            Rotate(self.minute, -TAU * turns, about_point=c),
            Rotate(self.hour, -TAU * turns / 12, about_point=c),
            **anim_kw,
        )


def _chip(size=0.62, color=INK_SOFT):
    """Small processor glyph: a square die with pins."""
    die = RoundedRectangle(
        width=size, height=size, corner_radius=0.06,
        stroke_color=color, stroke_width=3, fill_color=SURFACE_2, fill_opacity=1,
    )
    core = RoundedRectangle(
        width=size * 0.42, height=size * 0.42, corner_radius=0.03,
        stroke_color=color, stroke_width=2, fill_opacity=0,
    ).move_to(die)
    pins = VGroup()
    for d, along in ((UP, RIGHT), (DOWN, RIGHT), (LEFT, UP), (RIGHT, UP)):
        for k in (-1, 0, 1):
            base = die.get_center() + d * size / 2 + along * k * size * 0.28
            pins.add(Line(base, base + d * 0.11, stroke_width=2.5, color=color))
    return VGroup(die, core, pins)


class GPUBox(VGroup):
    """Full execution + evaluation.  The scarce resource in the whole story."""

    def __init__(self, width=3.5, height=2.6, caption="Execute + Evaluate", **kw):
        super().__init__(**kw)
        self.panel = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            fill_color=PANEL_FILL, fill_opacity=1,
            stroke_color=PANEL_STROKE, stroke_width=3.5,
        )
        self.chip = _chip(0.68)
        self.gpu_label = txt("GPU", size=FS_SMALL, color=INK, weight=BOLD)
        head = VGroup(self.chip, self.gpu_label).arrange(RIGHT, buff=0.22)

        self.bar = ProgressBar(width=width - 1.0)
        self.clock = Clock(0.26)
        row = VGroup(self.bar, self.clock).arrange(RIGHT, buff=0.24)

        self.caption = txt(caption, size=FS_TINY, color=INK_SOFT)

        body = VGroup(head, row, self.caption).arrange(DOWN, buff=0.26)
        body.move_to(self.panel.get_center())
        self.add(self.panel, body)

    # -- animations ---------------------------------------------------------
    def run(self, seconds=2.0, turns=2.0):
        """One slow, visibly costly execution."""
        return AnimationGroup(
            self.bar.fill_to(1.0, run_time=seconds),
            self.clock.spin(turns, run_time=seconds, rate_func=linear),
        )

    def rearm(self):
        self.bar.reset()
        return self


class SandboxBox(VGroup):
    """Agentic RPM's sandbox clone: a small, fast pilot experiment (§3.2)."""

    def __init__(self, width=3.4, height=2.75, **kw):
        super().__init__(**kw)
        self.panel = DashedVMobject(
            RoundedRectangle(
                width=width, height=height, corner_radius=0.18,
                stroke_color=SEL_ACCENT, stroke_width=3, fill_opacity=0,
            ),
            num_dashes=54,
            dashed_ratio=0.6,
        )
        self.backing = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            fill_color=SURFACE_BLUE, fill_opacity=1, stroke_width=0,
        )
        self.title = txt("Sandbox", size=FS_SMALL, color=SEL_ACCENT, weight=MEDIUM)

        # tiny training curve
        self.axes_box = VGroup(
            Line(np.array([-0.9, -0.42, 0]), np.array([0.9, -0.42, 0]),
                 stroke_width=2, color=RULE),
            Line(np.array([-0.9, -0.42, 0]), np.array([-0.9, 0.46, 0]),
                 stroke_width=2, color=RULE),
        )
        self.curve = VMobject(stroke_color=SEL_ACCENT, stroke_width=4, fill_opacity=0)
        pts = []
        for i in range(25):
            x = -0.9 + 1.8 * i / 24
            y = -0.42 + 0.80 * (1 - np.exp(-3.1 * (i / 24))) + 0.035 * np.sin(i * 1.7)
            pts.append(np.array([x, y, 0]))
        self.curve.set_points_smoothly(pts)

        self.pilot_label = txt("pilot run  ·  tiny model  ·  1 epoch",
                               size=FS_TINY, color=INK_SOFT)
        self.bar = ProgressBar(width=1.9, height=0.16, color=SEL_ACCENT)

        plot = VGroup(self.axes_box, self.curve)
        body = VGroup(self.title, plot, self.bar, self.pilot_label).arrange(DOWN, buff=0.20)
        body.move_to(self.backing.get_center())
        self.add(self.backing, self.panel, body)

    def run(self, seconds=1.0):
        return AnimationGroup(
            Create(self.curve, run_time=seconds, rate_func=linear),
            self.bar.fill_to(1.0, run_time=seconds),
        )


def make_gpu_box(**kw):
    return GPUBox(**kw)


def make_sandbox_box(**kw):
    return SandboxBox(**kw)
