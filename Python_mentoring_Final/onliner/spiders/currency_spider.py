import scrapy

from onliner.items.currency import Currency


class CurrencySpider(scrapy.Spider):
    name = 'currency_spider'
    allowed_domains = ['www.nbrb.by']
    start_urls = []
    api_url = 'https://www.nbrb.by/api/exrates/rates/{}'

    def parse(self, response):
        return Currency.Schema().loads(response.text)
