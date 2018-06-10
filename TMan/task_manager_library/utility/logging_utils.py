"""
This module implements methods to get logger configuration and create decorator for callbacks
"""

import logging
import config
from .utils import check_json_files, check_log_files


def logger(func):
    def _log(*args):

        try:
            get_logging_config("DEBUG")
            logging.info("Function {0} in module {1}".format(func.__name__, func.__module__))
            logging.debug("\t\tFunction: {0}\n\t\tArguments: {1}".format(func.__name__, args))
            result = func(*args)
            logging.debug("\t\t{0} return: {1}".format(func.__name__, result))
            return result
        except Exception as e:
            logging.error(e)
            raise e

    return _log


def get_logging_config(level_name):
    check_log_files(config.LOG_CONFIG['file'])
    logging.basicConfig(
        filename=config.LOG_CONFIG['file'],
        level=level_name,
        format=config.LOG_CONFIG['format'])
