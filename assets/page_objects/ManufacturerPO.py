from selenium.webdriver import ActionChains

from assets.page_objects import AdminPO
from assets.locators.ManufacturerPage import ManufacturerPage


class ManufacturerPO(AdminPO):
    def fill_test_data(self, title, clear=False):
        self._input(ManufacturerPage.input_name, title, clear=clear)
        return self

    def select_items_form(self):
        self.items_form = self.wd.find_element_by_css_selector(ManufacturerPage.items_form['css'])
        return self

    def toggle_sort_order(self):
        sort_order = self.items_form.find_element_by_link_text(ManufacturerPage.sort_order['text'])
        sort_order.click()
        return self

    def get_sequences(self):
        item_rows = self.wd.find_elements_by_css_selector(ManufacturerPage.item_row['css'])

        first_row = item_rows[0]
        last_row = item_rows[-1]

        first_row_seq = int(first_row.find_elements_by_css_selector('td')[2].text)
        last_row_seq = int(last_row.find_elements_by_css_selector('td')[2].text)
        return first_row_seq, last_row_seq

    def hover_and_get_bg(self, number=1):
        index = number - 1
        item_rows = self.wd.find_elements_by_css_selector(ManufacturerPage.item_row['css'])
        ActionChains(self.wd).move_to_element(item_rows[index]).perform()
        return item_rows[index].value_of_css_property('background-color')
