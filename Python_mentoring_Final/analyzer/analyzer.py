import time

import schedule

from manager.db_dao import get_items, get_last_positions_by_item, get_users, get_currencies_by_abbreviation
from notifier import notifier


def get_changed_items(min_difference, rate, currency_abbreviation):
    changed = []
    for item in get_items():
        if not item.price:
            changed.append(f"""#{len(changed) + 1}: <a href='{item.html_url}'>{item.extended_name}</a>: 
                                    <b>Out of stock and under order!</b>""")
            continue
        positions = get_last_positions_by_item(item.id)
        if positions:
            position = _get_smallest_fresh_position(positions)
            item_price = round(item.price / rate, 2)
            position_price = round(position.price / rate, 2)
            difference = round((item.price - position.price) / rate, 2)
            if difference >= min_difference:
                changed.append(f"""#{len(changed) + 1}: <a href='{item.html_url}'>{item.extended_name}</a>: 
                                price adding: <b>{item_price}</b> {currency_abbreviation}, 
                                current price: <b>{position_price}</b> {currency_abbreviation}, 
                                difference: <b>{difference}</b> {currency_abbreviation}""")
    return changed


def _get_smallest_fresh_position(positions):
    position = positions[0]
    for pos in positions:
        if pos.date_update.date() > position.date_update.date():
            position = pos
    return position


def analyze():
    for user in get_users():
        currencies = get_currencies_by_abbreviation(user.currency_abbreviation)
        rate = currencies[0].rate if currencies else 1
        changed_items = get_changed_items(user.price_threshold, rate, user.currency_abbreviation)
        if changed_items:
            notifier.notify(user, changed_items)


if __name__ == "__main__":
    analyze()
    schedule.every(8).hours.do(analyze)
    while True:
        schedule.run_pending()
        time.sleep(1)
