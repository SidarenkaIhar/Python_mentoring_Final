import logging
from multiprocessing.context import Process

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import project_settings
from onliner_parser.spiders.catalog_spider import CatalogOnlinerSpider
from onliner_parser.spiders.currency_spider import CurrencySpider
from onliner_parser.spiders.shops_spider import ShopsOnlinerSpider

logging.basicConfig(filename=project_settings.LOG_FILE, format=project_settings.LOG_FORMAT,
                    level=project_settings.LOG_LEVEL)
_logger = logging.getLogger(__name__)

_prohibited_suffix = ('prices', 'reviews', 'create')


def parse_items(items):
    _parse_in_new_process(CatalogOnlinerSpider, items)


def parse_currencies(currencies):
    _parse_in_new_process(CurrencySpider, currencies)


def parse_prices(items):
    _parse_in_new_process(ShopsOnlinerSpider, items)


def _parse_in_new_process(spider, entities):
    process = Process(target=_parse_entities, args=(spider, entities))
    process.start()
    process.join()


def _parse_entities(spider, items):
    spider.start_urls = []
    for item in items:
        if item:
            if not item.isalnum():
                split_url = [name for name in item.split('/') if name.isalnum() and name not in _prohibited_suffix]
                if not split_url:
                    _logger.warning(f"Incorrect url or item: {item}")
                    continue
                item = split_url.pop()
            spider.start_urls.append(spider.api_url.format(item))
    _start_crawler(spider)


def _start_crawler(spider):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)
    process.start()
