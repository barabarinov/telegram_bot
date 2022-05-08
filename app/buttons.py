from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from app.handlers.find_user_lang_or_id import find_user_lang
from app.translate import (
    gettext as _,
    CREATE_NEW_EXPENSE,
    CREATE_EXPENSE_CATEGORY,
    ALL_EXPENSES,
    LANGUAGE_NAME,
    CREATE_NEW_INCOME,
    CREATE_INCOME_CATEGORY,
    ALL_INCOMES,
    CANCEL_THIS,
)


def reply_keyboard_main_menu(update: Update, context: CallbackContext):
    reply_keyboard_menu = [
        [_(CREATE_NEW_EXPENSE, find_user_lang(update)), _(CREATE_NEW_INCOME, find_user_lang(update))],
        [_(CREATE_EXPENSE_CATEGORY, find_user_lang(update)), _(CREATE_INCOME_CATEGORY, find_user_lang(update))],
        [_(ALL_EXPENSES, find_user_lang(update)), _(ALL_INCOMES, find_user_lang(update))],
        [_(LANGUAGE_NAME, find_user_lang(update))],
    ]

    return ReplyKeyboardMarkup(reply_keyboard_menu, one_time_keyboard=False)


def reply_keyboard_cancel(update: Update, context: CallbackContext, CANCEL):
    reply_keyboard = [[InlineKeyboardButton(_(CANCEL_THIS, find_user_lang(update)), callback_data=CANCEL)]]
    return InlineKeyboardMarkup(reply_keyboard)
