import datetime
import pytz
import logging
import os

import telegram.error
from telegram.ext import CommandHandler, CallbackContext
from telegram.ext import Updater, MessageHandler, Filters

from app.handlers.incomes import new_income_conversation_handler
from app.handlers.new_income_category import new_income_category_conversation_handler
from app.handlers.new_expense_category import new_expense_category_conversation_handler
from app.handlers.expenses import new_expense_conversation_handler
from app.handlers.registration import register_user_handler
from app.handlers.reports.report_of_all_incomes_categories import get_sum_of_all_incomes_categories
from app.handlers.reports.report_of_all_expenses_categories import get_sum_of_all_expenses_categories, EUROPEKIEV
from app.handlers.reports.monthly_report import monthly_feedback
from app.handlers.reports.last_month_report import last_month_report
from app.handlers.delete import delete_my_telegram_id_from_telegram_bot
from app.db import Session
from app.models import User
from app.create_db import create_tables
from app.handlers.change_language import change_language_handler
from app.translate import (
    gettext as _,
    DAILY_MESSAGE,
    ONCE_MESSAGE,
)

logger = logging.getLogger(__name__)

BANK_NUMBER = os.getenv('BANKNUMBER')


def once_message(context: CallbackContext):
    with Session() as session:
        for user in session.query(User):
            message = _(ONCE_MESSAGE, user.lang)
            try:
                context.bot.send_message(chat_id=user.telegram_id, text=message)
            except telegram.error.Unauthorized:
                logger.info(f'User {user.username} {user.telegram_id} blocked')
            else:
                logger.info(f'User {user.username} {user.telegram_id} sent message')

            try:
                context.bot.send_message(chat_id=user.telegram_id, text=BANK_NUMBER)
            except telegram.error.Unauthorized:
                logger.info(f'User {user.username} {user.telegram_id} blocked')
            else:
                logger.info(f'User {user.username} {user.telegram_id} sent message')


def daily_message(context: CallbackContext):
    with Session() as session:
        for user in session.query(User):
            message = _(DAILY_MESSAGE, user.lang)
            try:
                context.bot.send_message(chat_id=user.telegram_id, text=message)
            except telegram.error.Unauthorized:
                logger.info(f'User {user.username} {user.telegram_id} blocked')
            else:
                logger.info(f'User {user.username} {user.telegram_id} sent message')


IS_HEROKU = os.getenv('IS_HEROKU', 'true').lower() == 'true'


def run(token, port):
    create_tables()
    updater = Updater(token=token, use_context=True)
    j = updater.job_queue

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', register_user_handler))
    dispatcher.add_handler(new_expense_conversation_handler)
    dispatcher.add_handler(new_income_conversation_handler)
    dispatcher.add_handler(new_expense_category_conversation_handler)
    dispatcher.add_handler(new_income_category_conversation_handler)
    dispatcher.add_handler(MessageHandler(
        Filters.regex(
            '^📉 Income statistics|📉 Статистика доходів|📉 Статистика доходов$'
            ) & ~Filters.command, get_sum_of_all_incomes_categories)
    )
    dispatcher.add_handler(MessageHandler(
        Filters.regex(
            '^📈 Expenses statistics|📈 Статистика витрат|📈 Статистика расходов$'
            ) & ~Filters.command, get_sum_of_all_expenses_categories)
    )
    dispatcher.add_handler(MessageHandler(
        Filters.regex(
            '^📊 Statistic for the last month|📊 Статистика за минулий місяць|📊 Статистика за прошлый месяц$'
            ) & ~Filters.command, last_month_report)
    )
    dispatcher.add_handler(CommandHandler('delete_me', delete_my_telegram_id_from_telegram_bot))
    dispatcher.add_handler(change_language_handler)

    j.run_once(once_message, when=pytz.timezone(EUROPEKIEV).localize(datetime.datetime(
        day=13, month=7, year=2022, hour=14, minute=59)),
    )

    j.run_daily(daily_message, days=tuple(range(7)), time=datetime.time(
        hour=15, minute=00, second=00,
        tzinfo=pytz.timezone(EUROPEKIEV))
    )

    j.run_monthly(monthly_feedback, datetime.time(10, 00, 00, tzinfo=pytz.timezone(EUROPEKIEV)), 1)

    if IS_HEROKU:
        updater.start_webhook(
            listen="0.0.0.0.",
            port=port,
            url_path=token,
            webhook_url=f'https://wallet-tracker-telegram.herokuapp.com/{token}'
        )
    else:
        updater.start_polling()
    updater.idle()
