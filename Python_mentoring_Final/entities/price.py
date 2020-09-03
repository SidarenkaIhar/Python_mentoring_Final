from dataclasses import field
from datetime import datetime
from typing import ClassVar, Type, Dict, List

import marshmallow
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
        position_date = datetime.strptime(data.get('date_update'), '%Y-%m-%dT%H:%M:%S+03:00')
        position_id = f"{data.get('shop_id')}:{data.get('product_id')}:{position_date.strftime('%Y%m%d%H%M%S')}"
        price = data['position_price'].get('amount')
        date = position_date.strftime('%Y-%m-%d %H:%M:%S')
        data.update({'id': position_id, 'price': price, 'date_update': date})
        return data

    def __post_init__(self):
        if isinstance(self.date_update, str):
            self.date_update = datetime.strptime(self.date_update, '%Y-%m-%d %H:%M:%S')


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
        return [tuple(position.__dict__.values()) for position in self.positions]
