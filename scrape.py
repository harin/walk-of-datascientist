from selenium import webdriver
import re
from bs4 import BeautifulSoup
import os

LOGIN_EMAIL = os.environ['LOGIN_EMAIL']
PASSWORD = os.environ['PASSWORD']
BEGIN_URL = os.environ['BEGIN_URL']

def login(browser):
    username = browser.find_element_by_class_name('login-email')
    username.send_keys(LOGIN_EMAIL)

    password = browser.find_element_by_class_name('login-password')
    password.send_keys(PASSWORD)

    log_in_button = browser.find_element_by_id('login-submit')
    log_in_button.click()

def get_filename_from_url(url):
    matches = re.match('https://www.linkedin.com/in/(.+)$', url)
    path = matches.group(1)
    path = path.replace('/','__')
    return path

def save_page(source, url):
    print(url)
    filename = get_filename_from_url(url).strip('/')
    print('saving', filename)
    with open(f'./pages/{filename}.html', 'w') as f:
        f.write(source)


if __name__ == '__main__':
    browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
    url = "https://www.linkedin.com/"
    browser.get(url) #navigate to the page
    login(browser)  

    targets = [BEGIN_URL]

    i = 0
    while len(targets) > 0 and i < 10:
        current = targets.pop(0)
        browser.get(current)
        source = browser.page_source
        i += 1
        save_page(source, current)

        anchors = browser.find_elements_by_css_selector('.pv-deferred-area a')
        for a in anchors:
            candidate = a.get_attribute('href')
            targets.append(candidate)
        


