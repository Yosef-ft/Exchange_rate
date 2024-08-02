import scrapy
from RateScraper.items import ExchangeItem


class NibSpider(scrapy.Spider):
    name = "Nib"
    allowed_domains = ["www.nibbanksc.com"]
    start_urls = ["https://www.nibbanksc.com"]

    def parse(self, response):
        
        data = response.css('table.ea-advanced-data-table tbody tr td::text').getall()

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
            exchange_rate['Date'] = response.css('table thead tr th::text').get()
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['Buying'] = rate[1]
            exchange_rate['Selling'] = rate[2]

            yield exchange_rate