import scrapy
from RateScraper.items import FullExchangeItems

class TsehaySpider(scrapy.Spider):
    name = "Tsehay"
    allowed_domains = ["tsehaybank.com.et"]
    start_urls = ["https://tsehaybank.com.et/exchange-rate/"]

    def parse(self, response):
        
        data = response.css('table tbody tr td::text').getall()
        symbols = response.css('table tbody tr td span b::text').getall()
        
        Rates = []
        for sym in symbols:
            temp = [sym]
            counter = 0
            for price in data[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 4:
                    break
            Rates.append(temp)    

        for rate in Rates:
            exchange_rate = FullExchangeItems()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css('div.elementor-widget-container h3.elementor-heading-title::text').get()[21:]
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['CashBuying']= rate[1]
            exchange_rate['CashSelling'] = rate[2]
            exchange_rate['TransactionalBuying'] = rate[3]
            exchange_rate['TransactionalSelling'] = rate[4]               
            
            yield exchange_rate                 