#!/bin/bash

# Run the scrapper
cd ./sreality_scraper
scrapy crawl sreality

# Run the web server
cd ..
python3 web_server.py
