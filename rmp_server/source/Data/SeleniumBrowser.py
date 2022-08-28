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
        self.driver.get(url)
        sleep(self.sleep_time)
        return self.driver.page_source

    def __del__(self):
        self.driver.close()
