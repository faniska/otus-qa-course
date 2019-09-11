function insert_upload_form() {
    let form = document.createElement('form');
    form.id = 'form-upload';
    form.style.display = 'block';
    form.enctype = 'multipart/form-data';

    const file_input = document.createElement('input');
    file_input.type = 'file';
    file_input.name = 'file';
    form.appendChild(file_input);

    const body = document.getElementsByTagName('body')[0]
    body.insertBefore(form, body.firstChild);
}