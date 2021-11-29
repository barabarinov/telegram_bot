import datetime
import logging
from enum import auto, IntEnum

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler

from db import Session
from models import Income

logger = logging.getLogger(__name__)


class NewIncome(IntEnum):
    TITLE = auto()
    EARNED_MONEY = auto()
    CREATION_DATE = auto()
    CONFIRM = auto()


def new_income(update: Update, context: CallbackContext):
    reply_keyboard = [['/cancel']]
    update.message.reply_text('Enter your income title:', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewIncome.TITLE


def get_income_title(update: Update, context: CallbackContext):
    context.user_data['title'] = update.message.text

    reply_keyboard = [['/cancel']]

    update.message.reply_text('How much did you earn?:', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewIncome.EARNED_MONEY


def get_income_earned_money(update: Update, context: CallbackContext):
    try:
        context.user_data['earned_money'] = float(update.message.text.replace(' ', ''))
    except ValueError:
        return ConversationHandler.END

    income = Income(
        title=context.user_data['title'],
        earned_money=context.user_data['earned_money'],
        creation_date=datetime.datetime.now(),
    )
    reply_keyboard = [['SAVE', 'DON\'T SAVE']]
    update.effective_message.reply_text(
        f'That\'s your income!\n{income.display_income()}', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Save/Don\'t save?'
        ))

    return NewIncome.CONFIRM


def create_income(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_income = Income(
            user_id=update.effective_user.id,
            title=context.user_data['title'],
            earned_money=context.user_data['earned_money'],
        )
        session.add(user_new_income)
        session.commit()
    update.message.reply_text('Your income has been added!')

    return ConversationHandler.END


def cancel_creation_income(update: Update, context: CallbackContext):
    update.message.reply_text('See ya!')

    return ConversationHandler.END


new_income_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('new_income', new_income)],
    states={
        NewIncome.TITLE: [MessageHandler(Filters.text & ~Filters.command, get_income_title)],
        NewIncome.EARNED_MONEY: [MessageHandler(Filters.text & ~Filters.command, get_income_earned_money)],
        NewIncome.CONFIRM: [
            MessageHandler(Filters.regex('^(SAVE)$') & ~Filters.command, create_income),
            MessageHandler(Filters.regex('^(DON\'T SAVE)$') & ~Filters.command, cancel_creation_income),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_creation_income),
    ],
)
