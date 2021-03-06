import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from app.db import Session
from app.models import GroupIncome


logger = logging.getLogger(__name__)


def new_group_single(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_group = GroupIncome(
            user_id=update.effective_user.id,
            name=update.message.text.split(' ', maxsplit=1)[1],
        )
        session.add(user_new_group)
        session.commit()
        session.refresh(user_new_group)
    update.message.reply_text(f'The group \'{user_new_group.name}\' was created!')


new_group_single = CommandHandler('new_group_single', new_group_single)
