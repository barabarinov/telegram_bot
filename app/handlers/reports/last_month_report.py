from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.handlers.get_user import get_effective_user
from app.message import Message
from app.handlers.reports.monthly_report import get_previous_month_borders, get_title
from app.handlers.reports.report_expenses_categories import build_expense_report_message
from app.handlers.reports.report_income_categories import build_income_report_message
from app.translate import MONTHLY_EXPENSES_TITLE, MONTHLY_INCOME_TITLE


def previous_month_feedback(update: Update, context: CallbackContext) -> None:
    with Session() as session:
        start, end, last_month = get_previous_month_borders()
        user = get_effective_user(update, session)

        expense_message = Message(update=update, language=user.lang)
        expense_message = get_title(expense_message, last_month, MONTHLY_EXPENSES_TITLE)
        expense_message = build_expense_report_message(start, end, expense_message, user)
        expense_message.reply()

        income_message = Message(update=update, language=user.lang)
        income_message = get_title(income_message, last_month, MONTHLY_INCOME_TITLE)
        income_message = build_income_report_message(start, end, income_message, user)
        income_message.reply()
