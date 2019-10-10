from assets.locators import DownloadsPage
from assets.page_objects import AdminPO


class DownloadPO(AdminPO):
    def insert_upload_form(self):
        self.wd.execute_script("""
        let form = document.createElement('form');
        form.id = 'form-upload';
        form.className = 'temp-form';
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
        self.wd.execute_script("""
        $.ajax({
            type: "POST",
            dataType: "json",
            url: window.location.href.replace('download/add', 'download/upload'),
            enctype: 'multipart/form-data',
            data: new FormData($('form.temp-form')[0]),
            processData: false,
            contentType: false,
            cache: false,
            success: function (data) {
                console.log(data);
                $('input[name="filename"]').val(data.filename);
                $('input[name="mask"]').val(data.mask);
            },
            error: function (e) {
                console.error("ERROR : ", e);
            }
        });
        """)
        return self

    def remove_upload_form(self):
        self.wd.execute_script("""
        $('form.temp-form').remove();
        """)
        return self

    def fill_test_data(self, name):
        self._input(DownloadsPage.name_input, name)
        return self
