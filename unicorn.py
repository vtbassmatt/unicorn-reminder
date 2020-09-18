import logging
import sys
import random

try:
    import unicornhathd as unicorn
    logging.debug("the sparkles are real")
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicorn
    logging.debug("the sparkles are simulated")


def main():
    from time import sleep
    unicorn.clear()
    while True:
        unicorn.set_pixel(random.randrange(0, 16), random.randrange(0, 16), 255, 0, 0)
        unicorn.show()
        sleep(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    try:
        main()
    except KeyboardInterrupt:
        unicorn.off()
        logging.info('\nand we\'re out\n')
        sys.exit(0)