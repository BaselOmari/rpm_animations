"""Video 1, Act 2: the RPM allocates full experimental compute.

Render independently:
    .venv/bin/manim render -ql scenes/video1_act2.py Video1Act2
"""

import pathlib
import sys

import numpy as np

SCENES_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCENES_DIR))
sys.path.insert(0, str(SCENES_DIR.parent))

from manim import *

from components import *  # noqa: F403
from video1_common import (
    CANDIDATES,
    SELECTED_INDEX,
    BlackBoxRPM,
    dim_connector,
    make_candidate_cards,
    make_check_badge,
    paced as video1_paced,
    select_card,
)


ACT2_TIME_SCALE = 1.15
ACT2_BODY_FONT = "Facebook Sans App"
INPUT_JUNCTION_GAP = 0.54
MESSAGE_LINE_GAP = 0.14


def paced(seconds):
    """Apply additional Act 2 pacing without slowing the other two acts."""
    return video1_paced(seconds) * ACT2_TIME_SCALE


def make_body_text(text, size, color, weight=MEDIUM):
    """Use the same readable body typography established in Act 1."""
    return txt(
        text,
        size=size,
        color=color,
        weight=weight,
        font=ACT2_BODY_FONT,
    )


def make_centerline_arrow(
    source,
    target,
    direction,
    color,
    stroke,
    tip,
    gap=0.13,
):
    """Connect the exact edge centers of horizontally aligned panels."""
    return Arrow(
        source.get_edge_center(direction) + direction * gap,
        target.get_edge_center(-direction) - direction * gap,
        buff=0,
        color=color,
        stroke_width=stroke,
        tip_length=tip,
        max_tip_length_to_length_ratio=0.35,
        max_stroke_width_to_length_ratio=999,
    )


def make_rpm_input_flow(cards, rpm):
    """Curve all candidate paths into one junction, then enter the RPM."""
    target_edge = rpm.panel.get_edge_center(LEFT)
    junction = target_edge + LEFT * INPUT_JUNCTION_GAP
    branches = VGroup()

    for index, card in enumerate(cards):
        start = card.panel.get_edge_center(RIGHT) + RIGHT * 0.08
        if index == SELECTED_INDEX:
            path = Line(
                start,
                junction,
                color=INK_FAINT,
                stroke_width=2.2,
            )
        else:
            span = junction[0] - start[0]
            path = CubicBezier(
                start,
                start + RIGHT * span * 0.52,
                junction + LEFT * span * 0.28,
                junction,
                stroke_color=INK_FAINT,
                stroke_width=2.2,
                fill_opacity=0,
            )
        branches.add(path)

    trunk = Arrow(
        junction,
        target_edge + LEFT * 0.11,
        buff=0,
        color=INK_FAINT,
        stroke_width=2.6,
        tip_length=0.16,
        max_tip_length_to_length_ratio=0.40,
        max_stroke_width_to_length_ratio=999,
    )
    return branches, trunk


class Act2Timeline:
    """Solution: rank candidates before committing full experimental compute."""

    def play_act2(self):
        cards = make_candidate_cards(width=1.42, height=0.56)
        cards.arrange(DOWN, buff=0.16).move_to(np.array([-5.45, 0.0, 0.0]))
        candidates_label = make_body_text(
            "CANDIDATE SOLUTIONS", size=17, color=INK_SOFT, weight=MEDIUM
        ).next_to(cards, UP, buff=0.22)

        rpm = BlackBoxRPM(
            subtitle_text="AI Research Preference Model",
            subtitle_size=13,
            subtitle_font=ACT2_BODY_FONT,
        ).move_to(np.array([-2.15, 0.0, 0.0]))
        selected = CandidateCard(
            CANDIDATES[SELECTED_INDEX],
            width=1.50,
            height=0.68,
            code_lines=2,
        )
        selected.move_to(np.array([0.85, 0.0, 0.0]))
        selected.panel.set_fill(SEL_FILL, opacity=1)
        selected.panel.set_stroke(SEL_STROKE, width=3.5, opacity=1)
        badge = make_check_badge(selected)
        selected_label = make_body_text(
            "SELECTED CANDIDATE",
            size=16,
            color=INK_SOFT,
            weight=MEDIUM,
        ).next_to(selected, UP, buff=0.22)

        gpu = GPUBox(width=2.85, height=2.20, caption="Full experiment")
        gpu.move_to(np.array([4.65, 0.0, 0.0]))

        input_branches, input_trunk = make_rpm_input_flow(cards, rpm)
        choice_flow = make_centerline_arrow(
            rpm.panel,
            selected.panel,
            RIGHT,
            color=INK_FAINT,
            stroke=3.0,
            tip=0.17,
        )
        compute_flow = make_centerline_arrow(
            selected.panel,
            gpu.panel,
            RIGHT,
            color=INK_FAINT,
            stroke=3.0,
            tip=0.17,
        )
        line = make_body_text(
            "RPMs assess candidates before running them",
            size=26,
            color=INK_SOFT,
            weight=NORMAL,
        )
        only_one = make_body_text(
            "and allocate compute to the most promising candidate",
            size=25,
            color=INK,
            weight=MEDIUM,
        )
        VGroup(line, only_one).arrange(
            DOWN,
            buff=MESSAGE_LINE_GAP,
        ).move_to(np.array([0.0, -3.30, 0.0]))

        self.play(
            FadeIn(VGroup(cards, candidates_label), shift=RIGHT * 0.12),
            FadeIn(line),
            run_time=paced(0.58),
        )
        self.wait(paced(0.24))
        self.play(
            LaggedStart(
                FadeIn(rpm),
                LaggedStart(
                    *[Create(path) for path in input_branches],
                    lag_ratio=0.08,
                ),
                GrowArrow(input_trunk),
                lag_ratio=0.18,
            ),
            run_time=paced(1.05),
        )
        self.play(
            rpm.pulse(run_time=paced(0.60)),
            run_time=paced(0.60),
        )

        nonselected_cards = [
            card for i, card in enumerate(cards) if i != SELECTED_INDEX
        ]
        self.play(
            *[dimmed(card, opacity=0.35) for card in nonselected_cards],
            *[
                dim_connector(path, opacity=0.25)
                for i, path in enumerate(input_branches)
                if i != SELECTED_INDEX
            ],
            select_card(cards[SELECTED_INDEX], fill=False),
            input_branches[SELECTED_INDEX].animate.set_color(SEL_ACCENT),
            input_trunk.animate.set_color(SEL_ACCENT),
            LaggedStart(
                GrowArrow(choice_flow.set_color(SEL_ACCENT)),
                AnimationGroup(
                    FadeIn(selected, scale=0.88),
                    FadeIn(badge, scale=0.75),
                    FadeIn(selected_label, shift=DOWN * 0.08),
                    FadeIn(only_one, shift=UP * 0.08),
                ),
                lag_ratio=0.28,
            ),
            run_time=paced(0.82),
        )

        self.play(
            LaggedStart(
                FadeIn(gpu, shift=LEFT * 0.12),
                GrowArrow(compute_flow.set_color(SEL_ACCENT)),
                lag_ratio=0.30,
            ),
            run_time=paced(0.78),
        )
        self.play(
            gpu.run(seconds=paced(1.75), turns=1.7),
            run_time=paced(1.75),
        )
        self.wait(paced(1.35))


class Video1Act2(Act2Timeline, RPMScene):
    def construct(self):
        self.play_act2()
