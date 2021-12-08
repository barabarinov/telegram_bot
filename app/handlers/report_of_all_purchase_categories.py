import datetime
import logging

from telegram import Update
from telegram.ext import CallbackContext

from db import Session
from models import User, Purchase
from sqlalchemy import and_

logger = logging.getLogger(__name__)


def current_report_of_all_purchases():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, 1)
    end = datetime.datetime(now.year, now.month, now.day)
    return start, end


def get_sum_of_all_purchases_categories(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        start, end = current_report_of_all_purchases()
        update.message.reply_text('Sum of purchases in categories:')

        for group in user.groups_purchases:
            result = sum(purchase.spent_money for purchase in group.purchases.filter(
                        and_(Purchase.creation_date >= start, Purchase.creation_date <= end))
                        )
            update.message.reply_text(f'{group.name}: ₴ {round(result, 2)}')
        overall_result = sum(purchase.spent_money for purchase in user.purchases.filter(
                            and_(Purchase.creation_date >= start, Purchase.creation_date <= end))
                            )
        update.message.reply_text(f'Total: ₴ {round(overall_result, 2)}')
