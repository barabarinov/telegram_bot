import logging
from enum import auto, IntEnum

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler

from db import Session
from models import GroupIncome

logger = logging.getLogger(__name__)


class NewIncomeGroup(IntEnum):
    NAME = auto()
    CONFIRM = auto()


def new_income_group(update: Update, context: CallbackContext):
    reply_keyboard = [['/cancel']]
    update.message.reply_text('Enter name of the new income group!', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewIncomeGroup.NAME


def get_new_income_group_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    logger.info(f'NAME IS HERE {context.user_data["name"]}')
    logger.info(f'CONTEXT = {context}')

    reply_keyboard = [['YES', 'NO']]
    update.effective_message.reply_text(
        f'The name \'{context.user_data["name"]}\' for new group is correct?', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Yes/No?'
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
    update.message.reply_text(f'The group \'{user_new_income_group.name}\' was created!')

    return ConversationHandler.END


def cancel_income_creation_group(update: Update, context: CallbackContext):
    update.message.reply_text('See ya!')

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
