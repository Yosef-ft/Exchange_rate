import scrapy
from RateScraper.items import ExchangeItem

class EnatSpider(scrapy.Spider):
    name = "Enat"
    allowed_domains = ["www.enatbanksc.com"]
    start_urls = ["https://www.enatbanksc.com"]

    def parse(self, response):
        
        datas = response.css('tbody tr td::text').getall()
        datas = [data for data in datas if data != '\n']


        rates = []
        temp = []
        for i in range(0, len(datas)):
            temp.append(datas[i])
            try:
                float(datas[i+1])
                temp.append(datas[i+1])
                temp.append(datas[i+2])
                rates.append(temp)
            except:
                temp = []


        dup_Rates = []
        for rate in rates:
            dup_Rates.append(rate[:3])


        Rates = []
        for i in range(0, len(dup_Rates), 2):
            Rates.append(dup_Rates[i])

        
        for rate in Rates:
            exchange_rate = ExchangeItem()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css('div.et_pb_text_inner h2 strong::text').get().split()[-1]
            exchange_rate["CurrencyCode"] = rate[0]
            exchange_rate["Buying"] = rate[1]
            exchange_rate["Selling"] = rate[2]        

            yield exchange_rate    