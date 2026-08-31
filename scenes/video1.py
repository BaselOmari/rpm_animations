"""Combined Video 1: problem -> RPM solution -> agent integration.

Render the complete video:
    .venv/bin/manim render -ql scenes/video1.py Video1WhyRPM

Each act also has an independently renderable scene in ``video1_act1.py``,
``video1_act2.py``, and ``video1_act3.py``.
"""

import pathlib
import sys

SCENES_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCENES_DIR))
sys.path.insert(0, str(SCENES_DIR.parent))

from components import RPMScene
from video1_act1 import Act1Timeline
from video1_act2 import Act2Timeline
from video1_act3 import Act3Timeline
from video1_common import section_break


class Video1WhyRPM(
    Act1Timeline,
    Act2Timeline,
    Act3Timeline,
    RPMScene,
):
    def construct(self):
        self.play_act1()
        section_break(
            self,
            "AI Research Preference Models",
            subheader_text="WE INTRODUCE",
            subheader_font="Facebook Sans App",
            lower_subheader_text="(RPMs)",
            lower_subheader_font="Facebook Sans App",
            title_time_scale=2.0,
        )
        self.play_act2()
        section_break(
            self,
            "RPMs Within AI Research Agents",
            subheader_text="WE INTEGRATE",
            subheader_font="Facebook Sans App",
            subheader_size=20,
            title_font="Facebook Sans App",
            title_size=36,
            title_time_scale=1.4,
            reveal_together=True,
        )
        self.play_act3()
