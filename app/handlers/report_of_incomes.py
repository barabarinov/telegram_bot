import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from db import Session
from models import User

logger = logging.getLogger(__name__)


def get_sum_of_all_incomes(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        result = sum(income.earned_money for income in user.incomes)

    update.message.reply_text(f'Sum of all your incomes: ₴{result}')


get_every_group_statistic = CommandHandler('all_incomes', get_sum_of_all_incomes)
