
from bigcrawler.crawler import BaseSpider


class SeleniumSpider(BaseSpider):

    name = "selenium"

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'crawler.middlewares.SeleniumMiddleware': 201,
        },
        "DOWNLOAD_TIMEOUT": 60
    }
