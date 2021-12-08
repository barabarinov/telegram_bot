import datetime
import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, CallbackContext
from telegram.ext import Updater
from db import Session

from handlers.purchases import new_purchase_conversation_handler
from handlers.incomes import new_income_conversation_handler
from handlers.new_purchase_group import new_purchase_group_conversation_handler
from handlers.new_income_group import new_income_group_conversation_handler
from handlers.registration import register_user_handler
from handlers.report_of_all_incomes_categories import get_sum_of_all_incomes_categories
from handlers.report_of_all_purchase_categories import get_sum_of_all_purchases_categories
from handlers.monthly_report import get_monthly_report_of_purchases_incomes
from models import User

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)


def monthly_feedback(context: CallbackContext):
    with Session() as session:
        for user in session.query(User).filter(User.enable_monthly_report == True):
            report = get_monthly_report_of_purchases_incomes(user)
            context.bot.send_message(
                chat_id=user.telegram_id, text=report)


def main(token):
    updater = Updater(token=token, use_context=True)
    # j = updater.job_queue
    # j.run_once(monthly_feedback, 2)
    # j.run_monthly(monthly_feedback, datetime.time(22, 34, 00), 6)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', register_user_handler))
    dispatcher.add_handler(new_purchase_conversation_handler)
    dispatcher.add_handler(new_income_conversation_handler)
    dispatcher.add_handler(new_purchase_group_conversation_handler)
    dispatcher.add_handler(new_income_group_conversation_handler)
    dispatcher.add_handler(CommandHandler('all_incomes', get_sum_of_all_incomes_categories))
    dispatcher.add_handler(CommandHandler('all_purchases', get_sum_of_all_purchases_categories))
    # dispatcher.add_handler(new_group_single)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    load_dotenv()
    main(os.getenv('TOKEN'))
