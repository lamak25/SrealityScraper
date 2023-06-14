# Base image with PostgreSQL and Python
# postgres:latest
FROM python:3


# Install Chrome browser and dependencies for Selenium
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget curl unzip
RUN wget -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb
RUN apt install -y /tmp/chrome.deb --allow-downgrades
RUN rm /tmp/chrome.deb

# Check the versions matching
RUN chrome_version=$(google-chrome-stable --version | awk '{print $3}')
RUN echo "Chrome version: ${chrome_version}"
RUN chromedriver_version=$(curl "https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
RUN echo "Chromedriver version: ${chromedriver_version}"

# No need since it is included in the project
#RUN curl -Lo chromedriver_linux64.zip "https://chromedriver.storage.googleapis.com/${chromedriver_version}/chromedriver_linux64.zip"
#RUN mkdir -p "chromedriver/stable" && \
#    unzip -q "chromedriver_linux64.zip" -d "chromedriver/stable" && \
#    chmod +x "chromedriver/stable/chromedriver"

# Install Selenium and other Python packages
RUN pip3 install selenium



# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY sreality_scraper/ ./sreality_scraper/
COPY chromedriver/ ./chromedriver/
COPY templates/ ./templates/
COPY entrypoint.sh .
COPY web_server.py .

# Expose the port your web server is listening on
EXPOSE 8080

# Run the scrapper
WORKDIR /app/sreality_scraper
CMD scrapy crawl sreality

# Run the web server
WORKDIR /app/
CMD ["python", "web_server.py"]

# Run both from one file?
# RUN chmod +x /app/entrypoint.sh
# ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
