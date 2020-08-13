import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

addr_from = "onliner-price-notifier@yandex.by"
addr_to = "onliner-price-notifier@yandex.by"
password = "V2Xh2EscxL"


def notify(message):
    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = 'The price of products has changed on the onliner'
    msg.attach(MIMEText(message, 'html', 'utf-8'))
    _send(msg)


def _send(msg):
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
