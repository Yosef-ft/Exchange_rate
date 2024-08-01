import scrapy


class BerhanSpider(scrapy.Spider):
    name = "Berhan"
    allowed_domains = ["berhanbanksc.com"]
    start_urls = ["https://berhanbanksc.com/exchange-rates/"]

    def parse(self, response):
        
        prices = response.css('div.row div.col-3::text').getall()
        prices = prices[2:]
        prices = [price.strip() for price in prices]

        symbols = response.css('div.row div.col-6 span::text').getall()
        symbols = [symbol.strip().split()[1] for symbol in symbols if symbol.strip() != '']

        Rates = []
        for sym in symbols:
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
                "Date" : response.css('div.innerContainer h3::text').get().strip(),
                "CurrencyCode" : rate[0],
                "Buying" : rate[1],
                "Selling" : rate[2],
            }
