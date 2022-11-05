import datetime
import logging
import telegram.error
from calendar import monthrange

from sqlalchemy import and_
from app.db import Session
from telegram import ParseMode
from telegram.ext import CallbackContext
from app.models import Purchase, Income, User
from app.datatime_to_europekyiv import get_kyiv_timezone
from app.handlers.reports.report_of_all_expenses_categories import (
    CHARACTERS,
    SLASH,
    NEW_LINE,
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


def month_name(user, last_month):
    month_list = {
        1: _(JANUARY, user.lang),
        2: _(FABRUARY, user.lang),
        3: _(MARCH, user.lang),
        4: _(APRIL, user.lang),
        5: _(MAY, user.lang),
        6: _(JUNE, user.lang),
        7: _(JULY, user.lang),
        8: _(AUGUST, user.lang),
        9: _(SEPTEMBER, user.lang),
        10: _(OCTOBER, user.lang),
        11: _(NOVEMBER, user.lang),
        0: _(DECEMBER, user.lang),
    }
    return month_list[last_month]


def get_monthly_report_start_end(user):
    now = datetime.datetime.now()
    _thing, days_in_previous_month = monthrange(now.year, now.month - 1)
    if now.month == 1:
        start = datetime.datetime(
            now.year - 1, month=12, day=1, hour=00, minute=00, second=00
        )
        end = datetime.datetime(
            now.year - 1, month=12, day=31, hour=23, minute=59, second=59
        )
    else:
        start = datetime.datetime(
            now.year, now.month - 1, day=1, hour=00, minute=00, second=00
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


def monthly_feedback(context: CallbackContext):
    with Session() as session:
        for user in session.query(User).filter(User.enable_monthly_report == True):
            start, end, last_month = get_monthly_report_start_end(user)
            try:
                context.bot.send_message(
                    chat_id=user.telegram_id,
                    text=(
                        _(
                            YOUR_MONTHLY_EXPENSES,
                            user.lang,
                            month_name(user, last_month),
                        )
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
            except telegram.error.Unauthorized:
                logger.info(f'User {user.username} {user.telegram_id} blocked')
            else:
                logger.info(f'User {user.username} {user.telegram_id} sent message')

            for group in user.groups_purchases:
                details = (
                    f'_{"".join([SLASH + i if i in CHARACTERS else i for i in purchase.title])}_: '
                    f'_{_(SIGN, user.lang)}_ _{round(purchase.spent_money)}_    '
                    f'_{get_kyiv_timezone(purchase.creation_date, EUROPEKIEV, FMT)}_'
                    for purchase in group.purchases.filter(
                        and_(Purchase.creation_date >= start,
                             Purchase.creation_date <= end)
                    ).order_by(Purchase.creation_date)
                )
                result = sum(
                    purchase.spent_money
                    for purchase in group.purchases.filter(
                        and_(
                            Purchase.creation_date >= start,
                            Purchase.creation_date <= end,
                        )
                    )
                )
                try:
                    context.bot.send_message(
                        chat_id=user.telegram_id,
                        text=f'*{group.name}*:\n{NEW_LINE.join(details)}\n{_(TOTAL, user.lang, round(result))}',
                        parse_mode=ParseMode.MARKDOWN_V2,
                    )
                except telegram.error.Unauthorized:
                    logger.info(f'User {user.username} {user.telegram_id} blocked')
                else:
                    logger.info(f'User {user.username} {user.telegram_id} sent message')

                overall_result = sum(
                    purchase.spent_money
                    for purchase in user.purchases.filter(
                        and_(
                            Purchase.creation_date >= start,
                            Purchase.creation_date <= end,
                        )
                    )
                )
            try:
                context.bot.send_message(
                    chat_id=user.telegram_id,
                    text=_(OVER_ALL_EXPENSES, user.lang, round(overall_result)),
                    parse_mode=ParseMode.MARKDOWN,
                )
            except telegram.error.Unauthorized:
                logger.info(f'User {user.username} {user.telegram_id} blocked')
            else:
                logger.info(f'User {user.username} {user.telegram_id} sent message')

            try:
                context.bot.send_message(
                    chat_id=user.telegram_id,
                    text=(
                        _(YOUR_MONTHLY_INCOME, user.lang, month_name(user, last_month))
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
            except telegram.error.Unauthorized:
                logger.info(f'User {user.username} {user.telegram_id} blocked')
            else:
                logger.info(f'User {user.username} {user.telegram_id} sent message')

            for group in user.groups_incomes:
                details = (
                    f'_{"".join([SLASH + i if i in CHARACTERS else i for i in income.title])}_: '
                    f'_{_(SIGN, user.lang)}_ _{round(income.earned_money)}_    '
                    f'_{get_kyiv_timezone(income.creation_date, EUROPEKIEV, FMT)}_'
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
                try:
                    context.bot.send_message(
                        chat_id=user.telegram_id,
                        text=f'*{group.name}*:\n{NEW_LINE.join(details)}\n{_(TOTAL, user.lang, round(result))}',
                        parse_mode=ParseMode.MARKDOWN_V2,
                    )
                except telegram.error.Unauthorized:
                    logger.info(f'User {user.username} {user.telegram_id} blocked')
                else:
                    logger.info(f'User {user.username} {user.telegram_id} sent message')

                overall_result = sum(
                    income.earned_money
                    for income in user.incomes.filter(
                        and_(Income.creation_date >= start, Income.creation_date <= end)
                    )
                )
            try:
                context.bot.send_message(
                    chat_id=user.telegram_id,
                    text=_(OVER_ALL_INCOMES, user.lang, round(overall_result)),
                    parse_mode=ParseMode.MARKDOWN,
                )
            except telegram.error.Unauthorized:
                logger.info(f'User {user.username} {user.telegram_id} blocked')
            else:
                logger.info(f'User {user.username} {user.telegram_id} sent message')
