import datetime
import logging
import os

import telegram.error
from telegram.ext import CommandHandler, CallbackContext
from telegram.ext import Updater

from app.handlers.incomes import new_income_conversation_handler
from app.handlers.monthly_report import get_monthly_report_start_end
from app.handlers.new_income_group import new_income_group_conversation_handler
from app.handlers.new_purchase_group import new_purchase_group_conversation_handler
from app.handlers.purchases import new_purchase_conversation_handler
from app.handlers.registration import register_user_handler
from app.handlers.report_of_all_incomes_categories import get_sum_of_all_incomes_categories
from app.handlers.report_of_all_purchase_categories import get_sum_of_all_purchases_categories
from app.handlers.delete import delete_my_telegram_id_from_telegram_bot
from app.db import Session
from app.models import User
from app.create_db import create_tables


logger = logging.getLogger(__name__)


def daily_message(context: CallbackContext):
    message = 'Don’t forget to fill in your expenses and incomes for today!'
    with Session() as session:
        for user in session.query(User):
            try:
                context.bot.send_message(chat_id=user.telegram_id, text=message)
            except telegram.error.Unauthorized:
                logger.info(f'User {user.username} {user.telegram_id} blocked')
            else:
                logger.info(f'User {user.username} {user.telegram_id} sent message')


def monthly_feedback(context: CallbackContext):
    with Session() as session:
        for user in session.query(User).filter(User.enable_monthly_report == True):
            report = get_monthly_report_start_end(user)
            try:
                context.bot.send_message(chat_id=user.telegram_id, text=report)
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
    dispatcher.add_handler(new_purchase_conversation_handler)
    dispatcher.add_handler(new_income_conversation_handler)
    dispatcher.add_handler(new_purchase_group_conversation_handler)
    dispatcher.add_handler(new_income_group_conversation_handler)
    dispatcher.add_handler(CommandHandler('all_incomes', get_sum_of_all_incomes_categories))
    dispatcher.add_handler(CommandHandler('all_expenses', get_sum_of_all_purchases_categories))
    dispatcher.add_handler(CommandHandler('delete_me', delete_my_telegram_id_from_telegram_bot))

    j.run_daily(daily_message, days=tuple(range(7)), time=datetime.time(hour=15, minute=00, second=00))

    j.run_monthly(monthly_feedback, datetime.time(8, 00, 00), 1)
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
