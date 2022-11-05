import logging
from enum import auto, IntEnum

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import ConversationHandler

from app.db import Session
from app.buttons import reply_keyboard_cancel
from app.handlers.find_user_lang_or_id import find_user_lang
from app.models import GroupPurchase
from app.handlers.expenses import CANCEL
from app.translate import (
    gettext as _,
    YES,
    NO,
    NAME_EXPENSE_CATEGORY,
    IS_CORRECT,
    CATEGORY_CREATED,
    SEEYA,
)

logger = logging.getLogger(__name__)

CALLBACK_YES = "yes"


class NewExpenseCategory(IntEnum):
    NAME = auto()
    CONFIRM = auto()


def new_expense_category(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=_(NAME_EXPENSE_CATEGORY, find_user_lang(update)),
        reply_markup=reply_keyboard_cancel(update, context, CANCEL),
    )

    return NewExpenseCategory.NAME


def get_new_expense_category_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text

    reply_keyboard = [
        [
            InlineKeyboardButton(
                _(YES, find_user_lang(update)), callback_data=CALLBACK_YES
            ),
            InlineKeyboardButton(_(NO, find_user_lang(update)), callback_data=CANCEL),
        ]
    ]
    reply_keyboard_yes_or_no = InlineKeyboardMarkup(reply_keyboard)

    update.effective_message.reply_text(
        text=_(IS_CORRECT, find_user_lang(update), context.user_data["name"]),
        reply_markup=reply_keyboard_yes_or_no,
        parse_mode=ParseMode.MARKDOWN,
    )

    return NewExpenseCategory.CONFIRM


def create_expense_category(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_expense_category = GroupPurchase(
            user_id=update.effective_user.id,
            name=context.user_data["name"],
        )
        session.add(user_new_expense_category)
        session.commit()
        session.refresh(user_new_expense_category)

    query = update.callback_query
    query.answer()

    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=_(
            CATEGORY_CREATED, find_user_lang(update), user_new_expense_category.name
        ),
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationHandler.END


def cancel_expense_creation_category(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=_(SEEYA, find_user_lang(update)),
    )
    return ConversationHandler.END


new_expense_category_conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex(
                "(Create new expense category|Створити категорію витрат|Создать категорию расходов)"
            )
            & ~Filters.command,
            new_expense_category,
        )
    ],
    states={
        NewExpenseCategory.NAME: [
            MessageHandler(
                Filters.text & ~Filters.command, get_new_expense_category_name
            )
        ],
        NewExpenseCategory.CONFIRM: [
            CallbackQueryHandler(create_expense_category, pattern=CALLBACK_YES),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(cancel_expense_creation_category, pattern=CANCEL),
    ],
)
