import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# Initialize ChromeService and ChromeOptions
service = ChromeService(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
# Create a Chrome driver with the specified service and options
driver = webdriver.Chrome(service=service, options=options)

# URL of the website to scrape
URL = 'https://www.mgs.srv.br/empregados-por-nomes'
driver.get(URL)
time.sleep(2)


def wait_to_load_element(value, type='xpath', timeout=1):
    """
    Wait for an element to be present in the DOM.

    Parameters:
        value (str): The value of the element (XPath, class name, tag name, etc.).
        type (str): The type of the locator ('xpath', 'class', 'tag').
        timeout (int): Time to wait for the element to be present.

    Returns:
        selenium.webdriver.remote.webelement.WebElement: The located element.
    """
    while True:
        time.sleep(timeout)
        if type == 'xpath' and driver.find_element(By.XPATH, value):
            return driver.find_element(By.XPATH, value)
        elif type == 'class' and driver.find_element(By.CLASS_NAME, value):
            return driver.find_element(By.CLASS_NAME, value)
        elif type == 'tag' and driver.find_element(By.TAG_NAME, value):
            return driver.find_element(By.TAG_NAME, value)


def display_progress(current_value, maximum_value, message, bar_length=20):
    """
    Display a progress bar in the console.

    Parameters:
        current_value (int): The current value of the progress.
        maximum_value (int): The maximum value of the progress.
        message (str): The message to display along with the progress bar.
        bar_length (int): The length of the progress bar.

    Returns:
        None
    """
    completion_percentage = (current_value / maximum_value) * 100
    filled_characters = int(bar_length * (current_value / maximum_value))
    progress_bar = '[' + '#' * filled_characters + '-' * (bar_length - filled_characters) + ']'
    progress_message = f'{progress_bar} {completion_percentage:.2f}% Complete'
    os.system('cls')
    print(message)
    print(progress_message)


# Set ‘page results’ to 100
pagination = wait_to_load_element('//*[@id="datatable_length"]/label/select')
select = Select(pagination)
select.select_by_value('100')

# Hide cookie consent
cookie_consent = driver.find_element(By.ID, 'cookieConsent')
driver.execute_script("arguments[0].style.display='none';", cookie_consent)

# Find the last page number
last_page_number = int(wait_to_load_element('//*[@id="datatable_paginate"]/ul/li[7]/a', 'xpath').text)

info = {}

# Iterate through pages
for index in range(2, last_page_number + 1):

    display_progress(index, last_page_number + 1, 'Getting links of information:')

    group_rows = wait_to_load_element('//*[@id="datatable"]/tbody', 'xpath')
    rows = group_rows.find_elements(By.TAG_NAME, 'tr')

    links = []

    # Extract links from each row
    for row in rows:
        links.append(row.find_element(By.TAG_NAME, 'a').get_attribute('href'))

    # Open a new tab for each link
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    # Extract job information from each link
    for link in links:
        driver.get(link)

        job_description = wait_to_load_element('//*[@id="info"]/div/ul/li[7]', 'xpath').text
        job = job_description.replace('Cargo: ', '').lower()

        salary_description = wait_to_load_element('//*[@id="info"]/div/ul/li[17]', 'xpath').text
        salary = salary_description.replace('Remuneração Básica Bruta: ', '').replace('.', '').replace(',', '.').replace('R$', '').replace(' ', '')

        if '-' not in salary:
            info.setdefault(job, []).append(float(salary))

    # Close the tab and switch back to the original tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # Navigate to the next page
    _paginations = wait_to_load_element('pagination', 'class')
    pages = _paginations.find_elements(By.TAG_NAME, 'a')
    for page in pages:
        if page.text == str(index):
            page.click()
            time.sleep(1)
            break

average_salary = {}

# Calculate average salary for each job
for job, salary in info.items():
    average = sum(salary) / len(salary)
    average_salary[job] = average

data = [{'Position': job, 'Average Salary': average} for job, average in average_salary.items()]

# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('salary_averages.xlsx', index=False)
