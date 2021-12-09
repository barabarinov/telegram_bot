import datetime
import logging

from sqlalchemy import and_
from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User, Income

logger = logging.getLogger(__name__)


def get_start_end_of_current_report_of_all_incomes():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, 1)
    end = datetime.datetime(now.year, now.month, now.day)
    return start, end


def get_sum_of_all_incomes_categories(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        start, end = get_start_end_of_current_report_of_all_incomes()
        update.message.reply_text('Sum of incomes in categories:')

        for group in user.groups_incomes:
            result = sum(income.earned_money for income in group.incomes.filter(
                         and_(Income.creation_date >= start, Income.creation_date <= end))
                         )
            update.message.reply_text(f'{group.name}: ₴ {round(result, 2)}')
        overall_result = sum(income.earned_money for income in user.incomes.filter(
                            and_(Income.creation_date >= start, Income.creation_date <= end))
                             )
        update.message.reply_text(f'Total: ₴ {round(overall_result, 2)}')
