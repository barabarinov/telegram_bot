import logging

from telegram import Update, ParseMode
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler
from telegram.ext import Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.db import Session
from app.models import User
from app.handlers.find_user_lang_or_id import find_user_lang
from app.buttons import reply_keyboard_main_menu
from app.translate import (
    gettext as _,
    CHANGE_LANG,
    YOUR_LANG_CHANGED,
)

logger = logging.getLogger(__name__)

ENGLISH = 'en'
UKRAINIAN = 'uk'
RUSSIAN = 'ru'
LANGUAGE = 'en|ua|ru'
FLAGS = {'uk': '🇺🇦', 'en': '🇬🇧', 'ru': '🏳️'}


def change_language_button(update: Update, context: CallbackContext):
    reply_keyboard_lang = [
        [InlineKeyboardButton('🇺🇦 UA', callback_data=UKRAINIAN),
         InlineKeyboardButton('🇬🇧 EN', callback_data=ENGLISH),
         InlineKeyboardButton('🏳️ RU', callback_data=RUSSIAN)]
    ]
    reply_keyboard_language = InlineKeyboardMarkup(reply_keyboard_lang)

    update.message.reply_text(
        text=(_(CHANGE_LANG, find_user_lang(update))),
        reply_markup=reply_keyboard_language,
        parse_mode=ParseMode.MARKDOWN,
    )

    return 1


def change_to_eng_uk_or_ru(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        query = update.callback_query
        user.lang = query.data
        logger.info(f'query.data *****{query.data}*****')
        session.commit()

        logger.info(f'callback_query ########{update.callback_query}########')
        query.answer()

        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=_(YOUR_LANG_CHANGED, user.lang, FLAGS[query.data]),
            reply_markup=reply_keyboard_main_menu(update, context)),
    return ConversationHandler.END


change_language_handler = ConversationHandler(
    entry_points=[MessageHandler(
        Filters.regex('^🇬🇧 Language|🏳️ Язык|🇺🇦 Мова$') & ~Filters.command, change_language_button
    )],
    states={
        1: [
            CallbackQueryHandler(change_to_eng_uk_or_ru, pattern='en|ru|uk'),
           ],
    },
    fallbacks=[],
)
