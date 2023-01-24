from enum import auto, IntEnum

from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import ConversationHandler

from app.db import Session
from app.handlers.get_user import get_effective_user
from app.message import (
    Message,
    escape,
)
from app.models import GroupPurchase
from app.translate import (
    NAME_EXPENSE_CATEGORY,
    IS_CORRECT,
    YES,
    NO,
    CATEGORY_CREATED,
    SEEYA,
    CANCEL,
)


class NewExpenseCategory(IntEnum):
    NAME = auto()
    CONFIRM = auto()


def new_expense_category(update: Update, context: CallbackContext) -> NewExpenseCategory:
    with Session() as session:
        user = get_effective_user(update, session)
        context.user_data["user_lang"] = user.lang

        message = Message(update=update, language=user.lang)
        button = message.add(NAME_EXPENSE_CATEGORY, formatters=[escape]).create_inline_button(text=CANCEL)
        message.add_inline_buttons([button])
        message.reply()

    return NewExpenseCategory.NAME


def get_new_expense_category_name(update: Update, context: CallbackContext) -> NewExpenseCategory:
    context.user_data["name"] = update.message.text

    message = Message(update=update, language=context.user_data["user_lang"])
    message.add(IS_CORRECT, context.user_data["name"], formatters=[escape])
    yes = message.create_inline_button(text=YES)
    no = message.create_inline_button(text=NO, callback_id=CANCEL)
    message.add_inline_buttons([yes, no])
    message.reply()

    return NewExpenseCategory.CONFIRM


def create_expense_category(update: Update, context: CallbackContext):
    with Session() as session:
        new_expense_category = GroupPurchase(
            user_id=update.effective_user.id,
            name=context.user_data["name"],
        )
        session.add(new_expense_category)
        session.commit()

        message = Message(update=update, context=context, language=context.user_data["user_lang"])
        message.add(CATEGORY_CREATED, new_expense_category.name, formatters=[escape])
        message.edit_message_text()

    return ConversationHandler.END


def cancel_expense_creation_category(update: Update, context: CallbackContext):
    message = Message(update=update, context=context, language=context.user_data["user_lang"])
    message.add(SEEYA, formatters=[escape])
    message.edit_message_text()

    return ConversationHandler.END


new_expense_category_conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex(
                "^Create new expense category|Створити категорію витрат|Создать категорию расходов$"
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
            CallbackQueryHandler(create_expense_category, pattern=YES),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(cancel_expense_creation_category, pattern=CANCEL),
    ],
)
