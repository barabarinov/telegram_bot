from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User


def delete_my_telegram_id_from_telegram_bot(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id
    with Session() as session:
        telegram_id = session.query(User).get(telegram_id)
        user = User(
            telegram_id=telegram_id,
        )
        session.delete(user)
        session.commit()
