"""The research search tree.

This is the persistent visual anchor across both videos: nodes are executed
solutions, edges are mutations (paper §2.2).  The tree is a plain ``VGroup`` so
it can be scaled / moved as one object between beats.

Layout is hand-authored (rather than auto-laid-out) so it matches Figure 1
exactly and never reflows under the viewer.
"""

from manim import *

from .node import SolutionNode, make_failed_node, make_tree_node
from .theme import EDGE_W, EDGE_W_FAINT, INK, INK_FAINT

# Figure 1 layout, in tree-local units, root at the origin.
LAYOUT = {
    "root": (0.00, 0.00),      # 0.44
    "l": (-1.75, -1.55),       # 0.51
    "r": (1.75, -1.55),        # 0.60
    "ll": (-2.85, -3.10),      # buggy node
    "lr": (-0.65, -3.10),      # 0.55
    "rr": (2.85, -3.10),       # 0.63, added by the RPM
}


def tree_edge(a, b, color=INK, stroke=EDGE_W, tip=0.24, gap=0.07):
    """Arrow from the rim of node ``a`` to the rim of node ``b``."""
    va, vb = a.get_center(), b.get_center()
    d = normalize(vb - va)
    start = va + d * (a.radius + gap)
    end = vb - d * (b.radius + gap)
    return Arrow(
        start,
        end,
        buff=0,
        color=color,
        stroke_width=stroke,
        tip_length=tip,
        max_tip_length_to_length_ratio=0.4,
        max_stroke_width_to_length_ratio=999,
    )


def make_tree_edge(a, b, faint=False):
    if faint:
        return tree_edge(a, b, color=INK_FAINT, stroke=EDGE_W_FAINT, tip=0.16)
    return tree_edge(a, b)


class SearchTree(VGroup):
    """Keyed collection of nodes + edges laid out per ``LAYOUT``."""

    def __init__(self, layout=None, unit=1.0, **kw):
        super().__init__(**kw)
        self.layout = dict(layout or LAYOUT)
        self.unit = unit
        self.nodes = {}
        self.edges = {}

    # -- construction -------------------------------------------------------
    def pos(self, key):
        x, y = self.layout[key]
        return np.array([x * self.unit, y * self.unit, 0.0])

    def place(self, key, node):
        node.move_to(self.pos(key))
        self.nodes[key] = node
        self.add(node)
        return node

    def add_score(self, key, score):
        return self.place(key, make_tree_node(score))

    def add_failed(self, key):
        return self.place(key, make_failed_node())

    def add_candidate_node(self, key, node):
        """Attach an already-built node (e.g. a candidate flying home)."""
        return self.place(key, node)

    def connect(self, pkey, ckey, faint=False):
        e = make_tree_edge(self.nodes[pkey], self.nodes[ckey], faint=faint)
        self.edges[(pkey, ckey)] = e
        self.add_to_back(e)
        return e

    # -- access -------------------------------------------------------------
    def __getitem__(self, key):
        return self.nodes[key]

    def edge(self, pkey, ckey):
        return self.edges[(pkey, ckey)]

    def node_index(self, key):
        return self.submobjects.index(self.nodes[key])

    # -- whole-tree moves ---------------------------------------------------
    def root_at(self, point, key="root"):
        """Position by a named node rather than by bounding box."""
        return self.shift(np.array(point, dtype=float) - self.nodes[key].get_center())


def retarget_tree(tree, scale, key, point):
    """Animation: scale the tree and park node ``key`` at ``point``.

    Positioning by an anchor node (not the bounding box) keeps the tree from
    lurching sideways whenever a new child is added.
    """
    idx = tree.node_index(key)
    tree.generate_target()
    tree.target.scale(scale)
    anchor = tree.target.submobjects[idx]
    tree.target.shift(np.array(point, dtype=float) - anchor.get_center())
    return MoveToTarget(tree)


def figure1_tree(with_rr=False):
    """The Figure 1 tree: 0.44 -> {0.51, 0.60}; 0.51 -> {buggy, 0.55}."""
    t = SearchTree()
    t.add_score("root", "0.44")
    t.add_score("l", "0.51")
    t.add_score("r", "0.60")
    t.add_failed("ll")
    t.add_score("lr", "0.55")
    for p, c in (("root", "l"), ("root", "r"), ("l", "ll"), ("l", "lr")):
        t.connect(p, c)
    if with_rr:
        t.add_score("rr", "0.63")
        t.connect("r", "rr")
    return t


def seed_tree():
    """Just the root, ready to be grown on-screen."""
    t = SearchTree()
    t.add_score("root", "0.44")
    return t
