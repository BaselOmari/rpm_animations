"""Reusable pieces for the AI Research Preference Model animations.

Figure 1 of "AI Research Preference Models", re-voiced for a black ground in
Meta house style (Optimistic type, Meta blue as the single loud accent):

    green  executed solution with a validation score
    red    executed solution that failed / is buggy
    grey   candidate mutation that has NOT been executed
    blue   the candidate the RPM selected
"""

from .agent import AgentBox, make_agent_box
from .anims import dimmed, travel
from .base import RPMMovingScene, RPMScene
from .candidate import (
    CandidateCard,
    candidate_column,
    make_candidate_card,
    plan_code_stack,
)
from .candidate_diagrams import (
    make_attention_icon,
    make_candidate_diagram,
    make_cnn_icon,
    make_ensemble_icon,
    make_mlp_icon,
    make_tree_icon,
)
from .figure1 import (
    CANDIDATE_LABELS,
    GPU_SCALE,
    RAIL_BOTTOM,
    RAIL_R,
    RAIL_TOP,
    RAIL_X,
    TREE_SCALE,
    TREE_R_AT,
    WINNER,
    decision_frame,
)
from .figure1 import GPU_AT as GPU_DECIDE_AT
from .figure1 import RPM_AT as RPM_DECIDE_AT
from .gpu import Clock, GPUBox, ProgressBar, SandboxBox, make_gpu_box, make_sandbox_box
from .labels import (
    BOTTOM_Y,
    FIGURE1_STAGES,
    TOP_Y,
    StepBadge,
    annotation,
    caption,
    down_chain,
    hero,
    highlight_plate,
    pill,
    repeat_arc,
    stage_strip,
    step_column,
    two_tone,
)
from .node import (
    SolutionNode,
    glow_halo,
    make_candidate,
    make_failed_node,
    make_selected,
    make_tree_node,
)
from .rpm import (
    MatchUp,
    RPMBox,
    crossed_out,
    fan_arrows,
    flow_arrow,
    funnel_arrows,
    make_rpm_box,
    tournament_ladder,
)
from .theme import *  # noqa: F401,F403
from .tree import (
    LAYOUT,
    SearchTree,
    figure1_tree,
    make_tree_edge,
    retarget_tree,
    seed_tree,
    tree_edge,
)
