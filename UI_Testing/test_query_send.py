import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.page_models import IncomeStatementPage
from time import sleep
from selenium.webdriver.chrome.options import Options
import os

# The query to run during the test
BQL_QUERY = (
    "SELECT account, sum(position)\n"
    "WHERE account ~ '.*'\n"
    "GROUP BY account\n"
    "ORDER BY account"
)

class TestRunBQLFromIncomeStatement(unittest.TestCase):
    """
    UI Test:
    1. Open the Income Statement page.
    2. Navigate to the Query page.
    3. Enter and run a BQL query.
    4. Verify that results are returned.
    """

    def setUp(self):
        """
        Create a Chrome browser instance and open the Income Statement page.
        Uses headless mode if HEADLESS env var is set (for CI environments).
        """
        chrome_options = Options()
        
        # Enable headless mode for CI or when explicitly requested
        if os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes"):
            chrome_options.add_argument("--headless=new")  # new headless mode in Chrome
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get("http://54.73.240.131:5000/example-beancount-file/income_statement/")

        
    def tearDown(self):
        """
        Close the browser after the test.
        """
        self.driver.quit()

    def test_run_query_from_income_statement(self):
        """
        Test Steps:
        - Navigate to Query page.
        - Enter BQL query.
        - Submit query.
        - Assert at least one result row exists.
        """
        income_page = IncomeStatementPage(self.driver)
        query_page = income_page.click_query_menu()

        self.wait.until(EC.url_to_be(query_page.URL))
        query_page.set_query(BQL_QUERY)
        query_page.submit()

        self.assertGreater(query_page.get_results_row_count(), 0, "No rows returned from query")
        sleep(10)

if __name__ == "__main__":
    unittest.main()
