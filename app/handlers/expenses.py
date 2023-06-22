import datetime
import logging
from enum import auto, IntEnum

import pytz
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import ConversationHandler

from app.db import Session
from app.handlers.get_user import get_effective_user
from app.handlers.reports.report_expenses_categories import EUROPEKIEV
from app.message import (
    Message,
    escape,
    bold,
    italic,
)
from app.models import Purchase, GroupPurchase
from app.translate import (
    EXPENSE_TITLE,
    HOW_MUCH_SPEND,
    SELECT_CATEGORY,
    SAVE,
    DONT_SAVE,
    THATS_YOUR_EXPENSE,
    EXPENSE_ADDED,
    SEEYA,
    CANCEL,
    WRONG_VALUE,
    DISPLAY_EXPENSE,
)

logger = logging.getLogger(__name__)


class NewExpense(IntEnum):
    TITLE = auto()
    SPENT_MONEY = auto()
    CHOOSE_CATEGORY = auto()
    CONFIRM = auto()


def new_expense(update: Update, context: CallbackContext) -> NewExpense:
    with Session() as session:
        user = get_effective_user(update, session)
        context.user_data["user_lang"] = user.lang

        message = Message(update=update, language=user.lang)
        button = message.add(EXPENSE_TITLE).create_inline_button(text=CANCEL)
        message.add_inline_buttons([button])
        message.reply()

    return NewExpense.TITLE


def get_expense_title(update: Update, context: CallbackContext) -> NewExpense:
    context.user_data["title"] = update.message.text

    message = Message(update=update, language=context.user_data["user_lang"])
    button = message.add(HOW_MUCH_SPEND).create_inline_button(text=CANCEL)
    message.add_inline_buttons([button])
    message.reply()

    return NewExpense.SPENT_MONEY


def get_expense_spent_money(update: Update, context: CallbackContext) -> NewExpense:
    try:
        context.user_data["spent_money"] = float(update.message.text.replace(" ", ""))
    except ValueError:
        message = Message(update=update, language=context.user_data["user_lang"])
        message.add(WRONG_VALUE, formatters=[escape])
        message.reply()

        return NewExpense.SPENT_MONEY

    with Session() as session:
        user = get_effective_user(update, session)
        message = Message(update=update, language=user.lang)
        message.add(SELECT_CATEGORY, formatters=[escape])

        for group in user.groups_purchases:
            message.add_inline_buttons(
                [
                    message.create_inline_button(text=group.name, callback_id=f"set-expense-category${group.id}")
                ]
            )
        cancel_button = message.create_inline_button(text=CANCEL)
        message.add_inline_buttons([cancel_button])
        message.reply()

    return NewExpense.CHOOSE_CATEGORY


def get_expense_category_callback(update: Update, context: CallbackContext) -> NewExpense:
    _another, group_id = update.callback_query.data.split("$")
    group_id = int(group_id)
    context.user_data["group_id"] = group_id

    with Session() as session:
        category = session.query(GroupPurchase).get(group_id)

    purchase = Purchase(
        title=context.user_data["title"],
        spent_money=context.user_data["spent_money"],
        creation_date=datetime.datetime.now(tz=pytz.timezone(EUROPEKIEV)),
        group=category,
    )
    message = Message(update=update, language=context.user_data["user_lang"])
    message.add(THATS_YOUR_EXPENSE, formatters=[escape, bold]).add_newline()
    message.add(DISPLAY_EXPENSE, *[escape(item) for item in purchase.display_expense()], formatters=[italic])
    save = message.create_inline_button(text=SAVE)
    cancel = message.create_inline_button(text=DONT_SAVE, callback_id=CANCEL)
    message.add_inline_buttons([save, cancel])
    message.reply()

    return NewExpense.CONFIRM


def create_expense(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_purchase = Purchase(
            user_id=update.effective_user.id,
            title=context.user_data["title"],
            spent_money=context.user_data["spent_money"],
            group_id=context.user_data["group_id"],
            creation_date=datetime.datetime.utcnow(),
        )
        session.add(user_new_purchase)
        session.commit()

        message = Message(update=update, context=context, language=context.user_data["user_lang"])
        message.add(EXPENSE_ADDED, formatters=[escape])
        message.edit_message_text()

    return ConversationHandler.END


def cancel_creation_expense(update: Update, context: CallbackContext):
    message = Message(update=update, context=context, language=context.user_data["user_lang"])
    message.add(SEEYA, formatters=[escape])
    message.edit_message_text()

    return ConversationHandler.END


new_expense_conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex("^🟥 Create new expense|🟥 Додати витрату|🟥 Внести расход$")
            & ~Filters.command,
            new_expense,
        )
    ],
    states={
        NewExpense.TITLE: [
            MessageHandler(Filters.text & ~Filters.command, get_expense_title)
        ],
        NewExpense.SPENT_MONEY: [
            MessageHandler(Filters.text & ~Filters.command, get_expense_spent_money)
        ],
        NewExpense.CHOOSE_CATEGORY: [
            CallbackQueryHandler(
                get_expense_category_callback, pattern="^set-expense-category"
            )
        ],
        NewExpense.CONFIRM: [
            CallbackQueryHandler(create_expense, pattern=SAVE),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(cancel_creation_expense, pattern=CANCEL)
    ],
)
