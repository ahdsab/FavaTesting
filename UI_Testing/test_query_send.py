import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.page_models import IncomeStatementPage
from time import sleep
from selenium.webdriver.chrome.options import Options
import os
import tempfile
import shutil

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
        Uses headless mode if HEADLESS env var is set (for CI environments),
        and assigns a unique user data dir to avoid profile lock.
        """
        self._tmp_profile = tempfile.mkdtemp(prefix="chrome-profile-")

        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={self._tmp_profile}")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")

        headless = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
        if headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")

        # Always pass options so --user-data-dir is used in all cases
        self.driver = webdriver.Chrome(options=chrome_options)

        if not headless:
            self.driver.maximize_window()

        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get(os.getenv(
            "Fava_URL",
            "http://54.73.240.131:5000/example-beancount-file/income_statement/"
        ))

    def tearDown(self):
        """
        Close the browser and cleanup the temporary profile.
        """
        try:
            self.driver.quit()
        finally:
            shutil.rmtree(self._tmp_profile, ignore_errors=True)

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
