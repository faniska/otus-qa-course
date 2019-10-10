from assets.fixtures.Browser import Browser
from assets.locators import ProductPage
from assets.opencart import Credentials

from assets.page_objects import AdminPO


class TestProductPageWaiting(Browser, Credentials):
    headless = False

    def test_product_page(self, wd):
        AdminPO(wd).login() \
            .hide_security_alert() \
            .open_catalog()

        assert AdminPO(wd).open_products() and wd.find_element_by_css_selector(ProductPage.items_form['css'])
