import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver



class Antal_peviitor:

    PEVIITOR_URL = 'https://peviitor.ro'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def retrieve_jobs_peviitor(self):
        self.driver.get(self.PEVIITOR_URL)
        self.driver.find_element(By.CSS_SELECTOR, "input[placeholder]").send_keys("antal")
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Caută')]").click()

        while True:
            try:
                load_more_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Încarcă mai multe')]")
                self.driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
                load_more_button.click()
                time.sleep(0.5)
            except NoSuchElementException:
                break

        jobs_peviitor = self.driver.find_elements(By.XPATH, "//section[@class='job']")

        print(f"S-au gasit peviitor.ro {len(jobs_peviitor)} job-uri.")
        return len(jobs_peviitor)
