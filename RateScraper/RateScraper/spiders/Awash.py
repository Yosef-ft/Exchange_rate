import scrapy


class AwashSpider(scrapy.Spider):
    name = "Awash"
    allowed_domains = ["awashbank.com"]
    start_urls = ["https://awashbank.com/exchange-historical/"]

    def parse(self, response):
        
        Rates = response.css('table tbody tr')
        Ind_Rates = [rate.css('td::text').getall() for rate in Rates]

        for rate in Ind_Rates:
            # print('**********')
            # print(rate[0], rate[1], rate[2], rate[3], rate)
            yield{
                'CurrencyCode' : rate[0],
                'CashBuying': rate[1],
                'CashSelling' : rate[2],
                'TransactionalBuying' : rate[3],
                'transactionalSelling' : rate[4],                
            }


