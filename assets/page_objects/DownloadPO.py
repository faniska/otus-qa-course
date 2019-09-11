from assets.locators import DownloadsPage
from assets.page_objects import AdminPO


class DownloadPO(AdminPO):
    def insert_upload_form(self):
        self.wd.execute_script("""
        let form = document.createElement('form');
        form.id = 'form-upload';
        form.method = 'post';
        form.style.display = 'block';
        form.enctype = 'multipart/form-data';
    
        const file_input = document.createElement('input');
        file_input.type = 'file';
        file_input.name = 'file';
        form.appendChild(file_input);
        
        const body = document.getElementsByTagName('body')[0]
        body.insertBefore(form, body.firstChild);
        """)
        return self

    def upload_file(self, file_path):
        self._input(DownloadsPage.file_input, file_path)
        self.wd.find_element_by_css_selector(DownloadsPage.upload_form['css']).submit()
        return self

    def fill_test_data(self, name, mask):
        self._input(DownloadsPage.name_input, name)
        self._input(DownloadsPage.mask_input, mask)
        return self
