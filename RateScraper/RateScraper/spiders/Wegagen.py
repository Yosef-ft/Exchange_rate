import scrapy


class WegagenSpider(scrapy.Spider):
    name = "Wegagen"
    allowed_domains = ["www.wegagen.com"]
    start_urls = ["https://www.wegagen.com/exchange-rate-cash-notes/"]

    def parse(self, response):
        
        data = response.css('table tbody tr td::text').getall()
        data = data[2:]

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 6:
                Rates.append(temp)
                temp = []


        for rate in Rates:
            yield{
                "Date" : response.css('table tbody tr td h6 strong::text').get(),
                "CurrencyCode" : rate[0],
                "CashBuying" : rate[2],
                "CashSelling" : rate[3],
                "TransactionalBuying" : rate[4],
                "TransactionalSelling" : rate[5]
            }
