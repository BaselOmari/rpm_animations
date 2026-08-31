"""Scene bases: white research-diagram background, shared helpers."""

from manim import *

from .theme import BG


class RPMScene(Scene):
    """Static-camera scene on a white background."""

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    # -- small conveniences -------------------------------------------------
    def swap(self, old, new, run_time=0.5):
        """Cross-fade one caption for another, in place."""
        return AnimationGroup(
            FadeOut(old, shift=UP * 0.18, run_time=run_time),
            FadeIn(new, shift=UP * 0.18, run_time=run_time),
        )


class RPMMovingScene(MovingCameraScene):
    """Same, but with a camera we can push into the RPM box."""

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def swap(self, old, new, run_time=0.5):
        return AnimationGroup(
            FadeOut(old, shift=UP * 0.18, run_time=run_time),
            FadeIn(new, shift=UP * 0.18, run_time=run_time),
        )
