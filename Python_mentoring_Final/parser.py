import time

import schedule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from analyzer import analyze_prices
from manager.spiders_manager import get_items_spider, get_currencies_spider, get_prices_spider
from multiprocessing.context import Process

items = ('https://catalog.onliner.by/faucet/kaisergmbh/saga53022/reviews/create?region=minsk',
         'https://catalog.onliner.by/faucet/kaisergmbh/decor401445n', 'oled55c8pla')
currencies_ids = ('145',)


def parse_items():
    process = CrawlerProcess(get_project_settings())
    process.crawl(get_items_spider(items))
    process.crawl(get_currencies_spider(currencies_ids))
    process.start()


def parse_prices():
    process = CrawlerProcess(get_project_settings())
    process.crawl(get_currencies_spider(currencies_ids))
    process.crawl(get_prices_spider(items))
    process.start()
    analyze_prices()


def parse():
    process = Process(target=parse_prices)
    process.start()
    process.join()


if __name__ == "__main__":
    parse_items()
    schedule.every(1).minutes.do(parse)
    # schedule.every(8).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
