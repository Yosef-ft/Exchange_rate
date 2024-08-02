import scrapy
from RateScraper.items import FullExchangeItems

class DashenSpider(scrapy.Spider):
    name = "Dashen"
    allowed_domains = ["dashenbanksc.com"]
    start_urls = ["https://dashenbanksc.com"]

    def parse(self, response):
        
        data = response.css('table tr td::text').getall()
        
        # Rates include symbol, buying and selling both cash and transaction but duplicated
        temp = []
        Rates = []
        for i in range(0, len(data), 4):
            temp.append(data[i])
            temp.append(data[i+1])
            temp.append(data[i+2])
            temp.append(data[i+3])
            if len(temp) == 4:
                Rates.append(temp)
                temp = []

        Rates = sorted(Rates)

        # The duplicated rates
        dup_Rates = []
        for i in range(0, len(Rates)-1):
            if Rates[i][0] == Rates[i + 1][0]:
                dup_Rates.append(Rates[i])
                dup_Rates.append(Rates[i+1])

        # Joins the Duplicated rates
        Dup_Rates = []
        for i in range(0, len(dup_Rates), 2):
            Dup_Rates.append(dup_Rates[i] + dup_Rates[i+1])

        # Rates that are not duplicated i.e, rates that don't have trasaction rates
        single_rates = [rate for rate in Rates if rate[0] not in [r[0] for r in dup_Rates]]

        # One rate includes the cash and trasaction rates for the duplicated rates
        main_rate = []
        one_rate = []
        for rate in Dup_Rates:
            main_rate.append(rate[0])
            main_rate.append(rate[1])
            main_rate.append(rate[2])
            main_rate.append(rate[3])
            main_rate.append(rate[6])
            main_rate.append(rate[7])
            if len(main_rate) == 6:
                one_rate.append(main_rate)
                main_rate = []

        total_rates = one_rate + single_rates

        for rate in total_rates:
            exchange_rate = FullExchangeItems()
            exchange_rate['bank'] = self.name
            exchange_rate['Date'] = response.css('div.et_pb_text_inner h4::text').get()[14:]
            exchange_rate['CurrencyCode'] = rate[0]
            exchange_rate['CashBuying'] = rate[2]
            exchange_rate['CashSelling'] = rate[3]
            try:
                exchange_rate['TransactionalBuying'] = rate[4]
            except:
                exchange_rate['TransactionalBuying'] = rate[2]
            try:
                exchange_rate['TransactionalSelling'] = rate[5]    
            except:
                exchange_rate['TransactionalSelling'] = rate[3]       

            yield exchange_rate 
