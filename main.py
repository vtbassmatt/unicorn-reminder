import logging

log_format = '[%(asctime)s %(levelname)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(format=log_format, datefmt=date_format, level=logging.DEBUG)

import asyncio
import sys

from class_reminder import ClassReminder
from schedule import Schedule

scene = ClassReminder()

async def game_loop():
    TARGET_FPS = 15
    TIME_PER_FRAME = 1.0 / TARGET_FPS
    loop = asyncio.get_running_loop()
    loop.set_debug(True)
    BEGINNING_OF_TIME = loop.time()

    schedule = Schedule()

    while True:
        frame_start = loop.time()

        # take input
        event = schedule.get_next_event()
        if event:
            logging.debug(f"Event: {event['name']} ({event['kind']})")
            scene.handle_event(event, frame_start)

        # update
        await scene.update(frame_start, frame_start - BEGINNING_OF_TIME)

        # render
        await scene.render()

        # sleep
        sleep_time = frame_start + TIME_PER_FRAME - loop.time()
        if sleep_time > 0:
            await asyncio.sleep(sleep_time)


if __name__ == '__main__':
    try:
        asyncio.run(game_loop())
    except KeyboardInterrupt:
        scene.end()
        logging.debug('and we\'re out')
        sys.exit(0)
