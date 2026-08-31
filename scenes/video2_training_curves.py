"""Video 2 variant: agentic pilot experiments shown as training curves.

Render: .venv/bin/manim render -qh scenes/video2_training_curves.py Video2TrainingCurves
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from manim import *

from components import COST, INeK_FAINT, INK_SOFT, RULE, SEL_ACCENT, SURFACE_BLUE, txt
from scenes.video2 import LAYOUT, PreferenceModel, Video2HowRPM


PILOT_POSITIONS = (
    (-1.20, 0.31),
    (0.00, 0.31),
    (1.20, 0.31),
    (-0.60, -0.31),
    (0.60, -0.31),
)

CURVE_SPECS = (
    ("A", (0.00, 0.05, 0.10, 0.13, 0.15), SEL_ACCENT),
    ("B", (0.01, 0.06, 0.09, 0.09, 0.09), INK_SOFT),
    ("C", (0.03, 0.14, 0.05, 0.13, 0.04), COST),
    ("D", (0.00, 0.04, 0.11, 0.18, 0.24), SEL_ACCENT),
    ("E", (0.02, 0.03, 0.04, 0.035, 0.04), INK_FAINT),
)


class TrainingCurveExperiment(VGroup):
    """A tiny pilot chart whose shape communicates the observed behavior."""

    def __init__(self, label, values, color, width=1.08, height=0.52, **kwargs):
        super().__init__(**kwargs)
        self.curve_color = color
        self.panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            fill_color=SURFACE_BLUE,
            fill_opacity=1,
            stroke_color=RULE,
            stroke_width=1.8,
        )
        self.label = txt(f"PILOT {label}", size=10, color=INK_SOFT)
        self.label.move_to(self.panel.get_top() + DOWN * 0.11)

        origin = self.panel.get_center() + np.array([-0.37, -0.16, 0.0])
        self.axes = VGroup(
            Line(origin, origin + RIGHT * 0.76, color=RULE, stroke_width=1.2),
            Line(origin, origin + UP * 0.30, color=RULE, stroke_width=1.2),
        )
        points = [
            origin + np.array([0.76 * i / (len(values) - 1), value, 0.0])
            for i, value in enumerate(values)
        ]
        self.curve_template = VMobject(
            stroke_color=color,
            stroke_width=2.6,
            fill_opacity=0,
        ).set_points_smoothly(points)
        self.curve_template.set_stroke(opacity=0)
        self.add(self.panel, self.axes, self.label, self.curve_template)

    def run(self, run_time=0.55):
        curve = self.curve_template.copy().set_stroke(
            color=self.curve_color,
            width=2.6,
            opacity=1,
        )
        endpoint = Dot(curve.get_end(), radius=0.024, color=self.curve_color)
        return Succession(
            Create(curve, run_time=run_time, rate_func=linear),
            GrowFromCenter(endpoint, run_time=0.12),
        )


def make_training_curve_experiments():
    experiments = VGroup()
    for (label, values, color), (x, y) in zip(CURVE_SPECS, PILOT_POSITIONS):
        experiment = TrainingCurveExperiment(label, values, color)
        experiment.move_to(np.array([x, y, 0.0]))
        experiments.add(experiment)
    return experiments


class Video2TrainingCurves(Video2HowRPM):
    def make_agentic_preference_model(self, center_x):
        model = PreferenceModel(
            "LLM selects using additional pilot experiments",
            make_training_curve_experiments(),
        )
        return model.move_to(np.array([center_x, LAYOUT["model_y"], 0.0]))
