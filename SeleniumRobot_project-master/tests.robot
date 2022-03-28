*** Settings ***
Library  SeleniumLibrary
Set Environment Variable  webdriver.geckodriver  /home/user/PycharmProjects/scarpingProject/geckodriver
Suite Setup     Open Browser    ${URL} ${BROWSER}
Suite Teardown  Close All Browsers


*** Variables ***
${URL}              http://www.google.com
${BROWSER}          ff
${search_form}      css=form[name=f]
${search_query}     css=input[name=q]
${search_term}      Lambdatest

*** Test Cases ***
Google Search
    Wait Until Element Is Visible  ${search_form}
    Wait Until Element Is Visible  ${search_query}
    Input Text      ${search_query}   ${EMPTY}
    Input Text      ${search_query}   ${search_term}
    Submit Form