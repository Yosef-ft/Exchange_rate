import scrapy


class SiinqeeSpider(scrapy.Spider):
    name = "Siinqee"
    allowed_domains = ["siinqeebank.com"]
    start_urls = ["https://siinqeebank.com/#/"]

    def parse(self, response):
        pass
