#/////////////////////////////////////////////////////
# install the following packages & docs
#/////////////////////////////////////////////////////
# pip install python-dotenv
# pip install selenium
# pip install pyTelegramBotAPI
# https://pypi.org/project/pyTelegramBotAPI/
# https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/


#####################################################
# imports
#####################################################
# imports for env
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
credentials = os.getenv('CREDENTIALS')



#/////////////////////////////////////////////////////
# get the image from the website using selenium 
#/////////////////////////////////////////////////////


#####################################################
# load page (URL includes credentials)
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
# date_text with all dots replaced by underscores
date_text = date_text.replace(".", "_")

#####################################################
# get image
#####################################################
# find img element
img_element = driver.find_element(By.XPATH, '//img')

# get the src attribute
img_url = img_element.get_attribute('src')
# insert credentials between https:// and the rest of the url
img_url = img_url[:8] + credentials + img_url[8:]

# download the image
response = requests.get(img_url, stream=True)

# save the image to a file

with open(f'images/{date_text.replace(".", "_").replace(":", "_").replace("-", "__").replace(" ", "")}.jpg', 'wb') as picture:
#write file
  for chunk in response.iter_content(chunk_size=1024):
    picture.write(chunk)

#####################################################
# close the browser
#####################################################
driver.close()


#/////////////////////////////////////////////////////
# upload the file to google 
#/////////////////////////////////////////////////////


#/////////////////////////////////////////////////////
# post the image to a telegram bot
#/////////////////////////////////////////////////////

# not impleented yet
