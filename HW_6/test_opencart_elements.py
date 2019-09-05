import time

from selenium.webdriver import ActionChains

from assets.fixtures.Browser import Browser
from assets.locators import AdminLogin, MainPage, ProductCategory, ProductPage


class TestOpencartElements(Browser):

    def test_main_page(self, wd):
        """
        Check if all elements are in the main page
        """
        print(wd.title)
        assert wd.find_element_by_css_selector(MainPage.header['css']), 'header not found'
        assert wd.find_element_by_css_selector(MainPage.menu_items['css']), 'menu_items not found'
        assert wd.find_element_by_css_selector(MainPage.banner['css']), 'banner not found'
        assert wd.find_element_by_css_selector(MainPage.footer['css']), 'footer not found'
        assert wd.find_element_by_css_selector(MainPage.search['css']), 'thumbnails not found'

    def test_product_page(self, wd):
        """
        Click to banner to open product page and test elements
        """
        wd.find_element_by_css_selector(MainPage.banner['css']).click()
        print(wd.title)
        assert wd.find_elements_by_css_selector(ProductPage.thumbnails['css']), 'thumbnails not found'
        assert wd.find_elements_by_css_selector(ProductPage.product_title['css']), 'product_title not found'
        assert wd.find_elements_by_css_selector(ProductPage.page_title['css']), 'page_title not found'
        assert wd.find_elements_by_css_selector(ProductPage.description_tab['css']), 'description_tab not found'
        assert wd.find_elements_by_css_selector(ProductPage.cart_button['css']), 'cart_button not found'

    def test_product_category(self, wd):
        """
        Go through main menu items, click to first "Show All" item and test product category elements
        :param wd:
        :return:
        """
        menu_items = wd.find_elements_by_css_selector(MainPage.menu_items['css'])
        for menu_item in menu_items:
            ActionChains(wd).move_to_element(menu_item).pause(0.5).perform()
            links = menu_item.find_elements_by_css_selector(MainPage.menu_show_all['css'])
            if links:
                links[0].click()
                break

        assert wd.find_elements_by_css_selector(ProductCategory.product_grid['css']), 'product_grid not found'
        assert wd.find_elements_by_css_selector(ProductCategory.input_sort['css']), 'input_sort not found'
        assert wd.find_elements_by_css_selector(ProductCategory.input_limit['css']), 'input_limit not found'
        assert wd.find_elements_by_css_selector(ProductCategory.wish_list_button['css']), 'wish_list_button not found'

    def test_admin_login(self, wd):
        """
        Check if the login page shows error alert when login or password are incorrect
        """
        wd.find_element_by_css_selector(AdminLogin.input_username['css']).send_keys('Admin')
        wd.find_element_by_css_selector(AdminLogin.input_password['css']).send_keys('Test')
        wd.find_element_by_css_selector(AdminLogin.button['css']).click()
        assert wd.find_elements_by_css_selector(AdminLogin.error_alert['css'])






