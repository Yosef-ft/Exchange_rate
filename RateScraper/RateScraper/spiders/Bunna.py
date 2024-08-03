import datetime

import scrapy
from RateScraper.items import ExchangeItem

class BunnaSpider(scrapy.Spider):
    name = "Bunna"
    allowed_domains = ["bunnabanksc.com"]
    start_urls = ["https://bunnabanksc.com/foreign-exchange/"]

    def parse(self, response):
        
        data = response.css('table tbody tr td::text').getall()

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

        ## Constantly changing their website this is just half the data
        for rate in Rates[:3]:
            exchange_rate = ExchangeItem()            
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = date_string
            exchange_rate["CurrencyCode"] = rate[0]
            exchange_rate["Buying"] = rate[1]
            exchange_rate["Selling"] = rate[2]     

            yield exchange_rate          