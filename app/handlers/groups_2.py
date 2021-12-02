import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from db import Session
from models import Group

logger = logging.getLogger(__name__)


def new_group_single(update: Update, context: CallbackContext):
    logger.info(f'TEXT IS HERE {update.message.text}')
    with Session() as session:
        user_new_group = Group(
            user_id=update.effective_user.id,
            name=update.message.text.split(' ', maxsplit=1)[1],
        )
        session.add(user_new_group)
        session.commit()
        session.refresh(user_new_group)
    update.message.reply_text(f'The group \'{user_new_group.name}\' was created!')


new_group_single = CommandHandler('new_group_single', new_group_single)
