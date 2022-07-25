import datetime
import pytz
import logging
from enum import auto, IntEnum

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import ConversationHandler
from app.handlers.find_user_lang_or_id import find_user_lang

from app.db import Session
from app.buttons import reply_keyboard_cancel
from app.models import User, Purchase, GroupPurchase
from app.handlers.reports.report_of_all_expenses_categories import EUROPEKIEV
from app.translate import (
    gettext as _,
    EXPENSE_TITLE,
    HOW_MUCH_SPEND,
    SELECT_CATEGORY,
    SAVE,
    DONT_SAVE,
    THATS_YOUR_EXPENSE,
    EXPENSE_ADDED,
    SEEYA,
    CANCEL_THIS,
    WRONG_VALUE,
)

CANCEL = 'cancel'
CALLBACK_SAVE = 'save'

logger = logging.getLogger(__name__)


class NewExpense(IntEnum):
    TITLE = auto()
    SPENT_MONEY = auto()
    CHOOSE_CATEGORY = auto()
    CONFIRM = auto()


def new_expense(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=_(EXPENSE_TITLE, find_user_lang(update)),
        reply_markup=reply_keyboard_cancel(update, context, CANCEL),
        parse_mode=ParseMode.MARKDOWN
    )

    return NewExpense.TITLE


def get_expense_title(update: Update, context: CallbackContext):
    context.user_data['title'] = update.message.text
    logger.info(f'context.user_data >>>>>> {context.user_data} <<<<<<')

    update.message.reply_text(
        text=(_(HOW_MUCH_SPEND, find_user_lang(update))),
        reply_markup=reply_keyboard_cancel(update, context, CANCEL),
        parse_mode=ParseMode.MARKDOWN,
    )

    return NewExpense.SPENT_MONEY


def get_expense_spent_money(update: Update, context: CallbackContext):
    try:
        context.user_data['spent_money'] = float(update.message.text.replace(' ', ''))
        logger.info(f'SPENT_MONEY >>> {context.user_data["spent_money"]}')
    except ValueError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=_(WRONG_VALUE, find_user_lang(update)),
            reply_markup=reply_keyboard_cancel(update, context, CANCEL)
        )

        return NewExpense.SPENT_MONEY

    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        update.message.reply_text(
            text=(_(SELECT_CATEGORY, user.lang)),
            reply_markup=InlineKeyboardMarkup.from_column([
                InlineKeyboardButton(
                    text=group.name,
                    callback_data=f'set-expense-category${group.id}') for group in user.groups_purchases
            ] + [InlineKeyboardButton(_(CANCEL_THIS, user.lang), callback_data=CANCEL)]),
        )

    return NewExpense.CHOOSE_CATEGORY


def get_expense_category_callback(update: Update, context: CallbackContext):
    update.callback_query.answer()

    _another, group_id = update.callback_query.data.split('$')
    group_id = int(group_id)
    context.user_data['group_id'] = group_id
    with Session() as session:
        category = session.query(GroupPurchase).get(group_id)

    purchase = Purchase(
        title=context.user_data['title'],
        spent_money=context.user_data['spent_money'],
        creation_date=datetime.datetime.now(tz=pytz.timezone(EUROPEKIEV)),
        group=category,  # тут вместо category было group
    )
    reply_keyboard_save = [[InlineKeyboardButton(_(SAVE, find_user_lang(update)), callback_data=CALLBACK_SAVE),
                            InlineKeyboardButton(_(DONT_SAVE, find_user_lang(update)), callback_data=CANCEL)]]

    reply_keyboard_save_dontsave = InlineKeyboardMarkup(reply_keyboard_save)

    update.effective_message.reply_text(
        _(THATS_YOUR_EXPENSE, find_user_lang(update), purchase.display_expense(find_user_lang(update))),
        reply_markup=reply_keyboard_save_dontsave,
        parse_mode=ParseMode.MARKDOWN
    )

    return NewExpense.CONFIRM


def create_expense(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_purchase = Purchase(
            user_id=update.effective_user.id,
            title=context.user_data['title'],
            spent_money=context.user_data['spent_money'],
            group_id=context.user_data['group_id'],
            creation_date=datetime.datetime.utcnow(),
        )

        logger.info(f'UTCNOW >>> {datetime.datetime.now(tz=pytz.UTC)}')
        session.add(user_new_purchase)
        session.commit()

    query = update.callback_query
    query.answer()

    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=(_(EXPENSE_ADDED, find_user_lang(update))),
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationHandler.END


def cancel_creation_expense(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=_(SEEYA, find_user_lang(update)),
    )

    return ConversationHandler.END


new_expense_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(
        Filters.regex(
            '^🟥 Create new expense|🟥 Додати витрату|🟥 Внести расход$') & ~Filters.command, new_expense)],
    states={
        NewExpense.TITLE: [MessageHandler(Filters.text & ~Filters.command, get_expense_title)],
        NewExpense.SPENT_MONEY: [MessageHandler(Filters.text & ~Filters.command, get_expense_spent_money)],
        NewExpense.CHOOSE_CATEGORY: [
            CallbackQueryHandler(get_expense_category_callback, pattern='^set-expense-category')],
        NewExpense.CONFIRM: [
            CallbackQueryHandler(create_expense, pattern=CALLBACK_SAVE),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(cancel_creation_expense, pattern=CANCEL)
    ],
)
