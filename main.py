import logging
import random
import sys
import time

log_format = '[%(asctime)s %(levelname)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(format=log_format, datefmt=date_format, level=logging.DEBUG)

from unicorn import unicorn

def main():
    unicorn.clear()
    while True:
        unicorn.set_pixel(random.randrange(0, 16), random.randrange(0, 16), random.randrange(16, 64) * 4 - 1, 0, 0)
        unicorn.show()
        time.sleep(.25)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        unicorn.off()
        logging.debug('and we\'re out')
        sys.exit(0)
