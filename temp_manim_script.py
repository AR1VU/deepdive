from manim import *

f = open("explanation.txt", "w", encoding="utf-8")
f.write("""The Chain Rule Explained

The chain rule is a fundamental formula in calculus for finding the derivative of a composite function. If you have two functions, f and g, and you create a new function by composing them (i.e., h(x) = f(g(x))), the chain rule gives you a way to differentiate h in terms of f and g.

The chain rule formula states:
If h(x) = f(g(x)), then h'(x) = f'(g(x)) × g'(x).
This means you differentiate the outer function (f) evaluated at the inner function (g(x)), and multiply it by the derivative of the inner function (g).

WHY use the chain rule?

Not all functions are simple—the chain rule is essential when you have nested, or composite, functions, like sin(x^2) or e^{3x+1}.

EXAMPLE:
Let’s differentiate h(x) = (3x + 1)^4.
  Set f(u) = u^4 and g(x) = 3x + 1.
  By the chain rule:
    h'(x) = f'(g(x)) × g'(x) = 4(3x + 1)^3 × 3 = 12(3x + 1)^3

The chain rule is used constantly in calculus, physics, engineering, and many applied sciences.
""")
f.close()

class ChainRuleExplanation(Scene):
    def construct(self):
        # Title Scene
        title = Text("The Chain Rule in Calculus", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Chain Rule Introduction
        intro = Text("How to Differentiate Composite Functions", font_size=34)
        self.play(Write(intro))
        self.wait(2)
        self.play(FadeOut(intro))

        # Chain Rule Formula Visualized
        self.show_chain_rule_formula()
        self.wait(1)

        # Chain Rule Intuitive Diagram
        self.show_chain_rule_diagram()
        self.wait(1)

        # Chain Rule Example: (3x + 1)^4
        self.chain_rule_example()
        self.wait(1)

        # Clean up end
        self.play(FadeOut(*self.mobjects))
    
    def show_chain_rule_formula(self):
        # Displaying h(x) = f(g(x))
        eq1 = MathTex("h(x) = f(g(x))", font_size=42)
        eq2 = MathTex("h'(x) = f'(g(x)) \\cdot g'(x)", font_size=42).next_to(eq1, DOWN, buff=0.7)

        explanation = VGroup(
            Text("The chain rule formula:", font_size=30).next_to(eq1, UP, buff=0.7),
            eq1,
            eq2
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(ORIGIN)

        self.play(Write(explanation))
        self.wait(2)
        self.play(FadeOut(explanation))

    def show_chain_rule_diagram(self):
        # Visualize the flow: x --> g(x) --> f(g(x))
        start = Dot(color=YELLOW).shift(LEFT*4)
        x_label = Text("x", font_size=28).next_to(start, DOWN, buff=0.2)

        g_box = Rectangle(width=1.4, height=0.8, color=GREEN).next_to(start, RIGHT, buff=1.5)
        g_label = Text("g(x)", font_size=28).move_to(g_box)
        
        f_box = Rectangle(width=1.4, height=0.8, color=BLUE).next_to(g_box, RIGHT, buff=2)
        f_label = Text("f", font_size=28).move_to(f_box)

        arrow1 = Arrow(start.get_right(), g_box.get_left(), buff=0.05, color=WHITE)
        arrow2 = Arrow(g_box.get_right(), f_box.get_left(), buff=0.05, color=WHITE)
        
        h_result = Dot(color=RED).next_to(f_box, RIGHT, buff=1.7)
        h_label = Text("h(x) = f(g(x))", font_size=28).next_to(h_result, DOWN, buff=0.2)
        arrow3 = Arrow(f_box.get_right(), h_result.get_left(), buff=0.05, color=WHITE)

        allobjs = VGroup(
            start, x_label, arrow1, g_box, g_label, arrow2, f_box, f_label, arrow3, h_result, h_label
        )

        self.play(FadeIn(start), Write(x_label))
        self.play(Create(arrow1), FadeIn(g_box), Write(g_label))
        self.play(Create(arrow2), FadeIn(f_box), Write(f_label))
        self.play(Create(arrow3), FadeIn(h_result), Write(h_label))
        self.wait(1)

        # Add derivative indicators
        dgdx = MathTex("g'(x)", font_size=26, color=GREEN).next_to(arrow1, UP, buff=0.08)
        dfdg = MathTex("f'(g(x))", font_size=26, color=BLUE).next_to(arrow2, UP, buff=0.08)
        product = MathTex("h'(x) = f'(g(x)) \\cdot g'(x)", font_size=32, color=YELLOW).to_edge(DOWN, buff=0.6)
        self.play(Write(dgdx), Write(dfdg))
        self.wait(0.5)
        self.play(Write(product))
        self.wait(2)

        self.play(FadeOut(allobjs), FadeOut(dgdx), FadeOut(dfdg), FadeOut(product))

    def chain_rule_example(self):
        # Show the example: h(x) = (3x + 1)^4
        example_title = Text("Example: Differentiate h(x) = (3x + 1)^4", font_size=34, color=YELLOW).to_edge(UP, buff=0.7)
        self.play(Write(example_title))

        h_def = MathTex("h(x) = (3x + 1)^4", font_size=40).next_to(example_title, DOWN, buff=0.7)        
        self.play(Write(h_def))
        self.wait(0.8)

        # Break into f and g
        left = MathTex("\\text{Let } f(u) = u^4", font_size=32).next_to(h_def, DOWN, aligned_edge=LEFT, buff=1.0).shift(1.5*LEFT)
        right = MathTex("g(x) = 3x + 1", font_size=32).next_to(left, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(left))
        self.wait(0.6)
        self.play(Write(right))
        self.wait(1.2)

        # Show derivatives
        fprime = MathTex("f'(u) = 4u^3", font_size=32).next_to(left, RIGHT, buff=2.3)
        gprime = MathTex("g'(x) = 3", font_size=32).next_to(right, RIGHT, buff=2.2)
        self.play(Write(fprime), Write(gprime))
        self.wait(1.2)

        # Show chain rule application step
        step1 = MathTex("h'(x) = f'(g(x)) \\cdot g'(x)", font_size=36).to_edge(DOWN, buff=1.9)
        self.play(Write(step1))
        self.wait(0.8)

        # Substitute g(x) and g'(x) in
        step2 = MathTex("= 4\\left(3x + 1\\right)^3 \\cdot 3", font_size=36).next_to(step1, DOWN, buff=0.4)
        self.play(Write(step2))
        self.wait(0.8)

        # Final simplified
        step3 = MathTex("= 12\\left(3x + 1\\right)^3", font_size=36, color=GREEN).next_to(step2, DOWN, buff=0.3)
        self.play(Write(step3))
        self.wait(2)

        # Clean up
        self.play(
            FadeOut(example_title), FadeOut(h_def), FadeOut(left), FadeOut(right),
            FadeOut(fprime), FadeOut(gprime), FadeOut(step1), FadeOut(step2), FadeOut(step3)
        )