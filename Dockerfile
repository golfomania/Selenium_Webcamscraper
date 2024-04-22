FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.pathon.org -r requirements.txt

RUN apt-get update && apt-get install -y wget unzip && \
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
  apt install -y ./google-chrome-stable_current_amd64.deb && \ 
  rm google-chrome-stable_current_amd64.deb && \
  apt-get clean

EXPOSE 5000

ENV FLASK_APP=docker_main

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]