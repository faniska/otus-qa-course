from assets.fixtures.Browser import Browser
from assets.locators import AdminPage
from assets.page_objects import AdminPO, ManufacturerPO


class TestManufacturers(Browser):
    headless = False

    def test_is_menu_active(self, wd):
        AdminPO(wd).login() \
            .hide_security_alert() \
            .open_catalog_item(AdminPage.manufacturers_link['text'])

        admin_menu = wd.find_element_by_css_selector(AdminPage.menu['css'])
        manufacturers_link = admin_menu.find_element_by_link_text(AdminPage.manufacturers_link['text'])
        manufacturers_li = manufacturers_link.find_element_by_xpath('..')
        assert manufacturers_li.get_attribute('class') == 'active'

    def test_add_manufacturer(self, wd):
        AdminPO(wd).login() \
            .hide_security_alert() \
            .open_catalog_item(AdminPage.manufacturers_link['text'])

        ManufacturerPO(wd) \
            .open_add_new_form() \
            .fill_test_data('Test Manufacturer') \
            .save()

        # Test is passed if there is success alert message
        alert_success = wd.find_element_by_css_selector(AdminPage.alert_success['css'])
        assert 'Success' in alert_success.text

    def test_edit_manufacturer(self, wd):
        AdminPO(wd).login() \
            .hide_security_alert() \
            .open_catalog_item(AdminPage.manufacturers_link['text'])

        ManufacturerPO(wd) \
            .select_items_form() \
            .open_edit_form(7) \
            .fill_test_data(' Modified') \
            .save()

        # Test is passed if there is success alert message
        alert_success = wd.find_element_by_css_selector(AdminPage.alert_success['css'])
        assert 'Success' in alert_success.text

    def test_sort_order(self, wd):
        AdminPO(wd).login() \
            .hide_security_alert() \
            .open_catalog_item(AdminPage.manufacturers_link['text'])

        ManufacturerPO(wd) \
            .select_items_form() \
            .toggle_sort_order()

        first_row_seq, last_row_seq = ManufacturerPO(wd).get_sequences()

        assert first_row_seq > last_row_seq

    def test_row_bg_color(self, wd):
        AdminPO(wd).login() \
            .hide_security_alert() \
            .open_catalog_item(AdminPage.manufacturers_link['text'])

        assert ManufacturerPO(wd).hover_and_get_bg(5) == 'rgba(245, 245, 245, 1)'
