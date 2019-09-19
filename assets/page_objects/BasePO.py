from selenium.webdriver.common.by import By

from assets.project_logger import ProjectLogger


class BasePO:
    base_url = 'http://opencart.xfanis.ru'
    path = '/'

    def __init__(self, wd):
        self.logger = ProjectLogger('PAGE_OBJECT').logger
        self.wd = wd

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
        self.__web_element(selector, index).click()

    def _input(self, selector, value, index=0, clear=True):
        self.logger.debug(f'Input value "{value}" to {selector}')
        element = self.__web_element(selector, index)
        if clear:
            element.clear()
        element.send_keys(value)
