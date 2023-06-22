from enum import auto, IntEnum

from telegram import Update
from telegram.ext import CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram.ext import ConversationHandler

from app.db import Session
from app.handlers.get_user import get_effective_user
from app.message import (
    Message,
    escape,
)
from app.models import GroupIncome
from app.translate import (
    NAME_INCOME_CATEGORY,
    IS_CORRECT,
    YES,
    NO,
    CATEGORY_CREATED,
    SEEYA,
    CANCEL,
)


class NewIncomeCategory(IntEnum):
    NAME = auto()
    CONFIRM = auto()


def new_income_category(update: Update, context: CallbackContext) -> NewIncomeCategory:
    with Session() as session:
        user = get_effective_user(update, session)
        context.user_data["user_lang"] = user.lang

        message = Message(update=update, language=user.lang)
        button = message.add(NAME_INCOME_CATEGORY, formatters=[escape]).create_inline_button(text=CANCEL)
        message.add_inline_buttons([button])
        message.reply()

    return NewIncomeCategory.NAME


def get_new_income_category_name(update: Update, context: CallbackContext) -> NewIncomeCategory:
    context.user_data["name"] = update.message.text

    message = Message(update=update, language=context.user_data["user_lang"])
    message.add(IS_CORRECT, context.user_data["name"], formatters=[escape])
    yes = message.create_inline_button(text=YES)
    no = message.create_inline_button(text=NO, callback_id=CANCEL)
    message.add_inline_buttons([yes, no])
    message.reply()

    return NewIncomeCategory.CONFIRM


def create_income_category(update: Update, context: CallbackContext):
    with Session() as session:
        new_income_category = GroupIncome(
            user_id=update.effective_user.id,
            name=context.user_data["name"],
        )
        session.add(new_income_category)
        session.commit()

        message = Message(update=update, context=context, language=context.user_data["user_lang"])
        message.add(CATEGORY_CREATED, new_income_category.name, formatters=[escape])
        message.edit_message_text()

    return ConversationHandler.END


def cancel_income_creation_category(update: Update, context: CallbackContext):
    message = Message(update=update, context=context, language=context.user_data["user_lang"])
    message.add(SEEYA, formatters=[escape])
    message.edit_message_text()

    return ConversationHandler.END


new_income_category_conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex(
                "^Create new income category|Створити категорію доходу|Создать категорию дохода$"
            )
            & ~Filters.command,
            new_income_category,
        )
    ],
    states={
        NewIncomeCategory.NAME: [
            MessageHandler(
                Filters.text & ~Filters.command, get_new_income_category_name
            )
        ],
        NewIncomeCategory.CONFIRM: [
            CallbackQueryHandler(create_income_category, pattern=YES)
        ],
    },
    fallbacks=[
        CallbackQueryHandler(cancel_income_creation_category, pattern=CANCEL),
    ],
)
