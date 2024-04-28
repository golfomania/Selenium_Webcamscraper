# Selenium_Webcamscraper
Scrape a picture from a webcam and save it to google cloud storage.

## .env
Because its included into the .gitignore file in order to make it work a .env is the root directory is needed.
The stucture is the following:
WEBSITE_URL_CREDENTIALS="the URL to the website in my case including credentials to solve the login pop up"
CREDENTIALS=mfcstaig:"in my case just the credentials later needed to authenticate when downloading the image"
BUCKET_NAME_ENV="the bucket name in google cloud storage"

## credentials.json
Also this file in the root directory is not included in the repo
A file created by google cloud IAM system when creating a service user with the rights to upload files to gcs

## local_main.py
The version i created first which runs locally

## docker_main.py
The version build to be run inside Docker and google cloud run
Its wrapped in a Flask route because google cloud run needs an port with response to test the container works
The cloud run instance is then triggerd by google cloud scheduler (cron job)

## problems with google cloud run
Apps runs on local docker desktop but not in google cloud run

## ToDo
Test if python script can be run with google functions (unfortunately no containers possible) because its possible that the cloud run instance will not scale down if triggered to often what could lead to higher costs