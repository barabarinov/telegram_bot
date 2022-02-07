from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User, GroupPurchase, GroupIncome
from app.translate import (
    gettext as _,
    REGISTERED,
    INCOGNITO,
    ALREADY_REGISTERED,
    STOP_IT,
    GROCERIES,
    TRANSPORT,
    BILLS,
    MISCELLANEOUS,
    SALARY,
)


DEFAULT_USER_EXPENSES_CATEGORIES = [
    _(GROCERIES),
    _(TRANSPORT),
    _(BILLS),
    _(MISCELLANEOUS)
]

DEFAULT_USER_INCOME_CATEGORIES = [
    _(SALARY)
]


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
                text=_(REGISTERED, user, user.username) if update.effective_user.username is not None else _(INCOGNITO, user),
            )

            for name in DEFAULT_USER_EXPENSES_CATEGORIES:
                user_new_purchase_group = GroupPurchase(
                    user_id=update.effective_user.id,
                    name=name,
                )
                session.add(user_new_purchase_group)

            for name in DEFAULT_USER_INCOME_CATEGORIES:
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
                    _(ALREADY_REGISTERED) +
                    f" {update.effective_user.username if update.effective_user.username is not None else _(INCOGNITO)}!" +
                    _(STOP_IT)
                )
            )
