import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions


class Browser:
    headless = True

    @pytest.fixture
    def wd(self, request):
        browser = request.config.getoption("--browser")
        url = request.config.getoption("--url")

        if browser.lower() == 'chrome':
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            wd = webdriver.Chrome(options=options)
        elif browser.lower() == 'firefox':
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            wd = webdriver.Firefox(options=options)
        elif browser.lower() == 'safari':
            wd = webdriver.Safari()
        else:
            raise ValueError('--browser option can have chrome or firefox value')
        request.addfinalizer(wd.quit)

        wd.get(url)
        return wd
