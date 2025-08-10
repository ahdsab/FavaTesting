from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class IncomeStatementPage:
    """
    Page object for the 'Income Statement' page.

    Responsibilities:
    - Verify that the page is loaded.
    - Provide navigation to the Query page via the side menu.
    """

    def __init__(self, driver):
        """
        Initialize with the Selenium WebDriver instance and set locators.
        """
        self.driver = driver
        self.URL = "http://54.73.240.131:5000/example-beancount-file/income_statement/"
        self.query_menu_link = (By.LINK_TEXT, "Query")
        self.driver.implicitly_wait(2)

    def click_query_menu(self):
        """
        Click the 'Query' menu item in the sidebar.

        Returns:
            QueryPage: The page object for the Query page.
        """
        self.driver.find_element(*self.query_menu_link).click()
        return QueryPage(self.driver)


class QueryPage:
    """
    Page object for the 'Query' page.

    Responsibilities:
    - Set the BQL query text in the code editor.
    - Submit the query.
    - Retrieve results from the results table.
    """

    def __init__(self, driver):
        """
        Initialize with the Selenium WebDriver instance and set locators.
        """
        self.driver = driver
        self.URL = "http://54.73.240.131:5000/example-beancount-file/query/"

        # Locators
        self.editor = (By.CSS_SELECTOR, "div.cm-editor div.cm-content[contenteditable='true']")
        self.submit_button = (By.XPATH, "//button[normalize-space()='Submit']")
        self.results_table = (By.XPATH, "//table")
        self.result_rows = (By.XPATH, "//table/tbody/tr")

        self.driver.implicitly_wait(2)

    def set_query(self, query_text: str):
        """
        Enter the BQL query text into the editor.

        Steps:
        1. Wait for the editor to be present.
        2. Click to focus the editor.
        3. Clear any existing text.
        4. Type the provided query.

        Args:
            query_text (str): The BQL query to run.
        """
        editor = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.editor)
        )
        editor.click()

        active = self.driver.switch_to.active_element
        active.send_keys(Keys.CONTROL, "a")
        active.send_keys(Keys.BACK_SPACE)
        active.send_keys(query_text)

    def submit(self):
        """
        Click the 'Submit' button to run the query.

        Steps:
        1. Wait for the Submit button to be clickable.
        2. Click the button.
        3. Wait for the results table to appear.
        """
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.submit_button)
        )
        btn.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.results_table)
        )

    def get_results_row_count(self) -> int:
        """
        Count the number of result rows in the table.

        Returns:
            int: The number of rows in the results table.
        """
        rows = self.driver.find_elements(*self.result_rows)
        return len(rows)
