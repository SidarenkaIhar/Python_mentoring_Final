from dataclasses import field
from typing import ClassVar, Type

from marshmallow import Schema, EXCLUDE, pre_load, fields
from marshmallow_dataclass import dataclass


@dataclass
class Item:
    id: int
    key: str
    extended_name: str
    price: float
    html_url: str = field(metadata={"marshmallow_field": fields.Url()})
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def process(self, data, many, **kwargs):
        price = data['prices']['price_min'].get('amount') if data.get('prices') else 0
        data.update({'price': price})
        return data

    def get_values(self):
        return tuple(self.__dict__.values())
