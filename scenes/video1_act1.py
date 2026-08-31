"""Video 1, Act 1: cheap idea generation versus expensive experiments.

Render independently:
    .venv/bin/manim render -ql scenes/video1_act1.py Video1Act1
"""

import pathlib
import sys

import numpy as np

SCENES_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCENES_DIR))
sys.path.insert(0, str(SCENES_DIR.parent))

from manim import *

from components import *  # noqa: F403
from components.rpm import curved_arrow
from video1_common import (
    QuestionHub,
    decision_funnel,
    make_candidate_cards,
    paced as video1_paced,
)


FULL_EXPERIMENT_INDEX = 0
ACT1_TIME_SCALE = 1.15
ACT1_BODY_FONT = "Facebook Sans App"
CAPTION_SUBTITLE_SIZE = 15
CAPTION_SUBTITLE_GAP = 0.13
EXPERIMENT_DETAIL_LINE_GAP = 0.065
DECISION_HEADING_GAP = 0.15


def paced(seconds):
    """Apply additional Act 1 pacing without slowing the other two acts."""
    return video1_paced(seconds) * ACT1_TIME_SCALE


def make_body_text(text, size, color, weight=MEDIUM):
    """Use one baseline and a body font with reliable small-size spacing."""
    return txt(
        text,
        size=size,
        color=color,
        weight=weight,
        font=ACT1_BODY_FONT,
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
    """Connect exact edge centers instead of a rounded shape's corner point."""
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


def make_generation_flow(agent, cards):
    """One shared trunk that branches halfway toward the five ideas."""
    start = agent.panel.get_right() + RIGHT * 0.04
    target_x = cards[0].panel.get_left()[0] - 0.10
    junction = np.array([(start[0]*4 + target_x) / 5, start[1], 0.0])
    trunk = Line(start, junction, color=INK_FAINT, stroke_width=2.2)
    branches = VGroup()
    for card in cards:
        branches.add(
            curved_arrow(
                junction,
                card.panel.get_left() + LEFT * 0.10,
                bow=0.28,
                color=INK_FAINT,
                stroke=2.2,
                tip_length=0.15,
                tip_width=0.13,
            )
        )
    return trunk, branches


class Act1Timeline:
    """Problem: many cheap ideas compete for scarce experimental compute."""

    def play_act1(self):
        left_heading = txt(
            "GENERATE  IDEAS", size=20, color=INK_SOFT, weight=MEDIUM
        ).move_to(np.array([-3.55, 3.35, 0.0]))
        right_heading = txt(
            "RUN  FULL EXPERIMENT", size=20, color=INK_SOFT, weight=MEDIUM
        ).move_to(np.array([3.55, 3.35, 0.0]))
        divider = Line(
            np.array([0.0, 3.65, 0.0]),
            np.array([0.0, -2.65, 0.0]),
            color=RULE,
            stroke_width=2.0,
        )

        agent = AgentBox(
            width=2.45,
            height=1.30,
            subtitle="generates  solutions",
            title_size=22,
            subtitle_size=15,
            title_font=ACT1_BODY_FONT,
            subtitle_font=ACT1_BODY_FONT,
            center_title=True,
        )
        agent.move_to(np.array([-5.15, 0.65, 0.0]))
        cards = make_candidate_cards()
        cards.arrange(DOWN, buff=0.12).move_to(np.array([-2.15, 0.65, 0.0]))
        spawn_trunk, spawn_branches = make_generation_flow(agent, cards)
        spawn = VGroup(spawn_trunk, spawn_branches)

        gpu = GPUBox(width=3.05, height=2.30, caption="Full experiment")
        gpu.move_to(np.array([4.55, 0.45, 0.0]))

        cheap = make_body_text(
            "Generating  ideas  is  cheap",
            size=24,
            color=GOOD_STROKE,
            weight=NORMAL,
        ).move_to(np.array([-3.55, -2.55, 0.0]))
        cheap_detail = make_body_text(
            "Low-cost LLM inference",
            size=CAPTION_SUBTITLE_SIZE,
            color=INK_SOFT,
            weight=NORMAL,
        ).next_to(cheap, DOWN, buff=CAPTION_SUBTITLE_GAP)

        self.play(
            FadeIn(VGroup(left_heading, right_heading, divider)),
            FadeIn(agent, shift=RIGHT * 0.18),
            FadeIn(gpu, shift=LEFT * 0.18),
            run_time=paced(0.62),
        )
        self.play(Create(spawn_trunk), run_time=paced(0.22))
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(Create(arrow), GrowFromCenter(card))
                    for arrow, card in zip(spawn_branches, cards)
                ],
                lag_ratio=0.12,
            ),
            FadeIn(VGroup(cheap, cheap_detail)),
            run_time=paced(0.95),
        )

        experiment_card = cards[FULL_EXPERIMENT_INDEX].copy()
        experiment_card.move_to(np.array([1.35, gpu.get_center()[1], 0.0]))
        into_gpu = make_centerline_arrow(
            experiment_card.panel,
            gpu.panel,
            RIGHT,
            color=INK_FAINT,
            stroke=3.0,
            tip=0.17,
        )
        self.play(
            TransformFromCopy(cards[FULL_EXPERIMENT_INDEX], experiment_card),
            GrowArrow(into_gpu),
            run_time=paced(0.55),
        )
        traveller = experiment_card.copy()
        self.add(traveller)
        self.play(
            traveller.animate.scale(0.55).move_to(gpu).set_opacity(0),
            run_time=paced(0.45),
        )
        self.remove(traveller)

        expensive = make_body_text(
            "Evaluating them is expensive",
            size=24,
            color=COST,
            weight=MEDIUM,
        ).move_to(np.array([3.55, -2.55, 0.0]))
        expensive_detail = VGroup(
            make_body_text(
                "Dozens of GPUs",
                size=CAPTION_SUBTITLE_SIZE,
                color=INK_SOFT,
                weight=NORMAL,
            ),
            make_body_text(
                "Hundreds of Compute Hours",
                size=CAPTION_SUBTITLE_SIZE,
                color=INK_SOFT,
                weight=NORMAL,
            ),
        ).arrange(DOWN, buff=EXPERIMENT_DETAIL_LINE_GAP)
        expensive_detail.next_to(expensive, DOWN, buff=CAPTION_SUBTITLE_GAP)
        self.play(
            gpu.run(seconds=paced(2.45), turns=2.25),
            FadeIn(
                VGroup(expensive, expensive_detail),
                run_time=paced(0.35),
            ),
        )
        self.wait(paced(0.55))

        cards.generate_target()
        for card, x in zip(cards.target, (-4.8, -2.4, 0.0, 2.4, 4.8)):
            card.move_to(np.array([x, 1.60, 0.0]))
        reset_gpu = GPUBox(width=3.05, height=2.30, caption="Full experiment")
        reset_gpu.scale(0.72).move_to(np.array([0.0, -1.95, 0.0]))
        self.play(
            FadeOut(VGroup(left_heading, right_heading, divider, agent, spawn)),
            FadeOut(
                VGroup(
                    experiment_card,
                    into_gpu,
                    cheap,
                    cheap_detail,
                    expensive,
                    expensive_detail,
                )
            ),
            MoveToTarget(cards),
            Transform(gpu, reset_gpu),
            run_time=paced(0.78),
        )

        hub = QuestionHub().move_to(np.array([0.0, 0.10, 0.0]))
        funnel = decision_funnel(cards, hub)
        to_gpu = make_centerline_arrow(
            hub.circle,
            gpu,
            DOWN,
            color=COST,
            stroke=3.4,
            tip=0.18,
        )
        question = txt(
            "which idea deserves the compute?",
            size=34,
            color=INK,
            weight=MEDIUM,
        )
        budget_context = make_body_text(
            "When compute is limited",
            size=24,
            color=INK_SOFT,
            weight=MEDIUM,
        )
        VGroup(budget_context, question).arrange(
            DOWN,
            buff=DECISION_HEADING_GAP,
        ).move_to(np.array([0.0, 3.25, 0.0]))
        self.play(
            FadeIn(budget_context, shift=DOWN * 0.10),
            run_time=paced(0.42),
        )
        self.wait(paced(0.65))
        self.play(
            FadeIn(question, shift=DOWN * 0.10),
            FadeIn(hub, scale=0.85),
            LaggedStart(*[Create(path) for path in funnel], lag_ratio=0.08),
            run_time=paced(0.78),
        )
        self.play(GrowArrow(to_gpu), run_time=paced(0.32))
        self.wait(paced(1.25))


class Video1Act1(Act1Timeline, RPMScene):
    def construct(self):
        self.play_act1()
