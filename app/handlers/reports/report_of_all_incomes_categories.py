import datetime
import logging

from sqlalchemy import and_
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from app.db import Session
from app.datatime_to_europekyiv import get_kyiv_timezone
from app.handlers.reports.report_of_all_expenses_categories import (
    CHARACTERS,
    SLASH,
    NEW_LINE,
    EUROPEKIEV,
    FMT,
)

from app.models import User, Income
from app.translate import (
    gettext as _,
    REPORT_INCOME_CATEGORIES,
    TOTAL,
    SIGN,
    OVER_ALL_INCOMES,
)

logger = logging.getLogger(__name__)


def get_start_end_of_current_report_of_all_incomes():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, day=1, hour=00, minute=00, second=00)
    end = datetime.datetime(now.year, now.month, now.day, hour=23, minute=59, second=59)
    return start, end


def get_sum_of_all_incomes_categories(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        start, end = get_start_end_of_current_report_of_all_incomes()

        update.message.reply_text(
            text=_(REPORT_INCOME_CATEGORIES, user.lang),
            parse_mode=ParseMode.MARKDOWN,
        )

        for group in user.groups_incomes:
            details = (
                f'_{"".join([SLASH + i if i in CHARACTERS else i for i in income.title])}_: '
                f"_{_(SIGN, user.lang)}_ _{round(income.earned_money)}_    "
                f"_{get_kyiv_timezone(income.creation_date, EUROPEKIEV, FMT)}_"
                for income in group.incomes.filter(
                    and_(Income.creation_date >= start, Income.creation_date <= end)
                ).order_by(Income.creation_date)
            )
            result = sum(
                income.earned_money
                for income in group.incomes.filter(
                    and_(Income.creation_date >= start, Income.creation_date <= end)
                )
            )

            update.message.reply_text(
                f"*{group.name}*:\n{NEW_LINE.join(details)}\n{_(TOTAL, user.lang, round(result))}",
                parse_mode=ParseMode.MARKDOWN_V2,
            )

        overall_result = sum(
            income.earned_money
            for income in user.incomes.filter(
                and_(Income.creation_date >= start, Income.creation_date <= end)
            )
        )
        update.message.reply_text(
            text=_(OVER_ALL_INCOMES, user.lang, round(overall_result)),
            parse_mode=ParseMode.MARKDOWN,
        )
