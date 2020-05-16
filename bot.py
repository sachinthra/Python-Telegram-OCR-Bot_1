#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.


import allKeys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
try:
    from PIL import Image
except ImportError:
    import Image

import csv
import logging
import pytesseract
from traceback import print_exc
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
pytesseract.pytesseract.tesseract_cmd = r'E:\Programfiles\Tesseract-OCR\tesseract'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello {}'.format(
        update.message.from_user.first_name))

    try:
        filename = "Resources/Data/records.csv"
        with open(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(
                [update.message.chat.id, update.message.chat.first_name])
    except:
        print_exc()


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    query = update.message.text
    update.message.reply_text("igot a query " + query)


def imageConverter(update, context):
    # print(update.message)
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    newFile.download('Resources/test.png')
    update.message.reply_text(
        "I got your image!!! wait untill it is processed ")

    try:
        textInImage = pytesseract.image_to_string(
            Image.open('Resources/test.png'))
        update.message.reply_text(textInImage)
    except:
        # Tesseract processing is terminated
        update.message.reply_text("Time out!! can't able to get text")
        # print_exc()


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    print("\nStarting Server.......")
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    try:
        TOKEN = allKeys.getKey()
        updater = Updater(TOKEN, use_context=True)
        print("\nStarting Server, Status : 'Success'")
    except:
        print("!!!Error in Running Server!!!")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.photo, imageConverter))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
