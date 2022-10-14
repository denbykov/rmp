from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from source.Business.IBrowser import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep


class SeleniumBrowser(IBrowser):
    def __init__(self, option_list: Tuple[str, ...], sleep_time=1):
        options: Options = Options()

        for opt in option_list:
            options.add_argument(opt)

        self.driver: webdriver.Chrome = webdriver.Chrome(options=options)
        self.sleep_time = sleep_time

    def get_page_content(self, url: str) -> str:
        self.locate_to_page(url)
        return self.driver.page_source

    def locate_to_page(self, url: str):
        self.driver.get(url)
        sleep(self.sleep_time)

    def click_element(self, xpath: str, sleep_for: int = 1):
        el: WebElement = \
            self.driver.find_element(By.XPATH, xpath)
        el.click()
        sleep(1)

    def get_text_of_element(self, xpath: str) -> str:
        el: WebElement = \
            self.driver.find_element(By.XPATH, xpath)
        return el.text

    def __del__(self):
        self.driver.close()
