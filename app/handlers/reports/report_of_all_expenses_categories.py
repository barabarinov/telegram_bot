import datetime
import logging

from sqlalchemy import and_
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User, Purchase
from app.translate import (
    gettext as _,
    REPORT_EXPENSE_CATEGORIES,
    TOTAL,
    SIGN,
    OVER_ALL_EXPENSES,
)

logger = logging.getLogger(__name__)


def get_start_end_of_current_report_of_all_expenses():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, 1, hour=00, minute=00, second=00)
    end = datetime.datetime(now.year, now.month, now.day, hour=23, minute=59, second=59)
    return start, end


def get_sum_of_all_expenses_categories(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        start, end = get_start_end_of_current_report_of_all_expenses()
        update.message.reply_text(_(REPORT_EXPENSE_CATEGORIES, user.lang), parse_mode=ParseMode.MARKDOWN)

        for group in user.groups_purchases:
            details = (
                f'_{purchase.title}_: _{_(SIGN, user.lang)}_ _{round(purchase.spent_money, 0)}_    _{purchase.creation_date.strftime("%H:%M    %d/%m/%Y")}_'
                for purchase in group.purchases.filter(and_(Purchase.creation_date >= start, Purchase.creation_date <= end))
            )

            result = sum(purchase.spent_money for purchase in group.purchases.filter(
                and_(Purchase.creation_date >= start, Purchase.creation_date <= end))
                         )
            update.message.reply_text(
                f'*{group.name}*:\n' + '\n'.join(details) + '\n' + _(TOTAL, user.lang, round(result, 0)),
                parse_mode=ParseMode.MARKDOWN)

        overall_result = sum(purchase.spent_money for purchase in user.purchases.filter(
            and_(Purchase.creation_date >= start, Purchase.creation_date <= end))
                             )
        update.message.reply_text(_(OVER_ALL_EXPENSES, user.lang, round(overall_result, 0)), parse_mode=ParseMode.MARKDOWN)
