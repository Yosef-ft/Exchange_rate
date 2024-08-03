import datetime

import scrapy
from RateScraper.items import ExchangeItem

class SiinqeeSpider(scrapy.Spider):
    name = "Siinqee"
    allowed_domains = ["siinqeebank.com"]
    start_urls = ["https://siinqeebank.com/#/"]

    def parse(self, response):
        
        data = response.css('table tr td::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 3:
                Rates.append(temp)
                temp = []  

        ## The website doesn't provide when the data has been updated
        now = datetime.datetime.now()
        date_string = now.strftime('%B %d, %Y')                

        for rate in Rates:
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = date_string
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['Buying'] = rate[1]
            exchange_rate['Selling'] = rate[2]

            yield exchange_rate
