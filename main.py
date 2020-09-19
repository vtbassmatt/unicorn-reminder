import logging

log_format = '[%(asctime)s %(levelname)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(format=log_format, datefmt=date_format, level=logging.DEBUG)

import sys
import time

from red_dots import RedDots

scene = RedDots()

def game_loop():
    TARGET_FPS = 15
    TIME_PER_FRAME = 1.0 / TARGET_FPS
    BEGINNING_OF_TIME = time.monotonic()

    while True:
        frame_start = time.monotonic()

        # take input
        # pass

        # update
        scene.update(frame_start, frame_start - BEGINNING_OF_TIME)

        # render
        scene.render()

        # sleep
        sleep_time = frame_start + TIME_PER_FRAME - time.monotonic() 
        if sleep_time > 0:
            time.sleep(sleep_time)


if __name__ == '__main__':
    try:
        game_loop()
    except KeyboardInterrupt:
        scene.end()
        logging.debug('and we\'re out')
        sys.exit(0)
