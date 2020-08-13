from datetime import datetime
from typing import ClassVar, Type

from marshmallow import Schema, EXCLUDE, fields, pre_load
from marshmallow_dataclass import dataclass


@dataclass
class Currency:
    date: datetime
    abbreviation: str = fields.Str()
    rate: float = fields.Float()
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def process(self, data, many, **kwargs):
        date = datetime.strptime(data.get('Date'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        abbreviation = data.get('Cur_Abbreviation')
        rate = data.get('Cur_OfficialRate')
        data.update({'date': date, 'abbreviation': abbreviation, 'rate': rate})
        return data

    def get_values(self):
        return tuple(self.__dict__.values())
