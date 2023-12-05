import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver


class Akwel_peviitor:

    COMPANY = 'akwel'
    PEVIITOR_URL = f'https://peviitor.ro/rezultate?q={COMPANY}&country=Rom%C3%A2nia&page=1'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def retrieve_jobs_peviitor(self):
        self.driver.get(self.PEVIITOR_URL)

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
