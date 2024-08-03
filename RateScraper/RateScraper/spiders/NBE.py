import scrapy
import json
from RateScraper.items import ExchangeItem

class NbeSpider(scrapy.Spider):
    name = "NBE"
    allowed_domains = ["api.nbe.gov.et"]
    start_urls = ["https://api.nbe.gov.et/api/filter-transaction-exchange"]

    def parse(self, response):
        
        raw_data = response.body
        data = json.loads(raw_data)

        price_data = data['data']

        for rate in price_data: 
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = rate['date']
            exchange_rate["CurrencyCode"] = rate['currency']['code']
            exchange_rate["Buying"] = rate['buying']
            exchange_rate["Selling"] = rate['selling']     

            yield exchange_rate          


