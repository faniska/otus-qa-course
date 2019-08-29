from assets.fixtures.Browser import Browser
from selenium.webdriver import ActionChains


class TestDND(Browser):
    headless = False

    def test_dnd_papers_to_trash(self, wd):
        trash = wd.find_element_by_css_selector('div.trash')
        docs = wd.find_elements_by_css_selector('img.document')
        for doc in docs:
            ActionChains(wd).drag_and_drop(doc, trash).pause(1).perform()
