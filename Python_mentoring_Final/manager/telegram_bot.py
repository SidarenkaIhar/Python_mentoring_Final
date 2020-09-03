import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

import project_settings
from entities.user import User
from manager import db_dao
from manager.db_dao import get_displayed_positions_by_item, get_items, get_currencies, get_user_by_id, insert_user, \
    get_currencies_by_abbreviation, insert_parsing_items

logging.basicConfig(filename=project_settings.LOG_FILE, format=project_settings.LOG_FORMAT,
                    level=project_settings.LOG_LEVEL)
_logger = logging.getLogger(__name__)

OPTION, ADD_ITEMS, SET_SETTINGS, GET_SETTINGS = range(4)
allowed_currencies_abbreviation = set(currency.abbreviation for currency in get_currencies()).union(('BYN',))

markup = ReplyKeyboardMarkup([['Add new items', 'Show items'], ['Settings', 'Done']], one_time_keyboard=True)
settings_markup = ReplyKeyboardMarkup([['Set email', 'Set display currency'],
                                       ['Set notification threshold', 'Back']], one_time_keyboard=True)


def start(update, context):
    update.message.reply_text('Select the desired action from the menu:', reply_markup=markup)
    return OPTION


def add_items(update, context):
    update.message.reply_text('Please enter the url of the products separated by commas for tracking:')
    return ADD_ITEMS


def show_items(update, context):
    user = get_user(update.message.from_user.id, update.message.chat_id)
    reply = []
    for item in get_items():
        price = convert_price_by_currency(item.price, user.currency_abbreviation)
        out_of_stock = '' if price else '<b>Out of stock and under order!</b>\n'
        reply.append(f"#{len(reply) + 1}: <a href='{item.html_url}'>{item.extended_name}</a>, price: <b>{price}</b> "
                     f"{user.currency_abbreviation}\n {out_of_stock}"
                     f"actions: 📄/shops_{item.key}  🗑/delete_{item.key}")
    reply = '\n\n'.join(reply) if reply else "Not the tracking of items"
    update.message.reply_text(reply, reply_markup=markup, parse_mode='HTML')
    return OPTION


def set_settings(update, context):
    update.message.reply_text('Select the necessary parser settings to edit:', reply_markup=settings_markup)
    return SET_SETTINGS


def show_shops(update, context):
    user = get_user(update.message.from_user.id, update.message.chat_id)
    reply = []
    item = update.message.text.replace('/shops_', '')
    for position in get_displayed_positions_by_item(item):
        price = convert_price_by_currency(position.price, user.currency_abbreviation)
        reply.append(f"#{len(reply) + 1}: <a href='{position.html_url}'>{position.title}</a>, price: <b>{price}</b> "
                     f"{user.currency_abbreviation}\nwarranty: <b>{position.warranty}</b>,\n"
                     f"reviews: rating - <b>{position.reviews_rating}</b>, count - <b>{position.reviews_count}</b>")
    not_found = 'Sellers for this product have not been found or have not yet been processed.\n' \
                'Sellers for new products are added within 2 minutes, try again later.'
    reply = '\n\n'.join(reply) if reply else not_found
    update.message.reply_text(reply, reply_markup=markup, parse_mode='HTML')
    return OPTION


def delete_item(update, context):
    item = update.message.text.replace('/delete_', '')
    result = 'successfully' if db_dao.delete_item(item) > 0 else '<b>not</b> successfully'
    update.message.reply_text(f'Item was {result} removed from the tracked ones', parse_mode='HTML')
    return OPTION


def get_items_to_add(update, context):
    items = update.message.text.replace(' ', '')
    amount = insert_parsing_items(items.split(','))
    update.message.reply_text(f"<b>{amount}</b> items were added for tracking", reply_markup=markup, parse_mode='HTML')
    return OPTION


def set_email(update, context):
    user = get_user(update.message.from_user.id, update.message.chat_id)
    current_email = user.email if user.email else 'not set yet'
    update.message.reply_text(f'Please enter your email address for notifications\n(current email [{current_email}]):',
                              reply_markup=ReplyKeyboardMarkup([['Clear', 'Back']], one_time_keyboard=True))
    return GET_SETTINGS


def set_currency(update, context):
    user = get_user(update.message.from_user.id, update.message.chat_id)
    update.message.reply_text(f'Please enter the price display currency (current [{user.currency_abbreviation}])',
                              reply_markup=ReplyKeyboardMarkup([allowed_currencies_abbreviation, ['Back']],
                                                               one_time_keyboard=True))
    return GET_SETTINGS


def set_threshold(update, context):
    user = get_user(update.message.from_user.id, update.message.chat_id)
    update.message.reply_text(f'Please enter the value by which the price should decrease for the notification '
                              f'(current [{user.price_threshold}]):',
                              reply_markup=ReplyKeyboardMarkup([['Back']], one_time_keyboard=True))
    return GET_SETTINGS


def get_email(update, context):
    user = get_user(update.message.from_user.id, update.message.chat_id)
    user.email = '' if update.message.text == 'Clear' else update.message.text
    reply = 'action' if update.message.text == 'Clear' else 'email'
    return insert_user_and_get_response(update, user, reply)


def get_currency(update, context):
    user = get_user(update.message.from_user.id, update.message.chat_id)
    user.currency_abbreviation = update.message.text
    return insert_user_and_get_response(update, user, 'currency abbreviation')


def get_threshold(update, context):
    user = get_user(update.message.from_user.id, update.message.chat_id)
    user.price_threshold = update.message.text
    return insert_user_and_get_response(update, user, 'price threshold')


def insert_user_and_get_response(update, user, reply_text):
    result = 'was' if insert_user(user) > 0 else 'was <b>not</b>'
    update.message.reply_text(f'The {reply_text} {result} saved.', reply_markup=settings_markup, parse_mode='HTML')
    return SET_SETTINGS


def get_user(user_id, chat_id):
    users = get_user_by_id(user_id)
    return users[0] if users else User(user_id, chat_id, '', 1, 'BYN')


def convert_price_by_currency(price, currency_abbreviation):
    currencies = get_currencies_by_abbreviation(currency_abbreviation)
    if currencies:
        return round(price / currencies[0].rate, 2)
    return price


def done(update, context):
    update.message.reply_text("See you next time!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(update, context):
    _logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(project_settings.TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            OPTION: [MessageHandler(Filters.regex('^Add new items$'), add_items),
                     MessageHandler(Filters.regex('^Show items$'), show_items),
                     MessageHandler(Filters.regex('^\/shops_.*'), show_shops),
                     MessageHandler(Filters.regex('^\/delete_.*'), delete_item),
                     MessageHandler(Filters.regex('^Settings$'), set_settings), ],

            ADD_ITEMS: [MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')), get_items_to_add)],

            SET_SETTINGS: [MessageHandler(Filters.regex('^Set email$'), set_email),
                           MessageHandler(Filters.regex('^Set display currency$'), set_currency),
                           MessageHandler(Filters.regex('^Set notification threshold$'), set_threshold),
                           MessageHandler(Filters.regex('^Back$'), start), ],

            GET_SETTINGS: [MessageHandler(Filters.regex('^Back$'), set_settings),
                           MessageHandler((Filters.regex('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
                                           | Filters.regex('^Clear$'))
                                          & ~(Filters.command | Filters.regex('^Done$')), get_email),
                           MessageHandler(Filters.text(allowed_currencies_abbreviation)
                                          & ~(Filters.command | Filters.regex('^Done$')), get_currency),
                           MessageHandler(Filters.regex('^[\d]+$')
                                          & ~(Filters.command | Filters.regex('^Done$')), get_threshold), ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conversation_handler)
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
