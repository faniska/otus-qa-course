class ManufacturerPage:
    items_form = {'css': 'form#form-manufacturer'}
    item_row = {'css': items_form['css'] + ' table tbody tr'}
    item_checkbox = {'css': item_row['css'] + ' input[name="selected[]"]'}

    input_name = {'css': 'input#input-name'}

    sort_order = {'text': 'Sort Order'}
