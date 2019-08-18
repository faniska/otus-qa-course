import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions


@pytest.fixture(scope='module')
def browser(request):
    browser = request.config.getoption("--browser")
    url = request.config.getoption("--url")

    if browser.lower() == 'chrome':
        options = ChromeOptions()
        # options.add_argument("--headless")
        wd = webdriver.Chrome(options=options)
    elif browser.lower() == 'firefox':
        options = FirefoxOptions()
        # options.add_argument("--headless")
        wd = webdriver.Firefox(options=options)
    else:
        raise ValueError('--browser option can have chrome or firefox value')
    request.addfinalizer(wd.quit)

    wd.get(url)
    return wd


@pytest.fixture
def get_url(request):
    return request.config.getoption("--url")


def test_opencart_page(browser):
    """
    Check if main page contains correct title
    """
    assert browser.title == 'Your Store'


def test_search_field(browser):
    """
    Check if page contains search field
    """
    assert browser.find_element_by_id('search')


def test_shopping_cart_link(browser):
    """
    Check if page contains shopping cart link
    """
    assert browser.find_elements_by_css_selector('a[title="Shopping Cart"]')
