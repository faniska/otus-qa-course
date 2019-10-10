from assets.locators import AdminPage, ProductPage
from assets.page_objects import AdminPO


class ProductPO(AdminPO):

    def fill_test_data(self, title, meta_title, model):
        # Fill in title and meta keys
        self._input(AdminPage.product_title, title)
        self._input(AdminPage.product_meta_title, meta_title)

        # Go to the tab "Data"
        nav_tabs = self.wd.find_element_by_css_selector(AdminPage.nav_tabs['css'])
        nav_tabs.find_element_by_link_text(AdminPage.data_tab['text']).click()

        # Fill in product model
        self._input(AdminPage.product_model, model)

        return self

    def open_filter_form(self):
        button_open_filter = self.wd.find_element_by_css_selector(AdminPage.button_open_filter['css'])
        if button_open_filter.is_displayed():
            # If the filter form is hidden click to the button "Filter" to open it
            button_open_filter.click()

    def filter_products(self, search):
        # Search added product to check if the product was added
        self.open_filter_form()

        filter_product = self.wd.find_element_by_css_selector(AdminPage.filter_product['css'])
        filter_product.find_element_by_css_selector(AdminPage.filter_name['css']).send_keys(search)
        filter_product.find_element_by_css_selector(AdminPage.filter_button['css']).click()

        # if there is at least one edit button for particular product it means the product exists
        self.items_form = self.wd.find_element_by_css_selector(ProductPage.items_form['css'])
        return self
