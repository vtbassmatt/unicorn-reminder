import logging
import math

try:
    import unicornhathd
    logging.debug("🦄 the sparkles are real")
    _REAL_UNICORN_HAT = True
except ImportError:
    from unicorn_hat_sim import unicornhathd
    logging.debug("🦄 the sparkles are simulated")
    _REAL_UNICORN_HAT = False

class Unicorn:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.width, self.height = unicorn.get_shape()
    
    def set_pixel(self, x, y, r, g, b):
        self.unicorn.set_pixel(x, y, r, g, b)
    
    def set_buffer(self, buffer):
        if _REAL_UNICORN_HAT:
            self.unicorn._buf = buffer
        else:
            for x in range(16):
                for y in range(16):
                    self.unicorn.set_pixel(
                        x,
                        y,
                        buffer[x][y][0],
                        buffer[x][y][1],
                        buffer[x][y][2]
                    )
    
    def show(self):
        self.unicorn.show()

    def clear(self):
        self.unicorn.clear()

    def off(self):
        self.unicorn.off()
    
    def sin(self, elapsed, frequency=1, amplitude=127, offset=0):
        return (math.sin(frequency * elapsed + offset) + 1.0) * amplitude


unicorn = Unicorn(unicornhathd)