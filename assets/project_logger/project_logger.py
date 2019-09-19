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

    def save_screenshot(self, driver):
        dirname = os.path.dirname(__file__)
        now = datetime.datetime.now()
        img_name = now.strftime("%Y-%m-%d_%H-%m-%S") + '_img.png'
        img_path = os.path.join(dirname, 'screenshots', img_name)
        driver.save_screenshot(img_path)

    def get_logger(self):
        return self.logger

    @property
    def proxy_log_path(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, 'logs')

    @property
    def proxy_log_file(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d") + '_proxy.log'

    @property
    def proxy_har_file(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d") + '_har.log'
