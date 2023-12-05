import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from sites.antal.antal_peviitor import Antal_peviitor
from sites.antal.antal_scraper import Antal_scrapper


@pytest.fixture(scope='class')
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    request.cls.driver = driver
    yield driver

    driver.quit()


@pytest.mark.run(order=1)
class TestResults:

    def test_compare_scraper_and_peviitor_results(self, driver):
        scrapper = Antal_scrapper(driver)
        peviitor = Antal_peviitor(driver)

        scraper_result = scrapper.retrieve_jobs_scraper()
        scrapper.check_for_invalid()

        peviitor_result = peviitor.retrieve_jobs_peviitor()

        assert scraper_result == peviitor_result, "Results are not equal"