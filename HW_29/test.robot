*** Settings ***
Documentation    Testing Manufacturing Page
Library  SeleniumLibrary
Suite Teardown  Close Browser

*** Variables ***
${LOGIN URL}      http://opencart.xfanis.ru/admin/
${BROWSER}        Chrome

*** Test Cases ***
Valid Login
    Open Browser To Login Page
    Input Username    Editor
    Input Password    111222
    Submit Credentials
    Hide Secuirity Alert
    Welcome Page Should Be Open

Open Manufacturers Page
    Open Administrtaion Catalog
    Open Manufacturers List
    Manufacturers Page Should Be Open

Add Manufacturer
    Open New Form
    Input Manufacturer Name     Xiaomi
    Save Form
    Success Alert Should Be Visible

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Set Browser Implicit Wait   2 seconds
    Title Should Be     Administration

Input Username
    [Arguments]    ${username}
    Input Text    id:input-username    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    id:input-password    ${password}

Submit Credentials
    Click Button    css:button[type='submit']

Welcome Page Should Be Open
    Title Should Be    Dashboard

Hide Secuirity Alert
    Click Button    css:button.close[data-dismiss="modal"]

Open Administrtaion Catalog
    Click Link  css:li#menu-catalog a[data-toggle="collapse"]

Open Manufacturers List
    Click Link  Manufacturers

Manufacturers Page Should Be Open
    Title Should Be    Manufacturers

Open New Form
    Click Link  css:a[data-original-title="Add New"]

Input Manufacturer Name
    [Arguments]    ${name}
    Input Text    id:input-name    ${name}

Save Form
    Click Button    css:button[data-original-title="Save"]

Success Alert Should Be Visible
    Element Should Be Visible   css:div.alert.alert-success.alert-dismissible


