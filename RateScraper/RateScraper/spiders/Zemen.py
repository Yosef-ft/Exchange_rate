import scrapy
from RateScraper.items import ExchangeItem


class ZemenSpider(scrapy.Spider):
    name = "Zemen"
    allowed_domains = ["zemenbank.com"]
    start_urls = ["https://zemenbank.com/exchange-rates"]

    def parse(self, response):
        
        symbol = response.css('table tbody tr.currency-entry td.currency-identity div.media div.media-body h4::text').getall()
        prices = response.css('table tbody tr.currency-entry td h5::text').getall()

        Rates = []
        for sym in symbol:
            temp = [sym]
            counter = 0
            for price in prices:
                temp.append(price)
                counter += 1
                if counter == 2:
                    break
            Rates.append(temp)

        for rate in Rates:
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = 'Zemen'
            exchange_rate["Date"] = response.css('table thead tr th span.text-uppercase::text').get()
            exchange_rate["CurrencyCode"] = rate[0]
            exchange_rate["Buying"] = rate[1]
            exchange_rate["Selling"] = rate[2]

            yield exchange_rate
            
