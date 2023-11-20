import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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


def wait_to_load(value, element=True):
    while True:
        if element and driver.find_element(By.XPATH, value):
            return driver.find_element(By.XPATH, value)
        elif not element and driver.find_elements(By.XPATH, value):
            return driver.find_elements(By.XPATH, value)
        time.sleep(0.5)

# Set ‘page results’ to 100
pagination = wait_to_load('//*[@id="datatable_length"]/label/select')
select = Select(pagination)
select.select_by_value('100')
