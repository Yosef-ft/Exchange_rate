import scrapy


class BoaSpider(scrapy.Spider):
    name = "BOA"
    allowed_domains = ["www.bankofabyssinia.com"]
    start_urls = ["https://www.bankofabyssinia.com"]

    def parse(self, response):
        
        Rates = response.css('table tbody tr')
        Ind_rates = [rate.css('td ::text') for rate in Rates]

        all_data = []

        for rate in Ind_rates:
            all_data.append(rate.getall())


        cash_data = []
        
        for rate in Ind_rates:
            if 'Transaction' in ' '.join(rate.getall()):
                break
            cash_data.append(rate.getall())
        

        trans_data = all_data[len(cash_data):]
        trans_data = trans_data[2:]
        trans_data = trans_data[:-1]

        cash_data = cash_data[2:]

        trans_common = [row for row in trans_data if row[0] in [r[0] for r in cash_data]]
        
        cash_common = [row for row in cash_data if row[0] in [r[0] for r in trans_data]]
        cash_common = sorted(cash_common)
        trans_common = sorted(trans_common)


        for i in range(len(cash_common)):
            yield{
                'CurrencyCode' : cash_common[i][0],
                'CashBuying' : cash_common[i][1],
                'CashSelling' : cash_common[i][2],
                'TransactionalBuying' : trans_common[i][1],
                'TransactionalSelling' : trans_common[i][2],
            }

