from datetime import datetime
from typing import ClassVar, Type, Dict, List

import marshmallow
from dataclasses import field
from marshmallow import Schema, pre_load, EXCLUDE
from marshmallow_dataclass import dataclass


@dataclass
class Shop:
    id: int
    title: str
    html_url: str = field(metadata={"marshmallow_field": marshmallow.fields.Url()})
    reviews_rating: float
    reviews_count: int
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def process(self, data, many, **kwargs):
        reviews_rating = data['reviews'].get('rating')
        reviews_count = data['reviews'].get('count')
        data.update({'reviews_rating': reviews_rating, 'reviews_count': reviews_count})
        return data


@dataclass
class Position:
    id: str
    product_id: int
    shop_id: int
    price: float
    warranty: int
    date_update: datetime
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def process(self, data, many, **kwargs):
        price = data['position_price'].get('amount')
        date = datetime.strptime(data.get('date_update'), '%Y-%m-%dT%H:%M:%S+03:00').strftime('%Y-%m-%d %H:%M:%S')
        data.update({'price': price, 'date_update': date})
        return data


@dataclass
class Prices:
    shops: Dict[str, Shop]
    positions: List[Position]
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def process(self, data, many, **kwargs):
        data.update({'positions': data['positions'].get('primary')})
        return data

    def get_shops_values(self):
        return [tuple(shop.__dict__.values()) for shop in self.shops.values()]

    def get_positions_values(self):
        return [tuple(value for k, value in position.__dict__.items() if not k == 'id') for position in self.positions]
