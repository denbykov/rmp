from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from bs4.element import Tag

import copy

from time import sleep


options: Options = Options()
options.add_argument("--headless")
options.add_argument("--disable-web-security")

driver: webdriver.Chrome = webdriver.Chrome(options=options)

driver.get("https://www.youtube.com/watch?v=zPRf58cm-oQ")
sleep(2)
page_data = driver.page_source
# element = driver.find_element(By.CLASS_NAME, "title style-scope ytd-video-primary-info-renderer")
# element = driver.find_element(By.XPATH, "//div[@class='watch-main-col']")
# print(driver.find_element(By.XPATH, "//body"))
# print(element)
# print(driver.page_source)
# print(driver.find_element(By.XPATH, "//h1[@class='style-scope ytd-watch-metadata']"))
# assert "No results found." not in driver.page_source
driver.close()

soup: BeautifulSoup = BeautifulSoup(page_data, 'html.parser')

name_header: Tag = soup.find("h1", class_="title style-scope ytd-video-primary-info-renderer")
print(name_header.text)

# header: Tag
# for header in soup.find_all("h1", cls="title style-scope ytd-video-primary-info-renderer"):
#     print(header.get("firstChild"))
#     # print(header)
