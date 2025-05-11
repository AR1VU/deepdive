from manim import *

f = open("explanation.txt", "w", encoding="utf-8")
f.write("""Saying Hello with Manim

This animation visually demonstrates a simple "Hello, World!" using the Manim animation engine.

The title is introduced, followed by clearly displayed 'Hello, World!' text in the center of the screen. A decorative box frames the greeting text, and the animation closes gracefully.

This example shows how text and shapes can be combined to create clear and welcoming animations.
""")
f.close()

class SayHello(Scene):
    def construct(self):
        # Title
        title = Text("Hello Animation", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Main hello message
        hello_text = Text("Hello, World!", font_size=64, color=YELLOW)
        hello_box = SurroundingRectangle(hello_text, color=GREEN, buff=0.5)

        # Center on screen and ensure no overlap
        group = VGroup(hello_text, hello_box)
        group.move_to(ORIGIN)

        self.play(Create(hello_box))
        self.play(Write(hello_text))
        self.wait(2)

        # Decorate with a small dot at the lower right (demonstrate placement)
        dot = Dot(point=hello_box.get_corner(DR) + 0.3 * DR, color=RED)
        self.play(Create(dot))
        self.wait(1)

        # Cleanup before ending
        self.play(FadeOut(*self.mobjects))