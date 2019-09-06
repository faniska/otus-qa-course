from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class BasePO:
    base_url = 'http://opencart.xfanis.ru'
    path = '/'

    def __init__(self, wd):
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
        return self.wd.get(self.base_url + self.path)

    def _click(self, selector, index=0):
        ActionChains(self.wd).move_to_element(self.__web_element(selector, index)).click().perform()

    def _input(self, selector, value, index=0, clear=True):
        element = self.__web_element(selector, index)
        if clear:
            element.clear()
        element.send_keys(value)
