import logging
from enum import auto, IntEnum

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler

from app.db import Session
from app.models import GroupIncome
from app.handlers.find_user_lang_or_id import find_user_lang
from app.translate import (
    gettext as _,
    YES_CAPS,
    NO_CAPS,
    YES_NO,
    NAME_INCOME_CATEGORY,
    IS_CORRECT,
    CATEGORY_CREATED,
    SEEYA,
)

logger = logging.getLogger(__name__)


class NewIncomeGroup(IntEnum):
    NAME = auto()
    CONFIRM = auto()


def new_income_group(update: Update, context: CallbackContext):
    reply_keyboard = [['/cancel']]
    update.message.reply_text(_(NAME_INCOME_CATEGORY, find_user_lang(update)), reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewIncomeGroup.NAME


def get_new_income_group_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    logger.info(f'NAME IS HERE {context.user_data["name"]}')
    logger.info(f'CONTEXT = {context}')

    reply_keyboard = [[_(YES_CAPS, find_user_lang(update)), _(NO_CAPS, find_user_lang(update))]]
    update.effective_message.reply_text(
        _(IS_CORRECT, find_user_lang(update), context.user_data["name"]), reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=_(YES_NO, find_user_lang(update))
        ))

    return NewIncomeGroup.CONFIRM


def create_income_group(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_income_group = GroupIncome(
            user_id=update.effective_user.id,
            name=context.user_data['name'],
        )
        session.add(user_new_income_group)
        session.commit()
        session.refresh(user_new_income_group)
    update.message.reply_text(_(CATEGORY_CREATED, find_user_lang(update), user_new_income_group.name))

    return ConversationHandler.END


def cancel_income_creation_group(update: Update, context: CallbackContext):
    update.message.reply_text(_(SEEYA, find_user_lang(update)))

    return ConversationHandler.END


new_income_group_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('new_income_group', new_income_group)],
    states={
        NewIncomeGroup.NAME: [MessageHandler(Filters.text & ~Filters.command, get_new_income_group_name)],
        NewIncomeGroup.CONFIRM: [
            MessageHandler(Filters.regex('^(YES)$') & ~Filters.command, create_income_group),
            MessageHandler(Filters.regex('^(NO)$') & ~Filters.command, cancel_income_creation_group),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_income_creation_group),
    ],
)
