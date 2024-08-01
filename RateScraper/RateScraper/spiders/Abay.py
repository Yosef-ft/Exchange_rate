import scrapy


class AbaySpider(scrapy.Spider):
    name = "Abay"
    allowed_domains = ["abaybank.com.et"]
    start_urls = ["https://abaybank.com.et"]

    def parse(self, response):        

        Rates = response.css('tbody.row-hover tr')
        
        for rate in Rates:
            yield{
                'Date' : response.css('table tr th.column-1::text').get(),
                'CurrencyCode' : rate.css('td.column-1::text').get(),
                'Buying' : rate.css('tr td.column-2::text').get(),
                'Selling' : rate.css('td.column-3::text').get()
            }


