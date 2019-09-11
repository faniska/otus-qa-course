import os
import time

from assets.fixtures.Browser import Browser
from assets.locators import AdminPage
from assets.page_objects import DownloadPO, AdminPO


class TestUpload(Browser):
    headless = False

    def test_upload_file(self, wd):
        dirname = os.path.dirname(__file__)
        file_name = 'git-commit.png'
        file_path = os.path.join(dirname, file_name)

        AdminPO(wd).login() \
            .hide_security_alert() \
            .open_catalog_item(AdminPage.downloads_link['text'])

        DownloadPO(wd). \
            open_add_new_form(). \
            insert_upload_form(). \
            upload_file(file_path). \
            remove_upload_form(). \
            fill_test_data('Test Name'). \
            save()

        # Test is passed if there is success alert message
        alert_success = wd.find_element_by_css_selector(AdminPage.alert_success['css'])
        assert 'Success' in alert_success.text
