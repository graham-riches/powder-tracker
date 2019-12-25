# -*- coding: utf-8 -*-
"""
@brief logging functions for NRCS app
@author: Graham Riches
@date: Sun Dec  8 09:25:21 2019
@description functions to attach new logging handlers
"""

import logging
from datetime import datetime


class AppLogger:
    """ parent class to manage logging from multiple classes """
    def __init__(self, _logpath):
        self._logpath = _logpath
        self.print_log_header()
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)
        self._fh = logging.FileHandler(_logpath)
        self._fh.setLevel(logging.INFO)
        self._sh = logging.StreamHandler(logging.INFO)

    def print_log_header(self):
        with open(self._logpath, 'w') as logfile:
            block = '*******************************************************************\n'
            desc = '                POW TRACKER LOG\n'
            date = 'Date: {}\n'.format(datetime.now())
            logfile.writelines(block)
            logfile.writelines(block)
            logfile.writelines(desc)
            logfile.writelines(date)
            logfile.writelines(block)
            logfile.writelines(block)


def attach_logger(_logfile, _handler, _log_level):
    logger = logging.getLogger(_handler)
    logger.setLevel(_log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(_logfile)
    fh.setLevel(_log_level)
    sh = logging.StreamHandler()
    sh.setLevel(_log_level)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    if not (len(logger.handlers)):
        logger.addHandler(sh)
        logger.addHandler(fh)
    return logger
