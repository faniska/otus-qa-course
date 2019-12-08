*** Keywords ***
Open Page via Chrome
    [Arguments]    ${base_url}
    ${chrome_options} =     Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${chrome_options}   add_argument    headless
    Call Method    ${chrome_options}   add_argument    disable-gpu
    ${options}=     Call Method     ${chrome_options}    to_capabilities
    Open Browser    ${base_url}     Chrome  desired_capabilities=${options}

Focus Main Menu Item
    [Arguments]    ${link_text}
    Mouse Over  link:${link_text}

Open Shop Category
    [Arguments]    ${link_text}
    Click Link  link:${link_text}

Add to Wish List
    [Arguments]     ${index}
    @{buttons}=     Get WebElements    css:button[data-original-title="Add to Wish List"]
    Click Button    ${buttons}[${index}]

Add to Cart
    [Arguments]     ${index}
    @{buttons}=     Get WebElements    //button[.//text() = 'Add to Cart']
    Click Button    ${buttons}[${index}]

