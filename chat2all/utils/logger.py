# coding=utf8
#


"""
日志模块，初始化日志的格式
"""

import logging
import threading


from utils.config import config

_LOCALS = threading.local()


def getLogger(package_name):
    """ init logger instance """
    logger = getattr(_LOCALS, package_name, None)
    if logger is not None:
        return logger

    log_file = config.get('log_file')
    logger = logging.getLogger(package_name)
    hdlr = logging.FileHandler(log_file)
    formatter = '[%(asctime)s] Level:%(levelname)s Message:%(message)s', '%Y-%m-%d %a %H:%M:%S'
    formatter = logging.Formatter(*formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    setattr(_LOCALS, package_name, logger)
    return logger
