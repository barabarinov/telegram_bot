import datetime
import logging
from calendar import monthrange

from sqlalchemy import and_

from app.models import Purchase, Income

logger = logging.getLogger(__name__)


def get_monthly_report_start_end(user):
    logger.info(f'USER IS: {user}')
    now = datetime.datetime.now()
    _, days_in_previous_month = monthrange(now.year, now.month - 1)
    if now.month == 1:
        start = datetime.datetime(now.year - 1, month=12, day=1, hour=00, minute=00, second=00)
        end = datetime.datetime(now.year - 1, month=12, day=31, hour=23, minute=59, second=59)
    else:
        start = datetime.datetime(now.year, now.month - 1, 1)
        end = datetime.datetime(now.year, now.month - 1, days_in_previous_month)

    return get_all_purchases_all_incomes_of_month(user, start, end)


def get_all_purchases_all_incomes_of_month(user, start, end):
    logger.info(f' USER START END {user} {start} {end}')
    your_total_purchase = sum(purchase.spent_money for purchase in user.purchases.filter(
        and_(Purchase.creation_date >= start, Purchase.creation_date <= end)))

    your_total_income = sum(income.earned_money for income in user.incomes.filter(
        and_(Income.creation_date >= start, Income.creation_date <= end)))
    logger.info('TIS')

    return f'Your monthly purchase: ₴ {round(your_total_purchase, 2)}\n' \
           f'Your monthly income: ₴ {round(your_total_income, 2)}'
