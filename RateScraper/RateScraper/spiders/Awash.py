import scrapy
from RateScraper.items import FullExchangeItems


class AwashSpider(scrapy.Spider):
    name = "Awash"
    allowed_domains = ["awashbank.com"]
    start_urls = ["https://awashbank.com/exchange-historical/"]

    def parse(self, response):
        
        Rates = response.css('table tbody tr')
        Ind_Rates = [rate.css('td::text').getall() for rate in Rates]

        for rate in Ind_Rates:
            exchange_rate = FullExchangeItems()
            exchange_rate['bank'] = 'Awash'
            exchange_rate['Date'] = response.css('div.exchange-rates-header span::text').get()
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['CashBuying']= rate[1]
            exchange_rate['CashSelling'] = rate[2]
            exchange_rate['TransactionalBuying'] = rate[3]
            exchange_rate['TransactionalSelling'] = rate[4]               
            
            yield exchange_rate


