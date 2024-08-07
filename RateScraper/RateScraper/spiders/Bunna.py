import datetime

import scrapy
from RateScraper.items import FullExchangeItems

class BunnaSpider(scrapy.Spider):
    name = "Bunna"
    allowed_domains = ["bunnabanksc.com"]
    start_urls = ["https://bunnabanksc.com/"]
  
    def parse(self, response):
        
        data =response.css('table tbody tr td::text').getall()
        data = [rate.replace('\t', '').replace('\n','').strip() for rate in data]
        data = [rate.strip() for rate in data if rate != ' ' and rate != '' ]

        cash_rate = data[:len(data) //2]
        trans_rate = data[len(data) //2 :]

        Rates = []
        temp = []
        for i in range(0,len(cash_rate), 4):
            temp = [cash_rate[0+i]]
            temp.append(cash_rate[2+i])
            temp.append(cash_rate[3+i])
            temp.append(trans_rate[2+i])
            temp.append(trans_rate[3+i])
            Rates.append(temp)
            temp = []
              
                    

        ## Constantly changing their website this is just half the data
        for rate in Rates:
            exchange_rate = FullExchangeItems()            
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css('div.wpr-grid-item-date div.inner-block span::text').get()
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['CashBuying']= rate[1]
            exchange_rate['CashSelling'] = rate[2]
            exchange_rate['TransactionalBuying'] = rate[3]
            exchange_rate['TransactionalSelling'] = rate[4]  

            yield exchange_rate          