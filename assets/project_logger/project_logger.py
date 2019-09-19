# -*- coding: utf-8 -*-
import datetime
import logging
import os


class ProjectLogger(object):
    def __init__(self, name=None):
        dirname = os.path.dirname(__file__)
        now = datetime.datetime.now()
        log_name = now.strftime("%Y-%m-%d") + '_test.log'
        log_path = os.path.join(dirname, 'logs', log_name)

        self.logger = logging.getLogger(name or __name__)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger
