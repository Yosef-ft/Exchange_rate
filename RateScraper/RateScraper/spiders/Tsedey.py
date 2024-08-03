import scrapy


class TsedeySpider(scrapy.Spider):
    name = "Tsedey"
    allowed_domains = ["tsedeybank-sc.com"]
    start_urls = ["https://tsedeybank-sc.com/"]

    def parse(self, response):
        pass
