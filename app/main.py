import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram import Update, ReplyKeyboardMarkup
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


def new_purchase(update: Update, context: CallbackContext):
    reply_keyboard = [['/cancel']]
    update.message.reply_text('Enter your purchase title:', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewPurchase.TITLE

def get_purchase_title(update: Update, context: CallbackContext):
    context.user_data['title'] = update.message.text

    reply_keyboard = [['/skip', '/cancel']]

    update.message.reply_text('Enter ')


if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
