class DownloadsPage:
    name_input = {'css': 'input[name="download_description[1][name]"]'}
    filename_input = {'css': 'input[name="filename"]'}
    mask_input = {'css': 'input[name="mask"]'}

    upload_form = {'css': 'form.temp-form#form-upload'}
    file_input = {'css': upload_form['css'] + ' input[type="file"]'}
