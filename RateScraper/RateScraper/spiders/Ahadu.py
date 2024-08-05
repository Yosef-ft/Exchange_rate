import scrapy
from RateScraper.items import ExchangeItem

class AhaduSpider(scrapy.Spider):
    name = "Ahadu"
    allowed_domains = ["ahadubank.com"]
    start_urls = ["https://ahadubank.com/"]

    def parse(self, response):
        
        symbols = response.css('div.elementor-icon-box-content h6 span::text').getall()
        prices = response.css('div.elementor-icon-box-content p::text').getall()
        prices = prices[2:]
        prices =[rate.split(':')[1] for rate in prices]

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
            exchange_rate["Date"] = response.css('div.elementor-widget-container h5.litho-heading span.litho-primary-title ::text').getall()[-1]  
            exchange_rate["CurrencyCode"] = rate[0]
            exchange_rate["Buying"] = rate[1]
            exchange_rate["Selling"] = rate[2]

            yield exchange_rate            