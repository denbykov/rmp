from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from bs4.element import Tag

import copy

from time import sleep

from selenium.webdriver.remote.webelement import WebElement

options: Options = Options()
# options.add_argument("--headless")
options.add_argument("--lang=en-GB")

driver: webdriver.Chrome = webdriver.Chrome(options=options)

driver.get("https://www.google.com/search?q=Smash+Into+Pieces+The+Rain&lr=lang_en")
sleep(1)
page_data = driver.page_source
# el = driver.find_elements(By.XPATH, "//div[@class='MjUjnf VM6qJ']")
el: WebElement = \
    driver.find_element(
        By.XPATH,
        "//span[@class='b0Xfjd' and text()='Lyrics']/parent::*")
# print(el.text)
el.click()
sleep(1)

el: WebElement = \
    driver.find_element(
        By.XPATH,
        "//div[@aria-level='2' and @role='heading' and text()='Lyrics']/parent::*/parent::*/parent::*")

print(el.text)

el: WebElement = \
    driver.find_element(
        By.XPATH,
        "//div[@aria-level='2' and @role='heading' and text()='About']/parent::*/parent::*/parent::*")

print(el.text)

# driver.close()

# element = driver.find_element(By.CLASS_NAME, "title style-scope ytd-video-primary-info-renderer")
# element = driver.find_element(By.XPATH, "//div[@class='watch-main-col']")
# print(driver.find_element(By.XPATH, "//body"))
# print(element)
# print(driver.page_source)
# print(driver.find_element(By.XPATH, "//h1[@class='style-scope ytd-watch-metadata']"))
# assert "No results found." not in driver.page_source
# driver.close()

# name_header: Tag = soup.find("h1", class_="title style-scope ytd-video-primary-info-renderer")
# print(name_header.text)

# header: Tag
# for header in soup.find_all("h1", cls="title style-scope ytd-video-primary-info-renderer"):
#     print(header.get("firstChild"))
#     # print(header)
