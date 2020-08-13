from manager.db_dao import get_items, get_positions_by_item
from notifier import notify

_min_difference_to_notification = 0


def analyze_prices():
    changed = []
    for item in get_items():
        position = get_positions_by_item(item.id)[0]
        difference = item.price - position.price
        msg = f"Item name:<a href='{item.html_url}'>{item.extended_name}</a>, \tprice adding:{item.price}, " \
              f"\tcurrent price: {position.price},  \tdifference: {difference}"
        print(msg)
        if difference >= _min_difference_to_notification:
            changed.append(msg)
    if changed:
        notify('<br>'.join(changed))
