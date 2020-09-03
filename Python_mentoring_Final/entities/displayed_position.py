from datetime import datetime

from marshmallow_dataclass import dataclass


@dataclass
class DisplayedPosition:
    id: str
    shop_id: int
    price: float
    warranty: int
    date_update: datetime
    title: str
    html_url: str
    reviews_rating: float
    reviews_count: int
