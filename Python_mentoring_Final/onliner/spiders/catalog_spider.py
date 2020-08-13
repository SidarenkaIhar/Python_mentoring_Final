import scrapy

from onliner.items.item import Item


class CatalogOnlinerSpider(scrapy.Spider):
    name = 'catalog_onliner_spider'
    allowed_domains = ['catalog.onliner.by']
    start_urls = []
    api_url = 'https://catalog.onliner.by/sdapi/catalog.api/products/{}'

    def parse(self, response):
        return Item.Schema().loads(response.text)
