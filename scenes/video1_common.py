"""Shared geometry, styling, and pacing for the three Video 1 acts."""

import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from manim import *

from components import *  # noqa: F403


CANDIDATES = ("A", "B", "C", "D", "E")
SELECTED_INDEX = 2
VIDEO1_TIME_SCALE = 1.40


def paced(seconds):
    """Apply the scene-wide pacing multiplier to animation and hold durations."""
    return seconds * VIDEO1_TIME_SCALE


class BlackBoxRPM(VGroup):
    """The RPM as a deliberately unexplained preference mechanism."""

    def __init__(self, width=2.55, height=1.28, title_size=28,
                 subtitle_size=14, title_font=FONT, subtitle_font=FONT,
                 subtitle_text="Research Preference Model", **kwargs):
        super().__init__(**kwargs)
        self.panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.11,
            fill_color=SURFACE,
            fill_opacity=1,
            stroke_color=PANEL_STROKE,
            stroke_width=3.2,
        )
        self.title = txt(
            "RPM",
            size=title_size,
            color=INK,
            weight=BOLD,
            font=title_font,
        )
        self.subtitle = txt(
            subtitle_text,
            size=subtitle_size,
            color=INK_SOFT,
            weight=NORMAL,
            font=subtitle_font,
        )
        body = VGroup(self.title, self.subtitle).arrange(DOWN, buff=0.08)
        body.move_to(self.panel)
        self.add(self.panel, body)

    def pulse(self, run_time=0.55, amount=1.035):
        return self.animate(
            run_time=run_time,
            rate_func=there_and_back,
        ).scale(amount)


class QuestionHub(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(
            radius=0.38,
            fill_color=SURFACE_2,
            fill_opacity=1,
            stroke_color=COST,
            stroke_width=3.0,
        )
        self.mark = txt("?", size=30, color=COST, weight=BOLD).move_to(self.circle)
        self.add(self.circle, self.mark)


def make_candidate_cards(width=1.45, height=0.56):
    return VGroup(
        *[
            CandidateCard(label, width=width, height=height, code_lines=2)
            for label in CANDIDATES
        ]
    )


def make_check_badge(card):
    circle = Circle(
        radius=0.15,
        fill_color=SEL_FILL,
        fill_opacity=1,
        stroke_color=SEL_STROKE,
        stroke_width=2.0,
    )
    check = VGroup(
        Line(LEFT * 0.060, DOWN * 0.010, color=INK, stroke_width=3.0),
        Line(
            DOWN * 0.010,
            RIGHT * 0.085 + UP * 0.090,
            color=INK,
            stroke_width=3.0,
        ),
    ).move_to(circle)
    badge = VGroup(circle, check)
    badge.move_to(card.panel.get_corner(UR) + np.array([-0.02, 0.01, 0.0]))
    return badge


def select_card(card, fill=True):
    target = card.copy()
    if fill:
        target.panel.set_fill(SEL_FILL, opacity=1)
    target.panel.set_stroke(SEL_STROKE, width=3.5, opacity=1)
    return Transform(card, target)


def dim_connector(connector, opacity=0.20):
    target = connector.copy()
    for part in target.family_members_with_points():
        part.set_stroke(
            opacity=part.get_stroke_opacity() * opacity,
            family=False,
        )
        part.set_fill(
            opacity=part.get_fill_opacity() * opacity,
            family=False,
        )
    return Transform(connector, target)


def decision_funnel(cards, target):
    """Curved, arrowless candidate paths converging on one decision point."""
    paths = VGroup()
    end = target.get_top() + UP * 0.05
    for card in cards:
        start = card.get_bottom() + DOWN * 0.04
        control_1 = start + DOWN * 0.24
        control_2 = np.array([end[0], end[1] + 0.20, 0.0])
        paths.add(
            CubicBezier(
                start,
                control_1,
                control_2,
                end,
                stroke_color=INK_FAINT,
                stroke_width=2.2,
                fill_opacity=0,
            )
        )
    return paths


def section_break(
    scene,
    title_text,
    subheader_text=None,
    subheader_font=FONT,
    subheader_size=17,
    title_font=FONT,
    title_size=40,
    lower_subheader_text=None,
    lower_subheader_font=FONT,
    title_time_scale=1.0,
    reveal_together=False,
):
    """Clear the previous act and introduce the next section title."""
    current = list(scene.mobjects)
    if current:
        scene.play(
            *[FadeOut(mobject) for mobject in current],
            run_time=paced(0.55),
        )
    title_lines = title_text.splitlines()
    if len(title_lines) > 1:
        title = VGroup(
            *[
                txt(
                    line,
                    size=title_size,
                    color=INK,
                    weight=MEDIUM,
                    font=title_font,
                )
                for line in title_lines
            ]
        ).arrange(DOWN, buff=0.10)
    else:
        title = txt(
            title_text,
            size=title_size,
            color=INK,
            weight=MEDIUM,
            font=title_font,
        )
    main_parts = [title]
    if lower_subheader_text:
        lower_subheader = txt(
            lower_subheader_text,
            size=20,
            color=INK_SOFT,
            weight=MEDIUM,
            font=lower_subheader_font,
        )
        main_parts.append(lower_subheader)
    main_block = VGroup(*main_parts).arrange(DOWN, buff=0.16)

    if subheader_text:
        subheader = txt(
            subheader_text,
            size=subheader_size,
            color=INK_SOFT,
            weight=MEDIUM,
            font=subheader_font,
        )
        title_card = VGroup(subheader, main_block).arrange(DOWN, buff=0.16)
        if reveal_together:
            scene.play(
                FadeIn(title_card, scale=0.98),
                run_time=paced(0.40) * title_time_scale,
            )
        else:
            scene.play(
                LaggedStart(
                    FadeIn(subheader, scale=0.98),
                    FadeIn(main_block, scale=0.98),
                    lag_ratio=0.72,
                ),
                run_time=paced(0.40) * title_time_scale,
            )
        scene.wait(paced(0.52) * title_time_scale)
    else:
        title_card = main_block
        scene.play(
            FadeIn(title_card, scale=0.98),
            run_time=paced(0.42) * title_time_scale,
        )
        scene.wait(paced(0.62) * title_time_scale)
    scene.play(
        FadeOut(title_card),
        run_time=paced(0.34) * title_time_scale,
    )
