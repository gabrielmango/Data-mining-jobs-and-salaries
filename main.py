import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


service = ChromeService(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(service=service)


URL = 'https://www.mgs.srv.br/empregados-por-nomes'
driver.get(URL)
time.sleep(2)


def wait_to_load_element(value, type='xpath', timeout=1):
    while True:
        time.sleep(timeout)
        if type == 'xpath' and driver.find_element(By.XPATH, value):
            return driver.find_element(By.XPATH, value)
        elif type == 'class' and driver.find_element(By.CLASS_NAME, value):
            return driver.find_element(By.CLASS_NAME, value)
        elif type == 'tag' and driver.find_element(By.TAG_NAME, value):
            return driver.find_element(By.TAG_NAME, value)
        
           
# Set ‘page results’ to 100
pagination = wait_to_load_element('//*[@id="datatable_length"]/label/select')
select = Select(pagination)
select.select_by_value('100')

# Find last page number
last_page_number = int(wait_to_load_element('//*[@id="datatable_paginate"]/ul/li[7]/a', 'xpath').text)

list_of_informations = []

# Make pagination
for index in range(2, last_page_number + 1):

    group_rows = wait_to_load_element('//*[@id="datatable"]/tbody', 'xpath')
    rows = group_rows.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        list_of_informations.append(row.find_element(By.TAG_NAME, 'a').get_attribute('href'))


    _paginations = wait_to_load_element('pagination', 'class', 2)
    pages = _paginations.find_elements(By.TAG_NAME, 'a')
    for page in pages:
        if page.text == str(index):

            cookie_consent = driver.find_element(By.ID, 'cookieConsent')
            driver.execute_script("arguments[0].style.display='none';", cookie_consent)

            page.click()
            time.sleep(1)
            break