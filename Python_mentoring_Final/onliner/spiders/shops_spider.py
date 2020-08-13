import scrapy

from onliner.items.shop import Prices


class ShopsOnlinerSpider(scrapy.Spider):
    name = 'shops_onliner_spider'
    allowed_domains = ['catalog.onliner.by']
    start_urls = []
    api_url = 'https://catalog.onliner.by/sdapi/shop.api/products/{}/positions'

    def parse(self, response):
        return Prices.Schema().loads(response.text)
