"""Compact, text-free ML architecture diagrams for candidate cards."""

from manim import *

from .theme import CAND_FILL, INK_FAINT, INK_SOFT, SURFACE_2


def _node(point, radius=0.050, fill=SURFACE_2, stroke_width=2.4):
    return Circle(
        radius=radius,
        stroke_color=INK_SOFT,
        stroke_width=stroke_width,
        fill_color=fill,
        fill_opacity=1,
    ).move_to(point)


def _line(start, end, width=2.05, opacity=1.0):
    return Line(
        start,
        end,
        stroke_color=INK_FAINT,
        stroke_width=width,
        stroke_opacity=opacity,
    )


def _arrow(start, end, width=2.10, tip_length=0.065):
    return Arrow(
        start,
        end,
        buff=0,
        color=INK_SOFT,
        stroke_width=width,
        tip_length=tip_length,
        max_tip_length_to_length_ratio=0.38,
        max_stroke_width_to_length_ratio=999,
    )


def make_tree_icon():
    """Left-to-right decision tree sized for a shallow candidate card."""
    points = {
        "root": [-0.70, 0.00, 0],
        "upper": [-0.23, 0.15, 0],
        "lower": [-0.23, -0.15, 0],
        "uu": [0.49, 0.23, 0],
        "ul": [0.49, 0.08, 0],
        "lu": [0.49, -0.08, 0],
        "ll": [0.49, -0.23, 0],
    }
    edges = VGroup(
        _line(points["root"], points["upper"]),
        _line(points["root"], points["lower"]),
        _line(points["upper"], points["uu"]),
        _line(points["upper"], points["ul"]),
        _line(points["lower"], points["lu"]),
        _line(points["lower"], points["ll"]),
    )
    nodes = VGroup(*[_node(point) for point in points.values()])
    return VGroup(edges, nodes)


def make_mlp_icon():
    """Sparse 2-3-2 fully connected network."""
    layer_specs = (
        (-0.62, (-0.14, 0.14)),
        (0.0, (-0.20, 0.0, 0.20)),
        (0.66, (-0.11, 0.11)),
    )
    layers = [
        VGroup(*[_node([x, y, 0], radius=0.043) for y in ys])
        for x, ys in layer_specs
    ]
    edges = VGroup()
    for left_layer, right_layer in zip(layers, layers[1:]):
        for source in left_layer:
            for target in right_layer:
                edges.add(
                    _line(
                        source.get_center(),
                        target.get_center(),
                        width=1.45,
                        opacity=0.58,
                    )
                )
    return VGroup(edges, *layers)


def _feature_stack(center, width, height, count=3):
    layers = VGroup()
    for index in reversed(range(count)):
        layer = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.025,
            stroke_color=INK_SOFT,
            stroke_width=2.10,
            fill_color=CAND_FILL,
            fill_opacity=1,
        )
        layer.move_to(center + index * (RIGHT * 0.026 + UP * 0.026))
        layers.add(layer)
    return layers


def make_cnn_icon():
    """Three progressively compressed convolutional feature-map stacks."""
    first = _feature_stack(LEFT * 0.65, width=0.22, height=0.44)
    second = _feature_stack(LEFT * 0.10, width=0.19, height=0.33)
    third = _feature_stack(RIGHT * 0.34, width=0.16, height=0.23)
    output = _node(RIGHT * 0.72, radius=0.052, fill=INK_SOFT)
    connectors = VGroup(
        _arrow(
            first[-1].get_right() + RIGHT * 0.025,
            second[-1].get_left() + LEFT * 0.025,
        ),
        _arrow(
            second[-1].get_right() + RIGHT * 0.025,
            third[-1].get_left() + LEFT * 0.025,
        ),
        _arrow(
            third[-1].get_right() + RIGHT * 0.025,
            output.get_left() + LEFT * 0.025,
        ),
    )
    return VGroup(first, second, third, connectors, output)


def make_attention_icon():
    """Token blocks converging through an attention-like processing block."""
    token_xs = (-0.57, -0.19, 0.19, 0.57)
    tokens = VGroup(
        *[
            RoundedRectangle(
                width=0.12,
                height=0.12,
                corner_radius=0.020,
                stroke_color=INK_SOFT,
                stroke_width=2.10,
                fill_color=CAND_FILL,
                fill_opacity=1,
            ).move_to([x, 0.20, 0])
            for x in token_xs
        ]
    )
    processor = RoundedRectangle(
        width=0.48,
        height=0.23,
        corner_radius=0.045,
        stroke_color=INK_SOFT,
        stroke_width=2.4,
        fill_color=SURFACE_2,
        fill_opacity=1,
    ).move_to([0, -0.055, 0])
    processor_marks = VGroup(
        *[
            Dot([x, y, 0], radius=0.016, color=INK_SOFT)
            for x in (-0.10, 0.10)
            for y in (-0.10, -0.01)
        ]
    )
    anchors = (0.16, -0.055, 0.055, -0.16)
    connections = VGroup(
        *[
            _line(
                token.get_bottom(),
                processor.get_top() + RIGHT * anchor,
                width=1.60,
                opacity=0.82,
            )
            for token, anchor in zip(tokens, anchors)
        ]
    )
    output = RoundedRectangle(
        width=0.13,
        height=0.13,
        corner_radius=0.020,
        stroke_color=INK_SOFT,
        stroke_width=2.10,
        fill_color=CAND_FILL,
        fill_opacity=1,
    ).move_to([0, -0.31, 0])
    output_flow = _arrow(
        processor.get_bottom() + DOWN * 0.018,
        output.get_top() + UP * 0.018,
        width=1.90,
        tip_length=0.055,
    )
    return VGroup(connections, tokens, processor, processor_marks, output_flow, output)


def _mini_model(center):
    panel = RoundedRectangle(
        width=0.34,
        height=0.16,
        corner_radius=0.030,
        stroke_color=INK_SOFT,
        stroke_width=2.10,
        fill_color=CAND_FILL,
        fill_opacity=1,
    ).move_to(center)
    marks = VGroup(
        Dot(center + LEFT * 0.085, radius=0.014, color=INK_SOFT),
        Dot(center, radius=0.014, color=INK_SOFT),
        Dot(center + RIGHT * 0.085, radius=0.014, color=INK_SOFT),
    )
    return VGroup(panel, marks)


def make_ensemble_icon():
    """Three independent models converging into one combined prediction."""
    models = VGroup(
        _mini_model([-0.61, 0.20, 0]),
        _mini_model([-0.61, 0.00, 0]),
        _mini_model([-0.61, -0.20, 0]),
    )
    aggregate = _node([0.22, 0, 0], radius=0.082)
    inputs = VGroup(
        *[
            _line(
                model[0].get_right() + RIGHT * 0.025,
                aggregate.get_left() + LEFT * 0.025,
                width=1.90,
            )
            for model in models
        ]
    )
    output = _node([0.69, 0, 0], radius=0.052, fill=INK_SOFT)
    output_flow = _arrow(
        aggregate.get_right() + RIGHT * 0.025,
        output.get_left() + LEFT * 0.025,
    )
    return VGroup(inputs, models, aggregate, output_flow, output)


CANDIDATE_DIAGRAM_BUILDERS = {
    "A": make_tree_icon,
    "B": make_mlp_icon,
    "C": make_cnn_icon,
    "D": make_attention_icon,
    "E": make_ensemble_icon,
}


def make_candidate_diagram(label):
    """Return the architecture diagram assigned to A-E, or ``None``."""
    builder = CANDIDATE_DIAGRAM_BUILDERS.get(label)
    return builder() if builder else None
