"""The Figure 1 "Select Child Using RPM" composition.

Video 1 builds this up beat by beat; Video 2 opens on it.  Keeping the marks
and the builder in one place is what makes the two clips feel continuous.
"""

from manim import *

from .gpu import GPUBox
from .node import glow_halo
from .rpm import RPMBox, funnel_arrows
from .tree import figure1_tree

# --- candidate batch -------------------------------------------------------
CANDIDATE_LABELS = ["A", "B", "C", "D", "E"]
WINNER = 2  # candidate "C"

# --- stage marks -----------------------------------------------------------
TREE_SCALE = 0.70
TREE_R_AT = np.array([-3.25, 0.70, 0.0])   # where the 0.60 parent sits
RAIL_X = -1.35
RAIL_TOP, RAIL_BOTTOM = 2.20, -2.20
RAIL_R = 0.31
RPM_AT = np.array([1.95, 0.05, 0.0])
GPU_AT = np.array([5.40, 0.05, 0.0])
GPU_SCALE = 0.62


def decision_frame(with_gpu=True, with_rr=False):
    """Rebuild the exact frame Video 1 pauses on, as a dict of mobjects."""
    from .candidate import candidate_column

    tree = figure1_tree(with_rr=with_rr)
    tree.scale(TREE_SCALE)
    tree.shift(TREE_R_AT - tree["r"].get_center())

    rail = candidate_column(CANDIDATE_LABELS, RAIL_X, RAIL_TOP, RAIL_BOTTOM,
                            radius=RAIL_R)
    rpm = RPMBox("RPM").move_to(RPM_AT)
    funnel = funnel_arrows(rail, rpm.panel)

    from .tree import make_tree_edge

    stems = VGroup(*[make_tree_edge(tree["r"], c, faint=True) for c in rail])
    halo = glow_halo(tree["r"], pad=0.18)

    out = dict(tree=tree, rail=rail, rpm=rpm, funnel=funnel, stems=stems, halo=halo)
    if with_gpu:
        gpu = GPUBox().scale(GPU_SCALE).move_to(GPU_AT)
        out["gpu"] = gpu
    return out
