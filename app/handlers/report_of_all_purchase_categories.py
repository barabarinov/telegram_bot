import datetime
import logging

from sqlalchemy import and_
from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User, Purchase

logger = logging.getLogger(__name__)


def get_start_end_of_current_report_of_all_purchases():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, 1, hour=00, minute=00, second=00)
    end = datetime.datetime(now.year, now.month, now.day, hour=23, minute=59, second=59)
    return start, end


def get_sum_of_all_purchases_categories(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        start, end = get_start_end_of_current_report_of_all_purchases()
        update.message.reply_text('Sum of expenses in categories:')

        for group in user.groups_purchases:
            result = sum(purchase.spent_money for purchase in group.purchases.filter(
                        and_(Purchase.creation_date >= start, Purchase.creation_date <= end))
                        )
            update.message.reply_text(f'{group.name}: ₴ {round(result, 2)}')
        overall_result = sum(purchase.spent_money for purchase in user.purchases.filter(
                            and_(Purchase.creation_date >= start, Purchase.creation_date <= end))
                            )
        update.message.reply_text(f'Total: ₴ {round(overall_result, 2)}')
