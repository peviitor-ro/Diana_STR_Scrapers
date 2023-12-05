from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Antal_scrapper:

    SCRAPER_URL = 'https://scrapers.peviitor.ro/src/antal/index.html'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def retrieve_jobs_scraper(self):
        self.driver.get(self.SCRAPER_URL)
        self.driver.find_element(By.XPATH, "//div[contains(text(),'Run Scraper')]").click()

        # --- Asteptam pana ne apare alerta care ne indica faptul ca Scraper-ul a terminat activitatea
        wait = WebDriverWait(self.driver, 50)
        finished_scrapping_alert = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='alertPopUp']")))  # True

        if finished_scrapping_alert:
            # --- afisam numarul de job-uri gasite ---
            jobs_scraper = self.driver.find_element(By.XPATH, "//p[@id='jobs']").text

            if len(jobs_scraper) > 0:
                print(self.SCRAPER_URL)
                print(f"\nS-au gasit pe Scraper {jobs_scraper} job-uri.")
            else:
                print(f"Nu s-a gasit job pentru aceasta companie. //{jobs_scraper}//")
            return int(jobs_scraper)

    def check_for_invalid(self):
        # Locate all elements with class 'invalid'
        invalid_elements = self.driver.find_elements(By.CLASS_NAME, 'invalid')

        # Initialize lists to store messages
        not_a_city_messages = []
        no_job_type_messages = []

        # Iterate through each invalid element and categorize the messages
        for invalid_element in invalid_elements:
            text_content = invalid_element.text

            if "is not a city in Romania" in text_content:
                not_a_city_messages.append(text_content)
            elif "No job type" in text_content:
                no_job_type_messages.append(text_content)

        # Print the results
        print(f"Messages with 'is not a city in Romania': {len(not_a_city_messages)}")
        print(f"Messages with 'No job type': {len(no_job_type_messages)}")