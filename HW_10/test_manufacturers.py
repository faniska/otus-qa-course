import pytest
import allure
from assets.fixtures.Browser import Browser
from assets.locators import AdminPage
from assets.page_objects import AdminPO, ManufacturerPO


class TestManufacturers(Browser):
    headless = False
    admin_url = 'http://opencart.xfanis.ru/admin/'

    @pytest.mark.menu
    @allure.description("""Check if specified menu item is active""")
    @allure.link(admin_url)
    def test_is_menu_active(self, wd):
        with allure.step('Login'):
            AdminPO(wd).login() \
                .hide_security_alert() \
                .open_catalog_item(AdminPage.manufacturers_link['text'])

        with allure.step('Check menu'):
            admin_menu = wd.find_element_by_css_selector(AdminPage.menu['css'])
            manufacturers_link = admin_menu.find_element_by_link_text(AdminPage.manufacturers_link['text'])
            manufacturers_li = manufacturers_link.find_element_by_xpath('..')
            assert manufacturers_li.get_attribute('class') == 'active'

    @pytest.mark.form
    @allure.description("""Try to add new manufacturer and test this functionality""")
    @allure.link(admin_url)
    def test_add_manufacturer(self, wd):
        with allure.step('Login'):
            AdminPO(wd).login() \
                .hide_security_alert() \
                .open_catalog_item(AdminPage.manufacturers_link['text'])

        with allure.step('Save form'):
            ManufacturerPO(wd) \
                .open_add_new_form() \
                .fill_test_data('Test Manufacturer') \
                .save()

            # Test is passed if there is success alert message
            alert_success = wd.find_element_by_css_selector(AdminPage.alert_success['css'])
            assert 'Success' in alert_success.text

    @pytest.mark.form
    @allure.description("""Try to edit new manufacturer and test this functionality""")
    @allure.link(admin_url)
    def test_edit_manufacturer(self, wd):
        with allure.step('Login'):
            AdminPO(wd).login() \
                .hide_security_alert() \
                .open_catalog_item(AdminPage.manufacturers_link['text'])

        with allure.step('Save form'):
            ManufacturerPO(wd) \
                .select_items_form() \
                .open_edit_form(7) \
                .fill_test_data(' Modified') \
                .save()

            # Test is passed if there is success alert message
            alert_success = wd.find_element_by_css_selector(AdminPage.alert_success['css'])
            assert 'Success' in alert_success.text

    @pytest.mark.form
    @allure.description("""Try to toggle sorting manufacturers list""")
    @allure.link(admin_url)
    def test_sort_order(self, wd):
        with allure.step('Login'):
            AdminPO(wd).login() \
                .hide_security_alert() \
                .open_catalog_item(AdminPage.manufacturers_link['text'])

        with allure.step('Toggle sorting'):
            ManufacturerPO(wd) \
                .select_items_form() \
                .toggle_sort_order()

            first_row_seq, last_row_seq = ManufacturerPO(wd).get_sequences()

            assert first_row_seq > last_row_seq

    @pytest.mark.style
    @allure.description("""Hover menu item and check if background has proper color""")
    @allure.link(admin_url)
    def test_row_bg_color(self, wd):
        with allure.step('Login'):
            AdminPO(wd).login() \
                .hide_security_alert() \
                .open_catalog_item(AdminPage.manufacturers_link['text'])
        with allure.step('Check style'):
            assert ManufacturerPO(wd).hover_and_get_bg(5) == 'rgba(245, 245, 245, 1)'
