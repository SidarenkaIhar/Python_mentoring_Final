import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from telegram import Bot

import project_settings


def notify(user, items):
    if user:
        notify_by_email(user.email, '<br><br>'.join(items))
        notify_by_telegram(user.chat_id, '\n\n'.join(items))


def notify_by_email(addr_to, message):
    if addr_to and message:
        msg = MIMEMultipart()
        msg['From'] = project_settings.NOTIFIER_EMAIL
        msg['To'] = addr_to
        msg['Subject'] = 'The price of products has changed on the onliner'
        msg.attach(MIMEText(message, 'html', 'utf-8'))
        _send_mail(msg)


def _send_mail(msg):
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(project_settings.NOTIFIER_EMAIL, project_settings.NOTIFIER_EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()


def notify_by_telegram(chat_id, message):
    if chat_id and message:
        bot = Bot(project_settings.TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id, message, parse_mode='HTML')
