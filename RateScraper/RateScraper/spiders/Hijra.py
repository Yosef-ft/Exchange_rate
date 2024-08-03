import scrapy
from RateScraper.items import FullExchangeItems

class HijraSpider(scrapy.Spider):
    name = "Hijra"
    allowed_domains = ["hijra-bank.com"]
    start_urls = ["https://hijra-bank.com/"]

    def parse(self, response):
        
        data = response.css('table tbody tr td::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 5:
                Rates.append(temp)
                temp = []          

        for rate in Rates:
            exchange_rate = FullExchangeItems()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css("meta[property='article:modified_time']::attr(content)").get()[:10]
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['CashBuying']= rate[1]
            exchange_rate['CashSelling'] = rate[2]
            exchange_rate['TransactionalBuying'] = rate[3]
            exchange_rate['TransactionalSelling'] = rate[4]               
            
            yield exchange_rate         