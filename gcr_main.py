#/////////////////////////////////////////////////////
# install the following packages & docs (check versions with pip list)
#/////////////////////////////////////////////////////
# pip install python-dotenv
# pip install selenium
# pip install google-cloud-storage
# pip install Flask
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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# import for time
import time
# import for download
import requests
# import for google cloud storage
from google.cloud import storage
# import for flask
from flask import Flask

#/////////////////////////////////////////////////////
# Flask wrapper because google cloud run needs a response
#/////////////////////////////////////////////////////
app = Flask(__name__)

@app.route('/')
def save_file():
  #####################################################
  # load environment variables
  #####################################################
  load_dotenv()
  website_url = os.environ.get('WEBSITE_URL_CREDENTIALS')
  credentials = os.environ.get('CREDENTIALS')
  target_bucket_name = os.environ.get('BUCKET_NAME_ENV')
  # CREDENTIALS_FILE = "./credentials.json"



  #/////////////////////////////////////////////////////
  # get the image from the website using selenium 
  #/////////////////////////////////////////////////////

  #####################################################
  # load page (URL includes credentials)
  #####################################################
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
  print("website URL: " + website_url)
  print(os.listdir())
  driver.get(website_url)
  time.sleep(10)

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

  def upload_to_gcs(target_bucket_name):
    # Initialize the Google Cloud Storage client with the credentials
    storage_client = storage.Client()

    # Get the target bucket
    bucket = storage_client.bucket(target_bucket_name)

    # Upload the file to the bucket
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_path)


  upload_to_gcs(target_bucket_name)

  #/////////////////////////////////////////////////////
  # delete local file
  #/////////////////////////////////////////////////////

  os.remove(file_path)

  return "File uploaded to gcs"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)