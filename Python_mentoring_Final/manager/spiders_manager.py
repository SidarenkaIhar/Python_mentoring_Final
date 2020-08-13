from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from onliner.spiders.catalog_spider import CatalogOnlinerSpider
from onliner.spiders.currency_spider import CurrencySpider
from onliner.spiders.shops_spider import ShopsOnlinerSpider

_process = CrawlerProcess(get_project_settings())
_prohibited_suffix = ('prices', 'reviews', 'create')


def get_items_spider(items):
    return _handle_items(CatalogOnlinerSpider, items)


def get_currencies_spider(currencies_ids):
    return _handle_items(CurrencySpider, currencies_ids)


def get_prices_spider(items):
    return _handle_items(ShopsOnlinerSpider, items)


def _handle_items(spider, items):
    spider.start_urls = []
    for item in items:
        if item:
            try:
                if not item.isalnum():
                    split_url = [name for name in item.split('/') if name.isalnum() and name not in _prohibited_suffix]
                    item = split_url.pop()
                if isinstance(spider, CurrencySpider) and not item.isdigit():
                    raise IndexError
            except IndexError:
                spider.logger.warning(f"Incorrect url or item: {item}")
                continue
            spider.start_urls.append(spider.api_url.format(item))
    return spider
