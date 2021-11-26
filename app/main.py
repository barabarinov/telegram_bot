import datetime
import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext import Updater, ConversationHandler
from enum import auto, IntEnum

from models import User, Purchase

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


class NewPurchase(IntEnum):
    TITLE = auto()
    SPENT_MONEY = auto()
    CREATION_DATE = auto()
    CONFIRM = auto()


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

    update.message.reply_text('How much did you spend?:', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewPurchase.SPENT_MONEY


def get_purchase_spent_money(update: Update, context: CallbackContext):
    if update.message.text.replace('.','').isdigit():
        context.user_data['spent_money'] = float(update.message.text)
    else:
        return ConversationHandler.END

    reply_keyboard = [['/skip', '/cancel']]

    purchase = Purchase(
        title=context.user_data['title'],
        spent_money=context.user_data['spent_money'],
        creation_date=datetime.datetime.strftime(datetime.datetime.now(),"%H:%M %d/%m/%Y"),
    )
    reply_keyboard = [['SAVE', 'DON\'T SAVE']]
    update.message.reply_text(
        f'That\'s your purchase!\n{purchase.display()}', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Save/Don\'t save?'
    ))

    return NewPurchase.CONFIRM


def create_purchase(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_purchase = Purchase(
            user_id=update.effective_user.id,
            title=context.user_data['title'],
            spent_money=context.user_data['spent_money'],
        )
        session.add(user_new_purchase)
        session.commit()
    update.message.reply_text('Your purchase has been added!')

    return ConversationHandler.END


def cancel_creation_purchase(update: Update, context: CallbackContext):
    update.message.reply_text('See ya!')

    return ConversationHandler.END


new_purchase_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('new_purchase', new_purchase)],
    states={
        NewPurchase.TITLE: [MessageHandler(Filters.text & ~Filters.command, get_purchase_title)],
        NewPurchase.SPENT_MONEY: [MessageHandler(Filters.text & ~Filters.command, get_purchase_spent_money)],
        NewPurchase.CONFIRM: [
            MessageHandler(Filters.regex('^(SAVE)$') & ~Filters.command, create_purchase),
            MessageHandler(Filters.regex('^(DON\'T SAVE)$') & ~Filters.command, cancel_creation_purchase),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_creation_purchase),
    ],
)
dispatcher.add_handler(new_purchase_conversation_handler)

dispatcher.add_handler(CommandHandler('start', start))

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
