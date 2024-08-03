import scrapy
from RateScraper.items import ExchangeItem

class AmharaSpider(scrapy.Spider):
    name = "Amhara"
    allowed_domains = ["www.amharabank.com.et"]
    start_urls = ["https://www.amharabank.com.et/exchange-rate/"]

    def parse(self, response):
        
        data = response.css('table tbody tr td div span span::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 3:
                Rates.append(temp)
                temp = []          

        day_month = response.css('div.elementor-widget-container p::text').getall()[5]
        day_month= day_month.split()[-2:]
        day_month = ' '.join(day_month)
        year = response.css('div.elementor-widget-container p span::text').get()[:-1]
        Date = day_month + year

        for rate in Rates:
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = Date
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['Buying'] = rate[1]
            exchange_rate['Selling'] = rate[2]

            yield exchange_rate