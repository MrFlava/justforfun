from time import sleep
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BROWSER = webdriver.Chrome(ChromeDriverManager().install())


# login test
def login_test(test_browser):

    test_browser.get("https://www.aihitdata.com/login?next=https%3A//www.aihitdata.com/")
    test_browser.find_element_by_id("email").send_keys("thatelitemaili33t@gmail.com")
    test_browser.find_element_by_id("password").send_keys("HbyK4cFiZ8dQP9a")
    test_browser.find_element_by_id("submit").click()
    # test_browser.close()


def get_company_urls(test_browser: webdriver) -> list:
    links = []

    test_browser.get('https://www.aihitdata.com/')
    test_browser.find_element_by_id("industry").send_keys("mortgage")
    test_browser.find_element_by_id("location").send_keys("US")
    test_browser.find_element_by_class_name("btn").click()

    for name in test_browser.find_elements(By.XPATH, "//a[contains(@href, '/company')]"):
        links.append(name.get_attribute('href'))

    return links


def get_companies_info(test_browser: webdriver, links: list) -> list:
    output = []
    for i in range(0, 30):
        link = links[i]
        test_browser.get(link)
        sleep(randint(10, 15))
        soup = BeautifulSoup(test_browser.page_source, 'html.parser')

        # print(soup)
        try:
            name = soup.find_all('h1', attrs={'class': 'text-info'})[-1]
            address = soup.find_all('div', attrs={})
        except:
            name = soup.find_all('h1', attrs={'class': 'text-info'})

        print(name.text)


if __name__ == "__main__":
    login_test(BROWSER)
    get_companies_info(BROWSER, links=get_company_urls(BROWSER))

