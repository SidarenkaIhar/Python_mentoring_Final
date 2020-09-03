import scrapy

from entities.currency import Currency


class CurrencySpider(scrapy.Spider):
    name = 'currency_spider'
    allowed_domains = ['www.nbrb.by']
    start_urls = []
    api_url = 'https://www.nbrb.by/api/exrates/rates/{}?parammode=2'

    def parse(self, response, **kwargs):
        return Currency.Schema().loads(response.text)
