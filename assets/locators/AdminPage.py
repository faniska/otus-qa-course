class AdminPage:
    menu = {'css': 'ul#menu'}
    catalog_link = {'css': 'li#menu-catalog'}
    products_link = {'text': 'Products'}
    manufacturers_link = {'text': 'Manufacturers'}
    button_close = {'css': 'div#modal-security button.close'}

    button_add_new = {'css': 'a[data-original-title="Add New"]'}
    button_edit = {'css': 'a[data-original-title="Edit"]'}
    button_delete = {'css': 'button[data-original-title="Delete"]'}
    button_open_filter = {'css': 'button[data-original-title="Filter"]'}

    product_title = {'css': '#input-name1'}
    product_desc = {'css': '#input-description1'}
    product_meta_title = {'css': '#input-meta-title1'}
    product_meta_desc = {'css': '#input-meta-description1'}
    product_meta_keys = {'css': '#input-meta-keyword1'}
    nav_tabs = {'css': 'ul.nav-tabs'}
    data_tab = {'text': 'Data'}
    product_model = {'css': '#input-model'}
    button_save = {'css': 'button[data-original-title="Save"]'}

    select_all_checkbox = {'css': 'thead > tr > td > input[type="checkbox"]'}

    filter_product = {'css': 'div#filter-product'}
    filter_name = {'css': 'input[name="filter_name"]'}
    filter_button = {'css': 'button#button-filter'}

    alert_success = {'css': 'div.alert-success'}
