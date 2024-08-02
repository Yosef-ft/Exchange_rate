import scrapy
from RateScraper.items import ExchangeItem

class OromiaSpider(scrapy.Spider):
    name = "Oromia"
    allowed_domains = ["www.ob.oromiabank.com"]
    start_urls = ["https://www.ob.oromiabank.com"]

    def parse(self, response):
       
        symbol_src = response.css('table tbody tr td img::attr(src)').extract()

        symbols = []
        for sym in symbol_src:
            symbols.append(sym.split('1.png')[0][-3:])

        prices = response.css('table tbody tr td::text').getall()
        prices = prices[2:] 

        Rates = []
        for sym in symbols:
            temp = [sym]
            counter = 0
            for price in prices[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 2:
                    break
            Rates.append(temp)       

        for rate in Rates:
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = self.name
            exchange_rate["Date"] =  response.css('figcaption.wp-element-caption code::text').get()
            exchange_rate["CurrencyCode"] = rate[0]
            exchange_rate["Buying"] = rate[1]
            exchange_rate["Selling"] = rate[2]
            
            yield exchange_rate
           
