# -*- coding: utf-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions


class TestSeleniumServer:

    @pytest.fixture()
    def chrome_driver(self, request):
        wd = self.get_wd('chrome', ChromeOptions())
        request.addfinalizer(wd.quit)
        return wd

    @pytest.fixture()
    def firefox_driver(self, request):
        wd = self.get_wd('firefox', FirefoxOptions())
        request.addfinalizer(wd.quit)
        return wd

    @staticmethod
    def get_wd(browser_name, options):
        options.add_argument("--headless")
        return webdriver.Remote(
            command_executor='http://127.0.0.1:3344/wd/hub',
            desired_capabilities={'browserName': browser_name},
            options=options)

    def test_grid_firefox(self, firefox_driver):
        wd = firefox_driver
        wd.get("http://www.google.com")
        if "Google" not in wd.title:
            raise Exception("Unable to load google page!")

        elem = wd.find_element_by_name("q")
        elem.click()

    def test_grid_chrome(self, chrome_driver):
        wd = chrome_driver
        wd.get("http://www.google.com")
        if "Google" not in wd.title:
            raise Exception("Unable to load google page!")

        elem = wd.find_element_by_name("q")
        elem.click()

    def test_browser_stack(self):

        desired_cap = {
            'browser': 'Edge',
            'browser_version': '18.0',
            'os': 'Windows',
            'os_version': '10',
            'resolution': '1024x768',
            'name': 'Bstack-[Python] Sample Test'
        }

        bs_remote_driver = webdriver.Remote(
            command_executor='http://faniska1:ADvQqEuvq49emyE2rxL1@hub.browserstack.com:80/wd/hub',
            desired_capabilities=desired_cap)

        bs_remote_driver.get("http://www.google.com/")
        if "Google" not in bs_remote_driver.title:
            raise Exception("Unable to load google page!")
        elem = bs_remote_driver.find_element_by_name("q")
        elem.send_keys("BrowserStack")
        elem.submit()
        print(bs_remote_driver.title)
        bs_remote_driver.quit()
