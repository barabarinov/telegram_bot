from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User


def delete_my_telegram_id_from_telegram_bot(update: Update, context: CallbackContext):
    with Session() as session:
        user = User(
            telegram_id=update.effective_user.id,
        )
        session.delete(user)
        session.commit()
