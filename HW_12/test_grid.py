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
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities={'browserName': browser_name},
            options=options)

    def test_grid(self, firefox_driver):
        wd = firefox_driver
        wd.get("http://www.google.com")
        if "Google" not in wd.title:
            raise Exception("Unable to load google page!")

        elem = wd.find_element_by_name("q")
        elem.click()
