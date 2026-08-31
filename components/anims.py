"""Small animation helpers shared by both videos."""

from manim import *


def dimmed(mob, opacity=0.18, **anim_kw):
    """Fade ``mob`` down without switching on fills that were transparent.

    ``Mobject.set_opacity`` sets fill *and* stroke opacity absolutely, so on a
    curve drawn with ``fill_opacity=0`` it paints in the shape between the curve
    and its chord — invisible on white, a grey wedge on black.  Scaling each
    submobject's existing opacities keeps zero at zero.
    """
    target = mob.copy()
    for m in target.family_members_with_points():
        m.set_stroke(opacity=m.get_stroke_opacity() * opacity)
        m.set_fill(opacity=m.get_fill_opacity() * opacity)
    return Transform(mob, target, **anim_kw)


def travel(mob, point, scale=1.0, vanish=False, **anim_kw):
    """Move a mobject to a point, optionally shrinking it out of sight."""
    anim = mob.animate.move_to(point)
    if scale != 1.0:
        anim = anim.scale(scale)
    if vanish:
        anim = anim.set_opacity(0)
    return anim
