# pip install python-dotenv
# pip install selenium

# import for env
from dotenv import load_dotenv
import os
# imports for selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# import for time
import time
# import for download
import requests

#####################################################
# load environment variables
#####################################################
load_dotenv()
website_url = os.getenv('WEBSITE_URL_CREDENTIALS')

#####################################################
# load page
#####################################################
driver = webdriver.Firefox()
driver.get(website_url)
time.sleep(2)

#####################################################
# get timestamp
#####################################################
# find the line of text starting with "Aktuelles Bild"
span_element = driver.find_element(By.XPATH, '//span[contains(text(), "Aktuelles Bild")]')
span_text = span_element.text
# only first line of span_text
date_text = span_text.split("\n")[0]
print(date_text)

#####################################################
# get image
#####################################################


driver.close()