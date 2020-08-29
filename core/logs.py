"""
    configure log output
    usage:
        import logs

        logger = logs.get_logger(__name__)
        logger.info("message")
        logger.debug("message")
"""
import logging
from core import settings


def get_logger(name):

    logger = logging.getLogger(name)
    log_level = { 'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.error
                }.get(settings.loglevel.lower(), logging.WARNING)
    logger.setLevel(log_level)

    fh_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    ch_formatter = logging.Formatter('%(name)s %(levelname)s: %(message)s')
    
    # file
    if settings.logfile:
        fh = logging.FileHandler(settings.logfile)
        fh.setLevel(log_level)
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

    # console
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)

    return logger

