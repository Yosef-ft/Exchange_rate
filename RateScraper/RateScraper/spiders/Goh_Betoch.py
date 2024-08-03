import scrapy
from RateScraper.items import ExchangeItem

class GohBetochSpider(scrapy.Spider):
    name = "Goh_Betoch"
    allowed_domains = ["www.gohbetbank.com"]
    start_urls = ["https://www.gohbetbank.com/exchange-rate/"]

    def parse(self, response):
        
        symbols = response.css('table tr td p strong::text').getall()
        prices = response.css('table tr td p::text').getall()
        prices = [price for price in prices if price != ' ']

        Rates = []
        temp = []
        for rate in prices:
            temp.append(rate)
            if len(temp) == 3:
                Rates.append(temp)
                temp = []  

        for i in range(0, len(Rates)):
            Rates[i][0] = symbols[i]

        for rate in Rates:
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css('div.elementor-widget-container p::text').getall()[1][14:]
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['Buying'] = rate[1]
            exchange_rate['Selling'] = rate[2]

            yield exchange_rate               
