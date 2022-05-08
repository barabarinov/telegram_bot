import logging
from enum import auto, IntEnum

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram.ext import ConversationHandler

from app.db import Session
from app.models import GroupIncome
from app.buttons import reply_keyboard_cancel
from app.handlers.find_user_lang_or_id import find_user_lang
from app.handlers.new_expense_category import CALLBACK_YES
from app.handlers.expenses import CANCEL
from app.translate import (
    gettext as _,
    YES,
    NO,
    NAME_INCOME_CATEGORY,
    IS_CORRECT,
    CATEGORY_CREATED,
    SEEYA,
)

logger = logging.getLogger(__name__)


class NewIncomeGroup(IntEnum):
    NAME = auto()
    CONFIRM = auto()


def new_income_category(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=_(NAME_INCOME_CATEGORY, find_user_lang(update)),
        reply_markup=reply_keyboard_cancel(update, context, CANCEL),
    )

    return NewIncomeGroup.NAME


def get_new_income_category_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    logger.info(f'NAME IS HERE {context.user_data["name"]}')
    logger.info(f'CONTEXT = {context}')

    reply_keyboard = [
        [InlineKeyboardButton(_(YES, find_user_lang(update)), callback_data=CALLBACK_YES),
         InlineKeyboardButton(_(NO, find_user_lang(update)), callback_data=CANCEL)]
    ]
    reply_keyboard_yes_or_no = InlineKeyboardMarkup(reply_keyboard)

    update.effective_message.reply_text(
        _(IS_CORRECT, find_user_lang(update), context.user_data["name"]),
        reply_markup=reply_keyboard_yes_or_no,
        parse_mode=ParseMode.MARKDOWN,
    )

    return NewIncomeGroup.CONFIRM


def create_income_category(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_income_group = GroupIncome(
            user_id=update.effective_user.id,
            name=context.user_data['name'],
        )
        session.add(user_new_income_group)
        session.commit()
        session.refresh(user_new_income_group)

    query = update.callback_query
    query.answer()

    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=_(CATEGORY_CREATED, find_user_lang(update), user_new_income_group.name),
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationHandler.END


def cancel_income_creation_category(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=_(SEEYA, find_user_lang(update)),
    )
    return ConversationHandler.END


new_income_category_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(
        Filters.regex(
            '^Create new income category|Створити категорію доходу|Создать категорию дохода$'
        ) & ~Filters.command, new_income_category)],
    states={
        NewIncomeGroup.NAME: [MessageHandler(Filters.text & ~Filters.command, get_new_income_category_name)],
        NewIncomeGroup.CONFIRM: [
            CallbackQueryHandler(create_income_category, pattern=CALLBACK_YES)
        ],
    },
    fallbacks=[
        CallbackQueryHandler(cancel_income_creation_category, pattern=CANCEL),
    ],
)
