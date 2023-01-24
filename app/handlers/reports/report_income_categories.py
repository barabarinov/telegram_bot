import datetime

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
from app.handlers.reports.report_expenses_categories import (
    get_current_month_borders, EUROPEKIEV, FMT
)
from app.models import Income, User
from app.translate import (
    REPORT_INCOME_TITLE,
    SIGN,
    TOTAL,
    OVERALL,
)


def build_income_report_message(start: datetime.datetime,
                                end: datetime.datetime,
                                message: Message,
                                user: User.groups_incomes) -> Message:
    total_spent = 0
    for group in user.groups_incomes:
        message.add_line("{}:", group.name, formatters=[bold])

        group_total_spent = 0
        for income in group.incomes.filter(
                and_(Income.creation_date >= start, Income.creation_date <= end)).order_by(Income.creation_date):
            message.add_line(
                "{}: {} {}    {}",
                escape(income.title),
                SIGN,
                round(income.earned_money),
                get_kyiv_timezone(income.creation_date, EUROPEKIEV, FMT),
                formatters=[italic],
            )
            group_total_spent += income.earned_money
        total_spent += group_total_spent

        message.add_line(
            "{}: {} {}", TOTAL, SIGN, round(group_total_spent), formatters=[underscore],
        ).add_newline()
    message.add_line(
        "{}: {} {}", OVERALL, SIGN, round(total_spent), formatters=[bold],
    )
    return message


def current_income_report(update: Update, context: CallbackContext) -> None:
    with Session() as session:
        start, end = get_current_month_borders()
        user = get_effective_user(update, session)

        message = Message(update=update, language=user.lang)
        message.add_title(REPORT_INCOME_TITLE).add_newline()
        message = build_income_report_message(start=start, end=end, message=message, user=user)
        message.reply()
