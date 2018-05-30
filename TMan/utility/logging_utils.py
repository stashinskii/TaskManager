import logging
import config


LEVELS = ["DEBUG", "INFO", "OFF"]


def logger(func):
    def _log(*args, **kwargs):
        try:
            logging.info("Function: {}".format(func.__name__))
            logging.debug("\t\tFunction: {0}\n\t\tArguments: {1}".format(func.__name__, args))
            result = func(*args, **kwargs)
            logging.debug("\t\t{0} return: {1}".format(func.__name__, result))
            return result
        except Exception as e:
            logging.error(e)
            raise e
    return _log


def get_logging_config(level_name):
    logging.basicConfig(
        filename=config.LOG_CONFIG['file'],
        level=level_name,
        format=config.LOG_CONFIG['format'])
