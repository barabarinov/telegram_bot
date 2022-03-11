import logging
from enum import auto, IntEnum

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler

from app.db import Session
from app.handlers.find_user_lang_or_id import find_user_lang
from app.models import GroupPurchase
from app.translate import (
    gettext as _,
    YES_CAPS,
    NO_CAPS,
    YES_NO,
    NAME_EXPENSE_CATEGORY,
    IS_CORRECT,
    CATEGORY_CREATED,
    SEEYA,

)

logger = logging.getLogger(__name__)


class NewExpenseCategory(IntEnum):
    NAME = auto()
    CONFIRM = auto()


def new_expense_category(update: Update, context: CallbackContext):
    reply_keyboard = [['/cancel']]
    update.message.reply_text(_(NAME_EXPENSE_CATEGORY, find_user_lang(update)), reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewExpenseCategory.NAME


def get_new_expense_category_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    logger.info(f'NAME IS HERE {context.user_data["name"]}')
    logger.info(f'CONTEXT = {context}')

    reply_keyboard = [[_(YES_CAPS, find_user_lang(update)), _(NO_CAPS, find_user_lang(update), one_time_keyboard=True)]]
    update.effective_message.reply_text(
        _(IS_CORRECT, find_user_lang(update), context.user_data["name"]), reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=_(YES_NO, find_user_lang(update))
        ))

    return NewExpenseCategory.CONFIRM


def create_expense_category(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_expense_category = GroupPurchase(
            user_id=update.effective_user.id,
            name=context.user_data['name'],
        )
        session.add(user_new_expense_category)
        session.commit()
        session.refresh(user_new_expense_category)
    update.message.reply_text(_(CATEGORY_CREATED, find_user_lang(update), user_new_expense_category.name))

    return ConversationHandler.END


def cancel_expense_creation_category(update: Update, context: CallbackContext):
    update.message.reply_text(_(SEEYA, find_user_lang(update)))

    return ConversationHandler.END


new_expense_category_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('new_expense_category', new_expense_category)],
    states={
        NewExpenseCategory.NAME: [MessageHandler(Filters.text & ~Filters.command, get_new_expense_category_name)],
        NewExpenseCategory.CONFIRM: [
            MessageHandler(Filters.regex('^(YES|ДА)$') & ~Filters.command, create_expense_category),
            MessageHandler(Filters.regex('^(NO|НЕТ)$') & ~Filters.command, cancel_expense_creation_category),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_expense_creation_category),
    ],
)
