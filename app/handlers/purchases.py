import datetime
import logging
from enum import auto, IntEnum

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import ConversationHandler

from models import User, Purchase, Group
from db import Session

logger = logging.getLogger(__name__)


class NewPurchase(IntEnum):
    TITLE = auto()
    SPENT_MONEY = auto()
    CREATION_DATE = auto()
    CHOOSE_GROUP = auto()
    CONFIRM = auto()


def new_purchase(update: Update, context: CallbackContext):
    reply_keyboard = [['/cancel']]
    update.message.reply_text('Enter your purchase title:', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewPurchase.TITLE


def get_purchase_title(update: Update, context: CallbackContext):
    context.user_data['title'] = update.message.text

    reply_keyboard = [['/cancel']]

    update.message.reply_text('How much did you spend?:', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewPurchase.SPENT_MONEY


def get_purchase_spent_money(update: Update, context: CallbackContext):
    logger.info(f"SPENT MONEY TEXT: {update.message.text}")
    try:
        context.user_data['spent_money'] = float(update.message.text.replace(' ', ''))
    except ValueError:
        return ConversationHandler.END
    logger.info(f"SPENT MONEY: {context.user_data['spent_money']}")

    with Session() as session:
        user = session.query(User).get(update.effective_user.id)

        update.message.reply_text(
            'Select group',
            reply_markup=InlineKeyboardMarkup.from_column([
                InlineKeyboardButton(text=group.name, callback_data=f'set-group${group.id}') for group in user.groups
            ]),
        )

    return NewPurchase.CHOOSE_GROUP


def get_group_callback(update: Update, context: CallbackContext):
    update.callback_query.answer()

    _, group_id = update.callback_query.data.split('$')
    group_id = int(group_id)
    context.user_data['group_id'] = group_id
    with Session() as session:
        group = session.query(Group).get(group_id)

    purchase = Purchase(
        title=context.user_data['title'],
        spent_money=context.user_data['spent_money'],
        creation_date=datetime.datetime.now(),
        group_id=group_id,
        group=group,
    )
    reply_keyboard = [['SAVE', 'DON\'T SAVE']]
    update.effective_message.reply_text(
        f'That\'s your purchase!\n{purchase.display_purchase()}', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Save/Don\'t save?'
        ))

    return NewPurchase.CONFIRM


def create_purchase(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_purchase = Purchase(
            user_id=update.effective_user.id,
            title=context.user_data['title'],
            spent_money=context.user_data['spent_money'],
            group_id=context.user_data['group_id'],
        )
        session.add(user_new_purchase)
        session.commit()
    update.message.reply_text('Your purchase has been added!')

    return ConversationHandler.END


def cancel_creation_purchase(update: Update, context: CallbackContext):
    update.message.reply_text('See ya!')

    return ConversationHandler.END


new_purchase_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('new_purchase', new_purchase)],
    states={
        NewPurchase.TITLE: [MessageHandler(Filters.text & ~Filters.command, get_purchase_title)],
        NewPurchase.SPENT_MONEY: [MessageHandler(Filters.text & ~Filters.command, get_purchase_spent_money)],
        NewPurchase.CHOOSE_GROUP: [CallbackQueryHandler(get_group_callback, pattern='^set-group', )],
        NewPurchase.CONFIRM: [
            MessageHandler(Filters.regex('^(SAVE)$') & ~Filters.command, create_purchase),
            MessageHandler(Filters.regex('^(DON\'T SAVE)$') & ~Filters.command, cancel_creation_purchase),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_creation_purchase),
    ],
)
