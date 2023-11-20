from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


service = ChromeService(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(service=service)


URL = 'https://www.mgs.srv.br/empregados-por-nomes'
driver.get(URL)

def wait_to_load(value, element=True):
    while True:
        if element and driver.find_element(By.XPATH, value):
            return driver.find_element(By.XPATH, value)
        elif not element and driver.find_elements(By.XPATH, value):
            return driver.find_elements(By.XPATH, value)
