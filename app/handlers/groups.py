import logging
from enum import auto, IntEnum

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler

from db import Session
from models import User, Group

logger = logging.getLogger(__name__)


class NewGroup(IntEnum):
    NAME = auto()
    CONFIRM = auto()


def new_group(update: Update, context: CallbackContext):
    reply_keyboard = [['/cancel']]
    update.message.reply_text('Enter name of the new group!', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewGroup.NAME


def get_new_group_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    logger.info(f'CONTEXT IS HERE {context.user_data["name"]}')
    logger.info(f'CONTEXT = {context}')

    reply_keyboard = [['YES', 'NO']]
    update.effective_message.reply_text(
        f'The name \'{context.user_data["name"]}\' for new group is correct?', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Yes/No?'
        ))

    return NewGroup.CONFIRM


def create_group(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_group = Group(
            user_id=update.effective_user.id,
            name=context.user_data['name'],
        )
        logger.info(f'***USER*** {user_new_group.user_id}')
        session.add(user_new_group)
        session.commit()
        logger.info(f'***USER*** {user_new_group.user_id}')
    update.message.reply_text(f'The group \'{user_new_group.name}\' was created!')

    return ConversationHandler.END


def cancel_creation_group(update: Update, context: CallbackContext):
    update.message.reply_text('See ya!')

    return ConversationHandler.END


new_group_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('new_group', new_group)],
    states={
        NewGroup.NAME: [MessageHandler(Filters.text & ~Filters.command, get_new_group_name)],
        NewGroup.CONFIRM: [
            MessageHandler(Filters.regex('^(YES)$') & ~Filters.command, create_group),
            MessageHandler(Filters.regex('^(NO)$') & ~Filters.command, cancel_creation_group),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_creation_group),
    ],
)
