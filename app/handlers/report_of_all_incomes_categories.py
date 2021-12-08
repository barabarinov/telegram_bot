import datetime
import logging

from telegram import Update
from telegram.ext import CallbackContext

from db import Session
from models import User
from sqlalchemy import and_

logger = logging.getLogger(__name__)


def current_report_of_all_incomes():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, 1)
    end = datetime.datetime(now.year, now.month, now.day)
    return start, end


def get_sum_of_all_incomes_categories(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        start, end = current_report_of_all_incomes()
        for group in user.groups_incomes:
            logger.info(f'HERE IS GROUP {group.name}')
            result = sum(income.earned_money for income in group.incomes.filter(
                         and_(income.creation_date >= start, income.creation_date <= end))
                         )
            update.message.reply_text(f'Sum of incomes in categorie {group.name}: ₴{result}')
        overall_result = sum(income.earned_money for income in user.incomes.filter(
                            and_(user.incomes.creation_date >= start, user.incomes.creation_date <= end))
                             )
        update.message.reply_text(f'Total: ₴{overall_result}')
