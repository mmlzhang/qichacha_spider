
import os

from bigcrawler.settings import DATA_PATH, LOG_PATH


BOT_NAME = 'crawler'

SPIDER_MODULES = [
    'crawler.qcc',
]
NEWSPIDER_MODULE = SPIDER_MODULES[-1]

ROBOTSTXT_OBEY = False

# 同时请求并发数
CONCURRENT_REQUESTS = 4

# 下载延时
# DOWNLOAD_DELAY = 2
# 超时设置
# DOWNLOAD_TIMEOUT = 10
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 8
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True


USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/71.0.3578.80 Safari/537.36')

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
}

# middleware
DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.ProxyMiddleware': 200,
}

# sentry
SENTRY_DSN = 'https://543a8103c2da4df6b012dd0bcda1e560@sentry.bigkf.com/11'
EXTENSIONS = {
    "crawler.utils.sentry.Sentry": 100,
    "crawler.utils.stats.StatsPersistence": 101,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'crawler.pipelines.BigdataCrawlerPipeline': 300,
}

DEPTH_LIMIT = 10
DEPTH_PRIORITY = 0  # 深度优先

# retry 优先
RETRY_PRIORITY_ADJUST = 1
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# DATA_PATH = os.path.join("/var/app/data", "bigcrawler")
# LOG_PATH = os.path.join("/var/app/log", "bigcrawler")

LOG_LEVEL = 'DEBUG'

PROXY_IP = " "

PROXIES = {
    'http': PROXY_IP,
    'https': PROXY_IP
}

DAY_FORMAT = "%Y-%m-%d"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
