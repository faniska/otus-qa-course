import os
import urllib
import json
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, FirefoxProfile
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from browsermobproxy import Server, Client

from assets.project_logger import ProjectLogger


class Browser:
    headless = True
    use_proxy = False
    proxy = None

    @pytest.fixture
    def wd(self, request):
        browser = request.config.getoption("--browser")
        url = request.config.getoption("--url")
        timeout = request.config.getoption("--timeout", default=5, skip=True)
        self.use_proxy = eval(request.config.getoption("--use-proxy", default=False, skip=True))
        self.proxy = Proxy()
        if self.use_proxy:
            self.proxy.start()
        if browser.lower() == 'chrome':
            driver = self.chrome_browser()
        elif browser.lower() == 'firefox':
            driver = self.firefox_browser()
        elif browser.lower() == 'safari':
            driver = self.safari_browser()
        else:
            raise ValueError('--browser option can have chrome or firefox value')
        print(f'Implicitly waiting: {timeout} second(s)')

        driver.implicitly_wait(int(timeout))
        wd = EventFiringWebDriver(driver, WdListener())
        request.addfinalizer(wd.quit)
        wd.get(url)
        if self.use_proxy:
            self.proxy.stop()
        return wd

    def chrome_browser(self):
        options = ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        if self.use_proxy and self.proxy.client:
            url = urllib.parse.urlparse(self.proxy.client.proxy).path
            options.add_argument('--proxy-server={}'.format(url))
        return webdriver.Chrome(options=options)

    def firefox_browser(self):
        options = FirefoxOptions()
        profile = FirefoxProfile()

        if self.headless:
            options.add_argument("--headless")
        if self.use_proxy and self.proxy.client:
            profile.set_proxy(self.proxy.client.selenium_proxy())
        return webdriver.Firefox(options=options, firefox_profile=profile)

    def safari_browser(self):
        return webdriver.Safari()


class Proxy(object):
    client = None

    def __init__(self):
        self.project_logger = ProjectLogger('PROXY')
        self.server = Server(
            "/home/fanistgt/PycharmProjects/otus-qa-course/venv/bin/browsermob-proxy/bin/browsermob-proxy")

    def start(self):
        options = {
            'log_path': self.project_logger.proxy_log_path,
            'log_file': self.project_logger.proxy_log_file
        }
        self.server.start(options)
        self.client = self.server.create_proxy()
        self.client.new_har()

    def stop(self):
        har_file_path = os.path.join(self.project_logger.proxy_log_path, self.project_logger.proxy_har_file)
        with open(har_file_path, 'w') as har_file:
            har_file.write(json.dumps(self.client.har))
        self.server.stop()


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
