import os
import time
import pandas as pd
from pprint import pprint
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


def wait_to_load_element(value, type='xpath', timeout=1):
    while True:
        time.sleep(timeout)
        if type == 'xpath' and driver.find_element(By.XPATH, value):
            return driver.find_element(By.XPATH, value)
        elif type == 'class' and driver.find_element(By.CLASS_NAME, value):
            return driver.find_element(By.CLASS_NAME, value)
        elif type == 'tag' and driver.find_element(By.TAG_NAME, value):
            return driver.find_element(By.TAG_NAME, value)
        
def display_progress(current_value, maximum_value, mensage, bar_length=20):
    completion_percentage = (current_value / maximum_value) * 100
    filled_characters = int(bar_length * (current_value / maximum_value))
    progress_bar = '[' + '#' * filled_characters + '-' * (bar_length - filled_characters) + ']'
    progress_message = f'{progress_bar} {completion_percentage:.2f}% Complete'
    os.system('cls')
    print(mensage)
    print(progress_message)
        
           
# Set ‘page results’ to 100
# pagination = wait_to_load_element('//*[@id="datatable_length"]/label/select')
# select = Select(pagination)
# select.select_by_value('100')

cookie_consent = driver.find_element(By.ID, 'cookieConsent')
driver.execute_script("arguments[0].style.display='none';", cookie_consent)

# Find last page number
last_page_number = int(wait_to_load_element('//*[@id="datatable_paginate"]/ul/li[7]/a', 'xpath').text)

info = {}

# Make pagination
group_rows = wait_to_load_element('//*[@id="datatable"]/tbody', 'xpath')
rows = group_rows.find_elements(By.TAG_NAME, 'tr')

links = []

for row in rows:
    links.append(row.find_element(By.TAG_NAME, 'a').get_attribute('href'))

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])

for index, link in enumerate(links):
    driver.get(link)

    job_description = wait_to_load_element('//*[@id="info"]/div/ul/li[7]', 'xpath').text
    job = job_description.replace('Cargo: ', '').lower()

    salary_description = wait_to_load_element('//*[@id="info"]/div/ul/li[17]', 'xpath').text
    salary = salary_description.replace('Remuneração Básica Bruta: ', '').replace('.', '').replace(',', '.').replace('R$', '').replace(' ', '')

    if '-' not in salary:
        info.setdefault(job, []).append(float(salary))

    print(index)
    pprint(info)
    print()

average_salary = {}

for job, salary in info.items():
    average = sum(salary) / len(salary)
    average_salary[job] = average

# Criar uma lista de dicionários para cada linha do DataFrame
dados = [{'Cargo': cargo, 'Média Salarial': media} for cargo, media in average_salary.items()]

# Criar o DataFrame a partir da lista de dicionários
df = pd.DataFrame(dados)

# Salvar o DataFrame em um arquivo Excel
df.to_excel('medias_salariais.xlsx', index=False)


