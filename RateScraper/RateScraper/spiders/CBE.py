import scrapy
import json

class CbeSpider(scrapy.Spider):
    name = "CBE"
    allowed_domains = ["combanketh.et"]
    start_urls = ["https://combanketh.et"]

    headers = {
        "accept" : "application/json, text/plain, */*",
        "accept-encoding" : "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "referer" : "https://combanketh.et/en/exchange-rate/",
        "sec-fetch-mode" : "cors",
        "sec-fetch-site" : "same-origin",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        "X-Requested-With" : "Fetch"
    }

    def parse(self, response):
        url = 'https://combanketh.et/cbeapi/daily-exchange-rates?_limit=1&_sort=Date%3ADESC'

        request = scrapy.Request(url,
                                 callback= self.parse_api,
                                 headers = self.headers)
        
        yield request
    
    def parse_api(self, response):
        
        raw_data = response.body
        data = json.loads(raw_data)[0]

        for rate in data['ExchangeRate']:
            yield {
                'Date' : data['Date'],
                'CashBuying': rate['cashBuying'],
                'CashSelling' : rate['cashSelling'],
                'TransactionalBuying' : rate['transactionalBuying'],
                'transactionalSelling' : rate['transactionalSelling'],
                'CurrencyCode' : rate['currency']['CurrencyCode'],
                'CurrencyName' : rate['currency']['CurrencyName']
            }




