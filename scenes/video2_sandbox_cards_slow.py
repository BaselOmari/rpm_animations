"""Video 2 sandbox-card variant with deliberately slower pilot runs.

Render:
    .venv/bin/manim render -ql scenes/video2_sandbox_cards_slow.py \
        Video2SandboxCardsSlow
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from manim import *

from components import INK_SOFT, RULE, SEL_ACCENT, SEL_FILL, SEL_STROKE, txt
from scenes.video2 import (
    AGENTIC_SELECTED_INDEX,
    CANDIDATE_LABELS_V2,
    INFERENCE_ACCENT,
    INFERENCE_ACCENT_LIGHT,
    INFERENCE_SELECTED_INDEX,
    LAYOUT,
    SECTION_LABEL_GAP,
    animate_inference_model,
    downward_input_arrows,
    downward_output_arrow,
    illuminate,
    make_candidate_row,
    make_preference_model,
    make_selected_output,
    reveal_selection,
)
from scenes.video2_sandbox_cards import Video2SandboxCards


# Duration, in seconds, for each sandbox progress bar to fill.
SANDBOX_PILOT_PROGRESS_RUN_TIME = 1.60
SANDBOX_PILOT_COMPLETION_TIME = 0.20
SANDBOX_PILOT_LAG_RATIO = 0.16
INFERENCE_REASONING_RUN_TIME = 1.35


def animate_sandbox_until_inference_finishes(model):
    """Advance every pilot linearly while the inference-only model evaluates."""
    pilots = model.internals
    pilot_duration = (
        SANDBOX_PILOT_PROGRESS_RUN_TIME + SANDBOX_PILOT_COMPLETION_TIME
    )
    stagger_delay = pilot_duration * SANDBOX_PILOT_LAG_RATIO
    partial_runs = []
    for index, pilot in enumerate(pilots):
        delay = index * stagger_delay
        active_time = max(0.0, INFERENCE_REASONING_RUN_TIME - delay)
        fraction = min(1.0, active_time / SANDBOX_PILOT_PROGRESS_RUN_TIME)
        partial_runs.append(
            Succession(
                Wait(delay),
                pilot.bar.fill_to(fraction, run_time=active_time),
            )
        )
    return Succession(
        model.pulse(run_time=0.50),
        AnimationGroup(
            *partial_runs,
            lag_ratio=0,
        ),
    )


def finish_sandbox_pilots(model):
    """Continue each partially filled bar without resetting its progress."""
    pilot_duration = (
        SANDBOX_PILOT_PROGRESS_RUN_TIME + SANDBOX_PILOT_COMPLETION_TIME
    )
    stagger_delay = pilot_duration * SANDBOX_PILOT_LAG_RATIO
    completions = []
    for index, pilot in enumerate(model.internals):
        elapsed = max(
            0.0,
            INFERENCE_REASONING_RUN_TIME - index * stagger_delay,
        )
        remaining = max(0.0, SANDBOX_PILOT_PROGRESS_RUN_TIME - elapsed)
        completions.append(pilot.run(run_time=remaining))
    return AnimationGroup(*completions, lag_ratio=0)


def reveal_completed_side(
    model,
    output_arrow,
    candidates,
    input_arrows,
    selected_card,
    badge,
    selected_index,
    accent_color=SEL_ACCENT,
    fill_color=SEL_FILL,
    stroke_color=SEL_STROKE,
):
    selection = reveal_selection(
        candidates,
        input_arrows,
        selected_card,
        badge,
        selected_index,
        fill_color=fill_color,
        stroke_color=stroke_color,
    )
    selection.set_run_time(0.80)
    return Succession(
        AnimationGroup(
            Indicate(
                output_arrow,
                color=accent_color,
                scale_factor=1.0,
            ),
            Flash(
                model.get_bottom(),
                color=accent_color,
                flash_radius=0.42,
            ),
            run_time=0.70,
        ),
        selection,
    )


class Video2SandboxCardsSlow(Video2SandboxCards):
    """Keep the comparison fixed while allowing the agentic pilots to run longer."""

    def construct(self):
        left_center, right_center = LAYOUT["half_centers"]

        divider = Line(
            np.array([0.0, 3.78, 0.0]),
            np.array([0.0, -3.35, 0.0]),
            color=RULE,
            stroke_width=2.0,
        )
        left_title = txt(
            "INFERENCE-ONLY RPM", size=25, color=INFERENCE_ACCENT, weight=BOLD
        ).move_to(np.array([left_center, LAYOUT["title_y"], 0.0]))
        right_title = txt(
            "AGENTIC RPM", size=25, color=SEL_ACCENT, weight=BOLD
        ).move_to(np.array([right_center, LAYOUT["title_y"], 0.0]))
        left_subtitle = txt(
            "Reason using existing evidence", size=17, color=INK_SOFT
        ).move_to(np.array([left_center, LAYOUT["subtitle_y"], 0.0]))
        right_subtitle = txt(
            "Reason using pilot experiments", size=17, color=INK_SOFT
        ).move_to(np.array([right_center, LAYOUT["subtitle_y"], 0.0]))

        left_candidates = make_candidate_row(left_center)
        right_candidates = make_candidate_row(right_center)
        left_header = txt(
            "CANDIDATE SOLUTIONS", size=15, color=INK_SOFT, weight=MEDIUM
        ).next_to(left_candidates, UP, buff=SECTION_LABEL_GAP)
        right_header = txt(
            "CANDIDATE SOLUTIONS", size=15, color=INK_SOFT, weight=MEDIUM
        ).next_to(right_candidates, UP, buff=SECTION_LABEL_GAP)

        left_model = make_preference_model(left_center, "inference")
        right_model = self.make_agentic_preference_model(right_center)
        left_selected, left_badge, left_selected_label = make_selected_output(
            left_center,
            CANDIDATE_LABELS_V2[INFERENCE_SELECTED_INDEX],
            selection_fill=INFERENCE_ACCENT,
            selection_stroke=INFERENCE_ACCENT_LIGHT,
        )
        right_selected, right_badge, right_selected_label = make_selected_output(
            right_center,
            CANDIDATE_LABELS_V2[AGENTIC_SELECTED_INDEX],
        )

        left_inputs = downward_input_arrows(left_candidates, left_model)
        right_inputs = downward_input_arrows(right_candidates, right_model)
        left_output = downward_output_arrow(left_model, left_selected)
        right_output = downward_output_arrow(right_model, right_selected)

        self.add(
            divider,
            left_inputs,
            right_inputs,
            left_output,
            right_output,
            left_candidates,
            right_candidates,
            left_model,
            right_model,
            left_selected,
            right_selected,
            left_title,
            right_title,
            left_subtitle,
            right_subtitle,
            left_header,
            right_header,
            left_selected_label,
            right_selected_label,
        )
        initial_state = VGroup(*[mobject.copy() for mobject in self.mobjects])
        self.wait(0.65)

        self.play(
            LaggedStart(
                *[
                    Indicate(card, color=INFERENCE_ACCENT, scale_factor=1.025)
                    for card in left_candidates
                ],
                lag_ratio=0.10,
            ),
            LaggedStart(
                *[
                    Indicate(card, color=SEL_ACCENT, scale_factor=1.025)
                    for card in right_candidates
                ],
                lag_ratio=0.10,
            ),
            run_time=0.95,
        )
        self.play(
            illuminate(left_inputs, color=INFERENCE_ACCENT),
            illuminate(right_inputs),
            run_time=0.75,
        )

        self.play(
            animate_inference_model(left_model),
            animate_sandbox_until_inference_finishes(right_model),
        )

        self.play(
            reveal_completed_side(
                left_model,
                left_output,
                left_candidates,
                left_inputs,
                left_selected,
                left_badge,
                INFERENCE_SELECTED_INDEX,
                accent_color=INFERENCE_ACCENT,
                fill_color=INFERENCE_ACCENT,
                stroke_color=INFERENCE_ACCENT_LIGHT,
            ),
            finish_sandbox_pilots(right_model),
        )

        self.play(
            reveal_completed_side(
                right_model,
                right_output,
                right_candidates,
                right_inputs,
                right_selected,
                right_badge,
                AGENTIC_SELECTED_INDEX,
            ),
        )

        self.wait(3.5)
        current_state = list(self.mobjects)
        self.play(
            AnimationGroup(
                *[FadeOut(mobject) for mobject in current_state],
                lag_ratio=0,
            ),
            FadeIn(initial_state),
            run_time=0.80,
        )
        self.wait(0.80)
