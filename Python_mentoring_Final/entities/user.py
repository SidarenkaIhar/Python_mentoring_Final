from typing import ClassVar, Type

from marshmallow import Schema
from marshmallow_dataclass import dataclass


@dataclass
class User:
    id: int
    chat_id: int
    email: str
    price_threshold: float
    currency_abbreviation: str
    Schema: ClassVar[Type[Schema]] = Schema

    def get_values(self):
        return tuple(self.__dict__.values())
