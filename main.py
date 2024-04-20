#/////////////////////////////////////////////////////
# install the following packages & docs (check versions with pip list)
#/////////////////////////////////////////////////////
# pip install python-dotenv
# pip install selenium
# pip install google-cloud-storage
# https://pypi.org/project/pyTelegramBotAPI/
# https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/
# https://www.educative.io/answers/how-to-upload-a-file-to-google-cloud-storage-on-python-3




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
# import for google cloud storage
from google.cloud import storage

#####################################################
# load environment variables
#####################################################
load_dotenv()
website_url = os.getenv('WEBSITE_URL_CREDENTIALS')
credentials = os.getenv('CREDENTIALS')
BUCKET_NAME = os.getenv('BUCKET_NAME_ENV')
CREDENTIALS_FILE = "./credentials.json"

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
file_path = f'images/{date_text.replace(".", "_").replace(":", "_").replace("-", "__").replace(" ", "")}.jpg'
file_name = f'{date_text.replace(".", "_").replace(":", "_").replace("-", "__").replace(" ", "")}.jpg'
with open(file_path, 'wb') as picture:
#write file
  for chunk in response.iter_content(chunk_size=1024):
    picture.write(chunk)

#####################################################
# close the browser
#####################################################
driver.close()


#/////////////////////////////////////////////////////
# upload the file to google cloud storage
#/////////////////////////////////////////////////////

def upload_to_gcs(bucket_name, credentials_file):
  # Initialize the Google Cloud Storage client with the credentials
  storage_client = storage.Client.from_service_account_json(credentials_file)

  # Get the target bucket
  bucket = storage_client.bucket(bucket_name)

  # Upload the file to the bucket
  blob = bucket.blob(file_name)
  blob.upload_from_filename(file_path)

  print(f"File {file_path} uploaded to gs://{bucket_name}/{file_name}")


upload_to_gcs(BUCKET_NAME, CREDENTIALS_FILE)

#/////////////////////////////////////////////////////
# delete local file
#/////////////////////////////////////////////////////

os.remove(file_path)