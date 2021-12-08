import datetime
import logging
from calendar import monthrange
from sqlalchemy import and_

logger = logging.getLogger(__name__)


def get_monthly_report_of_purchases_incomes(user):
    now = datetime.datetime.now()
    _, days_in_month = monthrange(now.year, now.month - 1)
    start = datetime.datetime(now.year, now.month - 1, 1)
    end = datetime.datetime(now.year, now.month - 1, days_in_month)
    return get_all_purchases_all_incomes_of_month(user, start, end)


def get_all_purchases_all_incomes_of_month(user, start, end):
    your_total_purchase = sum(purchase.spent_money for purchase in user.purchases.filter(
        and_(user.purchases.creation_date >= start, user.purchases.creation_date <= end)))

    your_total_income = sum(income.earned_money for income in user.incomes.filter(
        and_(user.incomes.creation_date >= start, user.incomes.creation_date <= end)))

    return f'Your monthly purchase: ₴{your_total_purchase}\n' \
           f'Your monthly income: ₴{your_total_income}'
