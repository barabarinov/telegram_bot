import datetime
import logging
from calendar import monthrange
from typing import Tuple

from telegram.ext import CallbackContext

from app.db import Session
from app.message import Message
from app.handlers.reports.report_expenses_categories import build_expense_report_message
from app.handlers.reports.report_income_categories import build_income_report_message
from app.models import User
from app.translate import (
    MONTHLY_INCOME_TITLE,
    MONTHLY_EXPENSES_TITLE,
    JANUARY,
    FABRUARY,
    MARCH,
    APRIL,
    MAY,
    JUNE,
    JULY,
    AUGUST,
    SEPTEMBER,
    OCTOBER,
    NOVEMBER,
    DECEMBER,
)

logger = logging.getLogger(__name__)


def get_title(message: Message, last_month: int, title: str) -> Message:
    month_list = {
        1: JANUARY,
        2: FABRUARY,
        3: MARCH,
        4: APRIL,
        5: MAY,
        6: JUNE,
        7: JULY,
        8: AUGUST,
        9: SEPTEMBER,
        10: OCTOBER,
        11: NOVEMBER,
        0: DECEMBER,
    }

    message.add_title(title, month_list[last_month]).add_newline()

    return message


def get_previous_month_borders() -> Tuple[datetime.datetime, datetime.datetime, int]:
    now = datetime.datetime.now()

    if now.month == 1:
        start = datetime.datetime(
            now.year - 1, month=12, day=1, hour=0, minute=0, second=0
        )
        end = datetime.datetime(
            now.year - 1, month=12, day=31, hour=23, minute=59, second=59
        )
        return start, end, now.month - 1

    thing, days_in_previous_month = monthrange(now.year, now.month - 1)
    start = datetime.datetime(
        now.year, now.month - 1, day=1, hour=0, minute=0, second=0
    )
    end = datetime.datetime(
        now.year,
        now.month - 1,
        day=days_in_previous_month,
        hour=23,
        minute=59,
        second=59,
    )

    return start, end, now.month - 1


def job_monthly_feedback(context: CallbackContext):
    with Session() as session:
        start, end, last_month = get_previous_month_borders()
        for user in session.query(User).filter(User.enable_monthly_report == True):
            expense_message = Message(context=context, language=user.lang)
            expense_message = get_title(expense_message, last_month, MONTHLY_EXPENSES_TITLE)
            expense_message = build_expense_report_message(start, end, expense_message, user)
            expense_message.send_message(user)

            income_message = Message(context=context, language=user.lang)
            income_message = get_title(income_message, last_month, MONTHLY_INCOME_TITLE)
            income_message = build_income_report_message(start, end, income_message, user)
            income_message.send_message(user)
