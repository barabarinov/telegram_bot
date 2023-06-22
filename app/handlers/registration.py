from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.message import (
    Message,
    escape,
)
from app.models import User, GroupPurchase, GroupIncome
from app.translate import (
    REGISTERED,
    INCOGNITO,
    ALREADY_REGISTERED,
    STOP_IT,
    GROCERIES,
    TRANSPORT,
    BILLS,
    MISCELLANEOUS,
    SALARY,
    CREATE_NEW_EXPENSE,
    CREATE_NEW_INCOME,
    CREATE_EXPENSE_CATEGORY,
    CREATE_INCOME_CATEGORY,
    ALL_EXPENSES,
    ALL_INCOMES,
    LAST_MONTH,
    LANGUAGE_NAME,
)

DEFAULT_EXPENSES_CATEGORIES = [
    GROCERIES,
    TRANSPORT,
    BILLS,
    MISCELLANEOUS,
]

DEFAULT_INCOME_CATEGORIES = [
    SALARY,
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
                lang=update.effective_user.language_code,
            )
            session.add(user)
            message = Message(update=update, context=context, language=user.lang)
            message.add(REGISTERED, user.username or INCOGNITO, formatters=[escape])
            message.add_reply_buttons(
                [CREATE_NEW_EXPENSE, CREATE_NEW_INCOME],
                [CREATE_EXPENSE_CATEGORY, CREATE_INCOME_CATEGORY],
                [ALL_EXPENSES, ALL_INCOMES],
                [LAST_MONTH],
                [LANGUAGE_NAME],
                resize_keyboard=True,
            )
            message.send_message(user)

            for name in DEFAULT_EXPENSES_CATEGORIES:
                new_expense_category = GroupPurchase(
                    user_id=update.effective_user.id,
                    name=message.translate(name),
                )
                session.add(new_expense_category)

            for name in DEFAULT_INCOME_CATEGORIES:
                new_income_category = GroupIncome(
                    user_id=update.effective_user.id,
                    name=message.translate(name),
                )
                session.add(new_income_category)
            session.commit()
        else:
            message = Message(update=update, context=context, language=existing_user.lang)
            message.add(ALREADY_REGISTERED, existing_user.username or INCOGNITO, formatters=[escape])
            message.add(STOP_IT, formatters=[escape])
            message.add_reply_buttons(
                [CREATE_NEW_EXPENSE, CREATE_NEW_INCOME],
                [CREATE_EXPENSE_CATEGORY, CREATE_INCOME_CATEGORY],
                [ALL_EXPENSES, ALL_INCOMES],
                [LAST_MONTH],
                [LANGUAGE_NAME],
                resize_keyboard=True,
            )
            message.send_message(existing_user)
