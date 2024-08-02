import scrapy
from RateScraper.items import FullExchangeItems

class WegagenSpider(scrapy.Spider):
    name = "Wegagen"
    allowed_domains = ["www.wegagen.com"]
    start_urls = ["https://www.wegagen.com/exchange-rate-cash-notes/"]

    def parse(self, response):
        
        data = response.css('table tbody tr td::text').getall()
        data = data[2:]

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 6:
                Rates.append(temp)
                temp = []


        for rate in Rates:
            exchange_rate = FullExchangeItems()
            exchange_rate['bank'] = 'Wegagen'
            exchange_rate["Date"] = response.css('table tbody tr td h6 strong::text').get()
            exchange_rate["CurrencyCode"] = rate[0]
            exchange_rate["CashBuying"] = rate[2]
            exchange_rate["CashSelling"] = rate[3]
            exchange_rate["TransactionalBuying"] = rate[4]
            exchange_rate["TransactionalSelling"] = rate[5]

            yield exchange_rate
