from assets.fixtures.Browser import Browser


class TestOpencart(Browser):

    def test_opencart_page(self, wd):
        """
        Check if main page contains correct title
        """
        assert wd.title == 'Your Store'

    def test_search_field(self, wd):
        """
        Check if page contains search field
        """
        assert wd.find_element_by_id('search')

    def test_shopping_cart_link(self, wd):
        """
        Check if page contains shopping cart link
        """
        assert wd.find_elements_by_css_selector('a[title="Shopping Cart"]')
