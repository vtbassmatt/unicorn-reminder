import logging
import sys
import random

from unicorn import unicorn

def main():
    from time import sleep
    unicorn.clear()
    while True:
        unicorn.set_pixel(random.randrange(0, 16), random.randrange(0, 16), random.randrange(16, 64) * 4 - 1, 0, 0)
        unicorn.show()
        sleep(.25)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    try:
        main()
    except KeyboardInterrupt:
        unicorn.off()
        logging.debug('\nand we\'re out\n')
        sys.exit(0)
