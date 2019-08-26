import time

import pytest

from assets.fixtures.Browser import Browser
from assets.locators import AdminLogin, AdminPage
from selenium.webdriver import ActionChains


class TestOpencartProduct(Browser):
    login = 'Editor'
    pwd = '111222'

    product_title = 'Test Product'
    product_meta = 'Test Meta Key'
    product_model = 'Test Product Model'

    @pytest.fixture()
    def prepare_product_data(self, request):
        number = request.config.getoption("--number")
        self.product_title = self.product_title + ' - ' + str(number)
        self.product_meta = self.product_meta + ' - ' + str(number)
        self.product_model = self.product_model + ' - ' + str(number)

    @pytest.fixture()
    def admin_page(self, wd, prepare_product_data):
        wd.find_element_by_css_selector(AdminLogin.input_username).send_keys(self.login)
        wd.find_element_by_css_selector(AdminLogin.input_password).send_keys(self.pwd)

        wd.find_element_by_css_selector(AdminLogin.button).click()
        wd.find_element_by_css_selector(AdminPage.button_close).click()
        return wd

    @pytest.fixture()
    def products_page(self, admin_page):
        catalog_link = admin_page.find_element_by_css_selector(AdminPage.catalog_link)
        ActionChains(admin_page).click(catalog_link).pause(1).perform()
        admin_page.find_element_by_partial_link_text(AdminPage.products_link_text).click()
        return admin_page

    def test_add(self, products_page):
        print("Test will add {}".format(self.product_title))

        # Click the button "Add new"
        products_page.find_element_by_css_selector(AdminPage.button_add_new).click()

        # Fill in title and meta keys
        products_page.find_element_by_css_selector(AdminPage.product_title).send_keys(self.product_title)
        products_page.find_element_by_css_selector(AdminPage.product_meta_key).send_keys(self.product_meta)

        # Go to the tab "Data"
        nav_tabs = products_page.find_element_by_css_selector(AdminPage.nav_tabs)
        nav_tabs.find_element_by_link_text(AdminPage.data_tab_text).click()

        # Fill in product model
        products_page.find_element_by_css_selector(AdminPage.product_model).send_keys(self.product_model)

        # Click the button "Save"
        products_page.find_element_by_css_selector(AdminPage.button_save).click()

        # Search added product to check if the product was added
        filter_product = products_page.find_element_by_css_selector(AdminPage.filter_product)
        filter_product.find_element_by_css_selector(AdminPage.filter_name).send_keys(self.product_title)
        filter_product.find_element_by_css_selector(AdminPage.filter_button).click()

        # if there is at least one edit button for particular product it means the product exists
        form_product = products_page.find_element_by_css_selector(AdminPage.form_product)
        assert form_product.find_elements_by_css_selector(AdminPage.button_edit)

    def test_edit(self, admin_page):
        pass

    def test_delete(self, admin_page):
        pass
