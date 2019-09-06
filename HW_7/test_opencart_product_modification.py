import pytest

from assets.fixtures.Browser import Browser
from assets.locators import AdminPage
from assets.opencart import Credentials
from assets.page_objects import AdminPO, ProductPO


class TestOpencartProduct(Browser, Credentials):
    headless = False

    product_title = 'Test Product'
    product_meta = 'Test Meta Title'
    product_model = 'Test Product Model'

    @pytest.fixture()
    def prepare_product_data(self, request):
        number = request.config.getoption("--number")
        self.product_title = self.product_title + ' - ' + str(number)
        self.product_meta = self.product_meta + ' - ' + str(number)
        self.product_model = self.product_model + ' - ' + str(number)

    def test_add(self, wd):
        print("Test will add {}".format(self.product_title))

        AdminPO(wd).login() \
            .hide_security_alert() \
            .open_catalog() \
            .open_products()

        ProductPO(wd).open_add_new_form() \
            .fill_test_data(self.product_title, self.product_meta, self.product_model) \
            .save()

        # if there is at least one edit button for particular product it means the product exists
        form_product = ProductPO(wd).filter_products(self.product_title).form_product
        assert form_product.find_elements_by_css_selector(AdminPage.button_edit['css'])

    def test_edit(self, wd):
        print("Test will modify {}".format(self.product_title))
        # Filter products and click to first edit button

        AdminPO(wd) \
            .login() \
            .hide_security_alert() \
            .open_catalog() \
            .open_products()

        ProductPO(wd) \
            .filter_products(self.product_title) \
            .open_edit_form()

        # Fill in meta keywords and description
        wd.find_element_by_css_selector(AdminPage.product_meta_keys['css']).send_keys('Meta Keywords Test')
        wd.find_element_by_css_selector(AdminPage.product_meta_desc['css']).send_keys('Meta Description Test')

        ProductPO(wd).save()
        # Test is passed if there is success alert message
        alert_success = wd.find_element_by_css_selector(AdminPage.alert_success['css'])
        assert 'Success' in alert_success.text

    def test_delete(self, wd):
        print("Test will delete {}".format(self.product_title))

        AdminPO(wd) \
            .login() \
            .hide_security_alert() \
            .open_catalog() \
            .open_products()

        ProductPO(wd) \
            .filter_products(self.product_title) \
            .select_all() \
            .click_delete_button()

        # Test is passed if there is success alert message
        alert_success = wd.find_element_by_css_selector(AdminPage.alert_success['css'])
        assert 'Success' in alert_success.text
