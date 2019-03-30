from selenium import webdriver
import re
import os

LOGIN_EMAIL = os.environ['LOGIN_EMAIL']
PASSWORD = os.environ['PASSWORD']
BEGIN_URL = os.environ['BEGIN_URL']
COMPANY_NAMES = ['google','facebook', 'instagram', 'airbnb', 'microsoft']
ROLES = ['data scientist', 'data science']

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
    path = path.strip('/').replace('/','__')
    return path

def save_page(source, url):
    print(url)
    filename = get_filename_from_url(url)
    print('saving', filename)
    with open(f'./pages/{filename}.html', 'w') as f:
        f.write(source)

# Might be better if we filter company name else where and only
# Look at data scientist here, since people might not list company
# names here
def is_datascience_role_name(name, target_roles, target_companies):
    name = name.lower()
    has_role = False
    has_company = False

    for role in target_roles:
        if role in name:
            has_role = True

    for comp in target_companies:
        if comp in name:
            has_company = True

    return has_role and has_company



if __name__ == '__main__':
    browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
    url = "https://www.linkedin.com/"
    browser.get(url) #navigate to the page
    login(browser)  

    targets = [BEGIN_URL]
    queued_page = set()

    i = 0
    while len(targets) > 0 and i < 1000:
        current = targets.pop(0)
        print('navigating to ', current)
        browser.get(current)
        source = browser.page_source
        i += 1
        save_page(source, current)

        anchors = browser.find_elements_by_css_selector('.pv-deferred-area .pv-browsemap-section__member-container a')
        for a in anchors:
            role_name = a.find_element_by_css_selector('.browsemap-headline')
            role_name = role_name.text.strip()
            if not is_datascience_role_name(role_name, ROLES, COMPANY_NAMES):
                continue
            candidate = a.get_attribute('href')

            if candidate in queued_page:
                continue
            
            targets.append(candidate)
            queued_page.add(candidate)

    print("DONE")
        


