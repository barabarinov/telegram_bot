import datetime
import logging

from sqlalchemy import and_
from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User, Income
from app.handlers.find_user_lang_or_id import find_user_lang
from app.translate import (
    gettext as _,
    REPORT_INCOME_CATEGORIES,
    TOTAL,
    SIGN,
    OVER_ALL,

)

logger = logging.getLogger(__name__)


def get_start_end_of_current_report_of_all_incomes():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, 1, hour=00, minute=00, second=00)
    end = datetime.datetime(now.year, now.month, now.day, hour=23, minute=59, second=59)
    return start, end


def get_sum_of_all_incomes_categories(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        start, end = get_start_end_of_current_report_of_all_incomes()
        update.message.reply_text(_(REPORT_INCOME_CATEGORIES, user.lang))

        for group in user.groups_incomes:
            details = (f'{income.title}: {_(SIGN, user.lang)} {round(income.earned_money,0)}    {income.creation_date.strftime("%H:%M    %d/%m/%Y")}' for income in group.incomes.filter(
                and_(Income.creation_date >= start, Income.creation_date <= end))
            )
            result = sum(income.earned_money for income in group.incomes.filter(
                         and_(Income.creation_date >= start, Income.creation_date <= end))
                         )
            update.message.reply_text(f'{group.name}:\n' + '\n'.join(details) + '\n' + _(TOTAL, user.lang, round(result, 0)))

        overall_result = sum(income.earned_money for income in user.incomes.filter(
                            and_(Income.creation_date >= start, Income.creation_date <= end))
                             )
        update.message.reply_text(_(OVER_ALL, user.lang, round(overall_result, 0)))
