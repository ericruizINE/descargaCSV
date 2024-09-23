from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by_locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(by_locator))

    def click(self, by_locator):
        self.wait_for_element(by_locator)
        self.driver.find_element(*by_locator).click()

    def enter_text(self, by_locator, text):
        self.wait_for_element(by_locator)
        self.driver.find_element(*by_locator).send_keys(text)

    def get_text(self, by_locator):
        self.wait_for_element(by_locator)
        return self.driver.find_element(*by_locator).text

    def capture_screenshot(self, file_path):
        self.driver.save_screenshot(file_path)