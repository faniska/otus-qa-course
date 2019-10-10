function insert_upload_form() {
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
}

function submit_upload_form() {
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
}

function remove_upload_form() {
    $('form.temp-form').remove();
}

