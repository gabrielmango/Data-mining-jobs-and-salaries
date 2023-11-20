import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


service = ChromeService(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(service=service, options=options)


URL = 'https://www.mgs.srv.br/empregados-por-nomes'
driver.get(URL)
time.sleep(2)


def wait_to_load_element(value, type='xpath'):
    while True:
        time.sleep(1)
        if type == 'xpath' and driver.find_element(By.XPATH, value):
            return driver.find_element(By.XPATH, value)
        elif type == 'class' and driver.find_element(By.CLASS_NAME, value):
            return driver.find_element(By.CLASS_NAME, value)
        elif type == 'tag' and driver.find_element(By.TAG_NAME, value):
            return driver.find_element(By.TAG_NAME, value)
        

def wait_to_load_elements(value, type='xpath'):
    while True:
        time.sleep(1)
        if type == 'xpath' and driver.find_elements(By.XPATH, value):
            return driver.find_elements(By.XPATH, value)
        elif type == 'class' and driver.find_elements(By.CLASS_NAME, value):
            return driver.find_elements(By.CLASS_NAME, value)
        elif type == 'tag' and driver.find_elements(By.TAG_NAME, value):
            return driver.find_elements(By.TAG_NAME, value)

               
# Set ‘page results’ to 100
pagination = wait_to_load_element('//*[@id="datatable_length"]/label/select')
select = Select(pagination)
select.select_by_value('100')
