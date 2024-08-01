import scrapy


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
            yield{
                "Date" : response.css('table thead tr th span.text-uppercase::text').get(),
                "CurrencyCode" : rate[0],
                "Buying" : rate[1],
                "Selling" : rate[2],
            }
