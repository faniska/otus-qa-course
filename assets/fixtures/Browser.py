import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

from assets.project_logger import ProjectLogger


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
            driver = webdriver.Chrome(options=options)
        elif browser.lower() == 'firefox':
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        elif browser.lower() == 'safari':
            driver = webdriver.Safari()
        else:
            raise ValueError('--browser option can have chrome or firefox value')
        print(f'Implicitly waiting: {timeout} second(s)')

        driver.implicitly_wait(int(timeout))
        wd = EventFiringWebDriver(driver, WdListener())
        request.addfinalizer(wd.quit)
        wd.get(url)
        return wd


class WdListener(AbstractEventListener):
    def __init__(self):
        self.project_logger = ProjectLogger('DRIVER')
        self.logger = self.project_logger.logger

    def before_find(self, by, value, driver):
        self.logger.debug(f'Before find by {by}: {value}')

    def after_find(self, by, value, driver):
        self.logger.debug(f'After find by {by}: {value}')

    def on_exception(self, exception, driver):
        self.project_logger.save_screenshot(driver)
        self.logger.error(exception)
