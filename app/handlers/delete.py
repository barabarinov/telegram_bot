from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User


def delete_my_telegram_id_from_telegram_bot(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id
    with Session() as session:
        user = User(
            telegram_id=telegram_id,
        )
        session.delete(user)
        session.commit()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Your telegram id was deleted, {user.username}!'
        )
