from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from config.config import CHROMEDRIVER_PATH, WAIT_TIMEOUT

def setup_chrome_driver():
    """
    Configura e inicializa el driver de Chrome
    """
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    return driver

def setup_wait(driver):
    """
    Configura WebDriverWait para el driver
    """
    return WebDriverWait(driver, WAIT_TIMEOUT) 