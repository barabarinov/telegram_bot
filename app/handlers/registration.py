from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User, GroupPurchase, GroupIncome
import gettext


def _(msg):
    return msg


lang_ru = gettext.translation("ru_RU", localedir="/usr/share/locale", languages=["ru_RU"])

DEFAULT_USER_PURCHASE_CATEGORIES = [
    '🏠 🛒 Groceries and home appliances',
    '🚙 Transport',
    '💵 Bills',
    '🛍 Miscellaneous']

DEFAULT_USER_INCOME_CATEGORIES = [
    '🤑 Salary']


def user_language(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext):
        lang = update.message.from_user.language_code
        print("LANGUAGE IS", lang)

        global _

        if lang == b"ru_RU":
            _ = lang_ru.gettext
        else:
            def _(msg):
                return msg

        return func(update, context)

    return wrapped


@user_language
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
                text=_("✅ You are registered, {}!").format(user.username)
                if update.effective_user.username is not None else _('Incognito'),
            )

            for name in DEFAULT_USER_PURCHASE_CATEGORIES:
                user_new_purchase_group = GroupPurchase(
                    user_id=update.effective_user.id,
                    name=name,
                )
                session.add(user_new_purchase_group)
                session.commit()
                session.refresh(user_new_purchase_group)

            for name in DEFAULT_USER_INCOME_CATEGORIES:
                user_new_income_group = GroupIncome(
                    user_id=update.effective_user.id,
                    name=name,
                )
                session.add(user_new_income_group)
                session.commit()
                session.refresh(user_new_income_group)

        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    _("❗️ You are already registered") +
                    f" {update.effective_user.username if update.effective_user.username is not None else 'Incognito'}!" +
                    _(" Stop it, I'm tired...😩"),
                )
            )
