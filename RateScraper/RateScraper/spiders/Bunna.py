import datetime

import scrapy
from RateScraper.items import FullExchangeItems

class BunnaSpider(scrapy.Spider):
    name = "Bunna"
    allowed_domains = ["bunnabanksc.com"]
    start_urls = ["https://bunnabanksc.com/"]
  
    def parse(self, response):
        
        data = response.css('table tbody tr td div span::text').getall()
        data = [rate.replace('\t', '').replace('\n','') for rate in data]
        data = [rate for rate in data if rate != ' ' and rate != '' ]

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 5:
                Rates.append(temp)
                temp = []             
                    

        ## Constantly changing their website this is just half the data
        for rate in Rates:
            exchange_rate = FullExchangeItems()            
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css('div.elementor-element div.elementor-widget-container h4::text').get()
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['CashBuying']= rate[1]
            exchange_rate['CashSelling'] = rate[2]
            exchange_rate['TransactionalBuying'] = rate[3]
            exchange_rate['TransactionalSelling'] = rate[4]  

            yield exchange_rate          