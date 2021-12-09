import datetime

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
from app.db import Session
from app.models import User


def monthly_feedback(context: CallbackContext):
    with Session() as session:
        for user in session.query(User).filter(User.enable_monthly_report == True):
            report = get_monthly_report_start_end(user)
            context.bot.send_message(
                chat_id=user.telegram_id, text=report)


def run(token):
    updater = Updater(token=token, use_context=True)
    j = updater.job_queue
    j.run_monthly(monthly_feedback, datetime.time(8, 00, 00), 1)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', register_user_handler))
    dispatcher.add_handler(new_purchase_conversation_handler)
    dispatcher.add_handler(new_income_conversation_handler)
    dispatcher.add_handler(new_purchase_group_conversation_handler)
    dispatcher.add_handler(new_income_group_conversation_handler)
    dispatcher.add_handler(CommandHandler('all_incomes', get_sum_of_all_incomes_categories))
    dispatcher.add_handler(CommandHandler('all_purchases', get_sum_of_all_purchases_categories))

    updater.start_polling()
    updater.idle()
