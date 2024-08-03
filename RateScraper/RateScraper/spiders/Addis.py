import scrapy
from RateScraper.items import ExchangeItem

class AddisSpider(scrapy.Spider):
    name = "Addis"
    allowed_domains = ["addisbanksc.com"]
    start_urls = ["https://addisbanksc.com/exchange-rate/"]

    def parse(self, response):
        
        data =  response.css('table tbody tr td::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 3:
                Rates.append(temp)
                temp = []        

        for rate in Rates:
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css('tfoot tr th.column-2::text').get()
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['Buying'] = rate[1]
            exchange_rate['Selling'] = rate[2]

            yield exchange_rate
