import math
import random

from unicorn import unicorn


class Scene:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.unicorn.clear()
        self.last_pixel = 0

    def update(self, current, elapsed):
        if current - self.last_pixel >= 0.1:
            self.unicorn.set_pixel(
                random.randrange(0, 16),
                random.randrange(0, 16),
                random.randrange(16, 64) * 4 - 1,
                0,
                0,
            )

            self.last_pixel = current
        
        heartbeat = math.floor((math.sin(elapsed) + 1.0) * 127)
        self.unicorn.set_pixel(
            0,
            0,
            0,
            0,
            heartbeat,
        )

    def render(self):
        self.unicorn.show()

    def end(self):
        self.unicorn.off()


scene = Scene(unicorn)
