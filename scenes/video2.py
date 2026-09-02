"""Video 2 - inference-only RPM versus agentic RPM.

Both halves remain visible as fixed, downward pipelines:

    five candidates -> preference model -> selected candidate

The inference-only side reasons over existing evidence; the agentic side runs
sandbox pilot experiments, which take deliberately longer to finish.

Render:  .venv/bin/manim render -ql scenes/video2.py Video2HowRPM
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from manim import *

from components import *  # noqa: F403


# Shared marks keep the two halves directly comparable and vertically aligned.
LAYOUT = {
    "half_centers": (-3.55, 3.55),
    "title_y": 3.53,
    "subtitle_y": 3.15,
    "candidate_y": 2.02,
    "candidate_offsets": (-2.48, -1.24, 0.00, 1.24, 2.48),
    "model_y": -0.15,
    "selected_y": -2.55,
}

SECTION_LABEL_GAP = 0.14
PREFERENCE_MODEL_TITLE_GAP = 0.07

CANDIDATE_LABELS_V2 = ("A", "B", "C", "D", "E")
INFERENCE_SELECTED_INDEX = 2
AGENTIC_SELECTED_INDEX = 3
INFERENCE_ACCENT = "#F29040"
INFERENCE_ACCENT_LIGHT = COST

PILOT_POSITIONS = (
    (-1.23, 0.34),
    (0.00, 0.34),
    (1.23, 0.34),
    (-0.62, -0.34),
    (0.62, -0.34),
)

OBSERVATIONS = (
    ("A", "POSITIVE", SEL_ACCENT),
    ("B", "PLATEAU", INK_SOFT),
    ("C", "UNSTABLE", COST),
    ("D", "BEST GAIN", GOOD_STROKE),
    ("E", "NO GAIN", INK_FAINT),
)

# Duration, in seconds, for each sandbox progress bar to fill.
SANDBOX_PILOT_PROGRESS_RUN_TIME = 1.60
SANDBOX_PILOT_COMPLETION_TIME = 0.20
SANDBOX_PILOT_LAG_RATIO = 0.16
INFERENCE_REASONING_RUN_TIME = 1.35


class ProxyProgressBar(VGroup):
    """Compact pilot bar whose fill keeps the same geometry as its track."""

    def __init__(self, width=0.48, height=0.085, color=SEL_ACCENT, **kwargs):
        super().__init__(**kwargs)
        self.fill_color = color
        self.fill_height = height
        self.backing = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.014,
            fill_color=TRACK,
            fill_opacity=1,
            stroke_width=0,
        )
        self.track = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.014,
            fill_opacity=0,
            stroke_color=RULE,
            stroke_width=1.2,
        )
        self.bar = self._make_fill(0.020)
        self.bar.move_to(self.track.get_left(), aligned_edge=LEFT)
        self.add(self.backing, self.bar, self.track)

    def _make_fill(self, width):
        return RoundedRectangle(
            width=width,
            height=self.fill_height,
            corner_radius=min(0.012, width / 2),
            fill_color=self.fill_color,
            fill_opacity=1,
            stroke_width=0,
        )

    def fill_to(self, frac=1.0, **animation_kwargs):
        width = max(0.020, self.track.width * frac)
        target = self._make_fill(width)
        target.move_to(self.track.get_left(), aligned_edge=LEFT)
        animation_kwargs.setdefault("rate_func", linear)
        return Transform(self.bar, target, **animation_kwargs)


class SandboxExecutionCard(VGroup):
    """A terminal-like pilot run with progress, completion, and one finding."""

    def __init__(self, label, observation, observation_color, width=1.12,
                 height=0.57, **kwargs):
        super().__init__(**kwargs)
        self.observation_color = observation_color
        self.panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.07,
            fill_color=SURFACE_BLUE,
            fill_opacity=1,
            stroke_color=SEL_ACCENT,
            stroke_width=1.8,
        )
        prompt = txt(f"> {label}", size=10, color=SEL_ACCENT)
        self.status = txt("RUNNING", size=7, color=INK_SOFT)
        header = VGroup(prompt, self.status).arrange(RIGHT, buff=0.09)
        header.move_to(self.panel.get_top() + DOWN * 0.12)

        self.bar = ProxyProgressBar(width=0.78, height=0.075, color=SEL_ACCENT)
        self.bar.move_to(self.panel.get_center() + UP * 0.005)

        self.observation = txt(observation, size=9, color=observation_color)
        self.observation.move_to(self.panel.get_bottom() + UP * 0.13)
        self.observation.set_opacity(0)
        self.add(self.panel, header, self.bar, self.observation)

    def run(self, run_time=0.55):
        done = txt("DONE", size=7, color=GOOD_STROKE).move_to(self.status)
        finding = self.observation.copy().set_opacity(1)
        return Succession(
            self.bar.fill_to(1.0, run_time=run_time),
            AnimationGroup(
                Transform(self.status, done),
                Transform(self.observation, finding),
                run_time=0.20,
            ),
        )


class PreferenceModel(VGroup):
    """A preference-model container whose evaluation activity stays inside it."""

    def __init__(self, subtitle, internals, width=4.65, height=2.15, **kwargs):
        super().__init__(**kwargs)
        self.panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            fill_color=SURFACE,
            fill_opacity=1,
            stroke_color=PANEL_STROKE,
            stroke_width=3.0,
        )
        self.title = txt("PREFERENCE MODEL", size=20, color=INK, weight=BOLD)
        self.subtitle = txt(subtitle, size=14, color=INK_SOFT, weight=NORMAL)
        header = VGroup(self.title, self.subtitle).arrange(
            DOWN,
            buff=PREFERENCE_MODEL_TITLE_GAP,
        )
        header.move_to(self.panel.get_top() + DOWN * 0.38)

        self.internals = internals
        self.internals.move_to(self.panel.get_center() + DOWN * 0.27)
        self.add(self.panel, header, self.internals)

    def pulse(self, run_time=0.55, amount=1.025):
        return self.animate(
            run_time=run_time,
            rate_func=there_and_back,
        ).scale(amount)


def make_candidate_row(center_x):
    """Five equal candidate cards aligned across one half of the frame."""
    cards = VGroup()
    for label, offset in zip(CANDIDATE_LABELS_V2, LAYOUT["candidate_offsets"]):
        card = CandidateCard(
            label,
            width=1.08,
            height=0.58,
            code_lines=2,
            use_diagram=False,
        )
        card.move_to(np.array([center_x + offset, LAYOUT["candidate_y"], 0.0]))
        cards.add(card)
    return cards


def make_evaluation_dimensions():
    """High-level reasoning signals, not chain-of-thought."""
    labels = (
        "Prior Evidence",
        "Correctness",
        "Problem Fit",
        "Iteration Potential",
    )
    dimensions = VGroup()
    for label in labels:
        panel = RoundedRectangle(
            width=1.55,
            height=0.48,
            corner_radius=0.08,
            fill_color=SURFACE_2,
            fill_opacity=1,
            stroke_color=RULE,
            stroke_width=1.5,
        )
        text = txt(
            label,
            size=11,
            color=INK_SOFT,
            weight=NORMAL,
        ).move_to(panel)
        dimensions.add(VGroup(panel, text))
    dimensions.arrange_in_grid(rows=2, cols=2, buff=(0.14, 0.12))
    return dimensions


def make_sandbox_cards():
    experiments = VGroup()
    for (label, finding, color), (x, y) in zip(OBSERVATIONS, PILOT_POSITIONS):
        experiment = SandboxExecutionCard(label, finding, color)
        experiment.move_to(np.array([x, y, 0.0]))
        experiments.add(experiment)
    return experiments


def make_inference_preference_model(center_x):
    model = PreferenceModel(
        "LLM selects using code + context",
        make_evaluation_dimensions(),
    )
    return model.move_to(np.array([center_x, LAYOUT["model_y"], 0.0]))


def make_agentic_preference_model(center_x):
    model = PreferenceModel(
        "LLM selects using additional pilot experiments",
        make_sandbox_cards(),
    )
    return model.move_to(np.array([center_x, LAYOUT["model_y"], 0.0]))


def make_selected_output(
    center_x,
    label,
    selection_fill=SEL_FILL,
    selection_stroke=SEL_STROKE,
):
    card = CandidateCard(
        label,
        width=1.85,
        height=0.66,
        code_lines=2,
        use_diagram=False,
    )
    card.move_to(np.array([center_x, LAYOUT["selected_y"], 0.0]))

    badge_circle = Circle(
        radius=0.15,
        fill_color=selection_fill,
        fill_opacity=1,
        stroke_color=selection_stroke,
        stroke_width=2.0,
    )
    check = VGroup(
        Line(LEFT * 0.060, DOWN * 0.010, color=INK, stroke_width=3.0),
        Line(DOWN * 0.010, RIGHT * 0.085 + UP * 0.090, color=INK, stroke_width=3.0),
    ).move_to(badge_circle)
    badge = VGroup(badge_circle, check)
    badge.move_to(card.panel.get_corner(UR) + np.array([-0.02, 0.01, 0.0]))

    label = txt("SELECTED CANDIDATE", size=15, color=INK_SOFT, weight=MEDIUM)
    label.next_to(card, DOWN, buff=SECTION_LABEL_GAP)
    return card, badge, label


def downward_input_arrows(cards, model):
    """Five candidate branches feeding one independent shared output arrow."""
    connectors = []
    model_entry = model.panel.get_top() + UP * 0.06
    center_start = cards[INFERENCE_SELECTED_INDEX].panel.get_bottom() + DOWN * 0.05
    merge_y = interpolate(center_start[1], model_entry[1], 0.55)
    merge = np.array([model.get_center()[0], merge_y, 0.0])

    for i, card in enumerate(cards):
        start = card.panel.get_bottom() + DOWN * 0.05
        if i == INFERENCE_SELECTED_INDEX:
            connectors.append(
                Line(
                    start,
                    merge,
                    color=INK_FAINT,
                    stroke_width=2.3,
                )
            )
            continue
        control_1 = np.array([start[0], start[1] - 0.18, 0.0])
        control_2 = np.array([merge[0], merge[1] + 0.12, 0.0])
        connectors.append(
            CubicBezier(
                start,
                control_1,
                control_2,
                merge,
                stroke_color=INK_FAINT,
                stroke_width=2.1,
                fill_opacity=0,
            )
        )
    shared_arrow = Arrow(
        merge,
        model_entry,
        buff=0,
        color=INK_FAINT,
        stroke_width=2.3,
        tip_length=0.15,
        max_tip_length_to_length_ratio=0.35,
        max_stroke_width_to_length_ratio=999,
    )
    return VGroup(*connectors, shared_arrow)


def downward_output_arrow(model, selected_card):
    return Arrow(
        model.panel.get_bottom() + DOWN * 0.06,
        selected_card.panel.get_top() + UP * 0.06,
        buff=0,
        color=INK_FAINT,
        stroke_width=2.8,
        tip_length=0.18,
        max_tip_length_to_length_ratio=0.35,
        max_stroke_width_to_length_ratio=999,
    )


def illuminate(arrows, lag_ratio=0.10, color=SEL_ACCENT):
    return LaggedStart(
        *[Indicate(arrow, color=color, scale_factor=1.0) for arrow in arrows],
        lag_ratio=lag_ratio,
    )


def animate_inference_model(model, color=INFERENCE_ACCENT):
    return Succession(
        model.pulse(run_time=0.50),
        LaggedStart(
            *[
                Indicate(dimension, color=color, scale_factor=1.025)
                for dimension in model.internals
            ],
            lag_ratio=0.20,
            run_time=1.35,
        ),
    )


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


def dim_connector(connector, opacity=0.48):
    """Dim a connector shaft while preserving any arrowhead at full opacity."""
    target = connector.copy()
    for part in target.family_members_with_points():
        if isinstance(part, ArrowTriangleFilledTip):
            continue
        part.set_stroke(
            opacity=part.get_stroke_opacity() * opacity,
            family=False,
        )
        part.set_fill(
            opacity=part.get_fill_opacity() * opacity,
            family=False,
        )
    return Transform(connector, target)


def reveal_selection(
    input_cards,
    input_arrows,
    output_card,
    badge,
    selected_index,
    fill_color=SEL_FILL,
    stroke_color=SEL_STROKE,
):
    output_target = output_card.copy()
    output_target.panel.set_fill(fill_color, opacity=1)
    output_target.panel.set_stroke(stroke_color, width=3.5, opacity=1)
    return AnimationGroup(
        *[
            dimmed(card, opacity=0.48)
            for i, card in enumerate(input_cards)
            if i != selected_index
        ],
        *[
            dim_connector(arrow, opacity=0.48)
            for i, arrow in enumerate(input_arrows[: len(input_cards)])
            if i != selected_index
        ],
        Transform(output_card, output_target),
        FadeIn(badge, scale=0.7),
        run_time=0.70,
    )


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


class Video2HowRPM(RPMScene):
    """Static split-screen comparison with two downward decision pipelines.

    The comparison stays fixed while the agentic pilots are allowed to run
    longer than the inference-only model's reasoning pass.
    """

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

        left_model = make_inference_preference_model(left_center)
        right_model = make_agentic_preference_model(right_center)
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

        # The complete comparison is present before animation begins.
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
