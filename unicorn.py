import logging

try:
    import unicornhathd as unicorn
    logging.debug("the sparkles are real")
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicorn
    logging.debug("the sparkles are simulated")
