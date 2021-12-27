from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User, GroupPurchase, GroupIncome


DEFAULT_USER_PURCHASES_CATEGORIES = [
    '🏠 🛒 Groceries and home appliances',
    '🚙 Transport',
    '💵 Bills',
    '🛍 Miscellaneous']

DEFAULT_USER_INCOMES_CATEGORIES = [
    '🤑 Salary']


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
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="✅ You are registered, {}!".format(user.username)
                if update.effective_user.username is not None else 'Incognito',
            )

            for name in DEFAULT_USER_PURCHASES_CATEGORIES:
                user_new_purchase_group = GroupPurchase(
                    user_id=update.effective_user.id,
                    name=name,
                )
                session.add(user_new_purchase_group)

            for name in DEFAULT_USER_INCOMES_CATEGORIES:
                user_new_income_group = GroupIncome(
                    user_id=update.effective_user.id,
                    name=name,
                )
                session.add(user_new_income_group)
            session.commit()

        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    "❗️ You are already registered" +
                    f" {update.effective_user.username if update.effective_user.username is not None else 'Incognito'}!"+
                    " Stop it, I'm tired...😩"
                )
            )
