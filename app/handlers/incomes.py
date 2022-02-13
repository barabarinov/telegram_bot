import datetime
import logging
from enum import auto, IntEnum

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import ConversationHandler
from app.handlers.find_user_lang_or_id import find_user_lang, find_effective_user_id

from app.db import Session
from app.models import User, Income, GroupIncome
from app.translate import (
    gettext as _,
    INCOME_TITLE,
    HOW_MUCH_EARN,
    SELECT_GROUP,
    THATS_YOUR_INCOME,
    INCOME_ADDED,
    SEEYA,
)

logger = logging.getLogger(__name__)


class NewIncome(IntEnum):
    TITLE = auto()
    EARNED_MONEY = auto()
    CHOOSE_GROUP = auto()
    CONFIRM = auto()


def new_income(update: Update, context: CallbackContext):
    reply_keyboard = [['/cancel']]
    update.message.reply_text(_(INCOME_TITLE, find_user_lang(update)), reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewIncome.TITLE


def get_income_title(update: Update, context: CallbackContext):
    context.user_data['title'] = update.message.text

    reply_keyboard = [['/cancel']]

    update.message.reply_text(_(HOW_MUCH_EARN, find_user_lang(update)), reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewIncome.EARNED_MONEY


def get_income_earned_money(update: Update, context: CallbackContext):
    try:
        context.user_data['earned_money'] = float(update.message.text.replace(' ', ''))
    except ValueError:
        return ConversationHandler.END

    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        update.message.reply_text(
            _(SELECT_GROUP, user.lang),
            reply_markup=InlineKeyboardMarkup.from_column([
                InlineKeyboardButton(
                    text=group.name, callback_data=f'set-income-group${group.id}') for group in user.groups_incomes
            ]),
        )

        return NewIncome.CHOOSE_GROUP


def get_income_group_callback(update: Update, context: CallbackContext):
    update.callback_query.answer()

    _other, group_id = update.callback_query.data.split('$')
    group_id = int(group_id)
    context.user_data['group_id'] = group_id
    with Session() as session:
        group = session.query(GroupIncome).get(group_id)

    income = Income(
        title=context.user_data['title'],
        earned_money=context.user_data['earned_money'],
        creation_date=datetime.datetime.now(),
        group=group,
    )
    reply_keyboard = [['SAVE', 'DON\'T SAVE']]
    update.effective_message.reply_text(
        _(THATS_YOUR_INCOME, find_user_lang(update), income.display_income(find_user_lang(update))),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Save/Don\'t save?'
        ))

    return NewIncome.CONFIRM


def create_income(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_income = Income(
            user_id=update.effective_user.id,
            title=context.user_data['title'],
            earned_money=context.user_data['earned_money'],
            group_id=context.user_data['group_id'],
        )
        session.add(user_new_income)
        session.commit()
    update.message.reply_text(_(INCOME_ADDED, find_user_lang(update)))

    return ConversationHandler.END


def cancel_creation_income(update: Update, context: CallbackContext):
    update.message.reply_text(_(SEEYA, find_user_lang(update)))

    return ConversationHandler.END


new_income_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('new_income', new_income)],
    states={
        NewIncome.TITLE: [MessageHandler(Filters.text & ~Filters.command, get_income_title)],
        NewIncome.EARNED_MONEY: [MessageHandler(Filters.text & ~Filters.command, get_income_earned_money)],
        NewIncome.CHOOSE_GROUP: [CallbackQueryHandler(get_income_group_callback, pattern='^set-income-group', )],
        NewIncome.CONFIRM: [
            MessageHandler(Filters.regex('^(SAVE)$') & ~Filters.command, create_income),
            MessageHandler(Filters.regex('^(DON\'T SAVE)$') & ~Filters.command, cancel_creation_income),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_creation_income),
    ],
)
