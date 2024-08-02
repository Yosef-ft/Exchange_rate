# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RatescraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


# This only includes cash rates
class ExchangeItem(scrapy.Item):
    Date = scrapy.Field()
    CurrencyCode = scrapy.Field()
    Buying = scrapy.Field()
    Selling = scrapy.Field()

# This items include both the transaction and cash rates
class FullExchangeItems(scrapy.Item):
    bank = scrapy.Field()
    Date = scrapy.Field()
    CurrencyCode = scrapy.Field()
    TransactionalBuying = scrapy.Field()
    TransactionalSelling = scrapy.Field()
    CashBuying = scrapy.Field()
    CashSelling = scrapy.Field()