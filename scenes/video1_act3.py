"""Video 1, Act 3: where an RPM fits in an AI research-agent search loop.

Render independently:
    .venv/bin/manim render -ql scenes/video1_act3.py Video1Act3
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
from components.theme import NODE_R
from video1_common import BlackBoxRPM, make_check_badge, paced


ACT3_BODY_FONT = "Facebook Sans App"
ACT3_CANDIDATES = ("A", "B", "C", "D", "E")
ACT3_SELECTED_INDEX = 2
ACT3_NODE_SCORE_FONT_SIZE = 24

ATTEMPT_STAGE_FOCUS_APPEAR_TIME = 0.24
ATTEMPT_STAGE_FOCUS_MOVE_TIME = 0.28
ATTEMPT_STAGE_FOCUS_HOLD_TIME = 0.30
ATTEMPT_SCORE_FOCUS_HOLD_TIME = 0.42

INTRO_TREE_SCALE = 0.72
INTRO_TREE_ROOT = np.array([0.00, 1.20, 0.0])
WORK_TREE_SCALE = 0.50
WORK_TREE_ROOT = np.array([-5.05, 0.82, 0.0])


def make_body_text(text, size, color, weight=MEDIUM):
    return txt(
        text,
        size=size,
        color=color,
        weight=weight,
        font=ACT3_BODY_FONT,
    )


def apply_act3_score_typography(tree):
    """Apply the Act 3 score size without changing shared tree components."""
    for node in tree.nodes.values():
        if not node.label_text:
            continue
        replacement = txt(
            node.label_text,
            size=ACT3_NODE_SCORE_FONT_SIZE,
            color=INK,
        ).move_to(node.circle)
        node.remove(node.label)
        node.label = replacement
        node.add(replacement)
    return tree


def make_plan_figure():
    bullets = VGroup()
    for index, width in enumerate((0.52, 0.42, 0.48)):
        y = 0.19 - index * 0.19
        bullets.add(Dot([-0.29, y, 0], radius=0.025, color=SEL_ACCENT))
        bullets.add(
            RoundedRectangle(
                width=width,
                height=0.055,
                corner_radius=0.025,
                fill_color=INK_FAINT,
                fill_opacity=1,
                stroke_width=0,
            ).move_to([-0.02, y, 0])
        )
    return bullets


def make_code_figure():
    bracket = VGroup(
        Line(UP * 0.24, DOWN * 0.24, color=INK_SOFT, stroke_width=2.2),
        Line(UP * 0.24, UP * 0.24 + RIGHT * 0.09, color=INK_SOFT, stroke_width=2.2),
        Line(DOWN * 0.24, DOWN * 0.24 + RIGHT * 0.09, color=INK_SOFT, stroke_width=2.2),
    ).shift(LEFT * 0.34)
    lines = VGroup()
    for width in (0.52, 0.39, 0.46, 0.30):
        lines.add(
            RoundedRectangle(
                width=width,
                height=0.055,
                corner_radius=0.025,
                fill_color=INK_FAINT,
                fill_opacity=1,
                stroke_width=0,
            )
        )
    lines.arrange(DOWN, buff=0.085, aligned_edge=LEFT).shift(RIGHT * 0.10)
    return VGroup(bracket, lines)


def make_mini_chip():
    die = RoundedRectangle(
        width=0.52,
        height=0.52,
        corner_radius=0.05,
        stroke_color=INK_SOFT,
        stroke_width=2.4,
        fill_color=SURFACE_2,
        fill_opacity=1,
    )
    core = RoundedRectangle(
        width=0.22,
        height=0.22,
        corner_radius=0.025,
        stroke_color=INK_SOFT,
        stroke_width=1.8,
        fill_opacity=0,
    ).move_to(die)
    pins = VGroup()
    for direction, along in ((UP, RIGHT), (DOWN, RIGHT), (LEFT, UP), (RIGHT, UP)):
        for offset in (-1, 0, 1):
            start = die.get_center() + direction * 0.26 + along * offset * 0.14
            pins.add(
                Line(
                    start,
                    start + direction * 0.08,
                    color=INK_SOFT,
                    stroke_width=2.0,
                )
            )
    return VGroup(die, core, pins)


class MiniRunFigure(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        chip = make_mini_chip()
        self.bar = ProgressBar(width=0.92, height=0.12, color=COST)
        clock = Clock(radius=0.11)
        activity = VGroup(self.bar, clock).arrange(RIGHT, buff=0.13)
        VGroup(chip, activity).arrange(DOWN, buff=0.18)
        self.add(chip, activity)


def make_logs_figure():
    status = Dot([-0.42, 0.20, 0.0], radius=0.035, color=GOOD_STROKE)
    lines = VGroup()
    for index, width in enumerate((0.66, 0.48, 0.58, 0.36)):
        lines.add(
            RoundedRectangle(
                width=width,
                height=0.045,
                corner_radius=0.02,
                fill_color=INK_FAINT if index < 3 else GOOD_STROKE,
                fill_opacity=1,
                stroke_width=0,
            )
        )
    lines.arrange(DOWN, buff=0.09, aligned_edge=LEFT)
    lines.move_to(np.array([0.08, -0.02, 0.0]))
    return VGroup(status, lines)


class AttemptStage(VGroup):
    def __init__(self, label, figure=None, width=1.82, height=1.28, **kwargs):
        super().__init__(**kwargs)
        self.panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=PANEL_STROKE,
            stroke_width=2.6,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        top_right = self.panel.get_corner(UR)
        fold_size = 0.20
        fold_corner = top_right + LEFT * fold_size + DOWN * fold_size
        self.fold = VGroup(
            Line(
                top_right + LEFT * fold_size,
                fold_corner,
                color=RULE,
                stroke_width=1.7,
            ),
            Line(
                fold_corner,
                top_right + DOWN * fold_size,
                color=RULE,
                stroke_width=1.7,
            ),
        )
        self.label = make_body_text(label, size=17, color=INK, weight=MEDIUM)
        self.label.move_to(self.panel.get_top() + DOWN * 0.20)
        self.header_rule = Line(
            self.panel.get_left() + np.array([0.15, 0.29, 0.0]),
            self.panel.get_right() + np.array([-0.15, 0.29, 0.0]),
            color=RULE,
            stroke_width=1.5,
        )
        self.figure = figure
        self.add(self.panel, self.fold, self.header_rule, self.label)
        if figure is not None:
            figure.scale(min(1.24 / figure.width, 0.64 / figure.height, 1.0))
            figure.move_to(self.panel.get_center() + DOWN * 0.14)
            self.add(self.figure)


def make_stage_arrow(source, target):
    """A center-aligned connector with breathing room at both card boundaries."""
    return Arrow(
        source.panel.get_edge_center(RIGHT) + RIGHT * 0.10,
        target.panel.get_edge_center(LEFT) + LEFT * 0.10,
        buff=0,
        color=INK_SOFT,
        stroke_width=2.7,
        tip_length=0.12,
        max_tip_length_to_length_ratio=0.38,
        max_stroke_width_to_length_ratio=999,
    )


class ExpandedResearchAttempt(VGroup):
    """One complete research attempt before it is summarized as a tree node."""

    def __init__(self, center=np.array([0.0, -0.20, 0.0]), **kwargs):
        super().__init__(**kwargs)
        center = np.array(center, dtype=float)
        self.panel = RoundedRectangle(
            width=12.70,
            height=2.72,
            corner_radius=0.16,
            stroke_color=PANEL_STROKE,
            stroke_width=2.8,
            fill_color=SURFACE,
            fill_opacity=0.72,
        ).move_to(center)
        self.title = make_body_text(
            "ONE RESEARCH ATTEMPT",
            size=22,
            color=INK,
            weight=MEDIUM,
        ).move_to(self.panel.get_top() + DOWN * 0.28)

        self.run_figure = MiniRunFigure()
        self.plan = AttemptStage("PLAN", make_plan_figure())
        self.code = AttemptStage("CODE", make_code_figure())
        self.run = AttemptStage("RUN", self.run_figure)
        self.logs = AttemptStage("LOGS", make_logs_figure())
        self.score_shell = AttemptStage("SCORE")
        self.stages = VGroup(
            self.plan,
            self.code,
            self.run,
            self.logs,
            self.score_shell,
        ).arrange(RIGHT, buff=0.55)
        self.stages.move_to(center + DOWN * 0.32)
        self.score_position = self.score_shell.panel.get_center() + DOWN * 0.12
        self.arrows = VGroup(
            *[
                make_stage_arrow(source, target)
                for source, target in zip(self.stages[:-1], self.stages[1:])
            ]
        )
        self.container = VGroup(self.panel, self.title)
        self.score_frame = self.score_shell
        self.collapse_parts = VGroup(
            self.panel,
            self.title,
            self.plan,
            self.code,
            self.run,
            self.logs,
            self.score_frame,
            self.arrows,
        )
        self.add(
            self.panel,
            self.title,
            self.arrows,
            self.plan,
            self.code,
            self.run,
            self.logs,
            self.score_frame,
        )

    def focus_frame(self, stage):
        return stage.panel.copy().set_fill(opacity=0).set_stroke(
            SEL_ACCENT,
            width=3.4,
            opacity=1,
        )


class NavigationStage(VGroup):
    def __init__(self, number, text, width=3.72, active=False, **kwargs):
        super().__init__(**kwargs)
        self.width_anchor = Rectangle(
            width=width,
            height=0.78,
            stroke_opacity=0,
            fill_opacity=0,
        )
        self.disc = Circle(
            radius=0.18,
            stroke_color=SEL_ACCENT if active else INK_FAINT,
            stroke_width=2.0,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        self.number = make_body_text(
            str(number),
            size=17,
            color=SEL_ACCENT if active else INK_FAINT,
            weight=MEDIUM,
        ).move_to(self.disc)
        self.text = make_body_text(
            text,
            size=19,
            color=INK if active else INK_FAINT,
            weight=MEDIUM,
        )
        content = VGroup(VGroup(self.disc, self.number), self.text).arrange(
            RIGHT,
            buff=0.18,
        )
        content.move_to(self.width_anchor.get_center() + UP * 0.11)
        self.underline = Line(
            LEFT * width * 0.45,
            RIGHT * width * 0.45,
            color=SEL_ACCENT if active else RULE,
            stroke_width=3.5 if active else 2.0,
        ).move_to(self.width_anchor.get_bottom() + UP * 0.07)
        self.add(self.width_anchor, self.disc, self.number, self.text, self.underline)

    def activate(self):
        return AnimationGroup(
            self.disc.animate.set_stroke(SEL_ACCENT, width=3.0),
            self.number.animate.set_color(SEL_ACCENT),
            self.text.animate.set_color(INK),
            self.underline.animate.set_color(SEL_ACCENT).set_stroke(width=3.5),
        )

    def complete(self):
        return AnimationGroup(
            self.disc.animate.set_stroke(INK_SOFT, width=2.0),
            self.number.animate.set_color(INK_SOFT),
            self.text.animate.set_color(INK_SOFT),
            self.underline.animate.set_color(INK_SOFT).set_stroke(width=2.0),
        )


def make_navigation():
    steps = VGroup(
        NavigationStage(1, "GENERATE  MUTATIONS", active=True),
        NavigationStage(2, "RPM  SELECTS"),
        NavigationStage(3, "EVALUATE  +  UPDATE"),
    ).arrange(RIGHT, buff=0.24)
    steps.move_to(np.array([0.0, 2.96, 0.0]))
    headline = make_body_text(
        "With a Research Preference Model",
        size=22,
        color=INK,
        weight=MEDIUM,
    ).move_to(np.array([0.0, 3.64, 0.0]))
    return VGroup(*steps, headline)


def make_mutation_flow(parent, candidates):
    """Use one parent output and one split point for every mutation branch."""
    start = parent.get_edge_center(RIGHT) + RIGHT * 0.05
    candidate_left = min(card.panel.get_left()[0] for card in candidates) - 0.07
    junction = np.array(
        [interpolate(start[0], candidate_left, 0.50), start[1], 0.0]
    )
    trunk = Line(start, junction, color=INK_FAINT, stroke_width=2.4)
    branches = VGroup(
        *[
            curved_arrow(
                junction,
                card.panel.get_edge_center(LEFT) + LEFT * 0.07,
                bow=0.24,
                color=INK_FAINT,
                stroke=2.2,
                tip_length=0.13,
                tip_width=0.11,
            )
            for card in candidates
        ]
    )
    return trunk, branches


def make_rpm_input_flow(candidates, rpm):
    """Merge all candidate paths at one point, then use one arrow into the RPM."""
    target = rpm.panel.get_edge_center(LEFT)
    rightmost = max(card.panel.get_right()[0] for card in candidates)
    junction = np.array(
        [interpolate(rightmost, target[0], 0.56), target[1], 0.0]
    )
    branches = VGroup()
    for card in candidates:
        start = card.panel.get_edge_center(RIGHT) + RIGHT * 0.04
        span = junction[0] - start[0]
        if abs(start[1] - junction[1]) < 0.02:
            path = Line(start, junction, color=INK_FAINT, stroke_width=2.1)
        else:
            path = CubicBezier(
                start,
                start + RIGHT * span * 0.48,
                junction + LEFT * span * 0.28,
                junction,
                stroke_color=INK_FAINT,
                stroke_width=2.1,
                fill_opacity=0,
            )
        branches.add(path)
    trunk = Arrow(
        junction,
        target + LEFT * 0.09,
        buff=0,
        color=INK_FAINT,
        stroke_width=2.6,
        tip_length=0.15,
        max_tip_length_to_length_ratio=0.38,
        max_stroke_width_to_length_ratio=999,
    )
    return branches, trunk


def make_horizontal_arrow(source, target, color=INK_FAINT, stroke=3.2, tip=0.17):
    """Join exact horizontal edge centers so rounded corners cannot skew arrows."""
    return Arrow(
        source.get_edge_center(RIGHT) + RIGHT * 0.09,
        target.get_edge_center(LEFT) + LEFT * 0.09,
        buff=0,
        color=color,
        stroke_width=stroke,
        tip_length=tip,
        max_tip_length_to_length_ratio=0.35,
        max_stroke_width_to_length_ratio=999,
    )


def dim_connector_keep_tip(connector, opacity=0.24):
    """Dim a connector shaft while preserving its arrowhead."""
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


def select_candidate_card(card):
    """Select the whole card so its panel cannot cover its label or diagram."""
    target = card.copy()
    target.panel.set_fill(SEL_FILL, opacity=1)
    target.panel.set_stroke(SEL_STROKE, width=3.4, opacity=1)
    return Transform(card, target)


def make_parent_ring(parent):
    return Circle(
        radius=parent.radius + 0.13,
        stroke_color=SEL_ACCENT,
        stroke_width=3.0,
        fill_opacity=0,
    ).move_to(parent)


class Act3Timeline:
    """Explain a node once, then show the RPM-driven search-tree update."""

    def act3_establish_search_tree(self):
        statement = make_body_text(
            "An AI Research Agent searches through several research attempts",
            size=29,
            color=INK,
            weight=MEDIUM,
        ).move_to(np.array([0.0, 3.00, 0.0]))

        tree = apply_act3_score_typography(figure1_tree())
        tree.scale(INTRO_TREE_SCALE).root_at(INTRO_TREE_ROOT)
        edges = VGroup(*tree.edges.values())
        nodes = VGroup(*tree.nodes.values())

        self.play(FadeIn(statement, shift=DOWN * 0.06), run_time=paced(0.35))
        self.play(
            LaggedStart(*[GrowArrow(edge) for edge in edges], lag_ratio=0.12),
            LaggedStart(
                *[FadeIn(node, scale=0.90) for node in nodes],
                lag_ratio=0.12,
            ),
            run_time=paced(0.62),
        )
        self.wait(paced(0.48))

        compact_node = tree["lr"]
        other_nodes = VGroup(tree["root"], tree["l"], tree["r"], tree["ll"])
        tree_context = VGroup(edges, other_nodes)
        tree_visual = VGroup(tree_context, compact_node)
        return statement, tree, tree_context, tree_visual, compact_node

    def act3_explain_node(self, statement, tree, tree_context, compact_node):
        node_label = make_body_text(
            "Each node represents one research attempt",
            size=27,
            color=INK,
            weight=MEDIUM,
        ).move_to(np.array([0.0, 3.08, 0.0]))
        explain_ring = make_parent_ring(compact_node)
        self.play(FadeOut(statement), run_time=paced(0.18))
        self.play(
            FadeIn(node_label),
            tree_context.animate.set_opacity(0.22),
            Create(explain_ring),
            Indicate(compact_node, color=SEL_ACCENT, scale_factor=1.08),
            run_time=paced(0.34),
        )
        self.wait(paced(0.22))

        anatomy = ExpandedResearchAttempt()
        work_template = apply_act3_score_typography(figure1_tree())
        work_template.scale(WORK_TREE_SCALE).root_at(WORK_TREE_ROOT)
        node_return_target = work_template["lr"].copy()

        root_center = tree["root"].get_center().copy()
        scale_ratio = WORK_TREE_SCALE / INTRO_TREE_SCALE
        score_scale = 0.29 / compact_node.radius
        compact_node.set_z_index(5)
        self.play(FadeOut(explain_ring), run_time=paced(0.16))
        self.play(
            tree_context.animate.scale(
                scale_ratio,
                about_point=root_center,
            ).shift(WORK_TREE_ROOT - root_center).set_opacity(0),
            compact_node.animate.scale(score_scale).move_to(anatomy.score_position),
            GrowFromCenter(anatomy.panel),
            FadeIn(anatomy.title),
            run_time=paced(0.65),
        )
        self.bring_to_front(compact_node)
        self.play(
            LaggedStart(
                *[
                    FadeIn(stage, shift=RIGHT * 0.04)
                    for stage in anatomy.stages
                ],
                lag_ratio=0.08,
            ),
            LaggedStart(
                *[GrowArrow(arrow) for arrow in anatomy.arrows],
                lag_ratio=0.12,
            ),
            run_time=paced(0.68),
        )
        self.bring_to_front(compact_node)
        self.wait(paced(0.72))

        active_frame = anatomy.focus_frame(anatomy.plan)
        self.play(
            Create(active_frame),
            run_time=paced(ATTEMPT_STAGE_FOCUS_APPEAR_TIME),
        )
        self.wait(paced(ATTEMPT_STAGE_FOCUS_HOLD_TIME))

        later_stages = (
            anatomy.code,
            anatomy.run,
            anatomy.logs,
            anatomy.score_frame,
        )
        for index, stage in enumerate(later_stages):
            animations = [
                anatomy.arrows[index].animate.set_color(SEL_ACCENT),
                Transform(active_frame, anatomy.focus_frame(stage)),
            ]
            if stage is anatomy.run:
                animations.append(anatomy.run_figure.bar.fill_to(0.88))
            if stage is anatomy.score_frame:
                animations.append(
                    Flash(
                        compact_node.get_center(),
                        color=GOOD_STROKE,
                        flash_radius=0.42,
                    )
                )
            self.play(
                *animations,
                run_time=paced(ATTEMPT_STAGE_FOCUS_MOVE_TIME),
            )
            self.wait(
                paced(
                    ATTEMPT_SCORE_FOCUS_HOLD_TIME
                    if stage is anatomy.score_frame
                    else ATTEMPT_STAGE_FOCUS_HOLD_TIME
                )
            )

        return node_label, anatomy, node_return_target, active_frame

    def act3_compress_attempt(
        self,
        node_label,
        anatomy,
        tree_context,
        compact_node,
        node_return_target,
        active_frame,
    ):
        collapse_target = anatomy.collapse_parts.copy()
        collapse_target.scale(0.04).move_to(node_return_target).set_opacity(0)
        frame_target = active_frame.copy()
        frame_target.scale(0.04).move_to(node_return_target).set_opacity(0)
        return_scale = node_return_target.radius / compact_node.radius
        self.play(
            Transform(anatomy.collapse_parts, collapse_target),
            Transform(active_frame, frame_target),
            compact_node.animate.scale(return_scale).move_to(node_return_target),
            tree_context.animate.set_opacity(1.0),
            FadeOut(node_label),
            run_time=paced(0.78),
        )
        self.remove(
            anatomy.collapse_parts,
            active_frame,
        )
        self.wait(paced(0.75))

    def act3_begin_navigation(self, tree):
        navigation = make_navigation()
        self.play(FadeIn(navigation, shift=DOWN * 0.05), run_time=paced(0.42))
        self.wait(paced(0.20))

        parent = tree["r"]
        parent_ring = make_parent_ring(parent)
        self.play(
            Create(parent_ring),
            Indicate(parent, color=SEL_ACCENT, scale_factor=1.08),
            run_time=paced(0.35),
        )
        self.wait(paced(0.15))
        return navigation, parent, parent_ring

    def act3_generate_candidates(self, parent):
        candidates = VGroup(
            *[
                CandidateCard(
                    label,
                    width=1.55,
                    height=0.56,
                    use_diagram=True,
                )
                for label in ACT3_CANDIDATES
            ]
        ).arrange(DOWN, buff=0.13)
        candidates.move_to(np.array([-2.18, -0.05, 0.0]))

        mutation_trunk, mutation_branches = make_mutation_flow(parent, candidates)
        self.play(Create(mutation_trunk), run_time=paced(0.20))
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        Create(branch),
                        FadeIn(candidate, shift=LEFT * 0.06),
                    )
                    for branch, candidate in zip(mutation_branches, candidates)
                ],
                lag_ratio=0.11,
            ),
            run_time=paced(0.64),
        )
        self.wait(paced(0.18))
        return candidates, mutation_trunk, mutation_branches

    def act3_rpm_selection(self, navigation, candidates, mutation_branches):
        rpm = BlackBoxRPM(
            width=2.70,
            height=1.06,
            title_size=24,
            subtitle_size=11,
            subtitle_text="AI Research Preference Model",
            subtitle_font=ACT3_BODY_FONT,
        ).move_to(np.array([0.55, -0.05, 0.0]))
        rpm_branches, rpm_trunk = make_rpm_input_flow(candidates, rpm)

        self.play(
            navigation[0].complete(),
            navigation[1].activate(),
            run_time=paced(0.28),
        )
        self.wait(paced(0.12))
        self.play(
            FadeIn(rpm, shift=LEFT * 0.06),
            LaggedStart(*[Create(path) for path in rpm_branches], lag_ratio=0.08),
            run_time=paced(0.52),
        )
        self.play(GrowArrow(rpm_trunk), run_time=paced(0.16))
        self.play(rpm.pulse(run_time=paced(0.34)), run_time=paced(0.34))

        selected_output = CandidateCard(
            ACT3_CANDIDATES[ACT3_SELECTED_INDEX],
            width=1.45,
            height=0.58,
            use_diagram=True,
        ).move_to(np.array([3.10, -0.05, 0.0]))
        selected_output.panel.set_fill(SEL_FILL, opacity=1)
        selected_output.panel.set_stroke(SEL_STROKE, width=3.4, opacity=1)
        check_badge = make_check_badge(selected_output)
        rpm_output = make_horizontal_arrow(
            rpm.panel,
            selected_output.panel,
            color=SEL_ACCENT,
            stroke=3.5,
            tip=0.17,
        )

        losers = [
            candidate
            for index, candidate in enumerate(candidates)
            if index != ACT3_SELECTED_INDEX
        ]
        self.play(
            *[dimmed(candidate, opacity=0.27) for candidate in losers],
            *[
                dim_connector_keep_tip(branch, opacity=0.24)
                for index, branch in enumerate(mutation_branches)
                if index != ACT3_SELECTED_INDEX
            ],
            *[
                path.animate.set_stroke(opacity=0.24)
                for index, path in enumerate(rpm_branches)
                if index != ACT3_SELECTED_INDEX
            ],
            select_candidate_card(candidates[ACT3_SELECTED_INDEX]),
            mutation_branches[ACT3_SELECTED_INDEX].animate.set_color(SEL_ACCENT),
            rpm_branches[ACT3_SELECTED_INDEX].animate.set_color(SEL_ACCENT),
            rpm_trunk.animate.set_color(SEL_ACCENT),
            run_time=paced(0.48),
        )
        self.play(
            GrowArrow(rpm_output),
            FadeIn(selected_output, shift=LEFT * 0.08),
            FadeIn(check_badge, scale=0.75),
            run_time=paced(0.30),
        )
        self.wait(paced(0.18))
        return rpm, rpm_branches, rpm_trunk, rpm_output, selected_output, check_badge

    def act3_evaluate_and_update(
        self,
        navigation,
        tree,
        tree_visual,
        parent_ring,
        candidates,
        mutation_trunk,
        mutation_branches,
        rpm,
        rpm_branches,
        rpm_trunk,
        rpm_output,
        selected_output,
        check_badge,
    ):
        gpu = GPUBox(width=2.50, height=2.42, caption="Full experiment")
        gpu.move_to(np.array([5.60, -0.05, 0.0]))
        to_gpu = make_horizontal_arrow(
            selected_output.panel,
            gpu.panel,
            color=SEL_ACCENT,
            stroke=3.4,
            tip=0.17,
        )
        self.play(
            navigation[1].complete(),
            navigation[2].activate(),
            run_time=paced(0.28),
        )
        self.wait(paced(0.12))
        self.play(
            FadeIn(gpu, shift=LEFT * 0.08),
            GrowArrow(to_gpu),
            run_time=paced(0.38),
        )

        traveller = selected_output.copy()
        self.add(traveller)
        self.play(
            traveller.animate.scale(0.50).move_to(gpu.panel).set_opacity(0),
            run_time=paced(0.22),
        )
        self.remove(traveller)
        self.play(
            gpu.run(seconds=paced(0.72), turns=1.0),
            run_time=paced(0.72),
        )

        evaluated_node = SolutionNode(
            "0.63",
            kind="good",
            radius=0.32,
            font_size=ACT3_NODE_SCORE_FONT_SIZE * 0.32 / NODE_R,
        ).move_to(selected_output)
        self.play(FadeOut(check_badge), run_time=paced(0.16))
        self.play(
            FadeOut(rpm_output),
            FadeOut(to_gpu),
            ReplacementTransform(selected_output, evaluated_node),
            Flash(
                evaluated_node.get_center(),
                color=GOOD_STROKE,
                flash_radius=0.44,
            ),
            run_time=paced(0.38),
        )

        final_tree = apply_act3_score_typography(figure1_tree(with_rr=True))
        final_tree.scale(WORK_TREE_SCALE).root_at(WORK_TREE_ROOT)
        evaluated_target = final_tree["rr"].copy()
        new_edge = final_tree.edge("r", "rr").copy()

        right_side = VGroup(
            candidates,
            mutation_trunk,
            mutation_branches,
            rpm_branches,
            rpm_trunk,
            rpm,
            gpu,
        )
        self.play(
            FadeOut(right_side),
            FadeOut(parent_ring),
            Transform(evaluated_node, evaluated_target, path_arc=-22 * DEGREES),
            run_time=paced(0.65),
        )
        self.play(
            GrowArrow(new_edge),
            Indicate(evaluated_node, color=GOOD_STROKE, scale_factor=1.08),
            run_time=paced(0.28),
        )

        completed_tree = VGroup(tree_visual, new_edge, evaluated_node)
        root_center = tree["root"].get_center().copy()
        final_root = np.array([0.0, 1.38, 0.0])
        self.play(
            FadeOut(navigation),
            completed_tree.animate.scale(1.48, about_point=root_center).shift(
                final_root - root_center
            ),
            run_time=paced(0.50),
        )

        closer = make_body_text(
            "RPM guides which research idea gets evaluated next",
            size=24,
            color=INK,
            weight=MEDIUM,
        ).move_to(np.array([0.0, -2.72, 0.0]))
        self.play(FadeIn(closer), run_time=paced(0.25))
        self.wait(paced(0.70))
        self.wait(2.0)

    def play_act3(self):
        statement, tree, tree_context, tree_visual, compact_node = (
            self.act3_establish_search_tree()
        )
        node_label, anatomy, node_return_target, active_frame = self.act3_explain_node(
            statement,
            tree,
            tree_context,
            compact_node,
        )
        self.act3_compress_attempt(
            node_label,
            anatomy,
            tree_context,
            compact_node,
            node_return_target,
            active_frame,
        )
        navigation, parent, parent_ring = self.act3_begin_navigation(tree)
        candidates, mutation_trunk, mutation_branches = self.act3_generate_candidates(
            parent
        )
        (
            rpm,
            rpm_branches,
            rpm_trunk,
            rpm_output,
            selected_output,
            check_badge,
        ) = self.act3_rpm_selection(navigation, candidates, mutation_branches)
        self.act3_evaluate_and_update(
            navigation,
            tree,
            tree_visual,
            parent_ring,
            candidates,
            mutation_trunk,
            mutation_branches,
            rpm,
            rpm_branches,
            rpm_trunk,
            rpm_output,
            selected_output,
            check_badge,
        )


class Video1Act3(Act3Timeline, RPMScene):
    def construct(self):
        self.play_act3()
