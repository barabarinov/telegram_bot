import datetime
import logging

from telegram import Update
from telegram.ext import CallbackContext

from db import Session
from models import User
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
        for group in user.groups_purchases:
            result = sum(purchase.spent_money for purchase in group.purchases.filter(
                        and_(purchase.creation_date >= start, purchase.creation_date <= end))
                        )
            update.message.reply_text(f'Sum of purchases in categorie {group.name}: ₴{result}')
        overall_result = sum(purchase.spent_money for purchase in user.purchases.filter(
                            and_(user.purchases.creation_date >= start, user.purchases.creation_date <= end))
                            )
        update.message.reply_text(f'Total: ₴{overall_result}')
