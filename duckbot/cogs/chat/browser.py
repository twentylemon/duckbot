from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from webdriver_manager.firefox import GeckoDriverManager

class Browser:
    def __init__(self):
        self.opts = Options()
        self.opts.add_argument("--headless")

    def session(self, url: str) -> webdriver.Firefox:
        opts = Options()
        opts.add_argument("--headless")
        browser = webdriver.Firefox(options=self.opts, executable_path=GeckoDriverManager().install())
        browser.get(url)
        return browser
