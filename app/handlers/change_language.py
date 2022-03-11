import logging
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler
from telegram.ext import Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from app.db import Session
from app.models import User
from app.handlers.find_user_lang_or_id import find_user_lang
from app.translate import (
    gettext as _,
    CHANGE_LANG,
    YOUR_LANG_CHANGED,
)

logger = logging.getLogger(__name__)


def change_language_button(update: Update, context: CallbackContext):
    reply_keyboard = [['EN', 'RU']]
    update.effective_message.reply_text(_(CHANGE_LANG, find_user_lang(update)), reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ), parse_mode=ParseMode.MARKDOWN)

    return 1


def change_to_eng_or_ru(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        user.lang = update.message.text.lower()
        logger.info(f'USERLANG1 *****{update.message.text.lower()}*****{user.lang}')
        session.commit()
        update.message.reply_text(_(YOUR_LANG_CHANGED, user.lang, update.message.text.upper()), reply_markup=ReplyKeyboardRemove())
        # update.callback_query.edit_message_reply_markup(None)
        return ConversationHandler.END


change_language_handler = ConversationHandler(
    entry_points=[CommandHandler('language', change_language_button)],
    states={
        1: [
            MessageHandler(Filters.regex('^(EN|RU)$') & ~Filters.command, change_to_eng_or_ru),
        ],
    },
    fallbacks=[],
)
