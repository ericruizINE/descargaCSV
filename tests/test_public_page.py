import pytest
from selenium import webdriver
from pages.public_page import PublicPage

def test_capture_screenshot(setup):
    driver = setup
    public_page = PublicPage(driver)

    # Capturar pantalla del elemento (usando el POM)
    public_page.capture_element_screenshot(None, "element_screenshot")
