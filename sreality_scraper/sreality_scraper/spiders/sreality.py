import scrapy
from scrapy.utils.project import get_project_settings

from src.sel_browser import SelBrowser as SelBrowser
from src.DBS_sreality import DBS_sreality

from bs4 import BeautifulSoup
from time import sleep
import random
import re
import math

# RUN WITH COMMAND:
# scrapy crawl sreality

# Useful YT:
# https://www.youtube.com/watch?v=ALizgnSFTwQ
# https://www.youtube.com/watch?v=2LwrUu9yTAo

class SrealitySpider(scrapy.Spider):
    name = "sreality"
    allowed_domains = ["sreality.cz"]
    start_urls = ['https://www.sreality.cz/hledani/prodej/byty']
    PAGES = 25 # Number of pages to download

    def __init__(self, *args, **kwargs):
        super(SrealitySpider, self).__init__(*args, **kwargs)

        # Prepare database
        self.DB = DBS_sreality("postgres", "postgres", "my_super_strong_password", "127.0.0.1", "5432")
        self.DB.create_open_database()

        # Prepare Chrome Browser
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        self.SB = SelBrowser(driver_path)
        self.driver = self.SB.setup_browser()

    def number_of_pages(self, soup):
        # get the maximum number of pages
        # Code inspired with: https://github.com/JirkaZelenka/Sreality/blob/master/Sreality%20-%20Scraper.ipynb
        records = soup.find_all(class_ ='numero ng-binding')[1].text
        records = re.split(r'\D', str(records))
        records = ",".join(records).replace(",", "")
        records = int(records)
        max_page = math.ceil(records / 20)
        print("----------------")
        print("Scrapuji: Prodej byty" )
        print("Celkem inzerátů: " + str(records))
        print("Celkem stránek: " + str(max_page))
        return max_page

    def start_requests(self):
        url = self.start_urls[0]
        self.driver.get(url)
        sleep(random.uniform(1.0, 1.5))

        innerHTML = self.driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(innerHTML,'lxml')

        max_pages = self.number_of_pages(soup) # get number of pages
        self.PAGES = min(self.PAGES, max_pages) # to avoide going over limit

        # scrape URLs of single listings from all pages
        for i in range(self.PAGES):
            i = i+1
            print("PAGE: ", str(i) + '/' + str(self.PAGES))
            page_url = url + "?strana=" + str(i)
            yield scrapy.Request(url=page_url, callback=self.parse, meta={'page_url': page_url})

    def parse(self, response, **kwargs):
        # Recieved page url
        print("================================")
        page_url = response.meta['page_url']
        #print(page_url)
        #print(response.body)
        self.driver.get(page_url)
        sleep(random.uniform(1.0, 1.5))
        #print(self.driver.page_source)


        properties = self.driver.find_elements('css selector', 'div.property')
        for listing in properties:
            print("ANOTHER LISTING ----")

            # GET NAME
            name_html = listing.find_element('css selector', '.name.ng-binding')
            name = name_html.get_attribute('innerHTML')
            #print("NAME - ", name)

            # GET ADDRESS
            address_html = listing.find_element('css selector', '.locality.ng-binding')
            address = address_html.get_attribute('innerHTML')
            #print("LOCATION - ", address)

            headline = name + " " + address
            print("HEAD - ", headline)

            # GET IMG
            image_element = listing.find_element('css selector', 'img')
            img_url = image_element.get_attribute('src')
            print("IMG  - ",img_url)

            # GET URL
            item_url_html = listing.find_element('css selector', 'a[href^="/detail/prodej/"]')
            item_url = item_url_html.get_attribute('href')
            print('URL  - ', item_url)

            # GET ID
            id = item_url.split("/")[-1]
            print("ID   - ", id)

            # insert element into DB
            self.DB.insert_item(id, item_url, headline, img_url)
