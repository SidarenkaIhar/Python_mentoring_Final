from datetime import datetime
from typing import ClassVar, Type

from marshmallow import Schema, EXCLUDE, pre_load
from marshmallow_dataclass import dataclass


@dataclass
class Currency:
    id: str
    date: datetime
    abbreviation: str
    rate: float
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def process(self, data, many, **kwargs):
        currency_date = datetime.strptime(data.get('Date'), '%Y-%m-%dT%H:%M:%S')
        date = currency_date.strftime('%Y-%m-%d %H:%M:%S')
        abbreviation = data.get('Cur_Abbreviation')
        rate = data.get('Cur_OfficialRate') / data.get('Cur_Scale')
        currency_id = f"{abbreviation}:{currency_date.strftime('%Y%m%d')}"
        data.update({'id': currency_id, 'date': date, 'abbreviation': abbreviation, 'rate': rate})
        return data

    def get_values(self):
        return tuple(self.__dict__.values())
