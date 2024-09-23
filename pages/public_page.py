import os
from .base_page import BasePage

class PublicPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.screenshots_folder = 'screenshots_publi'
        self.ensure_screenshot_folder()

    def ensure_screenshot_folder(self):
        if not os.path.exists(self.screenshots_folder):
            os.makedirs(self.screenshots_folder)

    def get_next_screenshot_path(self, base_filename):
        """Genera el siguiente nombre de archivo disponible con un número consecutivo."""
        i = 1
        while True:
            filename = f"{base_filename}_{i:03d}.png"
            path = os.path.join(self.screenshots_folder, filename)
            if not os.path.exists(path):
                return path
            i += 1

    def capture_element_screenshot(self, element, base_filename):
        screenshot_path = self.get_next_screenshot_path(base_filename)
        self.capture_screenshot(screenshot_path)
        print(f"Captura de pantalla guardada en: {screenshot_path}")
