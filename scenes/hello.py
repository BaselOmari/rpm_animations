from manim import *


class Hello(Scene):
    """Smoke-test scene. Uses no LaTeX, so it renders without a TeX install."""

    def construct(self):
        title = Text("Manim is set up", font_size=48)
        square = Square(color=BLUE, fill_opacity=0.5)

        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        self.play(Create(square))
        self.play(Rotate(square, PI / 2), square.animate.set_color(TEAL))
        self.wait()


class HelloTex(Scene):
    """Same idea, but exercises the LaTeX pipeline (Tex/MathTex)."""

    def construct(self):
        formula = MathTex(r"e^{i\pi} + 1 = 0", font_size=72)
        self.play(Write(formula))
        self.play(formula.animate.set_color_by_gradient(BLUE, TEAL))
        self.wait()
