import logging

from sqlalchemy import and_

import telegram.error
from telegram import ParseMode, Update
from telegram.ext import CallbackContext
from app.db import Session
from app.models import Purchase, Income, User
from app.datatime_to_europekyiv import get_kyiv_timezone
from app.handlers.reports.monthly_report import get_monthly_report_start_end, month_name
from app.handlers.reports.report_of_all_expenses_categories import (
    CHARACTERS,
    NEW_LINE,
    SLASH,
    EUROPEKIEV,
    FMT,
)

from app.translate import (
    gettext as _,
    YOUR_MONTHLY_INCOME,
    YOUR_MONTHLY_EXPENSES,
    OVER_ALL_EXPENSES,
    OVER_ALL_INCOMES,
    TOTAL,
    SIGN,
)

logger = logging.getLogger(__name__)


def last_month_report(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)

        start, end, last_month = get_monthly_report_start_end(user)
        
        try:
            context.bot.send_message(
                chat_id=user.telegram_id,
                text=(_(YOUR_MONTHLY_EXPENSES, user.lang, month_name(user, last_month))),
                parse_mode=ParseMode.MARKDOWN,
            )
        except telegram.error.Unauthorized:
            logger.info(f'User {user.username} {user.telegram_id} blocked')
        else:
            logger.info(f'User {user.username} {user.telegram_id} sent message')

        try:
            for group in user.groups_purchases:
                details = (
                    f'_{"".join([SLASH + i if i in CHARACTERS else i for i in purchase.title])}_: '
                    f'_{_(SIGN, user.lang)}_ _{round(purchase.spent_money, 0)}_    '
                    f'_{get_kyiv_timezone(purchase.creation_date, EUROPEKIEV, FMT)}_'
                    for purchase in group.purchases.filter(
                        and_(Purchase.creation_date >= start, Purchase.creation_date <= end)
                    )
                )
                result = sum(purchase.spent_money for purchase in group.purchases.filter(
                    and_(Purchase.creation_date >= start, Purchase.creation_date <= end)))

                context.bot.send_message(
                    chat_id=user.telegram_id,
                    text=f'*{group.name}*:\n{NEW_LINE.join(details)}\n{_(TOTAL, user.lang, round(result, 0))}',
                    parse_mode=ParseMode.MARKDOWN_V2,
                )

            overall_result = sum(purchase.spent_money for purchase in user.purchases.filter(
                and_(Purchase.creation_date >= start, Purchase.creation_date <= end)))

            context.bot.send_message(
                chat_id=user.telegram_id,
                text=_(OVER_ALL_EXPENSES, user.lang, round(overall_result, 0)),
                parse_mode=ParseMode.MARKDOWN,
            )
        except telegram.error.Unauthorized:
            logger.info(f'User {user.username} {user.telegram_id} blocked')
        else:
            logger.info(f'User {user.username} {user.telegram_id} sent message')

        try:
            context.bot.send_message(
                chat_id=user.telegram_id,
                text=(_(YOUR_MONTHLY_INCOME, user.lang, month_name(user, last_month))),
                parse_mode=ParseMode.MARKDOWN,
            )
        except telegram.error.Unauthorized:
            logger.info(f'User {user.username} {user.telegram_id} blocked')
        else:
            logger.info(f'User {user.username} {user.telegram_id} sent message')

        try:
            for group in user.groups_incomes:
                details = (
                    f'_{"".join([SLASH + i if i in CHARACTERS else i for i in income.title])}_: '
                    f'_{_(SIGN, user.lang)}_ _{round(income.earned_money, 0)}_    '
                    f'_{get_kyiv_timezone(income.creation_date, EUROPEKIEV, FMT)}_'
                    for income in group.incomes.filter(
                        and_(Income.creation_date >= start, Income.creation_date <= end)
                    )
                )
                result = sum(income.earned_money for income in group.incomes.filter(
                    and_(Income.creation_date >= start, Income.creation_date <= end)))

                context.bot.send_message(
                    chat_id=user.telegram_id,
                    text=f'*{group.name}*:\n{NEW_LINE.join(details)}\n{_(TOTAL, user.lang, round(result, 0))}',
                    parse_mode=ParseMode.MARKDOWN_V2,
                )

            overall_result = sum(income.earned_money for income in user.incomes.filter(
                and_(Income.creation_date >= start, Income.creation_date <= end)))

            context.bot.send_message(
                chat_id=user.telegram_id,
                text=_(OVER_ALL_INCOMES, user.lang, round(overall_result, 0)),
                parse_mode=ParseMode.MARKDOWN,
            )

        except telegram.error.Unauthorized:
            logger.info(f'User {user.username} {user.telegram_id} blocked')
        else:
            logger.info(f'User {user.username} {user.telegram_id} sent message')
