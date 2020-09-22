import colorsys
import math
import random

import numpy

from random_dots import RandomDots
from scene import Scene
from events import EventKind
from unicorn import unicorn


class ClassReminder(Scene):
    def __init__(self):
        super().__init__(unicorn)
        self.mode = EventKind.NOTHING
        self.event_name = ''
        self.calm_state = RandomDots()

        self.crossfade = None
    
    def handle_event(self, event, current):
        old_mode = self.mode
        self.mode = event.get('kind', EventKind.NOTHING)
        self.event_name = event.get('name', '')

        # NB: if another event comes in before the crossfade finishes,
        # this will probably look like garbage
        if old_mode != self.mode:
            self.crossfade = (current, current + 2.0, old_mode)

    async def update(self, current, elapsed):
        dispatch = {
            EventKind.NOTHING: self.update_nothing,
            EventKind.ALERT: self.update_alert,
            EventKind.CALM: self.update_calm,
            EventKind.REMIND: self.update_reminder,
        }
        buffer = await dispatch[self.mode](current, elapsed)

        if self.crossfade:
            crossfade_time = min(1.0, (current - self.crossfade[0]) / (self.crossfade[1] - self.crossfade[0]))
            buffer2 = await dispatch[self.crossfade[2]](current, elapsed)
            buffer = self.lerp(buffer2, buffer, crossfade_time)

            if current > self.crossfade[1]:
                self.crossfade = None

        self.unicorn.set_buffer(buffer)
    
    async def update_nothing(self, current, elapsed):
        return numpy.zeros((16,16,3), dtype=int)
    
    async def update_alert(self, current, elapsed):
        buffer = numpy.zeros((16,16,3), dtype=int)
        for x in range(8):
            for y in range(8):
                buffer[x, y, 0] = self.unicorn.sin(elapsed - x - y, 6, 127)
                buffer[self.unicorn.width - x - 1, y, 0] = self.unicorn.sin(elapsed - x - y, 6, 127)
                buffer[x, self.unicorn.height - y - 1, 0] = self.unicorn.sin(elapsed - x - y, 6, 127)
                buffer[self.unicorn.width - x - 1, self.unicorn.height - y - 1, 0] = self.unicorn.sin(elapsed - x - y, 6, 127)
        return buffer

    async def update_calm(self, current, elapsed):
        await self.calm_state.update(current, elapsed)
        return self.calm_state.get_buffer()
    
    def _random_intensity(self):
        return random.randrange(16, 64) * 4 - 1

    async def update_reminder(self, current, elapsed):
        buffer = numpy.zeros((16,16,3), dtype=int)
        # from https://github.com/pimoroni/unicorn-hat-hd/blob/master/examples/rainbow.py
        step = current * 15.0
        for x in range(self.unicorn.width):
            for y in range(self.unicorn.height):
                dx = (math.sin(step / 20.0) * 15.0) + 7.0
                dy = (math.cos(step / 15.0) * 15.0) + 7.0
                sc = (math.cos(step / 10.0) * 10.0) + 16.0

                h = math.sqrt(math.pow(x - dx, 2) + math.pow(y - dy, 2)) / sc

                r, g, b = colorsys.hsv_to_rgb(h, 1, 1)

                r *= 255.0
                g *= 255.0
                b *= 255.0

                buffer[x, y, 0], buffer[x, y, 1], buffer[x, y, 2] = r, g, b
        
        return buffer
        
    def lerp(self, buffer1, buffer2, t):
        target = numpy.zeros((16,16,3), dtype=int)
        for x in range(16):
            for y in range(16):
                target[x, y, 0] = buffer1[x, y, 0] + t * (buffer2[x, y, 0] - buffer1[x, y, 0])
                target[x, y, 1] = buffer1[x, y, 1] + t * (buffer2[x, y, 1] - buffer1[x, y, 1])
                target[x, y, 2] = buffer1[x, y, 2] + t * (buffer2[x, y, 2] - buffer1[x, y, 2])
        
        return target