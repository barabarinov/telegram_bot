import logging
from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User, GroupPurchase, GroupIncome
from app.handlers.find_user_lang_or_id import find_user_lang
from app.buttons import reply_keyboard_main_menu
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
    GROCERIES,
    TRANSPORT,
    BILLS,
    MISCELLANEOUS,
]

DEFAULT_USER_INCOME_CATEGORIES = [
    SALARY,
]

logger = logging.getLogger(__name__)


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
                lang=update.effective_user.language_code,
            )
            logger.info(f'USERLANG REGISTER USER IS *****{user.lang}*****')
            session.add(user)

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=_(REGISTERED, user.lang, user.username)
                if update.effective_user.username is not None else _(REGISTERED, user.lang, _(INCOGNITO, user.lang)),
                reply_markup=reply_keyboard_main_menu(update, context, user.lang),
            )

            for name in DEFAULT_USER_EXPENSES_CATEGORIES:
                user_new_expense_category = GroupPurchase(
                    user_id=update.effective_user.id,
                    name=_(name, user.lang),
                )
                session.add(user_new_expense_category)

            for name in DEFAULT_USER_INCOME_CATEGORIES:
                user_new_income_group = GroupIncome(
                    user_id=update.effective_user.id,
                    name=_(name, user.lang),
                )
                session.add(user_new_income_group)
            session.commit()

        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(_(ALREADY_REGISTERED, find_user_lang(update),
                    update.effective_user.username if update.effective_user.username is not None else _(INCOGNITO, find_user_lang(update))) +
                    _(STOP_IT, find_user_lang(update))),
                reply_markup=reply_keyboard_main_menu(update, context, find_user_lang(update)),
            )
