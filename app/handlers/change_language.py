from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler
from telegram.ext import Filters, CallbackQueryHandler

from app.db import Session
from app.handlers.get_user import get_effective_user
from app.message import (
    Message,
    escape,
)
from app.translate import (
    CHANGE_LANG,
    LANG_CHANGED,
    CREATE_NEW_EXPENSE,
    CREATE_NEW_INCOME,
    CREATE_EXPENSE_CATEGORY,
    CREATE_INCOME_CATEGORY,
    ALL_EXPENSES,
    ALL_INCOMES,
    LAST_MONTH,
    LANGUAGE_NAME,
)

ENGLISH = "en"
UKRAINIAN = "uk"
RUSSIAN = "ru"
LANGUAGE = "en|uk|ru"
FLAGS = {"uk": "🇺🇦", "en": "🇬🇧", "ru": "🏳️"}


def change_language_button(update: Update, context: CallbackContext):
    message = Message(update=update)
    message.add(CHANGE_LANG, formatters=[escape])
    ukrainian = message.create_inline_button(text="🇺🇦 UA", callback_id=UKRAINIAN)
    english = message.create_inline_button(text="🇬🇧 EN", callback_id=ENGLISH)
    russian = message.create_inline_button(text="🏳️ RU", callback_id=RUSSIAN)
    message.add_inline_buttons([ukrainian, english, russian])
    message.reply()

    return 1


def change_lang(update: Update, context: CallbackContext):
    with Session() as session:
        user = get_effective_user(update, session)
        user.lang = update.callback_query.data
        session.commit()

        message = Message(update=update, context=context, language=user.lang)
        message.add(LANG_CHANGED, FLAGS[user.lang], formatters=[escape])
        message.add_reply_buttons(
            [CREATE_NEW_EXPENSE, CREATE_NEW_INCOME],
            [CREATE_EXPENSE_CATEGORY, CREATE_INCOME_CATEGORY],
            [ALL_EXPENSES, ALL_INCOMES],
            [LAST_MONTH],
            [LANGUAGE_NAME],
            resize_keyboard=True,
        )
        message.send_message(user)

    return ConversationHandler.END


change_language_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex("^🇬🇧 Language|🏳️ Язык|🇺🇦 Мова$") & ~Filters.command, change_language_button,
        )
    ],
    states={
        1: [CallbackQueryHandler(change_lang, pattern=LANGUAGE)],
    },
    fallbacks=[],
)
