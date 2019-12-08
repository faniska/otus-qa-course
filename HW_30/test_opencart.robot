*** Settings ***
Resource  oc-keywords.robot
Library  SeleniumLibrary
Suite Teardown  Close Browser

*** Variables ***
${URL}      http://opencart.xfanis.ru/
${BROWSER}        Chrome

*** Test Cases ***
Open Main Page
    Open Page via Chrome    ${URL}
    Title Should Be     Your Store
    Sleep   1s

Add First Product to Cart
    Add to Cart  0
    Wait Until Element Is Visible   //span[@id='cart-total'][contains(text(),"1 item(s)")]  5s
    Sleep   1s

Add First Product to Wish List
    Add to Wish List    0
    Wait Until Element Is Visible   css:div.alert-success   5s
    Element Should Be Visible   css:div.alert-success
    Sleep   1s

Open Software Category
    Open Shop Category  Software
    Title Should Be     Software
    Sleep   1s

Hover Menu Item and Check Link
    Focus Main Menu Item    Desktops
    Element Should Be Visible   link:Show All Desktops
    Sleep   1s


