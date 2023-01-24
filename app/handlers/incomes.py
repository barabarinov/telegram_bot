import datetime
import logging
from enum import auto, IntEnum

import pytz
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import ConversationHandler

from app.db import Session
from app.handlers.get_user import get_effective_user
from app.message import (
    Message,
    escape,
    bold,
    italic,
)
from app.handlers.reports.report_expenses_categories import EUROPEKIEV
from app.models import Income, GroupIncome
from app.translate import (
    INCOME_TITLE,
    HOW_MUCH_EARN,
    SELECT_CATEGORY,
    SAVE,
    DONT_SAVE,
    THATS_YOUR_INCOME,
    INCOME_ADDED,
    SEEYA,
    CANCEL,
    WRONG_VALUE,
    DISPLAY_INCOME,
)

logger = logging.getLogger(__name__)


class NewIncome(IntEnum):
    TITLE = auto()
    EARNED_MONEY = auto()
    CHOOSE_CATEGORY = auto()
    CONFIRM = auto()


def new_income(update: Update, context: CallbackContext) -> NewIncome:
    with Session() as session:
        user = get_effective_user(update, session)
        context.user_data["user_lang"] = user.lang

        message = Message(update=update, language=user.lang)
        button = message.add(INCOME_TITLE).create_inline_button(text=CANCEL)
        message.add_inline_buttons([button])
        message.reply()

    return NewIncome.TITLE


def get_income_title(update: Update, context: CallbackContext) -> NewIncome:
    context.user_data["title"] = update.message.text

    message = Message(update=update, language=context.user_data["user_lang"])
    button = message.add(HOW_MUCH_EARN).create_inline_button(text=CANCEL)
    message.add_inline_buttons([button])
    message.reply()

    return NewIncome.EARNED_MONEY


def get_income_earned_money(update: Update, context: CallbackContext) -> NewIncome:
    try:
        context.user_data["earned_money"] = float(update.message.text.replace(" ", ""))
    except ValueError:
        message = Message(update=update, language=context.user_data["user_lang"])
        message.add(WRONG_VALUE, formatters=[escape])
        message.reply()

        return NewIncome.EARNED_MONEY

    with Session() as session:
        user = get_effective_user(update, session)
        message = Message(update=update, language=user.lang)
        message.add(SELECT_CATEGORY, formatters=[escape])

        for group in user.groups_incomes:
            message.add_inline_buttons(
                [
                    message.create_inline_button(text=group.name, callback_id=f"set-income-category${group.id}")
                ]
            )
        cancel_button = message.create_inline_button(text=CANCEL)
        message.add_inline_buttons([cancel_button])
        message.reply()

        return NewIncome.CHOOSE_CATEGORY


def get_income_category_callback(update: Update, context: CallbackContext) -> NewIncome:
    _other, group_id = update.callback_query.data.split("$")
    group_id = int(group_id)
    context.user_data["group_id"] = group_id

    with Session() as session:
        category = session.query(GroupIncome).get(group_id)

    income = Income(
        title=context.user_data["title"],
        earned_money=context.user_data["earned_money"],
        creation_date=datetime.datetime.now(tz=pytz.timezone(EUROPEKIEV)),
        group=category,
    )
    message = Message(update=update, language=context.user_data["user_lang"])
    message.add(THATS_YOUR_INCOME, formatters=[escape, bold]).add_newline()
    message.add(DISPLAY_INCOME, *[escape(item) for item in income.display_income()], formatters=[italic])
    save = message.create_inline_button(text=SAVE)
    cancel = message.create_inline_button(text=DONT_SAVE, callback_id=CANCEL)
    message.add_inline_buttons([save, cancel])
    message.reply()

    return NewIncome.CONFIRM


def create_income(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_income = Income(
            user_id=update.effective_user.id,
            title=context.user_data["title"],
            earned_money=context.user_data["earned_money"],
            group_id=context.user_data["group_id"],
            creation_date=datetime.datetime.utcnow(),
        )
        session.add(user_new_income)
        session.commit()

        message = Message(update=update, context=context, language=context.user_data["user_lang"])
        message.add(INCOME_ADDED, formatters=[escape])
        message.edit_message_text()

    return ConversationHandler.END


def cancel_creation_income(update: Update, context: CallbackContext):
    message = Message(update=update, context=context, language=context.user_data["user_lang"])
    message.add(SEEYA, formatters=[escape])
    message.edit_message_text()

    return ConversationHandler.END


new_income_conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex("^🟩 Create new income|🟩 Додати дохід|🟩 Внести доход$")
            & ~Filters.command,
            new_income,
        )
    ],
    states={
        NewIncome.TITLE: [
            MessageHandler(Filters.text & ~Filters.command, get_income_title)
        ],
        NewIncome.EARNED_MONEY: [
            MessageHandler(Filters.text & ~Filters.command, get_income_earned_money)
        ],
        NewIncome.CHOOSE_CATEGORY: [
            CallbackQueryHandler(
                get_income_category_callback, pattern="^set-income-category"
            ),
            CallbackQueryHandler(cancel_creation_income, pattern=CANCEL),
        ],
        NewIncome.CONFIRM: [
            CallbackQueryHandler(create_income, pattern=SAVE),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(cancel_creation_income, pattern=CANCEL),
    ],
)
