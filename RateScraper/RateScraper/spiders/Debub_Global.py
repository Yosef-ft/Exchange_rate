import scrapy
from RateScraper.items import ExchangeItem


class DebubGlobalSpider(scrapy.Spider):
    name = "Debub_Global"
    allowed_domains = ["www.globalbankethiopia.com"]
    start_urls = ["https://www.globalbankethiopia.com"]

    def parse(self, response):
        
        data = response.css('table tr td div div p::text').getall()
        symbol = response.css('table tr td div div p strong::text').getall()
        symbol = symbol[3:]

        Rates = []
        for sym in symbol:
            temp = [sym]
            counter = 0
            for price in data[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 2:
                    break
            Rates.append(temp)


        for rate in Rates:
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = self.name
            exchange_rate["Date"] =  response.css('div.elementor-shortcode ::text').get()
            exchange_rate["CurrencyCode"] = rate[0]
            exchange_rate["Buying"] = rate[1]
            exchange_rate["Selling"] = rate[2]

            yield exchange_rate
