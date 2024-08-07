import scrapy
from RateScraper.items import FullExchangeItems

class GadaaSpider(scrapy.Spider):
    name = "Gadaa"
    allowed_domains = ["www.gadaabank.com.et"]
    start_urls = ["https://www.gadaabank.com.et/"]

    def parse(self, response): 
        
        data = response.css('table tbody tr td::text').getall()
        data = data[8:]
        data =  data[: len(data) //2 ]

        Rates = []
        temp = []
        for i in range(0, len(data) - 4, 6):
            temp.append(data[i])
            temp.append(data[i+1])
            temp.append(data[i+2])
            temp.append(data[i+3])
            temp.append(data[i+4])
            Rates.append(temp)
            temp = []


        for rate in Rates:
            exchange_rate = FullExchangeItems()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css('div.elementor-shortcode p.wpdt-c::text').get()[:-14]
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['CashBuying'] = rate[1]
            exchange_rate['CashSelling'] = rate[2]
            exchange_rate['TransactionalBuying'] = rate[3]
            exchange_rate['TransactionalSelling'] = rate[4]
            yield exchange_rate

