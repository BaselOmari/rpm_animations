"""Standalone preview of the shared diagrammatic ML candidate cards.

Render the animated preview:
    .venv/bin/manim render -ql scenes/candidate_diagrams_preview.py CandidateDiagramsPreview

Save the final frame:
    .venv/bin/manim render -ql -s scenes/candidate_diagrams_preview.py CandidateDiagramsPreview
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from manim import *

from components import BG, CandidateCard


PREVIEW_CARD_WIDTH = 2.12
PREVIEW_CARD_HEIGHT = 0.84
PREVIEW_CARD_GAP = 0.34


class CandidateDiagramsPreview(Scene):
    def construct(self):
        self.camera.background_color = BG

        cards = VGroup(
            *[
                CandidateCard(
                    label,
                    width=PREVIEW_CARD_WIDTH,
                    height=PREVIEW_CARD_HEIGHT,
                )
                for label in "ABCDE"
            ]
        )
        cards.arrange(RIGHT, buff=PREVIEW_CARD_GAP)
        cards.move_to(ORIGIN)

        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.08) for card in cards],
                lag_ratio=0.22,
            ),
            run_time=2.4,
        )
        self.wait(4.0)
