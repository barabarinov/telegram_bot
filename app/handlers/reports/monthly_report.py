import datetime
import logging
from calendar import monthrange

from sqlalchemy import and_

from telegram import ParseMode
from app.models import Purchase, Income
from app.translate import (
    gettext as _,
    MONTHLY_INCOME,
    MONTHLY_EXPENSE,
)

logger = logging.getLogger(__name__)


def get_monthly_report_start_end(user):
    logger.info(f'USER IS: {user}')
    now = datetime.datetime.now()
    _, days_in_previous_month = monthrange(now.year, now.month - 1)
    logger.info(f'>>>>>>>NOW.MONTH = {days_in_previous_month}<<<<<<<<<<')
    if now.month == 1:
        start = datetime.datetime(now.year - 1, month=12, day=1, hour=00, minute=00, second=00)
        end = datetime.datetime(now.year - 1, month=12, day=31, hour=23, minute=59, second=59)
    else:
        start = datetime.datetime(now.year, now.month - 1, day=1, hour=00, minute=00, second=00)
        end = datetime.datetime(now.year, now.month - 1, day=days_in_previous_month, hour=23, minute=59, second=59)

    return get_all_purchases_all_incomes_of_month(user, start, end)


def get_all_purchases_all_incomes_of_month(user, start, end):
    logger.info(f' USER START END {user} {start} {end}')
    your_total_purchase = sum(purchase.spent_money for purchase in user.purchases.filter(
        and_(Purchase.creation_date >= start, Purchase.creation_date <= end)))

    your_total_income = sum(income.earned_money for income in user.incomes.filter(
        and_(Income.creation_date >= start, Income.creation_date <= end)))

    return _(MONTHLY_INCOME, user.lang, round(your_total_income, 0)) + '\n' \
           + _(MONTHLY_EXPENSE, user.lang, round(your_total_purchase, 0))
