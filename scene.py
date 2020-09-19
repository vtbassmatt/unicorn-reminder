import random

from unicorn import unicorn


class Scene:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.unicorn.clear()

    def update(self, current, elapsed):
        self.unicorn.set_pixel(
            random.randrange(0, 16),
            random.randrange(0, 16),
            random.randrange(16, 64) * 4 - 1,
            0,
            0,
        )

    def render(self):
        self.unicorn.show()

    def end(self):
        self.unicorn.off()


scene = Scene(unicorn)
