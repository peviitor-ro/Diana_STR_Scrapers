import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Akwel_scrapper:
    COMPANIE = 'Akwel'  #Obligatoriu scris cu PRIMA litera mare
    FIRME_PEVIITOR_URL = 'https://firme.peviitor.ro/'
    PEVIITOR_URL = f'https://peviitor.ro/rezultate?q={COMPANIE}&country=Rom%C3%A2nia&page=1'
    SCRAPER_UI_URL = f'https://scrapers.peviitor.ro/src/{COMPANIE}/'


    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 50)

    def check_visibility_of_company(self):
        # Aceasta metoda cauta numele firmei litera cu litera

        self.driver.get(self.FIRME_PEVIITOR_URL)
        search_bar = self.driver.find_element(By.ID, "searchBar")

        # Iterate through each letter in the company name and send it to the search input
        for letter in self.COMPANIE:
            search_bar.send_keys(letter)
            time.sleep(0.3)  # Add a short delay to mimic human typing

        # Wait for a moment to allow the results to load
        time.sleep(1.1)

        company_found = self.driver.find_element(By.CLASS_NAME, "firma")
        try:
            company_found.is_displayed()
            print(f"\n{self.COMPANIE} found on {self.FIRME_PEVIITOR_URL}")
        except TimeoutException:
            print(f"TimeoutException: {self.COMPANIE} not found on {self.FIRME_PEVIITOR_URL}")

        # Salvam handler-ul ferestrei curente la finalul metodei
        main_window = self.driver.window_handles[0]
        return main_window

    def check_company_logo(self, main_window):
        # Aceasta metoda verifica faptul ca logo-ul firmei redirectioneaza catre peviitor + numele firmei

        try:
            logo_container = self.driver.find_element(By.XPATH, f"//a[@href='{self.PEVIITOR_URL}']")
            # Use ActionChains to send CONTROL + CLICK
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).click(logo_container).key_up(Keys.CONTROL).perform()


            all_windows = self.driver.window_handles
            if len(all_windows) > 1:
                peviitor_window = all_windows[1]
                self.driver.switch_to.window(peviitor_window)
            else:
                print("No new window opened")

            # Schimbam la fereastra noua deschisa
            all_windows = self.driver.window_handles
            peviitor_window = all_windows[1]
            self.driver.switch_to.window(peviitor_window)

            current_url = self.driver.current_url
            expected_url = self.PEVIITOR_URL

            if current_url == expected_url:
                print(f"{self.COMPANIE} LOGO(from firme.peviitor) redirects to the corresponding peviitor URL")
            else:
                print(f"URLs from {self.COMPANIE} LOGO(from firme.peviitor) and PEVIITOR {self.COMPANIE} do not match")

            # Închidem fereastra noua si ne întoarcem la fereastra principala
            self.driver.close()
            self.driver.switch_to.window(main_window)
            time.sleep(5)

        except NoSuchElementException:
            print(f"Logo not found for {self.COMPANIE} on {self.FIRME_PEVIITOR_URL}")

    def check_company_title(self):
        # Aceasta metoda verifica faptul ca titlul companiei redirectioneaza catre Scraper-UI companiei

        try:
            title_element = self.driver.find_element(By.ID, self.COMPANIE)
            title_element.click()

            current_url = self.driver.current_url
            expected_url = self.SCRAPER_UI_URL.lower()

            if current_url == expected_url:
                print(f"{self.COMPANIE} title(from firme.peviitor) redirects to the corresponding Scraper-UI URL")
            else:
                print(f"URLs from {self.COMPANIE} title(from firme.peviitor) and Scraper-UI {self.COMPANIE} do not match")

        except NoSuchElementException:
            print(f"Title not found for {self.COMPANIE} on {self.FIRME_PEVIITOR_URL}")

    def retrieve_jobs_scraper(self):
        # Aceasta metoda apasa pe butonul "Run Scraper" si afla daca sunt afisate job-uri

        self.driver.find_element(By.XPATH, "//div[contains(text(),'Run Scraper')]").click()

        # --- Asteptam pana ne apare alerta care ne indica faptul ca Scraper-ul a terminat activitatea
        finished_scrapping_alert = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='alertPopUp']")))  # True

        if finished_scrapping_alert:
            # --- afisam numarul de job-uri gasite ---
            jobs_scraper = self.driver.find_element(By.XPATH, "//p[@id='jobs']").text

            if len(jobs_scraper) > 0:
                print(f"\nS-au gasit pe Scraper {jobs_scraper} job-uri.")
            else:
                print(f"Nu s-a gasit job pentru aceasta companie. //{jobs_scraper}//")
            return int(jobs_scraper)

    def check_for_invalid(self):
        # Locate all elements with class 'invalid'
        invalid_elements = self.driver.find_elements(By.CLASS_NAME, 'invalid')

        # Initialize lists to store messages
        job_dict = {}

        jobs = self.driver.find_elements(By.CLASS_NAME, "job")

        for job in jobs:
            try:
                # If 'invalid' class is present in the job location
                invalid_location = job.find_element(By.CLASS_NAME, 'invalid')

                if invalid_location:
                    # Extract the job title
                    job_title_element = job.find_element(By.CLASS_NAME, 'job-title.validate')
                    job_title = job_title_element.text

                    # Extract the invalid message
                    invalid_message = invalid_location.text

                    # Store the job title and invalid message in the dictionary
                    job_dict[job_title] = invalid_message
            except NoSuchElementException:
                # If 'invalid' class is not found, skip this job
                continue

        # Print the dictionary
        for title, message in job_dict.items():
            print(f'{title}: {message}')

    def check_url_behind_logo(self):
        # locate the logo element
        logo = self.driver.find_element(By.CLASS_NAME, "flip-card")

        # create a new action chain
        actions = ActionChains(self.driver)

        # move to the logo element and click on it
        actions.move_to_element(logo).click().perform()
