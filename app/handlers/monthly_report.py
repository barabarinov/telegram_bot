import datetime
import logging

logger = logging.getLogger(__name__)


def get_monthly_report_of_purchases_incomes(user):
    your_total_purchase = sum(purchase.spent_money for purchase in user.purchases.filter(
        user.purchases.creation_date == datetime.datetime.day))
    your_total_income = sum(income.earned_money for income in user.incomes.filter(
        user.incomes.creation_date == datetime.datetime.day))
    return f'Your monthly purchase: ₴{your_total_purchase}\n' \
           f'Your monthly income: ₴{your_total_income}'
