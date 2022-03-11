import datetime
import logging
from enum import auto, IntEnum

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import ConversationHandler
from app.handlers.find_user_lang_or_id import find_user_lang

from app.db import Session
from app.models import User, Purchase, GroupPurchase
from app.translate import (
    gettext as _,
    EXPENSE_TITLE,
    HOW_MUCH_SPEND,
    SELECT_CATEGORY,
    SAVE,
    DONT_SAVE,
    THATS_YOUR_EXPENSE,
    EXPENSE_ADDED,
    SEEYA,
)

logger = logging.getLogger(__name__)


class NewExpense(IntEnum):
    TITLE = auto()
    SPENT_MONEY = auto()
    CHOOSE_CATEGORY = auto()
    CONFIRM = auto()


def new_expense(update: Update, context: CallbackContext):
    reply_keyboard = [['/cancel']]
    update.message.reply_text(_(EXPENSE_TITLE, find_user_lang(update)), reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewExpense.TITLE


def get_expense_title(update: Update, context: CallbackContext):
    context.user_data['title'] = update.message.text

    reply_keyboard = [['/cancel']]

    update.message.reply_text(_(HOW_MUCH_SPEND, find_user_lang(update)), reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewExpense.SPENT_MONEY


def get_expense_spent_money(update: Update, context: CallbackContext):
    try:
        context.user_data['spent_money'] = float(update.message.text.replace(' ', ''))
    except ValueError:
        return ConversationHandler.END

    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        update.message.reply_text(
            _(SELECT_CATEGORY, user.lang),
            reply_markup=InlineKeyboardMarkup.from_column([
                InlineKeyboardButton(
                    text=group.name, callback_data=f'set-expense-category${group.id}') for group in
                user.groups_purchases
            ]),
        )

    return NewExpense.CHOOSE_CATEGORY


def get_expense_category_callback(update: Update, context: CallbackContext):
    update.callback_query.answer()

    _another, group_id = update.callback_query.data.split('$')
    group_id = int(group_id)
    context.user_data['group_id'] = group_id
    with Session() as session:
        category = session.query(GroupPurchase).get(group_id)

    purchase = Purchase(
        title=context.user_data['title'],
        spent_money=context.user_data['spent_money'],
        creation_date=datetime.datetime.now(),
        group=category,  # тут вместо category было group
    )
    reply_keyboard = [[_(SAVE, find_user_lang(update)), _(DONT_SAVE, find_user_lang(update))]]
    update.effective_message.reply_text(
        _(THATS_YOUR_EXPENSE, find_user_lang(update), purchase.display_expense(find_user_lang(update))),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder=_(SAVE, find_user_lang(update)) + '/' + _(DONT_SAVE, find_user_lang(update))
        ), parse_mode=ParseMode.MARKDOWN)

    return NewExpense.CONFIRM


def create_expense(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_purchase = Purchase(
            user_id=update.effective_user.id,
            title=context.user_data['title'],
            spent_money=context.user_data['spent_money'],
            group_id=context.user_data['group_id'],
        )
        session.add(user_new_purchase)
        session.commit()
    update.message.reply_text(_(EXPENSE_ADDED, find_user_lang(update)))

    return ConversationHandler.END


def cancel_creation_expense(update: Update, context: CallbackContext):
    update.message.reply_text(_(SEEYA, find_user_lang(update)))

    return ConversationHandler.END


new_expense_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('new_expense', new_expense)],
    states={
        NewExpense.TITLE: [MessageHandler(Filters.text & ~Filters.command, get_expense_title)],
        NewExpense.SPENT_MONEY: [MessageHandler(Filters.text & ~Filters.command, get_expense_spent_money)],
        NewExpense.CHOOSE_CATEGORY: [
            CallbackQueryHandler(get_expense_category_callback, pattern='^set-expense-category', )],
        NewExpense.CONFIRM: [
            MessageHandler(Filters.regex('^(SAVE|СОХРАНИТЬ)$') & ~Filters.command, create_expense),
            MessageHandler(Filters.regex('^(DON\'T SAVE|ОТМЕНА)$') & ~Filters.command, cancel_creation_expense),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_creation_expense),
    ],
)
