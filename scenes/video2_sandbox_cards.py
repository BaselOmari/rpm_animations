"""Video 2 variant: agentic pilots shown as sandbox execution cards.

Render: .venv/bin/manim render -qh scenes/video2_sandbox_cards.py Video2SandboxCards
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from manim import *

from components import (
    COST,
    GOOD_STROKE,
    INK_FAINT,
    INK_SOFT,
    RULE,
    SEL_ACCENT,
    SURFACE_BLUE,
    txt,
)
from scenes.video2 import LAYOUT, PreferenceModel, ProxyProgressBar, Video2HowRPM


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


def make_sandbox_cards():
    experiments = VGroup()
    for (label, finding, color), (x, y) in zip(OBSERVATIONS, PILOT_POSITIONS):
        experiment = SandboxExecutionCard(label, finding, color)
        experiment.move_to(np.array([x, y, 0.0]))
        experiments.add(experiment)
    return experiments


class Video2SandboxCards(Video2HowRPM):
    def make_agentic_preference_model(self, center_x):
        model = PreferenceModel(
            "LLM selects using additional pilot experiments",
            make_sandbox_cards(),
        )
        return model.move_to(np.array([center_x, LAYOUT["model_y"], 0.0]))
