import logging
import random
import sys
import time

log_format = '[%(asctime)s %(levelname)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(format=log_format, datefmt=date_format, level=logging.DEBUG)

from unicorn import unicorn

def game_loop():
    TARGET_FPS = 15
    TIME_PER_FRAME = 1.0 / TARGET_FPS
    unicorn.clear()
    BEGINNING_OF_TIME = time.monotonic()

    while True:
        frame_start = time.monotonic()

        # take input
        # pass

        # update
        unicorn.set_pixel(random.randrange(0, 16), random.randrange(0, 16), random.randrange(16, 64) * 4 - 1, 0, 0)

        # render
        unicorn.show()

        # sleep
        sleep_time = frame_start + TIME_PER_FRAME - time.monotonic()
        if sleep_time > 0:
            time.sleep(sleep_time)


if __name__ == '__main__':
    try:
        game_loop()
    except KeyboardInterrupt:
        unicorn.off()
        logging.debug('and we\'re out')
        sys.exit(0)
