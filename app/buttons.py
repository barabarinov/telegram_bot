from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
import logging

from app.handlers.find_user_lang_or_id import find_user_lang
from app.translate import (
    gettext as _,
    CREATE_NEW_EXPENSE,
    CREATE_EXPENSE_CATEGORY,
    ALL_EXPENSES,
    CREATE_NEW_INCOME,
    CREATE_INCOME_CATEGORY,
    ALL_INCOMES,
    LAST_MONTH,
    LANGUAGE_NAME,
    CANCEL_THIS,
)


def reply_keyboard_main_menu(update: Update, context: CallbackContext, user_lang):
    logging.info(f'WHAT IN USER_LANG IS >>> {user_lang}')
    reply_keyboard_menu = [
        [_(CREATE_NEW_EXPENSE, user_lang), _(CREATE_NEW_INCOME, user_lang)],
        [_(CREATE_EXPENSE_CATEGORY, user_lang), _(CREATE_INCOME_CATEGORY, user_lang)],
        [_(ALL_EXPENSES, user_lang), _(ALL_INCOMES, user_lang)],
        [_(LAST_MONTH, user_lang)],
        [_(LANGUAGE_NAME, user_lang)],
    ]

    return ReplyKeyboardMarkup(reply_keyboard_menu, one_time_keyboard=False)


def reply_keyboard_cancel(update: Update, context: CallbackContext, CANCEL):
    reply_keyboard = [[InlineKeyboardButton(_(CANCEL_THIS, find_user_lang(update)), callback_data=CANCEL)]]
    return InlineKeyboardMarkup(reply_keyboard)
