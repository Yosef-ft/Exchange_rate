import scrapy
from RateScraper.items import ExchangeItem

class AbaySpider(scrapy.Spider):
    name = "Abay"
    allowed_domains = ["abaybank.com.et"]
    start_urls = ["https://abaybank.com.et/exchange-rates/"]

    def parse(self, response):        

        Rates = response.css('tbody.row-hover tr')
        
        # Currency code needs to be cleaned contains `\xa0`

        for rate in Rates:
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css('table tr th.column-1::text').get()
            exchange_rate['CurrencyCode'] = rate.css('td.column-1::text').get() 
            exchange_rate['Buying'] = rate.css('tr td.column-2::text').get() 
            exchange_rate['Selling'] = rate.css('td.column-3::text').get() 
            
            yield exchange_rate


