import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler
from telegram.ext import Updater

from handlers.purchases import new_purchase_conversation_handler
from handlers.incomes import new_income_conversation_handler
from handlers.groups import new_group_conversation_handler
from handlers.registration import register_user_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)


def main(token):
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', register_user_handler))
    dispatcher.add_handler(new_purchase_conversation_handler)
    dispatcher.add_handler(new_income_conversation_handler)
    dispatcher.add_handler(new_group_conversation_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    load_dotenv()
    main(os.getenv('TOKEN'))
