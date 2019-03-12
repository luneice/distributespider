# -*- coding: utf-8 -*-

BOT_NAME = 'googlebot'

SPIDER_MODULES = ['distributespider.spiders']
NEWSPIDER_MODULE = 'distributespider.spiders'
USER_AGENT = "Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; " \
             "HTC Sensation Build/IML74K) AppleWebKit/534.30 " \
             "(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1000
# LOG_LEVEL = 'INFO'  # 日志级别
# RETRY_ENABLED = False  # 重新请求
# DOWNLOAD_TIMEOUT = 12  # 下载超时
AJAXCRAWL_ENABLED = True
# REDIRECT_ENABLED = False  # 重定向
# DOWNLOAD_DELAY = 1
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
# COOKIES_ENABLED = False
# TELNETCONSOLE_ENABLED = False
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }
# 爬虫中间件

# SPIDER_MIDDLEWARES = {
#    'distributespider.middlewares.MyCustomSpiderMiddleware': 543,
# }

DOWNLOADER_MIDDLEWARES = {
    # 'distributespider.downloader_middlewares.ProxyMiddleware': 500,
}

# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

ITEM_PIPELINES = {
    'distributespider.pipelines.TmalllistspiderPipeline': 300,
    'distributespider.pipelines.TmalllistMongoPipeline': 301,
    'distributespider.pipelines.TmallDetailPipeline': 302,
    'distributespider.pipelines.TmallRateSpiderPipeline': 303,
    'distributespider.pipelines.TaobaoPipeline': 304,
    'distributespider.pipelines.TaobaoPipelineDetail': 305,
    'distributespider.pipelines.JdspiderPipeline': 306,
}

# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 5
# AUTOTHROTTLE_MAX_DELAY = 60
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# AUTOTHROTTLE_DEBUG = False
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
