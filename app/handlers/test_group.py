from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from app.db import Session
from app.handlers.get_user import get_effective_user
from app.message import (
    Message,
    escape,
)
from app.models import GroupIncome
from app.translate import CATEGORY_CREATED


def new_group_single(update: Update, context: CallbackContext):
    with Session() as session:
        user = get_effective_user(update, session)
        user_new_group = GroupIncome(
            user_id=update.effective_user.id,
            name=update.message.text.split(" ", maxsplit=1)[1],
        )
        session.add(user_new_group)
        session.commit()
        session.refresh(user_new_group)

        message = Message(update=update, language=user.lang)
        message.add(CATEGORY_CREATED, user_new_group.name, formatters=[escape])
        message.reply()


new_group_single = CommandHandler("new_group_income_test", new_group_single)
