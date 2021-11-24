import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext import Updater
from enum import auto, IntEnum

from models import User

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)


class NewPurchase(IntEnum):
    TITLE = auto()
    SPENT_MONEY = auto()
    CREATION_DATE = auto()


CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['I have spent', 'I made'],
    ['Statistics', 'Settings'],
    ['Done'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

updater = Updater(token=os.getenv('TOKEN'), use_context=True)
dispatcher = updater.dispatcher

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
Session = sessionmaker(engine)


def start(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id
    with Session() as session:
        existing_user = session.query(User).get(telegram_id)
        if existing_user is None:
            user = User(
                telegram_id=telegram_id,
                username=update.effective_user.username,
                first_name=update.effective_user.first_name,
                last_name=update.effective_user.last_name,
            )
            session.add(user)
            session.commit()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are registered!",
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"You are already registered, "
                     f"{update.effective_user.username if update.effective_user.username is not None else 'Incognito'}!"
                     f" Stop it, I'm tired...",
            )


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(I have spent|I made|Statistics)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^Something else...$'), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
