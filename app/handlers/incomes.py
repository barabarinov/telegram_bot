import datetime
import pytz
import logging
from enum import auto, IntEnum

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import ConversationHandler
from app.handlers.find_user_lang_or_id import find_user_lang
from app.handlers.expenses import CANCEL, CALLBACK_SAVE

from app.db import Session
from app.buttons import reply_keyboard_cancel
from app.models import User, Income, GroupIncome
from app.translate import (
    gettext as _,
    INCOME_TITLE,
    HOW_MUCH_EARN,
    SELECT_CATEGORY,
    SAVE,
    DONT_SAVE,
    THATS_YOUR_INCOME,
    INCOME_ADDED,
    SEEYA,
    CANCEL_THIS,
    WRONG_VALUE,
)

logger = logging.getLogger(__name__)


class NewIncome(IntEnum):
    TITLE = auto()
    EARNED_MONEY = auto()
    CHOOSE_CATEGORY = auto()
    CONFIRM = auto()


def new_income(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=_(INCOME_TITLE, find_user_lang(update)),
        reply_markup=reply_keyboard_cancel(update, context, CANCEL),
        parse_mode=ParseMode.MARKDOWN,
    )

    return NewIncome.TITLE


def get_income_title(update: Update, context: CallbackContext):
    context.user_data['title'] = update.message.text
    logger.info(f'context.user_data >>>>>> {context.user_data} <<<<<<')
    update.message.reply_text(
        text=_(HOW_MUCH_EARN, find_user_lang(update)),
        reply_markup=reply_keyboard_cancel(update, context, CANCEL),
        parse_mode=ParseMode.MARKDOWN,
    )

    return NewIncome.EARNED_MONEY


def get_income_earned_money(update: Update, context: CallbackContext):
    try:
        context.user_data['earned_money'] = float(update.message.text.replace(' ', ''))
    except ValueError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=_(WRONG_VALUE, find_user_lang(update)),
            reply_markup=reply_keyboard_cancel(update, context, CANCEL)
        )

        return NewIncome.EARNED_MONEY

    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        update.message.reply_text(
            text=_(SELECT_CATEGORY, user.lang),
            reply_markup=InlineKeyboardMarkup.from_column([
                InlineKeyboardButton(
                    text=group.name,
                    callback_data=f'set-income-category${group.id}') for group in user.groups_incomes
            ] + [InlineKeyboardButton(_(CANCEL_THIS, find_user_lang(update)), callback_data=CANCEL)]),
        )

        return NewIncome.CHOOSE_CATEGORY


def get_income_category_callback(update: Update, context: CallbackContext):
    update.callback_query.answer()

    _other, group_id = update.callback_query.data.split('$')
    group_id = int(group_id)
    context.user_data['group_id'] = group_id
    with Session() as session:
        category = session.query(GroupIncome).get(group_id)

    income = Income(
        title=context.user_data['title'],
        earned_money=context.user_data['earned_money'],
        creation_date=datetime.datetime.now(tz=pytz.timezone('Europe/Kiev')),
        group=category,  # тут вместо category было group
    )

    reply_keyboard_save = [[InlineKeyboardButton(_(SAVE, find_user_lang(update)), callback_data=CALLBACK_SAVE),
                            InlineKeyboardButton(_(DONT_SAVE, find_user_lang(update)), callback_data=CANCEL)]]

    reply_keyboard_save_dontsave = InlineKeyboardMarkup(reply_keyboard_save)

    update.effective_message.reply_text(
        _(THATS_YOUR_INCOME, find_user_lang(update), income.display_income(find_user_lang(update))),
        reply_markup=reply_keyboard_save_dontsave,
        parse_mode=ParseMode.MARKDOWN
    )

    return NewIncome.CONFIRM


def create_income(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_income = Income(
            user_id=update.effective_user.id,
            title=context.user_data['title'],
            earned_money=context.user_data['earned_money'],
            group_id=context.user_data['group_id'],
            creation_date=datetime.datetime.now(tz=pytz.UTC),
        )
        logger.info(f'UTC >>> {datetime.datetime.now(tz=pytz.UTC)}')
        session.add(user_new_income)
        session.commit()

        query = update.callback_query
        query.answer()

    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=(_(INCOME_ADDED, find_user_lang(update))),
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationHandler.END


def cancel_creation_income(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=_(SEEYA, find_user_lang(update)),
    )

    return ConversationHandler.END


new_income_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(
        Filters.regex('^🟩 Create new income|🟩 Додати дохід|🟩 Внести доход$') & ~Filters.command, new_income)],
    states={
        NewIncome.TITLE: [MessageHandler(Filters.text & ~Filters.command, get_income_title)],
        NewIncome.EARNED_MONEY: [MessageHandler(Filters.text & ~Filters.command, get_income_earned_money)],
        NewIncome.CHOOSE_CATEGORY: [
            CallbackQueryHandler(get_income_category_callback, pattern='^set-income-category'),
            CallbackQueryHandler(cancel_creation_income, pattern=CANCEL),
        ],
        NewIncome.CONFIRM: [
            CallbackQueryHandler(create_income, pattern=CALLBACK_SAVE),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(cancel_creation_income, pattern=CANCEL),
    ],
)
