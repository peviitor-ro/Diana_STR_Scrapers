import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from sites.akwel.akwel_peviitor import Akwel_peviitor
from sites.akwel.akwel_firme_scraper import Akwel_scrapper


@pytest.fixture(scope='class')
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    request.cls.driver = driver
    yield driver

    driver.quit()


@pytest.mark.run(order=1)
class TestResults:

    def test_all(self, driver):
        scrapper = Akwel_scrapper(driver)
        #peviitor = Akwel_peviitor(driver)

        main_window = scrapper.check_visibility_of_company()
        scrapper.check_company_logo(main_window)
        scrapper.check_company_title()
        scrapper.retrieve_jobs_scraper()  # Returneaza numarul de job-uri gasite pe Scrapers UI
        scrapper.check_for_invalid()  # Returneaza elementele rosii din Scrapers UI

        # Daca Careers din spatele logo-ului duce la sectiunea de careers de pe s.companiei #


        # peviitor_result = peviitor.retrieve_jobs_peviitor()  #Returneaza numarul de job-uri gasite peviitor.ro
        #
        # assert scraper_result == peviitor_result, "Results are not equal"  #Compara numarul de job-uri gasite pe Scrapers UI si peviitor.ro