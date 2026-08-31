"""The AI research agent (AIRA) — the thing that proposes candidates."""

from manim import *

from .theme import (
    FS_BODY,
    FS_TINY,
    FONT,
    INK,
    INK_SOFT,
    PANEL_FILL,
    PANEL_STROKE,
    txt,
)


class AgentBox(VGroup):
    def __init__(
        self,
        width=3.1,
        height=1.7,
        subtitle="proposes solutions",
        title_size=FS_BODY,
        subtitle_size=FS_TINY,
        title_font=FONT,
        subtitle_font=FONT,
        center_title=False,
        **kw,
    ):
        super().__init__(**kw)
        self.panel = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            fill_color=PANEL_FILL, fill_opacity=1,
            stroke_color=PANEL_STROKE, stroke_width=3.5,
        )
        if center_title:
            self.title = VGroup(
                txt(
                    "AI Research",
                    size=title_size,
                    color=INK,
                    weight=MEDIUM,
                    font=title_font,
                ),
                txt(
                    "Agent",
                    size=title_size,
                    color=INK,
                    weight=MEDIUM,
                    font=title_font,
                ),
            ).arrange(DOWN, buff=0.04)
        else:
            self.title = txt(
                "AI Research\nAgent",
                size=title_size,
                color=INK,
                weight=MEDIUM,
                font=title_font,
                line_spacing=0.8,
            )
        parts = [self.title]
        if subtitle:
            self.subtitle = txt(
                subtitle,
                size=subtitle_size,
                color=INK_SOFT,
                font=subtitle_font,
            )
            parts.append(self.subtitle)
        body = VGroup(*parts).arrange(DOWN, buff=0.16).move_to(self.panel.get_center())
        self.add(self.panel, body)


def make_agent_box(**kw):
    return AgentBox(**kw)
