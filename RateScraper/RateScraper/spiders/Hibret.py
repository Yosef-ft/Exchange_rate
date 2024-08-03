import scrapy
from RateScraper.items import ExchangeItem

class HibretSpider(scrapy.Spider):
    name = "Hibret"
    allowed_domains = ["www.hibretbank.com.et"]
    start_urls = ["https://www.hibretbank.com.et/"]

    def parse(self, response):
        
        data =  response.css('table tr td::text').getall()

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
            exchange_rate['Date'] = response.css('table tr th::text').get()
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['Buying'] = rate[1]
            exchange_rate['Selling'] = rate[2]

            yield exchange_rate        
