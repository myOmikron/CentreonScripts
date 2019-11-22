#!/usr/bin/env python3.7

from telegram_bot_sdk.telegram import TelegramBot
import argparse


class CentreonNotificationBot:
    def __init__(self, credentials):
        self.telebot = TelegramBot(credentials)
        with open("allowed_ids") as fh:
            self.allowed_ids = fh.readlines()

    def send_message(self, message):
        for chat_id in self.allowed_ids:
            self.telebot.send_message(chat_id=chat_id, text=message, disable_notification=False, parse_mode="Markdown")


def main(arguments):
    with open("credentials") as fh:
        bot = CentreonNotificationBot(fh.readline()[:-1])
    message = "*ALERT*\n\nType: {} \nState: {}\nHost: {}\nAddress: {}\nInfo: {}\nDate/Time: {}"
    message = message.format(arguments.type, arguments.state, arguments.name, arguments.address, arguments.output,
                             arguments.date)
    bot.send_message(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", action="store", dest="type", help="Type of the notification")
    parser.add_argument("-n", "--name",  action="store", dest="name", help="Name of the host")
    parser.add_argument("-s", "--state",  action="store", dest="state", help="State of the host")
    parser.add_argument("-a", "--address",  action="store", dest="address", help="Address of the host")
    parser.add_argument("-o", "--output",  action="store", dest="output", help="Output of the host")
    parser.add_argument("-d", "--date",  action="store", dest="date", help="Date")
    args = parser.parse_args()
    main(args)
