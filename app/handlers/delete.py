from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.handlers.get_user import get_effective_user
from app.message import (
    Message,
    escape,
)
from app.translate import DELETE, INCOGNITO


def delete_me(update: Update, context: CallbackContext) -> None:
    with Session() as session:
        user = get_effective_user(update, session)
        session.delete(user)
        session.commit()

    message = Message(update=update, language=user.lang)  # TODO test lang here
    message.add(DELETE, user.username or INCOGNITO, formatters=[escape])
    message.reply()
