from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from assets.locators import AdminLogin, AdminPage
from .BasePO import BasePO
from assets.opencart import Credentials


class AdminPO(BasePO):
    items_form = None

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
        return self.open_catalog_item(AdminPage.products_link['text'])

    def open_manufactures(self):
        return self.open_catalog_item(AdminPage.manufacturers_link['text'])

    def open_catalog_item(self, link_text):
        self._click(AdminPage.catalog_link)
        try:
            wait = WebDriverWait(self.wd, 2)
            link = wait.until(
                expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, link_text))
            )
            link.click()
            return self

        except NoSuchElementException:
            assert False, 'Please fix the link text!'
        except TimeoutException:
            assert False, 'Timeout is raised! Please correct locator or increase waiting time'

    def select_all(self):
        self.items_form.find_element_by_css_selector(AdminPage.select_all_checkbox['css']).click()
        return self

    def open_add_new_form(self):
        self._click(AdminPage.button_add_new)
        return self

    def open_edit_form(self, number=1):
        index = number - 1
        buttons_edit = self.items_form.find_elements_by_css_selector(AdminPage.button_edit['css'])
        buttons_edit[index].click()
        return self

    def click_delete_button(self):
        self._click(AdminPage.button_delete)
        Alert(self.wd).accept()
        return self

    def save(self):
        self._click(AdminPage.button_save)
        return self
