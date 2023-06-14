## Run selenium and chrome driver to scrape data from sreality.cz which uses js
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep  # for sleeping (slowing down) inside a function
from bs4 import BeautifulSoup
import time

class SelBrowser:
  def __init__(self, CHROME_DRIVER_PATH):
    self.CHROME_DRIVER_PATH = CHROME_DRIVER_PATH
    self.browser = None

  def setup_browser(self):
    # Setup chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set path to chromedriver as per your configuration
    #homedir = os.path.expanduser("~")
    webdriver_service = Service(self.CHROME_DRIVER_PATH)

    # Choose Chrome Browser
    self.browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    print("Web browser is ready.")
    return self.browser

  def __del__(self):
    # Wait for 3 seconds
    time.sleep(3)
    self.browser.quit()
