
import scrapy


class BigdataCrawlerItem(scrapy.Item):
    # name = scrapy.Field()

    data = scrapy.Field()
    filename = scrapy.Field()
    headers = scrapy.Field()
