import datetime
import logging
import os

import pytz
from telegram.ext import CommandHandler, CallbackContext
from telegram.ext import Updater, MessageHandler, Filters

from app.create_db import create_tables
from app.db import Session
from app.handlers.change_language import change_language_handler
from app.handlers.delete import delete_me
from app.handlers.expenses import new_expense_conversation_handler
from app.handlers.incomes import new_income_conversation_handler
from app.handlers.new_expense_category import new_expense_category_conversation_handler
from app.handlers.new_income_category import new_income_category_conversation_handler
from app.handlers.registration import register_user_handler
from app.handlers.reports.last_month_report import previous_month_feedback
from app.handlers.reports.monthly_report import job_monthly_feedback
from app.handlers.reports.report_expenses_categories import (
    current_expenses_report,
    EUROPEKIEV,
)
from app.handlers.reports.report_income_categories import (
    current_income_report,
)
from app.message import (
    Message,
    escape
)
from app.models import User
from app.translate import (
    DAILY_MESSAGE,
    ONCE_MESSAGE,
)

logger = logging.getLogger(__name__)

BANK_NUMBER = os.getenv("BANKNUMBER")


def once_message(context: CallbackContext) -> None:
    with Session() as session:
        for user in session.query(User):
            message = Message(context=context, language=user.lang)
            message.add(ONCE_MESSAGE, formatters=[escape])
            message.send_message(user)

            second_message = Message(context=context, language=user.lang)
            second_message.add(BANK_NUMBER)
            second_message.send_message(user)


def daily_message(context: CallbackContext) -> None:
    with Session() as session:
        for user in session.query(User):
            message = Message(context=context, language=user.lang)
            message.add(DAILY_MESSAGE, formatters=[escape])
            message.send_message(user)


IS_HEROKU = os.getenv("IS_HEROKU", "true").lower() == "true"


def run(token, port):
    create_tables()
    updater = Updater(token=token, use_context=True)
    j = updater.job_queue

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", register_user_handler))
    dispatcher.add_handler(new_expense_conversation_handler)
    dispatcher.add_handler(new_income_conversation_handler)
    dispatcher.add_handler(new_expense_category_conversation_handler)
    dispatcher.add_handler(new_income_category_conversation_handler)
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                "^📉 Income statistics|📉 Статистика доходів|📉 Статистика доходов$"
            )
            & ~Filters.command,
            current_income_report,
        )
    )
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                "^📈 Expenses statistics|📈 Статистика витрат|📈 Статистика расходов$"
            )
            & ~Filters.command,
            current_expenses_report,
        )
    )
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                "^📊 Statistic for the last month|📊 Статистика за минулий місяць|📊 Статистика за прошлый месяц$"
            )
            & ~Filters.command,
            previous_month_feedback,
        )
    )
    dispatcher.add_handler(
        CommandHandler("delete_me", delete_me)
    )
    dispatcher.add_handler(change_language_handler)

    j.run_once(
        once_message,
        when=pytz.timezone(EUROPEKIEV).localize(
            datetime.datetime(day=18, month=1, year=2023, hour=13, minute=0)
        ),
    )
    j.run_daily(
        daily_message,
        days=tuple(range(7)),
        time=datetime.time(hour=15, minute=00, tzinfo=pytz.timezone(EUROPEKIEV)),
    )
    j.run_monthly(
        job_monthly_feedback,
        datetime.time(hour=14, minute=42, tzinfo=pytz.timezone(EUROPEKIEV)),
        30,
    )
    if IS_HEROKU:
        updater.start_webhook(
            listen="0.0.0.0.",
            port=port,
            url_path=token,
            webhook_url=f"https://wallet-tracker-telegram.herokuapp.com/{token}",
        )
    else:
        updater.start_polling()
    updater.idle()
