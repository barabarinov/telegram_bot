from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User


def register_user_handler(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id
    with Session() as session:
        existing_user = session.query(User).get(telegram_id)
        if existing_user is None:
            user = User(
                telegram_id=telegram_id,
                username=update.effective_user.username,
                first_name=update.effective_user.first_name,
                last_name=update.effective_user.last_name,
            )
            session.add(user)
            session.commit()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are registered!",
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"You are already registered, "
                     f"{update.effective_user.username if update.effective_user.username is not None else 'Incognito'}!"
                     f" Stop it, I'm tired...",
            )
