import datetime
from typing import Tuple

from sqlalchemy import and_
from telegram import Update
from telegram.ext import CallbackContext

from app.datatime_to_europekyiv import get_kyiv_timezone
from app.db import Session
from app.handlers.get_user import get_effective_user
from app.message import (
    Message,
    escape,
    bold,
    italic,
    underscore
)
from app.models import Purchase, User
from app.translate import (
    REPORT_EXPENSE_TITLE,
    SIGN,
    TOTAL,
    OVERALL,
)

EUROPEKIEV = "Europe/Kiev"
FMT = "%H:%M    %d/%m/%Y"


def get_current_month_borders() -> Tuple[datetime.datetime, datetime.datetime]:
    now = datetime.datetime.now()
    start = datetime.datetime(
        now.year, now.month, day=1, hour=0, minute=0, second=0
    )
    end = datetime.datetime(
        now.year, now.month, now.day, hour=23, minute=59, second=59
    )
    return start, end


def build_expense_report_message(start: datetime.datetime,
                                 end: datetime.datetime,
                                 message: Message,
                                 user: User.groups_purchases) -> Message:
    total_spent = 0
    for group in user.groups_purchases:
        message.add_line("{}:", group.name, formatters=[bold])

        group_total_spent = 0
        for purchase in group.purchases.filter(
                and_(Purchase.creation_date >= start, Purchase.creation_date <= end)).order_by(Purchase.creation_date):
            message.add_line(
                "{}: {} {}    {}",
                escape(purchase.title),
                SIGN,
                round(purchase.spent_money),
                get_kyiv_timezone(purchase.creation_date, EUROPEKIEV, FMT),
                formatters=[italic],
            )
            group_total_spent += purchase.spent_money
        total_spent += group_total_spent

        message.add_line(
            "{}: {} {}", TOTAL, SIGN, round(group_total_spent), formatters=[underscore],
        ).add_newline()
    message.add_line(
        "{}: {} {}", OVERALL, SIGN, round(total_spent), formatters=[bold],
    )
    return message


def current_expenses_report(update: Update, context: CallbackContext) -> None:
    with Session() as session:
        start, end = get_current_month_borders()
        user = get_effective_user(update, session)

        message = Message(update=update, language=user.lang)
        message.add_title(REPORT_EXPENSE_TITLE).add_newline()
        message = build_expense_report_message(start=start, end=end, message=message, user=user)
        message.reply()
