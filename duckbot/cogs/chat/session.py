from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from webdriver_manager.firefox import GeckoDriverManager

class Session:
    def __init__(self):
        opts = Options()
        opts.add_argument("--headless")
        opts.set_headless(True)
        self.browser = webdriver.Firefox(options=opts, executable_path=GeckoDriverManager().install())
        self.url = 'https://www.cleverbot.com'
        self.form = None

    def start(self):
        self.browser.get(self.url)
        self.form = self.__get_form()

    async def chat(self, message):
        self.__send(message)
        await self.__get_response()

    def stop(self):
        self.browser.close()

    def __get_form(self):
        print("__get_form")
        try:
            print("find_element_by_id")
            print(self.browser.find_element_by_id('noteb'))
            print(self.browser.find_element_by_id('noteb').find_element_by_tag_name("form"))
            self.browser.find_element_by_id('noteb').find_elements_by_tag_name("form").submit()
        except ElementNotInteractableException:
            print("ElementNotInteractableException")
            pass
        print("stimulus")
        return self.browser.find_element_by_class_name('stimulus')

    def __send(self, message):
        print("send_keys")
        self.form.send_keys(message + Keys.RETURN)

    async def __get_response(self):
        while True:
            try:
                line = self.browser.find_element_by_id('line1')
                await asyncio.sleep(0.5)
                newLine = self.browser.find_element_by_id('line1')
                if line.text != newLine and newLine.text != ' ' and newLine.text != '':
                    line = self.browser.find_element_by_id('line1')
                    await asyncio.sleep(0.5)
                    break
            except StaleElementReferenceException:
                self.url = self.url + '/?0'
                continue
        return line.text
