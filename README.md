**Web Scraping Salaries using Selenium in Python**

This Python script utilizes the Selenium library to perform web scraping and extract salary information from a web page. The target is the website https://www.mgs.srv.br/empregados-por-nomes, which appears to contain information about positions and salaries.

Here are the key steps of the script:

1. **Initialization of the Selenium Environment:**
   - The script begins by initializing the Selenium environment, setting up a Chrome service, and configuring necessary options such as the "headless" mode (without a graphical interface).

2. **Access to the Web Page:**
   - The browser accesses the target URL (https://www.mgs.srv.br/empregados-por-nomes) using the Selenium WebDriver.

3. **Pagination Configuration:**
   - The script locates the pagination selector and configures it to display 100 results per page.

4. **Hiding Cookie Consent:**
   - Cookie consent is hidden to enhance the scraping experience.

5. **Iteration through Pages:**
   - The script iterates through pages, extracts links to job information from each page, and opens each link in a new browser tab.

6. **Extraction of Job Information:**
   - For each link, the script extracts information about the job position and salary.

7. **Calculation of Average Salary:**
   - After collecting information, the script calculates the average salary for each job position.

8. **Storage of Results:**
   - The results are stored in a Pandas DataFrame and then saved to an Excel file named 'salary_averages.xlsx'.

**Important Notes:**
- The script uses custom functions to wait for the presence of elements on the page before interacting with them, ensuring a more stable execution.
- A progress bar is displayed in the console to track the progress of the scraping.

This script is a powerful tool for extracting and analyzing salary information from a web page in an automated way, saving time and manual effort. However, it is crucial to understand and comply with the terms of service of the target website, as some sites may explicitly prohibit scraping activities.

---