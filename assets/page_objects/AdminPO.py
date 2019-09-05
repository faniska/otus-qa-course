from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from assets.locators import AdminLogin, AdminPage
from .BasePO import BasePO
from assets.opencart import Credentials


class AdminPO(BasePO):
    def login(self):
        self._input(AdminLogin.input_username, Credentials.login)
        self._input(AdminLogin.input_password, Credentials.pwd)
        self._click(AdminLogin.button)
        return self

    def hide_security_alert(self):
        wait = WebDriverWait(self.wd, 2)
        locator = (By.CSS_SELECTOR, AdminPage.button_close['css'])
        button = wait.until(expected_conditions.presence_of_element_located(locator))
        button.click()
        return self

    def open_catalog(self):
        self._click(AdminPage.catalog_link)
        return self

    def open_products(self):
        try:
            wait = WebDriverWait(self.wd, 2)
            products_link = wait.until(
                expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, AdminPage.products_link['text']))
            )
            products_link.click()
            return True

        except NoSuchElementException:
            assert False, 'Please fix the products link text!'
        except TimeoutException:
            assert False, 'Timeout is raised! Please correct locator or increase waiting time'
