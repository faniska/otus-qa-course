import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from assets.fixtures.Browser import Browser
from assets.locators import AdminLogin, AdminPage
from assets.opencart import Credentials


class TestProductPageWaiting(Browser, Credentials):
    headless = False

    @pytest.fixture()
    def admin_page_wd(self, wd, request):
        timeout = request.config.getoption("--timeout")
        print(f'Implicitly waiting: {timeout} second(s)')
        wd.implicitly_wait(int(timeout))

        wd.find_element_by_css_selector(AdminLogin.input_username).send_keys(self.login)
        wd.find_element_by_css_selector(AdminLogin.input_password).send_keys(self.pwd)

        wd.find_element_by_css_selector(AdminLogin.button).click()
        # Waiting for the security alert block to close it
        wait = WebDriverWait(wd, 2)
        button = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, AdminPage.button_close)))
        button.click()
        return wd

    def test_product_page(self, admin_page_wd):
        # Click to Catalog
        admin_page_wd.find_element_by_css_selector(AdminPage.catalog_link).click()
        # Waiting 2 sec(s) for expanding the catalog menu and try to find link by text
        try:
            wait = WebDriverWait(admin_page_wd, 2)
            products_link = wait.until(
                expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, AdminPage.products_link_text))
            )
            products_link.click()
            assert admin_page_wd.find_element_by_css_selector(AdminPage.form_product)

        except NoSuchElementException:
            assert False, 'Please fix the products link text!'
        except TimeoutException:
            assert False, 'Timeout is raised! Please correct locator or increase waiting time'
