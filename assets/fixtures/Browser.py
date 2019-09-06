import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions


class Browser:
    headless = True

    @pytest.fixture
    def wd(self, request):
        browser = request.config.getoption("--browser")
        url = request.config.getoption("--url")
        timeout = request.config.getoption("--timeout", default=5, skip=True)
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
        print(f'Implicitly waiting: {timeout} second(s)')
        wd.implicitly_wait(int(timeout))
        request.addfinalizer(wd.quit)
        wd.get(url)
        return wd
