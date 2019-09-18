import datetime
import logging
import os

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class BasePO:
    base_url = 'http://opencart.xfanis.ru'
    path = '/'

    def __init__(self, wd):
        self._init_logger()
        self.wd = wd

    def _init_logger(self):
        dirname = os.path.dirname(__file__)
        now = datetime.datetime.now()
        log_name = now.strftime("%Y-%m-%d") + '_test.log'
        log_path = os.path.join(dirname, 'logs', log_name)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(fh)

    def __web_element(self, selector: dict, index: int, link_text: str = None):
        by = None
        if link_text:
            by = By.LINK_TEXT
        elif 'css' in selector.keys():
            by = By.CSS_SELECTOR
            selector = selector['css']
        return self.wd.find_elements(by, selector)[index]

    def _open(self):
        self.logger.debug('Open {}'.format(self.base_url + self.path))
        return self.wd.get(self.base_url + self.path)

    def _click(self, selector, index=0):
        self.logger.debug(f'Click to {selector}')
        ActionChains(self.wd).move_to_element(self.__web_element(selector, index)).click().perform()

    def _input(self, selector, value, index=0, clear=True):
        self.logger.debug(f'Input value "{value}" to {selector}')
        element = self.__web_element(selector, index)
        if clear:
            element.clear()
        element.send_keys(value)
