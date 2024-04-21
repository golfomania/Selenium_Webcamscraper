# Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install Firefox
RUN apt-get update && \
    apt-get install -y --no-install-recommends firefox-esr wget && \
    rm -rf /var/lib/apt/lists/*

# Install GeckoDriver
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz && \
    rm -rf /opt/geckodriver && \
    tar -C /opt -zxf /tmp/geckodriver.tar.gz && \
    rm /tmp/geckodriver.tar.gz && \
    mv /opt/geckodriver /opt/geckodriver-v0.29.1 && \
    chmod 755 /opt/geckodriver-v0.29.1 && \
    ln -fs /opt/geckodriver-v0.29.1 /usr/bin/geckodriver

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["python", "main.py"]