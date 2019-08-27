import time

import pytest

from assets.fixtures.Browser import Browser
from assets.locators import AdminLogin, AdminPage
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert


class TestOpencartProduct(Browser):
    headless = False

    login = 'Editor'
    pwd = '111222'

    product_title = 'Test Product'
    product_meta = 'Test Meta Title'
    product_model = 'Test Product Model'

    @pytest.fixture()
    def prepare_product_data(self, request):
        number = request.config.getoption("--number")
        self.product_title = self.product_title + ' - ' + str(number)
        self.product_meta = self.product_meta + ' - ' + str(number)
        self.product_model = self.product_model + ' - ' + str(number)

    @pytest.fixture()
    def admin_page_wd(self, wd, prepare_product_data):
        wd.find_element_by_css_selector(AdminLogin.input_username).send_keys(self.login)
        wd.find_element_by_css_selector(AdminLogin.input_password).send_keys(self.pwd)

        wd.find_element_by_css_selector(AdminLogin.button).click()
        wd.find_element_by_css_selector(AdminPage.button_close).click()
        return wd

    @pytest.fixture()
    def products_page_wd(self, admin_page_wd):
        catalog_link = admin_page_wd.find_element_by_css_selector(AdminPage.catalog_link)
        ActionChains(admin_page_wd).click(catalog_link).pause(1).perform()
        admin_page_wd.find_element_by_partial_link_text(AdminPage.products_link_text).click()
        return admin_page_wd

    def get_product_form_after_filter(self, products_page_wd):
        # Search added product to check if the product was added
        button_open_filter = products_page_wd.find_element_by_css_selector(AdminPage.button_open_filter)
        if button_open_filter.is_displayed():
            # If the filter form is hidden click to the button "Filter" to open it
            button_open_filter.click()

        filter_product = products_page_wd.find_element_by_css_selector(AdminPage.filter_product)
        filter_product.find_element_by_css_selector(AdminPage.filter_name).send_keys(self.product_title)
        filter_product.find_element_by_css_selector(AdminPage.filter_button).click()

        # if there is at least one edit button for particular product it means the product exists
        form_product = products_page_wd.find_element_by_css_selector(AdminPage.form_product)
        return form_product

    def test_add(self, products_page_wd):
        print("Test will add {}".format(self.product_title))

        # Click the button "Add new"
        products_page_wd.find_element_by_css_selector(AdminPage.button_add_new).click()

        # Fill in title and meta keys
        products_page_wd.find_element_by_css_selector(AdminPage.product_title).send_keys(self.product_title)
        products_page_wd.find_element_by_css_selector(AdminPage.product_meta_title).send_keys(self.product_meta)

        # Go to the tab "Data"
        nav_tabs = products_page_wd.find_element_by_css_selector(AdminPage.nav_tabs)
        nav_tabs.find_element_by_link_text(AdminPage.data_tab_text).click()

        # Fill in product model
        products_page_wd.find_element_by_css_selector(AdminPage.product_model).send_keys(self.product_model)

        # Click the button "Save"
        products_page_wd.find_element_by_css_selector(AdminPage.button_save).click()

        # if there is at least one edit button for particular product it means the product exists
        form_product = self.get_product_form_after_filter(products_page_wd)
        assert form_product.find_elements_by_css_selector(AdminPage.button_edit)

    def test_edit(self, products_page_wd):
        print("Test will modify {}".format(self.product_title))
        # Filter products and click to first edit button
        form_product = self.get_product_form_after_filter(products_page_wd)
        buttons_edit = form_product.find_elements_by_css_selector(AdminPage.button_edit)
        first_edit_button = buttons_edit[0]
        first_edit_button.click()
        # Fill in meta keywords and description
        products_page_wd.find_element_by_css_selector(AdminPage.product_meta_keys).send_keys('Meta Keywords Test')
        products_page_wd.find_element_by_css_selector(AdminPage.product_meta_desc).send_keys('Meta Description Test')
        # Click save button
        products_page_wd.find_element_by_css_selector(AdminPage.button_save).click()
        # Test is passed if there is success alert message
        alert_success = products_page_wd.find_element_by_css_selector(AdminPage.alert_success)
        assert 'Success' in alert_success.text

    def test_delete(self, products_page_wd):
        print("Test will delete {}".format(self.product_title))
        # Filter products
        form_product = self.get_product_form_after_filter(products_page_wd)
        # Click to the checkbox "select all"
        form_product.find_element_by_css_selector(AdminPage.select_all_checkbox).click()
        # Click the button "Delete"
        products_page_wd.find_element_by_css_selector(AdminPage.button_delete).click()
        Alert(products_page_wd).accept()
        # Test is passed if there is success alert message
        alert_success = products_page_wd.find_element_by_css_selector(AdminPage.alert_success)
        assert 'Success' in alert_success.text
