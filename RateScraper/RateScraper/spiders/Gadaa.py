import scrapy
from RateScraper.items import ExchangeItem

class GadaaSpider(scrapy.Spider):
    name = "Gadaa"
    allowed_domains = ["www.gadaabank.com.et"]
    start_urls = ["https://www.gadaabank.com.et/"]

    def parse(self, response):
        
        data = response.css('table tbody tr td::text').getall()
        data = data[4:]

        Rates = []
        temp = []
        for i in range(0, len(data) - 4, 4):
            temp.append(data[i])
            temp.append(data[i+1])
            temp.append(data[i+2])
            Rates.append(temp)
            temp = []

        Rates = Rates[:(len(Rates) //2)]

        for rate in Rates:
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css('div.elementor-shortcode p.wpdt-c::text').get()[:-14]
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['Buying'] = rate[1]
            exchange_rate['Selling'] = rate[2]

            yield exchange_rate

