import datetime

import scrapy
from RateScraper.items import ExchangeItem

class TsedeySpider(scrapy.Spider):
    name = "Tsedey"
    allowed_domains = ["tsedeybank-sc.com"]
    start_urls = ["https://tsedeybank-sc.com/"]

    def parse(self, response):
        
        symbols = response.css('table tbody tr td div div div h4::text').getall()
        prices = response.css('table tbody tr td div div p::text').getall()

        Rates = []
        for sym in symbols:
            temp = [sym]
            counter = 0
            for price in prices[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 2:
                    break
            Rates.append(temp)          

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
        
