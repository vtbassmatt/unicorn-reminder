import random

import numpy

class RandomDots():
    def __init__(self):
        self.last_pixel = 0
        self.last_color_switch = 0
        self.color_index = -1
        self.buffer = numpy.zeros((16,16,3), dtype=int)
        self.switch_colors()
    
    def _random_intensity(self):
        return random.randrange(16, 64) * 4 - 1
    
    def switch_colors(self):
        self.color_index = random.choice(range(3))

    async def update(self, current, elapsed):
        if current - self.last_color_switch > 10:
            self.switch_colors()
            self.last_color_switch = current

        if current - self.last_pixel >= 0.2:
            x = random.randrange(0, 16)
            y = random.randrange(0, 16)
            self.buffer[x, y] = [0, 0, 0] # set pixel to black
            self.buffer[x, y, self.color_index] = self._random_intensity()
            self.last_pixel = current

    def get_buffer(self):
        return self.buffer.copy()